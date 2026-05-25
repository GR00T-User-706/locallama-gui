"""
LLM Studio Plugin SDK — Base Plugin Interface.

Every plugin must subclass BasePlugin and define the class-level attributes.
The plugin manager discovers plugins by scanning for subclasses of BasePlugin
in any module inside the plugins/ directory.

Example minimal plugin:

    from app.plugin_sdk.base_plugin import BasePlugin, ToolDefinition

    class MyPlugin(BasePlugin):
        PLUGIN_ID   = "my_plugin"
        PLUGIN_NAME = "My Plugin"
        PLUGIN_DESC = "Does something useful"
        PLUGIN_VERSION = "1.0.0"
        PLUGIN_AUTHOR  = "Your Name"

        def get_tools(self):
            return [
                ToolDefinition(
                    name="my_tool",
                    description="Does X with input Y",
                    parameters={"input": {"type": "string"}},
                    handler=self.my_tool_handler,
                )
            ]

        def my_tool_handler(self, input: str) -> str:
            return f"Result: {input.upper()}"
"""

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Any, Callable, Dict, List, Optional


@dataclass
class ToolDefinition:
    """Describes a callable tool that can be used by agents."""
    name: str
    description: str
    parameters: Dict[str, Any]          # JSON Schema-style parameter spec
    handler: Callable                   # fn(**kwargs) -> str | dict
    required: List[str] = field(default_factory=list)
    returns: str = "string"             # string | json | markdown


@dataclass
class CommandDefinition:
    """A slash command available in the chat input."""
    name: str                           # e.g. "summarize"
    description: str
    handler: Callable                   # fn(args: str, session) -> str
    usage: str = ""


@dataclass
class PanelDefinition:
    """A custom panel to inject into the main window."""
    panel_id: str
    title: str
    widget_factory: Callable            # fn() -> QWidget
    dock_area: str = "right"           # left | right | bottom | top | float


class BasePlugin(ABC):
    """
    Base class for all LLM Studio plugins.

    Class attributes (must be defined on subclass):
        PLUGIN_ID      — unique snake_case identifier
        PLUGIN_NAME    — human-readable display name
        PLUGIN_DESC    — short description
        PLUGIN_VERSION — semver string e.g. "1.0.0"
        PLUGIN_AUTHOR  — author name
    """

    PLUGIN_ID: str = ""
    PLUGIN_NAME: str = ""
    PLUGIN_DESC: str = ""
    PLUGIN_VERSION: str = "1.0.0"
    PLUGIN_AUTHOR: str = ""

    def __init__(self):
        self._enabled = True
        self._config: Dict[str, Any] = {}
        self._app_context: Optional[Any] = None   # set by plugin manager

    # ── Lifecycle ─────────────────────────────────────────────────────────

    def on_load(self):
        """Called when the plugin is loaded. Perform initialization here."""

    def on_unload(self):
        """Called when the plugin is disabled or the app shuts down."""

    def on_settings_changed(self, settings: Dict[str, Any]):
        """Called when global app settings change."""

    # ── Extension points ──────────────────────────────────────────────────

    def get_tools(self) -> List[ToolDefinition]:
        """Return tool definitions this plugin exposes to agents."""
        return []

    def get_commands(self) -> List[CommandDefinition]:
        """Return slash commands this plugin adds to the chat."""
        return []

    def get_panels(self) -> List[PanelDefinition]:
        """Return custom UI panels to add to the main window."""
        return []

    def on_chat_message(self, message: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """
        Intercept outgoing chat messages.
        Return modified message dict or None to pass through unchanged.
        """
        return None

    def on_chat_response(self, response: str) -> Optional[str]:
        """
        Intercept incoming assistant responses.
        Return modified string or None to pass through unchanged.
        """
        return None

    def get_memory_provider(self):
        """Return a memory provider object (optional). Must implement store/retrieve."""
        return None

    # ── Config ────────────────────────────────────────────────────────────

    def configure(self, config: Dict[str, Any]):
        self._config = config

    def get_config_schema(self) -> Dict[str, Any]:
        """Return JSON Schema for plugin-specific configuration."""
        return {}

    def set_app_context(self, context: Any):
        """Called by plugin manager to inject app-level context."""
        self._app_context = context

    # ── Utility ───────────────────────────────────────────────────────────

    @property
    def enabled(self) -> bool:
        return self._enabled

    def __repr__(self):
        return f"<Plugin {self.PLUGIN_ID} v{self.PLUGIN_VERSION}>"
