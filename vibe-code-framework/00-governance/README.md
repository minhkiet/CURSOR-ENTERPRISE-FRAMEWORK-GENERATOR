# Governance — Resource Hub

This directory is the single governance location for the Resource Hub. The
manifest at `resource-manifest.json` is the only manifest for canonical
locations, ownership metadata, adapter boundaries, and script input rules.

## Execution input contract

Every install, sync, or validation run must resolve these inputs before doing
work:

| Input | Required contract |
|---|---|
| `SourcePath` | Resource Hub root. It must contain this manifest and `01-core-rules` through `08-scripts`; it must not be `08-scripts`, `.cursor`, or `.git`. |
| `TargetPath` | Consumer project directory. It may be created by install, but it must not be the Resource Hub or its `.git` directory. |
| `Tool` | One of `Cursor`, `ClaudeCode`, `Codex`, `Copilot`, `Windsurf`, `Antigravity`, `All`. |
| `Category` | One of `rules`, `skills`, `agents`, `workflows`, `all`. |
| `ManifestPath` | Optional override; defaults to `SourcePath/00-governance/resource-manifest.json` and must resolve to the canonical manifest. |

The default distribution direction is one-way:

`SOT-CANONICAL (Resource Hub) → adapter/consumer`

Scripts do not delete canonical resources or infer approval. Existing
`.cursor` content is retained as an adapter/project boundary. A migration of
an individual `.cursor` resource is `BLOCKED` until its owner, consumer,
canonical source, dependency impact, and rollback evidence are recorded.

## Canonical locations

| Resource | Canonical location | Source type |
|---|---|---|
| Core rules | `01-core-rules/` | `SOT-CANONICAL` |
| Stack guides | `02-stacks/` | `SOT-CANONICAL` |
| Skills | `03-skills/` | `SOT-CANONICAL` |
| Agents | `04-agents/` | `SOT-CANONICAL` |
| Workflows | `05-workflows/` | `SOT-CANONICAL` |
| Templates | `06-templates/` | `SOT-CANONICAL` |
| Tool adapters | `07-adapters/` | `SOT-CANONICAL` |
| Scripts | `08-scripts/` | `SOT-CANONICAL` |
| Governance and manifest | `00-governance/` | `SOT-CANONICAL` |

Record paths are also canonical and are defined only in the manifest:
`00-governance/records/cursor-inventory.json`,
`00-governance/records/conflicts.json`,
`00-governance/records/approvals.json`,
`00-governance/records/rollback.md`, and
`00-governance/records/evidence.json`. Additive GitHub skill provenance is
recorded in `00-governance/records/external-skills.json`; this is not an
approval register and never grants approval.

The current external import `frontend-design` remains `SOT-EXTERNAL` with
`EXTERNAL_OWNER_UNCONFIRMED`, `PENDING_REVIEW`, and `NOT_GRANTED`; it must be
reviewed before being treated as an approved shared resource.

The root `.cursor/` directory in the host repository is not a second
canonical source. It is a Cursor-specific/project-local boundary whose files
must be classified before migration.

## Conditions to unblock whole-ecosystem acceptance

The verdict may move from `BLOCKED` only when all applicable conditions below
have actual evidence. A missing condition is not an implicit approval.

| Condition | Required action | Required evidence | Owner |
|---|---|---|---|
| `COND-RUNTIME-001` | Install Python `>= 3.10`, install dev dependencies, run `python -m pytest -q` | Python version, install log, test output and exit code | `DEV` |
| `COND-INVENTORY-001` | Resolve all `.cursor` `UNKNOWN_RESOURCE` entries | Classification, canonical source, owner, consumer/dependency map | `DEV` |
| `COND-CONFLICT-001` | Decide duplicate/conflicting authority | Comparison and approved conflict decision | `LEAD` |
| `COND-APPROVAL-001` | Approve ownership-changing/destructive migration | Named Approval Record linked to Change IDs | `OWN` |
| `COND-ROLLBACK-001` | Test target-only backup and restore | Rollback procedure and restore verification | `REL` |
| `COND-ACCEPTANCE-001` | Re-run all affected checks after approved changes | Fresh evidence IDs, commands, exit codes, scope summaries | `QA` |

Migration remains one-way and non-destructive until `COND-INVENTORY-001`,
`COND-APPROVAL-001`, and `COND-ROLLBACK-001` are satisfied. Security, data,
public API, or deployment changes additionally require the relevant `SEC`,
Data Owner, API Owner, or Release approval.

Run `08-scripts/preflight.ps1` to evaluate these conditions from the
manifest. When the system `python` command is a Windows Store shim, pass an
explicit interpreter with `-PythonPath`. It returns exit code `0` only when every checked condition passes;
otherwise it returns `1` and reports the blocking evidence gap.

## Records and evidence

Use the IDs and status values from the master requirements when recording an
inventory, issue, change, evidence, or approval. A command may be marked
`PASS` only when its actual exit code and output are available. Missing owner,
approval, or dependency information is `BLOCKED`, not `PASS`.
