"""Placeholder module for fastapi pytest tests."""


def test_liveliness(dummy_client):
    response = dummy_client.get("/live")
    assert response.status_code == 200


def test_dummy_table(dummy_client):
    response = dummy_client.get("api/dummy_info/dummy")
    assert response.status_code == 200
