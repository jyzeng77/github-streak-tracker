# tui.py

import os
import sys
from streaks.core import StreakEngine

def run_streak_tracker(engine: StreakEngine, scope: str):
    """
    Runs the streak calculation logic and prints a user-friendly report to stdout.
    This function serves as the primary command execution point for the TUI/main entrypoint.
    """
    print("\n=====================================================")
    if scope == "all_repos":
        print("🔮 Scope: All Public Repositories (Global Streak)")
    elif scope == "single_repo":
         # Future enhancement: This would accept a repository name and use it to filter the API calls.
        print("🔍 Scope: Specific Repository Focus")
    else:
        print("🚨 Warning: Unknown scope selected.")
        return

    current_streak, peak_date, max_streak = engine.calculate_current_streak(scope)

    if current_streak is None or current_streak <= 0:
        print("\n💔 No verifiable streak found at this time. Check your token/scope settings or ensure you have made recent commits.")
    else:
        print("=====================================================")
        print("🏆 STREAK REPORT 💎")
        print("=====================================================")
        print(f"🔥 Current Consecutive Streak: {current_streak} days!")
        if peak_date:
            print(f"📅 Last recorded activity streak up to: {peak_date}")
        else:
            print("⚠️ Warning: Could not determine a clear end date.")
        # Historical best
        print(f"📈 Historical Longest Streak: {max_streak} days")
        print("\nKeep coding! You're building momentum!")

def main_tui():
    """
    Interactive command-line interface for the user.
    Guides the user through scope selection before calling the engine.
    """
    github_username = os.environ.get("GH_USER", "your_github_user")
    token = os.getenv("GH_TOKEN")

    if not token:
        print("\n🛑 Initialization Error: GH_TOKEN is missing from environment variables. Please set it in your .env file.")
        return

    try:
        # Initialize the engine with credentials
        engine = StreakEngine(github_username=github_username, token=token)

        print("--- GitHub Streak Tracker TUI Initialized ---")

        while True:
            print("\nSelect Scope:")
            print("  [A] All Public Repositories (Global)")
            print("  [R] Single Specific Repository (Future Feature)")
            print("  [Q] Quit")

            scope_choice = input("Enter scope [A/R/Q]: ").strip().upper()

            if scope_choice == 'Q':
                print("Goodbye! Keep hacking!")
                break
            elif scope_choice == 'A':
                # Execute the core logic for all repositories
                run_streak_tracker(engine, "all_repos")
            elif scope_choice == 'R':
                 # Placeholder for future specific repo targeting
                print("Feature not yet implemented. Please select 'All Public Repositories'.")
            else:
                print("Invalid choice.")

    except ValueError as e:
        print(f"\nFatal Initialization Error: {e}")
