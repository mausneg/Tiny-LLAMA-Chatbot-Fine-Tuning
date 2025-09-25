import streamlit as st
import requests
from datetime import datetime
import re
import html

# Page config
st.set_page_config(
    page_title="TinyLlama AI Assistant",
    page_icon="💬",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for Professional AI Assistant styling
st.markdown("""
<style>
    /* Global Styles */
    .main > div {
        padding-top: 2rem;
    }
    
    /* Header Styling */
    .main-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        text-align: center;
        padding: 2rem 0;
        border-radius: 12px;
        margin-bottom: 2rem;
        box-shadow: 0 4px 20px rgba(0,0,0,0.1);
    }
    
    .header-content h1 {
        margin: 0;
        font-size: 2.2rem;
        font-weight: 700;
        text-shadow: 0 2px 4px rgba(0,0,0,0.3);
    }
    
    .header-subtitle {
        margin-top: 0.5rem;
        font-size: 1.1rem;
        opacity: 0.9;
        font-weight: 300;
    }
    
    /* Chat Container */
    .chat-container {
        max-width: 900px;
        margin: 0 auto;
        padding: 0 1rem;
    }
    
    /* Message Bubbles - User */
    .user-message {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 1.2rem 1.5rem;
        border-radius: 18px 18px 4px 18px;
        margin: 1.5rem 0 1.5rem 3rem;
        position: relative;
        box-shadow: 0 2px 12px rgba(102, 126, 234, 0.3);
        max-width: 80%;
        margin-left: auto;
        margin-right: 0;
    }
    
    .user-message::before {
        content: "";
        background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' fill='white' viewBox='0 0 24 24'%3E%3Cpath d='M12 12c2.21 0 4-1.79 4-4s-1.79-4-4-4-4 1.79-4 4 1.79 4 4 4zm0 2c-2.67 0-8 1.34-8 4v2h16v-2c0-2.66-5.33-4-8-4z'/%3E%3C/svg%3E");
        position: absolute;
        right: -2.5rem;
        top: 0.8rem;
        width: 28px;
        height: 28px;
        display: block;
        background-color: #5a67d8;
        border-radius: 50%;
        padding: 6px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.2);
    }
    
    /* Message Bubbles - Assistant */
    .assistant-message {
        background: white;
        border: 1px solid #e2e8f0;
        color: #2d3748;
        padding: 1.2rem 1.5rem;
        border-radius: 18px 18px 18px 4px;
        margin: 1.5rem 3rem 1.5rem 0;
        position: relative;
        box-shadow: 0 2px 12px rgba(0,0,0,0.08);
        max-width: 80%;
    }
    
    .assistant-message::before {
        content: "";
        background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' fill='white' viewBox='0 0 24 24'%3E%3Cpath d='M20,2H4A2,2 0 0,0 2,4V22L6,18H20A2,2 0 0,0 22,16V4A2,2 0 0,0 20,2M6,9V7H18V9H6M14,11V13H6V11H14M16,15V17H6V15H16Z'/%3E%3C/svg%3E");
        position: absolute;
        left: -2.5rem;
        top: 0.8rem;
        width: 28px;
        height: 28px;
        display: block;
        background: linear-gradient(135deg, #4285f4 0%, #34a853 100%);
        border-radius: 50%;
        padding: 6px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.2);
    }
    
    /* Typing Indicator */
    .typing-indicator {
        background: #f7fafc;
        border: 1px solid #e2e8f0;
        color: #718096;
        padding: 1rem 1.5rem;
        border-radius: 18px 18px 18px 4px;
        margin: 1.5rem 3rem 1.5rem 0;
        position: relative;
        font-style: italic;
        max-width: 200px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.05);
    }
    
    .typing-indicator::before {
        content: "";
        background: linear-gradient(135deg, #4285f4 0%, #34a853 100%);
        position: absolute;
        left: -2.5rem;
        top: 0.8rem;
        width: 28px;
        height: 28px;
        border-radius: 50%;
        display: block;
        animation: pulse 1.5s infinite;
    }
    
    .typing-indicator::after {
        content: "";
        background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' fill='white' viewBox='0 0 24 24'%3E%3Cpath d='M20,2H4A2,2 0 0,0 2,4V22L6,18H20A2,2 0 0,0 22,16V4A2,2 0 0,0 20,2M6,9V7H18V9H6M14,11V13H6V11H14M16,15V17H6V15H16Z'/%3E%3C/svg%3E");
        position: absolute;
        left: -2.3rem;
        top: 0.9rem;
        width: 16px;
        height: 16px;
        animation: pulse 1.5s infinite;
    }
    
    @keyframes pulse {
        0%, 100% { 
            opacity: 1; 
            transform: scale(1);
        }
        50% { 
            opacity: 0.7;
            transform: scale(0.95);
        }
    }
    
    /* Chat Input Area */
    .chat-input-container {
        background: white;
        padding: 1.5rem;
        border-top: 1px solid #e2e8f0;
        border-radius: 12px 12px 0 0;
        margin-top: 2rem;
        box-shadow: 0 -2px 12px rgba(0,0,0,0.05);
    }
    
    .chat-messages {
        margin-bottom: 150px;
        min-height: 60vh;
        padding: 1rem 0;
    }
    
    /* Timestamps */
    .timestamp {
        font-size: 0.75rem;
        color: #a0aec0;
        margin-top: 0.5rem;
        font-weight: 500;
    }
    
    .user-message .timestamp {
        color: rgba(255,255,255,0.8);
        text-align: right;
    }
    
    /* Error Messages */
    .error-message {
        background: linear-gradient(135deg, #fed7d7 0%, #feb2b2 100%);
        border: 1px solid #fc8181;
        color: #c53030;
        padding: 1rem 1.5rem;
        border-radius: 12px;
        margin: 1rem 0;
        font-weight: 500;
    }
    
    /* Sidebar Styling */
    .sidebar-content {
        background: #f8fafc;
        border-radius: 12px;
        padding: 1.5rem;
        margin-bottom: 1rem;
        border: 1px solid #e2e8f0;
    }
    
    .status-badge {
        display: inline-flex;
        align-items: center;
        gap: 0.5rem;
        padding: 0.5rem 1rem;
        border-radius: 20px;
        font-size: 0.9rem;
        font-weight: 600;
        margin-bottom: 1rem;
    }
    
    .status-online {
        background: linear-gradient(135deg, #c6f6d5 0%, #9ae6b4 100%);
        color: #22543d;
        border: 1px solid #68d391;
    }
    
    .status-offline {
        background: linear-gradient(135deg, #fed7d7 0%, #feb2b2 100%);
        color: #742a2a;
        border: 1px solid #fc8181;
    }
    
    /* Custom Buttons */
    .stButton > button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        border-radius: 8px;
        padding: 0.6rem 1.2rem;
        font-weight: 600;
        transition: all 0.3s ease;
        box-shadow: 0 2px 8px rgba(102, 126, 234, 0.3);
    }
    
    .stButton > button:hover {
        transform: translateY(-1px);
        box-shadow: 0 4px 12px rgba(102, 126, 234, 0.4);
    }
    
    /* Form Elements */
    .stTextArea > div > div > textarea {
        border-radius: 12px;
        border: 2px solid #e2e8f0;
        padding: 1rem;
        font-size: 1rem;
        transition: border-color 0.3s ease;
    }
    
    .stTextArea > div > div > textarea:focus {
        border-color: #667eea;
        box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
    }
</style>
""", unsafe_allow_html=True)

# API Configuration
API_BASE_URL = "http://localhost:8082"
CONVERSATION_ENDPOINT = f"{API_BASE_URL}/api/v1/conversation"

# Initialize session state
if "messages" not in st.session_state:
    st.session_state.messages = []
if "is_typing" not in st.session_state:
    st.session_state.is_typing = False

def check_api_status():
    try:
        response = requests.get(f"{API_BASE_URL}/docs", timeout=5)
        return response.status_code == 200
    except:
        return False

def clean_response(response_text):
    print(response_text)
    """Extract only the most recent assistant response and clean it"""
    # Split by assistant tags to find all assistant responses
    assistant_parts = re.split(r'<\|assistant\|>', response_text)
    
    if len(assistant_parts) > 1:
        # Take the last assistant response (most recent)
        last_response = assistant_parts[-1]
    else:
        # If no assistant tag found, use the whole response
        last_response = response_text
    
    # Remove any remaining conversation tags and user input
    cleaned = re.sub(r'<\|user\|>.*?(?=<\|assistant\|>|$)', '', last_response, flags=re.DOTALL)
    cleaned = re.sub(r'<\|.*?\|>', '', cleaned)
    
    # Remove extra whitespace and newlines
    cleaned = cleaned.strip()
    
    # If the response is empty after cleaning, provide a fallback
    if not cleaned:
        return "I'm here to help! Could you please rephrase your question?"
    
    return cleaned

def send_message_to_api(message):
    """Send message to FastAPI backend"""
    try:
        payload = {
            "role": "user",
            "content": [message]
        }
        response = requests.post(
            CONVERSATION_ENDPOINT,
            json=payload,
            headers={"Content-Type": "application/json"},
            timeout=60*5
        )
        
        print(f"API Response Status: {response}")  # Debugging line
        if response.status_code == 200:
            result = response.json()
            raw_response = result.get("response", "No response received")
            # Clean the response before returning
            cleaned_response = clean_response(raw_response)
            return cleaned_response
        else:
            return f"Error: {response.status_code} - {response.text}"
    
    except requests.exceptions.Timeout:
        return "Error: Request timed out. The model might be processing a complex query."
    except requests.exceptions.ConnectionError:
        return "Error: Cannot connect to the API server. Please make sure the FastAPI server is running."
    except Exception as e:
        return f"Error: {str(e)}"

def display_message(message, is_user=True):
    """Display a message with appropriate styling"""
    timestamp = datetime.now().strftime("%H:%M")
    
    # Escape HTML characters to prevent rendering issues
    escaped_message = html.escape(message)
    
    if is_user:
        st.markdown(f"""
        <div class="user-message">
            <div>{escaped_message}</div>
            <div class="timestamp">{timestamp}</div>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown(f"""
        <div class="assistant-message">
            <div>{escaped_message}</div>
            <div class="timestamp">{timestamp}</div>
        </div>
        """, unsafe_allow_html=True)

def display_typing_indicator():
    """Display typing indicator"""
    st.markdown("""
    <div class="typing-indicator">
        TinyLlama is thinking...
    </div>
    """, unsafe_allow_html=True)

# Professional Sidebar
with st.sidebar:
    # Header
    st.markdown("""
    <div style="text-align: center; margin-bottom: 2rem;">
        <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                    padding: 1.5rem; border-radius: 12px; margin-bottom: 1rem;">
            <div style="display: flex; align-items: center; justify-content: center; gap: 0.8rem;">
                <svg width="28" height="28" fill="white" viewBox="0 0 24 24">
                    <path d="M20,2H4A2,2 0 0,0 2,4V22L6,18H20A2,2 0 0,0 22,16V4A2,2 0 0,0 20,2M6,9V7H18V9H6M14,11V13H6V11H14M16,15V17H6V15H16Z"/>
                </svg>
                <span style="font-size: 1.3rem; font-weight: 700; color: white;">TinyLlama AI</span>
            </div>
            <p style="color: rgba(255,255,255,0.9); margin: 0.5rem 0 0 0; font-size: 0.9rem;">
                Intelligent Conversational Assistant
            </p>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # API Status
    api_status = check_api_status()
    status_text = "System Online" if api_status else "System Offline"
    
    st.markdown("""
    <div style="display: flex; align-items: center; gap: 0.5rem; margin-bottom: 1rem;">
        <svg width="18" height="18" fill="#4285f4" viewBox="0 0 24 24">
            <path d="M12,2A10,10 0 0,0 2,12A10,10 0 0,0 12,22A10,10 0 0,0 22,12A10,10 0 0,0 12,2M11,7H13V9H11V7M11,11H13V17H11V11Z"/>
        </svg>
        <h4 style="margin: 0; color: #2d3748;">System Status</h4>
    </div>
    """, unsafe_allow_html=True)
    
    if api_status:
        st.markdown(f"""
        <div style="background: linear-gradient(135deg, #c6f6d5 0%, #9ae6b4 100%); 
                    color: #22543d; border: 1px solid #68d391; padding: 0.75rem 1rem; 
                    border-radius: 8px; margin: 0.5rem 0; display: flex; align-items: center; gap: 0.5rem;">
            <svg width="16" height="16" fill="#22543d" viewBox="0 0 24 24">
                <path d="M12,2A10,10 0 0,1 22,12A10,10 0 0,1 12,22A10,10 0 0,1 2,12A10,10 0 0,1 12,2M11,16.5L18,9.5L16.59,8.09L11,13.67L7.41,10.09L6,11.5L11,16.5Z"/>
            </svg>
            <span>{status_text}</span>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown(f"""
        <div style="background: linear-gradient(135deg, #fed7d7 0%, #feb2b2 100%); 
                    color: #742a2a; border: 1px solid #fc8181; padding: 0.75rem 1rem; 
                    border-radius: 8px; margin: 0.5rem 0; display: flex; align-items: center; gap: 0.5rem;">
            <svg width="16" height="16" fill="#742a2a" viewBox="0 0 24 24">
                <path d="M13,13H11V7H13M13,17H11V15H13M12,2A10,10 0 0,0 2,12A10,10 0 0,0 12,22A10,10 0 0,0 22,12A10,10 0 0,0 12,2Z"/>
            </svg>
            <span>{status_text}</span>
        </div>
        """, unsafe_allow_html=True)
    
    if not api_status:
        st.markdown("""
        <div style="background: linear-gradient(135deg, #fef5e7 0%, #fed7aa 100%); 
                    color: #744210; border: 1px solid #f6ad55; padding: 0.75rem 1rem; 
                    border-radius: 8px; margin: 0.5rem 0; display: flex; align-items: center; gap: 0.5rem;">
            <svg width="16" height="16" fill="#744210" viewBox="0 0 24 24">
                <path d="M13,13H11V7H13M13,17H11V15H13M12,2A10,10 0 0,0 2,12A10,10 0 0,0 12,22A10,10 0 0,0 22,12A10,10 0 0,0 12,2Z"/>
            </svg>
            <span><strong>Connection Error</strong>: Backend service is unavailable. Please contact system administrator.</span>
        </div>
        """, unsafe_allow_html=True)
    
    # Model Information
    st.markdown("""
    <div style="display: flex; align-items: center; gap: 0.5rem; margin-bottom: 1rem;">
        <svg width="18" height="18" fill="#4285f4" viewBox="0 0 24 24">
            <path d="M12,2A2,2 0 0,1 14,4C14,4.74 13.6,5.39 13,5.73V7H14A7,7 0 0,1 21,14H22A1,1 0 0,1 23,15V18A1,1 0 0,1 22,19H21V20A2,2 0 0,1 19,22H5A2,2 0 0,1 3,20V19H2A1,1 0 0,1 1,18V15A1,1 0 0,1 2,14H3A7,7 0 0,1 10,7H11V5.73C10.4,5.39 10,4.74 10,4A2,2 0 0,1 12,2Z"/>
        </svg>
        <h4 style="margin: 0; color: #2d3748;">AI Model Details</h4>
    </div>
    """, unsafe_allow_html=True)
    st.info("""
    **Model:** TinyLlama-1.1B-Chat-v1.2 
    **Architecture:** Transformer-based Language Model  
    **Optimization:** 8-bit Quantization  
    **Framework:** HuggingFace Transformers + PEFT  
    **Performance:** Optimized for conversational AI with efficient memory usage
    """)
    
    # Session Controls
    st.markdown("""
    <div style="display: flex; align-items: center; gap: 0.5rem; margin-bottom: 1rem;">
        <svg width="18" height="18" fill="#4285f4" viewBox="0 0 24 24">
            <path d="M12,15.5A3.5,3.5 0 0,1 8.5,12A3.5,3.5 0 0,1 12,8.5A3.5,3.5 0 0,1 15.5,12A3.5,3.5 0 0,1 12,15.5M19.43,12.97C19.47,12.65 19.5,12.33 19.5,12C19.5,11.67 19.47,11.34 19.43,11L21.54,9.37C21.73,9.22 21.78,8.95 21.66,8.73L19.66,5.27C19.54,5.05 19.27,4.96 19.05,5.05L16.56,6.05C16.04,5.66 15.5,5.32 14.87,5.07L14.5,2.42C14.46,2.18 14.25,2 14,2H10C9.75,2 9.54,2.18 9.5,2.42L9.13,5.07C8.5,5.32 7.96,5.66 7.44,6.05L4.95,5.05C4.73,4.96 4.46,5.05 4.34,5.27L2.34,8.73C2.22,8.95 2.27,9.22 2.46,9.37L4.57,11C4.53,11.34 4.5,11.67 4.5,12C4.5,12.33 4.53,12.65 4.57,12.97L2.46,14.63C2.27,14.78 2.22,15.05 2.34,15.27L4.34,18.73C4.46,18.95 4.73,19.03 4.95,18.95L7.44,17.94C7.96,18.34 8.5,18.68 9.13,18.93L9.5,21.58C9.54,21.82 9.75,22 10,22H14C14.25,22 14.46,21.82 14.5,21.58L14.87,18.93C15.5,18.68 16.04,18.34 16.56,17.94L19.05,18.95C19.27,19.03 19.54,18.95 19.66,18.73L21.66,15.27C21.78,15.05 21.73,14.78 21.54,14.63L19.43,12.97Z"/>
        </svg>
        <h4 style="margin: 0; color: #2d3748;">Session Controls</h4>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Clear", use_container_width=True, help="Clear conversation history", key="clear_btn"):
            st.session_state.messages = []
            st.rerun()
    
    with col2:
        if st.button("Refresh", use_container_width=True, help="Refresh system status", key="refresh_btn"):
            st.rerun()
    
    # Stats
    message_count = len(st.session_state.messages)
    st.markdown("""
    <div style="display: flex; align-items: center; gap: 0.5rem; margin-bottom: 1rem;">
        <svg width="18" height="18" fill="#4285f4" viewBox="0 0 24 24">
            <path d="M22,21H2V3H4V19H6V10H10V19H12V6H16V19H18V14H22V21Z"/>
        </svg>
        <h4 style="margin: 0; color: #2d3748;">Session Statistics</h4>
    </div>
    """, unsafe_allow_html=True)
    
    col_stat1, col_stat2 = st.columns(2)
    with col_stat1:
        st.metric("Messages", message_count)
    with col_stat2:
        st.metric("Status", "Active" if api_status else "Inactive")

# Professional Main Interface Header
st.markdown("""
<div class="main-header">
    <div class="header-content">
        <div style="display: flex; align-items: center; justify-content: center; gap: 1rem; margin-bottom: 0.5rem;">
            <svg width="40" height="40" fill="white" viewBox="0 0 24 24">
                <path d="M12,2A2,2 0 0,1 14,4C14,4.74 13.6,5.39 13,5.73V7H14A7,7 0 0,1 21,14H22A1,1 0 0,1 23,15V18A1,1 0 0,1 22,19H21V20A2,2 0 0,1 19,22H5A2,2 0 0,1 3,20V19H2A1,1 0 0,1 1,18V15A1,1 0 0,1 2,14H3A7,7 0 0,1 10,7H11V5.73C10.4,5.39 10,4.74 10,4A2,2 0 0,1 12,2Z"/>
            </svg>
            <h1>TinyLlama AI Assistant</h1>
        </div>
        <p class="header-subtitle">Advanced Conversational Intelligence • Powered by Neural Language Processing</p>
    </div>
</div>
""", unsafe_allow_html=True)

# Chat messages container
chat_container = st.container()

with chat_container:
    st.markdown('<div class="chat-messages">', unsafe_allow_html=True)
    
    # Display chat history
    for message in st.session_state.messages:
        display_message(message["content"], message["role"] == "user")
    
    # Display typing indicator if needed
    if st.session_state.is_typing:
        display_typing_indicator()
    
    st.markdown('</div>', unsafe_allow_html=True)

# Professional Chat Input Area
st.markdown('<div style="margin-bottom: 2rem;"></div>', unsafe_allow_html=True)

# Welcome message if no messages
if not st.session_state.messages:
    st.markdown("""
    <div style="text-align: center; padding: 3rem 1rem; color: #718096;">
        <svg width="64" height="64" fill="#cbd5e0" viewBox="0 0 24 24" style="margin-bottom: 1rem;">
            <path d="M20,2H4A2,2 0 0,0 2,4V22L6,18H20A2,2 0 0,0 22,16V4A2,2 0 0,0 20,2M6,9V7H18V9H6M14,11V13H6V11H14M16,15V17H6V15H16Z"/>
        </svg>
        <h3 style="color: #4a5568; margin-bottom: 0.5rem;">Welcome to TinyLlama AI Assistant</h3>
        <p style="font-size: 1.1rem; max-width: 600px; margin: 0 auto; line-height: 1.6;">
            Start a conversation with our advanced AI assistant. Ask questions, seek advice, 
            or engage in meaningful dialogue. I'm here to help with information, analysis, and creative tasks.
        </p>
        <div style="margin-top: 2rem; display: flex; gap: 1rem; justify-content: center; flex-wrap: wrap;">
            <div style="background: #f7fafc; padding: 1rem; border-radius: 8px; border: 1px solid #e2e8f0; max-width: 200px;">
                <div style="display: flex; align-items: center; gap: 0.5rem; margin-bottom: 0.5rem;">
                    <svg width="20" height="20" fill="#4285f4" viewBox="0 0 24 24">
                        <path d="M12,2A7,7 0 0,0 5,9C5,11.38 6.19,13.47 8,14.74V17A1,1 0 0,0 9,18H15A1,1 0 0,0 16,17V14.74C17.81,13.47 19,11.38 19,9A7,7 0 0,0 12,2M9,21A1,1 0 0,0 10,22H14A1,1 0 0,0 15,21V20H9V21Z"/>
                    </svg>
                    <strong style="color: #2d3748;">Ask Questions</strong>
                </div>
                <span style="font-size: 0.9rem;">Get answers on various topics</span>
            </div>
            <div style="background: #f7fafc; padding: 1rem; border-radius: 8px; border: 1px solid #e2e8f0; max-width: 200px;">
                <div style="display: flex; align-items: center; gap: 0.5rem; margin-bottom: 0.5rem;">
                    <svg width="20" height="20" fill="#4285f4" viewBox="0 0 24 24">
                        <path d="M9.5,3A6.5,6.5 0 0,1 16,9.5C16,11.11 15.41,12.59 14.44,13.73L14.71,14H15.5L20.5,19L19,20.5L14,15.5V14.71L13.73,14.44C12.59,15.41 11.11,16 9.5,16A6.5,6.5 0 0,1 3,9.5A6.5,6.5 0 0,1 9.5,3M9.5,5C7,5 5,7 5,9.5C5,12 7,14 9.5,14C12,14 14,12 14,9.5C14,7 12,5 9.5,5Z"/>
                    </svg>
                    <strong style="color: #2d3748;">Analysis</strong>
                </div>
                <span style="font-size: 0.9rem;">Deep dive into complex subjects</span>
            </div>
            <div style="background: #f7fafc; padding: 1rem; border-radius: 8px; border: 1px solid #e2e8f0; max-width: 200px;">
                <div style="display: flex; align-items: center; gap: 0.5rem; margin-bottom: 0.5rem;">
                    <svg width="20" height="20" fill="#4285f4" viewBox="0 0 24 24">
                        <path d="M12,17.27L18.18,21L16.54,13.97L22,9.24L14.81,8.62L12,2L9.19,8.62L2,9.24L7.45,13.97L5.82,21L12,17.27Z"/>
                    </svg>
                    <strong style="color: #2d3748;">Creative Tasks</strong>
                </div>
                <span style="font-size: 0.9rem;">Writing, brainstorming, and more</span>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

with st.form(key="chat_form", clear_on_submit=True):
    st.markdown("""
    <div style="margin-bottom: 0.5rem;">
        <label style="font-weight: 600; color: #2d3748; display: flex; align-items: center; gap: 0.5rem;">
            <svg width="16" height="16" fill="#4285f4" viewBox="0 0 24 24">
                <path d="M20,2H4A2,2 0 0,0 2,4V22L6,18H20A2,2 0 0,0 22,16V4A2,2 0 0,0 20,2"/>
            </svg>
            Enter your message
        </label>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns([5, 1])
    
    with col1:
        message_input = st.text_area(
            "Message",
            value="",
            height=80,
            placeholder="Type your message here... (e.g., 'Explain quantum computing' or 'Help me write a Python function')",
            label_visibility="collapsed",
            help="Enter your question or request. The AI will provide detailed, helpful responses."
        )
    
    with col2:
        st.markdown('<div style="margin-top: 1rem;"></div>', unsafe_allow_html=True)
        send_button = st.form_submit_button(
            "Send Message", 
            use_container_width=True,
            help="Send your message to the AI assistant"
        )

# Process message with professional handling
if send_button and message_input.strip():
    if not api_status:
        st.markdown("""
        <div style="background: linear-gradient(135deg, #fed7d7 0%, #feb2b2 100%); 
                    color: #742a2a; border: 1px solid #fc8181; padding: 0.75rem 1rem; 
                    border-radius: 8px; margin: 0.5rem 0; display: flex; align-items: center; gap: 0.5rem;">
            <svg width="16" height="16" fill="#742a2a" viewBox="0 0 24 24">
                <path d="M12,2C17.53,2 22,6.47 22,12C22,17.53 17.53,22 12,22C6.47,22 2,17.53 2,12C2,6.47 6.47,2 12,2M15.59,7L12,10.59L8.41,7L7,8.41L10.59,12L7,15.59L8.41,17L12,13.41L15.59,17L17,15.59L13.41,12L17,8.41L15.59,7Z"/>
            </svg>
            <span><strong>Service Unavailable</strong>: The AI backend service is currently offline. Please contact your system administrator or try again later.</span>
        </div>
        """, unsafe_allow_html=True)
    else:
        # Add user message to chat
        st.session_state.messages.append({
            "role": "user",
            "content": message_input.strip()
        })
        
        # Show typing indicator
        st.session_state.is_typing = True
        st.rerun()

# Handle API response with professional status updates
if st.session_state.is_typing and len(st.session_state.messages) > 0:
    last_message = st.session_state.messages[-1]
    
    if last_message["role"] == "user":
        # Send message to API with professional loading message
        with st.spinner("AI is processing your request... Please wait"):
            response = send_message_to_api(last_message["content"])
        
        # Add assistant response
        st.session_state.messages.append({
            "role": "assistant",
            "content": response
        })
        
        # Hide typing indicator
        st.session_state.is_typing = False
        st.rerun()

# Professional Footer
st.markdown("""
<div style="margin-top: 4rem; padding: 2rem 0; border-top: 1px solid #e2e8f0; background: #f8fafc;">
    <div style="text-align: center; max-width: 800px; margin: 0 auto;">
        <div style="display: flex; align-items: center; justify-content: center; gap: 0.8rem; margin-bottom: 1rem;">
            <svg width="24" height="24" fill="#4285f4" viewBox="0 0 24 24">
                <path d="M12,2A2,2 0 0,1 14,4C14,4.74 13.6,5.39 13,5.73V7H14A7,7 0 0,1 21,14H22A1,1 0 0,1 23,15V18A1,1 0 0,1 22,19H21V20A2,2 0 0,1 19,22H5A2,2 0 0,1 3,20V19H2A1,1 0 0,1 1,18V15A1,1 0 0,1 2,14H3A7,7 0 0,1 10,7H11V5.73C10.4,5.39 10,4.74 10,4A2,2 0 0,1 12,2Z"/>
            </svg>
            <h3 style="margin: 0; color: #2d3748; font-size: 1.4rem;">TinyLlama AI Assistant</h3>
        </div>
        <p style="color: #4a5568; font-size: 1rem; margin-bottom: 1.5rem; line-height: 1.6;">
            Enterprise-Grade Conversational AI • Powered by Advanced Neural Language Processing
        </p>
        <div style="display: flex; justify-content: center; gap: 2rem; flex-wrap: wrap; margin-bottom: 1.5rem;">
            <div style="display: flex; align-items: center; gap: 0.3rem; color: #718096; font-size: 0.9rem;">
                <svg width="14" height="14" fill="currentColor" viewBox="0 0 24 24">
                    <path d="M9,10H7V12H9V10M13,10H11V12H13V10M17,10H15V12H17V10M19,3H18V1H16V3H8V1H6V3H5C3.89,3 3,3.9 3,5V19A2,2 0 0,0 5,21H19A2,2 0 0,0 21,19V5A2,2 0 0,0 19,3M19,19H5V8H19V19Z"/>
                </svg>
                Version 1.0
            </div>
            <div style="display: flex; align-items: center; gap: 0.3rem; color: #718096; font-size: 0.9rem;">
                <svg width="14" height="14" fill="currentColor" viewBox="0 0 24 24">
                    <path d="M12,2A10,10 0 0,0 2,12A10,10 0 0,0 12,22A10,10 0 0,0 22,12A10,10 0 0,0 12,2M11,7H13V9H11V7M11,11H13V17H11V11Z"/>
                </svg>
                HuggingFace Transformers
            </div>
            <div style="display: flex; align-items: center; gap: 0.3rem; color: #718096; font-size: 0.9rem;">
                <svg width="14" height="14" fill="currentColor" viewBox="0 0 24 24">
                    <path d="M12,2L13.09,8.26L19,7L18.74,13.09L24,12L17.74,16.74L19,23L12.91,17.74L12,24L11.09,17.74L5,23L6.26,16.74L0,12L6.26,11.09L5,7L11.09,8.26L12,2Z"/>
                </svg>
                8-bit Optimized
            </div>
        </div>
        <div style="border-top: 1px solid #e2e8f0; padding-top: 1rem; color: #718096; font-size: 0.85rem;">
            <p style="margin: 0;">
                Developed by <strong>Maulana Surya Negara</strong> • 
                Built with Streamlit & FastAPI • 
                Neural Architecture: Transformer-based Language Model
            </p>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)