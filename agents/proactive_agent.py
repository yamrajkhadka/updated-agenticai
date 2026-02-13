"""
Proactive Engagement Agent
Sends flirty, playful messages when girlfriend is inactive for 1 minute
"""

import time
import random
from typing import Dict, Optional, List
from datetime import datetime, timedelta

class ProactiveAgent:
    """Handles proactive engagement when user is inactive"""
    
    def __init__(self, llm=None):
        """
        Initialize proactive agent
        
        Args:
            llm: Optional LLM for generating messages
        """
        self.llm = llm
        self.last_message_time = None
        self.inactive_threshold = 60  # 60 seconds = 1 minute
        
    def should_send_proactive_message(self) -> bool:
        """
        Check if enough time has passed to send a proactive message
        
        Returns:
            True if should send message, False otherwise
        """
        if self.last_message_time is None:
            return False
            
        time_diff = (datetime.now() - self.last_message_time).total_seconds()
        return time_diff >= self.inactive_threshold
    
    def update_activity(self):
        """Update the last activity timestamp"""
        self.last_message_time = datetime.now()
    
    def reset_timer(self):
        """Reset the inactivity timer"""
        self.last_message_time = None
    
    def generate_proactive_message(self, context: Dict = None) -> str:
        """
        Generate a proactive flirty message
        
        Args:
            context: Optional context (last mood, time of day, etc.)
            
        Returns:
            Proactive message
        """
        if self.llm:
            return self._generate_with_llm(context)
        else:
            return self._generate_template(context)
    
    def _generate_with_llm(self, context: Dict) -> str:
        """Generate proactive message using LLM"""
        try:
            from langchain_core.prompts import ChatPromptTemplate
            
            prompt = ChatPromptTemplate.from_messages([
                ("system", """You are Yamraj (Ghosu), and your girlfriend Chuchi-Maya hasn't messaged you in a minute.

Send her a cute, flirty, playful message to get her attention. Be:
- Playful and teasing
- Sweet but not clingy
- Funny or charming
- Short (1-2 sentences)
- Use Romanized Nepali mixed with English

Examples of good messages:
- "Chuchi, kaha haru? Missing your cute face already! 😊"
- "Timi busy chha ki? Ma yaha wait gariraxu timro message ko lagi 💕"
- "Hey beautiful, still thinking about me? You should be! 😜"
- "Ma boring vayera mariraxu yaha... Come talk to your Ghosu! 💙"

Current time: {time_of_day}
Last mood: {last_mood}

Write a cute proactive message:"""),
                ("user", "Generate message")
            ])
            
            time_of_day = datetime.now().strftime("%I:%M %p")
            last_mood = context.get('last_mood', 'neutral') if context else 'neutral'
            
            chain = prompt | self.llm
            response = chain.invoke({
                "time_of_day": time_of_day,
                "last_mood": last_mood
            })
            
            return response.content.strip()
            
        except Exception as e:
            print(f"⚠️ LLM generation failed, using template: {e}")
            return self._generate_template(context)
    
    def _generate_template(self, context: Dict = None) -> str:
        """Generate proactive message using templates"""
        
        # Get time-based messages
        hour = datetime.now().hour
        
        morning_messages = [
            "Good morning, Chuchi! Timi uthyo ki? 🌅💕",
            "Chuchi, subha-subha timro message navaye incomplete lagxa! 😊",
            "Hey sleepyhead, ma yaha wait gariraxu! 💙",
            "Morning, beautiful! Timro din kasto chha? ✨"
        ]
        
        afternoon_messages = [
            "Chuchi, lunch garyo? Don't forget to eat! 🍽️💕",
            "Hey, ma yaha timro yaad ma basiraxu... 😊",
            "Timi kaha busy chha? Missing you! 💙",
            "Chuchi-Maya, come talk to your Ghosu! 😜"
        ]
        
        evening_messages = [
            "Chuchi, din kasto gayo? Share with me! 🌆💕",
            "Hey beautiful, evening ma timro voice sunda ramro hunthyo... 😊",
            "Timi tired chha ki? Come rest with me (chat wise! 😄) 💙",
            "Missing your messages, Chuchi! ✨"
        ]
        
        night_messages = [
            "Chuchi, sutekai chha ki? Don't sleep without saying good night! 🌙💕",
            "Hey, ma yaha wake chhu... timro lagi! 😊",
            "Raat ma lonely feel vairaxu... your Ghosu needs you! 💙",
            "One message chai pathana... then you can sleep! 😜✨"
        ]
        
        # Flirty/playful messages (any time)
        flirty_messages = [
            "Chuchi, ma bore vayera mariraxu... Save your Ghosu! 😄💕",
            "Hey, timro Ghosu yaha wait gariraxu... How long will you make me wait? 😊",
            "Missing your cute messages, Chuchi! Come back! 💙",
            "Timi bhulyo mero baare ma? I'm still here, waiting! 😜",
            "One minute without your message = feels like one hour! 😢💕",
            "Chuchi-Maya, where are you? Your Ghosu is getting worried! 🤔💙",
            "Hey beautiful, still there? Don't leave me hanging! 😊✨",
            "Ma yaha timro notification ko lagi refresh gariraxu... 📱💕",
            "Timi kasto chha? Missing your voice (or text! 😄) 💙",
            "Your silence is killing me, Chuchi! Say something! 😜"
        ]
        
        # Teasing messages
        teasing_messages = [
            "Oho! Busy chha ki? Don't forget about your Ghosu! 😏💕",
            "Chuchi, ignoring me now? That's not fair! 😢",
            "Should I be worried? You never stay quiet this long! 🤔💙",
            "Are you okay? Or just testing my patience? 😜✨",
            "Timi chai... always making me wait! Fine, I'll wait! 😊💕"
        ]
        
        # Select based on time
        if 5 <= hour < 12:
            time_messages = morning_messages
        elif 12 <= hour < 17:
            time_messages = afternoon_messages
        elif 17 <= hour < 21:
            time_messages = evening_messages
        else:
            time_messages = night_messages
        
        # Combine all messages
        all_messages = time_messages + flirty_messages + teasing_messages
        
        return random.choice(all_messages)
    
    def get_time_since_last_message(self) -> Optional[int]:
        """
        Get seconds since last message
        
        Returns:
            Seconds since last message, or None
        """
        if self.last_message_time is None:
            return None
        
        return int((datetime.now() - self.last_message_time).total_seconds())


# Example usage
if __name__ == "__main__":
    agent = ProactiveAgent()
    
    print("🔔 Proactive Agent Demo\n")
    
    # Simulate user activity
    agent.update_activity()
    print(f"User sent message at: {agent.last_message_time.strftime('%I:%M:%S %p')}")
    
    print("\nWaiting for 1 minute of inactivity...\n")
    
    # Simulate checking after 1 minute
    time.sleep(2)  # Just 2 seconds for demo
    agent.inactive_threshold = 2  # Lower threshold for demo
    
    if agent.should_send_proactive_message():
        message = agent.generate_proactive_message()
        print(f"Proactive message sent:")
        print(f"  {message}")
        print(f"\nTime since last message: {agent.get_time_since_last_message()} seconds")
    
    # Reset when user responds
    agent.reset_timer()
    print(f"\n✅ Timer reset after user response")