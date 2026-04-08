from django.contrib import admin
from django.http import HttpRequest

from dj_control_room_base.core.conf import build_css_context


def get_panel_context(
    request: HttpRequest,
    settings_key: str,
    defaults: dict | None = None,
    **extra,
) -> dict:
    """
    Build a base template context for a panel view.

    Combines the Django admin context, CSS injection context, and any
    extra key/value pairs into a single dict ready to pass to render().

    :param request: The current HTTP request.
    :param settings_key: The Django settings attribute name for the panel.
    :param defaults: Panel-defined settings defaults.
    :param extra: Additional context values (e.g. title="My Panel").
    """
    context = admin.site.each_context(request)
    context.update(build_css_context(settings_key, defaults=defaults))
    context.update(extra)
    return context
