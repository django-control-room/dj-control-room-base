[![Django Control Room Panel](https://img.shields.io/badge/Django%20Control%20Room-Panel-0c4b33?logo=django)](https://github.com/yassi/dj-control-room)
[![Tests](https://github.com/yassi/dj-control-room-base/actions/workflows/test.yml/badge.svg)](https://github.com/yassi/dj-control-room-base/actions/workflows/test.yml)
[![codecov](https://codecov.io/gh/yassi/dj-control-room-base/branch/main/graph/badge.svg)](https://codecov.io/gh/yassi/dj-control-room-base)
[![PyPI version](https://badge.fury.io/py/dj-control-room-base.svg)](https://badge.fury.io/py/dj-control-room-base)
[![Python versions](https://img.shields.io/pypi/pyversions/dj-control-room-base.svg)](https://pypi.org/project/dj-control-room-base/)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](https://opensource.org/licenses/MIT)

# dj-control-room-base

![Admin home - DJ Control Room Base in the sidebar](https://raw.githubusercontent.com/yassi/dj-control-room-base/main/images/dj-control-room-base.png)



**dj-control-room-base** is a **core library** for [Django Control Room](https://github.com/yassi/dj-control-room) panels. It provides functionality for managing panel configuration, context, permissions and styles. All featured panels (ones developed by the DCR team) will use this as a base library for creating new panels.

Additionally, this project is also an installable panel on its own. As a panel it provides
an interactive styleguide with examples that can make working on new panels all the more easier.

The library **centralizes settings** that every panel would otherwise duplicate: **CSS** (whether to load the default design-system bundle, extra stylesheets, and hub-level overrides) and **permissions** (staff checks, optional superuser-only mode, Django group allow lists, and **scoped** rules per view). Panel authors who adopt `PanelConfig`, the placeholder admin pattern (`PanelPlaceholderModel` / `BasePanelAdmin`), and the shared template context helpers get that behavior **for free** instead of wiring merges, decorators, and admin sidebar rules by hand on each project.

- **Official site:** [djangocontrolroom.com](https://djangocontrolroom.com)
- **Control Room app:** [dj-control-room](https://github.com/yassi/dj-control-room)

## Documentation

Published docs (MkDocs): [yassi.github.io/dj-control-room-base](https://yassi.github.io/dj-control-room-base/)

## What you get

- **Centralized CSS and permissions** - One `PanelConfig` + settings key merges defaults, project settings, and (when the hub is present) Control Room overrides. You declare policy once; views and the admin placeholder reuse it.
- **Discoverable panel** - Registers with Control Room via the `dj_control_room.panels` entry point (`pyproject.toml`); see `dj_control_room_base/panel.py`.
- **`PanelConfig`** - One object per panel: merges defaults, project settings, and Control Room overrides; helpers for template context, optional default and extra CSS, and **scoped** `permission_required` decorators.
- **`PanelPlaceholderModel` / `BasePanelAdmin`** - Sidebar entry under Django admin that redirects to your panel URL, with no writable admin actions; respects the same permission rules as your views when you attach `panel_config`.
- **Sample views** - Design system landing page (`index`) and reference examples (`examples`), useful as copy-paste starting points.
- **Shipped assets** - Templates and static files under `dj_control_room_base/templates/` and `dj_control_room_base/static/`.

This package declares **Django** as its only runtime dependency. Using the full Control Room dashboard requires installing **`dj-control-room`** separately (see below).

## Screenshots

Django admin picks up a sidebar entry for this panel (placeholder model, no extra migrations for app tables):

![Admin home - DJ Control Room Base in the sidebar](https://raw.githubusercontent.com/yassi/dj-control-room-base/main/images/admin_home.png)

## Requirements

- Python 3.9+
- Django 4.2+ (tested in CI across Django 4.2, 5.2, and 6.0)


## Project layout

```
dj-control-room-base/
├── dj_control_room_base/
│   ├── core/              # PanelConfig, BasePanelAdmin, PanelPlaceholderModel
│   ├── templates/         # Panel templates
│   ├── static/            # Design system CSS and assets
│   ├── conf.py            # PanelConfig instance + settings key
│   ├── panel.py           # Control Room entry-point panel class
│   ├── views.py
│   ├── urls.py
│   ├── admin.py
│   └── models.py          # Placeholder model for admin sidebar
├── example_project/       # Runnable demo + pytest settings
├── tests/
├── mkdocs.yml             # Documentation site
└── requirements.txt       # Dev / demo deps (includes dj-control-room)
```


## Install and wire into Django

### 1. Install

```bash
pip install dj-control-room-base
```

For the Control Room hub UI:

```bash
pip install dj-control-room
```

### 2. `INSTALLED_APPS`

```python
INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "dj_control_room_base",
    # Optional: centralized dashboard
    # "dj_control_room",
]
```

### 3. URL include

Mount the panel under the admin namespace (path can differ; keep it consistent with how you document links):

```python
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin/dj-control-room-base/", include("dj_control_room_base.urls")),
    path("admin/", admin.site.urls),
]
```

With Control Room:

```python
urlpatterns = [
    path("admin/dj-control-room-base/", include("dj_control_room_base.urls")),
    path("admin/dj-control-room/", include("dj_control_room.urls")),
    path("admin/", admin.site.urls),
]
```

The placeholder model’s admin changelist redirects to `dj_control_room_base:index`, so staff users land on the panel home after clicking the sidebar entry.

### 4. Settings (optional)

`dj_control_room_base.conf` defines `panel_config` with settings key **`DJ_CONTROL_ROOM_BASE_SETTINGS`**. You can override defaults from your project:

```python
DJ_CONTROL_ROOM_BASE_SETTINGS = {
    "LOAD_DEFAULT_CSS": True,
    "EXTRA_CSS": [],
    # Panel-wide permission defaults (scopes can override below)
    "ALLOWED_GROUPS": [],
    "REQUIRE_SUPERUSER": False,
    # Per-view scopes, keyed to match @panel_config.permission_required("...")
    "SCOPE_PERMISSIONS": {
        "design-system": {
            "ALLOWED_GROUPS": [],
            "REQUIRE_SUPERUSER": False,
        },
        "examples": {
            "ALLOWED_GROUPS": [],
            "REQUIRE_SUPERUSER": False,
        },
    },
}
```

Rules of thumb:

- Users must be **staff** (and authenticated) to reach panel views; anonymous users are redirected to the admin login.
- **Superusers** bypass group checks but must still be staff.
- If `ALLOWED_GROUPS` is non-empty for a scope, the user must belong to one of those groups (by name).
- If `REQUIRE_SUPERUSER` is true for a scope, only superusers pass.

When Control Room is installed, it can inject overrides into the same merged settings (see `PanelConfig.get_settings()` / `apply_override_settings` in code).


### 5. Run the server

```bash
python manage.py migrate
python manage.py createsuperuser   # if needed
python manage.py runserver
```

Open `/admin/`, sign in, and use the **Dj Control Room Base** entry in the sidebar, or go directly to `/admin/dj-control-room-base/`.

**Note:** The placeholder model uses `managed = False`; you do not run migrations for `dj_control_room_base` tables. You still run `migrate` for Django’s built-in apps.


## Django Control Room dashboard

1. Add `dj_control_room` to `INSTALLED_APPS` (with `dj_control_room_base`).
2. Include `path("admin/dj-control-room/", include("dj_control_room.urls"))` as above.
3. Open `/admin/dj-control-room/` to see registered panels (this package advertises itself via the `dj_control_room.panels` entry point).

Panel metadata (name, description, icon, docs/PyPI links) lives in `dj_control_room_base/panel.py`; customize a fork or your own panel package the same way.


## Building your own panel on this package

Import primitives from `dj_control_room_base.core`:

- **`PanelConfig`** - Instantiate in `conf.py` with your settings key and defaults; use `get_context`, `permission_required`, and CSS helpers in views.
- **`PanelPlaceholderModel`** - Abstract `managed=False` base for a sidebar-only model.
- **`BasePanelAdmin`** - Redirect changelist to your `namespace:index` URL; set `panel_config` for aligned permissions.

Copy the entry-point pattern from `pyproject.toml`:

```toml
[project.entry-points."dj_control_room.panels"]
my_panel = "my_panel.panel:MyPanel"
```


## Development

Clone and install in editable mode with dev dependencies:

```bash
git clone https://github.com/yassi/dj-control-room-base.git
cd dj-control-room-base
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
make install                # pip install -r requirements.txt && pip install -e .
```

Run tests locally (uses SQLite by default via `example_project` settings):

```bash
make test_local
# or: python -m pytest tests/ -v
```

Coverage:

```bash
make test_coverage
```

Docker Compose provides a **dev** container (app on port 8000) and optional **Postgres**. From the repo root:

```bash
make docker_up
make docker_shell    # working directory: /app/example_project
```

Inside the container you can run `python manage.py runserver 0.0.0.0:8000` or pytest. For Postgres-backed runs, set `DB_ENGINE=postgresql` and point host/user/password at the `postgres` service.

Documentation:

```bash
make docs          # mkdocs build
make docs_serve    # local preview
```


## License

MIT. See [LICENSE](LICENSE).
