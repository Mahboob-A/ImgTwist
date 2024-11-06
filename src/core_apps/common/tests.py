from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase


class HealthCheckTests(APITestCase):
    """Test suite for the HealthCheck API view."""

    def setUp(self):
        """Set up data for the tests."""
        self.url = reverse("healthcheck")

    def test_healthcheck_success_status(self):
        """Test that healthcheck endpoint returns 200 OK status."""
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_healthcheck_response_content(self):
        """Test that healthcheck endpoint returns correct JSON response."""
        response = self.client.get(self.url)
        self.assertEqual(response.data, {"status": "OK"})

    def test_healthcheck_accessible_without_auth(self):
        """Test that healthcheck endpoint is accessible without authentication."""
        # First verify we're not authenticated
        self.assertFalse(self._is_authenticated())

        # Make request and verify success
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def _is_authenticated(self):
        """Helper method to check if current client is authenticated."""
        return hasattr(self.client, "credentials") and bool(self.client.credentials())
