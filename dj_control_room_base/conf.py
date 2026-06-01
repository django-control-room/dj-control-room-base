from dj_control_room_base.core import PanelConfig
from dj_control_room_base.core.panel_tool import PanelTool
from dj_control_room_base.tools import (
    handle_get_design_system_url,
    handle_get_resolved_settings,
)

panel_config = PanelConfig(
    settings_key="DJ_CONTROL_ROOM_BASE_SETTINGS",
    defaults={
        "LOAD_DEFAULT_CSS": True,
        "EXTRA_CSS": [],
    },
    tools=[
        PanelTool(
            name="get_resolved_settings",
            scope="design-system",
            description=(
                "Returns the current resolved settings for this panel, "
                "including built-in defaults and any project overrides."
            ),
            input_schema={
                "type": "object",
                "properties": {},
                "additionalProperties": False,
            },
            handler=handle_get_resolved_settings,
        ),
        PanelTool(
            name="get_design_system_url",
            scope="design-system",
            description="Returns the URL to the shared design system CSS file.",
            input_schema={
                "type": "object",
                "properties": {},
                "additionalProperties": False,
            },
            handler=handle_get_design_system_url,
        ),
    ],
)
