# Configuration

DJ control room base currently works out of the box with minimal configuration.

## Basic Setup

The only required configuration is adding the app to your `INSTALLED_APPS` and including the URLs in your URL configuration.

See the [Installation](installation.md) guide for setup instructions.

## URLs Configuration

```python
# urls.py
urlpatterns = [
    path('admin/dj-control-room-base/', include('dj_control_room_base.urls')),  # Custom path
    path('admin/', admin.site.urls),
]
```

## Security

DJ control room base uses Django's built-in admin authentication:

- Only staff users (`is_staff=True`) can access the panel
- All views require authentication via `@staff_member_required`
- No additional security configuration needed

## CSS Customization

You can customize panel styling with `DJ_CONTROL_ROOM_BASE_SETTINGS`:

### `LOAD_DEFAULT_CSS`

**Type:** `bool`  
**Default:** `True`  
**Description:** Whether to load the built-in panel stylesheet. Set to `False` to use your own styles.

### `EXTRA_CSS`

**Type:** `list[str]`  
**Default:** `[]`  
**Description:** Additional stylesheets to load after the default CSS. Accepts static file paths or full URLs.

```python
DJ_CONTROL_ROOM_BASE_SETTINGS = {
    'LOAD_DEFAULT_CSS': True,
    'EXTRA_CSS': [
        'dj_control_room_base/css/overrides.css',
        'https://cdn.example.com/theme.css',
    ],
}
```

## Advanced Configuration

Other advanced configuration options may be added in future releases.
