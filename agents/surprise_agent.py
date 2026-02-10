"""
Surprise Planner Agent
Plans virtual dates and sweet surprises
"""

from typing import Dict, List, Optional
from datetime import datetime
import random


class SurpriseAgent:
    """Plans dates, surprises, and sweet gestures"""
    
    VIRTUAL_DATE_IDEAS = {
        'movie_night': {
            'title': '🎬 Movie Night',
            'description': 'Watch a movie together over video call',
            'steps': [
                'Pick a movie you both want to watch',
                'Start a video call',
                'Hit play at the same time',
                'Share reactions and commentary',
                'Discuss the movie after!'
            ],
            'suggestions': [
                'Have the same snacks for authenticity',
                'Dress up like it\'s a real date',
                'Create a cozy atmosphere with candles/lights'
            ]
        },
        'cooking_together': {
            'title': '👨‍🍳 Cook Together',
            'description': 'Make the same recipe together over video',
            'steps': [
                'Choose a recipe you both like',
                'Get the same ingredients',
                'Start video call in kitchen',
                'Cook together, step by step',
                'Eat together on the call!'
            ],
            'suggestions': [
                'Try making her favorite dish',
                'Set the table nicely',
                'Light some candles for ambiance'
            ]
        },
        'stargazing': {
            'title': '⭐ Virtual Stargazing',
            'description': 'Look at the stars together',
            'steps': [
                'Check weather for clear skies',
                'Download a stargazing app (Sky Map, Star Walk)',
                'Go outside at the same time',
                'Stay on call while watching stars',
                'Share what you see'
            ],
            'suggestions': [
                'Make wishes on shooting stars together',
                'Learn about constellations',
                'Talk about dreams and future'
            ]
        },
        'game_night': {
            'title': '🎮 Online Game Night',
            'description': 'Play games together',
            'steps': [
                'Choose online multiplayer games',
                'Set up voice chat',
                'Play together for a few hours',
                'Keep score if competitive!',
                'Loser does something sweet for winner'
            ],
            'suggestions': [
                'Try: Among Us, Minecraft, Stardew Valley',
                'Or play mobile games like Ludo King',
                'Make it fun, not too competitive'
            ]
        },
        'museum_tour': {
            'title': '🎨 Virtual Museum Tour',
            'description': 'Explore world museums online',
            'steps': [
                'Visit Google Arts & Culture',
                'Pick a museum (Louvre, MoMA, etc.)',
                'Screen share on video call',
                'Explore exhibits together',
                'Discuss art and history'
            ],
            'suggestions': [
                'Each pick your favorite piece',
                'Learn something new together',
                'Make it educational and fun'
            ]
        }
    }
    
    SURPRISE_IDEAS = {
        'digital_gift': [
            'Make a playlist of "our songs"',
            'Create a photo collage of memories',
            'Write her a letter and email it',
            'Send her favorite book as ebook',
            'Order food delivery to her place as surprise'
        ],
        'sweet_gesture': [
            'Send good morning texts every day for a week',
            'Leave voice messages when she wakes up',
            'Create a countdown to when you meet',
            'Make a video compilation of your messages',
            'Write her a poem'
        ],
        'planning_ahead': [
            'Plan your next date in detail',
            'Make a bucket list of things to do together',
            'Create a "reasons I love you" jar (digital)',
            'Plan a future trip together',
            'Set relationship goals together'
        ]
    }
    
    def __init__(self, llm=None):
        """
        Initialize surprise agent
        
        Args:
            llm: Optional language model
        """
        self.llm = llm
    
    def plan_virtual_date(self, preferences: str = "") -> Dict:
        """
        Plan a virtual date
        
        Args:
            preferences: Any specific preferences
            
        Returns:
            Dict with date plan
        """
        # Select appropriate date based on preferences
        if 'movie' in preferences.lower():
            date_type = 'movie_night'
        elif 'cook' in preferences.lower() or 'food' in preferences.lower():
            date_type = 'cooking_together'
        elif 'star' in preferences.lower() or 'sky' in preferences.lower():
            date_type = 'stargazing'
        elif 'game' in preferences.lower() or 'play' in preferences.lower():
            date_type = 'game_night'
        elif 'art' in preferences.lower() or 'museum' in preferences.lower():
            date_type = 'museum_tour'
        else:
            # Random selection
            date_type = random.choice(list(self.VIRTUAL_DATE_IDEAS.keys()))
        
        date_plan = self.VIRTUAL_DATE_IDEAS[date_type].copy()
        date_plan['type'] = date_type
        
        # Add timing recommendation
        date_plan['best_time'] = self._recommend_timing()
        
        return date_plan
    
    def plan_surprise(self, occasion: str = "just_because") -> Dict:
        """
        Plan a surprise
        
        Args:
            occasion: What's the occasion (birthday, anniversary, just_because)
            
        Returns:
            Dict with surprise plan
        """
        all_ideas = []
        for category, ideas in self.SURPRISE_IDEAS.items():
            all_ideas.extend([
                {'idea': idea, 'category': category} 
                for idea in ideas
            ])
        
        # Select 3 random ideas
        selected = random.sample(all_ideas, 3)
        
        return {
            'occasion': occasion,
            'ideas': selected,
            'timing': self._recommend_timing(),
            'extra_tip': self._get_surprise_tip(occasion)
        }
    
    def get_date_ideas_by_mood(self, mood: str) -> List[Dict]:
        """
        Get date ideas based on current mood
        
        Args:
            mood: Current mood
            
        Returns:
            List of appropriate date ideas
        """
        mood_mapping = {
            'happy': ['game_night', 'cooking_together'],
            'romantic': ['movie_night', 'stargazing'],
            'playful': ['game_night', 'cooking_together'],
            'stressed': ['stargazing', 'museum_tour'],
            'sad': ['movie_night', 'cooking_together']
        }
        
        date_types = mood_mapping.get(mood, list(self.VIRTUAL_DATE_IDEAS.keys()))
        
        return [
            {**self.VIRTUAL_DATE_IDEAS[dt], 'type': dt}
            for dt in date_types
        ]
    
    def _recommend_timing(self) -> Dict:
        """Recommend best timing for dates/surprises"""
        now = datetime.now()
        hour = now.hour
        
        if hour < 12:
            time_slot = 'morning'
            suggestion = 'Perfect for a breakfast cooking date!'
        elif hour < 17:
            time_slot = 'afternoon'
            suggestion = 'Great for a museum tour or light activity!'
        elif hour < 21:
            time_slot = 'evening'
            suggestion = 'Ideal for movie night or dinner together!'
        else:
            time_slot = 'night'
            suggestion = 'Perfect for stargazing or a cozy chat!'
        
        return {
            'current_time': now.strftime('%I:%M %p'),
            'time_slot': time_slot,
            'suggestion': suggestion
        }
    
    def _get_surprise_tip(self, occasion: str) -> str:
        """Get a tip for planning surprises"""
        tips = {
            'birthday': 'Send a surprise at midnight! Make her day start with love 🎂',
            'anniversary': 'Reference specific memories from your time together 💕',
            'just_because': 'The best surprises are unexpected! No special reason needed ✨',
            'apology': 'Actions speak louder - show you care with consistent effort 💙',
            'celebration': 'Make her feel special and celebrated! 🎉'
        }
        return tips.get(occasion, 'Personal touches make it more special! 💖')
    
    def generate_message_schedule(self, days: int = 7) -> List[Dict]:
        """
        Generate a schedule of messages to send
        
        Args:
            days: Number of days to plan for
            
        Returns:
            List of scheduled messages
        """
        message_types = [
            'good_morning',
            'midday_thinking_of_you',
            'good_night',
            'random_compliment',
            'funny_meme',
            'song_recommendation',
            'sweet_message'
        ]
        
        schedule = []
        for day in range(1, days + 1):
            daily_messages = random.sample(message_types, 3)
            schedule.append({
                'day': day,
                'messages': daily_messages,
                'tip': 'Space them out throughout the day naturally'
            })
        
        return schedule
    
    def get_gift_ideas(self, budget: str = "low") -> List[str]:
        """
        Get gift ideas based on budget
        
        Args:
            budget: Budget level (low, medium, high)
            
        Returns:
            List of gift ideas
        """
        ideas = {
            'low': [
                'Handwritten letter sent as PDF',
                'Custom playlist with message',
                'Photo collage/edit',
                'Poem or creative writing',
                'Digital artwork/drawing',
                'Voice message compilation'
            ],
            'medium': [
                'Order her favorite food delivery',
                'Send flowers through online service',
                'Gift card to her favorite store',
                'Book she mentioned wanting',
                'Subscription to streaming service',
                'Online course she\'d enjoy'
            ],
            'high': [
                'Jewelry (shipped to her)',
                'Surprise plane ticket to visit',
                'Professional photoshoot voucher',
                'Experience gift (spa, adventure)',
                'Custom-made items (art, jewelry)',
                'Weekend getaway planned'
            ]
        }
        
        return ideas.get(budget, ideas['low'])


# Example usage
if __name__ == "__main__":
    agent = SurpriseAgent()
    
    print("🎁 Surprise Planner Demo\n")
    
    print("Virtual Date Plan:")
    date = agent.plan_virtual_date("movie")
    print(f"{date['title']}")
    print(f"{date['description']}\n")
    print("Steps:")
    for i, step in enumerate(date['steps'], 1):
        print(f"{i}. {step}")
    
    print("\n" + "="*50 + "\n")
    
    print("Surprise Ideas:")
    surprise = agent.plan_surprise("just_because")
    for idea in surprise['ideas']:
        print(f"• {idea['idea']} ({idea['category']})")
    print(f"\nTip: {surprise['extra_tip']}")