---
description: REA (Reverse Engineer Anything) — Reverse engineer native binaries, .NET assemblies, Electron/JS apps, Android APKs, WASM, EVM bytecode, and network/runtime behavior with REA MCP and CLI
trigger: rea, reverse, reverse-engineer, decompile, disasm, disassemble, binary analysis, ghidra, hopper, ida, asar, electron inspection, apk analysis, jadx, wasm analysis, evm bytecode, reverse engineering
category: Security
framework: Cursor Enterprise Framework V4
version: 1.0.0
---

# Command: /rea

## Mục tiêu

Thực hiện phân tích kỹ thuật đảo ngược (Reverse Engineering) đối với các file nhị phân (PE/ELF/Mach-O), ứng dụng Electron/ASAR, file .NET managed, gói Android APK, WebAssembly, hợp đồng thông minh EVM, Go binary và quan sát tiến trình runtime (pwntools, Frida, LLDB, CDP) với đầy đủ bằng chứng (evidence preservation) thông qua công cụ REA.

## Trigger Keywords

- `rea`, `reverse`, `reverse-engineer`, `reverse engineering`
- `decompile`, `disasm`, `disassemble`, `binary analysis`
- `ghidra`, `hopper`, `ida`, `jadx`, `apk analysis`
- `asar`, `electron inspection`, `wasm analysis`, `evm bytecode`
- Phân tích mã nguồn đóng, dịch ngược file exe/dll/so/dylib, bóc tách gói asar/apk

## Khi nào dùng

Dùng khi cần:
- Phân tích một binary, package, hoặc app đã biên dịch (không có sẵn source code gốc)
- Trích xuất cấu trúc module, routes, IPC boundaries của Electron/JS apps
- Dịch ngược bytecode .NET, Dalvik/APK, hoặc WASM/EVM
- Phân tích luồng thực thi, xrefs, symbols, memory layout, hoặc crash dump
- Tái tạo lại tính năng (feature reconstruction) từ ứng dụng đối thủ hoặc phần mềm mẫu

KHÔNG dùng khi:
- Codebase đã có sẵn đầy đủ source code trong workspace → dùng code analysis thông thường (`/review`, `/scan`)
- Quét lỗ hổng web bảo mật (pentest) → dùng `/pentest`
- Rà soát lỗ hổng bảo mật source code → dùng `/vbs-scan` hoặc `/security`

---

## Quy trình Thực hiện (Theo thứ tự)

### 1. Phân loại mục tiêu (Route the Target)

Chọn công cụ thích hợp dựa trên định dạng của file mục tiêu:

| Định dạng mục tiêu | Lệnh REA CLI / MCP Tool tương ứng | Ghi chú |
|-------------------|-----------------------------------|---------|
| **Electron / JS ASAR** | `analyze-javascript-application <path>` | Phân tích modules, imports, IPC handlers |
| **Android APK** | `inspect-android-package <path>` | Khám phá manifest, decompilation qua JADX |
| **Managed .NET (PE/DLL)** | `inspect-managed-artifact <path>` | Metadata, types, CIL decompilation |
| **Native Binary (PE/ELF/Mach-O)** | `open-binary <path>` sau đó `binary-overview` / `search` / `xrefs` | Kết nối Ghidra, Hopper, hoặc IDA |
| **WebAssembly (.wasm)** | `inspect-wasm-artifact <path>` | Phân tích section, WAT qua WABT |
| **EVM Bytecode** | `inspect-evm-interface <path>` | Khôi phục ABI/selectors qua evmole |
| **Go Executable** | `inspect-go-binary <path>` | Trích xuất module path, build flags, versions |
| **Linux ELF Layout / Core** | `inspect-binary-layout <path>` / `inspect-recorded-crash <core>` | Phân tích static layout hoặc crash dump |
| **Network Traces** | `inspect-web-network-capture <har/mitm>` | Bóc tách HTTP requests & responses |

### 2. Khởi chạy qua CLI hoặc MCP Server

- **Chạy trực tiếp qua CLI:**
  ```bash
  node tools/rea/scripts/rea.mjs <command> [options]
  ```
  *Ví dụ:*
  ```bash
  node tools/rea/scripts/rea.mjs analyze-javascript-application "path/to/extracted-app" --json
  node tools/rea/scripts/rea.mjs inspect-artifact "path/to/target.exe"
  ```

- **Sử dụng qua MCP:**
  Agent kích hoạt server `rea` đã được tích hợp trong framework (`mcp/mcp_config.json`):
  ```bash
  node tools/rea/scripts/rea.mjs mcp
  ```

### 3. Phân tích & Bảo toàn Bằng chứng (Evidence Preservation)

- Ghi lại các phát hiện kỹ thuật (function addresses, string literals, exported APIs, IPC channels).
- Lưu giữ bằng chứng (evidence) và giới hạn phân tích để làm cơ sở cho bước tái tạo mã nguồn.

### 4. Báo cáo & Đề xuất Giải pháp

- Tổng hợp cấu trúc hoạt động của module/tính năng vừa phân tích.
- Trình bày sơ đồ luồng dữ liệu (Data Flow / Control Flow).
- Đưa ra mẫu code tái hiện (Cleanroom Re-implementation) phù hợp với chuẩn kiến trúc của dự án.
