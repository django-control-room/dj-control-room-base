# Theme Adapters

Panels built on `dj_control_room_base` render with the classic Django admin palette by default. For projects using a themed admin skin, this package ships **theme adapters** - small, opt-in stylesheets that remap DCR's `--dcr-*` design tokens onto the host skin's own CSS variables, so panels blend in instead of clashing with the rest of the admin.

Adapters live under `dj_control_room_base/css/themes/` and are never loaded automatically. Add the one you need to `EXTRA_CSS` on each panel where you want it applied:

```python
DJ_MY_PANEL_SETTINGS = {
    "EXTRA_CSS": ["dj_control_room_base/css/themes/unfold.css"],
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

[`django-jazzmin`](https://github.com/farridav/django-jazzmin) is built on Bootstrap 5 and ships as a set of [Bootswatch](https://bootswatch.com/) skins, selected via `JAZZMIN_UI_TWEAKS["theme"]`. `themes/jazzmin.css` maps the same DCR tokens onto Bootstrap's `--bs-*` variables (`--bs-primary`, `--bs-body-*`, `--bs-border-color`, `--bs-secondary-color`, ...), with per-theme accent and dark-mode fallbacks sourced from each Bootswatch palette - so panels track whichever theme is active without any extra configuration.

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

Dark themes are detected via the `body.theme-<name>` class Jazzmin applies (not `data-bs-theme`, which Jazzmin doesn't document or set) - see [`ui_customisation`](https://django-jazzmin.readthedocs.io/ui_customisation/) for the full list Jazzmin ships.

---

## Build your own

Both adapters follow the same recipe: remap `--dcr-*` tokens to the host skin's variables, fall back to DCR's own defaults when a variable is missing, and leave semantic status colors (success/warning/danger/info) untouched since most skins don't expose those as configurable brand colors. This works well for any Tailwind CSS or Bootstrap admin skin that exposes its palette as CSS custom properties - use `unfold.css` or `jazzmin.css` as a starting point.
