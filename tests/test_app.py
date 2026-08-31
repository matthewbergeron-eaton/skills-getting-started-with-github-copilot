from copy import deepcopy

import pytest
from fastapi.testclient import TestClient

from src.app import app, activities


@pytest.fixture(autouse=True)
def reset_activities():
    original = deepcopy(activities)
    yield
    activities.clear()
    activities.update(original)


client = TestClient(app)


def test_signup_rejects_duplicate_email():
    response = client.post(
        "/activities/Chess Club/signup?email=michael@mergington.edu"
    )

    assert response.status_code == 400
    assert "already signed up" in response.json()["detail"].lower()


def test_delete_participant_removes_email_from_activity():
    response = client.delete(
        "/activities/Chess Club/participants?email=daniel@mergington.edu"
    )

    assert response.status_code == 200
    assert "daniel@mergington.edu" not in activities["Chess Club"]["participants"]
    assert response.json()["message"] == "Removed daniel@mergington.edu from Chess Club"
