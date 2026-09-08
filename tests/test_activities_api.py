def test_get_activities_returns_activity_details(client):
    # Arrange
    expected_activity = "Chess Club"

    # Act
    response = client.get("/activities")

    # Assert
    assert response.status_code == 200
    activities = response.json()
    assert expected_activity in activities
    assert {
        "description",
        "schedule",
        "max_participants",
        "participants",
    } <= activities[expected_activity].keys()


def test_signup_adds_participant(client):
    # Arrange
    activity = "Soccer Club"
    email = "new.student@mergington.edu"

    # Act
    response = client.post(
        f"/activities/{activity}/signup",
        params={"email": email},
    )

    # Assert
    assert response.status_code == 200
    assert response.json() == {"message": f"Signed up {email} for {activity}"}
    assert email in client.get("/activities").json()[activity]["participants"]


def test_duplicate_signup_returns_bad_request(client):
    # Arrange
    activity = "Chess Club"
    email = "michael@mergington.edu"

    # Act
    response = client.post(
        f"/activities/{activity}/signup",
        params={"email": email},
    )

    # Assert
    assert response.status_code == 400
    assert response.json()["detail"] == "Student already signed up for this activity"


def test_signup_for_unknown_activity_returns_not_found(client):
    # Arrange
    activity = "Photography Club"

    # Act
    response = client.post(
        f"/activities/{activity}/signup",
        params={"email": "student@mergington.edu"},
    )

    # Assert
    assert response.status_code == 404
    assert response.json()["detail"] == "Activity not found"


def test_signup_without_email_returns_unprocessable_entity(client):
    # Arrange
    activity = "Soccer Club"

    # Act
    response = client.post(f"/activities/{activity}/signup")

    # Assert
    assert response.status_code == 422


def test_signup_then_unregister_removes_participant(client):
    # Arrange
    activity = "Soccer Club"
    email = "leaving.student@mergington.edu"

    # Act: signup
    signup_response = client.post(
        f"/activities/{activity}/signup",
        params={"email": email},
    )

    # Assert: signup
    assert signup_response.status_code == 200

    # Act: unregister
    unregister_response = client.delete(
        f"/activities/{activity}/signup",
        params={"email": email},
    )

    # Assert: unregister
    assert unregister_response.status_code == 200
    assert unregister_response.json() == {
        "message": f"Unregistered {email} from {activity}"
    }
    assert email not in client.get("/activities").json()[activity]["participants"]


def test_unregister_from_unknown_activity_returns_not_found(client):
    # Arrange
    activity = "Photography Club"

    # Act
    response = client.delete(
        f"/activities/{activity}/signup",
        params={"email": "student@mergington.edu"},
    )

    # Assert
    assert response.status_code == 404
    assert response.json()["detail"] == "Activity not found"


def test_unregistering_non_participant_returns_not_found(client):
    # Arrange
    activity = "Soccer Club"
    email = "not.registered@mergington.edu"

    # Act
    response = client.delete(
        f"/activities/{activity}/signup",
        params={"email": email},
    )

    # Assert
    assert response.status_code == 404
    assert response.json()["detail"] == "Student is not signed up for this activity"


def test_unregister_without_email_returns_unprocessable_entity(client):
    # Arrange
    activity = "Soccer Club"

    # Act
    response = client.delete(f"/activities/{activity}/signup")

    # Assert
    assert response.status_code == 422


def test_root_redirects_to_static_index(client):
    # Arrange
    expected_location = "/static/index.html"

    # Act
    response = client.get("/", follow_redirects=False)

    # Assert
    assert response.status_code == 307
    assert response.headers["location"] == expected_location