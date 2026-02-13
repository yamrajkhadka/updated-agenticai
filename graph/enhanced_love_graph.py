"""
Enhanced Love Graph with Proactive Engagement
Manages conversation flow AND sends proactive messages after inactivity
"""

from typing import TypedDict, List, Dict, Optional
from datetime import datetime
import threading
import time

try:
    from langgraph.graph import StateGraph, END
    LANGGRAPH_AVAILABLE = True
except ImportError:
    LANGGRAPH_AVAILABLE = False
    print("⚠️ LangGraph not available. Install: pip install langgraph")

from agents.mood_detector import MoodDetector
from agents.memory_agent import MemoryAgent
from agents.romantic_agent import RomanticAgent
from agents.surprise_agent import SurpriseAgent
from agents.safety_agent import SafetyAgent


class LoveState(TypedDict):
    """State maintained throughout the conversation"""
    input: str
    mood: str
    mood_emoji: str
    memories: List[Dict]
    response: str
    agent_path: List[str]
    safe: bool
    safety_score: int


class EnhancedLoveGraph:
    """
    Orchestrates multiple agents with proactive engagement
    """
    
    def __init__(self, llm=None, enable_proactive: bool = True):
        """
        Initialize the enhanced love graph
        
        Args:
            llm: Language model for agents
            enable_proactive: Enable proactive messaging
        """
        # Initialize all agents
        self.llm = llm
        self.mood_detector = MoodDetector(llm=llm)
        self.memory_agent = MemoryAgent()
        
        # Import the enhanced romantic agent
        from agents.romantic_agent_enhanced import RomanticAgent as EnhancedRomanticAgent
        self.romantic_agent = EnhancedRomanticAgent(
            personality_config={'character': 'You are Yamraj (Ghosu)'},
            llm=llm  # Pass the LLM instance
        )
        
        self.surprise_agent = SurpriseAgent(llm=llm)
        self.safety_agent = SafetyAgent(strictness="medium")
        
        # Proactive engagement
        self.enable_proactive = enable_proactive
        if enable_proactive:
            from agents.proactive_agent import ProactiveAgent
            self.proactive_agent = ProactiveAgent(llm=llm)
            self.proactive_thread = None
            self.proactive_running = False
            self.proactive_callback = None
        
        self.last_mood = 'neutral'
        
    def process_message(self, message: str) -> Dict:
        """
        Process incoming message with MEMORY-FIRST approach
        
        Args:
            message: User's message
            
        Returns:
            Response dict
        """
        # Stop proactive messaging when user sends message
        if self.enable_proactive:
            self.stop_proactive_monitoring()
            self.proactive_agent.update_activity()
        
        # Step 1: Detect mood
        mood_result = self.mood_detector.detect(message, use_llm=True)
        mood = mood_result['mood']
        self.last_mood = mood
        
        print(f"\n📊 Mood detected: {mood} {mood_result['emoji']}")
        
        # Step 2: ALWAYS retrieve memories (not just for sad moods)
        # This is the KEY change - check memories for EVERY message
        memories = self.memory_agent.retrieve_memories(message, k=3)
        print(f"🧠 Retrieved {len(memories)} memories")
        if memories:
            print(f"   Top memory: {memories[0].get('category')} - {memories[0].get('content')[:60]}...")
        
        # Step 3: Generate response with MEMORY-FIRST approach
        response_result = self.romantic_agent.generate(
            message=message,
            mood=mood,
            context=message,
            memories=memories
        )
        
        # Step 4: Safety check
        safety_result = self.safety_agent.validate_and_fix(response_result['response'])
        
        # Start proactive monitoring after response
        if self.enable_proactive:
            self.start_proactive_monitoring()
        
        return {
            'response': safety_result['fixed_text'],
            'mood': mood,
            'mood_emoji': mood_result['emoji'],
            'memories_used': len(memories) if response_result['memory_used'] else 0,
            'memory_category': response_result.get('memory_category'),
            'safe': safety_result['fixed_safe'],
            'safety_score': safety_result['fixed_score']
        }
    
    def start_proactive_monitoring(self):
        """Start monitoring for inactivity"""
        if not self.enable_proactive:
            return
        
        if self.proactive_running:
            return  # Already running
        
        self.proactive_running = True
        self.proactive_thread = threading.Thread(
            target=self._proactive_monitor_loop,
            daemon=True
        )
        self.proactive_thread.start()
        print("🔔 Proactive monitoring started")
    
    def stop_proactive_monitoring(self):
        """Stop monitoring for inactivity"""
        if not self.enable_proactive:
            return
        
        self.proactive_running = False
        if self.proactive_thread:
            self.proactive_thread = None
        print("🔕 Proactive monitoring stopped")
    
    def _proactive_monitor_loop(self):
        """Background thread that monitors inactivity"""
        while self.proactive_running:
            time.sleep(5)  # Check every 5 seconds
            
            if self.proactive_agent.should_send_proactive_message():
                # Generate and send proactive message
                context = {
                    'last_mood': self.last_mood,
                    'time': datetime.now()
                }
                
                proactive_msg = self.proactive_agent.generate_proactive_message(context)
                
                # Trigger callback if set
                if self.proactive_callback:
                    self.proactive_callback(proactive_msg)
                else:
                    print(f"\n🔔 PROACTIVE MESSAGE:")
                    print(f"   {proactive_msg}")
                
                # Reset timer after sending
                self.proactive_agent.update_activity()
    
    def set_proactive_callback(self, callback):
        """
        Set callback for proactive messages
        
        Args:
            callback: Function to call with proactive message
        """
        self.proactive_callback = callback
    
    def get_stats(self) -> Dict:
        """Get system stats"""
        memory_stats = self.memory_agent.get_stats()
        
        stats = {
            'total_memories': memory_stats['total_memories'],
            'proactive_enabled': self.enable_proactive,
            'last_mood': self.last_mood
        }
        
        if self.enable_proactive:
            time_since = self.proactive_agent.get_time_since_last_message()
            stats['seconds_since_last_message'] = time_since
            stats['will_send_proactive_in'] = max(0, 60 - time_since) if time_since else None
        
        return stats


# Example usage with proactive messaging
if __name__ == "__main__":
    print("💕 Enhanced Love Graph with Proactive Engagement\n")
    
    # Initialize graph with proactive messaging
    graph = EnhancedLoveGraph(enable_proactive=True)
    
    # Set callback for proactive messages
    def handle_proactive(message):
        print(f"\n🔔 [PROACTIVE] Yamraj says: {message}")
    
    graph.set_proactive_callback(handle_proactive)
    
    # Simulate conversation
    messages = [
        "How did we first start talking?",
        "I miss you",
    ]
    
    for msg in messages:
        print(f"\n👩 Chuchi-Maya: {msg}")
        result = graph.process_message(msg)
        print(f"💕 Ghosu: {result['response']}")
        print(f"   Mood: {result['mood']} | Memories: {result['memories_used']}")
        
        time.sleep(2)
    
    # Wait to see proactive message
    print("\n⏳ Waiting for 1 minute of silence...")
    print("   (Proactive message should appear after 60 seconds)")
    
    try:
        time.sleep(70)  # Wait for proactive message
    except KeyboardInterrupt:
        print("\n\n✅ Demo interrupted")
    
    graph.stop_proactive_monitoring()
    print("\n✅ Demo complete")