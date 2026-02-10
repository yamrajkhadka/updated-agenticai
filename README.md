# 💖 HerAI - A Love Agent System

> *"This is not just a chatbot. This is an AI that thinks, remembers, and acts for her."*

A multi-agent Valentine AI built using **LangChain** and **LangGraph**. HerAI orchestrates multiple specialized agents to create meaningful, personalized romantic interactions.

## 🎯 What Makes This Special

This isn't your typical chatbot. HerAI uses **agentic reasoning** with multiple specialized AI agents working together:

- 💌 **Romantic Agent** - Writes love letters, poems, and heartfelt messages
- 🧠 **Memory Agent** - Remembers your special moments using RAG (Retrieval Augmented Generation)
- 🎵 **Mood Agent** - Detects emotional state and adapts responses
- 🎁 **Surprise Agent** - Plans thoughtful surprises and virtual dates
- 🛡️ **Safety Agent** - Keeps everything respectful and non-cringe

## 🏗️ Architecture

```
User Input
   ↓
Mood Detection Agent (detects: happy|sad|stressed|romantic|playful)
   ↓
LangGraph Router (intelligent routing based on mood + context)
   ├── Memory Agent (RAG with FAISS)
   ├── Romantic Agent (personalized messages)
   ├── Surprise Planner (creative ideas)
   └── Safety Check (quality control)
   ↓
Final Response Generator
```

Each node represents an agent, edges define decision logic, and state carries shared memory throughout the conversation.

## 🔧 Tech Stack

| Component | Technology |
|-----------|-----------|
| Framework | LangChain + LangGraph |
| LLM | Ollama (local) / OpenAI-compatible APIs |
| Memory | FAISS + Sentence Transformers |
| UI | Streamlit |
| Language | Python 3.9+ |

## 🚀 Quick Start

### 1. Clone and Setup

```bash
# Create project directory
mkdir HerAI && cd HerAI

# Install dependencies
pip install -r requirements.txt
```

### 2. Initialize Memory

The memory system stores special moments. Edit `memory/memories.json` to customize:

```json
[
  {
    "id": 1,
    "category": "first_meet",
    "content": "We first met at the coffee shop on Main Street. You smiled and I knew.",
    "date": "2024-01-15",
    "importance": 10
  },
  {
    "id": 2,
    "category": "nickname",
    "content": "I call her Sunshine because she lights up my world.",
    "date": "2024-02-01",
    "importance": 8
  }
]
```

### 3. Run the App

```bash
streamlit run app.py
```

The app will open at `http://localhost:8501`

## 📁 Project Structure

```
HerAI/
├── agents/                  # Individual AI agents
│   ├── mood_detector.py    # Emotion detection
│   ├── memory_agent.py     # RAG-based memory
│   ├── romantic_agent.py   # Content generation
│   ├── surprise_agent.py   # Surprise planning
│   └── safety_agent.py     # Quality control
│
├── graph/                   # LangGraph orchestration
│   └── love_graph.py       # Main workflow
│
├── memory/                  # Vector memory storage
│   └── memories.json       # Memory database
│
├── app.py                  # Streamlit UI
├── requirements.txt        # Dependencies
└── README.md              # This file
```

## 🧠 How Each Agent Works

### 1. Mood Detection Agent
```python
# Analyzes text to determine emotional state
mood = mood_detector.detect("I'm feeling sad today")
# Returns: "sad"

# Supports: happy, sad, stressed, romantic, playful, angry, neutral
```

### 2. Memory Agent (RAG)
```python
# Stores memories with semantic search
memory_agent.add_memory(
    "She loves stargazing. We spent hours looking at constellations.",
    category="special_moments",
    importance=9
)

# Retrieves relevant memories
memories = memory_agent.retrieve_memories("What does she like?", top_k=3)
```

### 3. Romantic Agent
```python
# Generates personalized romantic content
message = romantic_agent.generate_romantic_message(
    "I love you",
    mood="romantic",
    context=memories
)
```

### 4. Surprise Planner
```python
# Suggests creative date ideas
date_idea = surprise_agent.get_random_date_idea()
# Returns: Virtual movie night, cooking together, stargazing, etc.

# Plans occasions
surprise = surprise_agent.get_occasion_surprise("anniversary")
```

### 5. Safety Agent
```python
# Validates content for appropriateness
result = safety_agent.validate_romantic_message(message)
# Returns: {is_safe: bool, score: 0-100, warnings: [], suggestions: []}
```

## 🔄 LangGraph Workflow

The magic happens in `graph/love_graph.py`:

```python
# Simplified version of the routing logic
def route_by_mood(state: LoveState):
    mood = state["mood"]
    
    if mood in ["sad", "stressed"]:
        return "memory_retrieval"  # Use memories for comfort
    elif mood in ["happy", "playful"]:
        return "surprise_planning"  # Suggest fun activities
    else:
        return "romantic_response"  # Default loving response
```

This creates an **agentic system** where decisions are made dynamically based on context, not just pattern matching.

## 🎨 UI Features

### Main Chat Interface
- Real-time mood detection with emoji indicators
- Message history
- Debug mode (shows agent paths)

### Quick Actions (Sidebar)
- ✨ Write Something Special
- 🎁 Surprise Idea
- 🧠 What Do You Remember?
- 💌 Good Morning Message

### Stats Dashboard
- Message count
- Memory count
- Safety scores

## 💝 Valentine's Day Presentation

For maximum impact on Feb 14:

1. **Customize the welcome message** in `app.py`:
```python
st.markdown("""
<p>Hi [Her Name]! 💕</p>
<p>I'm HerAI, created by [Your Name] who loves you deeply...</p>
""")
```

2. **Pre-load special memories** in `memory/memories.json`

3. **Deploy** (optional):
   - Streamlit Cloud (free)
   - Heroku
   - Or share localhost URL

4. **First message auto-fill**:
```python
if st.session_state.first_visit:
    st.text_input(value="Hi ❤️ Tell me about yourself")
```

## 📈 Skills You'll Demonstrate

After building this, you can honestly say you've worked with:

✅ Multi-agent systems (5 specialized agents)  
✅ LangGraph for stateful agent orchestration  
✅ RAG (Retrieval Augmented Generation) with FAISS  
✅ Vector embeddings and semantic search  
✅ Conditional routing and decision logic  
✅ Prompt engineering and LLM integration  
✅ Production-ready UI with Streamlit  
✅ State management in conversational AI  

This is **portfolio gold** and genuinely impressive in interviews.

## 🔮 Future Enhancements

Want to take it further?

- [ ] **Voice Integration** - Add speech-to-text/text-to-speech
- [ ] **Scheduled Messages** - Auto-send good morning texts
- [ ] **Image Generation** - Create romantic images with DALL-E
- [ ] **Spotify Integration** - Playlist generation based on mood
- [ ] **Real LLM Integration** - Use GPT-4 or Claude for better responses
- [ ] **Mobile App** - React Native wrapper
- [ ] **Multi-language** - Support multiple languages

## 🤝 Contributing

This is a personal project, but feel free to:
- Fork it for your own romantic AI
- Adapt agents for different use cases
- Share improvements (keep it wholesome!)

## 📜 License

MIT License - Feel free to use this for your own love story!

## 💌 Credits

Built with love by someone who believes AI can help express what's in our hearts.

**Special thanks to:**
- LangChain team for the amazing framework
- The open-source community
- And most importantly, to **her** - for being the inspiration

---

*"The best code is written not for computers, but for the people we love."*

## 🐛 Troubleshooting

### Memory file not found
```bash
mkdir memory
# Edit memory/memories.json with your memories
```

### FAISS installation issues
```bash
pip install faiss-cpu --no-cache-dir
```

### Streamlit port already in use
```bash
streamlit run app.py --server.port 8502
```

## 📞 Need Help?

If you're stuck:
1. Check the agent test functions in each module
2. Enable debug mode in UI settings
3. Review LangGraph execution traces

---

**Remember:** This isn't just about the code. It's about showing someone they matter through the effort you put in. Good luck! 💖
