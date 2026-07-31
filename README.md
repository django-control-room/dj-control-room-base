[![Django Control Room Panel](https://img.shields.io/badge/Django%20Control%20Room-Panel-0c4b33?logo=django)](https://github.com/django-control-room/dj-control-room)
[![Tests](https://github.com/django-control-room/dj-control-room-base/actions/workflows/test.yml/badge.svg)](https://github.com/django-control-room/dj-control-room-base/actions/workflows/test.yml)
[![codecov](https://codecov.io/gh/django-control-room/dj-control-room-base/branch/main/graph/badge.svg)](https://codecov.io/gh/django-control-room/dj-control-room-base)
[![PyPI version](https://badge.fury.io/py/dj-control-room-base.svg)](https://badge.fury.io/py/dj-control-room-base)
[![Python versions](https://img.shields.io/pypi/pyversions/dj-control-room-base.svg)](https://pypi.org/project/dj-control-room-base/)
[![Downloads](https://img.shields.io/pypi/dm/dj-control-room-base.svg)](https://pypi.org/project/dj-control-room-base/)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](https://opensource.org/licenses/MIT)

# dj-control-room-base

![dj-control-room-base - a core library for creating DCR panels](https://raw.githubusercontent.com/django-control-room/dj-control-room-base/main/images/dj-control-room-base.png)

**dj-control-room-base** is a core library for [Django Control Room](https://github.com/django-control-room/dj-control-room) panels. It provides the shared primitives that every panel needs: settings management, CSS injection, permission enforcement, admin sidebar integration, template context helpers, and MCP-style panel tools.

**Official Django Control Room panels** ship with this package as a dependency and build on these APIs rather than reimplementing them panel by panel.

**Optionally**, the package can also be mounted as a full panel in its own right: it ships a bundled design system reference UI and example patterns that are useful when building or theming new panels.

- **Official site:** [djangocontrolroom.com](https://djangocontrolroom.com)
- **Control Room app:** [dj-control-room](https://github.com/django-control-room/dj-control-room)
- **Docs:** [django-control-room.github.io/dj-control-room-base](https://django-control-room.github.io/dj-control-room-base/)

## What this library provides

- **Centralized CSS and permissions** - a single `PanelConfig` object per panel drives CSS injection, staff/group/superuser checks, and settings merging across built-in, panel, hub, and project layers.
- **Admin sidebar integration** - `PanelPlaceholderModel` and `BasePanelAdmin` give any panel a sidebar entry with no extra migrations.
- **Template context helpers** - `panel_config.get_context(request, ...)` returns a ready-to-use context with CSS and Django admin variables included.
- **Entry-point discovery** - panels register with the hub via a `PanelPlugin` subclass and a `pyproject.toml` entry point.
- **Panel tools** - optional, permission-scoped callables the `dj-control-room` hub aggregates for AI agent and in-admin chat integrations.
- **Theme adapters** - opt-in stylesheets that match panels to `django-unfold`, `django-jazzmin`, or `django-grappelli`.

See the [full documentation](https://django-control-room.github.io/dj-control-room-base/) for configuration options and a guide to building your own panel on this library.

## Requirements

- Python 3.9+
- Django 4.2+ (tested in CI across Django 4.2, 5.2, and 6.0)

## Quick start

```bash
pip install dj-control-room-base
```

```python
# settings.py
INSTALLED_APPS = [
    ...
    "dj_control_room_base",
]
```

```python
# urls.py
urlpatterns = [
    path("admin/dj-control-room-base/", include("dj_control_room_base.urls")),
    path("admin/", admin.site.urls),
]
```

```bash
python manage.py migrate
python manage.py runserver
```

Open `/admin/` and sign in. A **DJ CONTROL ROOM BASE** entry appears in the sidebar and links to the panel at `/admin/dj-control-room-base/`.

See [Installation](https://django-control-room.github.io/dj-control-room-base/installation/) for the complete walkthrough, [Configuration](https://django-control-room.github.io/dj-control-room-base/configuration/) for CSS/permission settings and theme adapters, and [Building Panels](https://django-control-room.github.io/dj-control-room-base/building-panels/) for a guide to building your own panel on this library.

## Development

```bash
git clone https://github.com/django-control-room/dj-control-room-base.git
cd dj-control-room-base
make install
make test_local
```

See [Development](https://django-control-room.github.io/dj-control-room-base/development/) for Docker setup, coverage, and the full Makefile reference.

## License

MIT. See [LICENSE](LICENSE).
