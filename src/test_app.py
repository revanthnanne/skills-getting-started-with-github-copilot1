from fastapi.testclient import TestClient
import copy

from app import app, activities

client = TestClient(app)

INITIAL_ACTIVITIES = {
    "Chess Club": {
        "description": "Learn strategies and compete in chess tournaments",
        "schedule": "Fridays, 3:30 PM - 5:00 PM",
        "max_participants": 12,
        "participants": ["michael@mergington.edu", "daniel@mergington.edu"],
    },
    "Programming Class": {
        "description": "Learn programming fundamentals and build software projects",
        "schedule": "Tuesdays and Thursdays, 3:30 PM - 4:30 PM",
        "max_participants": 20,
        "participants": ["emma@mergington.edu", "sophia@mergington.edu"],
    },
    "Gym Class": {
        "description": "Physical education and sports activities",
        "schedule": "Mondays, Wednesdays, Fridays, 2:00 PM - 3:00 PM",
        "max_participants": 30,
        "participants": ["john@mergington.edu", "olivia@mergington.edu"],
    },
}


def setup_function():
    activities.clear()
    activities.update(copy.deepcopy(INITIAL_ACTIVITIES))


def test_signup_for_activity_success():
    response = client.post(
        "/activities/Chess%20Club/signup?email=newstudent@mergington.edu"
    )
    assert response.status_code == 200
    assert response.json() == {
        "message": "Signed up newstudent@mergington.edu for Chess Club"
    }
    assert "newstudent@mergington.edu" in activities["Chess Club"]["participants"]


def test_signup_for_activity_duplicate_fails():
    response1 = client.post(
        "/activities/Chess%20Club/signup?email=michael@mergington.edu"
    )
    assert response1.status_code == 400
    assert response1.json()["detail"] == "Student already signed up for this activity"


def test_signup_for_activity_full_capacity_fails():
    activities["Gym Class"]["participants"] = [f"student{i}@mergington.edu" for i in range(30)]
    assert len(activities["Gym Class"]["participants"]) == 30

    response = client.post(
        "/activities/Gym%20Class/signup?email=overflow@mergington.edu"
    )
    assert response.status_code == 400
    assert response.json()["detail"] == "Activity is full"
