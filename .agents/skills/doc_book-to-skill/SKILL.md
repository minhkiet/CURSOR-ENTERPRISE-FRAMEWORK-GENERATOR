---
name: book-to-skill
description: "Converts books and documents (PDF, EPUB, DOCX, HTML, Markdown, plain text, RTF, MOBI/AZW with Calibre) into structured agent skills, extracting frameworks, mental models, principles, techniques, and anti-patterns. Use when the user wants to study a document through GitHub Copilot CLI, Amp, or Claude Code, apply an author's frameworks while working, or build a reusable knowledge base from a file."
---

# Book-to-Skill Converter

Transform written knowledge into actionable agent skills by extracting structure — not producing summaries.

## Philosophy

Books contain crystallized expertise: frameworks, principles, and techniques that took years to develop. This skill extracts that knowledge into a format GitHub Copilot CLI, Amp, Claude Code, or another compatible agent can leverage repeatedly.

**Extract structure, not summaries.** A skill isn't a book report. It's a toolkit of:
- Named frameworks (mental models with clear application)
- Actionable principles (rules that guide decisions)
- Techniques (step-by-step methods)
- Anti-patterns (what to avoid and why)
- Voice calibration (how the author thinks and communicates)

**Preserve the author's precision.** Frameworks often have specific names for reasons. "The 5 Whys" isn't interchangeable with "ask why multiple times." Capture the exact formulation.

**Layer depth appropriately.** Simple books → simple skills. Complex books with 10+ frameworks → skills with reference files and on-demand chapters.

---

## Supported Formats

| Format | Extension | Notes |
|--------|----------|-------|
| PDF | `.pdf` | Use `pdf-extract.py` or OCR if scanned |
| EPUB | `.epub` | Extract HTML chapters |
| DOCX | `.docx` | Parse XML structure |
| Markdown | `.md`, `.markdown` | Direct parsing |
| HTML | `.html`, `.htm` | Strip tags, preserve structure |
| Plain Text | `.txt` | Basic tokenization |
| RTF | `.rtf` | Strip formatting |
| MOBI/AZW | `.mobi`, `.azw` | Convert via Calibre first |

---

## Modes of Operation

### 1. Full Conversion (Default)
**Trigger:** User provides document path without special instructions
**Action:** Run all steps (0-9)
**Output:** Complete skill with SKILL.md, chapters/, glossary, patterns, cheatsheet

### 2. Analyze Only
**Trigger:** User says "analyze", "just extract", "review before generating"
**Action:** Steps 0-3, produce structured extraction report
**Output:** Analysis report for user review

### 3. Generate from Prior Analysis
**Trigger:** User has existing analysis notes
**Action:** Skip 0-3, use provided analysis, run Steps 4-9
**Output:** Skill files from analysis

### 4. Update / Fold-in
**Trigger:** User provides new sources to update existing skill
**Action:** Merge new content into existing skill
**Output:** Updated existing skill

---

## Step 0 — Out-of-scope check

If no arguments provided, stop with:
> "book-to-skill requires a supported document path. Usage: `book-to-skill <path> [skill-name]`"

---

## Step 1 — Validate Input

Check for supported file types:
- `.pdf`, `.epub`, `.docx`, `.txt`, `.md`, `.html`, `.rst`, `.adoc`, `.rtf`, `.mobi`, `.azw`

If no supported files found, stop with error.

---

## Step 2 — Identify Content Type

Ask user:
> "What kind of content is this?"
- Business/Management book
- Technical/Programming book
- Self-help/Productivity
- Philosophy/Psychology
- Academic/Research
- Fiction (not recommended)

---

## Step 3 — Extract Content

### PDF Extraction
```bash
python3 .cursor/scripts/pdf-extract.py <file.pdf>
```

### EPUB Extraction
```bash
unzip -q <file.epub> -d /tmp/epub_extract/
```

### DOCX Extraction
```bash
python3 -c "from docx import Document; doc = Document('<file.docx>'); print('\n'.join([p.text for p in doc.paragraphs]))"
```

---

## Step 4 — Identify Frameworks

Scan for patterns:
- Named concepts (capitalized terms)
- Numbered lists (The 7 Habits)
- Acronyms (SMART, SWOT, OODA)
- Two-column contrasts (Eisenhower Matrix)
- Process steps (The 5 Whys)
- Framework names in bold/headers

---

## Step 5 — Extract Frameworks

For each framework found:
1. **Name** — exact term used by author
2. **Core principle** — one-sentence explanation
3. **When to use** — context/application
4. **How to apply** — step-by-step method
5. **Example** — real-world usage
6. **Anti-patterns** — common mistakes

---

## Step 6 — Extract Principles

Principles are rules that guide decisions:
- Actionable statements
- Specific enough to apply
- Often appear as rules, laws, or guidelines

Format:
```
### [Principle Name]

**What:** [Statement]
**Why:** [Rationale]
**When:** [Application context]
**Example:** [Usage example]
```

---

## Step 7 — Extract Anti-patterns

Anti-patterns warn against common mistakes:
- "Don't do X"
- "Avoid Y"
- "Most people fail by doing Z"

Format:
```
### [Anti-pattern Name]

**Problem:** [What goes wrong]
**Why:** [Root cause]
**Solution:** [What to do instead]
```

---

## Step 8 — Create Glossary

Extract key terms with definitions:
```
## Glossary

- **Term**: Definition
- **Term**: Definition
```

---

## Step 9 — Generate Skill Structure

Create directory structure:
```
<skill-name>/
├── SKILL.md              # Main skill file
├── chapters/            # Chapter summaries
│   ├── chapter-01.md
│   └── chapter-02.md
├── glossary.md          # Key terms
├── patterns.md          # Frameworks & techniques
├── principles.md       # Actionable rules
├── anti-patterns.md    # What to avoid
└── cheatsheet.md        # Quick reference
```

---

## SKILL.md Template

```markdown
---
name: <skill-name>
description: "<One-line description of what this skill provides>"
---

# [Book Title]

Based on "[Book Title]" by [Author]

## Core Frameworks

1. [Framework 1]
2. [Framework 2]

## Quick Start

[3-5 most important things to know]

## Frameworks

### [Framework Name]

**What:** One-sentence summary
**When:** When to use this
**How:**
1. Step one
2. Step two
3. Step three

## Principles

### [Principle Name]

[Description with application]

## Anti-patterns

### [Common Mistake]

**Problem:** What goes wrong
**Solution:** What to do instead

## References

- Chapter [N]: [Topic]
- [Page reference]: [Detail]
```

---

## Voice Calibration

Extract how the author thinks:
- Writing style (academic, casual, prescriptive)
- Tone (serious, encouraging, critical)
- Key assumptions
- Common examples used
- What the author emphasizes

---

## Usage Examples

### Convert a book
```bash
book-to-skill ./my-book.pdf "atomic-habits"
```

### Analyze only
```bash
book-to-skill ./my-book.pdf "analyze"
```

### Update existing skill
```bash
book-to-skill ./new-chapters.pdf "atomic-habits" --update
```

---

## Tips

1. **Preserve exact names** — "The 5 Whys" not "ask why multiple times"
2. **Extract actionable steps** — not just concepts
3. **Include anti-patterns** — what to avoid is as important as what to do
4. **Preserve examples** — real applications help understanding
5. **Layer appropriately** — simple book = simple skill

---

## Integration

This skill integrates with:
- `.cursor/skills/` — for Codex IDE skills
- `.github/skills/` — for GitHub Copilot skills
- `~/.claude/skills/` — for Claude Code skills
- `~/.copilot/skills/` — for GitHub Copilot CLI skills
