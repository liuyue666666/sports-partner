from datetime import datetime, timedelta, timezone

import pytest


def _future(hours: int = 24) -> str:
    return (datetime.now(timezone.utc) + timedelta(hours=hours)).isoformat()


def _activity_payload(**overrides) -> dict:
    start = datetime.now(timezone.utc) + timedelta(hours=48)
    deadline = datetime.now(timezone.utc) + timedelta(hours=24)
    data = {
        "title": "周末梧桐山徒步",
        "description": "一起爬山看日出",
        "sport_tag_id": 1,
        "start_time": start.isoformat(),
        "end_time": (start + timedelta(hours=4)).isoformat(),
        "latitude": 22.587,
        "longitude": 114.215,
        "address": "梧桐山北门",
        "max_participants": 4,
        "gender_requirement": 0,
        "registration_deadline": deadline.isoformat(),
    }
    data.update(overrides)
    return data


def test_create_activity(client, auth_headers):
    response = client.post("/api/v1/activities", headers=auth_headers, json=_activity_payload())
    assert response.status_code == 200
    body = response.json()
    assert body["title"] == "周末梧桐山徒步"
    assert body["current_participants"] == 1
    assert body["status"] == 1
    assert len(body["participants"]) == 1


def test_list_nearby_activities(client, auth_headers):
    client.post("/api/v1/activities", headers=auth_headers, json=_activity_payload())
    response = client.get(
        "/api/v1/activities",
        params={"lat": 22.58, "lng": 114.21, "radius": 10000},
    )
    assert response.status_code == 200
    assert len(response.json()) >= 1


def test_join_and_cancel(client, auth_headers):
    create = client.post("/api/v1/activities", headers=auth_headers, json=_activity_payload())
    activity_id = create.json()["id"]

    login2 = client.post("/api/v1/auth/wechat/login", json={"code": "test-code-002"})
    headers2 = {"Authorization": f"Bearer {login2.json()['access_token']}"}
    client.put("/api/v1/users/me", headers=headers2, json={"gender": 1})

    joined = client.post(f"/api/v1/activities/{activity_id}/join", headers=headers2)
    assert joined.status_code == 200
    assert joined.json()["current_participants"] == 2

    cancelled = client.delete(f"/api/v1/activities/{activity_id}/join", headers=headers2)
    assert cancelled.status_code == 200
    assert cancelled.json()["current_participants"] == 1


def test_my_activities(client, auth_headers):
    client.post("/api/v1/activities", headers=auth_headers, json=_activity_payload(title="我的活动"))
    created = client.get("/api/v1/activities/my/created", headers=auth_headers)
    joined = client.get("/api/v1/activities/my/joined", headers=auth_headers)
    assert created.status_code == 200
    assert len(created.json()) >= 1
    assert joined.status_code == 200


def test_cancel_activity(client, auth_headers):
    create = client.post("/api/v1/activities", headers=auth_headers, json=_activity_payload())
    activity_id = create.json()["id"]
    response = client.put(f"/api/v1/activities/{activity_id}/cancel", headers=auth_headers)
    assert response.status_code == 200
    assert response.json()["status"] == 5
