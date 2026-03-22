# Security Policy

## Scope

Guitar TUI is a local terminal application. It makes no network connections, stores no credentials, and has no server component. All data (lessons, chord/scale definitions, user settings) stays on your machine.

The attack surface is essentially limited to the content files bundled with the package (`guitar_tui/content/` and `guitar_tui/data/`). These are static Markdown and YAML files parsed at startup.

## Reporting a concern

If you believe you have found a security issue — for example, a way that malformed content files could cause unexpected behaviour — please open a GitHub issue describing the concern. There is no need for private disclosure given the local-only nature of this application.
