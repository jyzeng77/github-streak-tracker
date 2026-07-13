# streaks/calculator.py

from datetime import datetime, timedelta
from typing import List, Tuple
from collections import defaultdict


def calculate_streak(contribution_dates: list[str]) -> tuple[int, str | None]:
    """
    Calculates the longest consecutive streak from a set of date strings ('YYYY-MM-DD').

    This function is a pure calculation utility, requiring only cleaned date data as input.
    It handles the logic for finding gaps and determining the peak day.

    Args:
        contribution_dates: A list of unique date strings found in various API calls.

    Returns:
        A tuple containing (max_streak: int, peak_date: str | None): The longest streak count
        and the date the streak was measured up to. Returns (0, None) if no data is provided.
    """
    if not contribution_dates:
        return 0, None

    # Phase 1: Preparation - Convert strings to date objects for reliable arithmetic
    try:
        date_objects = []
        for d_str in contribution_dates:
            # Parsing must be robust. We assume the API guarantees 'YYYY-MM-DD'.
            date_obj = datetime.strptime(d_str, '%Y-%m-%d').date()
            date_objects.append(date_obj)
    except ValueError as e:
        print(f"CRITICAL ERROR: Date parsing failed during calculation phase. Check input data format. Error: {e}")
        return 0, None

    # Ensure uniqueness and sort the date objects in descending order (most recent first)
    date_set = sorted(list(set(date_objects)), reverse=True)


    # --- Phase 2: Core Streak Algorithm ---
    max_streak = 0
    current_attempt_streak = 0
    last_date = None # Holds the date object from the previous day in the loop

    for i in range(len(date_set)):
        current_date = date_set[i]

        if i == 0:
            # First day always starts a streak of at least 1
            current_attempt_streak = 1
            last_date = current_date
        else:
            # CORE CHECK: Is the difference between the last seen date and the current date exactly one day?
            # We keep `last_date` as the previous iteration's date object (more recent), so compare it to current_date.
            if (last_date - current_date).days == 1:
                current_attempt_streak += 1
            else:
                # Streak broken: record the streak and reset
                max_streak = max(max_streak, current_attempt_streak)
                current_attempt_streak = 1

            # Update last_date to the current date for the next loop
            last_date = current_date

        # Update max_streak regardless of whether we found a break, to capture the final running streak.
        max_streak = max(max_streak, current_attempt_streak)


    # The peak date is the most recent date encountered after sorting (the first element).
    peak_date = date_set[0] if date_set else None

    return max_streak, (peak_date.isoformat() if peak_date else None)