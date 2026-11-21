# Vibe Framework Status Line Plugin

Real-time telemetry and health monitoring in the Cursor IDE status bar.

## Features
- **Live Health Indicator**: Shows cache status (Warm, Cold, Stale).
- **Metric Summary**: Number of indexed skills, active rules, and token memory load.
- **Quick Menu**: Instant access to Warm Cache, Rebuild Index, Vibe Sync, Spec Kit, and Dashboard.
- **Auto-Refresh**: Configurable background polling and auto-update on file save.

## Settings
- `vibeFramework.statusLine.enabled`: Toggle status bar visibility (default: `true`).
- `vibeFramework.statusLine.refreshInterval`: Auto-refresh interval in ms (default: `30000`).
- `vibeFramework.statusLine.showTokens`: Display memory token usage.
- `vibeFramework.statusLine.showSkills`: Display skills count.
