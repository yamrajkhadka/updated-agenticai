"""
Enhanced Romantic Response Agent
Now checks memories FIRST, then generates LLM response if no relevant memory found
"""

from typing import Dict, List, Optional
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.messages import HumanMessage, AIMessage
import json

class RomanticAgent:
    def __init__(self, personality_config: Dict, llm=None):
        self.personality_config = personality_config
        self.llm = llm  # Accept LLM from outside (Groq, Anthropic, etc.)
        if self.llm:
            self._setup_prompts()
        
    def _setup_prompts(self):
        """Setup LLM prompts for different scenarios"""
        
        # MEMORY-FIRST SYSTEM PROMPT
        self.memory_first_prompt = ChatPromptTemplate.from_messages([
            ("system", f"""{self.personality_config['character']}

You are Yamraj (Ghosu), responding to your girlfriend Chuchi-Maya.

CRITICAL - MEMORY-FIRST APPROACH:
1. MEMORIES PROVIDED: {{memories}}
2. USER MESSAGE: {{context}}
3. CURRENT MOOD: {{mood}}

YOUR TASK:
- Check if ANY memory is relevant to the user's message
- If YES: Use that memory as the MAIN content of your response
- If NO: Respond naturally based on the mood and context

MEMORY RELEVANCE CRITERIA:
- Does the memory answer what she's asking about?
- Does the memory relate to her topic?
- Would mentioning this memory make sense in this conversation?

LANGUAGE RULES:
- Use Romanized Nepali: "Ma timro lagi", "Timi mero", "Chuchi"
- Mix with English for emotional phrases
- Keep it natural, caring, and personal
- Sign with heart emojis (💕, 💙, ✨, 🤗)

RESPONSE FORMAT:
- If using memory: Integrate it naturally (2-4 sentences)
- If no relevant memory: Respond based on mood (2-3 sentences)
- Always sound like YOU (Yamraj/Ghosu), not generic

Write your response now:"""),
            ("human", "{input}")
        ])
        
    def _check_memory_relevance(self, message: str, memories: List[Dict]) -> Optional[Dict]:
        """
        Check if any memory is actually relevant to the user's message
        Returns the most relevant memory or None
        """
        if not memories:
            return None
            
        message_lower = message.lower()
        
        # Category-based relevance matching
        relevance_keywords = {
            'first_contact': ['first', 'start', 'talking', 'message', 'began', 'facebook', 'friday', 'kura', 'gareko', 'shuru'],
            'first_date': ['date', 'restaurant', 'italian', 'first date', 'dinner', 'met'],
            'meeting': ['meet', 'met', 'saw', 'first saw', 'first time'],
            'stargazing': ['star', 'stars', 'night', 'orion', 'taara', 'sky', 'dreams'],
            'nickname': ['name', 'call', 'chuchi', 'maya', 'nickname'],
            'special_moments': ['moment', 'remember', 'yaad', 'special', 'time'],
            'promises': ['promise', 'promised', 'said', 'will'],
            'inside_jokes': ['joke', 'funny', 'laugh', 'remember when'],
            'favorites': ['favorite', 'like', 'love', 'prefer', 'best'],
            'personality': ['who', 'what', 'describe', 'personality', 'kind of person'],
            'apologies': ['sorry', 'apologize', 'forgive', 'my bad']
        }
        
        # Check each memory for relevance
        for memory in memories:
            category = memory.get('category', '')
            content = memory.get('content', '').lower()
            
            # Check if message keywords match this memory's category
            if category in relevance_keywords:
                keywords = relevance_keywords[category]
                if any(kw in message_lower for kw in keywords):
                    return memory
                    
            # Also check if any memory content words appear in the message
            # (for more flexible matching)
            content_words = set(content.split())
            message_words = set(message_lower.split())
            overlap = content_words & message_words
            if len(overlap) >= 2:  # At least 2 words match
                return memory
        
        return None
    
    def generate(self, 
                 message: str,
                 mood: str,
                 context: str,
                 memories: List[Dict] = None,
                 conversation_history: List = None) -> Dict:
        """
        Generate romantic response with MEMORY-FIRST approach
        
        Flow:
        1. Check if memories are relevant to the message
        2. If YES: Use memory in LLM prompt with STRONG instruction
        3. If NO: Generate romantic response based on mood
        """
        
        # Step 1: Check memory relevance
        relevant_memory = self._check_memory_relevance(message, memories or [])
        
        # Step 2: Prepare LLM input with memory-first logic
        if relevant_memory:
            # MEMORY FOUND - Make LLM use it directly
            memory_text = f"""
⚠️ CRITICAL INSTRUCTION - MEMORY-BASED RESPONSE REQUIRED:

A RELEVANT MEMORY was found that DIRECTLY answers her question:

Category: {relevant_memory.get('category')}
Content: {relevant_memory.get('content')}
Importance: {relevant_memory.get('importance')}/10

YOUR TASK:
1. Use the EXACT content from this memory as your PRIMARY response
2. DO NOT make up new information
3. Reference the memory content naturally in Romanized Nepali/English
4. Add emotional depth but STAY TRUE to the memory
5. Keep it 2-4 sentences

EXAMPLE FORMAT:
"Chuchi, [memory content in your own words]. Tyo din ko yaad aauxha malai... 💕"

Remember: The memory IS the answer. Don't deviate from it.
"""
            print(f"✅ Using relevant memory: {relevant_memory.get('category')}")
            print(f"   Content: {relevant_memory.get('content')[:60]}...")
        else:
            # NO MEMORY - Generate based on mood
            memory_text = f"""
No specific memory found for this question.

Her message: {message}
Her current mood: {mood}

YOUR TASK:
1. Respond naturally based on her mood
2. Be caring and romantic (you're Yamraj/Ghosu)
3. Use Romanized Nepali mixed with English
4. Keep it sweet and personal
5. 2-3 sentences

Respond based on the mood and be supportive.
"""
            print(f"ℹ️ No relevant memory found, generating mood-based response")
        
        # Step 3: Generate LLM response
        try:
            response = self.llm.invoke(
                self.memory_first_prompt.format(
                    input=message,
                    mood=mood,
                    context=context,
                    memories=memory_text
                )
            )
            
            return {
                'response': response.content,
                'mood': mood,
                'memory_used': relevant_memory is not None,
                'memory_category': relevant_memory.get('category') if relevant_memory else None
            }
            
        except Exception as e:
            print(f"❌ LLM generation error: {e}")
            # Fallback response
            return {
                'response': f"Chuchi, ma timro lagi always hunchhu. {self._get_mood_emoji(mood)}",
                'mood': mood,
                'memory_used': False,
                'memory_category': None
            }
    
    def _get_mood_emoji(self, mood: str) -> str:
        """Get emoji for mood"""
        mood_emojis = {
            'happy': '😊💕',
            'sad': '🤗💙',
            'romantic': '💕✨',
            'playful': '😄💖',
            'stressed': '🫂💙',
            'angry': '🤗💕'
        }
        return mood_emojis.get(mood, '💕')