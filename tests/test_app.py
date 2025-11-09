from fastapi.testclient import TestClient
from src.app import app

client = TestClient(app)


def get_participants(activity_name: str):
    resp = client.get("/activities")
    assert resp.status_code == 200
    data = resp.json()
    assert activity_name in data
    return data[activity_name]["participants"]


def test_get_activities():
    resp = client.get("/activities")
    assert resp.status_code == 200
    data = resp.json()
    # basic sanity checks
    assert isinstance(data, dict)
    assert "Chess Club" in data


def test_signup_and_unregister_flow():
    activity = "Basketball Team"
    test_email = "pytest-user@example.com"

    # Ensure test email is not already registered (cleanup if necessary)
    participants = get_participants(activity)
    if test_email in participants:
        # try to unregister to ensure clean start
        resp = client.post(f"/activities/{activity}/unregister", params={"email": test_email})
        # allow either success or 400 if not found

    # Sign up the test email
    resp = client.post(f"/activities/{activity}/signup", params={"email": test_email})
    assert resp.status_code == 200
    assert test_email in get_participants(activity)

    # Signing up again should fail with 400
    resp_dup = client.post(f"/activities/{activity}/signup", params={"email": test_email})
    assert resp_dup.status_code == 400
    assert "already" in resp_dup.json().get("detail", "").lower()

    # Unregister the participant
    resp_un = client.post(f"/activities/{activity}/unregister", params={"email": test_email})
    assert resp_un.status_code == 200
    assert test_email not in get_participants(activity)

    # Unregistering again should return 400
    resp_un2 = client.post(f"/activities/{activity}/unregister", params={"email": test_email})
    assert resp_un2.status_code == 400
