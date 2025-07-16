#!/usr/bin/env python3
"""
Test script for Property Research Agent
"""
import os
import sys
import json
from src.agents.property_research_agent import PropertyResearchAgent
from src.tools.web_search_tool import WebSearchTool

def test_web_search_tool():
    """Test the web search tool independently"""
    print("🔍 Testing Web Search Tool...")
    
    web_tool = WebSearchTool()
    
    # Test property search
    result = web_tool.search_property_info(
        property_address="123 Main Street",
        city="Anytown",
        state="CA",
        zip_code="12345"
    )
    
    print(f"✅ Web search completed: {result['success']}")
    if result['success']:
        print(f"📍 Property Address: {result['property_address']}")
        print(f"💰 Estimated Value: ${result['market_data'].get('estimated_value', 0):,}")
        print(f"🏘️ Walkability Score: {result['neighborhood_info'].get('walkability_score', 0)}/100")
        print(f"🎓 School District: {result['school_information'].get('school_district', 'N/A')}")
    else:
        print(f"❌ Error: {result['error']}")
    
    return result

def test_property_research_agent():
    """Test the property research agent"""
    print("\n🤖 Testing Property Research Agent...")
    
    try:
        # Initialize agent (this will fail without proper AWS credentials, but we can test the structure)
        agent = PropertyResearchAgent()
        
        # Get agent capabilities
        capabilities = agent.get_agent_capabilities()
        print(f"✅ Agent initialized: {capabilities['name']}")
        print(f"📋 Description: {capabilities['description']}")
        print("🔧 Capabilities:")
        for capability in capabilities['capabilities']:
            print(f"  • {capability}")
        
        return True
        
    except Exception as e:
        print(f"⚠️ Agent initialization failed (expected without AWS credentials): {str(e)}")
        return False

def test_mock_workflow():
    """Test a mock workflow without actual AWS calls"""
    print("\n📊 Testing Mock Workflow...")
    
    # Create mock document data
    mock_document_data = {
        'document_type': 'settlement_document',
        'extracted_data': {
            'property_address': '456 Oak Avenue',
            'property_city': 'Springfield',
            'property_state': 'IL',
            'property_zip': '62701',
            'sale_price': 350000,
            'closing_date': '2024-07-15',
            'buyer_name': 'John Doe',
            'seller_name': 'Jane Smith',
            'commission_amount': 21000
        },
        'classification_confidence': 0.95,
        'extraction_confidence': 0.88
    }
    
    # Test web search with extracted data
    web_tool = WebSearchTool()
    web_result = web_tool.search_property_info(
        property_address=mock_document_data['extracted_data']['property_address'],
        city=mock_document_data['extracted_data']['property_city'],
        state=mock_document_data['extracted_data']['property_state'],
        zip_code=mock_document_data['extracted_data']['property_zip']
    )
    
    print(f"✅ Mock workflow completed successfully!")
    print(f"📄 Document Type: {mock_document_data['document_type']}")
    print(f"📍 Property: {mock_document_data['extracted_data']['property_address']}")
    print(f"💰 Sale Price: ${mock_document_data['extracted_data']['sale_price']:,}")
    print(f"🌐 Web Search: {'Success' if web_result['success'] else 'Failed'}")
    
    if web_result['success']:
        print(f"📊 Current Est. Value: ${web_result['market_data'].get('estimated_value', 0):,}")
        print(f"🏘️ Walkability: {web_result['neighborhood_info'].get('walkability_score', 0)}/100")
        
        # Calculate value change
        sale_price = mock_document_data['extracted_data']['sale_price']
        current_value = web_result['market_data'].get('estimated_value', 0)
        if sale_price and current_value:
            change = current_value - sale_price
            change_pct = (change / sale_price) * 100
            print(f"📈 Value Change: ${change:,} ({change_pct:+.1f}%)")
    
    return True

def main():
    """Main test function"""
    print("🚀 Starting Property Research Agent Tests")
    print("=" * 50)
    
    # Test 1: Web Search Tool
    web_result = test_web_search_tool()
    
    # Test 2: Property Research Agent
    agent_result = test_property_research_agent()
    
    # Test 3: Mock Workflow
    workflow_result = test_mock_workflow()
    
    print("\n" + "=" * 50)
    print("📋 Test Summary:")
    print(f"🔍 Web Search Tool: {'✅ Pass' if web_result['success'] else '❌ Fail'}")
    print(f"🤖 Property Research Agent: {'✅ Pass' if agent_result else '❌ Fail'}")
    print(f"📊 Mock Workflow: {'✅ Pass' if workflow_result else '❌ Fail'}")
    
    print("\n🎉 All tests completed!")
    print("\n💡 To run the full application:")
    print("   streamlit run app.py")

if __name__ == "__main__":
    main()
