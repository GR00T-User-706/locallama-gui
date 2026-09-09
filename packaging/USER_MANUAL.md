# MyLoAI Control Center User Manual

## What MyLoAI does

MyLoAI Control Center is a desktop interface for working with local and remote large-language-model services. It provides model management, chat, provider configuration, sessions, prompts, agents, plugins, and diagnostics through one desktop application.

## First launch

1. Install MyLoAI Control Center using the installer for your operating system.
2. Start **MyLoAI Control Center** from the application menu or desktop shortcut.
3. Configure the LLM service you want to use in the provider/API settings.
4. Select an available model and start a session.

MyLoAI does not itself provide model weights. A local provider such as Ollama must have the desired model available, or a compatible remote API must be configured.

## Local Ollama use

If Ollama is running on the same computer, use the default local Ollama endpoint unless your installation uses a different address or port. The application can query the provider for available models and use the selected model for chat and related features.

## Remote providers

For an OpenAI-compatible service, enter the service endpoint and credentials required by that provider. Keep API keys private and do not place credentials in screenshots, issue reports, or public configuration files.

## Data and configuration

MyLoAI stores application state using platform-appropriate per-user application directories. Existing `locallama-gui` configuration paths are retained for compatibility with the current application data model.

## Diagnostics

Use the diagnostics and connection tools when a provider cannot be reached. Verify the service is running, the endpoint is correct, and local firewall/network rules permit the connection.

## Updating

Install a newer MyLoAI release over the existing installation when the platform installer supports in-place upgrades. User configuration and session data are stored separately from the application installation and should normally remain intact.

## Uninstalling

Use the operating system's normal application removal mechanism. Uninstalling the application removes installed application files; it does not imply deletion of your per-user application data.

## Support information

When reporting a problem, include the MyLoAI version, operating system, provider type, and a concise description of the failing operation. Do not include passwords, API keys, tokens, or other private credentials.
