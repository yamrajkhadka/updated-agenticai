"""
Romantic Agent
Generates loving messages, poems, and apologies
"""

from typing import Dict, Optional, List
from datetime import datetime
import random


class RomanticAgent:
    """Generates romantic content based on mood and context"""
    
    PERSONALITIES = {
        'Yamraj': {
            'tone': 'Soft, caring, slightly playful with deep affection',
            'style': 'Warm and protective, like a gentle guardian'
        },
        'Poetic': {
            'tone': 'Lyrical, metaphorical, deeply romantic',
            'style': 'Uses imagery and beautiful language'
        },
        'Playful': {
            'tone': 'Fun, teasing, lighthearted with love',
            'style': 'Keeps things fun and flirty'
        },
        'Deep': {
            'tone': 'Profound, sincere, emotionally intense',
            'style': 'Speaks from the heart with vulnerability'
        }
    }
    
    def __init__(self, llm=None, personality: str = "Yamraj"):
        """
        Initialize romantic agent
        
        Args:
            llm: Optional language model
            personality: Personality type (Yamraj, Poetic, Playful, Deep)
        """
        self.llm = llm
        self.personality = personality
        self.personality_config = self.PERSONALITIES.get(
            personality,
            self.PERSONALITIES['Yamraj']
        )
    
    def generate_message(
        self, 
        mood: str, 
        context: str = "", 
        memories: List[Dict] = None
    ) -> str:
        """
        Generate a romantic message
        
        Args:
            mood: Current mood (happy, sad, stressed, etc.)
            context: Additional context
            memories: Relevant memories to reference
            
        Returns:
            Romantic message
        """
        if self.llm:
            return self._generate_with_llm(mood, context, memories)
        else:
            return self._generate_template(mood, context, memories)
    
    def _generate_template(
        self, 
        mood: str, 
        context: str = "", 
        memories: List[Dict] = None
    ) -> str:
        """Generate message using templates (no LLM needed)"""
        
        # Base messages by mood
        templates = {
            'happy': [
                "Your happiness is my favorite thing in the world. Keep shining! ✨",
                "I love seeing you this happy! Your smile makes everything better 💕",
                "This joy in your heart? I want to protect it forever 🌟"
            ],
            'sad': [
                "I wish I could wrap you in the warmest hug right now. You're not alone 💙",
                "Even on hard days, remember: you're stronger than you know, and I'm always here 🤗",
                "Let me be your comfort. Your sadness matters to me, and so do you 💕"
            ],
            'stressed': [
                "Take a deep breath with me. You've got this, and I've got you 🌸",
                "I know it's overwhelming, but you're handling it beautifully. I'm proud of you 💪",
                "Let me help carry that weight. You don't have to do this alone 💙"
            ],
            'romantic': [
                "You make my heart do things I didn't know were possible 💕",
                "Every moment with you feels like a dream I never want to wake from ✨",
                "I fall for you more deeply with each passing day 💖"
            ],
            'playful': [
                "You're adorable when you're like this! 😊 Keep being your amazing self!",
                "Someone's in a good mood! And I'm absolutely here for it 🎉",
                "Your playful energy is contagious! Love this side of you 💫"
            ],
            'angry': [
                "I can tell you're upset. Want to talk about it? I'm listening 💙",
                "Your feelings are valid. I'm here, no judgment, just support 🤗",
                "Take your time. I'll be here when you're ready to share 💕"
            ],
            'neutral': [
                "Just wanted to remind you that you're wonderful 💕",
                "Thinking of you and hoping your day is going well ✨",
                "You're always on my mind 💙"
            ]
        }
        
        # Get appropriate template
        options = templates.get(mood, templates['neutral'])
        message = random.choice(options)
        
        # Add memory reference if available
        if memories and len(memories) > 0:
            memory = memories[0]
            message += f"\n\nRemembering: {memory.get('content', '')} 💭"
        
        return message
    
    def _generate_with_llm(
        self, 
        mood: str, 
        context: str, 
        memories: List[Dict] = None
    ) -> str:
        """Generate message using LLM"""
        # This would use the LLM to generate personalized messages
        # For now, fall back to templates
        return self._generate_template(mood, context, memories)
    
    def generate_poem(self, theme: str = "love", memories: List[Dict] = None) -> str:
        """
        Generate a romantic poem
        
        Args:
            theme: Poem theme
            memories: Memories to reference
            
        Returns:
            Poem text
        """
        poems = {
            'love': """In every moment, in every day,
My love for you grows in every way.
Your smile, your laugh, your gentle touch,
Mean more to me than words can clutch.

You are my dream, my morning light,
My peaceful day, my starry night.
With you, my heart has found its home,
No matter where, we'll never roam alone. 💕""",
            
            'missing': """Miles apart, yet close in heart,
This distance can't keep us apart.
I carry you in every thought,
In every moment, you're never forgot.

Until we meet and I see your face,
I'll hold you close in this empty space.
My love transcends both time and place,
Forever yours, in every embrace. 💙""",
            
            'appreciation': """For all you are and all you do,
These simple words: I cherish you.
Your kindness, strength, your caring ways,
Brighten even my darkest days.

You are a gift I'll treasure always,
Through all of life's twists and maze.
Thank you for being beautifully you,
My heart is yours, forever true. 💖"""
        }
        
        return poems.get(theme, poems['love'])
    
    def generate_apology(self, context: str = "") -> str:
        """
        Generate a heartfelt apology
        
        Args:
            context: What you're apologizing for
            
        Returns:
            Apology message
        """
        apology = f"""I'm truly sorry. """
        
        if context:
            apology += f"I know I hurt you by {context}, and that wasn't okay. "
        
        apology += """
I want you to know that your feelings matter to me more than being right. 
I'm listening, I'm learning, and I'm committed to doing better.

You deserve better, and I want to be better - for you, for us.
Can we talk about this? I'm here, whenever you're ready. 💙

I love you, and I'm sorry. 🤗"""
        
        return apology
    
    def generate_good_morning(self) -> str:
        """Generate a good morning message"""
        messages = [
            "Good morning, beautiful! ☀️ Hope your day is as amazing as you are 💕",
            "Rise and shine! 🌅 Sending you all my love to start your day right ✨",
            "Morning, love! 💙 May today bring you joy, laughter, and everything wonderful 🌸",
            "Good morning! ☕ Just wanted to be your first smile of the day 😊💕",
        ]
        return random.choice(messages)
    
    def generate_good_night(self) -> str:
        """Generate a good night message"""
        messages = [
            "Good night, sweetheart 🌙 Dream of us and all the beautiful moments ahead 💕",
            "Sleep tight, love 💙 I'll be thinking of you until morning ✨",
            "Sweet dreams! 🌟 You're the last thing on my mind before I sleep 💖",
            "Good night, my love 🌙 May your dreams be as wonderful as you are 😊💕",
        ]
        return random.choice(messages)
    
    def generate_encouragement(self, context: str = "") -> str:
        """
        Generate an encouraging message
        
        Args:
            context: What they need encouragement for
            
        Returns:
            Encouraging message
        """
        base = "I believe in you. "
        
        if "exam" in context.lower() or "test" in context.lower():
            base += "You've prepared well, and you're going to do amazing! Your hard work will pay off. 💪✨"
        elif "work" in context.lower() or "job" in context.lower():
            base += "You're capable of incredible things. This challenge? You've got this! 🌟"
        else:
            base += "Whatever you're facing, I know you have the strength to handle it. And I'm right here with you, every step. 💙"
        
        return base
    
    def get_personality_info(self) -> Dict:
        """Get current personality configuration"""
        return {
            'personality': self.personality,
            'tone': self.personality_config['tone'],
            'style': self.personality_config['style']
        }


# Example usage
if __name__ == "__main__":
    agent = RomanticAgent(personality="Yamraj")
    
    print("💌 Romantic Agent Demo\n")
    
    print("Message (Happy mood):")
    print(agent.generate_message('happy'))
    print("\n" + "="*50 + "\n")
    
    print("Message (Sad mood):")
    print(agent.generate_message('sad'))
    print("\n" + "="*50 + "\n")
    
    print("Love Poem:")
    print(agent.generate_poem('love'))
    print("\n" + "="*50 + "\n")
    
    print("Good Morning:")
    print(agent.generate_good_morning())