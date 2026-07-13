# GitHub Streak Tracker
(Project Status: Refactored & Modularized)

This application tracks your GitHub contribution streak using GitHub GraphQL as the authoritative source. It reports both your current consecutive streak and your historical longest streak.

## 🚀 Usage Instructions

### A. Production Mode (Recommended TUI Use)
Run the application using the project virtualenv:
```bash
.venv/bin/python -m main
```
This launches the interactive TUI and uses GitHub GraphQL to compute streaks from the contribution calendar.

### B. Development/Test Mode
To exercise lower-level modules manually, set the development flag:
```bash
export DEV_MODE=true
.venv/bin/python -m main
```
This prints the development/test setup information instead of launching the TUI.

## 🔧 Environment Variables
Create a `.env` file in the project root with:
```ini
GH_TOKEN=your_github_pat
GH_USER=your_github_username
```
- `GH_TOKEN` must be a GitHub Personal Access Token with access to public repo data.
- `GH_USER` is the GitHub username whose contribution graph you want to track.

You can copy `.env.example` to `.env` and fill in your values:
```bash
cp .env.example .env
```
## 📚 Technical Architecture
The codebase is modular and organized under `streaks/`:

* **`api_fetcher.py`** — uses GitHub GraphQL for the contribution calendar and treats that calendar as authoritative.
* **`calculator.py`** — computes both current and historical streaks from provided dates.
* **`core.py`** — orchestrates fetching and calculation through `StreakEngine`.
* **`tui.py`** — provides the terminal interface for user interaction.

Optional diagnostics support is kept in `api_fetcher.py` via `fetch_contributions_from_repos()`, but it is not used in the default streak calculation path.

## Setup & Installation
1. Clone the project: `git clone <repo-url>`
2. Activate the virtualenv or use the provided `.venv`.
3. Install dependencies:
```bash
pip install -r requirements.txt
```
4. Populate `.env` from `.env.example` with `GH_TOKEN` and `GH_USER`.
5. Run:
```bash
.venv/bin/python -m main
```
