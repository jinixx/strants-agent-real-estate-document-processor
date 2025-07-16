"""
Strands Agent implementation for document processing
"""
from typing import Dict, Any, List, Optional
from src.models.bedrock_model import BedrockModel
from src.tools.document_processor import DocumentProcessor
from src.config import Config

class StrandsDocumentAgent:
    """
    Main Strands Agent for document processing workflow
    """
    
    def __init__(self, aws_profile: Optional[str] = None):
        """
        Initialize the document processing agent
        
        Args:
            aws_profile: AWS profile name for authentication
        """
        # Initialize components
        self.bedrock_model = BedrockModel(profile_name=aws_profile)
        self.processor = DocumentProcessor()
        self.name = "StrandsDocumentProcessor"
        self.description = "AI agent for processing real estate documents and extracting structured data"
    
    def process_document(self, file_path: str) -> Dict[str, Any]:
        """
        Process and extract text from real estate documents (PDF, images)
        
        Args:
            file_path: Path to the document file
            
        Returns:
            Processing result with extracted text and metadata
        """
        # Validate document first
        validation = self.processor.validate_document(file_path)
        if not validation['valid']:
            return {
                'success': False,
                'error': validation['error'],
                'text': '',
                'metadata': {}
            }
        
        # Process the document
        return self.processor.process_document(file_path)
    
    def classify_document(self, document_text: str) -> Dict[str, Any]:
        """
        Classify real estate document type (settlement, purchase agreement, income verification)
        
        Args:
            document_text: Text content of the document
            
        Returns:
            Classification result with document type and confidence
        """
        return self.bedrock_model.classify_document(document_text)
    
    def extract_data(self, document_text: str, document_type: str) -> Dict[str, Any]:
        """
        Extract structured data from real estate documents
        
        Args:
            document_text: Text content of the document
            document_type: Type of document to extract data for
            
        Returns:
            Extraction result with structured data
        """
        return self.bedrock_model.extract_document_data(document_text, document_type)

    
    def process_document_workflow(self, file_path: str) -> Dict[str, Any]:
        """
        Complete document processing workflow
        
        Args:
            file_path: Path to the document file
            
        Returns:
            Complete processing result
        """
        workflow_result = {
            'file_path': file_path,
            'processing_steps': [],
            'final_result': {},
            'success': False,
            'error': None
        }
        
        try:
            # Step 1: Process document (extract text)
            print("Step 1: Processing document...")
            processing_result = self.process_document(file_path)
            workflow_result['processing_steps'].append({
                'step': 'document_processing',
                'result': processing_result
            })
            
            if not processing_result['success']:
                workflow_result['error'] = processing_result['error']
                return workflow_result
            
            document_text = processing_result['text']
            
            # Step 2: Classify document type
            print("Step 2: Classifying document type...")
            classification_result = self.classify_document(document_text)
            workflow_result['processing_steps'].append({
                'step': 'document_classification',
                'result': classification_result
            })
            
            document_type = classification_result.get('document_type', 'unknown')
            
            # Step 3: Extract structured data
            print(f"Step 3: Extracting data for {document_type}...")
            extraction_result = self.extract_data(document_text, document_type)
            workflow_result['processing_steps'].append({
                'step': 'data_extraction',
                'result': extraction_result
            })
            
            # Compile final result
            workflow_result['final_result'] = {
                'document_metadata': processing_result['metadata'],
                'document_type': document_type,
                'classification_confidence': classification_result.get('confidence_score', 0.0),
                'extracted_data': extraction_result.get('extracted_data', {}),
                'extraction_confidence': extraction_result.get('confidence_score', 0.0),
                'processing_notes': extraction_result.get('processing_notes', ''),
                'total_processing_time': None  # Could add timing if needed
            }
            
            workflow_result['success'] = True
            print("Document processing workflow completed successfully!")
            
        except Exception as e:
            workflow_result['error'] = f"Workflow failed: {str(e)}"
            print(f"Workflow error: {str(e)}")
        
        return workflow_result
    
    def batch_process_documents(self, file_paths: List[str]) -> List[Dict[str, Any]]:
        """
        Process multiple documents in batch
        
        Args:
            file_paths: List of document file paths
            
        Returns:
            List of processing results
        """
        results = []
        batch_size = Config.BATCH_SIZE
        
        print(f"Processing {len(file_paths)} documents in batches of {batch_size}...")
        
        for i in range(0, len(file_paths), batch_size):
            batch = file_paths[i:i + batch_size]
            print(f"Processing batch {i//batch_size + 1}: {len(batch)} documents")
            
            for file_path in batch:
                try:
                    result = self.process_document_workflow(file_path)
                    results.append(result)
                except Exception as e:
                    results.append({
                        'file_path': file_path,
                        'success': False,
                        'error': f"Batch processing failed: {str(e)}",
                        'final_result': {}
                    })
        
        return results
    
    def get_processing_statistics(self, results: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Generate processing statistics from batch results
        
        Args:
            results: List of processing results
            
        Returns:
            Processing statistics
        """
        total_docs = len(results)
        successful_docs = sum(1 for r in results if r['success'])
        failed_docs = total_docs - successful_docs
        
        # Document type distribution
        doc_types = {}
        for result in results:
            if result['success']:
                doc_type = result['final_result'].get('document_type', 'unknown')
                doc_types[doc_type] = doc_types.get(doc_type, 0) + 1
        
        # Average confidence scores
        classification_confidences = [
            r['final_result'].get('classification_confidence', 0.0) 
            for r in results if r['success']
        ]
        extraction_confidences = [
            r['final_result'].get('extraction_confidence', 0.0) 
            for r in results if r['success']
        ]
        
        avg_classification_confidence = (
            sum(classification_confidences) / len(classification_confidences) 
            if classification_confidences else 0.0
        )
        avg_extraction_confidence = (
            sum(extraction_confidences) / len(extraction_confidences) 
            if extraction_confidences else 0.0
        )
        
        return {
            'total_documents': total_docs,
            'successful_processing': successful_docs,
            'failed_processing': failed_docs,
            'success_rate': (successful_docs / total_docs * 100) if total_docs > 0 else 0.0,
            'document_type_distribution': doc_types,
            'average_classification_confidence': avg_classification_confidence,
            'average_extraction_confidence': avg_extraction_confidence
        }
