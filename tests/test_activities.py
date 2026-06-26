"""
Tests for the GET /activities endpoint
Following AAA (Arrange-Act-Assert) pattern
"""
import pytest


class TestGetActivities:
    """Test suite for GET /activities endpoint"""

    def test_get_activities_returns_all_activities(self, client):
        """
        Arrange: No setup needed
        Act: Make GET request to /activities
        Assert: Returns 200 status and contains all expected activities
        """
        # Arrange
        expected_activities = [
            "Chess Club",
            "Programming Class",
            "Gym Class",
            "Soccer Team",
            "Swimming Club",
            "Art Studio",
            "Drama Club",
            "Science Lab",
            "Debate Team",
        ]

        # Act
        response = client.get("/activities")

        # Assert
        assert response.status_code == 200
        data = response.json()
        for activity_name in expected_activities:
            assert activity_name in data

    def test_get_activities_returns_correct_structure(self, client):
        """
        Arrange: No setup needed
        Act: Make GET request to /activities
        Assert: Each activity has required fields
        """
        # Arrange
        required_fields = {
            "description",
            "schedule",
            "max_participants",
            "participants",
        }

        # Act
        response = client.get("/activities")
        data = response.json()

        # Assert
        assert response.status_code == 200
        for activity_name, activity_details in data.items():
            assert isinstance(activity_details, dict)
            assert required_fields.issubset(set(activity_details.keys()))

    def test_get_activities_participants_is_list(self, client):
        """
        Arrange: No setup needed
        Act: Make GET request to /activities
        Assert: Participants field is a list
        """
        # Act
        response = client.get("/activities")
        data = response.json()

        # Assert
        assert response.status_code == 200
        for activity_details in data.values():
            assert isinstance(activity_details["participants"], list)
            for participant in activity_details["participants"]:
                assert isinstance(participant, str)

    def test_get_activities_max_participants_is_positive_integer(self, client):
        """
        Arrange: No setup needed
        Act: Make GET request to /activities
        Assert: max_participants is a positive integer
        """
        # Act
        response = client.get("/activities")
        data = response.json()

        # Assert
        assert response.status_code == 200
        for activity_details in data.values():
            assert isinstance(activity_details["max_participants"], int)
            assert activity_details["max_participants"] > 0
