from typing import Optional

import shutil
from pathlib import Path

from django.core.management import call_command
from django.core.management.base import BaseCommand, CommandError
from django.template import Context, Engine

import dj_control_room_base


class Command(BaseCommand):
    help = (
        "Creates a minimal internal Django Control Room panel as a regular "
        "Django app. Runs Django's startapp command, then overlays panel "
        "files. The app name is prefixed with dcr_ unless it already starts "
        "with that prefix. Named dcr_startpanel to avoid clashing with "
        "OpenStack Horizon's startpanel. For a publishable panel "
        "repository, use cookiecutter-dj-control-room-plugin instead."
    )
    missing_args_message = "You must provide an application name."

    APP_PREFIX = "dcr_"
    OVERLAY_PY = (
        "apps.py",
        "admin.py",
        "models.py",
        "views.py",
        "panel.py",
        "conf.py",
        "urls.py",
    )

    def add_arguments(self, parser):
        parser.add_argument("name", help="Name of the application.")
        parser.add_argument(
            "directory", nargs="?", help="Optional destination directory"
        )
        parser.add_argument(
            "--prefix",
            default=self.APP_PREFIX,
            help="App name prefix (default: dcr_).",
        )

    def handle(self, **options):
        raw_name = options["name"]
        directory = options["directory"]
        prefix = options["prefix"]

        # first call the usual django startapp command to generate the app directory
        app_name, app_dir = self.generate_stock_app(raw_name, directory, prefix)

        # Then add DCR specific files to the app directory and overwrite any files
        # that need to be changed.
        self.write_overlay(app_dir, app_name, prefix)

        # Notify calling user about what to do next (e.g. adding the app to INSTALLED_APPS and including the panel URLs)
        self.print_next_steps(app_name, app_name.replace("_", "-"))

    def apply_app_prefix(self, name: str, prefix: Optional[str] = None) -> str:
        """Return ``name`` with ``prefix``, without double-prefixing."""
        prefix = self.APP_PREFIX if prefix is None else prefix.lower()
        if name.startswith(prefix):
            return name
        return f"{prefix}{name}"

    def verbose_name_from_app(self, app_name: str, prefix: Optional[str] = None) -> str:
        """Human-readable title derived from the app label (minus ``prefix``)."""
        prefix = self.APP_PREFIX if prefix is None else prefix
        stem = app_name[len(prefix) :] if app_name.startswith(prefix) else app_name
        return stem.replace("_", " ").title()

    def generate_stock_app(
        self,
        name: str,
        directory: Optional[str] = None,
        prefix: Optional[str] = None,
    ) -> tuple[str, Path]:
        """
        Represents the first step of the process. This generates a stock django app
        via the usual startapp command.
        """
        prefix = self.APP_PREFIX if prefix is None else prefix
        if not name:
            raise CommandError(
                "'{name}' is not a valid app name. Please make sure the "
                "name is a valid identifier.".format(name=name)
            )

        app_name = self.apply_app_prefix(name, prefix)
        # Note that we first apply the prefix before checking validity. This is because this
        # command adds a prefix to the app name that can make the app name valid.
        # Example: 123_foo is not a valid app name, but dcr_123_foo is.
        if not app_name.isidentifier():
            raise CommandError(
                "'{name}' is not a valid app name. Please make sure the "
                "name is a valid identifier.".format(name=app_name)
            )

        startapp_args = [app_name]
        if directory:
            startapp_args.append(directory)
            app_dir = Path(directory).resolve()
        else:
            app_dir = Path.cwd() / app_name

        call_command("startapp", *startapp_args)
        return app_name, app_dir

    def write_overlay(
        self, app_dir: Path, app_name: str, prefix: Optional[str] = None
    ) -> None:
        """Add DCR files and replace the startapp stubs that need to change."""
        prefix = self.APP_PREFIX if prefix is None else prefix
        # Overlay templates shipped next to this package.
        overlay = (
            Path(dj_control_room_base.__file__).resolve().parent / "startpanel_overlay"
        )
        context = Context(
            {
                "app_name": app_name,
                # Same transform startapp uses for camel_case_app_name.
                "camel_case_app_name": "".join(
                    part for part in app_name.title() if part != "_"
                ),
                "verbose_name": self.verbose_name_from_app(app_name, prefix),
            },
            autoescape=False,
        )
        engine = Engine(autoescape=False)

        for name in self.OVERLAY_PY:
            src = overlay / f"{name}-tpl"
            dest = app_dir / name
            dest.write_text(
                engine.from_string(src.read_text(encoding="utf-8")).render(context),
                encoding="utf-8",
            )

        html_dest = app_dir / "templates" / "admin" / app_name / "index.html"
        html_dest.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(
            overlay / "templates" / "admin" / "app_name" / "index.html",
            html_dest,
        )

    def print_next_steps(self, app_name: str, url_path: str) -> None:
        self.stdout.write("")
        self.stdout.write(
            self.style.SUCCESS(f"Created internal Control Room panel app '{app_name}'.")
        )
        self.stdout.write("")
        self.stdout.write("Add this entry to INSTALLED_APPS:")
        self.stdout.write(f'    "{app_name}",')
        self.stdout.write("")
        self.stdout.write("Then include the panel URLs:")
        self.stdout.write(f'    path("admin/{url_path}/", include("{app_name}.urls")),')
        self.stdout.write("")
        self.stdout.write(
            "This command does not modify INSTALLED_APPS. "
            "List the app before dj_control_room so the hub sidebar picks it up."
        )
        self.stdout.write("")
