# Project Log: GitHub Streak Tracker

## Overview
This project aims to create a "streaky" coding progress tracker for GitHub contributors, similar in concept to DuoLingo's streak system. It will monitor continuous daily commits and visualize the user's contribution graph and current consecutive streak.

## Goals
1.  Authenticate with GitHub using a Personal Access Token (PAT).
2.  Fetch commit history for a specified user/repository via the GitHub REST API.
3.  Calculate the last day of contribution, current streak length, and identify any breaks in the chain on a daily basis.
4.  Present the results in an engaging, "gamified" manner.

## Technical Details & Challenges
The primary challenge is querying contributions across all repositories for a user accurately. We will utilize the GitHub REST API to retrieve structured commit data rather than relying solely on simple profile feeds.

## Tools & State Changes
*   Implemented `requirements.txt` with `requests` and `python-dotenv`.
*   Created `.env.example` for secure token storage.
*   Structured the app using a class (`GitHubStreakTracker`) in `main.py`. 

## Session Logs 
These are the updates made in chronological order. Other people may have made changes and if they were not documented try to find the commit and time and fill in that info.

### [this one was not dated. when you have time find the time this stuff was completed.] 
Current Focus: Phase 2 - API Integration & Core Logic
We are currently upgrading the placeholder functions (`fetch_contribution_data`) in `main.py` to make live calls to GitHub APIs to gather real contribution data.

