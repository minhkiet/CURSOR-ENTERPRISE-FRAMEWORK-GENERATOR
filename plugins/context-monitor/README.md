# Vibe Framework Context Monitor Plugin

Inspects active conversation context, token consumption, memory stores, and cache hit metrics.

## Features
- **Session Memory Stats**: Real-time stats on visited files, pinned entities, and token footprints.
- **Inspect Context Prompt**: Previews the exact markdown context injected into agent LLM calls.
- **Token Budget Analysis**: Evaluates headroom against configured token limits with optimization tips.
- **Redis Observability**: Live query metrics, hit ratio, slowlogs, and distributed caching telemetry.
- **Session Memory Reset**: One-click wipe of temporary conversational memory.

## Settings
- `vibeFramework.contextMonitor.maxTokens`: Maximum token ceiling before warning (default: `4000`).
