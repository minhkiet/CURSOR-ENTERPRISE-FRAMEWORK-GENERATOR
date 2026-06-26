---
description: Karpathy Coding Discipline - Think Before Coding, simplicity, surgical changes, goal-driven execution. Mandatory overlay for all coding tasks. Complements ponytail for YAGNI optimization.
created: 2026-06-26
version: 1.1.0
tags: [karpathy, coding-discipline, vibe-code, simplicity, minimal, goal-driven, surgical, think-first]
---

# Karpathy Coding Discipline

## Tổng quan

Skill này tích hợp nguyên tắc từ [andrej-karpathy-skills](https://github.com/multica-ai/andrej-karpathy-skills) - 182k stars GitHub repo của Andrej Karpathy về cách giảm LLM coding mistakes.

**Đây là MANDATORY OVERLAY SKILL** — luôn chạy với mọi coding task. Think Before Coding, sau đó implement surgical.

## Complementarity with Ponytail

| Phase | Skill | Focus |
|-------|-------|-------|
| **THINK FIRST** | karpathy-coding | What to build? What are the options? What's the minimal scope? |
| **THEN BUILD** | ponytail (optional) | How to build it with least code? Use platform features? Skip YAGNI? |

**Flow:**
```
User Request
    ↓
karpathy-pre [K.1-K.4]  ← Think: assumptions, scope, goals
    ↓
[ponytail-pre]          ← YAGNI Ladder (if enabled)
    ↓
IMPLEMENT               ← Minimal code that solves the problem
    ↓
[ponytail-post]         ← Code reduction check (if enabled)
    ↓
karpathy-post [K.5-K.7] ← Verify surgical + goals achieved
    ↓
DELIVER
```

> **Note:** Ponytail enhances karpathy-coding by adding YAGNI optimization. They are complementary, not conflicting.

## Nguyên tắc cốt lõi

### 1. Think Before Coding

**Don't assume. Don't hide confusion. Surface tradeoffs.**

Trước khi implement:
- State your assumptions explicitly. Nếu không chắc → hỏi.
- Nếu có nhiều cách interpret → present all, don't pick silently.
- Nếu có approach đơn giản hơn → nói ra, push back when warranted.
- Nếu có gì unclear → STOP. Name what's confusing. Ask.

### 2. Simplicity First

**Minimum code that solves the problem. Nothing speculative.**

- Không features ngoài scope
- Không abstractions cho single-use code
- Không "flexibility" hay "configurability" không được request
- Không error handling cho impossible scenarios
- Nếu viết 200 lines mà có thể 50 → rewrite

**Ask yourself:** "Would a senior engineer say this is overcomplicated?" If yes → simplify.

### 3. Surgical Changes

**Touch only what you must. Clean up only your own mess.**

Khi edit existing code:
- Don't "improve" adjacent code, comments, or formatting
- Don't refactor things that aren't broken
- Match existing style, even if you'd do it differently
- Nếu notice dead code → mention it, don't delete it

Khi changes create orphans:
- Remove imports/variables/functions mà CHÍNH MÌNH tạo ra → removed
- Don't remove pre-existing dead code unless asked

**The test:** Every changed line should trace directly to the user's request.

### 4. Goal-Driven Execution

**Define success criteria. Loop until verified.**

Transform tasks into verifiable goals:
- "Add validation" → "Write tests for invalid inputs, then make them pass"
- "Fix the bug" → "Write a test that reproduces it, then make it pass"
- "Refactor X" → "Ensure tests pass before and after"

Multi-step tasks plan:
```
1. [Step] → verify: [check]
2. [Step] → verify: [check]
3. [Step] → verify: [check]
```

## Pre-Review Gate (Trước khi code)

### K.1 Think Before Coding
- [ ] State assumptions explicitly — đang assume gì về request?
- [ ] Nếu uncertain về interpretation nào → STOP and ask
- [ ] Nếu có multiple valid interpretations → present options
- [ ] Nếu có simpler approach → say so, push back
- [ ] Nếu có gì unclear → stop, name what's confusing, ask

### K.2 Simplicity Check
- [ ] Is this over-engineered?
- [ ] No speculative features beyond request
- [ ] No abstractions for single-use code
- [ ] No "flexibility" not requested
- [ ] No error handling for impossible scenarios
- [ ] If 200 lines can be 50 → rewrite

### K.3 Surgical Scope
- [ ] What MUST be changed? (list only required changes)
- [ ] What should NOT be touched?
- [ ] Will every changed line trace to request?
- [ ] Match existing style

### K.4 Goal Definition
- [ ] Success criteria defined in verifiable terms
- [ ] Multi-step plan with verification points

## Post-Review Gate (Sau khi code)

### K.5 Implementation Verification
- [ ] Code traces to request: every line connects to ask
- [ ] No adjacent code "improved"
- [ ] No unrelated refactoring
- [ ] Unused imports/variables from MY changes → removed
- [ ] Dead code from MY changes → removed

### K.6 Simplicity Re-Check
- [ ] If 200 lines written but can be 50 → rewrite now
- [ ] No speculative abstractions
- [ ] No "flexibility" not requested
- [ ] No single-use abstractions

### K.7 Goal Achievement
- [ ] Success criteria verified
- [ ] Tests pass (if written)
- [ ] No regressions
- [ ] Changes are minimal and surgical

## Integration với Primary Skills

Karpathy-coding chạy như **OVERLAY** với mọi primary skill:

```
│ Frontend Task │
│     ↓         │
│ karpathy-pre  │ ← Think + Simplicity + Scope + Goals
│     ↓         │
│ taste-pre    │ ← Design direction
│     ↓         │
│ IMPLEMENT     │
│     ↓         │
│ taste-post   │ ← Design review
│     ↓         │
│ karpathy-post │ ← Verify surgical + simplicity + goals
│     ↓         │
│ DELIVER      │
```

**Mọi task đều phải pass karpathy gates như overlay.**

## Indicators

Khi thấy các signals này → karpathy-coding cần được strengthen:

| Signal | Action |
|--------|--------|
| "just do it" / "simple" / "minimal" | Prioritize simplicity |
| Unclear request | Ask before assuming |
| 200+ lines proposed | Check if can be 50 |
| Adjacent code "improved" | Roll back, stay surgical |
| Multiple interpretations | Present options, don't pick |
| "I assumed..." later | Should have asked first |

## Anti-Patterns

### Karpathy Violations

| Violation | Why Bad | Fix |
|-----------|---------|-----|
| Assume instead of ask | Wrong direction, wasted work | Stop, ask |
| Over-engineer | Complex, hard to maintain | Simplify |
| Touch unrelated code | Scope creep, more bugs | Stay surgical |
| No success criteria | Can't verify completion | Define goals first |
| 200 lines when 50 works | Waste, cognitive load | Rewrite |

## Success Metrics

**These guidelines are working if:**
- Fewer unnecessary changes in diffs
- Fewer rewrites due to overcomplication
- Clarifying questions come BEFORE implementation
- Simplicity maintained across all outputs
- Surgical changes only
