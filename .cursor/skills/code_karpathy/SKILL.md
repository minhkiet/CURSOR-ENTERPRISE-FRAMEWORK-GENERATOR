---
description: Universal coding discipline overlay for all vibe coding agents (Cursor IDE, Codex, Claude Code, Grok). Think first, minimal code, surgical changes.
version: 3.0.0
tags: [karpathy, coding-discipline, think-first, minimal, goal-driven, surgical, verification, cross-agent, universal]
source: andrej-karpathy-skills (186k stars)
compatible_agents: [cursor, codex, claude-code, grok, universal]
---

# Vibe Coding Discipline

> **Universal Overlay Skill** - Runs with every coding agent. Never skip.
> 
> Supports: Cursor IDE, Codex (cursor.com), Claude Code (@cursor/codex), Grok (x.com/grok)

## Quick Card

```
┌─────────────────────────────────────────────────────────────────────────────┐
│  UNIVERSAL GATES (U.1-U.7)           AGENT-SPECIFIC GATES (optional)      │
├─────────────────────────────────────────────────────────────────────────────┤
│  PRE-CODE:                        C.X = Claude Code                       │
│  U.1 Think: assumptions?          CX.X = Codex                            │
│  U.2 Simple: over-engineer?       G.X = Grok                              │
│  U.3 Scope: surgical?             K.X = Cursor (karpathy legacy)          │
│  U.4 Goals: verifiable?                                          │
│  POST-CODE:                                                      │
│  U.5 Verify: traceable?           §X Verify for real                   │
│  U.6 Simple: 200→50?                                            │
│  U.7 Done: goals met?                                          │
└─────────────────────────────────────────────────────────────────────────────┘
```

## Agent Detection

The skill auto-detects which agent is running:

| Agent | Environment Variables | Gate Prefix |
|-------|----------------------|-------------|
| Cursor IDE | `CURSOR_IDE`, `CURSOR_PROJECT` | K.X (legacy) |
| Codex | `CODEX_ENABLED`, `ORIGIN_HOST` | CX.X |
| Claude Code | `CLAUDE_IDE`, `CLAUDE_API_KEY` | C.X |
| Grok | `GROK_API_KEY` | G.X |
| Unknown | fallback | U.X |

## Workflow

```
Request → U.1-U.4 → IMPLEMENT → U.5-U.7 → §X → DELIVER
              ↑                            ↓
         [ASK if unclear]        [VERIFIED? NO → loop]
```

---

## Universal Pre-Code Gates (U.1-U.4)

### U.1 Think Before Code

**Always ask:**
- What am I assuming? (state explicitly)
- Is there a simpler approach? (push back if warranted)
- Unclear → **STOP, ask now**

**If multiple interpretations:**
```
Option A: [description]
Option B: [description]
Recommendation: [reason]
```

### U.2 Simplicity Check

| Check | Action |
|-------|--------|
| 200 lines possible 50? | Rewrite |
| Speculative features? | Remove |
| Single-use abstraction? | Inline |
| "Flexibility" not requested? | Skip |

### U.3 Surgical Scope

```
MUST change:    [list only essential]
NOT touch:      [list boundaries]
Every line traces to request? [yes/no]
Style matched?  [yes/no]
```

### U.4 Goal Definition

```
Task → "Done when..." → [verifiable criteria]
```

**Examples:**
- "Fix bug" → "Test passes, edge cases covered"
- "Add feature" → "Demo works, no regressions"
- "Refactor" → "Tests pass before & after"

---

## Universal Post-Code Gates (U.5-U.7)

### U.5 Implementation Verification

- [ ] Every line traces to request
- [ ] No adjacent code "improved"
- [ ] No unrelated refactoring
- [ ] My orphans → removed

### U.6 Simplicity Re-Check

- [ ] 200 lines written → can be 50? Rewrite now.
- [ ] Speculative abstractions? Remove.
- [ ] Single-use code? Inline.

### U.7 Goal Achievement

- [ ] Success criteria verified (line-by-line)
- [ ] Tests pass (actually ran, not assumed)
- [ ] No regressions

---

## Agent-Specific Gates

### Claude Code Extensions (C.1-C.4)

#### C.1 Claude Context Check
- [ ] Max tokens within budget
- [ ] Context window efficiently used
- [ ] No redundant context included

#### C.2 Claude Tool Usage
- [ ] Using correct tool for the job
- [ ] Tool output properly handled
- [ ] Error handling for tool failures

#### C.3 Claude Multi-Step Planning
- [ ] Plan documented before implementation
- [ ] Each step verifiable
- [ ] Plan adapts to blockers

#### C.4 Claude Response Quality
- [ ] Clear, actionable responses
- [ ] Code is complete (no placeholders)
- [ ] Explanations match code

### Codex Extensions (CX.1-CX.4)

#### CX.1 Codex Project Context
- [ ] Project structure understood
- [ ] Framework conventions followed
- [ ] Consistent with existing patterns

#### CX.2 Codex File Operations
- [ ] Read before write
- [ ] No destructive operations without backup
- [ ] File changes atomic

#### CX.3 Codex Integration Points
- [ ] MCP tools used correctly
- [ ] External integrations documented
- [ ] API calls handled gracefully

#### CX.4 Codex Output Format
- [ ] Complete file generation
- [ ] No truncation (verify file sizes)
- [ ] Imports resolved

### Grok Extensions (G.1-G.4)

#### G.1 Grok Style Consistency
- [ ] Matches project coding style
- [ ] Naming conventions consistent
- [ ] Documentation format aligned

#### G.2 Grok Performance Awareness
- [ ] No obvious performance issues
- [ ] Async operations handled properly
- [ ] Resource usage reasonable

#### G.3 Grok Error Handling
- [ ] Errors caught and handled
- [ ] User-friendly error messages
- [ ] Logging appropriate

#### G.4 Grok Testing Verification
- [ ] Code has basic test coverage
- [ ] Tests actually run
- [ ] Edge cases considered

### Cursor Legacy Gates (K.1-K.7)

Original karpathy gates remain functional:

| Gate | Description |
|------|-------------|
| K.1 | Think before code |
| K.2 | Simplicity check |
| K.3 | Surgical scope |
| K.4 | Goal definition |
| K.5 | Implementation verification |
| K.6 | Simplicity re-check |
| K.7 | Goal achievement |

---

## §X - Verify Before Deliver

**This is a MANDATORY step, do not skip:**

```
□ Read actual code (re-open files)
□ Verify each U.4 criterion (line-by-line)
□ Run verification step (actually ran it)
□ No banned patterns: "// ...", "// TODO"
□ Cross-check with original request
```

**Anti-pattern:** "I think it works" → §X prevents this.

---

## §Y - Receiving Feedback

```
1. Read FULL feedback before responding
2. Verify each claim against code
3. Ask clarification if unclear
4. Push back if wrong (with evidence)
5. Fix or document "won't fix - because..."
6. Re-run §X after changes
```

---

## Cross-Agent Workflow Adapters

### Adapter: Cursor → Other Agents

When migrating patterns from Cursor to other agents:
- Replace `K.X` gates with corresponding `U.X` gates
- Document agent-specific quirks in skill metadata
- Test gate execution in each agent environment

### Adapter: Universal → Agent-Specific

For universal compatibility:
1. Execute U.1-U.7 (always required)
2. Append agent-specific gates if available
3. Skip gates not supported by current agent
4. Document any compatibility issues

### Adapter: Agent Detection Flow

```python
def detect_agent():
    if os.getenv("CURSOR_IDE"):
        return "cursor"
    elif os.getenv("CODEX_ENABLED"):
        return "codex"
    elif os.getenv("CLAUDE_IDE"):
        return "claude-code"
    elif os.getenv("GROK_API_KEY"):
        return "grok"
    else:
        return "unknown"
```

---

## Integration Flow

```
┌──────────────────────────────────────────────────────────────────┐
│ AGENT DETECTION (auto-detect via environment variables)         │
└──────────────────────────────────┬───────────────────────────────┘
                                   ↓
┌──────────────────────────────────────────────────────────────────┐
│ Universal Pre-Gates (U.1-U.4)                                    │
│ Think + Scope + Goals                                           │
└──────────────────────────────────┬───────────────────────────────┘
                                   ↓
┌──────────────────────────────────────────────────────────────────┐
│ Agent-Specific Pre-Gates (optional, if agent supports)        │
│ C.X (Claude) | CX.X (Codex) | G.X (Grok) | K.X (Cursor)       │
└──────────────────────────────────┬───────────────────────────────┘
                                   ↓
┌──────────────────────────────────────────────────────────────────┐
│ [Primary Skill]                                                 │
│ frontend-taste, security-review, etc.                          │
└──────────────────────────────────┬───────────────────────────────┘
                                   ↓
┌──────────────────────────────────────────────────────────────────┐
│ Universal Post-Gates (U.5-U.7) + §X                              │
│ Verify surgical + goals                                         │
└──────────────────────────────────┬───────────────────────────────┘
                                   ↓
┌──────────────────────────────────────────────────────────────────┐
│ Agent-Specific Post-Gates (optional)                           │
└──────────────────────────────────┬───────────────────────────────┘
                                   ↓
                              DELIVER
```

---

## Agent Compatibility Notes

### Cursor IDE
- **Strengths:** Full MCP integration, rule file support
- **Limitations:** None significant
- **Best practices:** Use `.cursor/rules/` for persistent guidance

### Codex (cursor.com)
- **Strengths:** Cloud-based, repository awareness
- **Limitations:** MCP tools may differ from local
- **Best practices:** Export `ORIGIN_HOST` for repo context

### Claude Code (@cursor/codex)
- **Strengths:** Anthropic reasoning, long context
- **Limitations:** Different tool naming conventions
- **Best practices:** Use `--dangerously-skip-permissions` sparingly

### Grok (x.com/grok)
- **Strengths:** Real-time information access
- **Limitations:** May have different code style preferences
- **Best practices:** Verify generated code against project style

### Graceful Degradation

If an agent doesn't support all gates:
1. Execute all universal gates (U.1-U.7 + §X)
2. Attempt agent-specific gates
3. Skip gracefully if not supported
4. Log compatibility issues

---

## Indicators → Actions

| Signal | Action |
|--------|--------|
| "just do it" | Slow down, U.1-U.2 first |
| Unclear request | Ask before assuming |
| 200+ lines proposed | Check if 50 works |
| Adjacent "improved" | Roll back |
| Multiple interpretations | Present options |
| "I assumed..." | Should have asked first |
| Agent-specific error | Use universal fallback |

---

## Anti-Patterns

| Violation | Fix |
|-----------|-----|
| Assume instead of ask | Stop, ask |
| Over-engineer | Simplify |
| Touch unrelated code | Stay surgical |
| No success criteria | Define first |
| 200 lines when 50 works | Rewrite |
| Agent gate not supported | Skip, use universal |

---

## Success Metrics

- Fewer unnecessary changes in diffs
- Clarifying questions BEFORE implementation
- Simplicity maintained across all agents
- Surgical changes only
- Cross-agent compatibility verified
