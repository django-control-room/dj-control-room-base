from dj_control_room_base.core import PanelPlaceholderModel


class BasePanelPlaceholder(PanelPlaceholderModel):
    """
    Placeholder model that registers the base panel in the Django admin sidebar.
    """

    class Meta(PanelPlaceholderModel.Meta):
        verbose_name = "Dj Control Room Base"
        verbose_name_plural = "Dj Control Room Base"
