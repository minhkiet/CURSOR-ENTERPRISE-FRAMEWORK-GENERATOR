# REA: Reverse Engineer Anything — Upstream Sync

This folder contains the complete, verified vendor drop of [morluto/rea](https://github.com/morluto/rea) (v6.4.0).
It provides a unified CLI and Model Context Protocol (MCP) server for reverse engineering across native binaries, managed .NET assemblies, JavaScript/Electron applications, Android APKs, WebAssembly, EVM bytecode, Go binaries, and runtime process observation.

The Cursor Enterprise Framework bridge skills live in:
- `.cursor/skills/sec_reverse-engineer-anything/`
- `.agents/skills/reverse-engineer-anything/`

The slash command lives in:
- `.cursor/commands/rea.md`

---

## Capabilities & Architecture

| Target Type | Supported Analysis & Tools | Engines / Providers |
|-------------|----------------------------|---------------------|
| **JavaScript / Electron** | AST parsing, module dependencies, ASAR extraction, source maps, Electron IPC boundaries | Built-in AST / Acorn / Babel |
| **Native Binaries (PE/ELF/Mach-O)** | Decompilation, disassembly, symbol extraction, xrefs, control-flow graph | Hopper, Ghidra, IDA Pro |
| **Managed .NET Assemblies** | CIL decompilation, P/Invoke boundary verification, metadata inspection | Built-in managed static provider |
| **Android Applications (APK)** | Manifest analysis, class/method search, JADX bridge, decompilation | JADX, ADB, Apktool |
| **WebAssembly (WASM)** | Section analysis, WAT disassembly, export/import analysis | WABT integration |
| **EVM Bytecode** | Contract interface recovery, selector matching, mutability analysis | evmole integration |
| **Go Binaries** | Module path, build settings, compiler version, embedded metadata | Built-in Go binary parser |
| **Network & Web** | HAR inspection, mitmproxy captures, CDP browser passive observation | CDP / mitmproxy |
| **Runtime Processes** | Memory layout, register states, crash dumps, Frida instrumentation | Frida, pwntools, pwndbg, LLDB |

---

## MCP Server Integration

To start the REA MCP server directly:
```bash
node tools/rea/scripts/rea.mjs mcp
```
Or via npx:
```bash
npx -y rea-agents mcp
```

### Config in Cursor Enterprise Framework (`mcp/mcp_config.json`):
```json
{
  "mcpServers": {
    "rea": {
      "command": "node",
      "args": ["${workspaceFolder}/tools/rea/scripts/rea.mjs", "mcp"],
      "description": "REA - Reverse Engineer Anything: native binaries, Electron/JS, APK, WASM via MCP"
    }
  }
}
```

---

## CLI Usage

Run any command directly:
```bash
node tools/rea/scripts/rea.mjs --help
node tools/rea/scripts/rea.mjs --version
node tools/rea/scripts/rea.mjs analyze-javascript-application <path-to-asar-or-folder> --json
node tools/rea/scripts/rea.mjs inspect-artifact <path-to-binary-or-archive>
```

---

## Quick Sanity Check

```powershell
# Run verification script
.\tools\rea\setup-rea.ps1
```
