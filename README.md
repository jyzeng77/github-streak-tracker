# GitHub Streak Tracker

This application monitors a user's continuous contributions to GitHub, tracking their commit streak like a Duolingo progress system. It connects directly to the GitHub API via a Personal Access Token (PAT).

## Prerequisites
1. **Python:** Python 3.8+
2. **GitHub PAT:** A token with read access to the user's repositories is required. Store this securely in a `.env` file.

## Setup & Installation
1. Clone the project: `git clone <repo-url>`
2. Install dependencies: `pip install -r requirements.txt`
3. Set up environment variables (See PROJECT_LOG.md for details).

## Usage
Run `python main.py` to calculate and display the streak progress!
