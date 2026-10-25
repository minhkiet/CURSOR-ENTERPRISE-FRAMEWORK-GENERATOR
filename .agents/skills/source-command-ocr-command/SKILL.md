---
name: "source-command-ocr-command"
description: "Migrated source command `ocr-command`"
---

# source-command-ocr-command

Use this skill when the user asks to run the migrated source command `ocr-command`.

## Command Template

# OCR Command

Extract text from images, screenshots, and scanned documents using Tesseract OCR.

## Usage

```
/ocr <image_path> [options]
/ocr extract <image_path> [-l lang] [-o output]
/ocr preview <image_path>
```

## Options

| Flag | Description | Default |
|------|-------------|---------|
| `-l, --lang` | Language code | `vie+eng` |
| `-o, --output` | Output file path | stdout |
| `--no-preprocess` | Skip preprocessing | false |
| `--json` | Output as JSON | false |
| `--psm` | Page segmentation mode | auto |
| `--preprocessor` | Engine: pillow/opencv | pillow |

## Examples

### Basic OCR

```
/ocr document.png
```

### Vietnamese Document

```
/ocr hoadon.png -l vie -o text.txt
```

### With JSON Output

```
/ocr screenshot.png --json
```

### OpenCV Preprocessing

```
/ocr receipt.png --preprocessor opencv
```

## Language Codes

| Code | Language |
|------|----------|
| `vie` | Vietnamese |
| `eng` | English |
| `vie+eng` | Vietnamese + English |
| `chi_sim` | Simplified Chinese |
| `jpn` | Japanese |
| `kor` | Korean |

## Workflow

### 1. Quick Extract

```
/ocr <image_path>
```

### 2. Language-Specific

```
/ocr <image_path> -l <lang>
```

### 3. Save to File

```
/ocr <image_path> -o output.txt
```

## Integration

This command uses the OCR tool at `.cursor/scripts/ocr_tool.py`.

```bash
python .cursor/scripts/ocr_tool.py <image> [options]
```
