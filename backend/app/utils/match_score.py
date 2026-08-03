from datetime import datetime, timedelta, timezone


def utcnow() -> datetime:
    return datetime.now(timezone.utc)


def minutes_overlap(
    start_a: datetime,
    end_a: datetime,
    start_b: datetime,
    end_b: datetime,
) -> float:
    """Return overlap duration in minutes between two time ranges."""
    overlap_start = max(start_a, start_b)
    overlap_end = min(end_a, end_b)
    if overlap_end <= overlap_start:
        return 0.0
    return (overlap_end - overlap_start).total_seconds() / 60.0


def time_availability_score(
    user_available_start: datetime | None,
    user_available_end: datetime | None,
    activity_start: datetime,
    activity_end: datetime | None,
    window_hours: int = 4,
) -> float:
    """
    Score how well user's available time overlaps with an activity.
    Returns 0-1; 1.0 if fully overlapping or no preference set.
    """
    if user_available_start is None or user_available_end is None:
        return 1.0

    act_end = activity_end or (activity_start + timedelta(hours=window_hours))
    overlap = minutes_overlap(user_available_start, user_available_end, activity_start, act_end)
    activity_duration = max((act_end - activity_start).total_seconds() / 60.0, 1.0)
    return min(1.0, overlap / activity_duration)
