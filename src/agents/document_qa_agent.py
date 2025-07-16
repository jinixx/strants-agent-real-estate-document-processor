"""
Document Q&A Agent using RAG (Retrieval-Augmented Generation)
"""
from typing import Dict, Any, List, Optional
import time
from src.tools.rag_tool import DocumentRAGTool
from src.config import Config

class DocumentQAAgent:
    """
    Agent for document question-answering using RAG approach
    """
    
    def __init__(self, aws_profile: Optional[str] = None):
        """
        Initialize the Document Q&A Agent
        
        Args:
            aws_profile: AWS profile name for authentication
        """
        self.rag_tool = DocumentRAGTool(aws_profile=aws_profile)
        self.name = "DocumentQAAgent"
        self.description = "AI agent for answering questions about documents using RAG"
        self.capabilities = [
            "Document loading and processing",
            "Intelligent text chunking and retrieval",
            "Question answering with context",
            "Document summarization",
            "Multi-turn conversations about documents"
        ]
        
        # Conversation history
        self.conversation_history = []
    
    def load_document_workflow(self, file_path: str) -> Dict[str, Any]:
        """
        Complete workflow for loading a document for Q&A
        
        Args:
            file_path: Path to the document file
            
        Returns:
            Loading result with document information
        """
        workflow_result = {
            'file_path': file_path,
            'agent_name': self.name,
            'workflow_steps': [],
            'document_info': {},
            'document_summary': {},
            'success': False,
            'error': None,
            'processing_time': 0
        }
        
        start_time = time.time()
        
        try:
            # Step 1: Load and process document
            print("📄 Step 1: Loading and processing document...")
            load_result = self.rag_tool.load_document(file_path)
            workflow_result['workflow_steps'].append({
                'step': 'document_loading',
                'status': 'completed' if load_result['success'] else 'failed',
                'result': load_result
            })
            
            if not load_result['success']:
                workflow_result['error'] = f"Document loading failed: {load_result.get('error', 'Unknown error')}"
                return workflow_result
            
            workflow_result['document_info'] = load_result
            
            # Step 2: Generate document summary
            print("📋 Step 2: Generating document summary...")
            summary_result = self.rag_tool.get_document_summary()
            workflow_result['workflow_steps'].append({
                'step': 'document_summary',
                'status': 'completed' if summary_result['success'] else 'failed',
                'result': summary_result
            })
            
            workflow_result['document_summary'] = summary_result
            
            # Clear conversation history for new document
            self.conversation_history = []
            
            workflow_result['success'] = True
            print("✅ Document loaded successfully and ready for Q&A!")
            
        except Exception as e:
            workflow_result['error'] = f"Workflow failed: {str(e)}"
            print(f"❌ Workflow error: {str(e)}")
        
        finally:
            workflow_result['processing_time'] = time.time() - start_time
        
        return workflow_result
    
    def ask_question_workflow(self, question: str, include_context: bool = True) -> Dict[str, Any]:
        """
        Complete workflow for answering a question about the loaded document
        
        Args:
            question: User's question
            include_context: Whether to include conversation context
            
        Returns:
            Answer result with context and confidence
        """
        workflow_result = {
            'question': question,
            'agent_name': self.name,
            'workflow_steps': [],
            'answer_result': {},
            'conversation_context': [],
            'success': False,
            'error': None,
            'processing_time': 0
        }
        
        start_time = time.time()
        
        try:
            # Check if document is loaded
            doc_info = self.rag_tool.get_document_info()
            if not doc_info['loaded']:
                workflow_result['error'] = "No document loaded. Please load a document first."
                return workflow_result
            
            # Step 1: Process question and retrieve relevant context
            print(f"🔍 Step 1: Processing question: '{question}'")
            
            # Enhance question with conversation context if requested
            enhanced_question = self._enhance_question_with_context(question) if include_context else question
            
            # Step 2: Answer the question using RAG
            print("🤖 Step 2: Generating answer using RAG...")
            answer_result = self.rag_tool.ask_question(enhanced_question)
            workflow_result['workflow_steps'].append({
                'step': 'question_answering',
                'status': 'completed' if answer_result['success'] else 'failed',
                'result': answer_result
            })
            
            if not answer_result['success']:
                workflow_result['error'] = f"Question answering failed: {answer_result.get('error', 'Unknown error')}"
                return workflow_result
            
            workflow_result['answer_result'] = answer_result
            
            # Step 3: Update conversation history
            self._update_conversation_history(question, answer_result['answer'])
            workflow_result['conversation_context'] = self.conversation_history[-5:]  # Last 5 exchanges
            
            workflow_result['success'] = True
            print("✅ Question answered successfully!")
            
        except Exception as e:
            workflow_result['error'] = f"Workflow failed: {str(e)}"
            print(f"❌ Workflow error: {str(e)}")
        
        finally:
            workflow_result['processing_time'] = time.time() - start_time
        
        return workflow_result
    
    def get_suggested_questions(self) -> List[str]:
        """
        Generate suggested questions based on the loaded document
        
        Returns:
            List of suggested questions
        """
        doc_info = self.rag_tool.get_document_info()
        if not doc_info['loaded']:
            return []
        
        # Basic suggested questions for real estate documents
        suggestions = [
            "What is the property address?",
            "What is the sale price?",
            "Who are the buyer and seller?",
            "When is the closing date?",
            "What is the commission amount?",
            "Are there any contingencies mentioned?",
            "What are the key terms of this agreement?",
            "What fees are mentioned in the document?",
            "Are there any special conditions?",
            "What is the earnest money amount?"
        ]
        
        # Add document-specific suggestions based on metadata
        metadata = doc_info.get('metadata', {})
        if metadata.get('pages', 0) > 10:
            suggestions.append("Can you summarize the main sections of this document?")
        
        return suggestions[:8]  # Return top 8 suggestions
    
    def get_conversation_summary(self) -> Dict[str, Any]:
        """
        Get a summary of the current conversation
        
        Returns:
            Conversation summary and statistics
        """
        return {
            'total_questions': len(self.conversation_history),
            'recent_questions': [item['question'] for item in self.conversation_history[-3:]],
            'document_loaded': self.rag_tool.get_document_info()['loaded'],
            'conversation_history': self.conversation_history
        }
    
    def clear_conversation(self):
        """Clear the conversation history"""
        self.conversation_history = []
    
    def _enhance_question_with_context(self, question: str) -> str:
        """
        Enhance question with conversation context for better answers
        
        Args:
            question: Original question
            
        Returns:
            Enhanced question with context
        """
        if not self.conversation_history:
            return question
        
        # Get recent conversation context
        recent_context = self.conversation_history[-2:]  # Last 2 exchanges
        
        if recent_context:
            context_str = "\n".join([
                f"Previous Q: {item['question']}\nPrevious A: {item['answer'][:200]}..."
                for item in recent_context
            ])
            
            enhanced_question = f"""
            Given this conversation context:
            {context_str}
            
            Current question: {question}
            
            Please answer the current question, taking into account the conversation context if relevant.
            """
            
            return enhanced_question
        
        return question
    
    def _update_conversation_history(self, question: str, answer: str):
        """
        Update conversation history with new Q&A pair
        
        Args:
            question: User's question
            answer: Generated answer
        """
        self.conversation_history.append({
            'timestamp': time.time(),
            'question': question,
            'answer': answer
        })
        
        # Keep only last 20 exchanges to manage memory
        if len(self.conversation_history) > 20:
            self.conversation_history = self.conversation_history[-20:]
    
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
            'supported_formats': Config.SUPPORTED_FORMATS,
            'max_file_size': Config.MAX_FILE_SIZE,
            'ai_model': Config.BEDROCK_MODEL_ID,
            'features': [
                'RAG-based question answering',
                'Document summarization',
                'Conversation context awareness',
                'Suggested questions generation',
                'Multi-format document support'
            ]
        }
