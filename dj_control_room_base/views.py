from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import render

from dj_control_room_base.conf import panel_config


@staff_member_required
def index(request):
    context = panel_config.get_context(request, title="DCR Design System")
    return render(request, "admin/dj_control_room_base/index.html", context)


@staff_member_required
def examples(request):
    context = panel_config.get_context(request, title="Examples")
    return render(request, "admin/dj_control_room_base/examples.html", context)


@staff_member_required
def ex_dashboard(request):
    context = panel_config.get_context(request, title="Installed Panels — Examples")
    context["ex_page"] = "dashboard"
    return render(request, "admin/dj_control_room_base/ex_dashboard.html", context)


@staff_member_required
def ex_workers(request):
    context = panel_config.get_context(request, title="Worker Dashboard — Examples")
    context["ex_page"] = "workers"
    return render(request, "admin/dj_control_room_base/ex_workers.html", context)


@staff_member_required
def ex_keys(request):
    context = panel_config.get_context(request, title="Key Browser — Examples")
    context["ex_page"] = "keys"
    return render(request, "admin/dj_control_room_base/ex_keys.html", context)


@staff_member_required
def ex_key_detail(request):
    context = panel_config.get_context(request, title="Key Detail — Examples")
    context["ex_page"] = "key_detail"
    return render(request, "admin/dj_control_room_base/ex_key_detail.html", context)


@staff_member_required
def ex_errors(request):
    context = panel_config.get_context(request, title="Error Groups — Examples")
    context["ex_page"] = "errors"
    return render(request, "admin/dj_control_room_base/ex_errors.html", context)
