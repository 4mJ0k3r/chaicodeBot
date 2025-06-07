import streamlit as st
from dotenv import load_dotenv
import os
import time
from typing import Dict
from openai import OpenAI

from vector_store import VectorStore
from chatengine import ChatEngine

# Load environment variables
load_dotenv()

# Page setup
st.set_page_config(
    page_title="ChaiCode Docs Bot",
    page_icon="☕",
    layout="wide"
)

# Enhanced styling
st.markdown("""
<style>
    .main-title {
        color: #2c3e50;
        font-size: 3rem;
        font-weight: 700;
        margin-bottom: 0.5rem;
        text-align: center;
    }
    
    .subtitle {
        color: #7f8c8d;
        font-size: 1.2rem;
        text-align: center;
        margin-bottom: 3rem;
        font-weight: 300;
    }
    
    .api-key-container {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 2rem;
        border-radius: 15px;
        margin: 2rem 0;
        text-align: center;
        color: white;
    }
    
    .source-box {
        background: #f8f9fa;
        border: 1px solid #dee2e6;
        padding: 15px;
        margin: 10px 0;
        border-radius: 8px;
        border-left: 4px solid #667eea;
    }
    
    .chat-container {
        max-width: 800px;
        margin: 0 auto;
    }
    
    .stTextInput > div > div > input {
        border-radius: 10px;
        border: 2px solid #e9ecef;
        padding: 12px;
    }
    
    .stTextInput > div > div > input:focus {
        border-color: #667eea;
        box-shadow: 0 0 0 0.2rem rgba(102, 126, 234, 0.25);
    }
</style>
""", unsafe_allow_html=True)

def validate_api_key(api_key: str) -> bool:
    """Test if the API key is valid by making a simple request"""
    try:
        client = OpenAI(api_key=api_key)
        # Test with a minimal request
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": "Hi"}],
            max_tokens=5
        )
        return True
    except Exception as e:
        return False

@st.cache_resource
def get_chat_components(api_key: str):
    """Setup chat components with user's API key"""
    vector_store = VectorStore(api_key=api_key)
    chat_engine = ChatEngine(api_key=api_key, vector_store=vector_store)
    return vector_store, chat_engine

@st.cache_data(ttl=1800, show_spinner=False)
def get_response(question: str, api_key: str) -> Dict:
    """Get bot response with caching"""
    _, engine = get_chat_components(api_key)
    return engine.get_answer(question)

# Session state
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "api_key_validated" not in st.session_state:
    st.session_state.api_key_validated = False
if "user_api_key" not in st.session_state:
    st.session_state.user_api_key = ""

# Header
st.markdown('<h1 class="main-title">☕ ChaiCode Docs Bot</h1>', unsafe_allow_html=True)
st.markdown('<p class="subtitle">Your personal AI assistant for ChaiCode documentation</p>', unsafe_allow_html=True)

# API Key validation section
if not st.session_state.api_key_validated:
    st.markdown("""
    <div class="api-key-container">
        <h3>🔐 Enter Your OpenAI API Key</h3>
        <p>To use this bot, please provide your OpenAI API key. Your key is stored securely in your session and never saved.</p>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        api_key_input = st.text_input(
            "OpenAI API Key", 
            type="password", 
            placeholder="sk-...",
            help="Get your API key from https://platform.openai.com/api-keys"
        )
        
        if st.button("🚀 Validate & Start Chat", use_container_width=True):
            if api_key_input:
                with st.spinner("Validating your API key..."):
                    if validate_api_key(api_key_input):
                        st.session_state.api_key_validated = True
                        st.session_state.user_api_key = api_key_input
                        st.success("✅ API key validated! You can now start chatting.")
                        st.rerun()
                    else:
                        st.error("❌ Invalid API key. Please check and try again.")
            else:
                st.warning("⚠️ Please enter your API key first.")
    
    # Info section
    with st.expander("ℹ️ How to get an OpenAI API Key"):
        st.markdown("""
        1. Go to [OpenAI Platform](https://platform.openai.com/api-keys)
        2. Sign in to your account (or create one)
        3. Click "Create new secret key"
        4. Copy the key and paste it above
        5. Make sure you have some credits in your account
        """)
    
    st.stop()

# Main chat interface (only shows after API key validation)
st.markdown('<div class="chat-container">', unsafe_allow_html=True)

# Simple sidebar with just info
with st.sidebar:
    st.markdown("### 📖 About")
    st.write("This bot uses your OpenAI API key to answer questions about ChaiCode documentation using RAG (Retrieval Augmented Generation).")
    
    st.markdown("### 🛠️ How it works")
    st.write("1. Enter your question below")
    st.write("2. The bot searches relevant docs")
    st.write("3. Gets AI-powered answer with sources")
    
    st.markdown("### 🔒 Privacy")
    st.write("Your API key is only stored in your browser session and is never saved permanently.")
    
    if st.button("🔄 Change API Key"):
        st.session_state.api_key_validated = False
        st.session_state.user_api_key = ""
        st.session_state.chat_history = []
        st.rerun()

# Display chat history
for chat in st.session_state.chat_history:
    with st.chat_message("user"):
        st.write(chat["question"])
    
    with st.chat_message("assistant"):
        st.write(chat["answer"])
        
        if chat.get("sources"):
            with st.expander(f"📚 Sources ({len(chat['sources'])})"):
                for i, src in enumerate(chat["sources"]):
                    source_url = src.get('source', 'Unknown')
                    st.markdown(f"""
                    <div class="source-box">
                        <strong>[{src.get('number', i+1)}]</strong> 
                        <a href="{source_url}" target="_blank" style="color: #667eea; text-decoration: none; font-weight: 500;">{source_url}</a>
                        <br><small style="color: #6c757d;">{src.get('preview', 'No preview')}</small>
                    </div>
                    """, unsafe_allow_html=True)

# Chat input
user_input = st.chat_input("Ask me anything about ChaiCode documentation...")

if user_input:
    # Add user message
    with st.chat_message("user"):
        st.write(user_input)
    
    # Get and display bot response
    with st.chat_message("assistant"):
        loading_placeholder = st.empty()
        loading_placeholder.markdown("🤔 **Thinking...**")
        
        try:
            start_time = time.time()
            response = get_response(user_input, st.session_state.user_api_key)
            response_time = time.time() - start_time
            
            loading_placeholder.empty()
            
            answer = response.get("answer", "Sorry, couldn't get an answer.")
            sources = response.get("sources", [])
            
            st.write(answer)
            
            if sources:
                with st.expander(f"📚 Sources ({len(sources)})"):
                    for i, src in enumerate(sources):
                        source_url = src.get('source', 'Unknown')
                        st.markdown(f"""
                        <div class="source-box">
                            <strong>[{src.get('number', i+1)}]</strong> 
                            <a href="{source_url}" target="_blank" style="color: #667eea; text-decoration: none; font-weight: 500;">{source_url}</a>
                            <br><small style="color: #6c757d;">{src.get('preview', 'No preview')}</small>
                        </div>
                        """, unsafe_allow_html=True)
            
            st.caption(f"⏱️ {response_time:.1f}s")
            
            # Save to history
            st.session_state.chat_history.append({
                "question": user_input,
                "answer": answer,
                "sources": sources,
                "time": response_time
            })
            
        except Exception as e:
            loading_placeholder.empty()
            st.error(f"Something went wrong: {str(e)}")
            
            st.session_state.chat_history.append({
                "question": user_input,
                "answer": "Error occurred",
                "sources": [],
                "time": 0
            })

st.markdown('</div>', unsafe_allow_html=True)

# Footer
st.markdown("---")
st.markdown(
    '<p style="text-align: center; color: #6c757d; font-size: 0.9rem;">ChaiCode Documentation Bot • Built with Streamlit & OpenAI</p>', 
    unsafe_allow_html=True
)
