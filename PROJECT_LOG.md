# Project Log: GitHub Streak Tracker

## Overview
This project aims to create a "streaky" coding progress tracker for GitHub contributors, similar in concept to DuoLingo's streak system. It will monitor continuous daily commits and visualize the user's contribution graph and current consecutive streak.

## Goals
1.  Authenticate with GitHub using a Personal Access Token (PAT).
2.  Fetch commit history for a specified user/repository.
3.  Calculate the last day of contribution, current streak length, and identify any breaks in the chain.
4.  Present the results in an engaging, "gamified" manner.

## Current State
*   Project directory created: `github-streak-tracker`.
*   Initial structure files to be generated/populated.

## Next Steps
1.  Define required dependencies (e.g., `requests`, potentially a database client if persistence is complex).
2.  Implement the core logic for fetching and parsing GitHub API commit data.
3.  Design the streak calculation algorithm.