from django.contrib import admin

from dj_control_room_base.core import BasePanelAdmin
from .models import BasePanelPlaceholder


@admin.register(BasePanelPlaceholder)
class BasePanelPlaceholderAdmin(BasePanelAdmin):
    redirect_url_name = "dj_control_room_base:index"
