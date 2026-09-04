# Security Review & Reverse-Skill Integration

> This document explains how the `security-review` skill integrates with the bundled [reverse-skill](https://github.com/zhaoxuya520/reverse-skill) package for advanced reverse-engineering and penetration-testing workflows.

---

## Overview

The `security-review` skill provides layered security analysis. The **advanced RE layer** (Security-9) routes into reverse-skill's specialized sub-skills for APK, binary, JS, firmware, and pentest workflows.

```
Security Review (security-review/SKILL.md)
    ├── Layer 1-8: Static + OWASP + LLM Security  (always in-scope)
    └── Layer 9:   Advanced RE                      (reverse-skill routing)
                       ├── apk-reverse/     → APK decompilation, Frida, SSL pinning
                       ├── ida-reverse/     → IDA Pro binary analysis
                       ├── radare2/         → CLI binary analysis, patching
                       ├── js-reverse/      → Frontend JS, encrypted params, CSP
                       ├── pentest-tools/   → Nmap, Nuclei, SQLMap, FFUF
                       ├── edr-bypass-re/   → EDR hook reversal, syscall direct
                       ├── firmware-pentest/→ IoT firmware extraction + emulation
                       ├── pwn-chain/       → Exploit writing, stack/heap pwn
                       ├── browser-automation/ → Playwright + desktop automation
                       └── llm-security/    → OWASP LLM Top 10, ASI Top 10
```

---

## Tool Availability (Current Machine)

Run `refresh-tool-index.ps1` after installing new tools to update this table.

| Tool | Available | Notes |
|------|:---------:|-------|
| jadx | no | Download from github.com/skylot/jadx |
| apktool | no | Download from apktool.org |
| Java (JDK) | yes | v17.0.12 — required for jadx/apktool |
| frida | yes | Python pip package installed |
| radare2 | yes | System installation |
| Python | yes | v3.13.5 — for Frida, helper scripts |
| Node.js | yes | v22.14.0 — for jshookmcp, anything-analyzer |
| npx | yes | Bundled with Node.js |
| IDA Pro | no | Commercial; needed for ida-reverse |
| apksigner / zipalign | no | Android SDK Build-Tools |
| adb | no | Android SDK platform-tools |
| anything-analyzer | no | pnpm project — clone from github.com/Mouseww/anything-analyzer |
| nmap | no | Install via winget or nmap.org |
| jshookmcp | runtime-only | Requires MCP client registration |

### Quick Tool Installation

```powershell
# Frida (already installed — verify)
pip install frida-tools
frida-ps -U

# radare2 (already installed — verify)
r2 -v

# jadx — download release zip, extract to C:\Users\<USER>\Tools\jadx\
# apktool — download from apktool.org, place apktool.bat + apktool.jar in same dir
# Java — already v17 installed

# Refresh tool index after installing
powershell -ExecutionPolicy Bypass -File ".cursor/skills/reverse-skill/skills/scripts/refresh-tool-index.ps1"
```

---

## Reverse-Skill Module Quick Reference

### APK Security Analysis

**Activate when:** Analyzing APK for hardcoded secrets, SSL pinning, root detection, or API key extraction.

```
Entry: Read skills/apk-reverse/SKILL.md
Tools: jadx (decompile), apktool (unpack), frida (hooking), adb (device)
```

```powershell
# Decode APK
powershell -File ".cursor/skills/reverse-skill/apk-reverse/scripts/decode.ps1" -ApkPath ".\app.apk"

# Frida hooking (example: bypass SSL pinning)
powershell -File ".cursor/skills/reverse-skill/apk-reverse/scripts/frida-run.ps1" -PackageName "com.example.app" -Script "frida_scripts/ssl-bypass.js"

# Rebuild + resign
powershell -File ".cursor/skills/reverse-skill/apk-reverse/scripts/rebuild-sign-install.ps1" -DecodedDir ".\app_decoded"

# Manifest summary
powershell -File ".cursor/skills/reverse-skill/apk-reverse/scripts/manifest-summary.ps1" -DecodedDir ".\app_decoded"
```

### Binary Analysis (radare2 / IDA Pro)

**Activate when:** Analyzing .exe, .dll, .so, ELF, Mach-O, or firmware binaries.

```
radare2 (free): Read skills/radare2/SKILL.md
IDA Pro (commercial): Read skills/ida-reverse/SKILL.md
```

```powershell
# Start IDA MCP service (requires IDA Pro + idalib-mcp)
powershell -File ".cursor/skills/reverse-skill/ida-reverse/scripts/start.ps1"

# Open sample in IDA (requires IDA Pro)
powershell -File ".cursor/skills/reverse-skill/ida-reverse/scripts/open.ps1" -Path "C:\path\to\sample.exe"

# radare2 CLI analysis (no IDA required)
r2 -A ./target.bin
[0x00000000]> afl          # list functions
[0x00000000]> iz           # strings
[0x00000000]> pdf @ sym.main  # decompile function
```

### Frontend JS Reverse Engineering

**Activate when:** Analyzing JavaScript bundles for encrypted parameters, request signatures, or webpack patterns.

```
Entry: Read skills/js-reverse/SKILL.md
Tools: node, npx, jshookmcp (MCP)
```

```json
// MCP registration for jshookmcp (add to Cursor MCP settings)
{
  "mcpServers": {
    "jshook": {
      "command": "npx",
      "args": ["-y", "@jshookmcp/jshook@latest"],
      "env": { "JSHOOK_BASE_PROFILE": "search" }
    }
  }
}
```

### Network Penetration Testing

**Activate when:** Port scanning, vulnerability scanning, web fuzzing, credential attacks.

```
Entry: Read skills/pentest-tools/SKILL.md
Tools: nmap, nuclei, sqlmap, ffuf, hashcat
```

```bash
# Port scan
nmap -sV -sC -oA scan_results 192.168.1.0/24

# Vulnerability scan
nuclei -u https://target.com -t vulnerabilities/

# SQL injection scan
sqlmap -u "https://target.com/?id=1" --batch --random-agent

# Web fuzzing
ffuf -w wordlist.txt -u https://target.com/FUZZ
```

### LLM / AI Security

**Activate when:** Prompt injection, prompt leakage, jailbreak attempts, agentic action risks, or LLM API security.

```
Entry: Read skills/llm-security/SKILL.md
Reference: OWASP LLM Top 10, ASI Top 10
```

Key concerns to check:
- Prompt injection in user input fields
- System prompt leakage
- Tool/function call abuse
- Resource exhaustion (token budget, infinite loops)
- Agentic action without human approval

---

## MCP Integration

### Recommended MCP Servers for Security Workflow

```json
{
  "mcpServers": {
    "jshook": {
      "command": "npx",
      "args": ["-y", "@jshookmcp/jshook@latest"],
      "env": { "JSHOOK_BASE_PROFILE": "search" }
    },
    "idapro": {
      "url": "http://127.0.0.1:13337/mcp"
    }
  }
}
```

### anything-analyzer (Browser Automation + HTTP Capture)

```bash
git clone https://github.com/Mouseww/anything-analyzer.git C:\work\anything-analyzer
cd C:\work\anything-analyzer
pnpm install
pnpm dev
# Service runs at http://localhost:23816/mcp
```

### Burp Suite MCP Bridge

```json
{
  "mcpServers": {
    "burpsuite": {
      "command": "node",
      "args": [".cursor/skills/reverse-skill/burp-mcp-full/mcp-bridge.js"]
    }
  }
}
```

---

## Workflow Integration

### How Security Review Calls Reverse-Skill

When a task triggers both `security-review` and RE workflows:

1. **Security-1 through Security-8** run from `security-review/SKILL.md` (static analysis)
2. **Security-9** routes to the appropriate reverse-skill module based on target type:
   - `.apk` / Android app → `reverse-skill/skills/apk-reverse/SKILL.md`
   - `.exe` / `.dll` / `.so` / ELF → `reverse-skill/skills/ida-reverse/SKILL.md` or `radare2/SKILL.md`
   - JavaScript / frontend bundle → `reverse-skill/skills/js-reverse/SKILL.md`
   - Firmware / IoT → `reverse-skill/skills/firmware-pentest/SKILL.md`
   - Network / web → `reverse-skill/skills/pentest-tools/SKILL.md`
   - Exploit development → `reverse-skill/skills/pwn-chain/SKILL.md`
   - LLM/AI → `reverse-skill/skills/llm-security/SKILL.md`

3. **Security findings** are captured in the security-review report format
4. **Field journal** writeback: After each RE engagement, write experience to `reverse-skill/skills/field-journal/` for self-evolution

---

## Self-Evolution: Field Journal

The reverse-skill package includes an auto-evolving knowledge base at `reverse-skill/skills/field-journal/`. After each RE engagement:

- Document the full execution chain (what worked, what didn't)
- Record pitfalls and their solutions
- Note tool version compatibility issues
- Update routing if new patterns were discovered

Template: `reverse-skill/skills/field-journal/_template.md`

---

## Quick Command Reference

```powershell
# Tool index refresh
powershell -ExecutionPolicy Bypass -File ".cursor/skills/reverse-skill/skills/scripts/refresh-tool-index.ps1"

# APK decode
powershell -File ".cursor/skills/reverse-skill/apk-reverse/scripts/decode.ps1" -ApkPath ".\app.apk"

# Frida hooking
powershell -File ".cursor/skills/reverse-skill/apk-reverse/scripts/frida-run.ps1" -PackageName "com.example.app" -Script "frida_scripts/ssl-bypass.js"

# IDA Pro MCP start
powershell -File ".cursor/skills/reverse-skill/ida-reverse/scripts/start.ps1"

# IDA Pro open sample
powershell -File ".cursor/skills/reverse-skill/ida-reverse/scripts/open.ps1" -Path "C:\path\to\sample.exe"

# radare2 analysis
r2 -A ./target.bin

# Dependency audit (for Security-6)
npm audit
pip-audit
```

---

## Key Files in Reverse-Skill

|| File | Purpose |
||------|---------|
| `SKILL.md` | Main routing controller |
| `routing.md` | Scenario → sub-skill dispatch matrix |
| `tool-index.md` | Local tool availability registry |
| `field-journal/` | Auto-evolving experience logs |
| `skills/apk-reverse/` | APK RE sub-skill |
| `skills/ida-reverse/` | IDA Pro binary analysis |
| `skills/radare2/` | radare2 CLI RE |
| `skills/js-reverse/` | Frontend JS reverse |
| `skills/pentest-tools/` | Penetration testing tools |
| `skills/edr-bypass-re/` | EDR bypass RE |
| `skills/firmware-pentest/` | Firmware security testing |
| `skills/pwn-chain/` | Exploit development |
| `skills/browser-automation/` | Playwright + desktop automation |
| `skills/llm-security/` | LLM/AI security |
| `skills/docs-generator/` | Auto-generate security reports |
| `skills/diagram-generator/` | Attack path diagrams |
| `skills/binary-diff/` | Cross-version symbol migration |
| `skills/patch-diff-exploit/` | N-day patch diff → exploit |
| `skills/reverse-engineering/` | Cross-platform RE methodology |
