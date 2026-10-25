---
name: "source-command-vbs-scan-security-command"
description: "vbsec Security Scanner - Quét lỗ hổng bảo mật 21 rule cross-language với L1-L4 data flow analysis, optional --sca (OSV.dev CVE) và --auto-fix"
---

# source-command-vbs-scan-security-command

Use this skill when the user asks to run the migrated source command `vbs-scan-security-command`.

## Command Template

# Command: /vbs-scan-security

## Mục tiêu

Security scan tự động với [vbsec](https://github.com/tanviet12/vbsec) — phát hiện 21 lỗ hổng bảo mật phổ biến nhất trong code (đặc biệt là code do AI sinh ra). Reasoning-based, không pattern-match thuần — giảm false positive so với grep-only scanners.

## Invocation

```
/vbs-scan-security                              # Toàn repo (default)
/vbs-scan-security all                          # Alias explicit
/vbs-scan-security uncommitted                  # Uncommitted changes
/vbs-scan-security staged                       # Staged files only
/vbs-scan-security commit within 7days          # 7 ngày gần
/vbs-scan-security commit id <sha>              # 1 commit cụ thể
/vbs-scan-security pr id <number>               # Pull request
/vbs-scan-security lang=en                      # Output tiếng Anh (mặc định: vi)
/vbs-scan-security --sca                       # + Live CVE lookup qua OSV.dev
/vbs-scan-security --auto-fix                  # + Tự sinh patch + verify build
/vbs-scan-security --run-tests                 # + Chạy test khi bump dependency
```

**Flags có thể kết hợp:** `/vbs-scan-security all --sca --auto-fix`

## 21 Rule được scan

| # | Rule | Severity |
|---|---|---|
| 1 | HARDCODED-SECRET | CRITICAL |
| 2 | SQL-INJECTION | CRITICAL |
| 3 | XSS | HIGH |
| 4 | IDOR | HIGH |
| 5 | SLOPSQUATTING | CRITICAL |
| 6 | BRUTE-FORCE | HIGH |
| 7 | MASS-ASSIGNMENT | CRITICAL |
| 8 | INSECURE-DESERIALIZATION | CRITICAL |
| 9 | SSRF | HIGH |
| 10 | PATH-TRAVERSAL | HIGH |
| 11 | CSRF | HIGH |
| 12 | BROKEN-ACCESS-CONTROL | CRITICAL |
| 13 | WEAK-PASSWORD-HASHING | CRITICAL |
| 14 | JWT-NONE-ALGORITHM | CRITICAL |
| 15 | CORS-MISCONFIG | HIGH |
| 16 | UNRESTRICTED-FILE-UPLOAD | CRITICAL |
| 17 | VERBOSE-ERROR-DEBUG-MODE | HIGH |
| 18 | MISSING-RATE-LIMIT | HIGH |
| 19 | RACE-CONDITION | HIGH |
| 20 | OUTDATED-DEPENDENCY | HIGH |
| 21 | COMMAND-INJECTION | CRITICAL |
| 22 | VULNERABLE-DEPENDENCY | CRITICAL (chỉ với `--sca`) |

## L1-L4 Data Flow Analysis

Scanner phân loại nguồn dữ liệu trước khi flag:
- **L1** (KHÔNG TIN): `req.body`, `$_GET`, `request.params`, `process.argv`
- **L2** (Bán tin): DB query result
- **L3** (Tin): Hardcoded strings, config keys
- **L4** (Tin): Env vars, file paths nội bộ

**Ví dụ:** `f"SELECT ... {x}"` chỉ CRITICAL nếu `x` là L1 không parameterize. SAFE nếu `x` là L3 (hardcoded).

## 5 Language Overlays

Ngoài 21 rule generic, có overlay chuyên sâu cho:
- **Go**: GORM SQLi, exec.Command, slog secrets, Colly SSRF
- **PHP**: mysqli/PDO, $_GET, eval/include, Laravel CSRF, unserialize
- **TypeScript/JavaScript**: Sequelize/Prisma/TypeORM/Mongoose, React/Vue XSS, Express/NestJS, child_process, JWT
- **Python**: SQLAlchemy/Django ORM, pickle/yaml, subprocess, PyJWT, flask-cors
- **.NET**: EF Core raw SQL, Newtonsoft TypeNameHandling, Process.Start, Developer Exception Page

## Quy trình (5 bước)

1. **Parse args**: scope, lang, flags
2. **Gather files**: git diff / git ls-files / find (nếu không có git)
3. **Detect language**: count file extension, chọn primary (≥30%)
4. **Route**: SMALL (inline) hoặc LARGE (delegate sub-agent)
5. **Apply rules**: Grep → Read → Trace L1-L4 → Verdict
6. **Generate report**: markdown + JSON canonical, save `vbsec-reports/scan-<timestamp>.md`

## Verdict

| Findings | Verdict |
|---|---|
| ≥1 CRITICAL | **FAIL** |
| 0 CRITICAL, ≥1 HIGH | **WARN** |
| 0 CRITICAL, 0 HIGH | **PASS** |

## Output Format

Report gồm:
- Header (scope, file count, primary lang, mode, date, lang)
- Verdict line + 1-line description
- **CRITICAL section** (verbose: tại sao nguy hiểm, attack scenario, code before/after)
- **HIGH section** (medium: tác động, code fix)
- **MEDIUM/LOW** (compact table)
- PASSED CHECKS
- Auto-fix summary (nếu `--auto-fix`)
- JSON summary (canonical EN, parse-able bằng CI/CD)

## Output Example

```markdown
# Báo cáo quét bảo mật vbsec

**Phạm vi:** Toàn bộ repo
**Số file:** 12 (8 .ts, 4 .py)
**Ngôn ngữ chính:** typescript (dùng rule chuyên sâu)
**Chế độ:** NHỎ (quét trực tiếp)
**Ngày quét:** 2026-10-03
**Ngôn ngữ báo cáo:** vi

## KẾT LUẬN: KHÔNG ĐẠT
...

## NGHIÊM TRỌNG (chặn deploy)
| File:Dòng | Loại lỗi | Mô tả | Cách sửa |
|---|---|---|---|
| `api/users.ts:42` | SQL-INJECTION | L1 input nối thẳng | Dùng parameterized query |
| `.env:1` | HARDCODED-SECRET | Stripe key đã commit | Xoay key + .gitignore |

## CAO (cần khắc phục)
| File:Dòng | Loại lỗi | Mô tả | Cách sửa |
|---|---|---|---|
| `auth.ts:18` | WEAK-PASSWORD-HASHING | MD5 cho password | Dùng bcrypt/argon2 |

## ĐÃ ĐẠT
- ✓ XSS — Vue auto-escape, không có v-html với user data
- ✓ CORS — Origin cụ thể, không dùng `*`
- ✓ CSRF — Token CSRF có trong form
- ...

🤖 Báo cáo tạo bởi [vbsec](https://github.com/tanviet12/vbsec)
> Báo cáo này tham khảo — không thay thế cho audit bảo mật chuyên nghiệp.

\`\`\`json
{
  "verdict": "FAIL",
  "summary": {"critical": 2, "high": 1, "medium": 0, "low": 0, "passed": 14},
  "scope": "all",
  "files_reviewed": 12,
  "primary_language": "typescript",
  "specialized_rules_used": true,
  "mode": "small",
  "date": "2026-10-03",
  "findings": [...]
}
\`\`\`
```

## Tích hợp với CI/CD

JSON summary canonical ở cuối report parse được bằng tooling:
```python
import json, re
with open("vbsec-reports/scan-2026-10-03-xxxx.md") as f:
    text = f.read()
data = json.loads(re.findall(r"```json\s*\n(.*?)\n```", text, re.S)[-1])
if data["verdict"] == "FAIL":
    sys.exit(1)  # Block merge
```

## So với các skills security khác

| Skill | Phạm vi | Cách dùng |
|---|---|---|
| **vbs-scan-security** (lệnh này) | Tự động scan 21 rule, có data flow analysis | Chạy thường xuyên, trước commit, trong PR |
| `sec_security-review` | Manual review với 5 layers checklist | Manual review sâu hơn, sau khi có report từ vbsec |
| `vietnam-payment-review` | VN payment gateway chuyên sâu | Review code payment cụ thể |
| `frontend-review` | Frontend-specific | Review UI/UX, không phải security chính |

**Kết hợp:** Chạy vbsec trước → review report → manual review bằng `sec_security-review` cho phần nhạy cảm.

## Files location

- Skill: `.cursor/skills/vbs-scan-security/`
- Rule: `.cursor/rules/security_vbsec.mdc`
- Command: `.cursor/commands/vbs-scan-security/command.md`
- Reports: `vbsec-reports/scan-<timestamp>.md` (nên add `.gitignore`)

## Best Practice

1. **Chạy trước mỗi PR**: `/vbs-scan-security uncommitted` hoặc `commit within 7days`
2. **Dùng `--sca` cho production repos**: cần network, scan thêm 30s
3. **Dùng `--auto-fix` cho CI auto-remediation**: chỉ apply patch đã verify build pass
4. **Review report thay vì trust verdict**: WARN ≠ approve, HIGH issues cần fix
5. **Save report cho audit trail**: report Markdown dễ share, JSON dễ parse

## Hạn chế

- Không thay thế audit chuyên nghiệp
- Không đảm bảo bắt 100% vulnerabilities
- Nên kết hợp với `npm audit`, `pip-audit`, `govulncheck` cho CVE database chính thức
- AI output có thể khác nhau giữa các lần chạy

## Liên kết

- [[../../skills/vbs-scan-security]] - Skill chính
- [[../../rules/security_vbsec]] - Rule rule
- [[../../rules/meta_security]] - Security framework meta
- [[../../skills/sec_security-review]] - Manual security review
- [[../../commands/security/command]] - Manual /security command
- [vbsec GitHub](https://github.com/tanviet12/vbsec) - Public repo
