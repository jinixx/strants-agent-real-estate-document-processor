"""
Configuration settings for StrandsDocumentProcessor
"""
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class Config:
    # AWS Configuration
    AWS_REGION = os.getenv('AWS_REGION', 'us-west-2')
    AWS_PROFILE = os.getenv('AWS_PROFILE', 'default')
    
    # Bedrock Configuration
    BEDROCK_MODEL_ID = os.getenv('BEDROCK_MODEL_ID', 'anthropic.claude-3-sonnet-20240229-v1:0')
    
    # Application Configuration
    APP_NAME = os.getenv('APP_NAME', 'StrandsDocumentProcessor')
    DEBUG = os.getenv('DEBUG', 'True').lower() == 'true'
    MAX_FILE_SIZE = os.getenv('MAX_FILE_SIZE', '50MB')
    SUPPORTED_FORMATS = os.getenv('SUPPORTED_FORMATS', 'pdf,png,jpg,jpeg,tiff').split(',')
    
    # Processing Configuration
    MAX_PAGES = int(os.getenv('MAX_PAGES', '500'))
    PROCESSING_TIMEOUT = int(os.getenv('PROCESSING_TIMEOUT', '300'))
    BATCH_SIZE = int(os.getenv('BATCH_SIZE', '10'))
    
    # Document Types
    DOCUMENT_TYPES = [
        'settlement',
        'purchase_agreement', 
        'income_verification'
    ]
    
    # Extraction Fields
    EXTRACTION_FIELDS = {
        'settlement': [
            'property_address',
            'sale_price',
            'commission_amount',
            'commission_percentage',
            'closing_date',
            'buyer_name',
            'seller_name',
            'agent_name',
            'brokerage_name'
        ],
        'purchase_agreement': [
            'property_address',
            'purchase_price',
            'earnest_money',
            'closing_date',
            'buyer_name',
            'seller_name',
            'agent_name',
            'contingencies'
        ],
        'income_verification': [
            'applicant_name',
            'employer_name',
            'annual_income',
            'employment_start_date',
            'employment_status',
            'verification_date'
        ]
    }
