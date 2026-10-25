# Resource Hub Baseline

## Scope

Baseline for the repository at `D:\PROJECTS\CURSORS\CURSOR ENTERPRISE FRAMEWORK GENERATOR`.
The inspected scopes are the four paths declared in the master requirements:

| Scope | Observed path | Initial classification |
|---|---|---|
| `SCOPE-RESOURCE-HUB` | `vibe-code-framework/` | Shared canonical source |
| `SCOPE-CORE` | `cursor_framework/` | Core project |
| `SCOPE-WEB` | `cursor_framework_web/` | Web project |
| `SCOPE-SETUP` | `cursor-setup-gui-wpf/` | Setup project |
| Cursor boundary | `.cursor/` | Adapter/project-local boundary; migration per resource is pending |

## Applied change

- `CHG-RESTRUCTURE`: add the governance boundary under
  `vibe-code-framework/00-governance/`.
- `CHG-FEATURE`: add a single Resource Hub manifest with an explicit execution
  input contract and canonical locations.
- `CHG-REFACTOR`: make script defaults resolve the Resource Hub root instead of
  the `08-scripts` directory.
- `CHG-REFACTOR`: update the root `CursorSetup.sln` project reference to the
  existing `cursor-setup-gui-wpf/CursorSetupWpf.csproj` project.
- No root `.cursor` resource was deleted, renamed, or overwritten.

## Baseline observations

- Git worktree was already dirty before this change. Existing user changes
  remain outside this change set.
- The pre-change validator was invoked as
  `vibe-code-framework/08-scripts/validate.ps1` and resolved its default path
  to `08-scripts`, producing 46 missing-file errors and exit code `1`.
- The pre-change `.cursor` inventory contained project and adapter material,
  including generated/cache areas. It was not safe to bulk-migrate it without
  per-resource ownership and dependency evidence.
- The pre-change hub did not contain a canonical manifest or explicit script
  input contract.

## Verification records

| Evidence ID | Criterion | Procedure | Result |
|---|---|---|---|
| `EVD-BASELINE-001` | `CONFIG-001` | Inspect repository paths, manifests, and Git status | `PASS` for discovery; worktree is intentionally dirty |
| `EVD-BASELINE-002` | `HUB-001` | Inspect `vibe-code-framework/` structure | `FAIL` before change: governance manifest absent |
| `EVD-BASELINE-003` | `REF-001` | Run `vibe-code-framework/08-scripts/validate.ps1` with defaults | `FAIL` before change: default path bug, exit code `1` |
| `EVD-BASELINE-004` | `SOT-008` | Review `.cursor` categories and current consumers | `BLOCKED`: per-resource mapping and approval are not yet complete |

The baseline records the state before implementation; it is not a claim that
the entire ecosystem was accepted.

## Post-change evidence

| Evidence ID | Criterion | Command/procedure | Result |
|---|---|---|---|
| `EVD-VERIFY-001` | `HUB-001`, `REF-001` | `vibe-code-framework/08-scripts/validate.ps1` | `PASS`, exit code `0`, framework valid |
| `EVD-VERIFY-002` | `SOT-005`, `SOT-009` | `vibe-code-framework/08-scripts/inventory.ps1` | `PASS`, 1,211 `.cursor` files classified; 910 remain `UNKNOWN_RESOURCE` |
| `EVD-VERIFY-003` | `ADAPTER-001`, `SOT-006` | Sync Cursor rules to an isolated temporary target | `PASS`, 5 `.mdc` rules created; existing targets are protected by default |
| `EVD-VERIFY-004` | `BUILD-001` | `npm run build` in `cursor_framework_web/` | `PASS`, Vite production build exit code `0` |
| `EVD-VERIFY-005` | `BUILD-001` | `dotnet build CursorSetup.sln --no-restore -v:minimal` | `PASS`, 0 warnings and 0 errors after solution reference correction |
| `EVD-VERIFY-006` | `TEST-001` | Bundled Python 3.12.14 venv: `python -m pytest -q` | `PASS`, 136 passed and 5 subtests passed; the system `python` command remains a Windows Store shim |
| `EVD-VERIFY-007` | `APPROVAL-001`, `SOT-008`, `SAFE-001` | `preflight.ps1 -PythonPath <approved interpreter>` | `BLOCKED`, runtime passes; 910 unknown resources, conflict approval, real approval, and rollback verification remain outstanding |
| `EVD-VERIFY-008` | `FEATURE-IMPORT-GITHUB` | `pytest -q tests/test_skill_installer.py` and CLI help | `PASS`, append-only GitHub importer tested with file/provenance handling, overwrite protection, and validation |
| `EVD-VERIFY-009` | `HUB-001`, `REF-001` | `vibe-code-framework/08-scripts/validate.ps1` after governance record additions | `PASS`, exit code `0` |
| `EVD-IMPORT-DRYRUN-001` | `FEATURE-IMPORT-GITHUB` | GitHub importer dry-run against `anthropics/skills` / `skills/frontend-design` / `main` | `PASS`, exit code `0`, SHA-256 recorded; no local write |
| `EVD-IMPORT-001` | `FEATURE-IMPORT-GITHUB` | GitHub importer real import against `anthropics/skills` / `skills/frontend-design` / `main` | `PASS`, exit code `0`, canonical skill and provenance record created |
| `EVD-RUNTIME-LOCAL-001` | `COND-RUNTIME-001` | Project-local `.venv` creation, editable dev install, and preflight auto-discovery | `PASS`, Python 3.12.14 and pytest detected without `-PythonPath` |
| `EVD-INVENTORY-001` | `COND-INVENTORY-001` | Inventory written to `00-governance/records/cursor-inventory.json` | `BLOCKED`, 1,211 resources recorded; 910 remain `UNKNOWN_RESOURCE` with required review fields unresolved |
| `EVD-ADAPTER-SMOKE-002` | `ADAPTER-001` | Cursor skills sync to an isolated temporary target | `PASS`, 10 skills synced including `frontend-design`; host `.cursor` untouched |
| `EVD-ROLLBACK-TARGET-001` | `COND-ROLLBACK-001` | Snapshot, intentional drift detection, target-only restore, and SHA-256 verification | `PASS`, whole `.cursor` target rejected; isolated target restored and verified |
| `EVD-ADAPTER-SMOKE-003` | `ADAPTER-001` | Cursor skills sync to an isolated temporary target after external import | `PASS`, 10 skills synced including `frontend-design`; exit code `0` |
| `EVD-BUILD-WEB-001` | `BUILD-001` | `npm run build` in `cursor_framework_web/` | `PASS`, Vue typecheck and Vite production build completed |
| `EVD-BUILD-WPF-001` | `BUILD-001` | Build both WPF solutions with `dotnet build --no-restore` | `PASS`, both builds completed with 0 warnings and 0 errors |
| `EVD-OPERATIONAL-PREFLIGHT-001` | `RUN-001` | `preflight.ps1 -OperationalOnly` | `PASS`, safe operational path is ready; `migrationAllowed=false`, whole-ecosystem verdict remains `BLOCKED` |
| `EVD-ADAPTER-SMOKE-004` | `ADAPTER-001` | Explicit `TargetPath` sync/install smoke and omitted-target safety checks | `PASS`, explicit targets work; omitted target is rejected with exit code `1` |
| `EVD-OPERATIONAL-PREFLIGHT-002` | `RUN-001` | Operational preflight after explicit-target safety changes | `PASS`, operational path remains ready; migration remains blocked and unauthorized |

## Current verdict

`BLOCKED` for whole-ecosystem acceptance. The Resource Hub validator, adapter
smoke test, web build, WPF build, and Python test runtime pass. Whole-ecosystem
acceptance remains blocked by per-resource ownership, dependency, conflict,
and approval evidence for the unresolved `.cursor` inventory. Target-only
rollback and all current validator, test, adapter, web-build, and WPF-build
checks are verified. The system `python` command remains a Windows Store shim,
but project-local `.venv` now supplies the verified runtime.

The safe operational path is available through `preflight.ps1 -OperationalOnly`.
It is intentionally narrower than migration acceptance: it supports validated
canonical Resource Hub operations while refusing to authorize `.cursor`
migration.

No approval record is fabricated; architecture/migration approval remains
`PENDING` for destructive or ownership-changing migration.

The GitHub skill importer is additive only. It targets
`vibe-code-framework/03-skills`, refuses to overwrite an existing skill, and
records external provenance with `SOT-EXTERNAL`, `PENDING_REVIEW`, and
`NOT_GRANTED` approval status. The verified `frontend-design` import is
present in the canonical hub, but remains pending owner review and does not
change the whole-ecosystem `BLOCKED` verdict.

## Required next conditions

The exact machine-readable conditions are defined in
`00-governance/resource-manifest.json`. Execution can proceed to a final
acceptance decision only after:

1. `COND-RUNTIME-001`: satisfied by the project-local `.venv` evidence; keep
   using that interpreter until the system Python shim is replaced.
2. `COND-INVENTORY-001`: all 910 current `UNKNOWN_RESOURCE` entries have a
   classification, canonical source, owner, consumers, dependencies, and
   rollback mapping.
3. `COND-CONFLICT-001`: duplicate/conflicting resources have one approved
   authority and a recorded resolution.
4. `COND-APPROVAL-001`: OWN/LEAD and any required security, data, API, or
   release approvers have recorded decisions before destructive migration.
5. `COND-ROLLBACK-001`: satisfied by target-only backup/restore evidence; this
   does not authorize whole-repository restore.
6. `COND-ACCEPTANCE-001`: satisfied for the current validator, adapter smoke,
   Python tests, web build, and WPF build evidence. Re-run after any approved
   change.
