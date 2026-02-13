"""
LangGraph Love Orchestrator
Manages multi-agent conversation flow
"""

from typing import TypedDict, List, Dict
import operator

try:
    from langgraph.graph import StateGraph, END
    LANGGRAPH_AVAILABLE = True
except ImportError:
    LANGGRAPH_AVAILABLE = False
    print("⚠️  LangGraph not available. Install: pip install langgraph")

from agents.mood_detector import MoodDetector
from agents.memory_agent import MemoryAgent
from agents.romantic_agent import RomanticAgent
from agents.surprise_agent import SurpriseAgent
from agents.safety_agent import SafetyAgent


# Define the state that flows through the graph
class LoveState(TypedDict):
    """State maintained throughout the conversation"""
    input: str                           # User's message
    mood: str                            # Detected mood
    mood_emoji: str                      # Mood emoji
    memories: List[Dict]                 # Retrieved memories
    response: str                        # Generated response
    agent_path: List[str]               # Track which agents were used
    safe: bool                          # Safety check passed
    safety_score: int                   # Safety score


class LoveGraph:
    """Orchestrates multiple agents to respond with love"""
    
    def __init__(self, use_llm: bool = False):
        """
        Initialize the love graph
        
        Args:
            use_llm: Whether to use LLM-based agents
        """
        # Initialize all agents
        self.mood_detector = MoodDetector(llm=None)
        # ✅ CRITICAL FIX: Disable vector search to use keyword-based matching
        self.memory_agent = MemoryAgent(use_vector=False)
        self.romantic_agent = RomanticAgent(llm=None, personality="Yamraj")
        self.surprise_agent = SurpriseAgent(llm=None)
        self.safety_agent = SafetyAgent(strictness="medium")
        
        self.use_llm = use_llm
        self.graph = None
        
        if LANGGRAPH_AVAILABLE:
            self._build_graph()
    
    def _build_graph(self):
        """Build the LangGraph workflow"""
        # Create the graph
        workflow = StateGraph(LoveState)
        
        # Add nodes (each node is an agent or processing step)
        workflow.add_node("detect_mood", self._detect_mood_node)
        workflow.add_node("retrieve_memories", self._retrieve_memories_node)
        workflow.add_node("generate_romantic", self._generate_romantic_node)
        workflow.add_node("generate_surprise", self._generate_surprise_node)
        workflow.add_node("safety_check", self._safety_check_node)
        
        # Set entry point
        workflow.set_entry_point("detect_mood")
        
        # Add conditional routing based on mood
        workflow.add_conditional_edges(
            "detect_mood",
            self._route_by_mood,
            {
                "memories": "retrieve_memories",
                "surprise": "generate_surprise",
                "romantic": "generate_romantic"
            }
        )
        
        # After retrieving memories, generate romantic response
        workflow.add_edge("retrieve_memories", "generate_romantic")
        
        # After generating surprise, go to safety check
        workflow.add_edge("generate_surprise", "safety_check")
        
        # After generating romantic response, go to safety check
        workflow.add_edge("generate_romantic", "safety_check")
        
        # Safety check is the final step
        workflow.add_edge("safety_check", END)
        
        # Compile the graph
        self.graph = workflow.compile()
    
    def _detect_mood_node(self, state: LoveState) -> LoveState:
        """Node: Detect user's mood"""
        result = self.mood_detector.detect(state['input'], use_llm=self.use_llm)
        
        state['mood'] = result['mood']
        state['mood_emoji'] = result['emoji']
        state['agent_path'].append('mood_detector')
        
        return state
    
    def _retrieve_memories_node(self, state: LoveState) -> LoveState:
        """Node: Retrieve relevant memories"""
        memories = self.memory_agent.retrieve_memories(state['input'], k=2)
        
        state['memories'] = memories
        state['agent_path'].append('memory_agent')
        
        return state
    
    def _generate_romantic_node(self, state: LoveState) -> LoveState:
        """Node: Generate romantic response"""
        response = self.romantic_agent.generate_message(
            mood=state['mood'],
            context=state['input'],
            memories=state.get('memories', [])
        )
        
        state['response'] = response
        state['agent_path'].append('romantic_agent')
        
        return state
    
    def _generate_surprise_node(self, state: LoveState) -> LoveState:
        """Node: Generate surprise/date idea"""
        date_ideas = self.surprise_agent.get_date_ideas_by_mood(state['mood'])
        
        if date_ideas:
            date = date_ideas[0]
            response = f"{date['title']}\n\n{date['description']}\n\n"
            response += "Here's how:\n"
            for i, step in enumerate(date['steps'][:3], 1):
                response += f"{i}. {step}\n"
            response += f"\n💡 {date['suggestions'][0] if date['suggestions'] else ''}"
        else:
            # Fallback to romantic response
            response = self.romantic_agent.generate_message(
                mood=state['mood'],
                context=state['input']
            )
        
        state['response'] = response
        state['agent_path'].append('surprise_agent')
        
        return state
    
    def _safety_check_node(self, state: LoveState) -> LoveState:
        """Node: Check response safety"""
        check = self.safety_agent.validate_and_fix(state['response'])
        
        state['response'] = check['fixed_text']
        state['safe'] = check['fixed_safe']
        state['safety_score'] = check['fixed_score']
        state['agent_path'].append('safety_agent')
        
        return state
    
    def _route_by_mood(self, state: LoveState) -> str:
        """Decide which path to take based on mood and message content"""
        mood = state['mood']
        
        # Check if asking about memories FIRST
        message_lower = state['input'].lower()
        memory_keywords = ['first', 'remember', 'yaad', 'start', 'began', 
                           'when', 'how', 'facebook', 'message', 'kura', 'gareko', 'garya']
        
        # If asking about memories, ALWAYS retrieve them
        if any(kw in message_lower for kw in memory_keywords):
            return "memories"
        
        # Sad or stressed → Get memories for comfort
        if mood in ['sad', 'stressed', 'angry']:
            return "memories"
        
        # Happy or playful → Suggest something fun
        elif mood in ['happy', 'playful']:
            return "surprise"
        
        # Romantic or neutral → Romantic response
        else:
            return "romantic"
    
    def process_message(self, message: str) -> Dict:
        """
        Process a message through the love graph
        
        Args:
            message: User's input message
            
        Returns:
            Dict with response and metadata
        """
        if not LANGGRAPH_AVAILABLE or not self.graph:
            # Fallback to simple processing
            return self._simple_process(message)
        
        # Initialize state
        initial_state = {
            'input': message,
            'mood': '',
            'mood_emoji': '',
            'memories': [],
            'response': '',
            'agent_path': [],
            'safe': True,
            'safety_score': 100
        }
        
        # Run the graph
        try:
            final_state = self.graph.invoke(initial_state)
            
            return {
                'response': final_state['response'],
                'mood': final_state['mood'],
                'mood_emoji': final_state['mood_emoji'],
                'agent_path': final_state['agent_path'],
                'safe': final_state['safe'],
                'safety_score': final_state['safety_score'],
                'memories_used': len(final_state.get('memories', []))
            }
        except Exception as e:
            print(f"❌ Graph execution failed: {e}")
            return self._simple_process(message)
    
    def _simple_process(self, message: str) -> Dict:
        """
        Simple processing without LangGraph (fallback)
        
        Args:
            message: User's input
            
        Returns:
            Dict with response
        """
        # Detect mood
        mood_result = self.mood_detector.detect(message)
        mood = mood_result['mood']
        
        # Check for memory-related queries
        message_lower = message.lower()
        memory_keywords = ['first', 'remember', 'yaad', 'start', 'began', 
                           'when', 'how', 'facebook', 'message', 'kura', 'gareko', 'garya']
        has_memory_query = any(kw in message_lower for kw in memory_keywords)
        
        # Get memories if needed
        memories = []
        if has_memory_query or mood in ['sad', 'stressed', 'angry']:
            memories = self.memory_agent.retrieve_memories(message, k=2)
            print(f"🧠 Retrieved {len(memories)} memories")
            if memories:
                print(f"   Top memory: {memories[0].get('category')} - {memories[0].get('content')[:60]}...")
        
        # Generate response
        if mood in ['happy', 'playful'] and not has_memory_query:
            # Get surprise idea
            date_ideas = self.surprise_agent.get_date_ideas_by_mood(mood)
            if date_ideas:
                date = date_ideas[0]
                response = f"{date['title']}\n\n{date['description']}"
            else:
                response = self.romantic_agent.generate_message(mood, message, memories)
        else:
            # Romantic response (will use memories if available)
            response = self.romantic_agent.generate_message(mood, message, memories)
        
        # Safety check
        safety_result = self.safety_agent.validate_and_fix(response)
        
        return {
            'response': safety_result['fixed_text'],
            'mood': mood,
            'mood_emoji': mood_result['emoji'],
            'agent_path': ['mood_detector', 'memory_agent' if memories else '', 'romantic_agent', 'safety_agent'],
            'safe': safety_result['fixed_safe'],
            'safety_score': safety_result['fixed_score'],
            'memories_used': len(memories)
        }
    
    def get_graph_visualization(self) -> str:
        """Get a text representation of the graph structure"""
        return """
🔄 Love Graph Flow:

User Input
    ↓
[Mood Detector] → Analyzes emotion
    ↓
    ├─ Memory Query? → [Memory Agent] → [Romantic Response]
    ├─ Sad/Stressed/Angry → [Memory Agent] → [Romantic Response]
    ├─ Happy/Playful → [Surprise Planner]
    └─ Romantic/Neutral → [Romantic Response]
    ↓
[Safety Check] → Validates output
    ↓
Final Response with mood emoji
"""


# Example usage
if __name__ == "__main__":
    graph = LoveGraph()
    
    print("🔄 Love Graph Demo\n")
    print(graph.get_graph_visualization())
    
    test_messages = [
        "How did we first start talking?",
        "I miss you so much 😢",
        "I'm so happy today! 😊",
        "I love you ❤️"
    ]
    
    for msg in test_messages:
        print(f"\nInput: {msg}")
        result = graph.process_message(msg)
        print(f"Mood: {result['mood']} {result['mood_emoji']}")
        print(f"Agent Path: {' → '.join(result['agent_path'])}")
        print(f"Memories Used: {result['memories_used']}")
        print(f"Response:\n{result['response']}")
        print(f"Safety Score: {result['safety_score']}/100")
        print("-" * 50)