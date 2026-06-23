---
name: full-output
description: Enforces complete, unabridged code generation. Overrides truncation behavior, bans placeholder patterns, handles token-limit splits cleanly. Applies before and after every code generation task. No TODO comments, no "continue later", no skeleton code.
---

# Full Output Enforcement Skill

> Use on every task requiring exhaustive output. Treat partial output as broken output.
> Includes mandatory pre-generation scope check and post-generation completeness verification.

---

## 0. REVIEW GATE: PRE-GENERATION SCOPE CHECK (Mandatory)

**Before writing any code, lock the scope.**

### 0.A Scope Lock
1. Read the full request completely
2. Count distinct deliverables: files, functions, sections, components, API endpoints, tests
3. Write the count explicitly: **"Delivering N deliverables:"** then list each one by name
4. This count is a contract. Every item on the list must appear in the output.

### 0.B Pre-Generation Checklist (PASS GATE)
Before writing code:
- [ ] Full request read and understood
- [ ] Deliverable count locked (N items minimum)
- [ ] All dependencies identified (packages, environment, tools)
- [ ] Framework/stack confirmed from codebase or request
- [ ] Output file paths confirmed
- [ ] Test strategy identified

---

## 1. BASELINE PRINCIPLE

Treat every task as production-critical. A partial output is a broken output.

- Optimize for **completeness**, not brevity
- If the user asks for a full file, deliver the full file
- If the user asks for 5 components, deliver 5 components
- No exceptions, no "you can extend this later"

---

## 2. BANNED OUTPUT PATTERNS

These are hard failures. Never produce them:

### 2.A In Code Blocks
- `// ...`, `// rest of code`, `// implement here`
- `// TODO`, `/* ... */`, `// similar to above`
- `// continue pattern`, `// add more as needed`
- Bare `...` standing in for omitted code
- `// [code omitted]`, `// [skipped]`

### 2.B In Prose
- "Let me know if you want me to continue"
- "I can provide more details if needed"
- "For brevity" / "for simplicity"
- "The rest follows the same pattern"
- "Similarly for the remaining"
- "And so on" (when replacing actual content)
- "I'll leave that as an exercise"
- "You can extend this by..."

### 2.C Structural Shortcuts
- Outputting a skeleton when the request was for a full implementation
- Showing first and last section while skipping the middle
- Replacing repeated logic with one example and a description
- Describing what code should do instead of writing it
- Using comments to describe logic instead of actual code

---

## 3. EXECUTION PROCESS

### Step 1: Build
Generate every deliverable completely. No partial drafts.

### Step 2: Cross-Check (Mandatory)
Before final output, re-read the original request. Compare:
- Deliverable count matches scope count
- Every file listed is present and complete
- Every function listed is fully implemented
- Every component listed has all states (loading, empty, error, default)

### Step 3: Self-Verify
Run the post-generation checklist before delivering.

---

## 4. HANDLING LONG OUTPUTS

When a response approaches the token limit:

1. **Do NOT compress** remaining sections to squeeze them in
2. **Do NOT skip ahead** to a conclusion
3. **Write at full quality** up to a clean breakpoint (end of a function, end of a file, end of a section)
4. **End with a PAUSE marker:**

```
[PAUSED — X of Y complete. Send "continue" to resume from: next section name]
```

On "continue", pick up **exactly** where you stopped. No recap, no repetition.

---

## 5. REVIEW GATE: POST-GENERATION VERIFICATION (Mandatory)

**Before finalizing, verify ALL of the following:**

### 5.A Completeness Check
- [ ] No banned patterns from Section 2 appear anywhere in output
- [ ] Every item from the scope list is present and finished
- [ ] Code blocks contain actual runnable code, not descriptions of what code would do
- [ ] Nothing was shortened to save space
- [ ] No skeleton code when full implementation was requested
- [ ] No skipped sections or "similarly for the rest" replacements

### 5.B Quality Check
- [ ] All imports actually exist in package.json or are standard library
- [ ] No hardcoded values that should be environment variables
- [ ] Error handling present for all async operations
- [ ] Type definitions complete (for TypeScript)
- [ ] Tests written for all new functions/components
- [ ] No commented-out debug code left in
- [ ] No TODO comments remaining (replace with actual implementation or document as backlog item)

### 5.C File Structure Check
- [ ] All file paths match the requested structure
- [ ] Entry points (index, main, app) correctly exported
- [ ] No circular import issues
- [ ] All referenced files actually exist in output

---

## 6. SPECIAL CASES

### 6.A Multi-File Projects
For projects with many files, use a **file manifest** at the start:
```
Delivering 7 files:
1. src/components/Button.tsx
2. src/components/Card.tsx
3. src/components/Modal.tsx
4. src/hooks/useAuth.ts
5. src/pages/login.tsx
6. src/pages/dashboard.tsx
7. src/styles/globals.css
```
Then deliver each file completely. Cross off each item as delivered.

### 6.B Generated Skeleton (Only When Explicitly Requested)
If the user explicitly asks for a "skeleton" or "outline", deliver exactly that:
- All files with correct paths
- Function signatures with complete types
- Empty bodies with a comment describing what the function should do
- But still NO banned patterns like `// ...` or `// TODO`

### 6.C Truncated Response Recovery
If output was truncated mid-delivery:
1. State exactly where you stopped: "Last delivered: src/components/Modal.tsx, line 45"
2. Resume from the exact stopping point
3. Do not re-summarize or re-explain what was already delivered
4. Deliver the remaining items completely
