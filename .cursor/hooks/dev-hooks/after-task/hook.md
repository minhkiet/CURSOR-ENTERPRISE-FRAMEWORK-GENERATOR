---
description: After-Task Hook - Update memory va summarize sau khi hoan thanh task
trigger: sau task, after task, ket thuc task
framework: Cursor Enterprise Framework V4
version: 1.0.0
---

# Hook: after-task

## Muc tieu
Update memory, create summary, va cleanup sau khi hoan thanh task.

## Trigger
Tu dong trigger sau khi hoan thanh moi task.

## Workflow

### Buoc 1: Task Summary
- [ ] Collect task description
- [ ] Collect changes made
- [ ] Collect files modified
- [ ] Collect decisions made
- [ ] Collect issues encountered

### Buoc 2: Memory Update
- [ ] Update session summary
- [ ] Add new ADRs if any
- [ ] Add new bug records if any
- [ ] Update code index if needed
- [ ] Update prompt cache

### Buoc 3: Knowledge Update
- [ ] Check if knowledge files need update
- [ ] Add new patterns discovered
- [ ] Update anti-patterns
- [ ] Update best practices

### Buoc 4: Token Usage
- [ ] Record token usage for this task
- [ ] Update token budget
- [ ] Optimize if over budget

### Buoc 5: Cleanup
- [ ] Clear temporary files
- [ ] Clear cached data
- [ ] Clear tool outputs

### Buoc 6: Report
- [ ] Print task summary
- [ ] Print changes made
- [ ] Print memory updates
- [ ] Print token usage

## Lien ket
- [[../rules/memory-first]] - Memory First Rules
- [[../rules/token-optimization]] - Token Optimization Rules
- [[../scripts/memory-builder]] - Memory Builder Script
