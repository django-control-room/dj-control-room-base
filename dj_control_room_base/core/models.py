from django.db import models


class PanelPlaceholderModel(models.Model):
    """
    Abstract base model for Control Room panel placeholder models.

    Creates a ``managed=False`` model that registers a sidebar entry in the
    Django admin without creating a database table. Subclass this and set
    ``verbose_name`` / ``verbose_name_plural`` in ``Meta`` to control how the
    entry appears in the admin sidebar.

    Example::

        from dj_control_room_base.core import PanelPlaceholderModel

        class MyPanelPlaceholder(PanelPlaceholderModel):
            class Meta(PanelPlaceholderModel.Meta):
                verbose_name = "My Panel"
                verbose_name_plural = "My Panel"
    """

    class Meta:
        abstract = True
        managed = False
