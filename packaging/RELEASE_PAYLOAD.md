# Release Payload Contract

A release artifact for MyLoAI Control Center may contain only:

- the production `locallama_gui` application package;
- runtime Python dependencies when the distribution bundles them;
- application resources required at runtime;
- the platform launcher and desktop/application metadata;
- required license and third-party redistribution notices;
- concise end-user documentation such as README/help/manual pages;
- installer metadata and uninstaller data required by the target platform.

The following are explicitly excluded from installed/downloaded release payloads:

- `archive/**`;
- `.github/**`;
- `tests/**`;
- development agents, prompts, and contributor-only instructions;
- internal repository analysis and planning documents;
- CI configuration;
- historical or experimental applications;
- development-only scripts and build environment files;
- unrelated documentation not required by end users.

## Verification requirement

Every release build must inspect its staged payload before packaging and fail when an excluded path is present. The source repository may retain excluded material; exclusion is a packaging boundary, not a repository deletion policy.
