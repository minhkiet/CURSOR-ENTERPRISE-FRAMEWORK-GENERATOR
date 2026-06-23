---
title: "Multi-modal RAG"
description: "Hướng dẫn về multi-modal RAG: image RAG, table RAG, PDF layout-aware chunking và multimodal embedding models"
tags: ["multimodal", "image-rag", "table-rag", "pdf", "layout-aware", "vision"]
created: "2026-06-23"
version: "1.0.0"
framework: "Cursor Enterprise Framework"
---

# Multi-modal RAG

## Tổng Quan

Multi-modal RAG mở rộng traditional text-based RAG để handle các loại content đa dạng như images, tables, PDFs với complex layouts, và thậm chí audio/video. Trong thực tế, enterprise documents thường chứa mixture của text, figures, tables, và visual elements mà traditional RAG systems bỏ qua.

Các thách thức chính bao gồm:
- Chọn đúng embedding models cho different modalities
- Parsing và understanding complex layouts
- Chunking strategies phù hợp với visual context
- Query routing giữa different modalities
- Synthesizing answers từ multiple content types

## Mục Đích

Tài liệu này nhằm cung cấp kiến thức toàn diện về multi-modal RAG:

Đầu tiên, chúng ta sẽ tìm hiểu image RAG - embedding và retrieve images alongside text.

Thứ hai, tài liệu hướng dẫn table RAG - structured data extraction và retrieval.

Thứ ba, chúng ta sẽ đề cập đến PDF layout-aware chunking.

Cuối cùng, tài liệu cung cấp multimodal embedding models và implementation examples.

## Key Concepts

### 1. Multi-modal Embedding Models

```python
from dataclasses import dataclass
from typing import List, Dict, Union

@dataclass
class MultiModalEmbedding:
    """Multi-modal embedding container."""
    text_embedding: List[float] = None
    image_embedding: List[float] = None
    table_embedding: List[float] = None
    combined_embedding: List[float] = None

class MultiModalEmbeddingModel:
    """
    Multi-modal embedding model supporting text, images, and tables.
    """
    
    def __init__(
        self,
        text_model: str = "text-embedding-3-small",
        vision_model: str = "clip-vit-base-patch32"
    ):
        self.text_model = text_model
        self.vision_model = vision_model
        self._initialize_models()
    
    def _initialize_models(self):
        """Initialize embedding models."""
        # Text embeddings (OpenAI, Cohere, etc.)
        # Vision embeddings (CLIP, etc.)
        pass
    
    async def embed_text(self, text: str) -> List[float]:
        """Embed text."""
        # Use text embedding model
        pass
    
    async def embed_image(self, image_path: str) -> List[float]:
        """Embed image."""
        # Use vision model (CLIP, etc.)
        pass
    
    async def embed_table(self, table: List[List[str]]) -> List[float]:
        """Embed table as structured data."""
        # Flatten table and embed as text
        # Or use specialized table embedding
        pass
    
    async def embed_document(
        self,
        document: Dict
    ) -> MultiModalEmbedding:
        """
        Embed document with all modalities.
        
        document: {
            "text": str,
            "images": List[str],  # Image paths or URLs
            "tables": List[List[List[str]]],  # Table data
            "layout": str  # Page layout information
        }
        """
        embedding = MultiModalEmbedding()
        
        # Embed text
        if document.get("text"):
            embedding.text_embedding = await self.embed_text(document["text"])
        
        # Embed images
        if document.get("images"):
            image_embeddings = [
                await self.embed_image(img)
                for img in document["images"]
            ]
            embedding.image_embedding = self._average_pool(image_embeddings)
        
        # Embed tables
        if document.get("tables"):
            table_embeddings = [
                await self.embed_table(t)
                for t in document["tables"]
            ]
            embedding.table_embedding = self._average_pool(table_embeddings)
        
        # Create combined embedding
        embedding.combined_embedding = self._create_combined_embedding(embedding)
        
        return embedding
    
    def _average_pool(self, embeddings: List[List[float]]) -> List[float]:
        """Average pool multiple embeddings."""
        import numpy as np
        return np.mean(embeddings, axis=0).tolist()
    
    def _create_combined_embedding(
        self,
        embedding: MultiModalEmbedding
    ) -> List[float]:
        """Create combined multi-modal embedding."""
        import numpy as np
        
        embeddings = []
        weights = []
        
        if embedding.text_embedding:
            embeddings.append(embedding.text_embedding)
            weights.append(0.5)
        
        if embedding.image_embedding:
            embeddings.append(embedding.image_embedding)
            weights.append(0.3)
        
        if embedding.table_embedding:
            embeddings.append(embedding.table_embedding)
            weights.append(0.2)
        
        if not embeddings:
            return []
        
        # Weighted average
        weights = np.array(weights) / sum(weights)
        combined = sum(w * np.array(e) for w, e in zip(weights, embeddings))
        
        return combined.tolist()
```

## Image RAG

### 1. Image Processing Pipeline

```python
import base64
from io import BytesIO
from PIL import Image
from typing import Optional

class ImageProcessor:
    """
    Process images for embedding and retrieval.
    """
    
    def __init__(
        self,
        vision_model,
        ocr_model=None
    ):
        self.vision = vision_model
        self.ocr = ocr_model
    
    async def process_image(
        self,
        image_source: Union[str, bytes, Image.Image],
        extract_text: bool = True
    ) -> Dict:
        """
        Process image and extract information.
        
        Returns:
            {
                "image_embedding": List[float],
                "extracted_text": str,
                "image_description": str,
                "metadata": Dict
            }
        """
        # Load image
        image = self._load_image(image_source)
        
        # Generate image embedding
        image_embedding = await self.vision.embed_image(image)
        
        # Extract text via OCR (if enabled)
        extracted_text = ""
        if extract_text and self.ocr:
            extracted_text = await self.ocr.extract_text(image)
        
        # Generate image description
        image_description = await self._describe_image(image)
        
        return {
            "image_embedding": image_embedding,
            "extracted_text": extracted_text,
            "image_description": image_description,
            "metadata": {
                "width": image.width,
                "height": image.height,
                "format": image.format
            }
        }
    
    def _load_image(
        self,
        source: Union[str, bytes, Image.Image]
    ) -> Image.Image:
        """Load image from various sources."""
        if isinstance(source, Image.Image):
            return source
        
        if isinstance(source, str):
            if source.startswith("http"):
                # URL
                import requests
                response = requests.get(source)
                return Image.open(BytesIO(response.content))
            else:
                # File path
                return Image.open(source)
        
        if isinstance(source, bytes):
            return Image.open(BytesIO(source))
        
        raise ValueError(f"Unsupported image source: {type(source)}")
    
    async def _describe_image(self, image: Image.Image) -> str:
        """
        Generate description of image using vision model.
        """
        # Use VLM to describe image
        pass
    
    def extract_visual_elements(
        self,
        image: Image.Image
    ) -> List[Dict]:
        """
        Extract visual elements (text regions, figures, etc.).
        """
        # Use detection model to find regions
        # This would use a specialized model like DETR, YOLO, etc.
        pass
```

### 2. Image Retrieval System

```python
class ImageRAG:
    """
    RAG system for images.
    """
    
    def __init__(
        self,
        vector_store,
        image_processor: ImageProcessor
    ):
        self.vector_store = vector_store
        self.image_processor = image_processor
        self.image_index = {}
    
    async def index_images(
        self,
        images: List[Dict]
    ):
        """
        Index images with their embeddings and metadata.
        
        images: List of {
            "id": str,
            "source": str,  # path, URL, or bytes
            "caption": str,
            "document_id": str,
            "page_number": int
        }
        """
        for img_data in images:
            # Process image
            processed = await self.image_processor.process_image(
                img_data["source"]
            )
            
            # Store metadata
            self.image_index[img_data["id"]] = {
                "id": img_data["id"],
                "caption": img_data.get("caption", ""),
                "extracted_text": processed["extracted_text"],
                "description": processed["image_description"],
                "document_id": img_data.get("document_id"),
                "page_number": img_data.get("page_number"),
                "metadata": processed["metadata"]
            }
            
            # Index for retrieval
            self.vector_store.index(
                ids=[img_data["id"]],
                texts=[
                    self._create_image_text(
                        processed["extracted_text"],
                        processed["image_description"],
                        img_data.get("caption", "")
                    )
                ],
                embeddings=[processed["image_embedding"]]
            )
    
    def _create_image_text(
        self,
        extracted_text: str,
        description: str,
        caption: str
    ) -> str:
        """Create combined text representation of image."""
        parts = []
        
        if caption:
            parts.append(f"Caption: {caption}")
        
        if description:
            parts.append(f"Description: {description}")
        
        if extracted_text:
            parts.append(f"Text: {extracted_text}")
        
        return " | ".join(parts)
    
    async def retrieve_images(
        self,
        query: str,
        query_image: str = None,
        top_k: int = 10
    ) -> List[Dict]:
        """
        Retrieve relevant images.
        """
        # Text query
        if query:
            results = await self.vector_store.search(
                query=query,
                k=top_k
            )
        
        # Image query
        elif query_image:
            processed = await self.image_processor.process_image(query_image)
            results = await self.vector_store.search_by_embedding(
                embedding=processed["image_embedding"],
                k=top_k
            )
        
        else:
            return []
        
        # Enrich results with metadata
        enriched = []
        for result in results:
            img_id = result["id"]
            metadata = self.image_index.get(img_id, {})
            
            enriched.append({
                **result,
                **metadata
            })
        
        return enriched
    
    async def answer_visual_question(
        self,
        query: str,
        retrieved_images: List[Dict],
        llm_client
    ) -> str:
        """
        Answer question about retrieved images.
        """
        prompt = f"""
Answer the following question based on the provided images.

Question: {query}

Images:"""
        
        for i, img in enumerate(retrieved_images[:3], 1):
            prompt += f"""

Image {i}:
- Description: {img.get('description', 'No description')}
- Caption: {img.get('caption', 'No caption')}
- Extracted Text: {img.get('extracted_text', 'No text')}
"""
        
        prompt += """

Answer:"""
        
        response = await llm_client.complete(prompt)
        return response
```

## Table RAG

### 1. Table Extraction và Processing

```python
import pandas as pd
from typing import List, Dict, Any

class TableProcessor:
    """
    Process tables for RAG.
    """
    
    def __init__(self):
        pass
    
    def extract_tables_from_document(
        self,
        document: Any
    ) -> List[pd.DataFrame]:
        """
        Extract tables from various document formats.
        """
        # Support PDF, HTML, Excel, etc.
        pass
    
    def process_table(
        self,
        table: pd.DataFrame,
        include_context: bool = True
    ) -> Dict:
        """
        Process table for embedding.
        """
        # Generate summary
        summary = self._generate_table_summary(table)
        
        # Generate column descriptions
        column_descriptions = self._describe_columns(table)
        
        # Generate row descriptions
        row_descriptions = self._describe_rows(table)
        
        # Create structured representation
        structured = self._create_structured_representation(table)
        
        return {
            "summary": summary,
            "column_descriptions": column_descriptions,
            "row_descriptions": row_descriptions,
            "structured": structured,
            "metadata": {
                "rows": len(table),
                "columns": len(table.columns),
                "column_names": list(table.columns)
            }
        }
    
    def _generate_table_summary(self, table: pd.DataFrame) -> str:
        """Generate natural language summary of table."""
        summary = f"This table has {len(table)} rows and {len(table.columns)} columns. "
        summary += f"Columns: {', '.join(str(c) for c in table.columns)}. "
        
        # Add sample data
        if len(table) > 0:
            summary += f"First row contains: {', '.join(str(v) for v in table.iloc[0])}. "
        
        return summary
    
    def _describe_columns(self, table: pd.DataFrame) -> List[str]:
        """Generate description for each column."""
        descriptions = []
        
        for col in table.columns:
            desc = f"Column '{col}'"
            
            # Data type
            dtype = table[col].dtype
            desc += f" contains {dtype} values"
            
            # Statistics
            if pd.api.types.is_numeric_dtype(table[col]):
                desc += f" (min: {table[col].min()}, max: {table[col].max()})"
            
            descriptions.append(desc)
        
        return descriptions
    
    def _describe_rows(self, table: pd.DataFrame, sample_size: int = 5) -> List[str]:
        """Generate description for rows."""
        descriptions = []
        
        for i, row in table.head(sample_size).iterrows():
            desc = f"Row {i}: " + ", ".join(f"{col}={val}" for col, val in row.items())
            descriptions.append(desc)
        
        if len(table) > sample_size:
            descriptions.append(f"... and {len(table) - sample_size} more rows")
        
        return descriptions
    
    def _create_structured_representation(
        self,
        table: pd.DataFrame
    ) -> str:
        """Create markdown representation of table."""
        lines = []
        
        # Header
        lines.append("| " + " | ".join(str(c) for c in table.columns) + " |")
        lines.append("| " + " | ".join(["---"] * len(table.columns)) + " |")
        
        # Rows
        for _, row in table.iterrows():
            lines.append("| " + " | ".join(str(v) for v in row.values) + " |")
        
        return "\n".join(lines)
```

### 2. Table Retrieval System

```python
class TableRAG:
    """
    RAG system for tables.
    """
    
    def __init__(
        self,
        vector_store,
        table_processor: TableProcessor,
        embedding_model
    ):
        self.vector_store = vector_store
        self.table_processor = table_processor
        self.embedding_model = embedding_model
        self.table_index = {}
    
    async def index_tables(
        self,
        tables: List[Dict]
    ):
        """
        Index tables with their embeddings and metadata.
        
        tables: List of {
            "id": str,
            "data": pd.DataFrame or List[List],
            "title": str,
            "context": str
        }
        """
        for table_data in tables:
            # Process table
            if isinstance(table_data["data"], pd.DataFrame):
                df = table_data["data"]
            else:
                df = pd.DataFrame(table_data["data"][1:], columns=table_data["data"][0])
            
            processed = self.table_processor.process_table(df)
            
            # Create text for embedding
            text_representation = self._create_text_representation(
                table_data.get("title", ""),
                processed,
                table_data.get("context", "")
            )
            
            # Generate embedding
            embedding = await self.embedding_model.embed_text(text_representation)
            
            # Store metadata
            self.table_index[table_data["id"]] = {
                "id": table_data["id"],
                "title": table_data.get("title", ""),
                "processed": processed,
                "data": df,
                "embedding": embedding
            }
            
            # Index for retrieval
            self.vector_store.index(
                ids=[table_data["id"]],
                texts=[text_representation],
                embeddings=[embedding]
            )
    
    def _create_text_representation(
        self,
        title: str,
        processed: Dict,
        context: str
    ) -> str:
        """Create text representation of table."""
        parts = []
        
        if title:
            parts.append(f"Table: {title}")
        
        if context:
            parts.append(f"Context: {context}")
        
        parts.append(f"Summary: {processed['summary']}")
        
        parts.append("Columns:")
        for col_desc in processed["column_descriptions"]:
            parts.append(f"  - {col_desc}")
        
        parts.append("\nSample rows:")
        for row_desc in processed["row_descriptions"]:
            parts.append(f"  - {row_desc}")
        
        return "\n".join(parts)
    
    async def retrieve_tables(
        self,
        query: str,
        top_k: int = 5
    ) -> List[Dict]:
        """
        Retrieve relevant tables.
        """
        results = await self.vector_store.search(
            query=query,
            k=top_k
        )
        
        # Enrich results
        enriched = []
        for result in results:
            table_id = result["id"]
            metadata = self.table_index.get(table_id, {})
            
            enriched.append({
                **result,
                "title": metadata.get("title", ""),
                "processed": metadata.get("processed", {}),
                "data": metadata.get("data"),
                "metadata": metadata.get("processed", {}).get("metadata", {})
            })
        
        return enriched
    
    async def answer_table_question(
        self,
        query: str,
        retrieved_tables: List[Dict],
        llm_client
    ) -> str:
        """
        Answer question about retrieved tables.
        """
        prompt = f"""
Answer the following question based on the provided tables.

Question: {query}

Tables:"""
        
        for i, table in enumerate(retrieved_tables[:2], 1):
            prompt += f"""

Table {i}: {table.get('title', 'Untitled')}
{processed.get('structured', '')}
"""
        
        prompt += """

Provide a direct answer to the question. If the information is not in the tables, say so.
Answer:"""
        
        response = await llm_client.complete(prompt)
        return response
```

## PDF Layout-aware Chunking

### 1. PDF Processing Pipeline

```python
from typing import List, Dict, Optional
import pdfplumber
from PIL import Image
import io

class PDFProcessor:
    """
    Process PDFs with layout awareness.
    """
    
    def __init__(
        self,
        ocr_model=None,
        table_processor: TableProcessor = None
    ):
        self.ocr = ocr_model
        self.table_processor = table_processor or TableProcessor()
    
    def process_pdf(
        self,
        pdf_path: str,
        extract_tables: bool = True,
        extract_images: bool = True,
        extract_layout: bool = True
    ) -> Dict:
        """
        Process PDF and extract structured content.
        """
        content = {
            "pages": [],
            "images": [],
            "tables": [],
            "structure": {}
        }
        
        with pdfplumber.open(pdf_path) as pdf:
            for page_num, page in enumerate(pdf.pages):
                page_content = {
                    "page_number": page_num + 1,
                    "text": "",
                    "blocks": [],
                    "tables": [],
                    "images": []
                }
                
                # Extract text with layout
                if extract_layout:
                    blocks = page.extract_words()
                    page_content["blocks"] = blocks
                    
                    # Group into paragraphs
                    paragraphs = self._group_into_paragraphs(blocks)
                    page_content["text"] = "\n\n".join(paragraphs)
                else:
                    page_content["text"] = page.extract_text()
                
                # Extract tables
                if extract_tables:
                    tables = page.extract_tables()
                    page_content["tables"] = tables
                    
                    for table in tables:
                        content["tables"].append({
                            "data": table,
                            "page": page_num + 1,
                            "source": pdf_path
                        })
                
                # Extract images
                if extract_images:
                    images = self._extract_images_from_page(page)
                    page_content["images"] = images
                    content["images"].extend(images)
                
                content["pages"].append(page_content)
        
        return content
    
    def _group_into_paragraphs(
        self,
        blocks: List[Dict]
    ) -> List[str]:
        """
        Group text blocks into paragraphs based on layout.
        """
        if not blocks:
            return []
        
        paragraphs = []
        current_para = []
        last_y = None
        last_x = None
        
        # Sort blocks by position (top to bottom, left to right)
        sorted_blocks = sorted(
            blocks,
            key=lambda b: (round(-b["top"] / 20) * 20, b["x0"])
        )
        
        for block in sorted_blocks:
            # Check if this block continues current paragraph
            is_same_paragraph = (
                last_y is not None and
                abs(block["top"] - last_y) < 20 and
                block["x0"] - last_x < 100  # Same line or close
            )
            
            if is_same_paragraph:
                current_para.append(block["text"])
            else:
                # Save current paragraph
                if current_para:
                    paragraphs.append(" ".join(current_para))
                current_para = [block["text"]]
            
            last_y = block["top"]
            last_x = block["x1"]
        
        # Add last paragraph
        if current_para:
            paragraphs.append(" ".join(current_para))
        
        return paragraphs
    
    def _extract_images_from_page(self, page) -> List[Dict]:
        """Extract images from PDF page."""
        images = []
        
        for img_info in page.images:
            images.append({
                "x0": img_info.get("x0"),
                "top": img_info.get("top"),
                "width": img_info.get("width"),
                "height": img_info.get("height"),
                "page": page.page_number,
                "image_index": len(images)
            })
        
        return images
```

### 2. Layout-aware Chunker

```python
class LayoutAwareChunker:
    """
    Chunk documents respecting layout structure.
    """
    
    def __init__(
        self,
        max_chunk_size: int = 500,
        overlap: int = 50
    ):
        self.max_chunk_size = max_chunk_size
        self.overlap = overlap
    
    def chunk_page(
        self,
        page_content: Dict,
        page_number: int
    ) -> List[Dict]:
        """
        Chunk a single page with layout awareness.
        """
        chunks = []
        
        # Chunk text paragraphs
        text_chunks = self._chunk_text(
            page_content.get("text", ""),
            page_number
        )
        chunks.extend(text_chunks)
        
        # Chunk tables
        for table_idx, table_data in enumerate(page_content.get("tables", [])):
            table_chunk = self._create_table_chunk(
                table_data,
                table_idx,
                page_number
            )
            chunks.append(table_chunk)
        
        # Handle images
        for img_info in page_content.get("images", []):
            img_chunk = self._create_image_chunk(
                img_info,
                page_number
            )
            chunks.append(img_chunk)
        
        return chunks
    
    def _chunk_text(
        self,
        text: str,
        page_number: int
    ) -> List[Dict]:
        """Chunk text while respecting paragraph boundaries."""
        paragraphs = text.split("\n\n")
        chunks = []
        current_chunk = []
        current_size = 0
        
        for para in paragraphs:
            para_size = len(para)
            
            if current_size + para_size > self.max_chunk_size and current_chunk:
                # Create chunk
                chunks.append({
                    "type": "text",
                    "content": "\n\n".join(current_chunk),
                    "page": page_number,
                    "chunk_index": len(chunks)
                })
                
                # Start new chunk with overlap
                overlap_size = sum(len(p) for p in current_chunk[-1:])
                current_chunk = current_chunk[-1:] if current_chunk else []
                current_size = overlap_size
            
            current_chunk.append(para)
            current_size += para_size
        
        # Add remaining content
        if current_chunk:
            chunks.append({
                "type": "text",
                "content": "\n\n".join(current_chunk),
                "page": page_number,
                "chunk_index": len(chunks)
            })
        
        return chunks
    
    def _create_table_chunk(
        self,
        table_data: List[List],
        table_idx: int,
        page_number: int
    ) -> Dict:
        """Create chunk for table."""
        # Convert to markdown
        lines = []
        for row in table_data:
            lines.append("| " + " | ".join(str(c) for c in row) + " |")
        
        markdown = "\n".join(lines)
        
        return {
            "type": "table",
            "content": markdown,
            "data": table_data,
            "page": page_number,
            "table_index": table_idx
        }
    
    def _create_image_chunk(
        self,
        img_info: Dict,
        page_number: int
    ) -> Dict:
        """Create chunk for image reference."""
        return {
            "type": "image",
            "content": f"[Image on page {page_number}]",
            "page": page_number,
            "image_index": img_info.get("image_index"),
            "position": {
                "x": img_info.get("x0"),
                "y": img_info.get("top"),
                "width": img_info.get("width"),
                "height": img_info.get("height")
            }
        }
    
    def chunk_document(
        self,
        document_content: Dict
    ) -> List[Dict]:
        """
        Chunk entire document.
        """
        all_chunks = []
        doc_id = document_content.get("id", "unknown")
        
        for page in document_content.get("pages", []):
            page_chunks = self.chunk_page(page, page["page_number"])
            
            for chunk in page_chunks:
                chunk["document_id"] = doc_id
                all_chunks.append(chunk)
        
        # Assign global chunk IDs
        for i, chunk in enumerate(all_chunks):
            chunk["id"] = f"{doc_id}_chunk_{i}"
        
        return all_chunks
```

## Multi-modal RAG System

### 1. Unified Multi-modal Index

```python
class MultiModalIndex:
    """
    Unified index for multi-modal content.
    """
    
    def __init__(
        self,
        vector_store,
        text_embedder,
        image_embedder,
        table_embedder
    ):
        self.vector_store = vector_store
        self.text_embedder = text_embedder
        self.image_embedder = image_embedder
        self.table_embedder = table_embedder
        
        self.content_index = {}  # id -> content metadata
    
    async def index_document(
        self,
        doc_id: str,
        content: Dict
    ):
        """
        Index document with all modalities.
        
        content: {
            "text": str,
            "images": List[Dict],
            "tables": List[Dict],
            "metadata": Dict
        }
        """
        # Index text chunks
        if content.get("text_chunks"):
            await self._index_text(doc_id, content["text_chunks"])
        
        # Index images
        if content.get("images"):
            await self._index_images(doc_id, content["images"])
        
        # Index tables
        if content.get("tables"):
            await self._index_tables(doc_id, content["tables"])
    
    async def _index_text(
        self,
        doc_id: str,
        chunks: List[Dict]
    ):
        """Index text chunks."""
        for chunk in chunks:
            chunk_id = f"{doc_id}_text_{chunk['chunk_index']}"
            
            embedding = await self.text_embedder.embed_text(chunk["content"])
            
            self.content_index[chunk_id] = {
                "id": chunk_id,
                "doc_id": doc_id,
                "type": "text",
                "content": chunk["content"],
                "page": chunk.get("page"),
                "metadata": chunk.get("metadata", {})
            }
            
            self.vector_store.index(
                ids=[chunk_id],
                texts=[chunk["content"]],
                embeddings=[embedding]
            )
    
    async def _index_images(
        self,
        doc_id: str,
        images: List[Dict]
    ):
        """Index images."""
        for img in images:
            img_id = f"{doc_id}_image_{img['index']}"
            
            embedding = await self.image_embedder.embed_image(img["source"])
            
            self.content_index[img_id] = {
                "id": img_id,
                "doc_id": doc_id,
                "type": "image",
                "content": img.get("caption", ""),
                "description": img.get("description", ""),
                "extracted_text": img.get("extracted_text", ""),
                "page": img.get("page"),
                "metadata": img.get("metadata", {})
            }
            
            self.vector_store.index(
                ids=[img_id],
                texts=[img.get("caption", "") + " " + img.get("description", "")],
                embeddings=[embedding]
            )
    
    async def _index_tables(
        self,
        doc_id: str,
        tables: List[Dict]
    ):
        """Index tables."""
        for table in tables:
            table_id = f"{doc_id}_table_{table['index']}"
            
            embedding = await self.table_embedder.embed_table(
                table["data"],
                table.get("title", "")
            )
            
            self.content_index[table_id] = {
                "id": table_id,
                "doc_id": doc_id,
                "type": "table",
                "content": table.get("title", ""),
                "data": table["data"],
                "page": table.get("page"),
                "metadata": table.get("metadata", {})
            }
            
            text_repr = self._create_table_text(table)
            self.vector_store.index(
                ids=[table_id],
                texts=[text_repr],
                embeddings=[embedding]
            )
    
    def _create_table_text(self, table: Dict) -> str:
        """Create text representation of table."""
        parts = []
        
        if table.get("title"):
            parts.append(f"Table: {table['title']}")
        
        parts.append(f"Rows: {len(table['data'])}, Columns: {len(table['data'][0]) if table['data'] else 0}")
        
        return "\n".join(parts)
```

### 2. Multi-modal Query Router

```python
class MultiModalQueryRouter:
    """
    Route queries to appropriate modalities.
    """
    
    def __init__(self, llm_client):
        self.llm = llm_client
    
    async def route(
        self,
        query: str
    ) -> Dict[str, float]:
        """
        Determine which modalities to query.
        
        Returns:
            Dict of modality -> weight (0-1)
        """
        prompt = f"""
Analyze this query and determine which types of content are most relevant.
Respond with a JSON object indicating the relevance of each modality.

Query: {query}

Modalities:
- text: General textual information
- image: Visual information, diagrams, figures
- table: Structured data, statistics, comparisons

Return JSON like:
{{"text": 0.8, "image": 0.1, "table": 0.1}}

Response:"""
        
        response = await self.llm.complete(prompt)
        
        # Parse JSON response
        import json
        import re
        
        json_match = re.search(r'\{[^}]+\}', response)
        if json_match:
            return json.loads(json_match.group())
        
        # Default to text-heavy
        return {"text": 0.8, "image": 0.1, "table": 0.1}
```

### 3. Complete Multi-modal RAG

```python
class MultiModalRAG:
    """
    Complete multi-modal RAG system.
    """
    
    def __init__(
        self,
        index: MultiModalIndex,
        router: MultiModalQueryRouter,
        text_retriever,
        image_retriever,
        table_retriever,
        llm_client
    ):
        self.index = index
        self.router = router
        self.text_retriever = text_retriever
        self.image_retriever = image_retriever
        self.table_retriever = table_retriever
        self.llm = llm_client
    
    async def query(
        self,
        query: str,
        top_k: int = 10,
        modality_weights: Dict[str, float] = None
    ) -> Dict:
        """
        Query multi-modal RAG system.
        """
        # Step 1: Route query
        if modality_weights is None:
            modality_weights = await self.router.route(query)
        
        # Step 2: Retrieve from each modality
        results = {}
        
        k_per_modality = {
            modality: max(1, int(top_k * weight))
            for modality, weight in modality_weights.items()
        }
        
        if modality_weights.get("text", 0) > 0:
            results["text"] = await self.text_retriever.retrieve(
                query, k=k_per_modality["text"]
            )
        
        if modality_weights.get("image", 0) > 0:
            results["image"] = await self.image_retriever.retrieve_images(
                query, k=k_per_modality["image"]
            )
        
        if modality_weights.get("table", 0) > 0:
            results["table"] = await self.table_retriever.retrieve_tables(
                query, k=k_per_modality["table"]
            )
        
        # Step 3: Generate answer
        answer = await self._generate_answer(query, results)
        
        return {
            "query": query,
            "answer": answer,
            "text_results": results.get("text", []),
            "image_results": results.get("image", []),
            "table_results": results.get("table", []),
            "modality_weights": modality_weights
        }
    
    async def _generate_answer(
        self,
        query: str,
        results: Dict
    ) -> str:
        """Generate answer from multi-modal results."""
        prompt = f"""
Answer the following question using the provided context from multiple modalities.

Question: {query}

Context:"""
        
        # Add text context
        if results.get("text"):
            prompt += "\n\n## Text Content:\n"
            for i, res in enumerate(results["text"][:5], 1):
                prompt += f"\n{i}. {res.get('content', '')[:500]}"
        
        # Add image context
        if results.get("image"):
            prompt += "\n\n## Images:\n"
            for i, img in enumerate(results["image"][:3], 1):
                prompt += f"\n{i}. {img.get('description', img.get('caption', 'No description'))}"
        
        # Add table context
        if results.get("table"):
            prompt += "\n\n## Tables:\n"
            for i, table in enumerate(results["table"][:2], 1):
                prompt += f"\n{i}. {table.get('content', table.get('title', 'Untitled'))}"
        
        prompt += "\n\nAnswer:"
        
        return await self.llm.complete(prompt)
```

## Best Practices

### 1. Choosing Embedding Models

```python
EMBEDDING_MODEL_GUIDE = {
    "text": {
        "high_quality": ["text-embedding-3-large", "embed-english-v3.0"],
        "balanced": ["text-embedding-3-small", "all-mpnet-base-v2"],
        "fast": ["all-MiniLM-L6-v2"]
    },
    "image": {
        "high_quality": ["clip-vit-large-patch14", "SigLIP"],
        "balanced": ["clip-vit-base-patch32"],
        "fast": ["mobileclip"]
    },
    "table": {
        "recommended": ["table-transformer", "tapex"],
        "fallback": "text-embedding with flattened table"
    }
}
```

### 2. Handling Modalities in Context

```python
def format_multi_modal_context(
    text_results: List[Dict],
    image_results: List[Dict],
    table_results: List[Dict],
    max_tokens: int = 4000
) -> str:
    """
    Format multi-modal results into context string.
    """
    context_parts = []
    current_tokens = 0
    
    # Add text first (usually most relevant)
    for result in text_results:
        text = result.get("content", "")
        token_count = len(text.split()) * 1.3  # Rough estimate
        
        if current_tokens + token_count > max_tokens:
            break
        
        context_parts.append(f"[Text] {text}")
        current_tokens += token_count
    
    # Add tables
    for result in table_results:
        table_text = result.get("content", "")
        token_count = len(table_text.split()) * 1.3
        
        if current_tokens + token_count > max_tokens:
            break
        
        context_parts.append(f"[Table] {table_text}")
        current_tokens += token_count
    
    # Add images (least token-intensive)
    for result in image_results:
        desc = result.get("description", result.get("caption", ""))
        token_count = len(desc.split()) * 1.3
        
        if current_tokens + token_count > max_tokens:
            break
        
        context_parts.append(f"[Image] {desc}")
        current_tokens += token_count
    
    return "\n\n".join(context_parts)
```

## Examples

### Example 1: Complete PDF Processing Pipeline

```python
class CompletePDFProcessor:
    """
    Complete pipeline for processing PDFs.
    """
    
    def __init__(
        self,
        config: dict
    ):
        # Initialize components
        self.pdf_processor = PDFProcessor()
        self.chunker = LayoutAwareChunker()
        self.multi_modal_rag = MultiModalRAG(...)
    
    async def process_pdf(
        self,
        pdf_path: str,
        doc_id: str = None
    ) -> Dict:
        """
        Process PDF end-to-end.
        """
        import os
        
        doc_id = doc_id or os.path.splitext(os.path.basename(pdf_path))[0]
        
        # Step 1: Extract content from PDF
        print(f"Processing PDF: {pdf_path}")
        content = self.pdf_processor.process_pdf(pdf_path)
        
        # Step 2: Chunk content
        print("Chunking content...")
        chunks = self.chunker.chunk_document({
            "id": doc_id,
            "pages": content["pages"]
        })
        
        # Step 3: Index chunks
        print("Indexing chunks...")
        await self.multi_modal_rag.index.index_document(
            doc_id=doc_id,
            content={
                "text_chunks": [c for c in chunks if c["type"] == "text"],
                "images": content["images"],
                "tables": content["tables"]
            }
        )
        
        return {
            "doc_id": doc_id,
            "num_pages": len(content["pages"]),
            "num_chunks": len(chunks),
            "num_images": len(content["images"]),
            "num_tables": len(content["tables"])
        }
```

### Example 2: Query Interface

```python
class MultiModalQueryInterface:
    """
    User interface for multi-modal queries.
    """
    
    def __init__(self, rag_system: MultiModalRAG):
        self.rag = rag_system
    
    async def ask(
        self,
        question: str,
        include_images: bool = True,
        include_tables: bool = True
    ) -> Dict:
        """
        Ask a question and get multi-modal answer.
        """
        # Set modality weights
        weights = {"text": 0.6}
        if include_images:
            weights["image"] = 0.25
        if include_tables:
            weights["table"] = 0.15
        
        # Normalize weights
        total = sum(weights.values())
        weights = {k: v / total for k, v in weights.items()}
        
        # Query
        result = await self.rag.query(
            query=question,
            top_k=10,
            modality_weights=weights
        )
        
        return {
            "answer": result["answer"],
            "sources": {
                "text_count": len(result.get("text_results", [])),
                "image_count": len(result.get("image_results", [])),
                "table_count": len(result.get("table_results", []))
            },
            "text_sources": [
                {"page": s.get("page"), "preview": s.get("content", "")[:200]}
                for s in result.get("text_results", [])[:3]
            ],
            "image_sources": [
                {"page": s.get("page"), "description": s.get("description", "")}
                for s in result.get("image_results", [])[:2]
            ],
            "table_sources": [
                {"page": s.get("page"), "title": s.get("title", "")}
                for s in result.get("table_results", [])[:2]
            ]
        }
```

## References

1. **CLIP**: https://openai.com/research/clip
2. **GPT-4V**: https://openai.com/research/gpt-4v
3. **LayoutLM**: https://arxiv.org/abs/1912.13318
4. **Table Transformer**: https://arxiv.org/abs/2110.00061
5. **Cursor Enterprise Framework - RAG Rules**: `.cursor/rules/rag.mdc`
