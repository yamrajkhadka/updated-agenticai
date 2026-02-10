"""
HerAI Simple Structure Test
Verifies all files and structure without requiring dependencies
"""

import os
import json


def check_file_exists(filepath, description):
    """Check if a file exists"""
    exists = os.path.exists(filepath)
    status = "✅" if exists else "❌"
    print(f"{status} {description}: {filepath}")
    return exists


def test_project_structure():
    """Test project structure"""
    print("\n" + "=" * 60)
    print("  📁 PROJECT STRUCTURE CHECK")
    print("=" * 60 + "\n")
    
    checks = [
        ("agents/__init__.py", "Agents package"),
        ("agents/mood_detector.py", "Mood Detector Agent"),
        ("agents/memory_agent.py", "Memory Agent (RAG)"),
        ("agents/romantic_agent.py", "Romantic Agent"),
        ("agents/surprise_agent.py", "Surprise Planner Agent"),
        ("agents/safety_agent.py", "Safety Agent"),
        ("graph/__init__.py", "Graph package"),
        ("graph/love_graph.py", "LangGraph Orchestrator"),
        ("memory/__init__.py", "Memory package"),
        ("memory/memories.json", "Memories database"),
        ("app.py", "Streamlit UI"),
        ("demo.py", "Demo script"),
        ("requirements.txt", "Dependencies"),
        ("README.md", "Documentation"),
        ("SETUP.md", "Setup guide"),
        (".gitignore", "Git ignore file"),
    ]
    
    all_exist = True
    for filepath, description in checks:
        if not check_file_exists(filepath, description):
            all_exist = False
    
    return all_exist


def test_memory_file():
    """Test memory file is valid JSON"""
    print("\n" + "=" * 60)
    print("  🧠 MEMORY FILE CHECK")
    print("=" * 60 + "\n")
    
    try:
        with open("memory/memories.json", 'r') as f:
            memories = json.load(f)
        
        print(f"✅ Memory file is valid JSON")
        print(f"   Found {len(memories)} memories")
        
        categories = set(m['category'] for m in memories)
        print(f"   Categories: {', '.join(categories)}")
        
        return True
    except Exception as e:
        print(f"❌ Error reading memory file: {e}")
        return False


def count_code_lines():
    """Count lines of code"""
    print("\n" + "=" * 60)
    print("  📊 CODE STATISTICS")
    print("=" * 60 + "\n")
    
    files = [
        "agents/mood_detector.py",
        "agents/memory_agent.py",
        "agents/romantic_agent.py",
        "agents/surprise_agent.py",
        "agents/safety_agent.py",
        "graph/love_graph.py",
        "app.py"
    ]
    
    total_lines = 0
    for filepath in files:
        try:
            with open(filepath, 'r') as f:
                lines = len(f.readlines())
                total_lines += lines
                print(f"  {filepath}: {lines} lines")
        except:
            pass
    
    print(f"\n  Total: {total_lines} lines of code")


def show_features():
    """Show implemented features"""
    print("\n" + "=" * 60)
    print("  ✨ IMPLEMENTED FEATURES")
    print("=" * 60 + "\n")
    
    features = [
        ("🎭", "Mood Detection Agent", "Detects 7 emotional states"),
        ("🧠", "Memory Agent (RAG)", "FAISS vector memory with semantic search"),
        ("💌", "Romantic Agent", "Personalized messages, poems, apologies"),
        ("🎁", "Surprise Planner", "Virtual dates, gestures, occasion planning"),
        ("🛡️", "Safety Agent", "Content filtering and quality control"),
        ("🔄", "LangGraph Router", "Intelligent agent orchestration"),
        ("🎨", "Streamlit UI", "Beautiful chat interface with sidebar actions"),
        ("💾", "Persistent Memory", "JSON-based memory storage"),
        ("📊", "Debug Mode", "Agent path tracking and safety scores"),
        ("⚙️", "Customizable", "Easy to personalize for your relationship")
    ]
    
    for emoji, name, description in features:
        print(f"{emoji} {name}")
        print(f"   └─ {description}\n")


def show_architecture():
    """Show system architecture"""
    print("\n" + "=" * 60)
    print("  🏗️  SYSTEM ARCHITECTURE")
    print("=" * 60 + "\n")
    
    print("""
    User Input
       ↓
    Mood Detection Agent
       ↓
    LangGraph Router (conditional routing)
       ├─→ Memory Retrieval (for sad/stressed/memory queries)
       ├─→ Romantic Response (for romantic/general messages)
       └─→ Surprise Planning (for happy/ideas requests)
       ↓
    Safety Check (validates all output)
       ↓
    Final Response
    """)


def show_usage_guide():
    """Show quick usage guide"""
    print("\n" + "=" * 60)
    print("  🚀 QUICK START GUIDE")
    print("=" * 60 + "\n")
    
    print("""
    1. INSTALL DEPENDENCIES:
       pip install -r requirements.txt
    
    2. CUSTOMIZE MEMORIES:
       Edit memory/memories.json with your real memories
    
    3. PERSONALIZE WELCOME:
       Edit app.py to add her name
    
    4. TEST THE SYSTEM:
       python demo.py
    
    5. LAUNCH THE APP:
       streamlit run app.py
    
    6. DEPLOY (optional):
       - Streamlit Cloud (free & easy)
       - Heroku
       - Local network share
    """)


def show_skills_showcase():
    """Show skills demonstrated"""
    print("\n" + "=" * 60)
    print("  📈 SKILLS SHOWCASED")
    print("=" * 60 + "\n")
    
    skills = [
        "✅ Multi-agent system architecture",
        "✅ LangGraph for stateful workflows",
        "✅ RAG (Retrieval Augmented Generation)",
        "✅ Vector embeddings & semantic search",
        "✅ Conditional routing & decision logic",
        "✅ Prompt engineering",
        "✅ State management in AI systems",
        "✅ Production-ready UI development",
        "✅ Content safety & filtering",
        "✅ Full-stack AI application"
    ]
    
    for skill in skills:
        print(f"  {skill}")


def main():
    """Run all tests"""
    print("\n" + "=" * 60)
    print("  💖 HerAI - Love Agent System")
    print("  Structure & Feature Verification")
    print("=" * 60)
    
    # Run tests
    structure_ok = test_project_structure()
    memory_ok = test_memory_file()
    
    count_code_lines()
    show_features()
    show_architecture()
    show_skills_showcase()
    show_usage_guide()
    
    print("\n" + "=" * 60)
    if structure_ok and memory_ok:
        print("  ✅ ALL CHECKS PASSED!")
        print("  Ready to install dependencies and run!")
    else:
        print("  ⚠️  SOME CHECKS FAILED")
        print("  Please verify all files are in place")
    print("=" * 60)
    
    print("\n💡 Next Steps:")
    print("   1. pip install -r requirements.txt")
    print("   2. Customize memory/memories.json")
    print("   3. python demo.py (to test with dependencies)")
    print("   4. streamlit run app.py\n")


if __name__ == "__main__":
    main()
