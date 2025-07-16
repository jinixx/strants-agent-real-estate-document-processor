#!/usr/bin/env python3
"""
Test script for Document Q&A functionality
"""
import os
import sys
import json
from src.agents.document_qa_agent import DocumentQAAgent
from src.tools.rag_tool import DocumentRAGTool

def test_rag_tool():
    """Test the RAG tool independently"""
    print("🔍 Testing RAG Tool...")
    
    rag_tool = DocumentRAGTool()
    
    # Test document chunking with sample text
    sample_text = """
    This is a sample real estate settlement statement for the property located at 123 Main Street, Springfield, IL 62701.
    The purchase price is $350,000 and the closing date is July 15, 2024.
    The buyer is John Doe and the seller is Jane Smith.
    The total commission amount is $21,000, which represents 6% of the sale price.
    The property is a single-family home with 3 bedrooms and 2 bathrooms.
    The earnest money deposit was $5,000.
    There are no special contingencies mentioned in this agreement.
    The closing costs total $8,500 and include title insurance, attorney fees, and recording fees.
    """
    
    # Test chunking
    chunks = rag_tool._chunk_document(sample_text, chunk_size=200, overlap=50)
    print(f"✅ Text chunking completed: {len(chunks)} chunks created")
    
    # Test keyword extraction
    question = "What is the purchase price and closing date?"
    keywords = rag_tool._extract_keywords(question)
    print(f"✅ Keywords extracted: {keywords}")
    
    # Test retrieval (simulate loaded document)
    rag_tool.current_document = {
        'text': sample_text,
        'chunks': chunks,
        'metadata': {'test': True},
        'file_path': 'test_document.txt'
    }
    
    relevant_chunks = rag_tool._retrieve_relevant_chunks(question, max_chunks=3)
    print(f"✅ Relevant chunks retrieved: {len(relevant_chunks)} chunks")
    
    for i, chunk in enumerate(relevant_chunks, 1):
        print(f"   Chunk {i}: Score {chunk['relevance_score']:.1f}, Keywords: {chunk['matched_keywords']}")
    
    return True

def test_document_qa_agent():
    """Test the Document Q&A agent"""
    print("\n🤖 Testing Document Q&A Agent...")
    
    try:
        # Initialize agent (this will fail without proper AWS credentials, but we can test the structure)
        agent = DocumentQAAgent()
        
        # Get agent capabilities
        capabilities = agent.get_agent_capabilities()
        print(f"✅ Agent initialized: {capabilities['name']}")
        print(f"📋 Description: {capabilities['description']}")
        print("🔧 Capabilities:")
        for capability in capabilities['capabilities']:
            print(f"  • {capability}")
        
        # Test suggested questions
        suggestions = agent.get_suggested_questions()
        print(f"✅ Suggested questions generated: {len(suggestions)} questions")
        for i, suggestion in enumerate(suggestions[:3], 1):
            print(f"   {i}. {suggestion}")
        
        return True
        
    except Exception as e:
        print(f"⚠️ Agent initialization failed (expected without AWS credentials): {str(e)}")
        return False

def test_mock_qa_workflow():
    """Test a mock Q&A workflow"""
    print("\n💬 Testing Mock Q&A Workflow...")
    
    # Create mock document data
    mock_document_text = """
    SETTLEMENT STATEMENT
    Property Address: 456 Oak Avenue, Springfield, IL 62701
    Sale Price: $425,000
    Closing Date: August 1, 2024
    Buyer: Alice Johnson
    Seller: Bob Wilson
    Commission: $25,500 (6% of sale price)
    Earnest Money: $10,000
    Property Type: Single Family Home
    Bedrooms: 4
    Bathrooms: 3
    Square Footage: 2,200
    Lot Size: 0.25 acres
    Special Conditions: Property sold as-is, buyer waives inspection contingency
    Closing Costs: $9,200
    Title Insurance: $1,500
    Attorney Fees: $800
    Recording Fees: $150
    """
    
    # Initialize RAG tool
    rag_tool = DocumentRAGTool()
    
    # Simulate document loading
    chunks = rag_tool._chunk_document(mock_document_text, chunk_size=300, overlap=50)
    rag_tool.current_document = {
        'text': mock_document_text,
        'chunks': chunks,
        'metadata': {'pages': 1, 'format': 'text'},
        'file_path': 'mock_settlement.txt'
    }
    
    # Test questions
    test_questions = [
        "What is the property address?",
        "What is the sale price?",
        "Who are the buyer and seller?",
        "What is the commission amount?",
        "Are there any special conditions?",
        "What are the closing costs?"
    ]
    
    print(f"✅ Mock document loaded with {len(chunks)} chunks")
    print("🔍 Testing Q&A with sample questions:")
    
    for i, question in enumerate(test_questions[:3], 1):  # Test first 3 questions
        print(f"\n   Q{i}: {question}")
        
        # Get relevant chunks
        relevant_chunks = rag_tool._retrieve_relevant_chunks(question, max_chunks=2)
        
        if relevant_chunks:
            print(f"   📚 Found {len(relevant_chunks)} relevant chunks")
            print(f"   🎯 Best match score: {relevant_chunks[0]['relevance_score']:.1f}")
            print(f"   📝 Context preview: {relevant_chunks[0]['text'][:100]}...")
        else:
            print("   ❌ No relevant chunks found")
    
    return True

def test_conversation_context():
    """Test conversation context functionality"""
    print("\n💭 Testing Conversation Context...")
    
    agent = DocumentQAAgent()
    
    # Simulate conversation history
    agent.conversation_history = [
        {
            'timestamp': 1234567890,
            'question': 'What is the sale price?',
            'answer': 'The sale price is $425,000.'
        },
        {
            'timestamp': 1234567891,
            'question': 'Who is the buyer?',
            'answer': 'The buyer is Alice Johnson.'
        }
    ]
    
    # Test context enhancement
    new_question = "What about the seller?"
    enhanced_question = agent._enhance_question_with_context(new_question)
    
    print("✅ Conversation context test:")
    print(f"   Original question: {new_question}")
    print(f"   Enhanced with context: {len(enhanced_question) > len(new_question)}")
    
    # Test conversation summary
    summary = agent.get_conversation_summary()
    print(f"✅ Conversation summary: {summary['total_questions']} questions in history")
    
    return True

def main():
    """Main test function"""
    print("🚀 Starting Document Q&A Tests")
    print("=" * 50)
    
    # Test 1: RAG Tool
    rag_result = test_rag_tool()
    
    # Test 2: Document Q&A Agent
    agent_result = test_document_qa_agent()
    
    # Test 3: Mock Q&A Workflow
    workflow_result = test_mock_qa_workflow()
    
    # Test 4: Conversation Context
    context_result = test_conversation_context()
    
    print("\n" + "=" * 50)
    print("📋 Test Summary:")
    print(f"🔍 RAG Tool: {'✅ Pass' if rag_result else '❌ Fail'}")
    print(f"🤖 Document Q&A Agent: {'✅ Pass' if agent_result else '❌ Fail'}")
    print(f"💬 Mock Q&A Workflow: {'✅ Pass' if workflow_result else '❌ Fail'}")
    print(f"💭 Conversation Context: {'✅ Pass' if context_result else '❌ Fail'}")
    
    print("\n🎉 All Document Q&A tests completed!")
    print("\n💡 To test the full application:")
    print("   streamlit run app.py")
    print("\n📝 New features available:")
    print("   • Document Q&A with RAG")
    print("   • Intelligent text chunking")
    print("   • Conversation context")
    print("   • Suggested questions")
    print("   • Source attribution")

if __name__ == "__main__":
    main()
