# LocalLama GUI Plugin SDK

Drop a `.py` file into the user plugin directory shown in **Help → Diagnostics** or into the repository `plugins/` directory during development. A plugin exposes a `Plugin` class with a `manifest`, `activate(context)`, and `deactivate()`.

```python
class Plugin:
    manifest = {"id": "my_plugin", "name": "My Plugin", "version": "1.0.0"}

    def activate(self, context):
        context.register_tool("tool_name", lambda text: text)
        context.register_command("command_name", lambda: None)
        context.register_chat_interceptor(lambda messages: messages)
        context.add_panel("Panel title", some_qwidget)

    def deactivate(self):
        print("my_plugin deactivated")
```

## Capabilities

- **Tools**: callable utilities agents and workflows can invoke.
- **Commands**: UI or automation commands.
- **Chat interceptors**: receive and return the outbound `ChatMessage` list before a request is sent.
- **UI extensions**: add custom PySide6 panels with `context.add_panel`.
- **Memory providers**: register custom memory backends on `context.memory_providers`.
- **Backend integrations**: provide command/tool wrappers around additional services.

Plugins run in-process and should avoid blocking the GUI thread. Use worker threads or async clients for slow operations.
