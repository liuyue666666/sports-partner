import pytest


def test_wechat_login_creates_user(client):
    response = client.post("/api/v1/auth/wechat/login", json={"code": "test-code-001"})
    assert response.status_code == 200
    data = response.json()
    assert data["token_type"] == "bearer"
    assert data["access_token"]
    assert data["refresh_token"]
    assert data["is_new_user"] is True


def test_wechat_login_existing_user(client):
    client.post("/api/v1/auth/wechat/login", json={"code": "test-code-002"})
    response = client.post("/api/v1/auth/wechat/login", json={"code": "test-code-002"})
    assert response.status_code == 200
    assert response.json()["is_new_user"] is False


def test_refresh_token(client):
    login = client.post("/api/v1/auth/wechat/login", json={"code": "test-code-003"}).json()
    response = client.post(
        "/api/v1/auth/refresh",
        json={"refresh_token": login["refresh_token"]},
    )
    assert response.status_code == 200
    assert response.json()["access_token"]


def test_get_me_requires_auth(client):
    response = client.get("/api/v1/users/me")
    assert response.status_code == 401


def test_get_and_update_me(client, auth_headers):
    me = client.get("/api/v1/users/me", headers=auth_headers)
    assert me.status_code == 200
    assert me.json()["nickname"] == "运动达人"

    updated = client.put(
        "/api/v1/users/me",
        headers=auth_headers,
        json={"nickname": "小明", "gender": 1, "bio": "喜欢徒步", "sport_tag_ids": [1, 2]},
    )
    assert updated.status_code == 200
    body = updated.json()
    assert body["nickname"] == "小明"
    assert body["gender"] == 1
    assert len(body["sport_tags"]) == 2


import pytest


def test_update_location(client, auth_headers):
    response = client.post(
        "/api/v1/users/location",
        headers=auth_headers,
        json={"latitude": 22.5431, "longitude": 114.0579},
    )
    assert response.status_code == 200
    body = response.json()
    assert body["latitude"] == pytest.approx(22.5431, rel=1e-4)
    assert body["longitude"] == pytest.approx(114.0579, rel=1e-4)
    assert body["location_updated_at"] is not None


def test_list_sport_tags(client):
    response = client.get("/api/v1/sport-tags")
    assert response.status_code == 200
    tags = response.json()
    assert len(tags) == 3
    assert tags[0]["name"] == "徒步"


def test_get_public_profile(client, auth_headers):
    me = client.get("/api/v1/users/me", headers=auth_headers).json()
    response = client.get(f"/api/v1/users/{me['id']}")
    assert response.status_code == 200
    assert response.json()["nickname"] == me["nickname"]
