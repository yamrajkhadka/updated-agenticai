"""
HerAI - Streamlit Web Application
Romantic AI Assistant powered by Llama 3.3 70B
With Romanized Nepali Language Support
"""

import os
import streamlit as st
from datetime import datetime, timedelta
from typing import Dict, List
import random
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Import utilities
from utils.llm_config import get_llm_instance

# Import agents
from agents.mood_detector import MoodDetector
from agents.memory_agent import MemoryAgent
from agents.romantic_agent import RomanticAgent
from agents.surprise_agent import SurpriseAgent
from agents.safety_agent import SafetyAgent

# ⭐ NEW: Import EnhancedLoveGraph
from graph.enhanced_love_graph import EnhancedLoveGraph

# Page configuration
st.set_page_config(
    page_title="HerAI - Your Romantic AI Assistant",
    page_icon="💕",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for romantic theme
st.markdown("""
<style>
    .main {
        background: linear-gradient(135deg, #ffeef8 0%, #fff5f7 100%);
    }
    .stTextInput > div > div > input {
        background-color: #fff;
        border: 2px solid #ff69b4;
        border-radius: 20px;
        padding: 10px 15px;
    }
    .chat-message {
        padding: 1.5rem;
        border-radius: 20px;
        margin-bottom: 1rem;
        display: flex;
        flex-direction: column;
    }
    .user-message {
        background-color: #ffe4f3;
        border-left: 5px solid #ff69b4;
    }
    .ai-message {
        background-color: #f0f8ff;
        border-left: 5px solid #4a90e2;
    }
    .mood-badge {
        display: inline-block;
        padding: 0.25rem 0.75rem;
        border-radius: 15px;
        font-size: 0.85rem;
        font-weight: 600;
        margin-right: 0.5rem;
    }
    .language-badge {
        display: inline-block;
        padding: 0.25rem 0.75rem;
        border-radius: 15px;
        font-size: 0.75rem;
        font-weight: 600;
        background-color: #e8f5e9;
        color: #2e7d32;
        margin-left: 0.5rem;
    }
    .header-container {
        text-align: center;
        padding: 2rem 0;
        background: linear-gradient(135deg, #ff69b4 0%, #ff1493 100%);
        color: white;
        border-radius: 15px;
        margin-bottom: 2rem;
    }
    .stats-card {
        background-color: white;
        padding: 1rem;
        border-radius: 10px;
        border: 2px solid #ff69b4;
        margin: 0.5rem 0;
    }
</style>
""", unsafe_allow_html=True)


class ValentineSurprise:
    """Valentine's Day surprise system with rotating puzzles and gifts"""
    
    # Puzzle templates (ULTRA SIMPLE & romantic)
    PUZZLES = [
        {
            'type': 'simple',
            'question': '💕 What does Ghosu call you? (starts with C)',
            'answer': 'chuchi',
            'hint': 'Your special nickname! 😄'
        },
        {
            'type': 'simple',
            'question': '💕 Complete: I love ___',
            'answer': 'you',
            'hint': 'Three letters! ❤️'
        },
        {
            'type': 'simple',
            'question': '💕 What word does Ghosu say all the time? (S____)',
            'answer': 'sorry',
            'hint': 'Ghosu\'s favorite word! 😅'
        },
        {
            'type': 'simple',
            'question': '💕 What color is a heart? ❤️',
            'answer': 'red',
            'hint': 'The color of love!'
        },
        {
            'type': 'simple',
            'question': '💕 1 + 1 = ?',
            'answer': '2',
            'hint': 'Super easy math! 💕'
        },
        {
            'type': 'simple',
            'question': '💕 What do you call Ghosu? (starts with G)',
            'answer': 'ghosu',
            'hint': 'Your name for him! 💖'
        },
        {
            'type': 'simple',
            'question': '💕 Complete: Good _____ (when you wake up)',
            'answer': 'morning',
            'hint': 'Start of the day! ☀️'
        },
        {
            'type': 'simple',
            'question': '💕 Complete: Good _____ (before sleep)',
            'answer': 'night',
            'hint': 'End of the day! 🌙'
        },
        {
            'type': 'simple',
            'question': '💕 What month is Valentine\'s Day?',
            'answer': 'february',
            'hint': 'Month of love! 💘'
        },
        {
            'type': 'simple',
            'question': '💕 Ghosu loves Chuchi = True or False?',
            'answer': 'true',
            'hint': 'Obviously! ❤️'
        },
        {
            'type': 'simple',
            'question': '💕 Complete: Kiss and ___',
            'answer': 'hug',
            'hint': 'Warm embrace! 🤗'
        },
        {
            'type': 'simple',
            'question': '💕 What beats in your chest? ❤️',
            'answer': 'heart',
            'hint': 'Lub-dub! 💓'
        },
        {
            'type': 'simple',
            'question': '💕 2 + 2 = ?',
            'answer': '4',
            'hint': 'Easy peasy! 😊'
        },
        {
            'type': 'simple',
            'question': '💕 Roses are ___',
            'answer': 'red',
            'hint': 'First word of the poem! 🌹'
        },
        {
            'type': 'simple',
            'question': '💕 Complete: I ___ you (4 letters)',
            'answer': 'love',
            'hint': 'The best feeling! 💕'
        },
    ]
    
    # Surprise messages (15-20 different ones)
    SURPRISES = [
        {
            'type': 'poem_nepali',
            'title': '💝 Romantic Poem for Chuchi',
            'content': '''
**Mero Chuchi, Mero Jeevan**

Timi darpok, timi chuchi,
Tara mero lagi sab kichhu ❤️

Timro dar ma mero maya,
Timro hasaai ma mero khushi pani chha 😊

Ma sorry bhanchu baar baar,
Kinaki timi mero sansar 🌍

Ghosu ra Chuchi, sadhain sanga,
Yei jindagi, yei prem ko geet ga 🎵

- Your Ghosu 💕
            '''
        },
        {
            'type': 'poem_english',
            'title': '💝 A Poem for My Scaredy-Cat',
            'content': '''
**My Fearless Love**

You may be chuchi, you may be darpok,
But to me, you're everything, my heart's unlock 🔓

When you're scared, I'll hold you tight,
When you're worried, I'll make it right 🤗

Sorry I say, a thousand times,
Because loving you is my sweetest rhyme 💕

Ghosu and Chuchi, forever we'll be,
My scaredy-cat queen, you complete me 👑

- Always yours, Ghosu ❤️
            '''
        },
    ]
    
    def __init__(self):
        """Initialize Valentine Surprise"""
        self._init_session_state()
    
    def _init_session_state(self):
        """Initialize session state for Valentine surprise"""
        if 'valentine_unlocked' not in st.session_state:
            st.session_state.valentine_unlocked = False
        if 'valentine_current_surprise' not in st.session_state:
            st.session_state.valentine_current_surprise = None
        if 'valentine_unlock_time' not in st.session_state:
            st.session_state.valentine_unlock_time = None
        if 'valentine_puzzle_attempts' not in st.session_state:
            st.session_state.valentine_puzzle_attempts = 0
        if 'valentine_current_puzzles' not in st.session_state:
            st.session_state.valentine_current_puzzles = []
        if 'valentine_solved_count' not in st.session_state:
            st.session_state.valentine_solved_count = 0
        if 'valentine_total_unlocks' not in st.session_state:
            st.session_state.valentine_total_unlocks = 0
    
    def _get_random_puzzles(self, count: int = 3) -> List[Dict]:
        """Get random puzzles"""
        return random.sample(self.PUZZLES, min(count, len(self.PUZZLES)))
    
    def _get_random_surprise(self) -> Dict:
        """Get a random surprise"""
        return random.choice(self.SURPRISES)
    
    def _check_answer(self, answer: str, correct: str) -> bool:
        """Check if answer is correct (case-insensitive, stripped)"""
        return answer.strip().lower() == correct.strip().lower()
    
    def _should_reset_surprise(self) -> bool:
        """Check if 5 minutes have passed since last unlock"""
        if st.session_state.valentine_unlock_time is None:
            return False
        
        time_elapsed = datetime.now() - st.session_state.valentine_unlock_time
        return time_elapsed >= timedelta(minutes=5)
    
    def render_valentine_button(self):
        """Render the hidden Valentine button in sidebar"""
        st.markdown("---")
        st.markdown("### 💝 Special Surprise")
        
        if st.button("🎁 Valentine's Mystery Gift", use_container_width=True):
            st.session_state.show_valentine_modal = True
    
    def render_valentine_modal(self):
        """Render the Valentine surprise modal/page"""
        if not st.session_state.get('show_valentine_modal', False):
            return
        
        # Check if we should reset (5 minutes passed)
        if st.session_state.valentine_unlocked and self._should_reset_surprise():
            st.session_state.valentine_unlocked = False
            st.session_state.valentine_current_surprise = None
            st.session_state.valentine_unlock_time = None
            st.session_state.valentine_solved_count = 0
            st.session_state.valentine_current_puzzles = []
            st.balloons()
            st.info("⏰ New surprise available! Solve the puzzles to unlock it! 💕")
        
        # Main Valentine modal
        st.markdown("""
        <div style='background: linear-gradient(135deg, #ff69b4 0%, #ff1493 100%); 
                    padding: 2rem; border-radius: 20px; text-align: center; color: white;'>
            <h1>💝 Valentine's Mystery Box 💝</h1>
            <p style='font-size: 1.2rem;'>Special surprises from Ghosu to Chuchi!</p>
            <p style='font-size: 0.9rem;'>Solve 3 easy puzzles to unlock each surprise 🎁</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        # Show stats
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("🎯 Puzzles Solved", st.session_state.valentine_solved_count)
        
        with col2:
            st.metric("🎁 Surprises Unlocked", st.session_state.valentine_total_unlocks)
        
        with col3:
            if st.session_state.valentine_unlock_time:
                time_until_next = timedelta(minutes=5) - (datetime.now() - st.session_state.valentine_unlock_time)
                mins = max(0, int(time_until_next.total_seconds() / 60))
                st.metric("⏰ Next Surprise In", f"{mins}m")
            else:
                st.metric("⏰ Next Surprise In", "Solve puzzles!")
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        # If unlocked, show surprise
        if st.session_state.valentine_unlocked:
            surprise = st.session_state.valentine_current_surprise
            st.success("🎉 SURPRISE UNLOCKED! 🎉")
            
            st.markdown(f"""
            <div style='background: white; padding: 2rem; border-radius: 15px; 
                        border: 3px solid #ff69b4; margin: 1rem 0;'>
                <h2 style='color: #ff1493; text-align: center;'>{surprise['title']}</h2>
                <div style='white-space: pre-line; line-height: 1.8; margin-top: 1rem;'>
{surprise['content']}
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            st.info("💕 A new surprise will be ready in 5 minutes! Come back to unlock it!")
            
            if st.button("🔙 Back to Chat", use_container_width=True):
                st.session_state.show_valentine_modal = False
                st.rerun()
        
        else:
            # Show puzzles
            st.info("💡 Solve all 3 puzzles to unlock your Valentine surprise!")
            
            # Generate puzzles if not exists
            if not st.session_state.valentine_current_puzzles:
                st.session_state.valentine_current_puzzles = self._get_random_puzzles(3)
            
            # Display puzzles
            for idx, puzzle in enumerate(st.session_state.valentine_current_puzzles, 1):
                with st.container():
                    st.markdown(f"### Puzzle {idx}/3")
                    st.write(puzzle['question'])
                    
                    # Show hint button
                    if st.button(f"💡 Show Hint", key=f"hint_{idx}"):
                        st.info(f"Hint: {puzzle['hint']}")
                    
                    # Answer input
                    answer = st.text_input(
                        "Your answer:",
                        key=f"puzzle_answer_{idx}",
                        placeholder="Type your answer here..."
                    )
                    
                    if answer:
                        if self._check_answer(answer, puzzle['answer']):
                            st.success("✅ Correct! Well done! 💕")
                            # Mark as solved
                            if f"puzzle_{idx}_solved" not in st.session_state:
                                st.session_state[f"puzzle_{idx}_solved"] = True
                                st.session_state.valentine_solved_count += 1
                        else:
                            st.error("❌ Not quite! Try again! 💪")
                    
                    st.markdown("---")
            
            # Check if all puzzles solved
            all_solved = all(
                st.session_state.get(f"puzzle_{i}_solved", False)
                for i in range(1, 4)
            )
            
            if all_solved:
                st.balloons()
                st.success("🎉 ALL PUZZLES SOLVED! 🎉")
                
                if st.button("🎁 UNLOCK MY SURPRISE!", use_container_width=True, type="primary"):
                    # Unlock surprise
                    st.session_state.valentine_unlocked = True
                    st.session_state.valentine_current_surprise = self._get_random_surprise()
                    st.session_state.valentine_unlock_time = datetime.now()
                    st.session_state.valentine_total_unlocks += 1
                    
                    # Reset puzzle states
                    for i in range(1, 4):
                        if f"puzzle_{i}_solved" in st.session_state:
                            del st.session_state[f"puzzle_{i}_solved"]
                    
                    st.balloons()
                    st.rerun()
            
            st.markdown("<br>", unsafe_allow_html=True)
            
            if st.button("🔙 Back to Chat", use_container_width=True):
                st.session_state.show_valentine_modal = False
                st.rerun()


class LanguageWrapper:
    """Wrapper to add language instructions without modifying romantic_agent"""
    
    @staticmethod
    def get_nepali_instruction() -> str:
        """Get Nepali language instruction to prepend to prompts"""
        return """
🇳🇵 CRITICAL: Respond in ROMANIZED NEPALI (Nepali in English script).

Examples of correct romanized Nepali:
- "Ma timilai maya garchu" (not "I love you")
- "Kasto chau?" (not "How are you?")
- "Subha prabhat mero maya!" (not "Good morning my love!")
- "Hajur, ma yaha chhu" (Yes, I'm here)
- "Timi mero jeevan ho" (You are my life)
- "Kina udaas chau?" (Why are you sad?)

Natural mixing is OK: "Ma office bata aairathe" (mixing "office")

Use Nepali sentence structure. DO NOT respond in pure English.

---
"""
    
    @staticmethod
    def wrap_context_for_nepali(context: str) -> str:
        """Wrap context with Nepali instruction"""
        return LanguageWrapper.get_nepali_instruction() + context
    
    @staticmethod
    def get_nepali_system_context() -> str:
        """Get system context for Nepali responses"""
        return """[Language Setting: ROMANIZED NEPALI - All responses must be in Nepali written in English script]
"""


class HerAIApp:
    """Streamlit HerAI Application with Enhanced Love Graph"""
    
    def __init__(self):
        """Initialize HerAI"""
        # Initialize session state
        if 'initialized' not in st.session_state:
            self._initialize_session_state()
        
        # Initialize HerAI components
        if 'herai_ready' not in st.session_state:
            self._initialize_herai()
    
    def _initialize_session_state(self):
        """Initialize Streamlit session state"""
        st.session_state.initialized = True
        st.session_state.messages = []
        st.session_state.mood_history = []
        st.session_state.conversation_count = 0
        st.session_state.api_key_set = False
        st.session_state.current_language = "Romanized Nepali"  # Default language
    
    def _initialize_herai(self):
        """Initialize HerAI components"""
        with st.spinner("💕 Initializing HerAI..."):
            try:
                # Get API key - try multiple sources
                api_key = None
                
                # 1. Try Streamlit secrets (for Streamlit Cloud)
                try:
                    api_key = st.secrets.get("GROQ_API_KEY")
                    if api_key:
                        st.sidebar.info(f"🔑 Using Streamlit secrets (key starts with: {api_key[:7]}...)")
                except Exception as e:
                    st.sidebar.warning(f"⚠️ Could not read from secrets: {str(e)}")
                
                # 2. Try environment variable (for local .env)
                if not api_key:
                    api_key = os.getenv("GROQ_API_KEY")
                    if api_key:
                        st.sidebar.info("🔑 Using environment variable")
                
                # 3. Try session state (user entered via UI)
                if not api_key:
                    api_key = st.session_state.get('user_api_key')
                    if api_key:
                        st.sidebar.info("🔑 Using user-provided key")
                
                if not api_key:
                    st.sidebar.error("❌ No API key found in any source!")
                
                # Get LLM instance
                llm = get_llm_instance(api_key)
                st.session_state.use_llm = llm is not None
                
                # ⭐ Initialize EnhancedLoveGraph with proactive messaging DISABLED
                st.session_state.love_graph = EnhancedLoveGraph(
                    llm=llm,
                    enable_proactive=False  # DISABLED to prevent token wastage
                )
                
                # Keep individual agents for backward compatibility
                st.session_state.mood_detector = MoodDetector(llm=llm)
                st.session_state.memory_agent = MemoryAgent()
                st.session_state.romantic_agent = RomanticAgent(llm=llm, personality="Yamraj")
                st.session_state.surprise_agent = SurpriseAgent(llm=llm)
                st.session_state.safety_agent = SafetyAgent(strictness="medium")
                
                st.session_state.herai_ready = True
                st.session_state.api_key_set = llm is not None
                
            except Exception as e:
                st.error(f"Error initializing HerAI: {e}")
                st.session_state.herai_ready = False
    
    def _detect_task_type(self, message: str) -> str:
        """Detect if message is asking for a specific task"""
        message_lower = message.lower()
        
        if any(word in message_lower for word in ['write a poem', 'poem for', 'make a poem']):
            return 'poem'
        elif any(word in message_lower for word in ['write a joke', 'tell me a joke', 'joke about yamraj', 'make fun of yourself']):
            return 'joke'
        elif any(word in message_lower for word in ['write a story', 'tell me a story']):
            return 'story'
        elif any(word in message_lower for word in ['write a letter', 'love letter']):
            return 'letter'
        elif any(word in message_lower for word in ['plan a date', 'date idea', 'what should we do']):
            return 'date_plan'
        elif any(word in message_lower for word in ['good morning', 'morning']):
            return 'good_morning'
        elif any(word in message_lower for word in ['good night', 'night']):
            return 'good_night'
        elif any(word in message_lower for word in ['sorry', 'apologize', 'my bad']):
            return 'apology'
        
        return None
    
    def _apply_language_wrapper(self, response: str, task_type: str = None) -> str:
        """
        Apply language translation if needed.
        This uses LLM to translate English responses to Nepali.
        """
        if st.session_state.current_language != "Romanized Nepali":
            return response
        
        # If already in Nepali (contains Nepali words), return as is
        nepali_indicators = ['ma ', 'timi', 'chau', 'garchu', 'bhayo', 'huncha', 'thiyo', 'hajur', 'mero', 'timro']
        if any(indicator in response.lower() for indicator in nepali_indicators):
            return response
        
        # Otherwise, try to translate using LLM
        if st.session_state.use_llm and st.session_state.get('romantic_agent'):
            try:
                llm = get_llm_instance(os.getenv("GROQ_API_KEY") or st.session_state.get('user_api_key'))
                if llm:
                    translate_prompt = f"""Translate this romantic message to ROMANIZED NEPALI (Nepali written in English script).

Original message: {response}

IMPORTANT: 
- Use romanized Nepali (Nepali words in English/Latin script)
- Examples: "Ma timilai maya garchu" not "I love you"
- "Kasto chau?" not "How are you?"
- Keep the same emotion and meaning
- Natural mixing of English words is OK

Romanized Nepali translation:"""

                    translated = llm.invoke(translate_prompt)
                    translated_text = translated.content if hasattr(translated, 'content') else str(translated)
                    return translated_text.strip()
            except:
                pass
        
        return response
    
    def process_message(self, message: str) -> Dict:
        """Process a message using EnhancedLoveGraph"""
        use_nepali = st.session_state.current_language == "Romanized Nepali"
        
        # Use EnhancedLoveGraph for processing
        try:
            # Wrap message with Nepali instruction if needed
            if use_nepali:
                message = LanguageWrapper.wrap_context_for_nepali(message)
            
            # Process through love graph
            result = st.session_state.love_graph.process_message(message)
            
            # Apply language wrapper if needed
            response = self._apply_language_wrapper(result['response'])
            
            return {
                'response': response,
                'mood': result.get('mood', 'happy'),
                'mood_emoji': result.get('mood_emoji', '😊'),
                'safe': result.get('safe', True),
                'safety_score': result.get('safety_score', 1.0),
                'task_type': result.get('task_type')
            }
            
        except Exception as e:
            st.error(f"Error processing message: {e}")
            # Fallback to simple response
            return {
                'response': "Ma timilai maya garchu! ❤️" if use_nepali else "I love you! ❤️",
                'mood': 'happy',
                'mood_emoji': '😊',
                'safe': True,
                'safety_score': 1.0,
                'task_type': None
            }
    
    def render_header(self):
        """Render app header"""
        st.markdown("""
        <div class="header-container">
            <h1>💕 HerAI - Your Romantic AI Assistant</h1>
            <p style="font-size: 1.2rem; margin-top: 0.5rem;">
                Powered by Llama 3.3 70B through Groq
            </p>
            <p style="font-size: 0.9rem; margin-top: 0.5rem; opacity: 0.9;">
                ✨ With Enhanced Love Graph
            </p>
        </div>
        """, unsafe_allow_html=True)
    
    def render_sidebar(self):
        """Render sidebar with stats and settings"""
        with st.sidebar:
            st.header("⚙️ Settings")
            
            # API Key configuration
            if not st.session_state.api_key_set:
                st.warning("⚠️ No API key configured")
                api_key = st.text_input(
                    "Groq API Key",
                    type="password",
                    help="Enter your Groq API key for best experience"
                )
                if st.button("Set API Key"):
                    if api_key:
                        st.session_state.user_api_key = api_key
                        st.session_state.herai_ready = False
                        self._initialize_herai()
                        st.rerun()
            else:
                st.success("✅ API Key configured")
                if st.button("Change API Key"):
                    st.session_state.api_key_set = False
                    st.session_state.herai_ready = False
                    st.rerun()
            
            st.divider()
            
            # Language Settings
            st.header("🌐 Language")
            language_option = st.radio(
                "Yamraj's Response Language",
                options=["Romanized Nepali 🇳🇵", "English 🇬🇧"],
                index=0,  # Default to Nepali
                help="Choose the language for Yamraj's responses"
            )
            
            # Update language preference
            new_language = "Romanized Nepali" if "Nepali" in language_option else "English"
            if st.session_state.current_language != new_language:
                st.session_state.current_language = new_language
                st.success(f"Language changed to {new_language}!")
            
            # Show language examples
            if "Nepali" in language_option:
                st.info("📝 Yamraj will speak in romanized Nepali:\n- 'Ma timilai maya garchu'\n- 'Kasto chau?'\n- 'Subha prabhat!'")
            else:
                st.info("📝 Yamraj will speak in English:\n- 'I love you'\n- 'How are you?'\n- 'Good morning!'")
            
            st.divider()
            
            # Statistics
            st.header("📊 Statistics")
            col1, col2 = st.columns(2)
            
            with col1:
                st.metric("Messages", st.session_state.conversation_count)
            
            with col2:
                if st.session_state.mood_history:
                    recent_mood = st.session_state.mood_history[-1]
                    st.metric("Current Mood", recent_mood)
            
            # Mood history
            if st.session_state.mood_history:
                st.subheader("Mood Trends")
                mood_counts = {}
                for mood in st.session_state.mood_history:
                    mood_counts[mood] = mood_counts.get(mood, 0) + 1
                
                for mood, count in sorted(mood_counts.items(), key=lambda x: x[1], reverse=True):
                    st.write(f"• {mood.capitalize()}: {count}")
            
            st.divider()
            
            # Actions
            st.header("🎯 Quick Actions")
            
            if st.button("✨ Plan a Date"):
                st.session_state.quick_message = "Plan a virtual date for us"
            
            if st.button("📝 Write a Poem"):
                st.session_state.quick_message = "Write a poem for me about love"
            
            if st.button("😄 Tell a Joke"):
                st.session_state.quick_message = "Tell me a joke about yourself Yamraj"
            
            if st.button("🌅 Good Morning"):
                st.session_state.quick_message = "Good morning"
            
            if st.button("🌙 Good Night"):
                st.session_state.quick_message = "Good night"
            
            if st.button("🔄 Clear Chat"):
                st.session_state.messages = []
                st.session_state.mood_history = []
                st.session_state.conversation_count = 0
                st.rerun()
            
            # Valentine Surprise Button
            st.divider()
            valentine = ValentineSurprise()
            valentine.render_valentine_button()
    
    def render_chat_message(self, role: str, content: str, mood: str = None, mood_emoji: str = None):
        """Render a chat message"""
        if role == "user":
            st.markdown(f"""
            <div class="chat-message user-message">
                <div style="font-weight: 600; color: #ff69b4; margin-bottom: 0.5rem;">
                    👩 Chuchi-Maya
                </div>
                <div>{content}</div>
            </div>
            """, unsafe_allow_html=True)
        else:
            mood_badge = f'<span class="mood-badge" style="background-color: #ffe4f3; color: #ff1493;">{mood_emoji} {mood}</span>' if mood else ''
            lang_badge = f'<span class="language-badge">🇳🇵 NP</span>' if st.session_state.current_language == "Romanized Nepali" else '<span class="language-badge">🇬🇧 EN</span>'
            
            st.markdown(f"""
            <div class="chat-message ai-message">
                <div style="font-weight: 600; color: #4a90e2; margin-bottom: 0.5rem;">
                    💕 Ghosu {mood_badge}{lang_badge}
                </div>
                <div>{content}</div>
            </div>
            """, unsafe_allow_html=True)
    
    def run(self):
        """Run the Streamlit app"""
        # Render header
        self.render_header()
        
        # Check and render Valentine modal if active
        valentine = ValentineSurprise()
        valentine.render_valentine_modal()
        if st.session_state.get('show_valentine_modal', False):
            return  # Don't render chat when Valentine modal is active
        
        # Render sidebar
        self.render_sidebar()
        
        # Check if HerAI is ready
        if not st.session_state.herai_ready:
            st.warning("HerAI is initializing or not configured properly. Please check your API key.")
            return
        
        # Display mode indicator
        if not st.session_state.use_llm:
            st.info("ℹ️ Running in fallback mode (no LLM). Set your GROQ_API_KEY for the best experience.")
        
        # Display current language
        lang_emoji = "🇳🇵" if st.session_state.current_language == "Romanized Nepali" else "🇬🇧"
        st.info(f"{lang_emoji} Language: **{st.session_state.current_language}** - Change in sidebar")
        
        # Chat container
        chat_container = st.container()
        
        # Display chat history
        with chat_container:
            for msg in st.session_state.messages:
                self.render_chat_message(
                    msg['role'],
                    msg['content'],
                    msg.get('mood'),
                    msg.get('mood_emoji')
                )
        
        # Chat input
        st.divider()
        
        # Handle quick messages
        default_message = st.session_state.get('quick_message', '')
        if default_message:
            del st.session_state.quick_message
        
        user_input = st.chat_input("Type your message here...", key="chat_input")
        
        if user_input or default_message:
            message = user_input or default_message
            
            # Add user message to history
            st.session_state.messages.append({
                'role': 'user',
                'content': message
            })
            
            # Process message
            with st.spinner("💭 Yamraj is thinking..."):
                try:
                    result = self.process_message(message)
                    
                    # Add AI response to history
                    st.session_state.messages.append({
                        'role': 'assistant',
                        'content': result['response'],
                        'mood': result['mood'],
                        'mood_emoji': result['mood_emoji']
                    })
                    
                    # Update statistics
                    st.session_state.conversation_count += 1
                    st.session_state.mood_history.append(result['mood'])
                    
                except Exception as e:
                    st.error(f"❌ Error: {e}")
            
            # Rerun to update chat
            st.rerun()


def main():
    """Main entry point"""
    app = HerAIApp()
    app.run()


if __name__ == "__main__":
    main()
