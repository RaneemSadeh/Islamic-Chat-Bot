"""
RAG-powered Islamic Chatbot with Streamlit
A chatbot that uses Retrieval-Augmented Generation to answer questions based on uploaded PDFs
"""

import os
import streamlit as st
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.messages import HumanMessage, AIMessage
from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_nomic import NomicEmbeddings
from langchain_groq import ChatGroq
from langchain_community.vectorstores import FAISS


# ============================================================================
# SESSION STATE INITIALIZATION
# ============================================================================

def initialize_session_state():
    """Initialize all session state variables"""
    if 'database' not in st.session_state:
        st.session_state.database = None
    
    if 'chat_history' not in st.session_state:
        st.session_state.chat_history = []
    
    if 'backup_history' not in st.session_state:
        st.session_state.backup_history = []
    
    if 'documents' not in st.session_state:
        st.session_state.documents = None


# ============================================================================
# CONFIGURATION FUNCTIONS
# ============================================================================

def setup_sidebar():
    """Configure sidebar with model selection and API keys"""
    
    st.sidebar.title("Configuration")
    
    # Model selection
    model = st.sidebar.selectbox(
        "Select LLM Model",
        ("gemma2-9b-it", "llama-3.1-8b-instant", "mixtral-8x7b-32768", "llama3-8b-8192"),
        help="Choose the language model for responses"
    )
    
    # API Keys
    st.sidebar.subheader("API Keys")
    
    groq_api_key = st.sidebar.text_input(
        "GROQ API Key", 
        type="password",
        help="Enter your GROQ API key"
    )
    
    nomic_api_key = st.sidebar.text_input(
        "Nomic API Key", 
        type="password",
        help="Enter your Nomic API key for embeddings"
    )
    
    # Set environment variables
    if groq_api_key:
        os.environ["GROQ_API_KEY"] = groq_api_key
    else:
        st.sidebar.warning("⚠️ Please enter your GROQ API key")
    
    if nomic_api_key:
        os.environ["NOMIC_API_KEY"] = nomic_api_key
    else:
        st.sidebar.warning("⚠️ Please enter your Nomic API key")
    
    return model, groq_api_key, nomic_api_key


def setup_document_upload():
    """Handle PDF upload and processing"""
    
    st.sidebar.divider()
    st.sidebar.subheader("Document Upload")
    
    uploaded_pdf = st.sidebar.file_uploader(
        'Upload PDF File', 
        type='pdf',
        help="Upload a PDF document to enable RAG functionality"
    )
    
    docs = None
    
    if uploaded_pdf:
        temp_file = "./temp.pdf"
        
        try:
            with open(temp_file, "wb") as file:
                file.write(uploaded_pdf.getvalue())
            
            loader = PyPDFLoader(temp_file)
            docs = loader.load()
            
            st.sidebar.success(f"✅ PDF '{uploaded_pdf.name}' loaded successfully!")
            
        except Exception as e:
            st.sidebar.error(f"❌ Error loading PDF: {str(e)}")
    
    return docs


def setup_chunking_parameters():
    """Configure text chunking parameters"""
    
    st.sidebar.divider()
    st.sidebar.subheader("Chunking Parameters")
    
    chunk_size = st.sidebar.slider(
        "Chunk Size",
        min_value=100,
        max_value=1000,
        value=500,
        step=50,
        help="Size of text chunks for processing"
    )
    
    chunk_overlap = st.sidebar.slider(
        "Chunk Overlap",
        min_value=0,
        max_value=200,
        value=50,
        step=10,
        help="Overlap between consecutive chunks"
    )
    
    return chunk_size, chunk_overlap


# ============================================================================
# DATABASE FUNCTIONS
# ============================================================================

def create_vector_database(docs, chunk_size, chunk_overlap):
    """Create FAISS vector database from documents"""
    
    if not docs:
        st.sidebar.error("❌ No document loaded. Please upload a PDF first.")
        return None
    
    if chunk_size == 0 or chunk_overlap == 0:
        st.sidebar.error("❌ Invalid chunking parameters")
        return None
    
    try:
        # Split documents into chunks
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap
        )
        documents = text_splitter.split_documents(docs)
        
        # Create embeddings
        embeddings = NomicEmbeddings(model="nomic-embed-text-v1.5")
        
        # Create vector database
        database = FAISS.from_documents(documents, embedding=embeddings)
        
        st.sidebar.success(f"✅ Database created with {len(documents)} chunks!")
        return database
        
    except Exception as e:
        st.sidebar.error(f"❌ Error creating database: {str(e)}")
        return None


# ============================================================================
# CHAT FUNCTIONS
# ============================================================================

def get_response(user_question, chat_history, llm_model, database):
    """Generate response using LLM with or without RAG"""
    
    if database:
        # RAG mode: Use vector database for context
        search_docs = database.similarity_search(user_question, k=3)
        context = [doc.page_content for doc in search_docs]
        
        template = """You are a helpful assistant who answers questions based on provided context.

Context:
{context}

Chat History:
{chat_history}

Question: {user_question}

Instructions:
- Answer based on the context provided above
- Be clear, accurate, and helpful
- If the context doesn't contain the answer, say so
- Think step by step before answering

Answer:"""
    
    else:
        # Normal chat mode: No context
        template = """You are a helpful assistant.

Chat History:
{chat_history}

Question: {user_question}

Instructions:
- Provide a helpful and accurate response
- Be conversational and friendly
- Use the chat history to maintain context

Answer:"""
    
    # Create prompt template
    prompt = ChatPromptTemplate.from_template(template)
    
    # Create chain
    output_parser = StrOutputParser()
    chain = prompt | llm_model | output_parser
    
    # Generate response
    if database:
        return chain.stream({
            'chat_history': chat_history,
            'user_question': user_question,
            'context': context
        })
    else:
        return chain.stream({
            'chat_history': chat_history,
            'user_question': user_question
        })


def display_chat_history():
    """Display conversation history"""
    
    for message in st.session_state.chat_history:
        if isinstance(message, HumanMessage):
            with st.chat_message('user'):
                st.markdown(message.content)
        else:
            with st.chat_message('assistant'):
                st.markdown(message.content)


def handle_user_input(user_question, llm_model):
    """Process user input and generate response"""
    
    # Add user message to history
    st.session_state.chat_history.append(HumanMessage(user_question))
    
    # Display user message
    with st.chat_message("user"):
        st.markdown(user_question)
    
    # Generate and display AI response
    with st.chat_message('assistant'):
        ai_response = st.write_stream(
            get_response(
                user_question,
                st.session_state.chat_history,
                llm_model,
                st.session_state.database
            )
        )
    
    # Add AI message to history
    st.session_state.chat_history.append(AIMessage(ai_response))


# ============================================================================
# MAIN APPLICATION
# ============================================================================

def main():
    """Main application function"""
    
    # Page configuration
    st.set_page_config(
        page_title="RAG Chatbot",
        page_icon="robot",
        layout="wide"
    )
    
    # Initialize session state
    initialize_session_state()
    
    # Header
    st.markdown(
        "<h1 style='text-align: center;'>RAG-Powered Chatbot</h1>",
        unsafe_allow_html=True
    )
    st.markdown(
        "<p style='text-align: center;'>Upload a PDF and chat with your documents using AI</p>",
        unsafe_allow_html=True
    )
    
    # Sidebar configuration
    model, groq_api_key, nomic_api_key = setup_sidebar()
    
    # Check if API keys are provided
    if not groq_api_key:
        st.warning("⚠️ Please enter your GROQ API key in the sidebar to continue")
        st.stop()
    
    # Initialize LLM
    llm_model = ChatGroq(model=model, api_key=groq_api_key)
    
    # Document upload
    docs = setup_document_upload()
    
    # Chunking parameters
    chunk_size, chunk_overlap = setup_chunking_parameters()
    
    # Database creation
    st.sidebar.divider()
    st.sidebar.subheader("Vector Database")
    
    if st.sidebar.button('Create Database', type="primary"):
        if nomic_api_key:
            with st.spinner("Creating vector database..."):
                st.session_state.database = create_vector_database(
                    docs, chunk_size, chunk_overlap
                )
        else:
            st.sidebar.error("❌ Please enter Nomic API key first")
    
    # Display database status
    if st.session_state.database:
        st.sidebar.info("Database is active (RAG mode)")
    else:
        st.sidebar.info("Normal chat mode (no RAG)")
    
    # Chat history controls
    st.sidebar.divider()
    st.sidebar.subheader("Chat History")
    
    col1, col2 = st.sidebar.columns(2)
    
    with col1:
        if st.button('Clear'):
            st.session_state.backup_history = st.session_state.chat_history.copy()
            st.session_state.chat_history = []
            st.rerun()
    
    with col2:
        if st.button('Undo'):
            if st.session_state.backup_history:
                st.session_state.chat_history = st.session_state.backup_history.copy()
                st.rerun()
    
    # Display chat history
    display_chat_history()
    
    # Chat input
    user_question = st.chat_input("Type your message here...")
    
    if user_question:
        handle_user_input(user_question, llm_model)


# ============================================================================
# RUN APPLICATION
# ============================================================================

if __name__ == "__main__":
    main()

# To run: streamlit run RAG_Islamic_Chatbot.py