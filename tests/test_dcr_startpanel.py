import os
import shutil
import sys
import tempfile
import types
from io import StringIO

from django.conf import settings
from django.contrib import admin
from django.core.management import call_command
from django.core.management.base import CommandError
from django.test import override_settings
from django.urls import clear_url_caches, include, path

from .base import BasePanelTestCase


APP_NAME = "dcr_customer_lookup"
URLCONF_NAME = "dcr_startpanel_test_urls"


class TestDcrStartpanel(BasePanelTestCase):
    def setUp(self):
        super().setUp()
        self._cwd = os.getcwd()
        self.tmpdir = tempfile.mkdtemp(prefix="dcr_startpanel_")
        os.chdir(self.tmpdir)
        sys.path.insert(0, self.tmpdir)

    def tearDown(self):
        for model in list(admin.site._registry):
            if model._meta.app_label == APP_NAME:
                admin.site.unregister(model)
        if self.tmpdir in sys.path:
            sys.path.remove(self.tmpdir)
        os.chdir(self._cwd)
        shutil.rmtree(self.tmpdir, ignore_errors=True)
        super().tearDown()

    def test_command_creates_a_working_panel(self):
        call_command("dcr_startpanel", "customer_lookup", stdout=StringIO())

        for relative in (
            "apps.py",
            "admin.py",
            "models.py",
            "views.py",
            "panel.py",
            "conf.py",
            "urls.py",
            f"templates/admin/{APP_NAME}/index.html",
        ):
            self.assertTrue(
                os.path.isfile(os.path.join(APP_NAME, relative)),
                f"expected generated file {relative}",
            )

        with override_settings(INSTALLED_APPS=[*settings.INSTALLED_APPS, APP_NAME]):
            urlconf = types.ModuleType(URLCONF_NAME)
            urlconf.urlpatterns = [
                path("panel/", include(f"{APP_NAME}.urls")),
                path("admin/", admin.site.urls),
            ]
            sys.modules[URLCONF_NAME] = urlconf
            with override_settings(ROOT_URLCONF=URLCONF_NAME):
                clear_url_caches()
                response = self.client.get("/panel/")

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Customer Lookup")

    def test_rejects_name_that_is_not_a_python_identifier(self):
        # "customer-lookup" becomes "dcr_customer-lookup", which is not a
        # valid identifier, so the command must fail before writing an app.
        # this is actually functionality in the django startapp command
        with self.assertRaises(CommandError) as ctx:
            call_command("dcr_startpanel", "customer-lookup", stdout=StringIO())
        self.assertFalse(os.path.exists("dcr_customer-lookup"))
