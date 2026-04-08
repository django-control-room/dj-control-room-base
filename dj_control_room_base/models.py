from django.db import models


class BasePanelPlaceholder(models.Model):
    """
    This is a fake model used to create an entry in the admin panel for dj_control_room_base.
    When we register this app with the admin site, it is configured to simply load
    the panel templates.
    """

    class Meta:
        managed = False
        verbose_name = "Dj Control Room Base"
        verbose_name_plural = "Dj Control Room Base"
