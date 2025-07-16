"""
Agentic AI Agent for Property Research using AWS Strands AI
Processes settlement documents and searches web information about properties
"""
from typing import Dict, Any, List, Optional
import json
import time
from src.agents.document_agent import StrandsDocumentAgent
from src.tools.web_search_tool import WebSearchTool
from src.models.bedrock_model import BedrockModel
from src.config import Config

class PropertyResearchAgent:
    """
    Agentic AI Agent that combines document processing with web-based property research
    """
    
    def __init__(self, aws_profile: Optional[str] = None):
        """
        Initialize the Property Research Agent
        
        Args:
            aws_profile: AWS profile name for authentication
        """
        # Initialize core components
        self.document_agent = StrandsDocumentAgent(aws_profile=aws_profile)
        self.web_search_tool = WebSearchTool()
        self.bedrock_model = BedrockModel(profile_name=aws_profile)
        
        # Agent metadata
        self.name = "PropertyResearchAgent"
        self.description = "Agentic AI agent that processes settlement documents and researches property information from web sources"
        self.capabilities = [
            "Document processing and data extraction",
            "Property information web search",
            "Market analysis and insights",
            "Comprehensive property reports",
            "Investment analysis"
        ]
    
    def research_property_workflow(self, file_path: str) -> Dict[str, Any]:
        """
        Complete property research workflow combining document processing and web search
        
        Args:
            file_path: Path to the settlement document
            
        Returns:
            Comprehensive property research result
        """
        workflow_result = {
            'file_path': file_path,
            'agent_name': self.name,
            'workflow_steps': [],
            'document_analysis': {},
            'web_research': {},
            'ai_insights': {},
            'comprehensive_report': {},
            'success': False,
            'error': None,
            'processing_time': 0
        }
        
        start_time = time.time()
        
        try:
            # Step 1: Process the settlement document
            print("🔍 Step 1: Processing settlement document...")
            document_result = self.document_agent.process_document_workflow(file_path)
            workflow_result['workflow_steps'].append({
                'step': 'document_processing',
                'status': 'completed' if document_result['success'] else 'failed',
                'result': document_result
            })
            
            if not document_result['success']:
                workflow_result['error'] = f"Document processing failed: {document_result.get('error', 'Unknown error')}"
                return workflow_result
            
            workflow_result['document_analysis'] = document_result['final_result']
            
            # Step 2: Extract property address from document
            print("📍 Step 2: Extracting property information...")
            property_info = self._extract_property_info(document_result['final_result'])
            workflow_result['workflow_steps'].append({
                'step': 'property_extraction',
                'status': 'completed',
                'result': property_info
            })
            
            if not property_info.get('address'):
                workflow_result['error'] = "Could not extract property address from document"
                return workflow_result
            
            # Step 3: Web search for property information
            print("🌐 Step 3: Searching web for property information...")
            web_search_result = self.web_search_tool.search_property_info(
                property_address=property_info['address'],
                city=property_info.get('city', ''),
                state=property_info.get('state', ''),
                zip_code=property_info.get('zip_code', '')
            )
            workflow_result['workflow_steps'].append({
                'step': 'web_search',
                'status': 'completed' if web_search_result['success'] else 'failed',
                'result': web_search_result
            })
            
            workflow_result['web_research'] = web_search_result
            
            # Step 4: Generate AI insights combining document and web data
            print("🤖 Step 4: Generating AI insights...")
            ai_insights = self._generate_ai_insights(
                document_data=workflow_result['document_analysis'],
                web_data=web_search_result
            )
            workflow_result['workflow_steps'].append({
                'step': 'ai_insights',
                'status': 'completed' if ai_insights['success'] else 'failed',
                'result': ai_insights
            })
            
            workflow_result['ai_insights'] = ai_insights
            
            # Step 5: Generate comprehensive property report
            print("📊 Step 5: Generating comprehensive property report...")
            comprehensive_report = self._generate_comprehensive_report(
                document_analysis=workflow_result['document_analysis'],
                web_research=workflow_result['web_research'],
                ai_insights=workflow_result['ai_insights']
            )
            workflow_result['workflow_steps'].append({
                'step': 'comprehensive_report',
                'status': 'completed',
                'result': comprehensive_report
            })
            
            workflow_result['comprehensive_report'] = comprehensive_report
            workflow_result['success'] = True
            
            print("✅ Property research workflow completed successfully!")
            
        except Exception as e:
            workflow_result['error'] = f"Workflow failed: {str(e)}"
            print(f"❌ Workflow error: {str(e)}")
        
        finally:
            workflow_result['processing_time'] = time.time() - start_time
        
        return workflow_result
    
    def _extract_property_info(self, document_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Extract property information from processed document data
        
        Args:
            document_data: Processed document data
            
        Returns:
            Extracted property information
        """
        extracted_data = document_data.get('extracted_data', {})
        
        # Extract address components
        property_info = {
            'address': extracted_data.get('property_address', ''),
            'city': extracted_data.get('property_city', ''),
            'state': extracted_data.get('property_state', ''),
            'zip_code': extracted_data.get('property_zip', ''),
            'sale_price': extracted_data.get('sale_price', 0),
            'closing_date': extracted_data.get('closing_date', ''),
            'buyer_name': extracted_data.get('buyer_name', ''),
            'seller_name': extracted_data.get('seller_name', '')
        }
        
        # Clean up address if needed
        if not property_info['address'] and 'property_information' in extracted_data:
            # Try to extract from property_information field
            prop_info = str(extracted_data['property_information'])
            # Simple address extraction logic (can be enhanced)
            lines = prop_info.split('\n')
            for line in lines:
                if any(word in line.lower() for word in ['street', 'ave', 'road', 'dr', 'way', 'blvd']):
                    property_info['address'] = line.strip()
                    break
        
        return property_info
    
    def _generate_ai_insights(self, document_data: Dict[str, Any], web_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Generate AI insights by analyzing document and web data
        
        Args:
            document_data: Processed document data
            web_data: Web search results
            
        Returns:
            AI-generated insights
        """
        try:
            # Prepare data for AI analysis
            analysis_prompt = self._create_analysis_prompt(document_data, web_data)
            
            # Use Bedrock model to generate insights
            insights_result = self.bedrock_model.generate_property_insights(analysis_prompt)
            
            return {
                'success': True,
                'insights': insights_result.get('insights', {}),
                'investment_analysis': insights_result.get('investment_analysis', {}),
                'market_comparison': insights_result.get('market_comparison', {}),
                'risk_assessment': insights_result.get('risk_assessment', {}),
                'recommendations': insights_result.get('recommendations', [])
            }
            
        except Exception as e:
            return {
                'success': False,
                'error': f"AI insights generation failed: {str(e)}",
                'insights': {},
                'investment_analysis': {},
                'market_comparison': {},
                'risk_assessment': {},
                'recommendations': []
            }
    
    def _create_analysis_prompt(self, document_data: Dict[str, Any], web_data: Dict[str, Any]) -> str:
        """
        Create analysis prompt for AI insights generation
        
        Args:
            document_data: Document analysis data
            web_data: Web search data
            
        Returns:
            Formatted prompt for AI analysis
        """
        extracted_data = document_data.get('extracted_data', {})
        market_data = web_data.get('market_data', {})
        neighborhood_info = web_data.get('neighborhood_info', {})
        
        prompt = f"""
        Analyze the following property transaction and market data to provide comprehensive insights:

        TRANSACTION DATA:
        - Property Address: {extracted_data.get('property_address', 'N/A')}
        - Sale Price: ${extracted_data.get('sale_price', 'N/A')}
        - Closing Date: {extracted_data.get('closing_date', 'N/A')}
        - Commission: ${extracted_data.get('commission_amount', 'N/A')}

        MARKET DATA:
        - Estimated Current Value: ${market_data.get('estimated_value', 'N/A')}
        - Property Type: {market_data.get('property_type', 'N/A')}
        - Days on Market: {market_data.get('days_on_market', 'N/A')}
        - Market Trends: {market_data.get('market_trends', {})}

        NEIGHBORHOOD DATA:
        - Walkability Score: {neighborhood_info.get('walkability_score', 'N/A')}
        - Transit Score: {neighborhood_info.get('transit_score', 'N/A')}
        - Demographics: {neighborhood_info.get('demographics', {})}

        Please provide:
        1. Investment analysis (ROI potential, market position)
        2. Market comparison (how this sale compares to market)
        3. Risk assessment (potential risks and opportunities)
        4. Recommendations for buyers/sellers/investors
        """
        
        return prompt
    
    def _generate_comprehensive_report(self, document_analysis: Dict[str, Any], 
                                     web_research: Dict[str, Any], 
                                     ai_insights: Dict[str, Any]) -> Dict[str, Any]:
        """
        Generate comprehensive property report
        
        Args:
            document_analysis: Document processing results
            web_research: Web search results
            ai_insights: AI-generated insights
            
        Returns:
            Comprehensive property report
        """
        extracted_data = document_analysis.get('extracted_data', {})
        market_data = web_research.get('market_data', {})
        neighborhood_info = web_research.get('neighborhood_info', {})
        
        report = {
            'report_generated': time.strftime('%Y-%m-%d %H:%M:%S'),
            'property_summary': {
                'address': extracted_data.get('property_address', 'N/A'),
                'sale_price': extracted_data.get('sale_price', 0),
                'estimated_current_value': market_data.get('estimated_value', 0),
                'property_type': market_data.get('property_type', 'N/A'),
                'closing_date': extracted_data.get('closing_date', 'N/A')
            },
            'financial_analysis': {
                'transaction_price': extracted_data.get('sale_price', 0),
                'current_market_value': market_data.get('estimated_value', 0),
                'value_change': self._calculate_value_change(
                    extracted_data.get('sale_price', 0),
                    market_data.get('estimated_value', 0)
                ),
                'commission_paid': extracted_data.get('commission_amount', 0),
                'price_per_sqft': self._calculate_price_per_sqft(
                    extracted_data.get('sale_price', 0),
                    market_data.get('square_footage', 0)
                )
            },
            'market_analysis': {
                'market_trends': market_data.get('market_trends', {}),
                'days_on_market': market_data.get('days_on_market', 0),
                'comparable_properties': web_research.get('comparable_properties', []),
                'market_temperature': market_data.get('market_trends', {}).get('market_temperature', 'N/A')
            },
            'neighborhood_analysis': {
                'walkability_score': neighborhood_info.get('walkability_score', 0),
                'transit_score': neighborhood_info.get('transit_score', 0),
                'bike_score': neighborhood_info.get('bike_score', 0),
                'nearby_amenities': neighborhood_info.get('nearby_amenities', []),
                'demographics': neighborhood_info.get('demographics', {}),
                'school_information': web_research.get('school_information', {}),
                'crime_statistics': web_research.get('crime_statistics', {})
            },
            'ai_insights': ai_insights.get('insights', {}),
            'investment_analysis': ai_insights.get('investment_analysis', {}),
            'recommendations': ai_insights.get('recommendations', []),
            'risk_assessment': ai_insights.get('risk_assessment', {}),
            'data_sources': {
                'document_processing': 'AWS Bedrock Claude Sonnet',
                'web_search': 'Multiple real estate sources',
                'ai_analysis': 'AWS Bedrock Claude Sonnet'
            }
        }
        
        return report
    
    def _calculate_value_change(self, sale_price: float, current_value: float) -> Dict[str, Any]:
        """Calculate value change between sale and current estimated value"""
        if not sale_price or not current_value:
            return {'amount': 0, 'percentage': 0, 'direction': 'unknown'}
        
        change_amount = current_value - sale_price
        change_percentage = (change_amount / sale_price) * 100 if sale_price > 0 else 0
        direction = 'increase' if change_amount > 0 else 'decrease' if change_amount < 0 else 'stable'
        
        return {
            'amount': change_amount,
            'percentage': round(change_percentage, 2),
            'direction': direction
        }
    
    def _calculate_price_per_sqft(self, sale_price: float, square_footage: float) -> float:
        """Calculate price per square foot"""
        if not sale_price or not square_footage:
            return 0
        return round(sale_price / square_footage, 2)
    
    def get_agent_capabilities(self) -> Dict[str, Any]:
        """
        Get agent capabilities and information
        
        Returns:
            Agent capabilities and metadata
        """
        return {
            'name': self.name,
            'description': self.description,
            'capabilities': self.capabilities,
            'supported_document_types': Config.DOCUMENT_TYPES,
            'web_search_sources': self.web_search_tool.search_sources,
            'ai_model': Config.BEDROCK_MODEL_ID
        }
