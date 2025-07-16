"""
Streamlit web interface for StrandsDocumentProcessor
"""
import streamlit as st
import os
import json
import time
from datetime import datetime
import pandas as pd
from src.agents.document_agent import StrandsDocumentAgent
from src.agents.property_research_agent import PropertyResearchAgent
from src.agents.document_qa_agent import DocumentQAAgent
from src.config import Config

# Page configuration
st.set_page_config(
    page_title="Strands Document Processor",
    page_icon="📄",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    .success-box {
        padding: 1rem;
        border-radius: 0.5rem;
        background-color: #d4edda;
        border: 1px solid #c3e6cb;
        color: #155724;
        margin: 1rem 0;
    }
    .error-box {
        padding: 1rem;
        border-radius: 0.5rem;
        background-color: #f8d7da;
        border: 1px solid #f5c6cb;
        color: #721c24;
        margin: 1rem 0;
    }
    .info-box {
        padding: 1rem;
        border-radius: 0.5rem;
        background-color: #d1ecf1;
        border: 1px solid #bee5eb;
        color: #0c5460;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

def initialize_session_state():
    """Initialize session state variables"""
    if 'processing_results' not in st.session_state:
        st.session_state.processing_results = []
    if 'research_results' not in st.session_state:
        st.session_state.research_results = []
    if 'qa_results' not in st.session_state:
        st.session_state.qa_results = []
    if 'agent' not in st.session_state:
        st.session_state.agent = None
    if 'research_agent' not in st.session_state:
        st.session_state.research_agent = None
    if 'qa_agent' not in st.session_state:
        st.session_state.qa_agent = None
    if 'current_qa_document' not in st.session_state:
        st.session_state.current_qa_document = None
    if 'qa_conversation' not in st.session_state:
        st.session_state.qa_conversation = []

def create_agent():
    """Create and cache the document agent"""
    if st.session_state.agent is None:
        with st.spinner("Initializing AI agent..."):
            try:
                st.session_state.agent = StrandsDocumentAgent(aws_profile=Config.AWS_PROFILE)
                st.success("AI agent initialized successfully!")
            except Exception as e:
                st.error(f"Failed to initialize AI agent: {str(e)}")
                return None
    return st.session_state.agent

def create_research_agent():
    """Create and cache the property research agent"""
    if st.session_state.research_agent is None:
        with st.spinner("Initializing Property Research AI Agent..."):
            try:
                st.session_state.research_agent = PropertyResearchAgent(aws_profile=Config.AWS_PROFILE)
                st.success("Property Research AI Agent initialized successfully!")
            except Exception as e:
                st.error(f"Failed to initialize Property Research Agent: {str(e)}")
                return None
    return st.session_state.research_agent

def create_qa_agent():
    """Create and cache the document Q&A agent"""
    if st.session_state.qa_agent is None:
        with st.spinner("Initializing Document Q&A AI Agent..."):
            try:
                st.session_state.qa_agent = DocumentQAAgent(aws_profile=Config.AWS_PROFILE)
                st.success("Document Q&A AI Agent initialized successfully!")
            except Exception as e:
                st.error(f"Failed to initialize Document Q&A Agent: {str(e)}")
                return None
    return st.session_state.qa_agent

def save_uploaded_file(uploaded_file):
    """Save uploaded file to uploads directory"""
    uploads_dir = "uploads"
    os.makedirs(uploads_dir, exist_ok=True)
    
    # Create unique filename with timestamp
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"{timestamp}_{uploaded_file.name}"
    file_path = os.path.join(uploads_dir, filename)
    
    with open(file_path, "wb") as f:
        f.write(uploaded_file.getbuffer())
    
    return file_path

def display_processing_result(result):
    """Display processing result in a formatted way"""
    if result['success']:
        st.markdown('<div class="success-box">', unsafe_allow_html=True)
        st.write("✅ **Processing Successful**")
        st.markdown('</div>', unsafe_allow_html=True)
        
        final_result = result['final_result']
        
        # Document Information
        st.subheader("📋 Document Information")
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("Document Type", final_result.get('document_type', 'Unknown'))
        with col2:
            st.metric("Classification Confidence", f"{final_result.get('classification_confidence', 0):.2%}")
        with col3:
            st.metric("Extraction Confidence", f"{final_result.get('extraction_confidence', 0):.2%}")
        
        # Document Metadata
        with st.expander("📊 Document Metadata"):
            metadata = final_result.get('document_metadata', {})
            for key, value in metadata.items():
                st.write(f"**{key.replace('_', ' ').title()}:** {value}")
        
        # Extracted Data
        st.subheader("🔍 Extracted Data")
        extracted_data = final_result.get('extracted_data', {})
        
        if extracted_data:
            # Convert to DataFrame for better display
            data_items = []
            for key, value in extracted_data.items():
                if value is not None:
                    data_items.append({
                        'Field': key.replace('_', ' ').title(),
                        'Value': str(value)
                    })
            
            if data_items:
                df = pd.DataFrame(data_items)
                st.dataframe(df, use_container_width=True)
            else:
                st.info("No data could be extracted from this document.")
        else:
            st.info("No data could be extracted from this document.")
        
        # Processing Notes
        processing_notes = final_result.get('processing_notes', '')
        if processing_notes:
            with st.expander("📝 Processing Notes"):
                st.write(processing_notes)
        
        # Raw JSON (for debugging)
        with st.expander("🔧 Raw Processing Result (JSON)"):
            st.json(result)
    
    else:
        st.markdown('<div class="error-box">', unsafe_allow_html=True)
        st.write("❌ **Processing Failed**")
        st.write(f"**Error:** {result.get('error', 'Unknown error')}")
        st.markdown('</div>', unsafe_allow_html=True)

def display_property_research_result(result):
    """Display property research result in a comprehensive format"""
    if result['success']:
        st.markdown('<div class="success-box">', unsafe_allow_html=True)
        st.write("✅ **Property Research Completed Successfully**")
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Processing time
        processing_time = result.get('processing_time', 0)
        st.write(f"⏱️ **Total Processing Time:** {processing_time:.2f} seconds")
        
        # Property Summary
        st.header("🏠 Property Summary")
        report = result.get('comprehensive_report', {})
        property_summary = report.get('property_summary', {})
        
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Sale Price", f"${property_summary.get('sale_price', 0):,}")
        with col2:
            st.metric("Current Est. Value", f"${property_summary.get('estimated_current_value', 0):,}")
        with col3:
            st.metric("Property Type", property_summary.get('property_type', 'N/A'))
        with col4:
            st.metric("Closing Date", property_summary.get('closing_date', 'N/A'))
        
        # Address
        st.write(f"📍 **Address:** {property_summary.get('address', 'N/A')}")
        
        # Financial Analysis
        st.header("💰 Financial Analysis")
        financial_analysis = report.get('financial_analysis', {})
        
        col1, col2, col3 = st.columns(3)
        with col1:
            value_change = financial_analysis.get('value_change', {})
            change_amount = value_change.get('amount', 0)
            change_pct = value_change.get('percentage', 0)
            direction = value_change.get('direction', 'unknown')
            
            delta_color = "normal" if direction == "increase" else "inverse" if direction == "decrease" else "off"
            st.metric(
                "Value Change", 
                f"${change_amount:,.0f}",
                delta=f"{change_pct:+.1f}%",
                delta_color=delta_color
            )
        
        with col2:
            st.metric("Commission Paid", f"${financial_analysis.get('commission_paid', 0):,}")
        
        with col3:
            st.metric("Price per Sq Ft", f"${financial_analysis.get('price_per_sqft', 0):.0f}")
        
        # Market Analysis
        st.header("📊 Market Analysis")
        market_analysis = report.get('market_analysis', {})
        
        col1, col2 = st.columns(2)
        with col1:
            st.subheader("Market Trends")
            market_trends = market_analysis.get('market_trends', {})
            for key, value in market_trends.items():
                st.write(f"**{key.replace('_', ' ').title()}:** {value}")
        
        with col2:
            st.subheader("Market Metrics")
            st.metric("Days on Market", market_analysis.get('days_on_market', 0))
            st.write(f"**Market Temperature:** {market_analysis.get('market_temperature', 'N/A')}")
        
        # Comparable Properties
        comparable_properties = market_analysis.get('comparable_properties', [])
        if comparable_properties:
            st.subheader("🏘️ Comparable Properties")
            comp_data = []
            for comp in comparable_properties:
                if 'error' not in comp:
                    comp_data.append({
                        'Address': comp.get('address', 'N/A'),
                        'Sale Price': f"${comp.get('sale_price', 0):,}",
                        'Sale Date': comp.get('sale_date', 'N/A'),
                        'Sq Ft': f"{comp.get('square_footage', 0):,}",
                        'Bed/Bath': f"{comp.get('bedrooms', 0)}/{comp.get('bathrooms', 0)}",
                        'Distance': f"{comp.get('distance_miles', 0):.1f} mi"
                    })
            
            if comp_data:
                comp_df = pd.DataFrame(comp_data)
                st.dataframe(comp_df, use_container_width=True)
        
        # Neighborhood Analysis
        st.header("🏘️ Neighborhood Analysis")
        neighborhood_analysis = report.get('neighborhood_analysis', {})
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Walkability Score", f"{neighborhood_analysis.get('walkability_score', 0)}/100")
        with col2:
            st.metric("Transit Score", f"{neighborhood_analysis.get('transit_score', 0)}/100")
        with col3:
            st.metric("Bike Score", f"{neighborhood_analysis.get('bike_score', 0)}/100")
        
        # Nearby Amenities
        amenities = neighborhood_analysis.get('nearby_amenities', [])
        if amenities:
            st.subheader("🏪 Nearby Amenities")
            for amenity in amenities:
                st.write(f"• {amenity}")
        
        # School Information
        school_info = neighborhood_analysis.get('school_information', {})
        if school_info:
            st.subheader("🎓 School Information")
            
            col1, col2 = st.columns(2)
            with col1:
                st.write(f"**School District:** {school_info.get('school_district', 'N/A')}")
                st.metric("District Rating", f"{school_info.get('district_rating', 0)}/10")
            
            with col2:
                # Display schools by type
                for school_type in ['elementary_schools', 'middle_schools', 'high_schools']:
                    schools = school_info.get(school_type, [])
                    if schools:
                        st.write(f"**{school_type.replace('_', ' ').title()}:**")
                        for school in schools:
                            st.write(f"• {school.get('name', 'N/A')} - Rating: {school.get('rating', 0)}/10")
        
        # Crime Statistics
        crime_stats = neighborhood_analysis.get('crime_statistics', {})
        if crime_stats:
            st.subheader("🚔 Safety Information")
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Overall Crime Rate", f"{crime_stats.get('overall_crime_rate', 0)}/1000")
            with col2:
                st.metric("Safety Score", f"{crime_stats.get('safety_score', 0)}/100")
            with col3:
                st.write("**Recent Incidents:**")
                incidents = crime_stats.get('recent_incidents', [])
                for incident in incidents[:3]:  # Show first 3
                    st.write(f"• {incident.get('type', 'N/A')} ({incident.get('distance', 'N/A')})")
        
        # AI Insights
        st.header("🤖 AI Insights & Analysis")
        ai_insights = result.get('ai_insights', {})
        
        if ai_insights.get('success', False):
            # Investment Analysis
            investment_analysis = ai_insights.get('investment_analysis', {})
            if investment_analysis:
                st.subheader("📈 Investment Analysis")
                col1, col2 = st.columns(2)
                with col1:
                    st.write(f"**ROI Potential:** {investment_analysis.get('roi_potential', 'N/A')}")
                    st.write(f"**Investment Grade:** {investment_analysis.get('investment_grade', 'N/A')}")
                with col2:
                    st.write(f"**Appreciation Outlook:** {investment_analysis.get('appreciation_outlook', 'N/A')}")
                    st.write(f"**Rental Potential:** {investment_analysis.get('rental_potential', 'N/A')}")
            
            # Risk Assessment
            risk_assessment = ai_insights.get('risk_assessment', {})
            if risk_assessment:
                st.subheader("⚠️ Risk Assessment")
                st.write(f"**Overall Risk Level:** {risk_assessment.get('overall_risk_level', 'N/A')}")
                
                col1, col2 = st.columns(2)
                with col1:
                    market_risks = risk_assessment.get('market_risks', [])
                    if market_risks:
                        st.write("**Market Risks:**")
                        for risk in market_risks:
                            st.write(f"• {risk}")
                
                with col2:
                    property_risks = risk_assessment.get('property_risks', [])
                    if property_risks:
                        st.write("**Property Risks:**")
                        for risk in property_risks:
                            st.write(f"• {risk}")
            
            # Recommendations
            recommendations = ai_insights.get('recommendations', [])
            if recommendations:
                st.subheader("💡 AI Recommendations")
                for i, recommendation in enumerate(recommendations, 1):
                    st.write(f"{i}. {recommendation}")
        
        else:
            st.warning("AI insights generation encountered issues. Basic analysis completed.")
        
        # Workflow Steps
        with st.expander("🔍 Processing Workflow Details"):
            workflow_steps = result.get('workflow_steps', [])
            for step in workflow_steps:
                status_icon = "✅" if step.get('status') == 'completed' else "❌"
                st.write(f"{status_icon} **{step.get('step', 'Unknown').replace('_', ' ').title()}**")
        
        # Raw Data (for debugging)
        with st.expander("🔧 Raw Research Result (JSON)"):
            st.json(result)
    
    else:
        st.markdown('<div class="error-box">', unsafe_allow_html=True)
        st.write("❌ **Property Research Failed**")
        st.write(f"**Error:** {result.get('error', 'Unknown error')}")
        st.markdown('</div>', unsafe_allow_html=True)

def display_qa_document_load_result(result):
    """Display document loading result for Q&A"""
    if result['success']:
        st.markdown('<div class="success-box">', unsafe_allow_html=True)
        st.write("✅ **Document Loaded Successfully**")
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Document Information
        doc_info = result.get('document_info', {})
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("Text Length", f"{doc_info.get('text_length', 0):,} chars")
        with col2:
            st.metric("Text Chunks", doc_info.get('chunks_count', 0))
        with col3:
            processing_time = result.get('processing_time', 0)
            st.metric("Processing Time", f"{processing_time:.2f}s")
        
        # Document Preview
        preview = doc_info.get('preview', '')
        if preview:
            with st.expander("📄 Document Preview"):
                st.text_area("First 500 characters:", preview, height=150, disabled=True)
        
        # Document Summary
        summary_result = result.get('document_summary', {})
        if summary_result.get('success') and summary_result.get('summary'):
            st.subheader("📋 Document Summary")
            st.write(summary_result['summary'])
        
    else:
        st.markdown('<div class="error-box">', unsafe_allow_html=True)
        st.write("❌ **Document Loading Failed**")
        st.write(f"**Error:** {result.get('error', 'Unknown error')}")
        st.markdown('</div>', unsafe_allow_html=True)

def display_qa_answer(result):
    """Display Q&A answer result"""
    if result['success']:
        answer_result = result.get('answer_result', {})
        
        # Question
        st.markdown(f"**❓ Question:** {result.get('question', 'N/A')}")
        
        # Answer
        st.markdown("**🤖 Answer:**")
        st.write(answer_result.get('answer', 'No answer provided'))
        
        # Confidence and metadata
        col1, col2, col3 = st.columns(3)
        with col1:
            confidence = answer_result.get('confidence', 0)
            st.metric("Confidence", f"{confidence:.1%}")
        with col2:
            chunks_used = answer_result.get('chunk_count_used', 0)
            st.metric("Sources Used", chunks_used)
        with col3:
            processing_time = result.get('processing_time', 0)
            st.metric("Response Time", f"{processing_time:.2f}s")
        
        # Reasoning
        reasoning = answer_result.get('reasoning', '')
        if reasoning:
            with st.expander("🧠 AI Reasoning"):
                st.write(reasoning)
        
        # Relevant chunks/sources
        relevant_chunks = answer_result.get('relevant_chunks', [])
        if relevant_chunks:
            with st.expander(f"📚 Source Context ({len(relevant_chunks)} chunks)"):
                for i, chunk in enumerate(relevant_chunks, 1):
                    st.write(f"**Source {i} (Score: {chunk.get('relevance_score', 0):.1f}):**")
                    st.write(chunk.get('text', 'No text available'))
                    if chunk.get('matched_keywords'):
                        st.write(f"*Keywords: {', '.join(chunk['matched_keywords'])}*")
                    st.write("---")
    
    else:
        st.markdown('<div class="error-box">', unsafe_allow_html=True)
        st.write("❌ **Question Answering Failed**")
        st.write(f"**Error:** {result.get('error', 'Unknown error')}")
        st.markdown('</div>', unsafe_allow_html=True)

def main():
    """Main application function"""
    initialize_session_state()
    
    # Header
    st.markdown('<h1 class="main-header">📄 Real Estate Document Processor with AI Agents</h1>', unsafe_allow_html=True)
    st.markdown('<div class="info-box">AI-powered document processing with Property Research and Document Q&A using AWS Strands AI</div>', unsafe_allow_html=True)
    
    # Sidebar
    with st.sidebar:
        st.header("⚙️ Configuration")
        
        # AWS Profile selection
        aws_profile = st.selectbox(
            "AWS Profile",
            options=["default", "custom"],
            index=0,
            help="Select AWS profile for Bedrock authentication"
        )
        
        # Document type filter
        st.header("📋 Document Types")
        st.write("Supported document types:")
        for doc_type in Config.DOCUMENT_TYPES:
            st.write(f"• {doc_type.replace('_', ' ').title()}")
        
        # Processing statistics
        if st.session_state.processing_results or st.session_state.research_results or st.session_state.qa_conversation:
            st.header("📊 Session Statistics")
            
            # Document processing stats
            if st.session_state.processing_results:
                total_processed = len(st.session_state.processing_results)
                successful = sum(1 for r in st.session_state.processing_results if r['success'])
                st.subheader("Document Processing")
                st.metric("Documents Processed", total_processed)
                st.metric("Success Rate", f"{(successful/total_processed*100):.1f}%")
            
            # Property research stats
            if st.session_state.research_results:
                total_researched = len(st.session_state.research_results)
                successful_research = sum(1 for r in st.session_state.research_results if r['success'])
                st.subheader("Property Research")
                st.metric("Properties Researched", total_researched)
                st.metric("Research Success Rate", f"{(successful_research/total_researched*100):.1f}%")
            
            # Q&A stats
            if st.session_state.qa_conversation:
                total_questions = len(st.session_state.qa_conversation)
                successful_qa = sum(1 for q in st.session_state.qa_conversation if q['result']['success'])
                st.subheader("Document Q&A")
                st.metric("Questions Asked", total_questions)
                st.metric("Q&A Success Rate", f"{(successful_qa/total_questions*100):.1f}%")
                
                if st.session_state.current_qa_document:
                    st.write(f"**Current Doc:** {st.session_state.current_qa_document['file_name'][:20]}...")
    
    # Main content
    tab1, tab2, tab3, tab4, tab5 = st.tabs(["📤 Upload & Process", "🔍 Property Research", "💬 Document Q&A", "📊 Batch Processing", "❓ Help & Feedback"])
    
    with tab1:
        st.header("Single Document Processing")
        
        # File upload
        uploaded_file = st.file_uploader(
            "Choose a document file",
            type=['pdf', 'png', 'jpg', 'jpeg', 'tiff'],
            help=f"Supported formats: {', '.join(Config.SUPPORTED_FORMATS)}"
        )
        
        if uploaded_file is not None:
            # Display file info
            st.write(f"**File:** {uploaded_file.name}")
            st.write(f"**Size:** {uploaded_file.size / 1024 / 1024:.2f} MB")
            
            # Process button
            if st.button("🚀 Process Document", type="primary"):
                agent = create_agent()
                if agent is None:
                    st.error("Cannot process document: AI agent initialization failed")
                    return
                
                try:
                    # Save uploaded file
                    file_path = save_uploaded_file(uploaded_file)
                    
                    # Process document
                    with st.spinner("Processing document... This may take a few moments."):
                        start_time = time.time()
                        result = agent.process_document_workflow(file_path)
                        processing_time = time.time() - start_time
                        
                        # Add processing time to result
                        if result['success']:
                            result['final_result']['processing_time_seconds'] = processing_time
                    
                    # Store result
                    st.session_state.processing_results.append(result)
                    
                    # Display result
                    display_processing_result(result)
                    
                    # Clean up uploaded file
                    try:
                        os.remove(file_path)
                    except:
                        pass
                        
                except Exception as e:
                    st.error(f"Processing failed: {str(e)}")
    
    with tab2:
        st.header("🔍 Property Research with Agentic AI")
        st.markdown("""
        <div class="info-box">
        <strong>🤖 Agentic AI Property Research</strong><br>
        Upload a settlement document and our AI agent will:
        <ul>
        <li>📄 Process and extract property details from the document</li>
        <li>🌐 Search the web for current market information</li>
        <li>📊 Analyze market trends and comparable properties</li>
        <li>🏘️ Research neighborhood information and amenities</li>
        <li>🎓 Find school ratings and district information</li>
        <li>🚔 Provide safety and crime statistics</li>
        <li>💡 Generate AI-powered investment insights and recommendations</li>
        </ul>
        </div>
        """, unsafe_allow_html=True)
        
        # File upload for property research
        research_file = st.file_uploader(
            "Upload Settlement Document for Property Research",
            type=['pdf', 'png', 'jpg', 'jpeg', 'tiff'],
            help="Upload a settlement document to research the property",
            key="research_uploader"
        )
        
        if research_file is not None:
            # Display file info
            st.write(f"**File:** {research_file.name}")
            st.write(f"**Size:** {research_file.size / 1024 / 1024:.2f} MB")
            
            # Research options
            st.subheader("🔧 Research Options")
            col1, col2 = st.columns(2)
            
            with col1:
                include_market_analysis = st.checkbox("Include Market Analysis", value=True)
                include_neighborhood_info = st.checkbox("Include Neighborhood Information", value=True)
                include_school_info = st.checkbox("Include School Information", value=True)
            
            with col2:
                include_crime_stats = st.checkbox("Include Crime Statistics", value=True)
                include_ai_insights = st.checkbox("Generate AI Insights", value=True)
                include_investment_analysis = st.checkbox("Include Investment Analysis", value=True)
            
            # Process button
            if st.button("🚀 Start Property Research", type="primary", key="research_button"):
                research_agent = create_research_agent()
                if research_agent is None:
                    st.error("Cannot start property research: AI agent initialization failed")
                    return
                
                try:
                    # Save uploaded file
                    file_path = save_uploaded_file(research_file)
                    
                    # Show agent capabilities
                    with st.expander("🤖 Agent Capabilities"):
                        capabilities = research_agent.get_agent_capabilities()
                        st.write(f"**Agent Name:** {capabilities['name']}")
                        st.write(f"**Description:** {capabilities['description']}")
                        st.write("**Capabilities:**")
                        for capability in capabilities['capabilities']:
                            st.write(f"• {capability}")
                    
                    # Process with progress tracking
                    progress_container = st.container()
                    with progress_container:
                        st.write("🔄 **Processing Status:**")
                        progress_bar = st.progress(0)
                        status_text = st.empty()
                        
                        # Step-by-step progress updates
                        status_text.text("🔍 Step 1/5: Processing settlement document...")
                        progress_bar.progress(20)
                        time.sleep(1)  # Brief pause for UI update
                        
                        status_text.text("📍 Step 2/5: Extracting property information...")
                        progress_bar.progress(40)
                        
                        status_text.text("🌐 Step 3/5: Searching web for property data...")
                        progress_bar.progress(60)
                        
                        status_text.text("🤖 Step 4/5: Generating AI insights...")
                        progress_bar.progress(80)
                        
                        status_text.text("📊 Step 5/5: Compiling comprehensive report...")
                        progress_bar.progress(100)
                        
                        # Perform actual research
                        start_time = time.time()
                        result = research_agent.research_property_workflow(file_path)
                        processing_time = time.time() - start_time
                        
                        status_text.text(f"✅ Research completed in {processing_time:.2f} seconds!")
                    
                    # Store result
                    st.session_state.research_results.append(result)
                    
                    # Display comprehensive results
                    st.markdown("---")
                    display_property_research_result(result)
                    
                    # Clean up uploaded file
                    try:
                        os.remove(file_path)
                    except:
                        pass
                        
                except Exception as e:
                    st.error(f"Property research failed: {str(e)}")
                    import traceback
                    st.error(f"Detailed error: {traceback.format_exc()}")
        
        # Research History
        if st.session_state.research_results:
            st.markdown("---")
            st.subheader("📚 Research History")
            
            # Summary statistics
            total_researched = len(st.session_state.research_results)
            successful_research = sum(1 for r in st.session_state.research_results if r['success'])
            
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Properties Researched", total_researched)
            with col2:
                st.metric("Successful Research", successful_research)
            with col3:
                success_rate = (successful_research / total_researched * 100) if total_researched > 0 else 0
                st.metric("Success Rate", f"{success_rate:.1f}%")
            
            # Recent research results
            with st.expander("📋 Recent Research Results"):
                for i, result in enumerate(reversed(st.session_state.research_results[-5:]), 1):
                    if result['success']:
                        report = result.get('comprehensive_report', {})
                        property_summary = report.get('property_summary', {})
                        st.write(f"**{i}.** {property_summary.get('address', 'Unknown Address')} - "
                                f"${property_summary.get('sale_price', 0):,} "
                                f"({property_summary.get('closing_date', 'Unknown Date')})")
                    else:
                        st.write(f"**{i}.** Research failed: {result.get('error', 'Unknown error')}")
    
    with tab3:
        st.header("💬 Document Q&A with RAG")
        st.markdown("""
        <div class="info-box">
        <strong>🤖 Intelligent Document Q&A</strong><br>
        Upload any document and ask questions about its content using RAG (Retrieval-Augmented Generation):
        <ul>
        <li>📄 Load and process documents (PDF, images)</li>
        <li>🔍 Intelligent text chunking and retrieval</li>
        <li>💬 Ask natural language questions</li>
        <li>🎯 Get accurate answers with source citations</li>
        <li>📚 Maintain conversation context</li>
        <li>📋 Generate document summaries</li>
        </ul>
        </div>
        """, unsafe_allow_html=True)
        
        # Document loading section
        st.subheader("📄 Step 1: Load Document")
        
        # Check if document is already loaded
        if st.session_state.current_qa_document:
            st.success(f"✅ Document loaded: {st.session_state.current_qa_document.get('file_name', 'Unknown')}")
            
            col1, col2 = st.columns([3, 1])
            with col1:
                st.write(f"**Chunks:** {st.session_state.current_qa_document.get('chunks_count', 0)}")
                st.write(f"**Text Length:** {st.session_state.current_qa_document.get('text_length', 0):,} characters")
            with col2:
                if st.button("🗑️ Clear Document", key="clear_qa_doc"):
                    st.session_state.current_qa_document = None
                    st.session_state.qa_conversation = []
                    qa_agent = st.session_state.get('qa_agent')
                    if qa_agent:
                        qa_agent.rag_tool.clear_document()
                        qa_agent.clear_conversation()
                    st.rerun()
        
        # File upload for Q&A
        qa_file = st.file_uploader(
            "Upload Document for Q&A",
            type=['pdf', 'png', 'jpg', 'jpeg', 'tiff'],
            help="Upload any document to ask questions about its content",
            key="qa_uploader"
        )
        
        if qa_file is not None and not st.session_state.current_qa_document:
            st.write(f"**File:** {qa_file.name}")
            st.write(f"**Size:** {qa_file.size / 1024 / 1024:.2f} MB")
            
            if st.button("📚 Load Document for Q&A", type="primary", key="load_qa_doc"):
                qa_agent = create_qa_agent()
                if qa_agent is None:
                    st.error("Cannot load document: Q&A agent initialization failed")
                else:
                    try:
                        # Save uploaded file
                        file_path = save_uploaded_file(qa_file)
                        
                        # Load document
                        with st.spinner("Loading document for Q&A..."):
                            result = qa_agent.load_document_workflow(file_path)
                        
                        # Display result
                        display_qa_document_load_result(result)
                        
                        if result['success']:
                            # Store document info in session state
                            st.session_state.current_qa_document = {
                                'file_name': qa_file.name,
                                'file_path': file_path,
                                'chunks_count': result['document_info'].get('chunks_count', 0),
                                'text_length': result['document_info'].get('text_length', 0),
                                'load_result': result
                            }
                            st.rerun()
                        
                        # Clean up uploaded file
                        try:
                            os.remove(file_path)
                        except:
                            pass
                            
                    except Exception as e:
                        st.error(f"Document loading failed: {str(e)}")
        
        # Q&A section (only show if document is loaded)
        if st.session_state.current_qa_document:
            st.markdown("---")
            st.subheader("💬 Step 2: Ask Questions")
            
            # Get Q&A agent
            qa_agent = st.session_state.get('qa_agent')
            if qa_agent:
                # Suggested questions
                suggested_questions = qa_agent.get_suggested_questions()
                if suggested_questions:
                    st.write("**💡 Suggested Questions:**")
                    cols = st.columns(2)
                    for i, suggestion in enumerate(suggested_questions):
                        col_idx = i % 2
                        with cols[col_idx]:
                            if st.button(f"❓ {suggestion}", key=f"suggest_{i}"):
                                st.session_state.current_question = suggestion
                
                # Question input
                question = st.text_input(
                    "Ask a question about the document:",
                    value=st.session_state.get('current_question', ''),
                    placeholder="e.g., What is the main topic of this document?",
                    key="qa_question_input"
                )
                
                # Clear current question after use
                if 'current_question' in st.session_state:
                    del st.session_state.current_question
                
                col1, col2, col3 = st.columns([2, 1, 1])
                with col1:
                    ask_button = st.button("🤖 Ask Question", type="primary", disabled=not question.strip())
                with col2:
                    include_context = st.checkbox("Use Context", value=True, help="Include conversation history for better answers")
                with col3:
                    if st.button("🗑️ Clear Chat"):
                        st.session_state.qa_conversation = []
                        qa_agent.clear_conversation()
                        st.rerun()
                
                # Process question
                if ask_button and question.strip():
                    try:
                        with st.spinner("Generating answer..."):
                            result = qa_agent.ask_question_workflow(question, include_context=include_context)
                        
                        # Store in conversation
                        st.session_state.qa_conversation.append({
                            'question': question,
                            'result': result,
                            'timestamp': time.time()
                        })
                        
                        # Display answer
                        display_qa_answer(result)
                        
                    except Exception as e:
                        st.error(f"Question answering failed: {str(e)}")
                
                # Conversation history
                if st.session_state.qa_conversation:
                    st.markdown("---")
                    st.subheader("💬 Conversation History")
                    
                    # Show recent conversations (last 5)
                    recent_conversations = st.session_state.qa_conversation[-5:]
                    
                    for i, conv in enumerate(reversed(recent_conversations), 1):
                        with st.expander(f"Q{len(recent_conversations)-i+1}: {conv['question'][:50]}..."):
                            display_qa_answer(conv['result'])
                    
                    # Conversation statistics
                    if len(st.session_state.qa_conversation) > 5:
                        st.info(f"Showing last 5 of {len(st.session_state.qa_conversation)} questions. Use 'Clear Chat' to reset.")
        
        else:
            st.info("👆 Please load a document first to start asking questions.")
    
    with tab4:
        st.header("Batch Document Processing")
        st.info("Upload multiple documents for batch processing")
        
        # Multiple file upload
        uploaded_files = st.file_uploader(
            "Choose multiple document files",
            type=['pdf', 'png', 'jpg', 'jpeg', 'tiff'],
            accept_multiple_files=True,
            help="Select multiple files for batch processing"
        )
        
        if uploaded_files:
            st.write(f"Selected {len(uploaded_files)} files for batch processing")
            
            # Show file list
            with st.expander("📁 Selected Files"):
                for file in uploaded_files:
                    st.write(f"• {file.name} ({file.size / 1024 / 1024:.2f} MB)")
            
            if st.button("🚀 Process Batch", type="primary"):
                agent = create_agent()
                if agent is None:
                    st.error("Cannot process documents: AI agent initialization failed")
                    return
                
                try:
                    # Save all files
                    file_paths = []
                    for uploaded_file in uploaded_files:
                        file_path = save_uploaded_file(uploaded_file)
                        file_paths.append(file_path)
                    
                    # Process batch
                    progress_bar = st.progress(0)
                    status_text = st.empty()
                    
                    results = []
                    for i, file_path in enumerate(file_paths):
                        status_text.text(f"Processing {i+1}/{len(file_paths)}: {os.path.basename(file_path)}")
                        progress_bar.progress((i + 1) / len(file_paths))
                        
                        result = agent.process_document_workflow(file_path)
                        results.append(result)
                        st.session_state.processing_results.append(result)
                    
                    status_text.text("Batch processing completed!")
                    
                    # Display batch statistics
                    stats = agent.get_processing_statistics(results)
                    
                    st.subheader("📊 Batch Processing Results")
                    col1, col2, col3, col4 = st.columns(4)
                    
                    with col1:
                        st.metric("Total Documents", stats['total_documents'])
                    with col2:
                        st.metric("Successful", stats['successful_processing'])
                    with col3:
                        st.metric("Failed", stats['failed_processing'])
                    with col4:
                        st.metric("Success Rate", f"{stats['success_rate']:.1f}%")
                    
                    # Document type distribution
                    if stats['document_type_distribution']:
                        st.subheader("📋 Document Type Distribution")
                        type_df = pd.DataFrame(
                            list(stats['document_type_distribution'].items()),
                            columns=['Document Type', 'Count']
                        )
                        st.bar_chart(type_df.set_index('Document Type'))
                    
                    # Clean up files
                    for file_path in file_paths:
                        try:
                            os.remove(file_path)
                        except:
                            pass
                            
                except Exception as e:
                    st.error(f"Batch processing failed: {str(e)}")
    
    with tab5:
        st.header("Help & User Feedback")
        
        # Help section
        st.subheader("📖 How to Use")
        st.write("""
        1. **Single Document Processing**: Upload one document at a time for detailed processing
        2. **Property Research**: Upload settlement documents for comprehensive property research with AI insights
        3. **Document Q&A (NEW!)**: Upload any document and ask questions about its content using RAG
        4. **Batch Processing**: Upload multiple documents for efficient bulk processing
        5. **Supported Formats**: PDF, PNG, JPG, JPEG, TIFF
        6. **Maximum File Size**: 50MB per document
        7. **Maximum Pages**: 500 pages per PDF document
        """)
        
        st.subheader("🎯 Document Types")
        st.write("""
        The system can automatically classify and extract data from:
        - **Settlement Documents**: Property sales, commissions, closing details
        - **Purchase Agreements**: Purchase terms, buyer/seller information
        - **Income Verification**: Employment and income details
        """)
        
        st.subheader("💬 Document Q&A Features")
        st.write("""
        Our new **Document Q&A with RAG** feature provides:
        - **Smart Document Loading**: Processes and chunks documents for optimal retrieval
        - **Natural Language Questions**: Ask questions in plain English about document content
        - **Accurate Answers**: RAG-based responses with source citations and confidence scores
        - **Conversation Context**: Maintains context across multiple questions
        - **Suggested Questions**: AI-generated relevant questions based on document content
        - **Source Attribution**: Shows which parts of the document were used to answer questions
        - **Document Summaries**: Automatic generation of document overviews
        """)
        
        st.subheader("🔍 Property Research Features")
        st.write("""
        Our **Agentic AI Property Research** feature provides:
        - **Document Processing**: Extracts property details from settlement documents
        - **Web Research**: Searches multiple sources for current market data
        - **Market Analysis**: Compares property value to market trends and comparable sales
        - **Neighborhood Intelligence**: Walkability, transit scores, amenities, demographics
        - **School Information**: Ratings, districts, and nearby schools
        - **Safety Data**: Crime statistics and safety scores
        - **AI Insights**: Investment analysis, risk assessment, and recommendations
        - **Comprehensive Reports**: All data compiled into actionable insights
        """)
        
        st.subheader("🤖 AI Agent Capabilities")
        st.write("""
        The system uses **AWS Strands AI** with multiple specialized agents:
        - **Document Agent**: Processes documents with Claude Sonnet on Amazon Bedrock
        - **Property Research Agent**: Orchestrates comprehensive property analysis
        - **Document Q&A Agent**: Provides intelligent question-answering with RAG
        - **Web Search Tool**: Gathers real-time property and market information
        - **RAG Tool**: Enables accurate document-based question answering
        """)
        
        # User feedback section
        st.subheader("💬 User Feedback")
        st.write("Help us improve the document processor by sharing your feedback!")
        
        with st.form("feedback_form"):
            # Additional document types
            st.write("**What additional document types would you like to see supported?**")
            additional_doc_types = st.text_area(
                "Document Types",
                placeholder="e.g., Loan applications, Property appraisals, Insurance documents..."
            )
            
            # Additional extraction fields
            st.write("**What additional data fields would you like to extract?**")
            additional_fields = st.text_area(
                "Extraction Fields",
                placeholder="e.g., Property tax information, HOA fees, Inspection details..."
            )
            
            # General feedback
            st.write("**General feedback or suggestions:**")
            general_feedback = st.text_area(
                "Feedback",
                placeholder="Share your experience, suggestions for improvement, or any issues you encountered..."
            )
            
            submitted = st.form_submit_button("📤 Submit Feedback")
            
            if submitted:
                # In a real application, you would save this feedback to a database
                st.success("Thank you for your feedback! Your input helps us improve the system.")
                
                # Display feedback summary
                with st.expander("📋 Your Feedback Summary"):
                    if additional_doc_types:
                        st.write(f"**Additional Document Types:** {additional_doc_types}")
                    if additional_fields:
                        st.write(f"**Additional Fields:** {additional_fields}")
                    if general_feedback:
                        st.write(f"**General Feedback:** {general_feedback}")

if __name__ == "__main__":
    main()
