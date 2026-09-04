---
name: "source-command-doc-command"
description: "Doc - Tạo tài liệu (README, API docs, inline docs)"
---

# source-command-doc-command

Use this skill when the user asks to run the migrated source command `doc-command`.

## Command Template

# Command: /doc

## Mục tiêu
Tạo và duy trì tài liệu cho codebase.

## Trigger Keywords
- doc
- document
- tài liệu
- documentation
- generate doc
- tạo doc
- write doc
- api doc
- readme
- inline doc
- jsdoc

## Doc Types

### /doc readme
- [ ] Analyze codebase structure
- [ ] Write project overview
- [ ] Write getting started guide
- [ ] Write architecture overview
- [ ] Write contribution guide
- [ ] Write deployment guide
- [ ] Write troubleshooting guide

### /doc api
- [ ] Load api rules
- [ ] Generate API documentation
- [ ] Document request/response schemas
- [ ] Document error codes
- [ ] Add examples

### /doc inline
- [ ] Analyze functions/classes
- [ ] Add JSDoc/TSDoc comments
- [ ] Add README comments in code
- [ ] Add architecture decision notes

### /doc adr
- [ ] Load adr-generator skill
- [ ] Identify decision to document
- [ ] Create ADR following template
- [ ] Add to decisions database

## Liên kết
- [[../templates/adr-template]] - ADR Template
- [[../templates/feature-spec-template]] - Feature Spec Template
- [[../skills/knowledge-compiler]] - Knowledge Compiler Skill
- [[../rules/api]] - API Rules
