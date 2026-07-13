import os
from dotenv import load_dotenv

# Load environment variables from .env if present so downstream modules can access them
load_dotenv()
# Import the main execution interface from our newly created package structure
try:
    from streaks.core import StreakEngine
except ImportError:
    print("Error: Could not find 'streaks/core.py'. Ensure your project is structured correctly.")

def main():
    """Thin entrypoint for the application."""
    # The logic now uses environment flags to determine execution path (Dev vs Production)
    is_dev = os.environ.get("DEV_MODE") == "true"

    if is_dev:
        print("\n[! DEVE/TEST MODE ACTIVATED !]")
        print("Running unit tests/exercise code against the modular components.")
        # In a real scenario, this would run pytest or other test runners.
        from streaks.api_fetcher import GitHubAPIClient
        from streaks.calculator import calculate_streak
        print("[Test] Test setup complete. Ready to run manual module tests.")

    else:
        # Production Mode: Launch the TUI for user interaction
        print("\n[🚀 PRODUCTION MODE] Launching Interactive Dashboard...")
        try:
            from tui import main_tui # Import and run the dedicated TUI script
            main_tui()
        except ImportError as e:
             print(f"\n[!] FATAL ERROR: Could not import TUI. Ensure 'tui.py' exists and is executable. Error: {e}")

if __name__ == "__main__":
    main()