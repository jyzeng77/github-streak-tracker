# streaks/core.py

import os
from typing import Optional, Tuple

# Import the modular components
from .api_fetcher import GitHubAPIClient
from .calculator import calculate_streak


class StreakEngine:
    """
    The core engine that orchestrates fetching data and calculating the final streak report.
    This module abstracts away API complexity from the calling code (main.py/tui.py).
    It acts as the single, reliable interface for asking "What is my streak?".
    """

    def __init__(self, github_username: str, token: Optional[str] = None):
        if not token:
             raise ValueError("GH_TOKEN must be provided to initialize StreakEngine.")

        # Initialize the client which contains authentication and fetching logic
        self.api_client = GitHubAPIClient(github_username=github_username, token=token)

    def calculate_current_streak(self, scope: str = "all_repos") -> Tuple[int, Optional[str]]:
        """
        Executes the full workflow: Fetch Data -> Calculate Streak.

        Args:
            scope (str): Defines what data to fetch ('all_repos' or 'single_repo').
                          The current implementation defaults to and supports only 'all_repos'.

        Returns:
            A tuple containing (streak_count: int, peak_date: str | None).
        """
        # Currently, the API client is hardcoded/optimized for fetching all user events.
        raw_dates = self.api_client.fetch_contribution_data()

        if not raw_dates:
            return 0, None # API failed or no data found

        # --- Calculation ---
        print(f"\n[Core Engine]: Running streak calculation based on {len(raw_dates)} unique contributing days.")
        streak, peak_date = calculate_streak(raw_dates)

        return streak, peak_date