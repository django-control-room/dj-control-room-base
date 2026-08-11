# Theme Adapters

Panels built on `dj_control_room_base` render with the classic Django admin palette by default. For projects using a themed admin skin, this package ships **theme adapters** - small stylesheets that remap DCR's `--dcr-*` design tokens onto the host skin's own CSS variables, so panels blend in instead of clashing with the rest of the admin.

Adapters live under `dj_control_room_base/css/themes/`. With the default `THEME_AUTO_DETECT = True`, `PanelConfig` detects the active admin skin from `INSTALLED_APPS` and injects either a first-class adapter or a [general light/dark pin](configuration.md#general-light-and-dark-pins) through the same pipeline as `EXTRA_CSS`. Turn it off to opt out and load an adapter manually:

```python
DJ_MY_PANEL_SETTINGS = {
    "THEME_AUTO_DETECT": True,  # default
    # Or opt out:
    # "THEME_AUTO_DETECT": False,
    # "EXTRA_CSS": ["dj_control_room_base/css/themes/unfold.css"],
}
```

See [Configuration - Theme adapters](configuration.md#theme-adapters) for the full settings reference, general pin fallbacks, and dark-mode wiring. This page is a visual tour of what's currently supported.

---

## Compatibility status

| Admin skin | `INSTALLED_APPS` label | Status | Stylesheet |
|---|---|---|---|
| Classic Django admin | — | Built-in (no adapter needed) | — |
| [django-unfold](https://github.com/unfoldadmin/django-unfold) | `unfold` | First-class adapter | `themes/unfold.css` |
| [django-jazzmin](https://github.com/farridav/django-jazzmin) | `jazzmin` | First-class adapter | `themes/jazzmin.css` |
| [django-grappelli](https://github.com/sehmaschine/django-grappelli) | `grappelli` | First-class adapter | `themes/grappelli.css` |
| [django-admin-interface](https://github.com/fabiocaccamo/django-admin-interface) | `admin_interface` | First-class adapter | `themes/admin-interface.css` |
| [django-admin-dracula](https://github.com/dracula/django-admin) | `django_admin_dracula` | First-class adapter | `themes/dracula.css` |
| [django-simpleui](https://github.com/newpanjing/simpleui) | `simpleui` | General light pin | `themes/general-light.css` |
| [django-semantic-admin](https://github.com/globophobe/django-semantic-admin) | `semantic_admin` | General light pin | `themes/general-light.css` |
| [django-admin-kubi](https://github.com/dengunorg/django-admin-kubi) | `django_admin_kubi` | General light pin | `themes/general-light.css` |
| [django-daisy](https://github.com/hypy13/django-daisy) | `django_daisy` | General light pin | `themes/general-light.css` |
| [django-jet-reboot](https://github.com/assem-ch/django-jet-reboot) | `jet` | General light pin | `themes/general-light.css` |
| [djangocms-admin-style](https://github.com/django-cms/djangocms-admin-style) | `djangocms_admin_style` | General light pin | `themes/general-light.css` |
| [bootstrap-admin](https://github.com/douglasmiranda/django-admin-bootstrap) | `bootstrap_admin` | General light pin | `themes/general-light.css` |


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

## django-admin-dracula

[`django-admin-dracula`](https://github.com/dracula/django-admin) overrides Django admin CSS with the Dracula palette and supports light / dark / auto via Django's `data-theme` toggle. `themes/dracula.css` remaps DCR tokens onto Dracula's `--body-*`, `--default-button-bg`, and `--dracula-*` variables so panels track both modes (purple accent, cyan/pink/green semantic colors).

```python
DJ_MY_PANEL_SETTINGS = {
    "EXTRA_CSS": ["dj_control_room_base/css/themes/dracula.css"],
}
```

![Django Control Room running with the django-admin-dracula theme](https://raw.githubusercontent.com/django-control-room/dj-control-room-base/main/images/dcr-base-dracula.png)

---

## General light and dark pins (unsupported skins)

Skins without a first-class adapter get a pinned palette when auto-detect finds them first in `INSTALLED_APPS`:

- `themes/general-light.css` for light-chrome skins (for example [django-simpleui](https://github.com/newpanjing/simpleui) or [django-semantic-admin](https://github.com/globophobe/django-semantic-admin))
- `themes/general-dark.css` for dark-chrome skins

These pins keep panel surfaces aligned with the host chrome; they do not attempt brand remapping.

```python
DJ_MY_PANEL_SETTINGS = {
    "EXTRA_CSS": ["dj_control_room_base/css/themes/general-light.css"],
    # Or:
    # "EXTRA_CSS": ["dj_control_room_base/css/themes/general-dark.css"],
}
```

See [Configuration - General light and dark pins](configuration.md#general-light-and-dark-pins) for the recognized app labels.

---

## Build your own

Want to support another admin skin? Use `unfold.css`, `jazzmin.css`, `grappelli.css`, `admin-interface.css`, or `dracula.css` as a starting point and remap the `--dcr-*` tokens to match. Until then, a general light or dark pin keeps panels readable under that skin.
