"""
RAG (Retrieval-Augmented Generation) tool for document Q&A
"""
import re
from typing import Dict, Any, List, Optional, Tuple
from src.models.bedrock_model import BedrockModel
from src.tools.document_processor import DocumentProcessor

class DocumentRAGTool:
    """
    RAG tool for answering questions about documents using retrieval and generation
    """
    
    def __init__(self, aws_profile: Optional[str] = None):
        """
        Initialize the RAG tool
        
        Args:
            aws_profile: AWS profile name for authentication
        """
        self.bedrock_model = BedrockModel(profile_name=aws_profile)
        self.document_processor = DocumentProcessor()
        self.name = "DocumentRAGTool"
        self.description = "RAG-based question answering system for documents"
        
        # Document storage for current session
        self.current_document = {
            'text': '',
            'chunks': [],
            'metadata': {},
            'file_path': ''
        }
    
    def load_document(self, file_path: str) -> Dict[str, Any]:
        """
        Load and process a document for Q&A
        
        Args:
            file_path: Path to the document file
            
        Returns:
            Processing result with document chunks
        """
        try:
            # Process the document to extract text
            processing_result = self.document_processor.process_document(file_path)
            
            if not processing_result['success']:
                return {
                    'success': False,
                    'error': processing_result['error'],
                    'chunks_count': 0
                }
            
            document_text = processing_result['text']
            metadata = processing_result['metadata']
            
            # Split document into chunks for better retrieval
            chunks = self._chunk_document(document_text)
            
            # Store document for Q&A
            self.current_document = {
                'text': document_text,
                'chunks': chunks,
                'metadata': metadata,
                'file_path': file_path
            }
            
            return {
                'success': True,
                'text_length': len(document_text),
                'chunks_count': len(chunks),
                'metadata': metadata,
                'preview': document_text[:500] + "..." if len(document_text) > 500 else document_text
            }
            
        except Exception as e:
            return {
                'success': False,
                'error': f"Document loading failed: {str(e)}",
                'chunks_count': 0
            }
    
    def ask_question(self, question: str, max_chunks: int = 5) -> Dict[str, Any]:
        """
        Answer a question about the loaded document using RAG
        
        Args:
            question: User's question about the document
            max_chunks: Maximum number of relevant chunks to use
            
        Returns:
            Answer with relevant context and confidence
        """
        if not self.current_document['text']:
            return {
                'success': False,
                'error': "No document loaded. Please load a document first.",
                'answer': '',
                'relevant_chunks': [],
                'confidence': 0.0
            }
        
        try:
            # Retrieve relevant chunks
            relevant_chunks = self._retrieve_relevant_chunks(question, max_chunks)
            
            # Generate answer using retrieved context
            answer_result = self._generate_answer(question, relevant_chunks)
            
            return {
                'success': True,
                'question': question,
                'answer': answer_result['answer'],
                'relevant_chunks': relevant_chunks,
                'confidence': answer_result['confidence'],
                'reasoning': answer_result.get('reasoning', ''),
                'chunk_count_used': len(relevant_chunks)
            }
            
        except Exception as e:
            return {
                'success': False,
                'error': f"Question answering failed: {str(e)}",
                'answer': '',
                'relevant_chunks': [],
                'confidence': 0.0
            }
    
    def get_document_summary(self) -> Dict[str, Any]:
        """
        Generate a summary of the loaded document
        
        Returns:
            Document summary and key information
        """
        if not self.current_document['text']:
            return {
                'success': False,
                'error': "No document loaded",
                'summary': ''
            }
        
        try:
            # Use first few chunks for summary
            summary_text = ' '.join(self.current_document['chunks'][:3])
            
            summary_prompt = f"""
            Please provide a concise summary of this document excerpt:
            
            {summary_text}
            
            Include:
            1. Document type and purpose
            2. Key information and details
            3. Main parties or entities mentioned
            4. Important dates, amounts, or numbers
            
            Keep the summary under 200 words.
            """
            
            response = self.bedrock_model.invoke_model(summary_prompt, max_tokens=1000)
            
            if response['success']:
                return {
                    'success': True,
                    'summary': response['content'],
                    'document_stats': {
                        'total_length': len(self.current_document['text']),
                        'chunks_count': len(self.current_document['chunks']),
                        'file_path': self.current_document['file_path']
                    }
                }
            else:
                return {
                    'success': False,
                    'error': f"Summary generation failed: {response['error']}",
                    'summary': ''
                }
                
        except Exception as e:
            return {
                'success': False,
                'error': f"Summary generation failed: {str(e)}",
                'summary': ''
            }
    
    def _chunk_document(self, text: str, chunk_size: int = 1000, overlap: int = 200) -> List[Dict[str, Any]]:
        """
        Split document into overlapping chunks for better retrieval
        
        Args:
            text: Document text to chunk
            chunk_size: Size of each chunk in characters
            overlap: Overlap between chunks in characters
            
        Returns:
            List of text chunks with metadata
        """
        chunks = []
        
        # Clean and normalize text
        text = re.sub(r'\s+', ' ', text.strip())
        
        # Simple chunking approach - split by character count with sentence boundaries
        current_pos = 0
        chunk_id = 0
        
        while current_pos < len(text):
            # Determine chunk end position
            chunk_end = min(current_pos + chunk_size, len(text))
            
            # Try to end at a sentence boundary if possible
            if chunk_end < len(text):
                # Look for sentence endings within the last 100 characters
                search_start = max(chunk_end - 100, current_pos)
                sentence_endings = []
                
                for i in range(search_start, chunk_end):
                    if text[i] in '.!?':
                        sentence_endings.append(i + 1)
                
                if sentence_endings:
                    chunk_end = sentence_endings[-1]  # Use the last sentence ending
            
            # Extract chunk text
            chunk_text = text[current_pos:chunk_end].strip()
            
            if chunk_text:  # Only add non-empty chunks
                chunks.append({
                    'id': chunk_id,
                    'text': chunk_text,
                    'length': len(chunk_text),
                    'start_pos': current_pos
                })
                chunk_id += 1
            
            # Move to next chunk with overlap
            if chunk_end >= len(text):
                break
                
            current_pos = max(chunk_end - overlap, current_pos + 1)
        
        return chunks
    
    def _retrieve_relevant_chunks(self, question: str, max_chunks: int = 5) -> List[Dict[str, Any]]:
        """
        Retrieve most relevant chunks for the question using simple keyword matching
        In production, this would use vector embeddings and similarity search
        
        Args:
            question: User's question
            max_chunks: Maximum chunks to return
            
        Returns:
            List of relevant chunks with relevance scores
        """
        if not self.current_document['chunks']:
            return []
        
        # Extract keywords from question
        question_keywords = self._extract_keywords(question.lower())
        
        # Score chunks based on keyword overlap
        chunk_scores = []
        
        for chunk in self.current_document['chunks']:
            chunk_text = chunk['text'].lower()
            
            # Calculate relevance score
            score = 0
            matched_keywords = []
            
            for keyword in question_keywords:
                if keyword in chunk_text:
                    # Count occurrences and weight by keyword importance
                    occurrences = chunk_text.count(keyword)
                    keyword_weight = len(keyword) / 10  # Longer keywords get higher weight
                    score += occurrences * keyword_weight
                    matched_keywords.append(keyword)
            
            # Boost score for exact phrase matches
            if len(question_keywords) > 1:
                question_phrase = ' '.join(question_keywords[:3])  # First 3 keywords
                if question_phrase in chunk_text:
                    score += 5
            
            chunk_scores.append({
                'chunk': chunk,
                'score': score,
                'matched_keywords': matched_keywords
            })
        
        # Sort by relevance score and return top chunks
        chunk_scores.sort(key=lambda x: x['score'], reverse=True)
        
        relevant_chunks = []
        for item in chunk_scores[:max_chunks]:
            if item['score'] > 0:  # Only include chunks with some relevance
                relevant_chunks.append({
                    'text': item['chunk']['text'],
                    'relevance_score': item['score'],
                    'matched_keywords': item['matched_keywords'],
                    'chunk_id': item['chunk']['id']
                })
        
        return relevant_chunks
    
    def _extract_keywords(self, text: str) -> List[str]:
        """
        Extract keywords from text for relevance matching
        
        Args:
            text: Input text
            
        Returns:
            List of keywords
        """
        # Remove common stop words
        stop_words = {
            'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 'of', 'with',
            'by', 'is', 'are', 'was', 'were', 'be', 'been', 'have', 'has', 'had', 'do', 'does',
            'did', 'will', 'would', 'could', 'should', 'may', 'might', 'can', 'this', 'that',
            'these', 'those', 'what', 'when', 'where', 'why', 'how', 'who', 'which'
        }
        
        # Extract words and filter
        words = re.findall(r'\b\w+\b', text.lower())
        keywords = [word for word in words if len(word) > 2 and word not in stop_words]
        
        # Remove duplicates while preserving order
        seen = set()
        unique_keywords = []
        for keyword in keywords:
            if keyword not in seen:
                seen.add(keyword)
                unique_keywords.append(keyword)
        
        return unique_keywords
    
    def _generate_answer(self, question: str, relevant_chunks: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Generate answer using retrieved chunks and LLM
        
        Args:
            question: User's question
            relevant_chunks: Retrieved relevant text chunks
            
        Returns:
            Generated answer with confidence and reasoning
        """
        if not relevant_chunks:
            return {
                'answer': "I couldn't find relevant information in the document to answer your question.",
                'confidence': 0.1,
                'reasoning': "No relevant text chunks were found for the question."
            }
        
        # Prepare context from relevant chunks
        context = "\n\n".join([f"[Chunk {chunk['chunk_id']}]: {chunk['text']}" 
                              for chunk in relevant_chunks])
        
        # Create prompt for answer generation
        prompt = f"""
        Based on the following document excerpts, please answer the user's question accurately and concisely.
        
        DOCUMENT EXCERPTS:
        {context}
        
        QUESTION: {question}
        
        Please provide your response in the following JSON format:
        {{
            "answer": "Your detailed answer based on the document content",
            "confidence": 0.0-1.0,
            "reasoning": "Brief explanation of how you arrived at this answer",
            "source_chunks": [list of chunk IDs that were most relevant]
        }}
        
        Guidelines:
        - Only use information from the provided document excerpts
        - If the answer isn't in the document, say so clearly
        - Provide specific details and quotes when possible
        - Rate your confidence based on how well the document supports your answer
        - Be concise but comprehensive
        """
        
        response = self.bedrock_model.invoke_model(prompt, max_tokens=2000)
        
        if response['success']:
            try:
                # Try to parse JSON response
                import json
                result = json.loads(response['content'])
                return {
                    'answer': result.get('answer', response['content']),
                    'confidence': float(result.get('confidence', 0.7)),
                    'reasoning': result.get('reasoning', 'Generated from document analysis'),
                    'source_chunks': result.get('source_chunks', [])
                }
            except (json.JSONDecodeError, ValueError):
                # If JSON parsing fails, return raw content
                return {
                    'answer': response['content'],
                    'confidence': 0.7,
                    'reasoning': 'Generated from document analysis'
                }
        else:
            return {
                'answer': f"I encountered an error while generating the answer: {response['error']}",
                'confidence': 0.0,
                'reasoning': "Error in answer generation"
            }
    
    def clear_document(self):
        """Clear the currently loaded document"""
        self.current_document = {
            'text': '',
            'chunks': [],
            'metadata': {},
            'file_path': ''
        }
    
    def get_document_info(self) -> Dict[str, Any]:
        """Get information about the currently loaded document"""
        return {
            'loaded': bool(self.current_document['text']),
            'file_path': self.current_document['file_path'],
            'text_length': len(self.current_document['text']),
            'chunks_count': len(self.current_document['chunks']),
            'metadata': self.current_document['metadata']
        }
