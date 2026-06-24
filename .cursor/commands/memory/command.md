---
description: Memory - Quản lý memory system (build, query, update memory)
trigger: memory, quản lý memory, build memory, update memory, memory system, session summary
category: Memory
framework: Cursor Enterprise Framework V4
version: 1.0.0
---

# Command: /memory

## Mục tiêu
Quản lý memory system - build, query, update, và maintain memory.

## Trigger Keywords
- memory
- quản lý memory
- build memory
- update memory
- memory system
- session summary
- context memory
- project memory
- decisions memory
- bugs memory

## Sub-Commands

### /memory build
- [ ] Run `memory-builder/build-memory.ps1`
- [ ] Build decisions index
- [ ] Build bugs index
- [ ] Build project index
- [ ] Build code index

### /memory query
- [ ] Query decisions.sqlite
- [ ] Query bugs.sqlite
- [ ] Query session history
- [ ] Return relevant context

### /memory update
- [ ] Update session summary
- [ ] Add new ADR decision
- [ ] Add new bug record
- [ ] Update prompt cache

### /memory stats
- [ ] Show memory statistics
- [ ] Show hit rate
- [ ] Show staleness rate
- [ ] Show memory size

## Liên kết
- [[../rules/memory-first]] - Memory First Rules
- [[../skills/memory-manager]] - Memory Manager Skill
- [[../scripts/memory-builder]] - Memory Builder Script
- [[../memory/]] - Memory Directory
