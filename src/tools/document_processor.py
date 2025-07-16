"""
Document processing tools for handling various document formats
"""
import os
import io
from typing import Dict, Any, List, Optional, Tuple
from PIL import Image, ImageEnhance, ImageOps
import PyPDF2
import base64
from src.config import Config

class DocumentProcessor:
    """
    Handles document processing including format conversion, OCR, and quality enhancement
    """
    
    def __init__(self):
        self.supported_formats = Config.SUPPORTED_FORMATS
        self.max_pages = Config.MAX_PAGES
    
    def process_document(self, file_path: str) -> Dict[str, Any]:
        """
        Main document processing function
        
        Args:
            file_path: Path to the document file
            
        Returns:
            Processing result with extracted text and metadata
        """
        try:
            file_extension = os.path.splitext(file_path)[1].lower().lstrip('.')
            
            if file_extension not in self.supported_formats:
                return {
                    'success': False,
                    'error': f'Unsupported file format: {file_extension}',
                    'text': '',
                    'metadata': {}
                }
            
            if file_extension == 'pdf':
                return self._process_pdf(file_path)
            else:
                return self._process_image(file_path)
                
        except Exception as e:
            return {
                'success': False,
                'error': f'Document processing failed: {str(e)}',
                'text': '',
                'metadata': {}
            }
    
    def _process_pdf(self, file_path: str) -> Dict[str, Any]:
        """
        Process PDF documents
        
        Args:
            file_path: Path to PDF file
            
        Returns:
            Extracted text and metadata
        """
        try:
            with open(file_path, 'rb') as file:
                pdf_reader = PyPDF2.PdfReader(file)
                
                # Check page count
                num_pages = len(pdf_reader.pages)
                if num_pages > self.max_pages:
                    return {
                        'success': False,
                        'error': f'Document has {num_pages} pages, maximum allowed is {self.max_pages}',
                        'text': '',
                        'metadata': {}
                    }
                
                # Extract text from all pages
                text_content = []
                for page_num, page in enumerate(pdf_reader.pages):
                    try:
                        page_text = page.extract_text()
                        if page_text.strip():
                            text_content.append(f"--- Page {page_num + 1} ---\\n{page_text}")
                    except Exception as e:
                        text_content.append(f"--- Page {page_num + 1} ---\\n[Error extracting text: {str(e)}]")
                
                full_text = "\\n\\n".join(text_content)
                
                # Extract metadata
                metadata = {
                    'num_pages': num_pages,
                    'file_size': os.path.getsize(file_path),
                    'format': 'pdf',
                    'has_text': len(full_text.strip()) > 0
                }
                
                # Add PDF metadata if available
                if pdf_reader.metadata:
                    metadata.update({
                        'title': pdf_reader.metadata.get('/Title', ''),
                        'author': pdf_reader.metadata.get('/Author', ''),
                        'creator': pdf_reader.metadata.get('/Creator', ''),
                        'creation_date': str(pdf_reader.metadata.get('/CreationDate', ''))
                    })
                
                return {
                    'success': True,
                    'text': full_text,
                    'metadata': metadata,
                    'error': None
                }
                
        except Exception as e:
            return {
                'success': False,
                'error': f'PDF processing failed: {str(e)}',
                'text': '',
                'metadata': {}
            }
    
    def _process_image(self, file_path: str) -> Dict[str, Any]:
        """
        Process image documents (PNG, JPG, TIFF)
        
        Args:
            file_path: Path to image file
            
        Returns:
            Enhanced image data and metadata
        """
        try:
            with Image.open(file_path) as image:
                # Enhance image quality
                enhanced_image = self._enhance_image_quality(image)
                
                # Convert to base64 for potential OCR processing
                img_buffer = io.BytesIO()
                enhanced_image.save(img_buffer, format='PNG')
                img_base64 = base64.b64encode(img_buffer.getvalue()).decode()
                
                # Extract metadata
                metadata = {
                    'format': image.format.lower() if image.format else 'unknown',
                    'size': image.size,
                    'mode': image.mode,
                    'file_size': os.path.getsize(file_path),
                    'enhanced': True
                }
                
                # Note: For actual OCR, you would integrate with services like Amazon Textract
                # For now, we'll return a placeholder indicating OCR is needed
                return {
                    'success': True,
                    'text': '[OCR_REQUIRED] This is an image document that requires OCR processing.',
                    'image_data': img_base64,
                    'metadata': metadata,
                    'error': None
                }
                
        except Exception as e:
            return {
                'success': False,
                'error': f'Image processing failed: {str(e)}',
                'text': '',
                'metadata': {}
            }
    
    def _enhance_image_quality(self, image: Image.Image) -> Image.Image:
        """
        Enhance image quality for better OCR results
        
        Args:
            image: PIL Image object
            
        Returns:
            Enhanced image
        """
        try:
            # Convert to RGB if necessary
            if image.mode != 'RGB':
                image = image.convert('RGB')
            
            # Auto-orient the image
            image = ImageOps.exif_transpose(image)
            
            # Enhance contrast
            enhancer = ImageEnhance.Contrast(image)
            image = enhancer.enhance(1.2)
            
            # Enhance sharpness
            enhancer = ImageEnhance.Sharpness(image)
            image = enhancer.enhance(1.1)
            
            # Resize if too large (maintain aspect ratio)
            max_dimension = 3000
            if max(image.size) > max_dimension:
                ratio = max_dimension / max(image.size)
                new_size = tuple(int(dim * ratio) for dim in image.size)
                image = image.resize(new_size, Image.Resampling.LANCZOS)
            
            return image
            
        except Exception as e:
            # If enhancement fails, return original image
            print(f"Image enhancement failed: {str(e)}")
            return image
    
    def validate_document(self, file_path: str) -> Dict[str, Any]:
        """
        Validate document before processing
        
        Args:
            file_path: Path to document file
            
        Returns:
            Validation result
        """
        try:
            if not os.path.exists(file_path):
                return {
                    'valid': False,
                    'error': 'File does not exist'
                }
            
            file_size = os.path.getsize(file_path)
            max_size = 50 * 1024 * 1024  # 50MB in bytes
            
            if file_size > max_size:
                return {
                    'valid': False,
                    'error': f'File size ({file_size / 1024 / 1024:.1f}MB) exceeds maximum allowed size (50MB)'
                }
            
            file_extension = os.path.splitext(file_path)[1].lower().lstrip('.')
            if file_extension not in self.supported_formats:
                return {
                    'valid': False,
                    'error': f'Unsupported file format: {file_extension}'
                }
            
            return {
                'valid': True,
                'file_size': file_size,
                'format': file_extension
            }
            
        except Exception as e:
            return {
                'valid': False,
                'error': f'Validation failed: {str(e)}'
            }
