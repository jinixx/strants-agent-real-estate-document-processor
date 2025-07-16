# StrandsDocumentProcessor

A conversational AI agent built with AWS Strands Agent SDK for processing and extracting data from real estate documents, now enhanced with **Agentic AI Property Research** and **Document Q&A** capabilities.

## Features

- **Automatic Document Classification**: Identifies settlement documents, purchase agreements, and income verifications
- **Intelligent Data Extraction**: Extracts critical transaction data including commission details and property information
- **🆕 Agentic AI Property Research**: Combines document processing with web-based property research and AI insights
- **🆕 Document Q&A with RAG**: Ask natural language questions about any uploaded document
- **Multi-Format Support**: Handles PDF, PNG, JPG, JPEG, and TIFF files (2-500 pages)
- **Quality Enhancement**: Automatically handles poor image quality and orientation issues
- **Batch Processing**: Efficiently processes 150,000+ annual settlement documents
- **Real-time Interface**: Clean Streamlit web interface with real-time processing status
- **AWS Integration**: Uses Claude Sonnet on Amazon Bedrock for AI processing

## 🆕 New: Document Q&A with RAG

The new **Document Q&A Agent** provides intelligent question-answering capabilities:

### 💬 RAG-Based Q&A
- **Smart Document Loading**: Processes and chunks documents for optimal retrieval
- **Natural Language Questions**: Ask questions in plain English about document content
- **Accurate Answers**: RAG-based responses with source citations and confidence scores
- **Conversation Context**: Maintains context across multiple questions for better understanding

### 🔍 Q&A Features
- **Suggested Questions**: AI-generated relevant questions based on document content
- **Source Attribution**: Shows which parts of the document were used to answer questions
- **Document Summaries**: Automatic generation of document overviews
- **Multi-turn Conversations**: Maintains conversation history for contextual answers
- **Confidence Scoring**: Provides confidence levels for each answer
- **Chunk Visualization**: Shows relevant document sections used for answers

## 🆕 New: Agentic AI Property Research

The new **Property Research Agent** provides comprehensive property analysis by:

### 🤖 Autonomous AI Workflow
- **Document Processing**: Extracts property details from settlement documents
- **Web Research**: Searches multiple sources for current market data
- **Data Integration**: Combines document and web data for comprehensive analysis
- **AI Insights**: Generates investment analysis and recommendations

### 📊 Research Capabilities
- **Market Analysis**: Current property values, price trends, comparable sales
- **Neighborhood Intelligence**: Walkability scores, transit access, demographics
- **School Information**: District ratings, nearby schools, enrollment data
- **Safety Data**: Crime statistics and safety scores
- **Investment Analysis**: ROI potential, risk assessment, market timing
- **Comprehensive Reports**: All data compiled into actionable insights

### 🔍 Data Sources
- Real estate market data (Zillow, Realtor.com, Redfin, Trulia)
- Neighborhood and demographic information
- School district and rating data
- Crime and safety statistics
- AI-powered analysis using AWS Bedrock Claude Sonnet

## Architecture

```
StrandsDocumentProcessor/
├── src/
│   ├── agents/          # Strands Agent implementation
│   ├── models/          # Bedrock model integration
│   ├── tools/           # Document processing tools
│   ├── utils/           # Utility functions
│   └── config.py        # Configuration settings
├── tests/               # Test files
├── uploads/             # Temporary file storage
├── app.py              # Streamlit web interface
├── requirements.txt    # Python dependencies
└── .env               # Environment variables
```

## Quick Start

### Prerequisites

- Python 3.8+
- AWS CLI configured with appropriate permissions
- Access to Amazon Bedrock (Claude Sonnet model)

### Installation

1. **Clone and navigate to the project:**
   ```bash
   cd /home/ubuntu/environment/capproject/StrandsDocumentProcessor
   ```

2. **Activate the virtual environment:**
   ```bash
   source venv/bin/activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment variables:**
   Edit `.env` file with your AWS settings:
   ```
   AWS_REGION=us-west-2
   AWS_PROFILE=default
   BEDROCK_MODEL_ID=anthropic.claude-3-sonnet-20240229-v1:0
   ```

5. **Run the application:**
   ```bash
   streamlit run app.py
   ```

## Usage

### Web Interface

1. **Single Document Processing:**
   - Upload a document (PDF or image)
   - Click "Process Document"
   - View extracted data and classification results

2. **🆕 Property Research:**
   - Upload a settlement document
   - Click "Start Property Research"
   - View comprehensive property analysis including:
     - Document processing results
     - Current market data and trends
     - Neighborhood information and amenities
     - School ratings and district information
     - Crime statistics and safety scores
     - AI-generated investment insights and recommendations

3. **🆕 Document Q&A:**
   - Upload any document (PDF or image)
   - Click "Load Document for Q&A"
   - Ask questions about the document content
   - Get AI-powered answers with source citations
   - Use suggested questions or ask custom questions
   - Maintain conversation context across multiple questions

4. **Batch Processing:**
   - Upload multiple documents
   - Monitor processing progress
   - Review batch statistics and results

### Programmatic Usage

```python
from src.agents.document_agent import StrandsDocumentAgent
from src.agents.property_research_agent import PropertyResearchAgent
from src.agents.document_qa_agent import DocumentQAAgent

# Initialize document agent
agent = StrandsDocumentAgent(aws_profile='default')

# Process single document
result = agent.process_document_workflow('path/to/document.pdf')

# Process multiple documents
results = agent.batch_process_documents(['doc1.pdf', 'doc2.pdf'])

# Get processing statistics
stats = agent.get_processing_statistics(results)

# 🆕 Initialize property research agent
research_agent = PropertyResearchAgent(aws_profile='default')

# Perform comprehensive property research
research_result = research_agent.research_property_workflow('path/to/settlement.pdf')

# Access comprehensive report
if research_result['success']:
    report = research_result['comprehensive_report']
    property_summary = report['property_summary']
    market_analysis = report['market_analysis']
    ai_insights = research_result['ai_insights']

# 🆕 Initialize document Q&A agent
qa_agent = DocumentQAAgent(aws_profile='default')

# Load document for Q&A
load_result = qa_agent.load_document_workflow('path/to/document.pdf')

# Ask questions about the document
if load_result['success']:
    qa_result = qa_agent.ask_question_workflow("What is the main topic of this document?")
    answer = qa_result['answer_result']['answer']
    confidence = qa_result['answer_result']['confidence']
    
    # Get suggested questions
    suggestions = qa_agent.get_suggested_questions()
```

## Document Types

### Settlement Documents
- Property address and sale price
- Commission amount and percentage
- Closing date and parties involved
- Agent and brokerage information

### Purchase Agreements
- Purchase price and earnest money
- Buyer and seller details
- Closing date and contingencies
- Agent information

### Income Verification
- Applicant and employer information
- Annual income and employment status
- Employment dates and verification details

## Configuration

### Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `AWS_REGION` | AWS region for Bedrock | `us-west-2` |
| `AWS_PROFILE` | AWS CLI profile | `default` |
| `BEDROCK_MODEL_ID` | Bedrock model identifier | `anthropic.claude-3-sonnet-20240229-v1:0` |
| `MAX_PAGES` | Maximum pages per document | `500` |
| `MAX_FILE_SIZE` | Maximum file size | `50MB` |
| `PROCESSING_TIMEOUT` | Processing timeout (seconds) | `300` |

### AWS Permissions

Required AWS permissions:
- `bedrock:InvokeModel` for the Claude Sonnet model
- Access to the specified AWS region

## Performance

- **Processing Time**: Reduced from 3-5 days to 1 day
- **Throughput**: Handles 150,000+ annual documents
- **Accuracy**: AI-powered classification and extraction
- **Scalability**: Batch processing with configurable batch sizes

## API Reference

### StrandsDocumentAgent

Main agent class for document processing workflows.

#### Methods

- `process_document_workflow(file_path)`: Process single document
- `batch_process_documents(file_paths)`: Process multiple documents
- `get_processing_statistics(results)`: Generate processing statistics

### DocumentProcessor

Handles document format conversion and quality enhancement.

#### Methods

- `process_document(file_path)`: Extract text from document
- `validate_document(file_path)`: Validate document before processing

### BedrockModel

AWS Bedrock integration for AI processing.

#### Methods

- `classify_document(text)`: Classify document type
- `extract_document_data(text, doc_type)`: Extract structured data

## Testing

Run tests with:
```bash
python -m pytest tests/
```

## Troubleshooting

### Common Issues

1. **AWS Authentication Errors:**
   - Verify AWS CLI configuration: `aws configure list`
   - Check AWS profile permissions for Bedrock access

2. **Model Access Errors:**
   - Ensure Claude Sonnet model is enabled in your AWS account
   - Verify the model ID in your configuration

3. **File Processing Errors:**
   - Check file format is supported
   - Verify file size is under 50MB limit
   - Ensure PDF has fewer than 500 pages

### Debug Mode

Enable debug mode in `.env`:
```
DEBUG=True
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Submit a pull request

## License

This project is licensed under the MIT License.

## Support

For support and questions:
- Check the troubleshooting section
- Review AWS Bedrock documentation
- Submit issues via the feedback form in the web interface
