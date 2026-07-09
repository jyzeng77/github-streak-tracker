import os
from dotenv import load_dotenv
import requests
from datetime import datetime, timedelta
from collections import defaultdict

class GitHubStreakTracker:
    """Manages the connection and logic for tracking GitHub contribution streaks."""

    def __init__(self, github_username="your_github_user"):
        """Initializes the tracker with the user's username."""
        self.GITHUB_TOKEN = os.getenv("GH_TOKEN")
        # Use a default value or raise error if token is missing
        if not self.GITHUB_TOKEN:
            print("Error: GH_TOKEN not found in environment variables.")
        else:
            # Use a dedicated Accept header for clear API interaction
            self.headers = {
                "Authorization": f"token {self.GITHUB_TOKEN}",
                "Accept": "application/vnd.github.v3+json"
            }
        self.target_username = github_username

    def fetch_contribution_data(self):
        """
        Fetches all unique contribution dates for the target user across their public repositories
        by querying paginated commit data and aggregating event types (PushEvent, etc.).

        Returns:
            list[str]: A list of unique date strings ('YYYY-MM-DD') from activity. Returns empty list on failure.
        """
        if not self.GITHUB_TOKEN or self.target_username == "your_github_user":
            print("\n[!] Cannot fetch contribution data. GH_TOKEN is missing or target username is default.")
            return []

        all_dates = set()
        # Querying general activity events (PushEvent covers most commit activities)
        url = f"https://api.github.com/users/{self.target_username}/events?type=PushEvent&per_page=100"
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

    def calculate_streak(self, contribution_dates):
        """
        Calculates the longest consecutive streak from a set of date strings.
        'contribution_dates' is expected to be a list of 'YYYY-MM-DD' strings.
        """
        if not contribution_dates:
            print("No contribution data found.")
            return 0, None

        # Use date objects for robust comparison
        date_set = set(contribution_dates)
        sorted_dates_str = sorted(list(date_set), reverse=True)

        # Convert all strings to datetime.date object immediately for efficiency
        try:
            date_objects = [datetime.strptime(d, '%Y-%m-%d').date() for d in sorted_dates_str]
        except ValueError as e:
            print(f"Error converting dates for streak calculation: {e}")
            return 0, None

        # --- Streak Calculation Logic (Optimized) ---
        max_streak = 0
        current_attempt_streak = 0
        last_date = None # The date object before the current iteration's starting date

        for i in range(len(date_objects)):
            current_date = date_objects[i]

            if i == 0:
                # First day always starts a streak of at least 1
                current_attempt_streak = 1
                last_date = current_date
            else:
                previous_date = date_objects[i-1]

                # If the gap is exactly one day, increment streak
                if (last_date - previous_date).days == 1:
                    current_attempt_streak += 1
                else:
                    # Streak broken. Start a new potential streak of 1.
                    current_attempt_streak = 1

                last_date = previous_date # The previously checked day becomes the reference for the next comparison

            max_streak = max(max_streak, current_attempt_streak)

        peak_date = datetime.strptime(sorted_dates_str[0], '%Y-%m-%d').date() if sorted_dates_str else None
        return max_streak, peak_date


def main():
    """Main function to run the streak tracker."""
    print("--- GitHub Streak Tracker Initializing ---")

    # Get username from argument or environment variable
    username = os.environ.get("GH_USER", "your_github_user")
    tracker = GitHubStreakTracker(github_username=username)

    if not tracker.GITHUB_TOKEN:
        print("\n[!] Cannot run streak calculation. Please ensure GH_TOKEN is set in the .env file.")
        return

    # Step 1: Fetch Data using live API calls
    contribution_dates = tracker.fetch_contribution_data() # Returns list of 'YYYY-MM-DD' strings

    if not contribution_dates:
        print("Streak calculation skipped due to lack of contribution data or API failure.")
        return # Exit if no dates were fetched

    # Step 2: Calculate Streak using the live data
    streak, peak_date = tracker.calculate_streak(contribution_dates)

    if streak > 0 and peak_date:
        print("\n=====================================================")
        print("🏆 STREAK REPORT 💎")
        print("=====================================================")
        print(f"🔥 Current Consecutive Streak: {streak} days!")
        print(f"📅 Last recorded activity streak up to: {peak_date}")
        print("\nKeep coding! Don't lose your momentum.")
    else:
        print("Could not determine a solid streak. Check configurations or data availability.")

if __name__ == "__main__":
    main()