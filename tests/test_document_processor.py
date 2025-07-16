"""
Test cases for StrandsDocumentProcessor
"""
import unittest
import os
import tempfile
from src.tools.document_processor import DocumentProcessor
from src.models.bedrock_model import BedrockModel
from src.agents.document_agent import StrandsDocumentAgent

class TestDocumentProcessor(unittest.TestCase):
    """Test cases for DocumentProcessor"""
    
    def setUp(self):
        self.processor = DocumentProcessor()
    
    def test_validate_document_nonexistent(self):
        """Test validation of non-existent file"""
        result = self.processor.validate_document("nonexistent.pdf")
        self.assertFalse(result['valid'])
        self.assertIn('does not exist', result['error'])
    
    def test_validate_document_unsupported_format(self):
        """Test validation of unsupported file format"""
        with tempfile.NamedTemporaryFile(suffix='.txt', delete=False) as tmp:
            tmp.write(b"test content")
            tmp_path = tmp.name
        
        try:
            result = self.processor.validate_document(tmp_path)
            self.assertFalse(result['valid'])
            self.assertIn('Unsupported file format', result['error'])
        finally:
            os.unlink(tmp_path)

class TestBedrockModel(unittest.TestCase):
    """Test cases for BedrockModel"""
    
    def setUp(self):
        # Note: These tests require AWS credentials and Bedrock access
        # Skip if not available
        try:
            self.model = BedrockModel()
        except Exception:
            self.skipTest("AWS credentials or Bedrock access not available")
    
    def test_classify_document_sample(self):
        """Test document classification with sample text"""
        sample_text = """
        SETTLEMENT STATEMENT
        Property Address: 123 Main Street, Anytown, ST 12345
        Sale Price: $350,000
        Commission: $21,000 (6%)
        Closing Date: 2024-01-15
        """
        
        result = self.model.classify_document(sample_text)
        self.assertIn('document_type', result)
        self.assertIn('confidence_score', result)

class TestStrandsDocumentAgent(unittest.TestCase):
    """Test cases for StrandsDocumentAgent"""
    
    def setUp(self):
        try:
            self.agent = StrandsDocumentAgent()
        except Exception:
            self.skipTest("Agent initialization failed - AWS credentials may not be available")
    
    def test_agent_initialization(self):
        """Test agent initialization"""
        self.assertIsNotNone(self.agent)
        self.assertEqual(self.agent.name, "StrandsDocumentProcessor")
        self.assertEqual(len(self.agent.tools), 3)

if __name__ == '__main__':
    unittest.main()
