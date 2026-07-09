# 📘 Project Development Rules and Guidelines

These rules govern how the project will be developed and tracked within this workspace. Adherence to these guidelines ensures a consistent, auditable, and maintained codebase.

## Core Operating Procedures
1. **Log Updates:** Always update `PROJECT_LOG.md` with a detailed summary immediately after any task is successfully completed or a significant decision is made. The log must document *what* was done and *why*.
2. **Version Control Workflow:** After any successful change to the codebase (`main.py`, etc.), the developer MUST commit the changes and push them to the remote repository (e.g., `git add . && git commit -m "Feature: [...]" && git push`). All planning steps must conclude with a commit simulation or execution notice.
3. **Data Integrity:** NEVER overwrite historical data within `PROJECT_LOG.md`. Any structural changes or additions to the log must append new information while preserving all records of previous milestones and decisions.

## Common Mistakes
1. When writing a file, you write `write ...` and omit a proper file name. Fill in the `...`.
2. When writing a file, you assume the content you read from it before is the same. If a write error has occured try rereading the file to see if any changes were made.
