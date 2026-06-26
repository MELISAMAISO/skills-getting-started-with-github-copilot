"""
Tests for the DELETE /activities/{activity_name}/signup endpoint
Following AAA (Arrange-Act-Assert) pattern
"""
import pytest


class TestUnregisterHappyPath:
    """Happy path test cases for unregister endpoint"""

    def test_unregister_successful(self, client):
        """
        Arrange: Sign up a student, get activity state
        Act: Unregister the student
        Assert: Returns 200 status and confirmation message
        """
        # Arrange
        activity_name = "Chess Club"
        email = "student_to_remove@mergington.edu"
        
        # Pre-register the student
        client.post(
            f"/activities/{activity_name}/signup",
            params={"email": email}
        )

        # Act
        response = client.delete(
            f"/activities/{activity_name}/signup",
            params={"email": email}
        )

        # Assert
        assert response.status_code == 200
        data = response.json()
        assert "message" in data
        assert email in data["message"]
        assert activity_name in data["message"]

    def test_unregister_removes_participant(self, client):
        """
        Arrange: Sign up a student
        Act: Unregister the student
        Assert: Participant count decreases and student is removed
        """
        # Arrange
        activity_name = "Programming Class"
        email = "remove_me@mergington.edu"
        
        # Pre-register
        client.post(
            f"/activities/{activity_name}/signup",
            params={"email": email}
        )
        
        pre_removal_response = client.get("/activities")
        pre_removal_count = len(pre_removal_response.json()[activity_name]["participants"])

        # Act
        response = client.delete(
            f"/activities/{activity_name}/signup",
            params={"email": email}
        )

        # Assert
        assert response.status_code == 200
        
        post_removal_response = client.get("/activities")
        post_removal_count = len(post_removal_response.json()[activity_name]["participants"])
        assert post_removal_count == pre_removal_count - 1
        assert email not in post_removal_response.json()[activity_name]["participants"]

    def test_unregister_multiple_participants(self, client):
        """
        Arrange: Sign up multiple students to an activity
        Act: Remove each one
        Assert: Each removal works correctly
        """
        # Arrange
        activity_name = "Gym Class"
        emails = [
            "multi_test_1@mergington.edu",
            "multi_test_2@mergington.edu",
            "multi_test_3@mergington.edu",
        ]
        
        # Pre-register all students
        for email in emails:
            client.post(
                f"/activities/{activity_name}/signup",
                params={"email": email}
            )

        # Act & Assert
        for email in emails:
            response = client.delete(
                f"/activities/{activity_name}/signup",
                params={"email": email}
            )
            assert response.status_code == 200
            
            # Verify removal
            activities_response = client.get("/activities")
            assert email not in activities_response.json()[activity_name]["participants"]


class TestUnregisterErrorCases:
    """Error case test cases for unregister endpoint"""

    def test_unregister_activity_not_found(self, client):
        """
        Arrange: Use non-existent activity name
        Act: Attempt to unregister
        Assert: Returns 404 error
        """
        # Arrange
        nonexistent_activity = "NonExistent Activity"
        email = "test@mergington.edu"

        # Act
        response = client.delete(
            f"/activities/{nonexistent_activity}/signup",
            params={"email": email}
        )

        # Assert
        assert response.status_code == 404
        assert "Activity not found" in response.json()["detail"]

    def test_unregister_student_not_registered(self, client, sample_email):
        """
        Arrange: Use email that's not registered for activity
        Act: Attempt to unregister
        Assert: Returns 400 error
        """
        # Arrange
        activity_name = "Art Studio"

        # Act
        response = client.delete(
            f"/activities/{activity_name}/signup",
            params={"email": sample_email}
        )

        # Assert
        assert response.status_code == 400
        assert "not signed up" in response.json()["detail"]

    def test_unregister_twice(self, client):
        """
        Arrange: Sign up a student
        Act: Unregister twice
        Assert: Second unregister returns 400 error
        """
        # Arrange
        activity_name = "Swimming Club"
        email = "double_remove@mergington.edu"
        
        # Pre-register
        client.post(
            f"/activities/{activity_name}/signup",
            params={"email": email}
        )

        # First unregister should succeed
        first_response = client.delete(
            f"/activities/{activity_name}/signup",
            params={"email": email}
        )
        assert first_response.status_code == 200

        # Act - attempt second unregister
        second_response = client.delete(
            f"/activities/{activity_name}/signup",
            params={"email": email}
        )

        # Assert
        assert second_response.status_code == 400
        assert "not signed up" in second_response.json()["detail"]

    def test_unregister_existing_participant(self, client):
        """
        Arrange: Get an existing participant from an activity
        Act: Unregister that participant
        Assert: Returns 200 and participant is removed
        """
        # Arrange
        activity_name = "Debate Team"
        existing_response = client.get("/activities")
        existing_email = existing_response.json()[activity_name]["participants"][0]
        initial_count = len(existing_response.json()[activity_name]["participants"])

        # Act
        response = client.delete(
            f"/activities/{activity_name}/signup",
            params={"email": existing_email}
        )

        # Assert
        assert response.status_code == 200
        
        final_response = client.get("/activities")
        final_count = len(final_response.json()[activity_name]["participants"])
        assert final_count == initial_count - 1
        assert existing_email not in final_response.json()[activity_name]["participants"]
