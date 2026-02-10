"""
HerAI - Streamlit App
A Love Agent System built with LangChain + LangGraph
"""

import streamlit as st
from datetime import datetime
import sys
import os

# Add current directory to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from agents.mood_detector import MoodDetector
from agents.memory_agent import MemoryAgent
from agents.romantic_agent import RomanticAgent
from agents.surprise_agent import SurpriseAgent
from agents.safety_agent import SafetyAgent
from graph.love_graph import LoveGraph


# Page config
st.set_page_config(
    page_title="HerAI - Your Love Agent",
    page_icon="💖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    }
    .stTextInput > div > div > input {
        background-color: #f0f0f0;
    }
    .stButton > button {
        background-color: #ff6b9d;
        color: white;
        border-radius: 20px;
        border: none;
        padding: 10px 24px;
        font-weight: bold;
    }
    .stButton > button:hover {
        background-color: #ff4d88;
    }
    h1 {
        color: #fff;
        text-align: center;
        font-family: 'Arial', sans-serif;
    }
    .love-message {
        background-color: #ffe6f0;
        padding: 20px;
        border-radius: 15px;
        margin: 10px 0;
        border-left: 5px solid #ff6b9d;
    }
    .agent-info {
        background-color: #f0e6ff;
        padding: 10px;
        border-radius: 10px;
        font-size: 12px;
        color: #666;
    }
</style>
""", unsafe_allow_html=True)


# Initialize session state
if 'initialized' not in st.session_state:
    st.session_state.initialized = True
    st.session_state.chat_history = []
    st.session_state.first_visit = True
    
    # Initialize the love graph (it creates all agents internally)
    st.session_state.love_graph = LoveGraph(use_llm=False)
    
    # Get references to the agents for sidebar functionality
    st.session_state.mood_detector = st.session_state.love_graph.mood_detector
    st.session_state.memory_agent = st.session_state.love_graph.memory_agent
    st.session_state.romantic_agent = st.session_state.love_graph.romantic_agent
    st.session_state.surprise_agent = st.session_state.love_graph.surprise_agent
    st.session_state.safety_agent = st.session_state.love_graph.safety_agent


def display_message(role: str, content: str, metadata: dict = None):
    """Display a chat message"""
    if role == "user":
        st.markdown(f"""
        <div style='text-align: right; margin: 10px 0;'>
            <span style='background-color: #e3f2fd; padding: 10px 15px; 
                        border-radius: 15px; display: inline-block;'>
                {content}
            </span>
        </div>
        """, unsafe_allow_html=True)
    else:
        mood_emoji = metadata.get("mood_emoji", "💖") if metadata else "💖"
        st.markdown(f"""
        <div class='love-message'>
            <div style='font-size: 24px; margin-bottom: 10px;'>{mood_emoji}</div>
            <div>{content}</div>
        </div>
        """, unsafe_allow_html=True)
        
        if metadata and st.session_state.get('show_debug', False):
            agent_path = ' → '.join(metadata.get('agent_path', [])) if metadata.get('agent_path') else 'N/A'
            st.markdown(f"""
            <div class='agent-info'>
                <b>Agent Path:</b> {agent_path}<br>
                <b>Mood:</b> {metadata.get('mood', 'N/A')}<br>
                <b>Safety Score:</b> {metadata.get('safety_score', 'N/A')}/100
            </div>
            """, unsafe_allow_html=True)


def main():
    # Title
    st.markdown("<h1>💖 HerAI - Your Love Agent</h1>", unsafe_allow_html=True)
    
    # Welcome message
    if st.session_state.first_visit:
        st.markdown("""
        <div class='love-message' style='background-color: #fff0f5;'>
            <h3>Hi there! 💕</h3>
            <p>I'm HerAI, an AI trained by someone who loves you deeply. 
            I can write poems, plan surprises, remember your special moments, 
            and just be here for you whenever you need.</p>
            <p><i>What's on your mind today?</i></p>
        </div>
        """, unsafe_allow_html=True)
        st.session_state.first_visit = False
    
    # Sidebar
    with st.sidebar:
        st.markdown("### 💝 Quick Actions")
        
        col1, col2 = st.columns(2)
        
        with col1:
            if st.button("✨ Write Something Special"):
                user_input = "Write me something special"
                st.session_state.sidebar_input = user_input
        
        with col2:
            if st.button("🎁 Surprise Idea"):
                user_input = "Give me a surprise idea"
                st.session_state.sidebar_input = user_input
        
        if st.button("🧠 What Do You Remember?"):
            user_input = "What do you remember about us?"
            st.session_state.sidebar_input = user_input
        
        if st.button("💌 Good Morning Message"):
            greeting = st.session_state.romantic_agent.generate_greeting(
                "good morning", 
                use_llm=False
            )
            st.session_state.chat_history.append({
                "role": "assistant",
                "content": greeting,
                "metadata": {"mood_emoji": "🌅", "mood": "morning"}
            })
            st.rerun()
        
        st.markdown("---")
        st.markdown("### ⚙️ Settings")
        st.session_state.show_debug = st.checkbox("Show Agent Debug Info", value=False)
        
        st.markdown("---")
        st.markdown("### 📊 Stats")
        st.write(f"💬 Messages: {len(st.session_state.chat_history)}")
        memory_count = len(st.session_state.memory_agent.memories)
        st.write(f"🧠 Memories: {memory_count}")
        
        st.markdown("---")
        st.markdown("### 💡 About")
        st.markdown("""
        <small>
        HerAI is a multi-agent system built with:
        - 🧠 LangChain
        - 🔄 LangGraph
        - 💾 FAISS (Vector Memory)
        - 🎨 Streamlit
        
        Created with love 💕
        </small>
        """, unsafe_allow_html=True)
    
    # Display chat history
    for message in st.session_state.chat_history:
        display_message(
            message["role"],
            message["content"],
            message.get("metadata")
        )
    
    # Check for sidebar input
    if hasattr(st.session_state, 'sidebar_input'):
        user_input = st.session_state.sidebar_input
        del st.session_state.sidebar_input
        
        # Add user message
        st.session_state.chat_history.append({
            "role": "user",
            "content": user_input
        })
        
        # Get response
        with st.spinner("💭 Thinking with love..."):
            result = st.session_state.love_graph.process_message(user_input)
        
        # Add assistant message
        st.session_state.chat_history.append({
            "role": "assistant",
            "content": result["response"],
            "metadata": result
        })
        
        st.rerun()
    
    # Input area
    with st.container():
        col1, col2 = st.columns([6, 1])
        
        with col1:
            user_input = st.text_input(
                "Message HerAI...",
                key="user_input",
                placeholder="Type your message here... 💕",
                label_visibility="collapsed"
            )
        
        with col2:
            send_button = st.button("Send 💌", use_container_width=True)
    
    # Handle send
    if send_button and user_input:
        # Add user message
        st.session_state.chat_history.append({
            "role": "user",
            "content": user_input
        })
        
        # Get response
        with st.spinner("💭 Thinking with love..."):
            result = st.session_state.love_graph.process_message(user_input)
        
        # Add assistant message
        st.session_state.chat_history.append({
            "role": "assistant",
            "content": result["response"],
            "metadata": result
        })
        
        st.rerun()
    
    # Footer
    st.markdown("---")
    st.markdown("""
    <div style='text-align: center; color: white; padding: 20px;'>
        <p>Made with 💖 for someone special</p>
        <p><small>Remember: This is more than code. This is a piece of my heart.</small></p>
    </div>
    """, unsafe_allow_html=True)


if __name__ == "__main__":
    main()