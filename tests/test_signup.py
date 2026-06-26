"""
Tests for the POST /activities/{activity_name}/signup endpoint
Following AAA (Arrange-Act-Assert) pattern
"""
import pytest


class TestSignupHappyPath:
    """Happy path test cases for signup endpoint"""

    def test_signup_successful(self, client, sample_email):
        """
        Arrange: Get initial activity state
        Act: Sign up a new student
        Assert: Returns 200 status and confirmation message
        """
        # Arrange
        activity_name = "Chess Club"
        initial_response = client.get("/activities")
        initial_participants = initial_response.json()[activity_name]["participants"].copy()
        initial_count = len(initial_participants)

        # Act
        response = client.post(
            f"/activities/{activity_name}/signup",
            params={"email": sample_email}
        )

        # Assert
        assert response.status_code == 200
        data = response.json()
        assert "message" in data
        assert sample_email in data["message"]
        assert activity_name in data["message"]

    def test_signup_adds_participant_to_activity(self, client, sample_email):
        """
        Arrange: Get initial participant count
        Act: Sign up a new student
        Assert: Participant is added to the activity
        """
        # Arrange
        activity_name = "Programming Class"
        initial_response = client.get("/activities")
        initial_count = len(initial_response.json()[activity_name]["participants"])

        # Act
        client.post(
            f"/activities/{activity_name}/signup",
            params={"email": sample_email}
        )

        # Assert
        final_response = client.get("/activities")
        final_count = len(final_response.json()[activity_name]["participants"])
        assert final_count == initial_count + 1
        assert sample_email in final_response.json()[activity_name]["participants"]

    def test_signup_different_activities(self, client):
        """
        Arrange: Prepare emails for different activities
        Act: Sign up students to different activities
        Assert: Each student is in their respective activity
        """
        # Arrange
        test_cases = [
            ("Gym Class", "student1@mergington.edu"),
            ("Art Studio", "student2@mergington.edu"),
            ("Drama Club", "student3@mergington.edu"),
        ]

        # Act & Assert
        for activity_name, email in test_cases:
            response = client.post(
                f"/activities/{activity_name}/signup",
                params={"email": email}
            )
            assert response.status_code == 200

            final_response = client.get("/activities")
            assert email in final_response.json()[activity_name]["participants"]


class TestSignupErrorCases:
    """Error case test cases for signup endpoint"""

    def test_signup_activity_not_found(self, client, sample_email):
        """
        Arrange: Use non-existent activity name
        Act: Attempt to sign up
        Assert: Returns 404 error
        """
        # Arrange
        nonexistent_activity = "NonExistent Club"

        # Act
        response = client.post(
            f"/activities/{nonexistent_activity}/signup",
            params={"email": sample_email}
        )

        # Assert
        assert response.status_code == 404
        assert "Activity not found" in response.json()["detail"]

    def test_signup_duplicate_email(self, client):
        """
        Arrange: Sign up student to activity
        Act: Attempt to sign up same student again
        Assert: Returns 400 error
        """
        # Arrange
        activity_name = "Swimming Club"
        email = "duplicate@mergington.edu"
        
        # First signup should succeed
        client.post(
            f"/activities/{activity_name}/signup",
            params={"email": email}
        )

        # Act - attempt duplicate signup
        response = client.post(
            f"/activities/{activity_name}/signup",
            params={"email": email}
        )

        # Assert
        assert response.status_code == 400
        assert "already signed up" in response.json()["detail"]

    def test_signup_already_registered_participant(self, client):
        """
        Arrange: Get an existing participant from an activity
        Act: Attempt to sign up that participant again
        Assert: Returns 400 error
        """
        # Arrange
        activity_name = "Chess Club"
        existing_response = client.get("/activities")
        existing_email = existing_response.json()[activity_name]["participants"][0]

        # Act
        response = client.post(
            f"/activities/{activity_name}/signup",
            params={"email": existing_email}
        )

        # Assert
        assert response.status_code == 400
        assert "already signed up" in response.json()["detail"]

    def test_signup_special_characters_in_activity_name(self, client, sample_email):
        """
        Arrange: Use activity name with URL-encoded characters
        Act: Sign up with encoded activity name
        Assert: Returns 404 (activity not found) since it's invalid
        """
        # Act
        response = client.post(
            f"/activities/NonExistent%20Activity/signup",
            params={"email": sample_email}
        )

        # Assert
        assert response.status_code == 404
