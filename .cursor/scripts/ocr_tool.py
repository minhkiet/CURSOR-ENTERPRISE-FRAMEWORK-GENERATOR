#!/usr/bin/env python3
"""
OCR Utility Script for Document Scanner Integration
Part of Cursor Enterprise Framework

Usage:
    python ocr_tool.py <image_path> [options]
    
Examples:
    python ocr_tool.py document.png
    python ocr_tool.py hoadon.png -l vie -o text.txt
    python ocr_tool.py screenshot.png --json
"""

import argparse
import sys
import json
from pathlib import Path
from typing import Optional, Dict, Any, List
from dataclasses import dataclass, asdict

try:
    from PIL import Image, ImageFilter, ImageEnhance, ImageOps
except ImportError:
    print("Error: Pillow not installed. Run: pip install pillow")
    sys.exit(1)

try:
    import pytesseract
except ImportError:
    print("Error: pytesseract not installed. Run: pip install pytesseract")
    sys.exit(1)

try:
    import numpy as np
    import cv2
    OPENCV_AVAILABLE = True
except ImportError:
    OPENCV_AVAILABLE = False
    np = None
    cv2 = None


@dataclass
class OCRResult:
    """OCR Result DataClass"""
    success: bool
    text: str
    confidence: float
    language: str
    image_path: str
    error: Optional[str] = None
    word_count: int = 0
    preprocessing_applied: bool = False


class DocumentPreprocessor:
    """Document image preprocessor for better OCR results"""
    
    @staticmethod
    def preprocess_pil(img: Image.Image, enhance: bool = True) -> Image.Image:
        """Preprocess using Pillow only"""
        # Convert to grayscale
        img = img.convert('L')
        
        if enhance:
            # Increase contrast
            enhancer = ImageEnhance.Contrast(img)
            img = enhancer.enhance(1.5)
            
            # Sharpen
            enhancer = ImageEnhance.Sharpness(img)
            img = enhancer.enhance(1.5)
            
            # Denoise
            img = img.filter(ImageFilter.MedianFilter(size=3))
            
            # Auto levels
            img = ImageOps.autocontrast(img)
        
        return img
    
    @staticmethod
    def preprocess_opencv(img: np.ndarray) -> Image.Image:
        """Preprocess using OpenCV for better results"""
        if not OPENCV_AVAILABLE:
            raise ImportError("OpenCV not available")
        
        # Convert to grayscale
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        
        # Denoise
        denoised = cv2.fastNlMeansDenoising(gray, None, 10, 7, 21)
        
        # Threshold (Otsu's method)
        _, binary = cv2.threshold(denoised, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
        
        # Morphological operations
        kernel = np.ones((1, 1), np.uint8)
        processed = cv2.morphologyEx(binary, cv2.MORPH_CLOSE, kernel)
        
        # Convert back to PIL Image
        return Image.fromarray(processed)
    
    @staticmethod
    def preprocess_vietnamese(img: Image.Image) -> Image.Image:
        """Special preprocessing for Vietnamese documents"""
        # Convert to grayscale
        img = img.convert('L')
        
        # Increase contrast more aggressively
        enhancer = ImageEnhance.Contrast(img)
        img = enhancer.enhance(1.7)
        
        # Increase brightness
        enhancer = ImageEnhance.Brightness(img)
        img = enhancer.enhance(1.15)
        
        # Sharpen
        enhancer = ImageEnhance.Sharpness(img)
        img = enhancer.enhance(2.0)
        
        # Denoise multiple times
        for _ in range(2):
            img = img.filter(ImageFilter.MedianFilter(size=3))
        
        # Auto levels
        img = ImageOps.autocontrast(img, cutoff=2)
        
        return img


class OCREngine:
    """OCR Engine wrapper for Tesseract"""
    
    def __init__(self, language: str = 'vie+eng'):
        self.language = language
        self.psm_modes = {
            'auto': 3,
            'block': 4,
            'line': 7,
            'word': 8,
            'sparse': 11,
            'osd': 3,
        }
    
    def extract_text(
        self,
        image_path: str,
        lang: Optional[str] = None,
        psm: str = 'auto',
        preprocess: bool = True,
        preprocessor: str = 'pillow'
    ) -> OCRResult:
        """Extract text from image"""
        try:
            # Load image
            if preprocessor == 'opencv' and OPENCV_AVAILABLE:
                img_cv = cv2.imread(image_path)
                if img_cv is None:
                    return OCRResult(
                        success=False,
                        text="",
                        confidence=0,
                        language=lang or self.language,
                        image_path=image_path,
                        error="Could not read image"
                    )
                img_pil = DocumentPreprocessor.preprocess_opencv(img_cv)
            else:
                img_pil = Image.open(image_path)
                
                if preprocess:
                    if 'vie' in (lang or self.language).lower():
                        img_pil = DocumentPreprocessor.preprocess_vietnamese(img_pil)
                    else:
                        img_pil = DocumentPreprocessor.preprocess_pil(img_pil)
            
            # Get PSM mode
            page_seg_mode = self.psm_modes.get(psm, 3)
            
            # Custom config
            custom_config = f'--psm {page_seg_mode}'
            
            # OCR
            lang_used = lang or self.language
            text = pytesseract.image_to_string(
                img_pil,
                lang=lang_used,
                config=custom_config
            )
            
            # Get confidence (approximate)
            data = pytesseract.image_to_data(
                img_pil,
                lang=lang_used,
                config=custom_config,
                output_type=pytesseract.Output.DICT
            )
            
            confidences = [int(c) for c in data['conf'] if c != '-1']
            avg_confidence = sum(confidences) / len(confidences) if confidences else 0
            
            # Clean text
            text = text.strip()
            word_count = len(text.split())
            
            return OCRResult(
                success=True,
                text=text,
                confidence=avg_confidence,
                language=lang_used,
                image_path=image_path,
                word_count=word_count,
                preprocessing_applied=preprocess
            )
            
        except FileNotFoundError:
            return OCRResult(
                success=False,
                text="",
                confidence=0,
                language=lang or self.language,
                image_path=image_path,
                error=f"File not found: {image_path}"
            )
        except Exception as e:
            return OCRResult(
                success=False,
                text="",
                confidence=0,
                language=lang or self.language,
                image_path=image_path,
                error=str(e)
            )


def extract_text_from_document(
    image_path: str,
    lang: str = 'vie+eng',
    preprocess: bool = True,
    output: Optional[str] = None,
    json_output: bool = False,
    psm: str = 'auto',
    preprocessor: str = 'pillow'
) -> OCRResult:
    """Main extraction function"""
    engine = OCREngine(language=lang)
    result = engine.extract_text(
        image_path,
        lang=lang,
        psm=psm,
        preprocess=preprocess,
        preprocessor=preprocessor
    )
    
    if result.success and output:
        Path(output).write_text(result.text, encoding='utf-8')
    
    return result


def main():
    parser = argparse.ArgumentParser(
        description='OCR Text Extraction Tool for Cursor Enterprise Framework',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s document.png
  %(prog)s hoadon.png -l vie -o text.txt
  %(prog)s screenshot.png --json
  %(prog)s receipt.png -l eng --preprocessor opencv

Supported Languages:
  vie    - Vietnamese
  eng    - English
  vie+eng - Vietnamese + English
  chi_sim - Simplified Chinese
  jpn    - Japanese
  kor    - Korean

PSM Modes (Page Segmentation):
  auto   - Automatic (default)
  block  - Uniform block of text
  line   - Single text line
  word   - Single word
  sparse - Sparse text (mixed content)
        """
    )
    
    parser.add_argument('image', help='Input image file (PNG, JPG, TIFF, BMP, WEBP)')
    parser.add_argument('-o', '--output', help='Output text file')
    parser.add_argument('-l', '--lang', default='vie+eng', 
                       help='Language code (default: vie+eng)')
    parser.add_argument('--no-preprocess', action='store_true', 
                       help='Skip image preprocessing')
    parser.add_argument('--json', action='store_true', 
                       help='Output as JSON')
    parser.add_argument('--psm', default='auto', choices=['auto', 'block', 'line', 'word', 'sparse'],
                       help='Page segmentation mode (default: auto)')
    parser.add_argument('--preprocessor', default='pillow', choices=['pillow', 'opencv'],
                       help='Preprocessor engine (default: pillow)')
    parser.add_argument('-v', '--verbose', action='store_true',
                       help='Verbose output')
    
    args = parser.parse_args()
    
    # Check file exists
    if not Path(args.image).exists():
        print(f"Error: File not found: {args.image}", file=sys.stderr)
        sys.exit(1)
    
    # Run OCR
    if args.verbose:
        print(f"Processing: {args.image}")
        print(f"Language: {args.lang}")
        print(f"Preprocessing: {'enabled' if not args.no_preprocess else 'disabled'}")
        print(f"PSM Mode: {args.psm}")
        print("-" * 50)
    
    result = extract_text_from_document(
        args.image,
        lang=args.lang,
        preprocess=not args.no_preprocess,
        output=args.output,
        json_output=args.json,
        psm=args.psm,
        preprocessor=args.preprocessor if not args.no_preprocess else 'pillow'
    )
    
    if result.success:
        if args.json:
            output = {
                'success': True,
                'text': result.text,
                'confidence': round(result.confidence, 2),
                'language': result.language,
                'word_count': result.word_count,
                'image_path': result.image_path,
                'preprocessing_applied': result.preprocessing_applied
            }
            print(json.dumps(output, ensure_ascii=False, indent=2))
        else:
            print(result.text)
        
        if args.output:
            print(f"\nText saved to: {args.output}", file=sys.stderr)
        
        if args.verbose:
            print("-" * 50)
            print(f"Confidence: {result.confidence:.1f}%")
            print(f"Word count: {result.word_count}")
    else:
        if args.json:
            print(json.dumps({
                'success': False,
                'error': result.error,
                'image_path': result.image_path
            }, indent=2))
        else:
            print(f"Error: {result.error}", file=sys.stderr)
        sys.exit(1)


if __name__ == '__main__':
    main()
