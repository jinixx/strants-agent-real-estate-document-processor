"""
Bedrock Model integration for StrandsDocumentProcessor
"""
import boto3
import json
from typing import Dict, Any, Optional
from src.config import Config

class BedrockModel:
    """
    AWS Bedrock model integration using Claude Sonnet
    """
    
    def __init__(self, profile_name: Optional[str] = None):
        """
        Initialize Bedrock client
        
        Args:
            profile_name: AWS profile name for authentication
        """
        self.profile_name = profile_name or Config.AWS_PROFILE
        self.region = Config.AWS_REGION
        self.model_id = Config.BEDROCK_MODEL_ID
        
        # Initialize Bedrock client
        session = boto3.Session(profile_name=self.profile_name)
        self.bedrock_client = session.client(
            service_name='bedrock-runtime',
            region_name=self.region
        )
    
    def invoke_model(self, prompt: str, max_tokens: int = 4000) -> Dict[str, Any]:
        """
        Invoke Claude Sonnet model via Bedrock
        
        Args:
            prompt: Input prompt for the model
            max_tokens: Maximum tokens to generate
            
        Returns:
            Model response as dictionary
        """
        try:
            # Prepare request body for Claude
            body = {
                "anthropic_version": "bedrock-2023-05-31",
                "max_tokens": max_tokens,
                "messages": [
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                "temperature": 0.1,
                "top_p": 0.9
            }
            
            # Invoke model
            response = self.bedrock_client.invoke_model(
                modelId=self.model_id,
                body=json.dumps(body),
                contentType='application/json',
                accept='application/json'
            )
            
            # Parse response
            response_body = json.loads(response['body'].read())
            
            return {
                'success': True,
                'content': response_body.get('content', [{}])[0].get('text', ''),
                'usage': response_body.get('usage', {}),
                'model_id': self.model_id
            }
            
        except Exception as e:
            return {
                'success': False,
                'error': str(e),
                'content': '',
                'model_id': self.model_id
            }
    
    def extract_document_data(self, document_text: str, document_type: str) -> Dict[str, Any]:
        """
        Extract structured data from document text
        
        Args:
            document_text: Raw text from document
            document_type: Type of document (settlement, purchase_agreement, income_verification)
            
        Returns:
            Extracted data as dictionary
        """
        extraction_fields = Config.EXTRACTION_FIELDS.get(document_type, [])
        
        prompt = f"""
        You are a real estate document processing expert. Extract the following information from this {document_type} document:
        
        Fields to extract: {', '.join(extraction_fields)}
        
        Document text:
        {document_text}
        
        Please return the extracted information in JSON format with the following structure:
        {{
            "document_type": "{document_type}",
            "extracted_data": {{
                // Include only the fields that are found in the document
                // Use null for fields that cannot be found
            }},
            "confidence_score": // A number between 0-1 indicating extraction confidence,
            "processing_notes": "Any issues or observations about the document quality or extraction"
        }}
        
        Important guidelines:
        - Only extract information that is clearly present in the document
        - Use null for missing information
        - Normalize dates to YYYY-MM-DD format
        - Normalize currency amounts to numbers without symbols
        - Be precise and accurate
        """
        
        response = self.invoke_model(prompt)
        
        if response['success']:
            try:
                # Try to parse JSON from response
                extracted_data = json.loads(response['content'])
                return extracted_data
            except json.JSONDecodeError:
                # If JSON parsing fails, return raw response
                return {
                    'document_type': document_type,
                    'extracted_data': {},
                    'confidence_score': 0.0,
                    'processing_notes': f'Failed to parse extraction results: {response["content"]}'
                }
        else:
            return {
                'document_type': document_type,
                'extracted_data': {},
                'confidence_score': 0.0,
                'processing_notes': f'Model invocation failed: {response["error"]}'
            }
    
    def classify_document(self, document_text: str) -> Dict[str, Any]:
        """
        Classify document type
        
        Args:
            document_text: Raw text from document
            
        Returns:
            Classification result
        """
        document_types = Config.DOCUMENT_TYPES
        
        prompt = f"""
        You are a real estate document classifier. Analyze the following document text and classify it into one of these categories:
        
        Categories: {', '.join(document_types)}
        
        Document text:
        {document_text[:2000]}...  # First 2000 characters for classification
        
        Please return your classification in JSON format:
        {{
            "document_type": "one of the categories above",
            "confidence_score": // A number between 0-1,
            "reasoning": "Brief explanation of why you classified it this way"
        }}
        """
        
        response = self.invoke_model(prompt)
        
        if response['success']:
            try:
                classification = json.loads(response['content'])
                return classification
            except json.JSONDecodeError:
                return {
                    'document_type': 'unknown',
                    'confidence_score': 0.0,
                    'reasoning': f'Failed to parse classification: {response["content"]}'
                }
        else:
            return {
                'document_type': 'unknown',
                'confidence_score': 0.0,
                'reasoning': f'Classification failed: {response["error"]}'
            }
    
    def generate_property_insights(self, analysis_prompt: str) -> Dict[str, Any]:
        """
        Generate AI insights for property analysis
        
        Args:
            analysis_prompt: Formatted prompt with property and market data
            
        Returns:
            AI-generated insights and analysis
        """
        enhanced_prompt = f"""
        {analysis_prompt}
        
        Please provide a comprehensive analysis in JSON format with the following structure:
        {{
            "insights": {{
                "market_position": "Analysis of how this property compares to the market",
                "value_assessment": "Assessment of the property value and pricing",
                "transaction_analysis": "Analysis of the transaction details"
            }},
            "investment_analysis": {{
                "roi_potential": "Return on investment potential",
                "appreciation_outlook": "Property appreciation outlook",
                "rental_potential": "Rental income potential if applicable",
                "investment_grade": "A-F grade for investment potential"
            }},
            "market_comparison": {{
                "vs_neighborhood_average": "How this compares to neighborhood average",
                "vs_comparable_sales": "Comparison to recent comparable sales",
                "market_timing": "Assessment of market timing for this transaction"
            }},
            "risk_assessment": {{
                "market_risks": ["List of market-related risks"],
                "property_risks": ["List of property-specific risks"],
                "overall_risk_level": "Low/Medium/High",
                "risk_mitigation": ["Suggestions for risk mitigation"]
            }},
            "recommendations": [
                "Specific actionable recommendations for buyers, sellers, or investors"
            ]
        }}
        
        Base your analysis on the provided data and real estate market principles.
        """
        
        response = self.invoke_model(enhanced_prompt, max_tokens=6000)
        
        if response['success']:
            try:
                insights = json.loads(response['content'])
                return insights
            except json.JSONDecodeError:
                return {
                    'insights': {'error': 'Failed to parse AI insights'},
                    'investment_analysis': {},
                    'market_comparison': {},
                    'risk_assessment': {},
                    'recommendations': [response['content']]  # Return raw content as recommendation
                }
        else:
            return {
                'insights': {'error': f'AI insights generation failed: {response["error"]}'},
                'investment_analysis': {},
                'market_comparison': {},
                'risk_assessment': {},
                'recommendations': []
            }
