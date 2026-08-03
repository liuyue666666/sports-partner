import math


def haversine_distance_meters(
    lat1: float,
    lon1: float,
    lat2: float,
    lon2: float,
) -> float:
    """Calculate great-circle distance between two GPS points in meters."""
    radius = 6371000.0
    phi1, phi2 = math.radians(lat1), math.radians(lat2)
    d_phi = math.radians(lat2 - lat1)
    d_lambda = math.radians(lon2 - lon1)

    a = math.sin(d_phi / 2) ** 2 + math.cos(phi1) * math.cos(phi2) * math.sin(d_lambda / 2) ** 2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    return radius * c


def distance_score(distance_meters: float, max_radius_meters: float) -> float:
    """Normalize distance to 0-1 score (closer = higher)."""
    if max_radius_meters <= 0:
        return 0.0
    return max(0.0, 1.0 - distance_meters / max_radius_meters)
