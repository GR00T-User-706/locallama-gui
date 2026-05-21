# LocalLama GUI Plugin SDK

By default, LocalLama only discovers plugins from the **user plugin directory** shown in **Help → Diagnostics**. Repository `plugins/` is only scanned when `developer_mode` is enabled in config.

A plugin exposes a `Plugin` class with a `manifest`, `activate(context)`, and `deactivate()`.

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

## Manifest validation

Plugin manifests must contain all required keys:

- `id`
- `name`
- `version`

Plugins with missing keys are treated as invalid and cannot be enabled.

## Trust boundary

Plugins are loaded as Python code in the same process as the app. Before a plugin can be enabled, its manifest `id` must be explicitly added to `trusted_plugins` in the app config.

Being discoverable is **not** the same as being trusted.

## Threat model notes

- A trusted plugin can execute arbitrary Python in-process.
- A malicious plugin may read or modify local files accessible to the user.
- A plugin can intercept chat traffic through chat interceptors.
- A plugin can register commands/tools that trigger external process or network actions.

Only trust plugin IDs from vetted sources, and review plugin source code before adding to `trusted_plugins`.

## Capabilities

- **Tools**: callable utilities agents and workflows can invoke.
- **Commands**: UI or automation commands.
- **Chat interceptors**: receive and return the outbound `ChatMessage` list before a request is sent.
- **UI extensions**: add custom PySide6 panels with `context.add_panel`.
- **Memory providers**: register custom memory backends on `context.memory_providers`.
- **Backend integrations**: provide command/tool wrappers around additional services.

Plugins run in-process and should avoid blocking the GUI thread. Use worker threads or async clients for slow operations.
