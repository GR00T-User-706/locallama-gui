# MyLoAI Control Center User Manual

## What MyLoAI does

MyLoAI Control Center is a desktop interface for working with local and remote large-language-model services. It provides model management, chat, provider configuration, sessions, prompts, agents, plugins, and diagnostics through one desktop application.

## First launch

On the first launch, MyLoAI runs a short setup wizard. It reports basic CPU/RAM information, checks the local Ollama endpoint, recommends a starter model appropriate to the detected system memory, and can pull that model when Ollama is already available.

If Ollama is not installed or running, the wizard leaves the application configured and provides a direct path to the official Ollama download page. You can return later and use **Models → Browse & Pull Models...**.

## Model discovery

Use **Models → Browse & Pull Models...** to see curated starter models without having to know model names in advance. The browser includes small general-purpose models, a classic 7B model, reasoning and coding options, and a link to the official Ollama model library for broader discovery.

MyLoAI does not itself provide model weights. A local provider such as Ollama must have the desired model available, or a compatible remote API must be configured.

## Local Ollama use

If Ollama is running on the same computer, use the default local Ollama endpoint unless your installation uses a different address or port. The application can query the provider for available models and use the selected model for chat and related features.

## Remote providers

For an OpenAI-compatible service, enter the service endpoint and credentials required by that provider. Keep API keys private and do not place credentials in screenshots, issue reports, or public configuration files.

## Data and configuration

MyLoAI stores application state using platform-appropriate per-user application directories. Existing `locallama-gui` configuration paths are retained for compatibility with the current application data model.

## Diagnostics

Use the diagnostics and connection tools when a provider cannot be reached. Verify the service is running, the endpoint is correct, and local firewall/network rules permit the connection. Developer diagnostics expose separate logs, console, operations, request, and token surfaces rather than multiple aliases for the same panel.

## Updating

Install a newer MyLoAI release over the existing installation when the platform installer supports in-place upgrades. User configuration and session data are stored separately from the application installation and should normally remain intact.

## Uninstalling

Use the operating system's normal application removal mechanism. Uninstalling the application removes installed application files; it does not imply deletion of your per-user application data.

## Support information

When reporting a problem, include the MyLoAI version, operating system, provider type, and a concise description of the failing operation. Do not include passwords, API keys, tokens, or other private credentials.
