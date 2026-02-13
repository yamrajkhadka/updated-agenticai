# test_new_features.py (NEW FILE)
from graph.enhanced_love_graph import EnhancedLoveGraph
from utils.llm_config import get_llm_instance

# Initialize
llm = get_llm_instance()
graph = EnhancedLoveGraph(llm=llm, enable_proactive=True)

# Set proactive callback
def handle_proactive(message):
    print(f"\n🔔 PROACTIVE: {message}")

graph.set_proactive_callback(handle_proactive)

# Test
print("Testing new features...\n")

# Test 1: Memory-first
result = graph.process_message("How did we first start talking?")
print(f"Response: {result['response']}")
print(f"Memory used: {result.get('memory_category')}")

# Test 2: Wait for proactive
print("\nWaiting 65 seconds for proactive message...")
import time
time.sleep(65)

graph.stop_proactive_monitoring()