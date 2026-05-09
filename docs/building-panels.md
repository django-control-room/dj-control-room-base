# Building Panels

This guide is for panel authors who want to build a new Django Control Room panel using `dj-control-room-base` as the core library.

By building on this library you get CSS injection, permission enforcement, admin sidebar integration, and template context helpers for free - without reimplementing them per panel.

---

## Prerequisites

Your panel will be a standard Django app distributed as a Python package. It needs to:

1. Declare `dj-control-room-base` as a dependency in `pyproject.toml`.
2. Register itself with Control Room via an entry point.
3. Use `PanelConfig` from `dj_control_room_base.core` in its own `conf.py`.

---

## 1. Declare the dependency

```toml
# pyproject.toml
[project]
name = "dj-my-panel"
dependencies = [
    "Django>=4.2",
    "dj-control-room-base>=0.1.0",
]
```

---

## 2. Register the entry point

Control Room discovers installed panels by scanning the `dj_control_room.panels` entry point group. Add one entry that points to your panel class:

```toml
# pyproject.toml
[project.entry-points."dj_control_room.panels"]
dj_my_panel = "dj_my_panel.panel:MyPanel"
```

---

## 3. Create the panel class

The panel class provides metadata that Control Room displays on the hub dashboard. Create `panel.py` in your app:

```python
# dj_my_panel/panel.py

class MyPanel:
    name = "My Panel"
    description = "A short description of what this panel does."
    icon = "database"           # icon name from the design system
    app_name = "dj_my_panel"   # must match the app label in INSTALLED_APPS
    docs_url = "https://github.com/yourname/dj-my-panel"
    pypi_url = "https://pypi.org/project/dj-my-panel/"

    def get_url_name(self):
        return "index"
```

---

## 4. Create `conf.py`

Instantiate `PanelConfig` once. This object is the single source of truth for your panel's settings, CSS, and permission logic.

```python
# dj_my_panel/conf.py
from dj_control_room_base.core import PanelConfig

panel_config = PanelConfig(
    settings_key="DJ_MY_PANEL_SETTINGS",
    defaults={
        "LOAD_DEFAULT_CSS": True,
        "EXTRA_CSS": [],
    },
)
```

`settings_key` is the Django settings variable that project owners use to configure your panel. The `defaults` dict is the fallback when the project hasn't set that variable.

You do not need to declare `ALLOWED_GROUPS`, `REQUIRE_SUPERUSER`, or `SCOPE_PERMISSIONS` in `defaults` - those are provided automatically by the built-in defaults (`PANEL_BUILTIN_DEFAULTS`).

---

## 5. Write views

Use `@panel_config.permission_required("scope-name")` to protect views and `panel_config.get_context(request, ...)` to build the template context. Both use the same merged settings, so they stay in sync automatically.

```python
# dj_my_panel/views.py
from django.shortcuts import render
from .conf import panel_config


@panel_config.permission_required("dashboard")
def dashboard(request):
    context = panel_config.get_context(request, title="My Panel")
    return render(request, "dj_my_panel/dashboard.html", context)


@panel_config.permission_required("detail")
def detail(request, pk):
    context = panel_config.get_context(request, title="Detail View")
    return render(request, "dj_my_panel/detail.html", context)
```

The scope string (`"dashboard"`, `"detail"`) becomes a key in `SCOPE_PERMISSIONS` that project owners can override without touching your code:

```python
# In the project's settings.py
DJ_MY_PANEL_SETTINGS = {
    "SCOPE_PERMISSIONS": {
        "dashboard": {"ALLOWED_GROUPS": ["ops"]},
        "detail": {"REQUIRE_SUPERUSER": True},
    }
}
```

---

## 6. Register URLs

```python
# dj_my_panel/urls.py
from django.urls import path
from . import views

app_name = "dj_my_panel"

urlpatterns = [
    path("", views.dashboard, name="index"),
    path("<int:pk>/", views.detail, name="detail"),
]
```

The `app_name` must match `panel.app_name` and the `app_name` in `AppConfig`.

---

## 7. Add the admin sidebar entry

Use `PanelPlaceholderModel` and `BasePanelAdmin` to register a Django admin sidebar entry that redirects to your panel's main view. No database table is created.

```python
# dj_my_panel/models.py
from dj_control_room_base.core import PanelPlaceholderModel

class MyPanelPlaceholder(PanelPlaceholderModel):
    class Meta(PanelPlaceholderModel.Meta):
        verbose_name = "My Panel"
        verbose_name_plural = "My Panel"
```

```python
# dj_my_panel/admin.py
from django.contrib import admin
from dj_control_room_base.core import BasePanelAdmin
from .conf import panel_config
from .models import MyPanelPlaceholder


@admin.register(MyPanelPlaceholder)
class MyPanelAdmin(BasePanelAdmin):
    redirect_url_name = "dj_my_panel:index"
    panel_config = panel_config
```

Attaching `panel_config` to `BasePanelAdmin` means the sidebar entry is only visible to users who have permission to access the panel. The same permission rules configured in `DJ_MY_PANEL_SETTINGS` apply to the admin entry automatically.

---

## 8. Create templates

Extend `panel_base.html` (shipped with this library) to inherit the design system CSS wiring and Django admin chrome:

```html
{% extends "admin/dj_control_room_base/panel_base.html" %}

{% block content %}
  <div class="dcr-page-header">
    <h1 class="dcr-page-header__title">My Panel</h1>
  </div>
  <!-- your panel content -->
{% endblock %}
```

The base template automatically handles `dj_cr_load_default_css` and `dj_cr_extra_css` from the context, so CSS injection requires no additional template code.

---

## Full `conf.py` / `views.py` example

```python
# conf.py
from dj_control_room_base.core import PanelConfig

panel_config = PanelConfig(
    settings_key="DJ_MY_PANEL_SETTINGS",
    defaults={
        "LOAD_DEFAULT_CSS": True,
        "EXTRA_CSS": [],
    },
)
```

```python
# views.py
from django.shortcuts import render
from .conf import panel_config


@panel_config.permission_required("main")
def index(request):
    context = panel_config.get_context(request, title="My Panel")
    context["items"] = get_items()  # add your own data
    return render(request, "dj_my_panel/index.html", context)
```

That is the full wiring. One `PanelConfig` declaration in `conf.py` gives all views:

- Consistent permission enforcement
- Automatic CSS injection
- Full Django admin context (breadcrumbs, sidebar, CSRF token, etc.)
- Centralized project-level override via `DJ_MY_PANEL_SETTINGS`

---

## `PanelConfig` API reference

### `PanelConfig(settings_key, defaults=None)`

Instantiate once in `conf.py`.

| Argument | Type | Description |
|---|---|---|
| `settings_key` | `str` | The Django settings variable name (e.g. `"DJ_MY_PANEL_SETTINGS"`). |
| `defaults` | `dict` | Panel-level defaults merged above built-in defaults but below hub and project settings. |

### `panel_config.get_settings(key=None)`

Returns the fully merged settings dict. Pass a key string to retrieve a single value.

### `panel_config.get_context(request, **extra)`

Returns a template context dict with the Django admin context, CSS injection variables, and any extra kwargs. Use this in every view.

### `panel_config.get_css_context()`

Returns only the CSS portion of the context (`dj_cr_load_default_css`, `dj_cr_extra_css`). Useful if you need to merge CSS context separately.

### `panel_config.has_permission(request, scope=None)`

Returns `True` if the request's user may access the panel or a specific scope. Used internally by `permission_required` but available for manual checks.

### `@panel_config.permission_required(scope=None)`

View decorator. Redirects unauthenticated users to the admin login page, raises 403 for authenticated users who fail the permission check.

### `panel_config.apply_override_settings(settings)`

Called by the `dj-control-room` hub to inject cross-panel settings. Panel authors do not call this directly.

---

## `PanelPlaceholderModel` reference

Abstract `managed=False` base model. Subclass it and set `verbose_name` / `verbose_name_plural` in `Meta` to control how the entry appears in the admin sidebar. No migration is generated.

## `BasePanelAdmin` reference

| Attribute | Type | Description |
|---|---|---|
| `redirect_url_name` | `str` | Namespaced URL to redirect the changelist to, e.g. `"my_panel:index"`. |
| `panel_config` | `PanelConfig` | When set, `has_view_permission` and `has_change_permission` delegate to `panel_config.has_permission(request)`. |

All write permissions (`has_add_permission`, `has_delete_permission`) return `False`. The changelist redirects immediately to `redirect_url_name`.
