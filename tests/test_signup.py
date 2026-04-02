from src import app as app_module


def test_signup_for_activity_succeeds_for_new_student(client):
    response = client.post(
        "/activities/Chess%20Club/signup",
        params={"email": "newstudent@mergington.edu"},
    )

    assert response.status_code == 200
    assert response.json() == {
        "message": "Signed up newstudent@mergington.edu for Chess Club"
    }

    activities_response = client.get("/activities")
    participants = activities_response.json()["Chess Club"]["participants"]
    assert "newstudent@mergington.edu" in participants


def test_signup_for_activity_returns_404_when_activity_not_found(client):
    response = client.post(
        "/activities/Unknown%20Club/signup",
        params={"email": "student@mergington.edu"},
    )

    assert response.status_code == 404
    assert response.json() == {"detail": "Activity not found"}


def test_signup_for_activity_returns_400_for_duplicate_registration(client):
    email = "michael@mergington.edu"

    response = client.post(
        "/activities/Chess%20Club/signup",
        params={"email": email},
    )

    assert response.status_code == 400
    assert response.json() == {
        "detail": "Student already signed up for this activity"
    }


def test_signup_for_activity_returns_422_when_email_missing(client):
    response = client.post("/activities/Chess%20Club/signup")

    assert response.status_code == 422


def test_signup_currently_does_not_enforce_max_participants(client):
    app_module.activities["Mini Capacity Club"] = {
        "description": "Temporary activity for capacity behavior test",
        "schedule": "Fridays, 4:00 PM - 5:00 PM",
        "max_participants": 1,
        "participants": ["seed@mergington.edu"],
    }

    response = client.post(
        "/activities/Mini%20Capacity%20Club/signup",
        params={"email": "extra@mergington.edu"},
    )

    assert response.status_code == 200
    participants = client.get("/activities").json()["Mini Capacity Club"]["participants"]
    assert participants == ["seed@mergington.edu", "extra@mergington.edu"]
