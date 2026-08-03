import math

from app.utils.geo import distance_score, haversine_distance_meters


def test_haversine_same_point():
    assert haversine_distance_meters(22.5, 114.0, 22.5, 114.0) == 0.0


def test_haversine_known_distance():
    # Shenzhen to Guangzhou approx 120km
    dist = haversine_distance_meters(22.5431, 114.0579, 23.1291, 113.2644)
    assert 100_000 < dist < 150_000


def test_distance_score():
    assert distance_score(0, 5000) == 1.0
    assert distance_score(2500, 5000) == 0.5
    assert distance_score(5000, 5000) == 0.0
    assert distance_score(6000, 5000) == 0.0
