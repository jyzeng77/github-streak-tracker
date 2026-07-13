# streaks/calculator.py

from datetime import datetime, timedelta
from typing import Optional, Tuple


def calculate_streak(contribution_dates: list[str]) -> tuple[int, str | None, int]:
    """
    Calculates both the current consecutive streak and the historical longest streak
    from a set of date strings ('YYYY-MM-DD').

    Args:
        contribution_dates: A list of unique date strings found in GitHub contributions.

    Returns:
        A tuple containing:
        - current_streak (int): consecutive streak ending on the most recent date.
        - peak_date (str | None): most recent contribution date.
        - max_streak (int): historical longest consecutive streak.
    """
    if not contribution_dates:
        return 0, None, 0

    # Phase 1: Preparation - Convert strings to date objects for reliable arithmetic
    try:
        date_objects = []
        for d_str in contribution_dates:
            # Parsing must be robust. We assume the API guarantees 'YYYY-MM-DD'.
            date_obj = datetime.strptime(d_str, '%Y-%m-%d').date()
            date_objects.append(date_obj)
    except ValueError as e:
        print(f"CRITICAL ERROR: Date parsing failed during calculation phase. Check input data format. Error: {e}")
        return 0, None, 0

    # Ensure uniqueness and sort the date objects in descending order (most recent first)
    date_set = sorted(list(set(date_objects)), reverse=True)


    # --- Phase 2: Current Streak Algorithm ---
    # The product expects the "current consecutive streak" up to the most recent
    # contributing day (not the historical maximum). We'll compute the streak that
    # ends at the most recent date in `date_set`.

    # Build a set for O(1) membership checks
    date_lookup = set(date_set)

    if not date_set:
        return 0, None, 0

    most_recent = date_set[0]

    # Current consecutive streak: walk backwards from most_recent
    current_streak = 0
    cursor = most_recent
    while cursor in date_lookup:
        current_streak += 1
        cursor = cursor - timedelta(days=1)

    # Historical maximum streak: iterate through sorted unique dates and find longest run
    max_streak = 0
    running = 0
    prev = None
    for d in date_set:
        if prev is None:
            running = 1
        else:
            if (prev - d).days == 1:
                running += 1
            else:
                max_streak = max(max_streak, running)
                running = 1
        prev = d
    max_streak = max(max_streak, running)

    peak_date = most_recent

    return current_streak, (peak_date.isoformat() if peak_date else None), max_streak