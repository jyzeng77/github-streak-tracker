# streaks/api_fetcher.py

import requests
from datetime import datetime, timedelta

class GitHubAPIClient:
    """Handles all interaction with the GitHub REST API for fetching contribution data."""

    def __init__(self, github_username: str, token: str):
        self.GITHUB_TOKEN = token
        if not self.GITHUB_TOKEN:
            raise ValueError("GH_TOKEN must be provided to initialize GitHubAPIClient.")

        # Standard headers for authentication and content negotiation
        self.headers = {
            "Authorization": f"token {self.GITHUB_TOKEN}",
            "Accept": "application/vnd.github.v3+json"
        }
        self.target_username = github_username

    def _get_date_for_since_query(self) -> str:
        """Helper to calculate the date N-days ago for API 'since' parameter."""
        # Looking back 1 year is a reasonable default window for contribution tracking.
        return (datetime.now() - timedelta(days=365)).strftime('%Y-%m-%d')

    def fetch_contribution_data(self):
        """
        Fetches all unique activity dates across the user's public repositories
        by querying paginated GitHub API events.

        Returns:
            list[str]: A list of unique date strings ('YYYY-MM-DD'). Returns empty list on failure.
        """
        all_dates = set()
        # We start with PushEvent as it covers most commits, but we must handle general events for completeness.
        url = f"https://api.github.com/users/{self.target_username}/events?type=PushEvent&per_page=100&since={self._get_date_for_since_query()}"
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
                events = data.get('events', [])

                if not events:
                    break

                # Process fetched events/commits
                for event in events:
                    created_at = event.get('created_at')
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
                if link_header and 'rel="next"' in link_header:
                    try:
                        import re
                        # Extracting URL from <url>; rel="next" structure
                        next_match = re.findall(r'<([^>]+)>;\s*rel\s*=\s*["']next["']', link_header)
                        url = next_match[0]
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