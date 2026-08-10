# Configuration

`dj_control_room_base` works out of the box with sensible defaults. Everything is optional - you only need to add settings when you want to change the default behavior.

The settings key for this panel is **`DJ_CONTROL_ROOM_BASE_SETTINGS`**.

```python
# settings.py
DJ_CONTROL_ROOM_BASE_SETTINGS = {
    "LOAD_DEFAULT_CSS": True,
    "EXTRA_CSS": [],
    "THEME_AUTO_DETECT": True,
    "ALLOWED_GROUPS": [],
    "REQUIRE_SUPERUSER": False,
    "SCOPE_PERMISSIONS": {},
}
```

All keys shown above are the defaults. You only need to declare the keys you want to change.

---

## How settings are merged

Settings are resolved fresh on each request by merging four layers, from lowest to highest priority:

| Priority | Layer | Source |
|---|---|---|
| 1 (lowest) | Built-in defaults | `PANEL_BUILTIN_DEFAULTS` in `core/panel_config.py` |
| 2 | Panel defaults | `defaults={}` passed to `PanelConfig(...)` in `conf.py` |
| 3 | Hub overrides | Injected at runtime by `dj-control-room` when installed |
| 4 (highest) | Project settings | `DJ_CONTROL_ROOM_BASE_SETTINGS` in your Django settings file |

This layering means:

- **Panel authors** declare a minimal set of defaults for their panel. They never need to worry about the built-in keys.
- **The hub** can enforce cross-panel policies (e.g. disable the default CSS globally, restrict permissions) without touching individual panels.
- **Project owners** always win. Anything in `DJ_CONTROL_ROOM_BASE_SETTINGS` overrides everything else, so you can always opt out of hub defaults.

---

## CSS settings

### `LOAD_DEFAULT_CSS`

**Type:** `bool` | **Default:** `True`

Controls whether the shared `design-system.css` bundle shipped with this package is loaded in panel templates. When `True`, the bundle is injected automatically via the template context.

Set to `False` if:

- The Control Room hub already loads the design-system CSS globally and you want to avoid a double load.
- You are replacing the design system entirely with your own stylesheet.

```python
DJ_CONTROL_ROOM_BASE_SETTINGS = {
    "LOAD_DEFAULT_CSS": False,
}
```

### `EXTRA_CSS`

**Type:** `list[str]` | **Default:** `[]`

Additional stylesheets to inject after the default bundle (or after nothing, if `LOAD_DEFAULT_CSS` is `False`). Each entry can be either:

- A **Django static file path** (relative to `STATIC_ROOT`) - resolved through `staticfiles` at render time.
- An **absolute URL** starting with `http://`, `https://`, or `//` - used as-is.

```python
DJ_CONTROL_ROOM_BASE_SETTINGS = {
    "LOAD_DEFAULT_CSS": True,
    "EXTRA_CSS": [
        "my_panel/css/overrides.css",  # resolved via staticfiles
        "https://cdn.example.com/theme.css",  # used as-is
    ],
}
```

!!! note "How CSS reaches templates"
    `panel_config.get_context(request)` calls `get_css_context()` internally and merges the result into the template context. Templates receive two variables:

    - `dj_cr_load_default_css` - boolean, whether to render the design-system `<link>` tag
    - `dj_cr_extra_css` - pre-rendered `<link>` tag HTML for the resolved theme adapter (if any) plus each `EXTRA_CSS` entry, marked safe

    If you are writing a panel template from scratch, extend `panel_base.html` (which handles these variables) or render them yourself.

### `THEME_AUTO_DETECT`

**Type:** `bool` | **Default:** `True`

When `True`, detect the first known admin skin in `INSTALLED_APPS` and inject a stylesheet through the same pipeline as `EXTRA_CSS`:

1. A first-class [theme adapter](#theme-adapters) when the skin is `unfold`, `jazzmin`, `grappelli`, or `admin_interface`.
2. A [general light/dark pin](#general-light-and-dark-pins) (`themes/general-light.css` or `themes/general-dark.css`) when a known unsupported skin is detected first.
3. Nothing for classic Django admin (no theme app).

When `False`, do nothing automatically - load an adapter (or any other CSS) yourself via `EXTRA_CSS`.

Detection walks `INSTALLED_APPS` in order; the first recognized theme app wins. If the resolved path is already listed in `EXTRA_CSS`, it is not duplicated.

```python
DJ_MY_PANEL_SETTINGS = {
    "THEME_AUTO_DETECT": True,  # default
    # Or opt out and load manually:
    # "THEME_AUTO_DETECT": False,
    # "EXTRA_CSS": ["dj_control_room_base/css/themes/unfold.css"],
}
```

### Theme adapters

The package ships token-override stylesheets under `dj_control_room_base/css/themes/` for admin skins that don't match the classic Django admin palette. With the default `THEME_AUTO_DETECT = True`, the matching adapter is loaded automatically when the skin's app is in `INSTALLED_APPS`. To choose the adapter yourself, set `THEME_AUTO_DETECT` to `False` and add it via `EXTRA_CSS`:

```python
DJ_MY_PANEL_SETTINGS = {
    "THEME_AUTO_DETECT": False,
    "EXTRA_CSS": ["dj_control_room_base/css/themes/unfold.css"],
}
```

Currently available:

| File | For |
|---|---|
| `themes/unfold.css` | Projects using [django-unfold](https://github.com/unfoldadmin/django-unfold) as their admin skin. |
| `themes/jazzmin.css` | Projects using [django-jazzmin](https://github.com/farridav/django-jazzmin) as their admin skin. |
| `themes/grappelli.css` | Projects using [django-grappelli](https://github.com/sehmaschine/django-grappelli) as their admin skin. |
| `themes/admin-interface.css` | Projects using [django-admin-interface](https://github.com/fabiocaccamo/django-admin-interface) as their admin skin. |
| `themes/general-light.css` | Light-pin fallback for known skins without a first-class adapter (see below). |
| `themes/general-dark.css` | Dark-pin fallback for known skins without a first-class adapter (see below). |


You can also make your own theme adapters easily by following the `unfold.css` or
`jazzmin.css` examples. This works very well for any Tailwind CSS or Bootstrap
driven admin that exposes its palette as CSS custom properties.

See [Theme Adapters](themes.md) for a full visual gallery, including every Jazzmin/Bootswatch skin currently supported.

### General light and dark pins

Many third-party admin skins keep a fixed light or dark chrome and do not expose the same color-scheme signals as stock Django admin / Unfold / Jazzmin. Without a first-class adapter, `design-system.css` can follow the OS preference (or stay on light defaults) and clash with that host.

For curated lists of such skins, auto-detect loads `themes/general-light.css` or `themes/general-dark.css` instead. Those stylesheets pin `--dcr-*` tokens to the matching design-system palette (with `!important`) so panels stay readable. They do **not** remap brand/accent colors onto the host skin - for that, write a custom adapter and load it via `EXTRA_CSS`.

Recognized general-light app labels (first match in `INSTALLED_APPS`):

`simpleui`, `semantic_admin`, `django_admin_kubi`, `daisy`, `jet`, `bootstrap_admin`, `djangocms_admin_style`, `material`

Recognized general-dark app labels: none yet (the stylesheet and detection path are ready; add labels as dark-only unsupported skins are identified).

---

## Permission settings

Panels built on this library use a two-level permission model: **panel-wide** defaults and optional **per-scope** overrides for individual views.

All permission checks require the user to be **authenticated and staff** as a baseline. Anonymous users are redirected to the Django admin login page.

### `ALLOWED_GROUPS`

**Type:** `list[str]` | **Default:** `[]`

A list of Django group names that are allowed to access the panel. The check uses group name matching.

- **Empty list (default):** any staff user can access the panel.
- **Non-empty list:** the user must belong to at least one of the named groups.

```python
DJ_CONTROL_ROOM_BASE_SETTINGS = {
    "ALLOWED_GROUPS": ["ops", "support"],
}
```

!!! note "Superusers bypass group checks"
    Superusers always pass, regardless of `ALLOWED_GROUPS`. This mirrors Django's own admin behavior.

### `REQUIRE_SUPERUSER`

**Type:** `bool` | **Default:** `False`

When `True`, only superusers can access the panel. Non-superuser staff receive a 403.

```python
DJ_CONTROL_ROOM_BASE_SETTINGS = {
    "REQUIRE_SUPERUSER": True,
}
```

---

## Scoped permissions

`SCOPE_PERMISSIONS` lets you set different permission rules for individual views, overriding the panel-wide policy for just that view.

A **scope** is a string label that matches the argument passed to `@panel_config.permission_required("my-scope")` on a view function. Each scope entry accepts the same `ALLOWED_GROUPS` and `REQUIRE_SUPERUSER` keys as the panel-wide settings.

```python
DJ_CONTROL_ROOM_BASE_SETTINGS = {
    # Panel-wide defaults (apply to any view not listed in SCOPE_PERMISSIONS)
    "ALLOWED_GROUPS": [],
    "REQUIRE_SUPERUSER": False,
    "SCOPE_PERMISSIONS": {
        # Only superusers can reach the design-system view
        "design-system": {
            "REQUIRE_SUPERUSER": True,
        },
        # Only the "editors" group can reach the examples view
        "examples": {
            "ALLOWED_GROUPS": ["editors"],
        },
    },
}
```

If a scope key is present but its dict is empty (`{}`), that view inherits the panel-wide `ALLOWED_GROUPS` and `REQUIRE_SUPERUSER` values exactly.

### Permission resolution order

For every request, permissions are resolved as follows:

1. **Not authenticated** - redirect to admin login.
2. **Not staff** - 403.
3. **Superuser** - always allowed (mirrors Django admin).
4. **`REQUIRE_SUPERUSER` is True** for the resolved scope - 403 for non-superusers.
5. **`ALLOWED_GROUPS` is non-empty** for the resolved scope - 403 if the user is not in any of those groups.
6. Otherwise - allowed.

---

## Full reference

All supported keys with their types and defaults:

| Key | Type | Default | Description |
|---|---|---|---|
| `LOAD_DEFAULT_CSS` | `bool` | `True` | Load the bundled `design-system.css`. |
| `EXTRA_CSS` | `list[str]` | `[]` | Extra stylesheets to inject (static paths or URLs). |
| `THEME_AUTO_DETECT` | `bool` | `True` | Auto-detect a known admin skin and inject its adapter or a general light/dark pin. |
| `ALLOWED_GROUPS` | `list[str]` | `[]` | Group names allowed panel-wide. Empty means any staff. |
| `REQUIRE_SUPERUSER` | `bool` | `False` | Restrict panel to superusers only. |
| `SCOPE_PERMISSIONS` | `dict` | `{}` | Per-scope overrides for `ALLOWED_GROUPS` and `REQUIRE_SUPERUSER`. |
