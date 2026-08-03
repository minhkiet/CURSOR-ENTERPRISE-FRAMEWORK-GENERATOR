---
description: PixelRAG skill cho Visual Retrieval-Augmented Generation - đọc tài liệu bằng hình ảnh (PDF, website, bảng biểu, sơ đồ). Cải thiện độ chính xác retrieval 18.1% so với Text RAG truyền thống. Tích hợp pixelshot CLI, Qwen3-VL-Embedding, và FAISS index.
created: 2026-06-26
version: 1.0.0
tags: [pixelrag, visual-rag, screenshot, document, pdf, vision, multimodal, embedding, faiss, retrieval, tables, charts, diagrams]
---

# PixelRAG - Visual Retrieval-Augmented Generation Skill

## Tổng quan

PixelRAG là hệ thống RAG dựa trên hình ảnh, cho phép AI "nhìn" tài liệu như con người nhìn màn hình thay vì đọc text. Điều này đặc biệt hữu ích cho:

- Tài liệu có nhiều bảng biểu phức tạp
- Báo cáo tài chính với số liệu
- PDF khoa học với công thức, hình vẽ
- Website có layout phức tạp
- Knowledge base nội bộ doanh nghiệp
- Trích xuất dữ liệu từ infographic

### Ưu điểm so với Text RAG

| Metric | Text RAG | PixelRAG | Improvement |
|--------|----------|----------|-------------|
| Retrieval accuracy | Baseline | +18.1% | +18.1% |
| Table comprehension | Poor | Excellent | Game-changer |
| Chart/diagram understanding | None | Full | Native |
| Token efficiency | Baseline | -60% | Significant |
| Layout preservation | Lost | Intact | Critical |

### Kiến trúc hoạt động

```
Render trang → Chia thành screenshot tiles → Vision Embedding → FAISS Index → Retrieval → VLM trả lời
```

## Kích hoạt khi

- Đọc tài liệu PDF phức tạp
- Phân tích báo cáo tài chính
- Hỏi đáp về bảng biểu, sơ đồ
- Web scraping với layout preservation
- Knowledge base với mixed content
- Trích xuất dữ liệu từ hình ảnh
- Tài liệu khoa học có công thức
- Document Q&A với visual content
- "đọc file PDF", "phân tích bảng", "hỏi về biểu đồ"
- "screenshot website", "visual search", "pixel-native"

## Pipeline Commands

| Command | Description | Install |
|---------|-------------|---------|
| `pixelshot` | Document → image tiles | `pip install pixelrag` |
| `pixelrag chunk` | Tiles → chunks metadata | `pip install 'pixelrag[embed]'` |
| `pixelrag embed` | Chunks → vectors (Qwen3-VL) | `pip install 'pixelrag[embed]'` |
| `pixelrag build-index` | Vectors → FAISS index | `pip install 'pixelrag[index]'` |
| `pixelrag index` | Full pipeline (source → index) | `pip install 'pixelrag[index]'` |
| `pixelrag serve` | FAISS search API (FastAPI) | `pip install 'pixelrag[serve]'` |

## Auto-Dependencies

```json
{
  "python": ">=3.10",
  "packages": ["pixelrag[full]"],
  "tools": {
    "pixelshot": "uv tool install pixelrag",
    "playwright": "pip install playwright && playwright install chromium"
  },
  "optional_gpu": {
    "cuda": "Linux GPU",
    "mps": "Apple Silicon"
  }
}
```

## Pre-Review Gate

### P.1 Document Analysis

- [ ] Xác định loại document (PDF, website, local file)
- [ ] Đánh giá độ phức tạp của visual content:
  - Có bảng biểu không? Bao nhiêu? Phức tạp không?
  - Có sơ đồ, biểu đồ không?
  - Có layout đặc biệt cần preserve?
- [ ] Xác định use case: Q&A, search, extraction?

### P.2 Strategy Selection

- [ ] **PixelRAG Native** (recommend for visual-heavy docs):
  - Tables, charts, diagrams
  - Complex layouts
  - Scientific papers with figures
  
- [ ] **Hybrid (PixelRAG + Text RAG)** (for mixed content):
  - Text-heavy with some visuals
  - Need both semantic search and visual understanding
  
- [ ] **Text RAG only** (NOT recommended for visual docs):
  - Pure text documents
  - Simple formatting

### P.3 Infrastructure Planning

- [ ] Device selection:
  - `device: cuda` - Linux with NVIDIA GPU
  - `device: mps` - Apple Silicon
  - `device: cpu` - Fallback (slower)
- [ ] Index storage planning (FAISS indexes can be large)
- [ ] Serve endpoint planning (local vs hosted API)

### P.4 Pre-Code Checklist

- [ ] Document type identified
- [ ] Visual complexity assessed
- [ ] Strategy selected (PixelRAG vs Hybrid)
- [ ] Device confirmed (cuda/mps/cpu)
- [ ] Dependencies identified

## Implementation Guidelines

### Phase 1: Installation & Setup

```bash
# Install pixelrag (choose extras as needed)
pip install 'pixelrag[index]'  # Full pipeline for building indexes
pip install 'pixelrag[serve]'   # For serving API

# Install playwright for screenshot capture
pip install playwright
playwright install chromium

# Or use uv (recommended for clean isolation)
uv tool install pixelrag
```

### Phase 2: Configuration (pixelrag.yaml)

```yaml
# For building your own index
source:
  type: local
  path: ./my_docs

embed:
  model: Qwen/Qwen3-VL-Embedding-2B
  device: auto  # auto-detect: cuda > mps > cpu

output: ./my_index
```

### Phase 3: Document Processing

```bash
# Quick start - render a PDF to tiles
curl -L -o paper.pdf https://raw.githubusercontent.com/StarTrail-org/PixelRAG/main/assets/pixelrag-paper.pdf
pixelshot paper.pdf -o ./tiles --dpi 200

# Or render a website
pixelshot https://en.wikipedia.org/wiki/Python -o ./tiles

# Build index
pixelrag index build

# Serve locally
pixelrag serve --index-dir ./my_index --port 30001
```

### Phase 4: Query with Visual Context

```bash
# Query the index
curl -X POST http://localhost:30001/search \
  -H "Content-Type: application/json" \
  -d '{"queries": [{"text": "Overview of PixelRAG and the diagram"}], "n_docs": 1}'
```

### Python API Usage

```python
from pixelrag_render import render_url, render_file

# Render a single page for agent to read
tiles = render_url("https://en.wikipedia.org/wiki/Python", "./tiles")
# Returns list of tile paths

# Or render PDF
tiles = render_file("document.pdf", "./tiles", dpi=200)
```

## Comparison: Text RAG vs PixelRAG

### Text RAG (Traditional)

```python
# Text RAG - loses table structure
loader = PDFLoader("report.pdf")
text = loader.load()
chunks = text_splitter.split_text(text)
embeddings = embedding_model.embed(chunks)
# Table becomes: "The quarterly revenue was $1.2M, $1.5M, $1.8M, and $2.1M..."
# Question "Which quarter had highest revenue?" → confuses order
```

### PixelRAG (Visual)

```python
# PixelRAG - preserves table structure
tiles = render_file("report.pdf", "./tiles", dpi=200)
# Table becomes an image tile
# Question "Which quarter had highest revenue?" → reads table image directly
# Answer: "Q4 with $2.1M"
```

### When to Use Each

| Use Case | Recommended | Why |
|----------|-------------|-----|
| Simple text Q&A | Text RAG | Faster, simpler |
| Table-heavy documents | **PixelRAG** | Native table reading |
| Financial reports | **PixelRAG** | Precise number extraction |
| Scientific papers | **PixelRAG** | Figure/equation preservation |
| Websites with charts | **PixelRAG** | Layout understanding |
| Knowledge bases | Hybrid | Both semantic + visual search |
| Code documentation | Text RAG | Code is text-based |

## Hybrid Architecture (Recommended for Knowledge Bases)

```yaml
# pixelrag-hybrid.yaml
source:
  type: local
  path: ./knowledge_base

embed:
  vision_model: Qwen/Qwen3-VL-Embedding-2B
  text_model: text-embedding-3-small
  device: auto

output: ./hybrid_index

# This creates TWO indexes:
# 1. Visual index (FAISS) - for tables, charts, diagrams
# 2. Text index (FAISS) - for semantic search
```

## Post-Review Gate

### P.5 Retrieval Quality

- [ ] Relevant tiles returned for queries
- [ ] Tables/figures correctly identified
- [ ] No irrelevant results (hallucination in retrieval)
- [ ] Response accuracy verified against source

### P.6 Performance

- [ ] Embedding generation time acceptable
- [ ] Search latency within SLA
- [ ] Index size optimized
- [ ] GPU utilization efficient (if applicable)

### P.7 Token Efficiency

- [ ] Retrieved tiles are concise (not full document)
- [ ] Token budget respected
- [ ] Response includes citations

### P.8 Quality Verification

- [ ] Table questions answered correctly
- [ ] Chart/diagram questions answered correctly
- [ ] Layout questions answered correctly
- [ ] No hallucinations in answers

## Anti-Patterns

- [ ] **Using Text RAG for visual documents** - loses critical information
- [ ] **Low DPI for screenshots** - unreadable text in tiles
- [ ] **No overlap in tiles** - missing content at boundaries
- [ ] **Ignoring table structure** - treating tables as plain text
- [ ] **Over-embedding** - too many tiles稀释 relevance
- [ ] **CPU for large datasets** - extremely slow, use GPU/MPS

## Use Cases Examples

### Financial Report Analysis

```
Query: "What was the YoY growth for Q3 2023?"
Text RAG: May confuse quarters, hallucinate numbers
PixelRAG: Reads table directly → "17.3% YoY growth"
```

### Scientific Paper Q&A

```
Query: "Explain the architecture diagram in section 3"
Text RAG: Cannot access figures
PixelRAG: Shows diagram tile → accurate explanation
```

### Complex Table Query

```
Query: "Which product category had the highest margin?"
Text RAG: May misread column alignment
PixelRAG: Reads table as image → correct answer
```

## Integration với Cursor Enterprise Framework

PixelRAG hoạt động tốt với:

- **weknora-kb**: Knowledge base với visual content
- **weknora-agent**: ReAct agent có thể browse visual content
- **RAG rule**: Bổ sung visual retrieval vào pipeline
- **Claude integration**: Claude có thể đọc screenshot tiles

## Deliverables Checklist

```
[ ] Installation commands provided
[ ] Configuration (pixelrag.yaml) template
[ ] Document processing workflow
[ ] Index building pipeline
[ ] API serve setup
[ ] Query examples
[ ] Hybrid setup (if applicable)
[ ] Performance optimization tips
```

---

**Source:** [StarTrail-org/PixelRAG](https://github.com/StarTrail-org/PixelRAG) (Apache-2.0 License)

**Key Features:**
- 18.1% improvement in retrieval accuracy
- Native table/chart/diagram understanding
- 60% token reduction vs Text RAG
- Qwen3-VL-Embedding model
- FAISS vector search
- Pre-built Wikipedia index (8.28M pages)
- Cross-platform (Linux CUDA, macOS MPS, CPU fallback)

**Last Updated:** 2026-06-26
