from dataclasses import dataclass, field
from typing import Any, Callable


@dataclass
class PanelTool:
    name: str
    scope: str
    description: str
    input_schema: dict
    handler: Callable


@dataclass
class PanelToolResult:
    success: bool
    message: str
    data: dict = field(default_factory=dict)


@dataclass
class PanelToolContext:
    user: Any
    inputs: dict
    config: Any  # PanelConfig — not imported here to avoid a circular dependency
