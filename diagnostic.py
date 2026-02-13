"""
Diagnostic Script - Check if fixes are applied
"""

def check_memory_agent():
    """Check if memory_agent.py has the fixes"""
    try:
        with open('agents/memory_agent.py', 'r') as f:
            content = f.read()
        
        print("="*60)
        print("CHECKING: agents/memory_agent.py")
        print("="*60)
        
        # Check 1: Nepali keywords added?
        if "'kura', 'gareko', 'garya'" in content:
            print("✅ Fix 1: Nepali keywords found")
        else:
            print("❌ Fix 1: Nepali keywords MISSING")
        
        # Check 2: Score boost to 30?
        if "score += 30" in content and "category == 'first_contact'" in content:
            print("✅ Fix 2: Score boost to 30 found")
        else:
            print("❌ Fix 2: Score boost still at 15")
        
        # Check 3: Enhanced scoring?
        if "score += 25" in content and "category == 'first_meet'" in content:
            print("✅ Fix 3: Enhanced meeting scoring found")
        else:
            print("❌ Fix 3: Meeting scoring not updated")
        
        print()
    except Exception as e:
        print(f"❌ Error reading memory_agent.py: {e}\n")


def check_romantic_agent():
    """Check if romantic_agent.py has the fixes"""
    try:
        with open('agents/romantic_agent.py', 'r') as f:
            content = f.read()
        
        print("="*60)
        print("CHECKING: agents/romantic_agent.py")
        print("="*60)
        
        # Check 1: Memory-first approach?
        if "if memories and len(memories) > 0:" in content and "if category == 'first_contact':" in content:
            print("✅ Fix 1: Memory-first response logic found")
        else:
            print("❌ Fix 1: Memory-first response logic MISSING")
        
        # Check 2: First contact template?
        if "Tyo din ko yaad aauxha malai" in content:
            print("✅ Fix 2: First contact template found")
        else:
            print("❌ Fix 2: First contact template MISSING")
        
        # Check 3: Enhanced LLM prompt?
        if "CRITICAL - MEMORY USAGE" in content:
            print("✅ Fix 3: Enhanced LLM prompt found")
        else:
            print("❌ Fix 3: Enhanced LLM prompt MISSING")
        
        print()
    except Exception as e:
        print(f"❌ Error reading romantic_agent.py: {e}\n")


def check_love_graph():
    """Check if love_graph.py has the fixes"""
    try:
        with open('graph/love_graph.py', 'r') as f:
            content = f.read()
        
        print("="*60)
        print("CHECKING: graph/love_graph.py")
        print("="*60)
        
        # Check 1: Memory keyword detection in routing?
        if "memory_keywords = ['first', 'remember', 'yaad'" in content:
            print("✅ Fix 1: Memory keyword detection in routing found")
        else:
            print("❌ Fix 1: Memory keyword detection in routing MISSING")
        
        # Check 2: has_memory_query in simple_process?
        if "has_memory_query = any(kw in message_lower for kw in memory_keywords)" in content:
            print("✅ Fix 2: Memory query detection in fallback found")
        else:
            print("❌ Fix 2: Memory query detection in fallback MISSING")
        
        # Check 3: Debug logging?
        if "print(f\"🧠 Retrieved {len(memories)} memories\")" in content:
            print("✅ Fix 3: Debug logging found")
        else:
            print("❌ Fix 3: Debug logging MISSING")
        
        print()
    except Exception as e:
        print(f"❌ Error reading love_graph.py: {e}\n")


def test_memory_retrieval():
    """Test actual memory retrieval"""
    print("="*60)
    print("TESTING: Memory Retrieval")
    print("="*60)
    
    try:
        from agents.memory_agent import MemoryAgent
        
        agent = MemoryAgent()
        
        # Test query
        query = "How did we first start talking?"
        results = agent.retrieve_memories(query, k=3)
        
        print(f"Query: '{query}'")
        print(f"Memories found: {len(results)}\n")
        
        if results:
            print("Top 3 memories:")
            for i, mem in enumerate(results[:3], 1):
                print(f"\n{i}. Category: {mem.get('category')}")
                print(f"   Content: {mem.get('content')[:80]}...")
                print(f"   Importance: {mem.get('importance')}")
            
            # Check if first result is correct
            if results[0].get('category') == 'first_contact':
                print("\n✅ CORRECT: First result is 'first_contact' category!")
            else:
                print(f"\n❌ WRONG: First result is '{results[0].get('category')}' instead of 'first_contact'")
        else:
            print("❌ No memories retrieved!")
        
        print()
    except Exception as e:
        print(f"❌ Error testing memory retrieval: {e}\n")


def test_full_pipeline():
    """Test the full graph pipeline"""
    print("="*60)
    print("TESTING: Full Pipeline")
    print("="*60)
    
    try:
        from graph.love_graph import LoveGraph
        
        graph = LoveGraph()
        
        # Test query
        query = "How did we first start talking?"
        print(f"Query: '{query}'\n")
        
        result = graph.process_message(query)
        
        print(f"Mood: {result['mood']}")
        print(f"Memories Used: {result['memories_used']}")
        print(f"Agent Path: {' → '.join(result['agent_path'])}")
        print(f"\nResponse:\n{result['response']}")
        
        # Check if response mentions Facebook
        if 'Facebook' in result['response'] or 'facebook' in result['response']:
            print("\n✅ CORRECT: Response mentions Facebook!")
        else:
            print("\n❌ WRONG: Response does NOT mention Facebook")
        
        # Check if memories were used
        if result['memories_used'] > 0:
            print("✅ CORRECT: Memories were retrieved!")
        else:
            print("❌ WRONG: No memories were retrieved")
        
    except Exception as e:
        print(f"❌ Error testing full pipeline: {e}\n")


if __name__ == "__main__":
    print("\n🔍 HerAI Diagnostic Tool\n")
    
    # Check all files
    check_memory_agent()
    check_romantic_agent()
    check_love_graph()
    
    # Test functionality
    test_memory_retrieval()
    test_full_pipeline()
    
    print("="*60)
    print("Diagnostic Complete!")
    print("="*60)