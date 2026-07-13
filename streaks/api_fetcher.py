# streaks/api_fetcher.py

import re
import requests
from datetime import datetime, timedelta


class GitHubAPIClient:
    """Handles all interaction with the GitHub REST and GraphQL APIs for fetching contribution data."""

    def __init__(self, github_username: str, token: str):
        self.GITHUB_TOKEN = token
        if not self.GITHUB_TOKEN:
            raise ValueError("GH_TOKEN must be provided to initialize GitHubAPIClient.")

        # Standard headers for authentication and content negotiation
        self.headers = {
            "Authorization": f"token {self.GITHUB_TOKEN}",
            "Accept": "application/vnd.github.v3+json",
        }
        self.target_username = github_username

    def _get_date_for_since_query(self) -> str:
        """Helper to calculate the date N-days ago for API 'since' parameter."""
        # Looking back 1 year is a reasonable default window for contribution tracking.
        return (datetime.now() - timedelta(days=365)).strftime('%Y-%m-%d')

    def fetch_contribution_data(self):
        """
        Fetches all unique activity dates across the user's public repositories
        by preferring GraphQL contributions calendar and falling back to events/repos.

        Returns:
            list[str]: A list of unique date strings ('YYYY-MM-DD'). Returns empty list on failure.
        """
        # Prefer GraphQL collection which returns a consolidated contributions
        # calendar across repositories. Fall back to REST-based methods if it
        # fails or returns no data.
        try:
            gql_dates = self.fetch_contribution_data_graphql()
            if gql_dates:
                return list(sorted(set(gql_dates)))
        except Exception:
            pass

        all_dates = set()
        # We start with PushEvent as it covers most commits, but we must handle general events for completeness.
        url = f"https://api.github.com/users/{self.target_username}/events?per_page=100&since={self._get_date_for_since_query()}"
        headers = self.headers

        print(f"Starting paginated fetch of activity data from GitHub API for {self.target_username}...")

        while url:
            try:
                response = requests.get(url, headers=headers)

                # Check for rate limiting/errors first
                if response.status_code != 200:
                    print(f"\n[!] API Request Failed. Status Code: {response.status_code}")
                    if response.status_code == 403 and 'rate limit exceeded' in str(response.text):
                        print("Rate limit exceeded! Please wait or use a GitHub App token with higher limits.")
                    elif response.status_code == 401:
                        print("Authentication Failed (401). Check if GH_TOKEN is correct and has required permissions.")
                    return [] # Stop execution on API failure

                data = response.json()
                # The API returns a list of events for this endpoint. Be defensive
                # in case another shape is returned by a proxy or wrapper.
                if isinstance(data, list):
                    events = data
                elif isinstance(data, dict):
                    # some APIs/layers may wrap results under 'events' or 'items'
                    events = data.get('events') or data.get('items') or []
                else:
                    events = []

                if not events:
                    break

                # Process fetched events/commits
                for event in events:
                    # Only consider PushEvent (commits/pushes)
                    if isinstance(event, dict) and event.get('type') != 'PushEvent':
                        continue
                    # Events returned by the events API are dicts with 'created_at'
                    created_at = event.get('created_at') if isinstance(event, dict) else None
                    if created_at:
                        try:
                            # Standardize date format by stripping Z and appending UTC offset (+00:00)
                            date_obj = datetime.fromisoformat(created_at.replace('Z', '+00:00'))
                            formatted_date = date_obj.strftime('%Y-%m-%d')
                            all_dates.add(formatted_date)
                        except ValueError as e:
                            print(f"Warning: Could not parse date '{created_at}'. Error: {e}")

                # Handle pagination: Check for the 'next' link in headers
                link_header = response.headers.get('link')
                if link_header and ('rel="next"' in link_header or 'rel=next' in link_header):
                    try:
                        # Extract the URL from the Link header e.g.
                        # <https://api.github.com/...>; rel="next", <...>; rel="last"
                        next_match = re.findall(r"<([^>]+)>;\s*rel\s*=\s*['\"]next['\"]", link_header)
                        url = next_match[0] if next_match else None
                    except Exception:
                        print("Warning: Could not parse 'next' URL from Link header.")
                        url = None
                else:
                    # No next page found
                    url = None

            except requests.exceptions.RequestException as e:
                print(f"\n[!] Network or Request Error during fetch: {e}")
                return []

        all_dates_list = list(all_dates)
        print(f"✅ Successfully fetched data covering {len(all_dates_list)} unique days.")
        return all_dates_list

    def fetch_contribution_data_graphql(self, years: int | None = None) -> list[str]:
        """
        Use the GitHub GraphQL API to fetch the contributions calendar for the
        specified user. This provides a consolidated cross-repo contribution
        history and is generally the most complete source for daily activity.

        Args:
            years: number of years in the past to include (best-effort). If None,
                   the function will request year-by-year from 2008 to present.

        Returns:
            list[str]: list of unique 'YYYY-MM-DD' date strings with >0 contributions.
        """
        # GraphQL endpoint
        url = "https://api.github.com/graphql"
        headers = {
            "Authorization": f"Bearer {self.GITHUB_TOKEN}",
            "Accept": "application/vnd.github.v4+json",
        }

        now = datetime.utcnow()
        windows = []

        if years is None:
            start_year = 2008
            end_year = now.year
            for y in range(start_year, end_year + 1):
                s = datetime(y, 1, 1)
                e = datetime(y, 12, 31, 23, 59, 59)
                if e > now:
                    e = now
                windows.append((s, e))
        else:
            # Single continuous window for recent years
            from_dt = now - timedelta(days=365 * years)
            windows.append((from_dt, now))

        query = """
        query($login: String!, $from: DateTime!, $to: DateTime!) {
          user(login: $login) {
            contributionsCollection(from: $from, to: $to) {
              contributionCalendar {
                weeks {
                  contributionDays {
                    date
                    contributionCount
                  }
                }
              }
            }
          }
        }
        """

        all_dates = set()
        for (s_dt, e_dt) in windows:
            variables = {
                "login": self.target_username,
                "from": s_dt.strftime("%Y-%m-%dT00:00:00Z"),
                "to": e_dt.strftime("%Y-%m-%dT23:59:59Z"),
            }

            try:
                resp = requests.post(url, headers=headers, json={"query": query, "variables": variables}, timeout=30)
                if resp.status_code != 200:
                    # If auth/rate limit issues arise, abort and fall back
                    print(f"Warning: GraphQL query failed (status {resp.status_code}).")
                    return []

                payload = resp.json()
                if payload.get('errors'):
                    # On errors (e.g., user not found), bail out early for that window
                    continue

                coll = payload.get('data', {}).get('user', {}).get('contributionsCollection')
                if not coll:
                    continue

                cal = coll.get('contributionCalendar', {})
                weeks = cal.get('weeks', []) or []
                for week in weeks:
                    for day in week.get('contributionDays', []) or []:
                        try:
                            if day.get('contributionCount', 0) and day.get('date'):
                                all_dates.add(day.get('date'))
                        except Exception:
                            continue

            except requests.exceptions.RequestException as e:
                print(f"Warning: GraphQL request error for window {s_dt} - {e}")
                continue

        # If we found nothing and we had attempted full-history, retry with 1 year window
        if not all_dates and years is None:
            return self.fetch_contribution_data_graphql(years=1)

        return list(all_dates)

    def fetch_contributions_from_repos(self):
        """
        Best-effort retrieval of commit activity by enumerating the user's public
        repositories and collecting commit dates authored by the user. This can
        provide older history than the events API in many cases.

        Returns:
            list[str]: unique date strings found in commits across repos.
        """
        repo_dates = set()
        repos_url = f"https://api.github.com/users/{self.target_username}/repos?per_page=100"
        try:
            while repos_url:
                r = requests.get(repos_url, headers=self.headers)
                if r.status_code != 200:
                    print(f"Warning: Could not list repos (status {r.status_code}), skipping repo-based collection.")
                    break
                repos = r.json()
                if not isinstance(repos, list):
                    break

                for repo in repos:
                    repo_name = repo.get('name')
                    owner = repo.get('owner', {}).get('login')
                    if not repo_name or not owner:
                        continue

                    commits_url = f"https://api.github.com/repos/{owner}/{repo_name}/commits?author={self.target_username}&per_page=100"
                    try:
                        next_commits = commits_url
                        while next_commits:
                            cr = requests.get(next_commits, headers=self.headers)
                            if cr.status_code != 200:
                                break
                            commits = cr.json()
                            if not isinstance(commits, list):
                                break
                            for commit in commits:
                                # commit['commit']['author']['date'] is the authored date
                                date_str = None
                                try:
                                    date_str = commit.get('commit', {}).get('author', {}).get('date')
                                except Exception:
                                    date_str = None
                                if date_str:
                                    try:
                                        date_obj = datetime.fromisoformat(date_str.replace('Z', '+00:00'))
                                        repo_dates.add(date_obj.strftime('%Y-%m-%d'))
                                    except Exception:
                                        pass

                            # pagination for commits
                            link = cr.headers.get('link')
                            if link and 'rel="next"' in link:
                                nm = re.findall(r"<([^>]+)>;\s*rel\s*=\s*['\"]next['\"]", link)
                                next_commits = nm[0] if nm else None
                            else:
                                next_commits = None
                    except requests.exceptions.RequestException:
                        continue

                # pagination for repos
                link = r.headers.get('link')
                if link and 'rel="next"' in link:
                    nm = re.findall(r"<([^>]+)>;\s*rel\s*=\s*['\"]next['\"]", link)
                    repos_url = nm[0] if nm else None
                else:
                    repos_url = None

        except requests.exceptions.RequestException as e:
            print(f"Warning: Network error while listing repos: {e}")

        return list(repo_dates)