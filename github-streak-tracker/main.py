import os
from dotenv import load_dotenv
import requests
from datetime import datetime, timedelta
from collections import defaultdict

# Load environment variables from .env file
load_dotenv()

class GitHubStreakTracker:
    """Manages the connection and logic for tracking GitHub contribution streaks."""

    def __init__(self, github_username="your_github_user"):
        """Initializes the tracker with the user's username."""
        self.GITHUB_TOKEN = os.getenv("GH_TOKEN")
        # Use a default value or raise error if token is missing
        if not self.GITHUB_TOKEN:
            print("Error: GH_TOKEN not found in environment variables.")
        else:
            self.headers = {
                "Authorization": f"token {self.GITHUB_TOKEN}",
                "Accept": "application/vnd.github.v3+json"
            }
        self.target_username = github_username

    def fetch_contribution_data(self):
        """
        Placeholder: Fetches the necessary contribution data from GitHub API.
        This will need to be updated based on whether we track contributions 
        across all repos or focus on one profile's activity feed.
        
        For simplicity in V1, let's use the main contribution endpoint
        if available, otherwise we iterate through recent commits of a default repo.
        """
        print("Fetching raw commit data... (Placeholder)")
        # Actual implementation will go here
        # We need to gather all relevant dates across all repos/commits for the user.
        pass 

    def calculate_streak(self, contribution_dates):
        """
        Calculates the longest consecutive streak from a set of dates.
        'contribution_dates' is expected to be a list or set of datetime objects.
        """
        if not contribution_dates:
            print("No contribution data found.")
            return 0, None

        # Convert to sorted unique dates (start with the most recent)
        sorted_dates = sorted(list(set(contribution_dates)), reverse=True)
        
        current_streak = 1
        last_date = sorted_dates[0]
        current_window_end = last_date
        
        print("Calculating streak...")

        for i in range(1, len(sorted_dates)):
            day = sorted_dates[i]
            # Check if the gap is exactly one day (24 hours)
            if (last_date - day).days == 1:
                current_streak += 1
            else:
                # Streak broken. Check if this new start date begins a better streak?
                # For simplicity, we only track the current run extending backward from today/max date.
                pass # Reset if necessary, but since it's sorted reverse, we are looking for continuity.
            
            last_date = day
        
        # Reworking simple loop to find max streak:
        max_streak = 0
        current_attempt_streak = 0
        
        if not sorted_dates: return 0, None

        for i in range(len(sorted_dates)):
            day = datetime.strptime(sorted_dates[i], '%Y-%m-%d').date()
            if i == 0:
                current_attempt_streak = 1
            else:
                previous_day = datetime.strptime(sorted_dates[i-1], '%Y-%m-%d').date()
                # If the day is exactly one day before the previous recorded day
                if (previous_day - day).days == 1:
                    current_attempt_streak += 1
                else:
                    current_attempt_streak = 1 # Start new potential streak

            max_streak = max(max_streak, current_attempt_streak)
        
        # Use the last date recorded as 'peak' for display purposes if successful.
        return max_streak, sorted_dates[0]


def main():
    """Main function to run the streak tracker."""
    print("--- GitHub Streak Tracker Initializing ---")

    # Get username from argument or environment variable
    username = os.environ.get("GH_USER", "your_github_user") 
    tracker = GitHubStreakTracker(github_username=username)

    if not tracker.GITHUB_TOKEN:
        print("\n[!] Cannot run streak calculation. Please ensure GH_TOKEN is set in the .env file.")
        return

    # Step 1: Fetch Data
    # This placeholder will be implemented later, but we pass an empty list for now 
    # to simulate a successful data structure flow.
    contribution_dates = [] # List of 'YYYY-MM-DD' strings or date objects

    # For testing the streak calculation logic without making API calls initially:
    print("\n--- Running with Mock Data (Test) ---\n")
    mock_data = [
        "2023-12-31", # Start of a long chain
        "2024-01-01",
        "2024-01-02",
        # Break here (missing 2024-01-03)
        "2024-01-05", # New streak starts
        "2024-01-06",
    ]
    contribution_dates = mock_data

    # Step 2: Calculate Streak
    streak, peak_date = tracker.calculate_streak(contribution_dates)

    if streak > 0 and peak_date:
        print("\n=====================================================")
        print("🏆 STREAK REPORT 💎")
        print("=====================================================")
        print(f"🔥 Current Consecutive Streak (Mock): {streak} days!")
        print(f"📅 Last recorded activity streak up to: {peak_date}")
        print("\nKeep coding! Don't lose your momentum.")
    else:
        print("Could not determine a solid streak. Check configurations or data availability.")


if __name__ == "__main__":
    main()