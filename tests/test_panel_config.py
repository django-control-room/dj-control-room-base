"""
Tests for PanelConfig — settings merging, CSS context, and template context.
"""

from unittest.mock import MagicMock

from django.test import TestCase, RequestFactory, override_settings

from dj_control_room_base.core import PanelConfig


_SETTINGS_KEY = "DJ_TEST_PANEL_SETTINGS"


class TestPanelConfigGetSettings(TestCase):
    """Tests for PanelConfig.get_settings() — precedence and merging."""

    def _make_config(self, defaults=None):
        return PanelConfig(settings_key=_SETTINGS_KEY, defaults=defaults)

    def test_returns_defaults_when_no_user_settings(self):
        config = self._make_config(defaults={"LOAD_DEFAULT_CSS": True, "EXTRA_CSS": []})
        result = config.get_settings()
        self.assertEqual(result, {"LOAD_DEFAULT_CSS": True, "EXTRA_CSS": []})

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

    def test_no_defaults_returns_empty_dict(self):
        config = PanelConfig(settings_key=_SETTINGS_KEY)
        result = config.get_settings()
        self.assertEqual(result, {})


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
    """Tests for PanelConfig.get_css_context() — CSS link rendering."""

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
    """Tests for PanelConfig.get_context() — full template context building."""

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
