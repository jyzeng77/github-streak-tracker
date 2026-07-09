# Project Development Rules and Guidelines

These rules govern how the project will be developed and tracked within this workspace. Adherence to these guidelines ensures a consistent, auditable, and maintained codebase.

## Core Operating Procedures
1. **Log Updates:** Always update `PROJECT_LOG.md` under Session Log with a detailed summary immediately after any task is successfully completed or a significant decision is made. The log must document *what* was done and *why*. Start each entry with a header containing the date and time in DD/MM/YYYY HH:MM:SS (24 hour format).
2. **Version Control Workflow:** Always create a branch to work on tasks and merge to main branch after reviewing and my approval.  After any successful change to the codebase (`main.py`, etc.), the developer MUST commit the changes and push them to the remote repository (e.g., `git add . && git commit -m "Feature: [...]" && git push`). All planning steps must conclude with execution notice.
3. **Data Integrity:** NEVER overwrite historical data within `PROJECT_LOG.md`. Any structural changes or additions to the log must append new information while preserving all records of previous milestones and decisions.

## Additional Rules
- main.py must end up as a thin entrypoint only: checks for a flag, 
  runs test/exercise code if present, else launches whatever the main application is
- All streak logic lives in modules outside main.py
- After each major step, run tests if possible and confirm that it works
- Never force-push, never touch main branch, never delete files 
  without moving their logic first. You may merge code from a working branch after review and upon my approval
- If genuinely blocked or ambiguous, write the question under a Blockers subsection of the current log entry you are writing and make a reasonable and documented assumption rather than stopping
