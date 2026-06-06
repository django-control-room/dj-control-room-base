from django.shortcuts import render
from django.templatetags.static import static

from dj_control_room_base.conf import panel_config
from dj_control_room_base.templatetags.dcr_icons import ICONS

_ICON_COLORS = [
    "accent",
    "success",
    "warning",
    "danger",
    "info",
    "indigo",
    "purple",
    "muted",
]


@panel_config.permission_required("design-system")
def index(request):
    context = panel_config.get_context(
        request,
        title="DCR Design System",
        icon_keys=list(ICONS.keys()),
        icon_colors=_ICON_COLORS,
        icon_example_logo_url=static("dj_control_room_base/images/example-logo.png"),
    )
    return render(request, "admin/dj_control_room_base/index.html", context)


@panel_config.permission_required("examples")
def examples(request):
    context = panel_config.get_context(request, title="Reference Examples")
    return render(request, "admin/dj_control_room_base/examples.html", context)
