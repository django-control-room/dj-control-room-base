"""
Tests for PanelConfig - settings merging, CSS context, and template context.
"""

from unittest.mock import MagicMock

from django.contrib.auth import get_user_model
from django.contrib.auth.models import AnonymousUser, Group
from django.core.exceptions import PermissionDenied
from django.test import TestCase, RequestFactory, override_settings

from dj_control_room_base.core import PanelConfig, PANEL_BUILTIN_DEFAULTS


User = get_user_model()


_SETTINGS_KEY = "DJ_TEST_PANEL_SETTINGS"


class TestPanelConfigGetSettings(TestCase):
    """Tests for PanelConfig.get_settings() - precedence and merging."""

    def _make_config(self, defaults=None):
        return PanelConfig(settings_key=_SETTINGS_KEY, defaults=defaults)

    def test_returns_defaults_when_no_user_settings(self):
        config = self._make_config(defaults={"LOAD_DEFAULT_CSS": True, "EXTRA_CSS": []})
        result = config.get_settings()
        self.assertEqual(
            result,
            {
                **PANEL_BUILTIN_DEFAULTS,
                "LOAD_DEFAULT_CSS": True,
                "EXTRA_CSS": [],
            },
        )

    def test_permission_keys_exist_without_explicit_panel_defaults(self):
        """Permission-related keys come from builtins when omitted from panel defaults."""
        config = self._make_config(defaults={"FOO": "bar"})
        result = config.get_settings()
        self.assertEqual(result["FOO"], "bar")
        self.assertEqual(result["ALLOWED_GROUPS"], [])
        self.assertFalse(result["REQUIRE_SUPERUSER"])
        self.assertEqual(result["SCOPE_PERMISSIONS"], {})

    @override_settings(**{_SETTINGS_KEY: {"LOAD_DEFAULT_CSS": False}})
    def test_user_settings_override_defaults(self):
        config = self._make_config(defaults={"LOAD_DEFAULT_CSS": True, "EXTRA_CSS": []})
        result = config.get_settings()
        self.assertFalse(result["LOAD_DEFAULT_CSS"])
        self.assertEqual(result["EXTRA_CSS"], [])

    @override_settings(**{_SETTINGS_KEY: {"LOAD_DEFAULT_CSS": False}})
    def test_user_settings_take_precedence_over_overrides(self):
        config = self._make_config(defaults={"LOAD_DEFAULT_CSS": True, "EXTRA_CSS": []})
        config.apply_override_settings({"LOAD_DEFAULT_CSS": True})
        result = config.get_settings()
        # User-defined per-panel key wins over override settings
        self.assertFalse(result["LOAD_DEFAULT_CSS"])

    def test_override_settings_take_precedence_over_defaults(self):
        config = self._make_config(defaults={"LOAD_DEFAULT_CSS": True, "EXTRA_CSS": []})
        config.apply_override_settings({"LOAD_DEFAULT_CSS": False})
        result = config.get_settings()
        self.assertFalse(result["LOAD_DEFAULT_CSS"])

    def test_get_settings_with_key_returns_single_value(self):
        config = self._make_config(defaults={"LOAD_DEFAULT_CSS": True, "EXTRA_CSS": []})
        self.assertTrue(config.get_settings("LOAD_DEFAULT_CSS"))
        self.assertEqual(config.get_settings("EXTRA_CSS"), [])

    @override_settings(**{_SETTINGS_KEY: {"LOAD_DEFAULT_CSS": False}})
    def test_get_settings_with_key_reflects_user_settings(self):
        config = self._make_config(defaults={"LOAD_DEFAULT_CSS": True, "EXTRA_CSS": []})
        self.assertFalse(config.get_settings("LOAD_DEFAULT_CSS"))

    def test_get_settings_with_unknown_key_returns_none(self):
        config = self._make_config(defaults={"LOAD_DEFAULT_CSS": True})
        self.assertIsNone(config.get_settings("NONEXISTENT_KEY"))

    @override_settings(**{_SETTINGS_KEY: None})
    def test_none_user_settings_falls_back_to_defaults(self):
        config = self._make_config(defaults={"LOAD_DEFAULT_CSS": True, "EXTRA_CSS": []})
        result = config.get_settings()
        self.assertTrue(result["LOAD_DEFAULT_CSS"])

    def test_no_panel_defaults_merges_builtins_only(self):
        config = PanelConfig(settings_key=_SETTINGS_KEY)
        result = config.get_settings()
        self.assertEqual(result, dict(PANEL_BUILTIN_DEFAULTS))


class TestPanelConfigApplyOverrideSettings(TestCase):
    """Tests for PanelConfig.apply_override_settings()."""

    def test_apply_override_settings_stores_overrides(self):
        config = PanelConfig(settings_key=_SETTINGS_KEY)
        config.apply_override_settings({"LOAD_DEFAULT_CSS": False})
        self.assertEqual(config._override_settings, {"LOAD_DEFAULT_CSS": False})

    def test_apply_override_settings_replaces_previous_overrides(self):
        config = PanelConfig(settings_key=_SETTINGS_KEY)
        config.apply_override_settings({"LOAD_DEFAULT_CSS": False})
        config.apply_override_settings({"EXTRA_CSS": ["new.css"]})
        self.assertEqual(config._override_settings, {"EXTRA_CSS": ["new.css"]})


class TestPanelConfigGetCssContext(TestCase):
    """Tests for PanelConfig.get_css_context() - CSS link rendering."""

    def test_load_default_css_true_in_context(self):
        config = PanelConfig(
            settings_key=_SETTINGS_KEY,
            defaults={"LOAD_DEFAULT_CSS": True, "EXTRA_CSS": []},
        )
        ctx = config.get_css_context()
        self.assertTrue(ctx["dj_cr_load_default_css"])

    @override_settings(**{_SETTINGS_KEY: {"LOAD_DEFAULT_CSS": False}})
    def test_load_default_css_false_in_context(self):
        config = PanelConfig(
            settings_key=_SETTINGS_KEY,
            defaults={"LOAD_DEFAULT_CSS": True, "EXTRA_CSS": []},
        )
        ctx = config.get_css_context()
        self.assertFalse(ctx["dj_cr_load_default_css"])

    def test_extra_css_empty_produces_empty_string(self):
        config = PanelConfig(
            settings_key=_SETTINGS_KEY,
            defaults={"LOAD_DEFAULT_CSS": True, "EXTRA_CSS": []},
        )
        ctx = config.get_css_context()
        self.assertEqual(str(ctx["dj_cr_extra_css"]), "")

    def test_extra_css_absolute_url_renders_link_tag(self):
        config = PanelConfig(
            settings_key=_SETTINGS_KEY,
            defaults={"LOAD_DEFAULT_CSS": True, "EXTRA_CSS": ["https://cdn.example.com/theme.css"]},
        )
        ctx = config.get_css_context()
        self.assertIn('href="https://cdn.example.com/theme.css"', str(ctx["dj_cr_extra_css"]))

    def test_extra_css_protocol_relative_url_renders_link_tag(self):
        config = PanelConfig(
            settings_key=_SETTINGS_KEY,
            defaults={"LOAD_DEFAULT_CSS": True, "EXTRA_CSS": ["//cdn.example.com/theme.css"]},
        )
        ctx = config.get_css_context()
        self.assertIn('href="//cdn.example.com/theme.css"', str(ctx["dj_cr_extra_css"]))

    @override_settings(STATIC_URL="/static/", **{_SETTINGS_KEY: {"EXTRA_CSS": ["mypanel/css/overrides.css"]}})
    def test_extra_css_static_path_resolves_via_static(self):
        config = PanelConfig(
            settings_key=_SETTINGS_KEY,
            defaults={"LOAD_DEFAULT_CSS": True, "EXTRA_CSS": []},
        )
        ctx = config.get_css_context()
        self.assertIn("mypanel/css/overrides.css", str(ctx["dj_cr_extra_css"]))
        self.assertIn("<link", str(ctx["dj_cr_extra_css"]))

    def test_multiple_extra_css_entries_render_multiple_link_tags(self):
        config = PanelConfig(
            settings_key=_SETTINGS_KEY,
            defaults={
                "LOAD_DEFAULT_CSS": True,
                "EXTRA_CSS": ["https://a.example.com/a.css", "https://b.example.com/b.css"],
            },
        )
        ctx = config.get_css_context()
        output = str(ctx["dj_cr_extra_css"])
        self.assertIn("a.example.com/a.css", output)
        self.assertIn("b.example.com/b.css", output)
        self.assertEqual(output.count("<link"), 2)


class TestPanelConfigGetContext(TestCase):
    """Tests for PanelConfig.get_context() - full template context building."""

    def setUp(self):
        self.factory = RequestFactory()
        self.config = PanelConfig(
            settings_key=_SETTINGS_KEY,
            defaults={"LOAD_DEFAULT_CSS": True, "EXTRA_CSS": []},
        )

    def _make_request(self):
        request = self.factory.get("/")
        request.user = MagicMock(is_active=True, is_staff=True)
        return request

    def test_context_includes_css_context_keys(self):
        ctx = self.config.get_context(self._make_request())
        self.assertIn("dj_cr_load_default_css", ctx)
        self.assertIn("dj_cr_extra_css", ctx)

    def test_extra_kwargs_are_included_in_context(self):
        ctx = self.config.get_context(self._make_request(), title="My Panel", foo="bar")
        self.assertEqual(ctx["title"], "My Panel")
        self.assertEqual(ctx["foo"], "bar")

    def test_extra_kwargs_override_css_context_if_keys_collide(self):
        ctx = self.config.get_context(self._make_request(), dj_cr_load_default_css=False)
        self.assertFalse(ctx["dj_cr_load_default_css"])


class TestPanelConfigHasPermission(TestCase):
    """Tests for PanelConfig.has_permission() - panel-level and scope-level access."""

    def setUp(self):
        self.factory = RequestFactory()
        self.staff_user = User.objects.create_user(
            username="staff", password="pass", is_staff=True
        )
        self.superuser = User.objects.create_superuser(
            username="super", password="pass", email="super@example.com"
        )
        self.regular_user = User.objects.create_user(
            username="regular", password="pass", is_staff=False
        )
        self.group = Group.objects.create(name="ops")

    def _config(self, overrides=None):
        config = PanelConfig(settings_key=_SETTINGS_KEY, defaults={})
        if overrides:
            config.apply_override_settings(overrides)
        return config

    def _request(self, user):
        request = self.factory.get("/")
        request.user = user
        return request

    # --- default behaviour (any staff) ---

    def test_staff_allowed_by_default(self):
        config = self._config()
        self.assertTrue(config.has_permission(self._request(self.staff_user)))

    def test_superuser_allowed_by_default(self):
        config = self._config()
        self.assertTrue(config.has_permission(self._request(self.superuser)))

    def test_regular_user_denied_by_default(self):
        config = self._config()
        self.assertFalse(config.has_permission(self._request(self.regular_user)))

    # --- ALLOWED_GROUPS ---

    def test_staff_in_group_allowed(self):
        self.staff_user.groups.add(self.group)
        config = self._config({"ALLOWED_GROUPS": ["ops"]})
        self.assertTrue(config.has_permission(self._request(self.staff_user)))

    def test_staff_not_in_group_denied(self):
        config = self._config({"ALLOWED_GROUPS": ["ops"]})
        self.assertFalse(config.has_permission(self._request(self.staff_user)))

    def test_superuser_bypasses_allowed_groups(self):
        config = self._config({"ALLOWED_GROUPS": ["ops"]})
        self.assertTrue(config.has_permission(self._request(self.superuser)))

    # --- REQUIRE_SUPERUSER ---

    def test_superuser_allowed_when_required(self):
        config = self._config({"REQUIRE_SUPERUSER": True})
        self.assertTrue(config.has_permission(self._request(self.superuser)))

    def test_staff_denied_when_superuser_required(self):
        config = self._config({"REQUIRE_SUPERUSER": True})
        self.assertFalse(config.has_permission(self._request(self.staff_user)))

    def test_require_superuser_takes_precedence_over_allowed_groups(self):
        """REQUIRE_SUPERUSER wins; ALLOWED_GROUPS is ignored."""
        self.staff_user.groups.add(self.group)
        config = self._config({"REQUIRE_SUPERUSER": True, "ALLOWED_GROUPS": ["ops"]})
        self.assertFalse(config.has_permission(self._request(self.staff_user)))
        self.assertTrue(config.has_permission(self._request(self.superuser)))

    # --- SCOPE_PERMISSIONS ---

    def test_scope_inherits_panel_level_when_not_overridden(self):
        config = self._config({"ALLOWED_GROUPS": ["ops"]})
        self.assertFalse(config.has_permission(self._request(self.staff_user), scope="examples"))
        self.assertTrue(config.has_permission(self._request(self.superuser), scope="examples"))

    def test_scope_overrides_allowed_groups(self):
        self.staff_user.groups.add(self.group)
        config = self._config({
            "ALLOWED_GROUPS": [],
            "SCOPE_PERMISSIONS": {"examples": {"ALLOWED_GROUPS": ["ops"]}},
        })
        self.assertTrue(config.has_permission(self._request(self.staff_user), scope="examples"))
        # panel-level still allows any staff
        self.assertTrue(config.has_permission(self._request(self.staff_user)))

    def test_scope_overrides_require_superuser(self):
        config = self._config({
            "REQUIRE_SUPERUSER": False,
            "SCOPE_PERMISSIONS": {"danger": {"REQUIRE_SUPERUSER": True}},
        })
        self.assertFalse(config.has_permission(self._request(self.staff_user), scope="danger"))
        self.assertTrue(config.has_permission(self._request(self.superuser), scope="danger"))
        # panel-level still allows any staff
        self.assertTrue(config.has_permission(self._request(self.staff_user)))

    def test_scope_with_no_overrides_behaves_as_panel_level(self):
        config = self._config({
            "SCOPE_PERMISSIONS": {"examples": {}},
        })
        self.assertTrue(config.has_permission(self._request(self.staff_user), scope="examples"))

    def test_unknown_scope_falls_back_to_panel_level(self):
        config = self._config({"ALLOWED_GROUPS": ["ops"]})
        self.assertFalse(config.has_permission(self._request(self.staff_user), scope="nonexistent"))
        self.assertTrue(config.has_permission(self._request(self.superuser), scope="nonexistent"))


class TestPanelConfigPermissionRequired(TestCase):
    """Tests for the permission_required decorator."""

    def setUp(self):
        self.factory = RequestFactory()
        self.staff_user = User.objects.create_user(
            username="staff", password="pass", is_staff=True
        )
        self.regular_user = User.objects.create_user(
            username="regular", password="pass", is_staff=False
        )

    def _config(self, overrides=None):
        config = PanelConfig(settings_key=_SETTINGS_KEY, defaults={})
        if overrides:
            config.apply_override_settings(overrides)
        return config

    def _request(self, user, path="/panel/"):
        request = self.factory.get(path)
        request.user = user
        return request

    def test_authorised_user_reaches_view(self):
        config = self._config()
        sentinel = object()

        @config.permission_required()
        def view(request):
            return sentinel

        self.assertIs(view(self._request(self.staff_user)), sentinel)

    def test_unauthenticated_user_redirected_to_login(self):
        config = self._config()

        @config.permission_required()
        def view(request):
            pass  # pragma: no cover

        request = self.factory.get("/panel/")
        request.user = AnonymousUser()
        response = view(request)
        self.assertEqual(response.status_code, 302)
        self.assertIn("/admin/login/", response["Location"])

    def test_redirect_preserves_next_url(self):
        config = self._config()

        @config.permission_required()
        def view(request):
            pass  # pragma: no cover

        request = self.factory.get("/panel/index/")
        request.user = AnonymousUser()
        response = view(request)
        self.assertIn("next=", response["Location"])
        self.assertIn("/panel/index/", response["Location"])

    def test_authenticated_non_staff_raises_403(self):
        config = self._config()

        @config.permission_required()
        def view(request):
            pass  # pragma: no cover

        with self.assertRaises(PermissionDenied):
            view(self._request(self.regular_user))

    def test_scope_restriction_raises_403_for_staff(self):
        config = self._config({
            "SCOPE_PERMISSIONS": {"examples": {"REQUIRE_SUPERUSER": True}},
        })

        @config.permission_required("examples")
        def view(request):
            pass  # pragma: no cover

        with self.assertRaises(PermissionDenied):
            view(self._request(self.staff_user))

    def test_decorator_preserves_view_name(self):
        config = self._config()

        @config.permission_required()
        def my_named_view(request):
            pass

        self.assertEqual(my_named_view.__name__, "my_named_view")
