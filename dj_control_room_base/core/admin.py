from django.contrib import admin
from django.http import HttpResponseRedirect
from django.urls import reverse


class BasePanelAdmin(admin.ModelAdmin):
    """
    Base admin class for Control Room panel placeholder models.

    Redirects the changelist to the panel's main view and restricts all write
    permissions so the admin sidebar entry is read-only for staff.

    Required class attribute:
        redirect_url_name (str): Namespaced URL name to redirect to,
            e.g. ``"my_panel:index"``.

    Example::

        from dj_control_room_base.core import BasePanelAdmin
        from .models import MyPanelPlaceholder

        @admin.register(MyPanelPlaceholder)
        class MyPanelAdmin(BasePanelAdmin):
            redirect_url_name = "my_panel:index"
    """

    redirect_url_name: str = None

    def changelist_view(self, request, extra_context=None):
        return HttpResponseRedirect(reverse(self.redirect_url_name))

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return request.user.is_staff

    def has_delete_permission(self, request, obj=None):
        return False

    def has_view_permission(self, request, obj=None):
        return request.user.is_staff
