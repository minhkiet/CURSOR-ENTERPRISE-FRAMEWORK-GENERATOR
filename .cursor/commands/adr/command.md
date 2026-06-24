---
description: ADR - Tạo Architecture Decision Record
trigger: adr, architecture decision, tạo adr, architecture record, decision record
category: Architecture
framework: Cursor Enterprise Framework V4
version: 1.0.0
---

# Command: /adr

## Mục tiêu
Tạo Architecture Decision Record (ADR) cho các quyết định kiến trúc quan trọng.

## Trigger Keywords
- adr
- architecture decision
- tạo adr
- architecture record
- decision record
- architectural decision
- design decision
- quyết định kiến trúc

## Workflow

### Bước 1: Context
- [ ] Identify the decision to document
- [ ] Gather context và background
- [ ] Check existing ADRs for related decisions

### Bước 2: Decision Analysis
- [ ] Describe the situation
- [ ] List considered options
- [ ] Analyze pros/cons of each option
- [ ] Select the decision

### Bước 3: ADR Creation
- [ ] Follow ADR template
- [ ] Write title và status
- [ ] Write context và decision
- [ ] Write consequences
- [ ] Write related ADRs

### Bước 4: ADR Storage
- [ ] Save to `memory/decisions.sqlite`
- [ ] Save to `memory/decision-history/`
- [ ] Link to related ADRs

## Liên kết
- [[../templates/adr-template]] - ADR Template
- [[../prompts/adr-generator]] - ADR Generator Prompt
- [[../skills/adr-generator]] - ADR Generator Skill
