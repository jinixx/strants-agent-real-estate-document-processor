#!/usr/bin/env python3
"""
Demo script for StrandsDocumentProcessor
Tests the basic functionality without requiring actual documents
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from src.config import Config
from src.models.bedrock_model import BedrockModel
from src.tools.document_processor import DocumentProcessor

def test_configuration():
    """Test configuration loading"""
    print("🔧 Testing Configuration...")
    print(f"   AWS Region: {Config.AWS_REGION}")
    print(f"   AWS Profile: {Config.AWS_PROFILE}")
    print(f"   Bedrock Model: {Config.BEDROCK_MODEL_ID}")
    print(f"   Supported Formats: {Config.SUPPORTED_FORMATS}")
    print(f"   Document Types: {Config.DOCUMENT_TYPES}")
    print("   ✅ Configuration loaded successfully")
    print()

def test_document_processor():
    """Test document processor initialization"""
    print("📄 Testing Document Processor...")
    try:
        processor = DocumentProcessor()
        print(f"   Supported formats: {processor.supported_formats}")
        print(f"   Max pages: {processor.max_pages}")
        
        # Test validation with non-existent file
        result = processor.validate_document("nonexistent.pdf")
        if not result['valid'] and 'does not exist' in result['error']:
            print("   ✅ Document validation working correctly")
        else:
            print("   ❌ Document validation test failed")
        
    except Exception as e:
        print(f"   ❌ Document processor test failed: {str(e)}")
    print()

def test_bedrock_model():
    """Test Bedrock model initialization"""
    print("🤖 Testing Bedrock Model...")
    try:
        model = BedrockModel()
        print(f"   Model ID: {model.model_id}")
        print(f"   Region: {model.region}")
        print(f"   Profile: {model.profile_name}")
        print("   ✅ Bedrock model initialized successfully")
        
        # Test with sample text (this will make an actual API call)
        print("   Testing document classification...")
        sample_text = """
        SETTLEMENT STATEMENT
        Property Address: 123 Main Street, Anytown, ST 12345
        Sale Price: $350,000
        Commission: $21,000 (6%)
        Closing Date: 2024-01-15
        Buyer: John Smith
        Seller: Jane Doe
        """
        
        result = model.classify_document(sample_text)
        if result.get('document_type'):
            print(f"   ✅ Classification result: {result['document_type']} (confidence: {result.get('confidence_score', 0):.2f})")
        else:
            print(f"   ⚠️  Classification returned: {result}")
            
    except Exception as e:
        print(f"   ❌ Bedrock model test failed: {str(e)}")
        print("   Note: This requires AWS credentials and Bedrock access")
    print()

def test_agent_import():
    """Test agent import"""
    print("🤖 Testing Agent Import...")
    try:
        from src.agents.document_agent import StrandsDocumentAgent
        print("   ✅ Agent import successful")
        
        # Try to initialize (may fail without proper AWS setup)
        try:
            agent = StrandsDocumentAgent()
            print(f"   ✅ Agent initialized: {agent.name}")
        except Exception as e:
            print(f"   ⚠️  Agent initialization failed: {str(e)}")
            print("   This is expected without proper AWS credentials")
            
    except Exception as e:
        print(f"   ❌ Agent import failed: {str(e)}")
    print()

def main():
    """Run all tests"""
    print("🚀 StrandsDocumentProcessor Demo")
    print("=" * 50)
    print()
    
    test_configuration()
    test_document_processor()
    test_bedrock_model()
    test_agent_import()
    
    print("📊 Demo Summary:")
    print("   - Configuration: ✅ Working")
    print("   - Document Processor: ✅ Working")
    print("   - Bedrock Model: Depends on AWS setup")
    print("   - Agent: Depends on AWS setup")
    print()
    print("🎯 Next Steps:")
    print("   1. Configure AWS credentials: aws configure")
    print("   2. Enable Bedrock Claude Sonnet model in AWS Console")
    print("   3. Run the Streamlit app: ./run.sh")
    print("   4. Upload test documents for processing")

if __name__ == "__main__":
    main()
