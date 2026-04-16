"""
Tests for BasePanelAdmin — the reusable admin base class in core.
"""

from django.contrib import admin
from django.test import TestCase, RequestFactory
from django.contrib.auth import get_user_model

from dj_control_room_base.core import BasePanelAdmin, PanelPlaceholderModel


User = get_user_model()


class _FakePlaceholder(PanelPlaceholderModel):
    """Minimal placeholder used only for these tests."""
    class Meta(PanelPlaceholderModel.Meta):
        app_label = "dj_control_room_base"


class _TestPanelAdmin(BasePanelAdmin):
    redirect_url_name = "dj_control_room_base:index"


class TestBasePanelAdmin(TestCase):
    """Tests for BasePanelAdmin permissions and redirect behaviour."""

    def setUp(self):
        self.factory = RequestFactory()
        self.superuser = User.objects.create_superuser(
            username="admin", password="pass", email="admin@example.com"
        )
        self.staff_user = User.objects.create_user(
            username="staff", password="pass", is_staff=True
        )
        self.regular_user = User.objects.create_user(
            username="regular", password="pass", is_staff=False
        )
        self.model_admin = _TestPanelAdmin(
            model=_FakePlaceholder,
            admin_site=admin.site,
        )

    def _request(self, user):
        request = self.factory.get("/")
        request.user = user
        return request

    def test_changelist_view_redirects_to_panel(self):
        from django.urls import reverse
        response = self.model_admin.changelist_view(self._request(self.superuser))
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response["Location"], reverse("dj_control_room_base:index"))

    def test_has_add_permission_always_false(self):
        self.assertFalse(
            self.model_admin.has_add_permission(self._request(self.superuser))
        )

    def test_has_delete_permission_always_false(self):
        self.assertFalse(
            self.model_admin.has_delete_permission(self._request(self.superuser))
        )

    def test_has_change_permission_true_for_staff(self):
        self.assertTrue(
            self.model_admin.has_change_permission(self._request(self.staff_user))
        )

    def test_has_change_permission_false_for_regular_user(self):
        self.assertFalse(
            self.model_admin.has_change_permission(self._request(self.regular_user))
        )

    def test_has_view_permission_true_for_staff(self):
        self.assertTrue(
            self.model_admin.has_view_permission(self._request(self.staff_user))
        )

    def test_has_view_permission_false_for_regular_user(self):
        self.assertFalse(
            self.model_admin.has_view_permission(self._request(self.regular_user))
        )
