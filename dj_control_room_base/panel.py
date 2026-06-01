"""
DJ Control Room panel configuration.

This module defines the panel that will be discovered and registered
by DJ Control Room via entry points.
"""


class DJcontrolroombasePanel:
    """
    Panel configuration for DJ control room base.
    
    This class is discovered by DJ Control Room via the entry point
    defined in pyproject.toml under [project.entry-points."dj_control_room.panels"]
    """
    
    # Display name shown in the DJ Control Room dashboard
    name = "DJ control room base"

    # Brief description shown on the panel card
    description = "Core framework for Django Control Room panels"

    # Icon to display (options: database, layers, link, chart, radio, cog, etc.)
    icon = "database"

    # Django app label as it appears in INSTALLED_APPS and the URL namespace
    # in urls.py. Defaults to the normalized dist name if not set.
    app_name = "dj_control_room_base"

    # Optional links shown on the install/configure page.
    docs_url = "https://github.com/yassi/dj-control-room-base"
    pypi_url = "https://pypi.org/project/dj-control-room-base/"

    def get_config(self):
        from .conf import panel_config
        return panel_config

    def get_url_name(self):
        """
        Return the URL name for the panel's main view.

        This should match the name of your main URL pattern in urls.py.
        Typically this is "index".

        Returns:
            str: The URL name (e.g., "index")
        """
        return "index"
