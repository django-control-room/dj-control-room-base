# Theme Adapters

Panels built on `dj_control_room_base` render with the classic Django admin palette by default. For projects using a themed admin skin, this package ships **theme adapters** - small stylesheets that remap DCR's `--dcr-*` design tokens onto the host skin's own CSS variables, so panels blend in instead of clashing with the rest of the admin.

Adapters live under `dj_control_room_base/css/themes/`. With the default `THEME_AUTO_DETECT = True`, `PanelConfig` detects the active admin skin from `INSTALLED_APPS` and injects the matching adapter through the same pipeline as `EXTRA_CSS`. Turn it off to opt out and load an adapter manually:

```python
DJ_MY_PANEL_SETTINGS = {
    "THEME_AUTO_DETECT": True,  # default
    # Or opt out:
    # "THEME_AUTO_DETECT": False,
    # "EXTRA_CSS": ["dj_control_room_base/css/themes/unfold.css"],
}
```

See [Configuration - Theme adapters](configuration.md#theme-adapters) for the full settings reference, fallback behavior, and dark-mode wiring. This page is a visual tour of what's currently supported.

---

## django-unfold

[`django-unfold`](https://github.com/unfoldadmin/django-unfold) themes are driven by `--color-primary-*`, `--color-base-*`, and `--color-font-*` CSS variables. `themes/unfold.css` remaps DCR's accent, surface, border, and muted-text tokens onto those variables, so panels automatically pick up whatever brand color the project has configured for Unfold - light or dark mode included.

```python
DJ_MY_PANEL_SETTINGS = {
    "EXTRA_CSS": ["dj_control_room_base/css/themes/unfold.css"],
}
```

![Django Control Room running with the django-unfold admin theme](https://raw.githubusercontent.com/django-control-room/dj-control-room-base/main/images/dcr-base-unfold.png)

---

## django-jazzmin

[`django-jazzmin`](https://github.com/farridav/django-jazzmin) is built on Bootstrap 5 and ships as a set of [Bootswatch](https://bootswatch.com/) skins, selected via `JAZZMIN_UI_TWEAKS["theme"]`. `themes/jazzmin.css` maps DCR's tokens onto Bootstrap's own CSS variables, so panels track whichever theme is active, including Jazzmin's dark skins, without any extra configuration.

```python
DJ_MY_PANEL_SETTINGS = {
    "EXTRA_CSS": ["dj_control_room_base/css/themes/jazzmin.css"],
}
```

![Django Control Room running with the django-jazzmin admin theme](https://raw.githubusercontent.com/django-control-room/dj-control-room-base/main/images/dcr-base-jazzmin.png)

All of Jazzmin's built-in Bootswatch themes are covered, each with its own accent color and (for the dark ones) matching surface/border/text fallbacks:

| Light themes | Dark themes |
|---|---|
| `cerulean`, `cosmo`, `flatly`, `journal`, `litera`, `lumen`, `lux`, `materia`, `minty`, `pulse`, `sandstone`, `simplex`, `sketchy`, `spacelab`, `united`, `yeti` | `cyborg`, `darkly`, `slate`, `solar`, `superhero` |

See [`ui_customisation`](https://django-jazzmin.readthedocs.io/ui_customisation/) for the full list of themes Jazzmin ships.

---

## django-grappelli

[`django-grappelli`](https://github.com/sehmaschine/django-grappelli) support via `themes/grappelli.css`, matching its teal accent and boxy, light-only look.

```python
DJ_MY_PANEL_SETTINGS = {
    "EXTRA_CSS": ["dj_control_room_base/css/themes/grappelli.css"],
}
```

![Django Control Room running with the django-grappelli admin theme](https://raw.githubusercontent.com/django-control-room/dj-control-room-base/main/images/dcr-base-grappelli.png)

---

## django-admin-interface

[`django-admin-interface`](https://github.com/fabiocaccamo/django-admin-interface)

```python
DJ_MY_PANEL_SETTINGS = {
    "EXTRA_CSS": ["dj_control_room_base/css/themes/admin-interface.css"],
}
```

![Django Control Room running with the django-admin-interface admin theme](https://raw.githubusercontent.com/django-control-room/dj-control-room-base/main/images/dcr-base-admin-interface.png)

---

## Build your own

Want to support another admin skin? Use `unfold.css`, `jazzmin.css`, `grappelli.css`, or `admin-interface.css` as a starting point and remap the `--dcr-*` tokens to match.
