# README.md

# GitHub Streak Tracker
(Project Status: Refactored & Modularized)

This application monitors a user's continuous contribution streak on GitHub, providing an accurate "streak counter" experience similar to Duolingo. It connects directly to the GitHub API using a Personal Access Token (PAT).

## 🚀 Usage Instructions

### A. Production Mode (Recommended TUI Use)
Run the application normally: `python main.py`. This will launch the interactive TUI, allowing you to select the scope of your streak check (e.g., all repos vs. specific repo).

### B. Development/Test Mode
To test underlying modules or debug components, set the environment flag:
`export DEV_MODE=true`
Then run: `python main.py`. This bypasses the TUI and exercises the isolated module tests directly in the console.

## 📚 Technical Architecture (Advanced Users)
The entire logic has been refactored into a modular package named `streaks/`, which enforces strict separation of concerns:

*   **`api_fetcher.py`:** Manages all external HTTP communication with GitHub, handling pagination and authentication.
*   **`calculator.py`:** Houses the pure mathematical function (`calculate_streak`), ensuring streak logic is isolated and easily unit-testable.
*   **`core.py`:** Acts as the `StreakEngine`, acting as a wrapper that orchestrates calls between API fetching and calculation, presenting a stable interface to the rest of the application.

## Setup & Installation
1.  Clone the project: `git clone <repo-url>`
2.  Install dependencies: `pip install -r requirements.txt`
3.  Set up environment variables (See `.env.example`).