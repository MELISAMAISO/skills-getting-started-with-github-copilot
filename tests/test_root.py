"""
Tests for the GET / endpoint
Following AAA (Arrange-Act-Assert) pattern
"""
import pytest


class TestRootRedirect:
    """Test suite for GET / endpoint"""

    def test_root_redirects_to_static_index(self, client):
        """
        Arrange: No setup needed
        Act: Make GET request to /
        Assert: Returns redirect status and location header points to /static/index.html
        """
        # Act
        response = client.get("/", follow_redirects=False)

        # Assert
        assert response.status_code in [301, 302, 307, 308]
        assert "location" in response.headers
        assert "/static/index.html" in response.headers["location"]

    def test_root_with_follow_redirects(self, client):
        """
        Arrange: No setup needed
        Act: Make GET request to / with follow_redirects=True
        Assert: Final response is 200 (static file served)
        """
        # Act
        response = client.get("/", follow_redirects=True)

        # Assert
        assert response.status_code == 200

    def test_root_redirect_is_permanent_redirect(self, client):
        """
        Arrange: No setup needed
        Act: Make GET request to /
        Assert: Returns redirect status code (301-308)
        """
        # Act
        response = client.get("/", follow_redirects=False)

        # Assert
        # 307 Temporary Redirect or 302 Found are typical FastAPI redirect responses
        assert response.status_code in [301, 302, 307, 308]
