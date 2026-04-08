from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import render

from dj_control_room_base.conf import DEFAULTS, SETTINGS_KEY
from dj_control_room_base.core.context import get_panel_context


@staff_member_required
def index(request):
    context = get_panel_context(
        request, SETTINGS_KEY, defaults=DEFAULTS, title="Dj Control Room Base"
    )
    return render(request, "admin/dj_control_room_base/index.html", context)
