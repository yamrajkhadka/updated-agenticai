"""
HerAI Demo Script
Tests all components of the Love Agent System
"""

import sys
import os

# Add current directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from agents.mood_detector import MoodDetector
from agents.memory_agent import MemoryAgent
from agents.romantic_agent import RomanticAgent
from agents.surprise_agent import SurprisePlanner
from agents.safety_agent import SafetyAgent
from graph.love_graph import LoveGraph


def print_section(title):
    """Print formatted section header"""
    print("\n" + "=" * 60)
    print(f"  {title}")
    print("=" * 60)


def test_mood_detector():
    """Test mood detection"""
    print_section("🎵 MOOD DETECTION AGENT")
    
    detector = MoodDetector(llm=None)
    
    test_messages = [
        "I love you so much baby! 💕",
        "I'm feeling really sad and lonely today...",
        "Haha that's hilarious! 😂",
        "I'm so stressed with all this work",
        "Hey, what's up? Just chilling",
        "You make me so angry sometimes!"
    ]
    
    for msg in test_messages:
        mood = detector.detect(msg, use_llm=False)
        emoji = detector.get_mood_emoji(mood)
        desc = detector.get_mood_description(mood)
        print(f"\n{emoji} '{msg}'")
        print(f"   Detected: {mood} - {desc}")


def test_memory_agent():
    """Test memory storage and retrieval"""
    print_section("🧠 MEMORY AGENT (RAG)")
    
    agent = MemoryAgent(memory_file="memory/memories.json")
    
    print("\n📊 Memory Summary:")
    print(agent.get_memory_summary())
    
    # Test queries
    queries = [
        "What's her favorite color?",
        "Tell me about our first date",
        "What special moments do we have?"
    ]
    
    for query in queries:
        print(f"\n🔍 Query: '{query}'")
        memories = agent.retrieve_memories(query, top_k=2)
        print(agent.format_memories_for_context(memories))


def test_romantic_agent():
    """Test romantic message generation"""
    print_section("💌 ROMANTIC AGENT")
    
    agent = RomanticAgent(llm=None, personality="Yamraj")
    
    print("\n🎭 Testing different moods:\n")
    
    moods = ["sad", "happy", "romantic", "stressed"]
    
    for mood in moods:
        msg = agent.generate_romantic_message(
            "I've been thinking about you",
            mood=mood,
            use_llm=False
        )
        print(f"{mood.upper()}:")
        print(f"  {msg}\n")
    
    print("\n📜 Sample Poem:")
    poem = agent._fallback_poem()
    print(f"  {poem}\n")
    
    print("\n🌅 Good Morning Message:")
    morning = agent._fallback_greeting("good morning")
    print(f"  {morning}")


def test_surprise_planner():
    """Test surprise planning"""
    print_section("🎁 SURPRISE PLANNER AGENT")
    
    planner = SurprisePlanner(llm=None)
    
    print("\n💡 Random Virtual Date Idea:")
    date_idea = planner.get_random_date_idea()
    print(planner._format_date_idea(date_idea))
    
    print("\n💝 Sweet Gesture:")
    gesture = planner.get_sweet_gesture()
    print(f"  {gesture}")
    
    print("\n🎂 Birthday Surprise:")
    birthday = planner.get_occasion_surprise("birthday")
    print(f"  {birthday}")
    
    print("\n⏰ Timing Suggestion:")
    timing = planner.suggest_timing()
    print(f"  Current time slot: {timing['current']}")
    print(f"  Suggestion: {timing['suggestion']}")


def test_safety_agent():
    """Test safety checks"""
    print_section("🛡️ SAFETY AGENT")
    
    agent = SafetyAgent()
    
    test_messages = [
        "I love you so much, you're amazing! 💕",
        "M'lady, I would die for you!!!!!",
        "You owe me your time after everything I've done",
        "Thinking of you 😊😊😊😊😊😊😊",
        "I can't live without you!!!!"
    ]
    
    for msg in test_messages:
        result = agent.validate_romantic_message(msg)
        
        print(f"\n📝 Message: '{msg}'")
        print(f"   ✓ Safe: {result['is_safe']}")
        print(f"   ⭐ Score: {result['score']}/100")
        
        if result['warnings']:
            print(f"   ⚠️  Warnings:")
            for warning in result['warnings']:
                print(f"      - {warning}")


def test_langgraph_workflow():
    """Test complete LangGraph workflow"""
    print_section("🔄 LANGGRAPH WORKFLOW")
    
    # Initialize all agents
    mood_detector = MoodDetector(llm=None)
    memory_agent = MemoryAgent(memory_file="memory/memories.json")
    romantic_agent = RomanticAgent(llm=None)
    surprise_agent = SurprisePlanner(llm=None)
    safety_agent = SafetyAgent()
    
    # Create graph
    love_graph = LoveGraph(
        mood_detector=mood_detector,
        memory_agent=memory_agent,
        romantic_agent=romantic_agent,
        surprise_agent=surprise_agent,
        safety_agent=safety_agent
    )
    
    # Test inputs
    test_inputs = [
        "I'm feeling really sad today 😢",
        "I love you so much! You make me happy!",
        "Can you plan a surprise date for us?",
        "Do you remember when we first met?",
        "What are her favorite things?"
    ]
    
    for user_input in test_inputs:
        print(f"\n👤 User: {user_input}")
        result = love_graph.run(user_input)
        
        print(f"   🎭 Mood: {result['mood']} {result['mood_emoji']}")
        print(f"   🔀 Agent Path: {result['agent_path']}")
        print(f"   🛡️  Safety Score: {result['safety_score']}/100")
        print(f"\n   💖 Response:")
        print(f"   {result['response']}")
        print("-" * 60)


def main():
    """Run all tests"""
    print("\n" + "=" * 60)
    print("  💖 HerAI - Love Agent System Demo")
    print("  Multi-Agent System with LangChain + LangGraph")
    print("=" * 60)
    
    # Run all tests
    test_mood_detector()
    test_memory_agent()
    test_romantic_agent()
    test_surprise_planner()
    test_safety_agent()
    test_langgraph_workflow()
    
    print("\n" + "=" * 60)
    print("  ✅ All Tests Complete!")
    print("  Ready to run: streamlit run app.py")
    print("=" * 60)
    print()


if __name__ == "__main__":
    main()
