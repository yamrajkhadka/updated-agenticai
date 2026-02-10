# 🚀 HerAI Setup Guide

## Step-by-Step Installation

### Prerequisites
- Python 3.9 or higher
- pip (Python package manager)
- Git (optional, for version control)

### Step 1: Environment Setup

```bash
# Create a virtual environment (recommended)
python -m venv herai_env

# Activate the virtual environment
# On Windows:
herai_env\Scripts\activate
# On Mac/Linux:
source herai_env/bin/activate
```

### Step 2: Install Dependencies

```bash
# Install all required packages
pip install -r requirements.txt

# If you encounter issues with specific packages:
pip install langchain==0.1.0 --no-cache-dir
pip install faiss-cpu==1.7.4 --no-cache-dir
pip install sentence-transformers==2.2.2 --no-cache-dir
```

### Step 3: Customize Your Memories

Edit `memory/memories.json` with your actual memories:

```json
[
  {
    "id": 1,
    "category": "first_meet",
    "content": "We first met at [SPECIFIC PLACE]. [WHAT HAPPENED]",
    "date": "YYYY-MM-DD",
    "importance": 10
  }
]
```

**Categories to use:**
- `first_meet` - How you met
- `nickname` - Pet names and why
- `favorites` - Her favorite things
- `special_moments` - Important dates/events
- `inside_jokes` - Shared humor
- `promises` - Commitments you've made

### Step 4: Test the System

```bash
# Run the demo to verify everything works
python demo.py
```

You should see output from all agents with test messages.

### Step 5: Launch the App

```bash
# Start Streamlit
streamlit run app.py
```

The app will open at `http://localhost:8501`

## 🎨 Customization Guide

### 1. Personality Settings

Edit `agents/romantic_agent.py`:

```python
# Change personality type
romantic_agent = RomanticAgent(llm=None, personality="Yamraj")

# Available personalities:
# - Yamraj: Soft, caring, slightly playful (default)
# - Poetic: Thoughtful and artistic
# - Playful: Light-hearted and fun
# - Deep: Philosophical and profound
```

### 2. Welcome Message

Edit `app.py` around line 140:

```python
st.markdown("""
<div class='love-message' style='background-color: #fff0f5;'>
    <h3>Hi [Her Name]! 💕</h3>
    <p>I'm HerAI, created by [Your Name] who loves you deeply...</p>
</div>
""", unsafe_allow_html=True)
```

### 3. Color Theme

Edit the CSS in `app.py`:

```python
st.markdown("""
<style>
    .main {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        # Change these colors ^^^
    }
</style>
""")
```

### 4. Add More Surprise Ideas

Edit `agents/surprise_agent.py`:

```python
SURPRISE_IDEAS = {
    "virtual_dates": [
        {
            "name": "Your New Date Idea",
            "description": "Description here",
            "duration": "2 hours",
            "prep": "What's needed"
        }
    ]
}
```

## 🔧 Troubleshooting

### Issue: FAISS won't install

**Solution:**
```bash
# Try this instead
pip install faiss-cpu --no-binary :all:

# Or for M1/M2 Mac:
conda install -c pytorch faiss-cpu
```

### Issue: Streamlit won't start

**Solution:**
```bash
# Try a different port
streamlit run app.py --server.port 8502

# Check if Python path is correct
which python
```

### Issue: Memory file not found

**Solution:**
```bash
# Ensure the memory directory exists
mkdir -p memory

# Check if memories.json exists
ls memory/memories.json
```

### Issue: Import errors

**Solution:**
```bash
# Make sure you're in the HerAI directory
cd HerAI

# Run from the project root
python app.py  # NOT from agents/ or graph/
```

## 🚀 Deployment Options

### Option 1: Streamlit Cloud (Recommended - FREE)

1. Push code to GitHub
2. Go to [share.streamlit.io](https://share.streamlit.io)
3. Connect your GitHub repo
4. Deploy!

**Note:** Update `requirements.txt` for cloud deployment:
```txt
# Remove local-only packages
# Add cloud-compatible versions
```

### Option 2: Heroku

```bash
# Create Procfile
echo "web: streamlit run app.py --server.port $PORT" > Procfile

# Create setup.sh
cat > setup.sh << 'EOF'
mkdir -p ~/.streamlit/
echo "[server]
headless = true
port = $PORT
enableCORS = false
" > ~/.streamlit/config.toml
EOF

# Deploy
heroku create your-herai-app
git push heroku main
```

### Option 3: Local Network Share

```bash
# Find your local IP
# Windows:
ipconfig
# Mac/Linux:
ifconfig

# Run with network access
streamlit run app.py --server.address 0.0.0.0

# Share the link: http://YOUR_IP:8501
```

## 💝 Valentine's Day Checklist

- [ ] Customize all memories in `memory/memories.json`
- [ ] Update welcome message with her name
- [ ] Add personal inside jokes to surprise ideas
- [ ] Test all features thoroughly
- [ ] Deploy or prepare local access
- [ ] Prepare the reveal message
- [ ] Have backup plan (screenshots) if tech fails!

## 🎯 Making It Extra Special

### Pre-load a conversation

Add to `app.py`:

```python
if st.session_state.first_visit:
    # Auto-start with a special message
    initial_message = "Tell me what you love most about us"
    result = st.session_state.love_graph.run(initial_message)
    st.session_state.chat_history.append({
        "role": "assistant",
        "content": result["response"]
    })
```

### Schedule surprises

Create a cron job or scheduled task:

```python
# surprise_scheduler.py
import schedule
import time

def send_morning_message():
    # Your logic here
    pass

schedule.every().day.at("08:00").do(send_morning_message)
```

### Add voice

```python
# Install additional packages
pip install SpeechRecognition pyttsx3

# Add to app
import speech_recognition as sr
import pyttsx3
```

## 📚 Learning Resources

- [LangChain Docs](https://python.langchain.com/docs/get_started/introduction)
- [LangGraph Tutorial](https://langchain-ai.github.io/langgraph/)
- [FAISS Guide](https://github.com/facebookresearch/faiss/wiki)
- [Streamlit Docs](https://docs.streamlit.io/)

## 🆘 Getting Help

1. Check the demo output: `python demo.py`
2. Enable debug mode in the UI
3. Review error messages carefully
4. Check that all files are in the right directories

## 📝 Final Checks Before Launch

```bash
# Run all tests
python demo.py

# Test in browser
streamlit run app.py

# Verify memories load
# Verify all buttons work
# Test each agent type
# Check safety filters
```

## 💖 Good Luck!

Remember: The code is impressive, but the thought behind it is what matters most.

Take your time, personalize it, and most importantly - make it genuine. She'll appreciate the effort more than perfection.

**You've got this!** 🚀
