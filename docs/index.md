# dj-control-room-base

![dj-control-room-base connects panels to shared CSS, permissions, templates, and the Control Room hub](https://raw.githubusercontent.com/django-control-room/dj-control-room-base/main/images/dj-control-room-base.png)

**dj-control-room-base** is the shared core library for [Django Control Room](https://django-control-room.github.io/dj-control-room/) panels: settings, CSS injection, permissions, admin sidebar integration, and template helpers. Official panels depend on it instead of reimplementing those pieces.

Optionally it can also be mounted as a panel itself, a design-system reference UI useful when building or theming new panels.

- **Official site:** [djangocontrolroom.com](https://djangocontrolroom.com)
- **Control Room app:** [dj-control-room](https://django-control-room.github.io/dj-control-room/)
- **Source:** [github.com/django-control-room/dj-control-room-base](https://github.com/django-control-room/dj-control-room-base)
- **PyPI:** [pypi.org/project/dj-control-room-base](https://pypi.org/project/dj-control-room-base/)

---

## Documentation

| Page | What you'll find |
|---|---|
| [Installation](installation.md) | Install, `INSTALLED_APPS`, URLs, and optional hub wiring |
| [Configuration](configuration.md) | `PanelConfig` settings, CSS, permissions, theme auto-detect |
| [Building Panels](building-panels.md) | Authoring a panel on this library (including panel tools) |
| [Theme Adapters](themes.md) | Supported admin skins, screenshots, and DIY adapters |
| [Design System](design-system.html) | Live reference UI for `dcr-*` components |
| [Contributing](contributing.md) | Contributing and local setup |

---

## Requirements

- Python 3.9+
- Django 4.2+ (tested against Django 4.2, 5.2, 6.0, and 6.1)

The only runtime dependency is Django. `dj-control-room` is optional and only needed for the centralized hub dashboard.

---

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

See [Installation](installation.md) for the full walkthrough.

---

## License

MIT. See the [LICENSE](https://github.com/django-control-room/dj-control-room-base/blob/main/LICENSE) file.
