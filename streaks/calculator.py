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


    # --- Phase 2: Current Streak Algorithm ---
    # The product expects the "current consecutive streak" up to the most recent
    # contributing day (not the historical maximum). We'll compute the streak that
    # ends at the most recent date in `date_set`.

    # Build a set for O(1) membership checks
    date_lookup = set(date_set)

    if not date_set:
        return 0, None

    most_recent = date_set[0]

    # Walk backwards from the most recent date counting consecutive days
    current_streak = 0
    cursor = most_recent
    while cursor in date_lookup:
        current_streak += 1
        cursor = cursor - timedelta(days=1)

    peak_date = most_recent

    return current_streak, (peak_date.isoformat() if peak_date else None)