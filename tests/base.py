"""
Base test case for dj-control-room-base tests.
"""

from django.contrib.auth import get_user_model
from django.test import Client, TestCase


User = get_user_model()


class BasePanelTestCase(TestCase):
    """
    Base test case for DJ Control Room panel tests.
    Sets up an authenticated staff/superuser client.
    """

    def setUp(self):
        self.user = User.objects.create_user(
            username="admin",
            password="testpass123",
            is_staff=True,
            is_superuser=True,
        )
        self.client = Client()
        self.client.force_login(self.user)
