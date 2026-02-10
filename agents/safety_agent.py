"""
Safety Agent
Ensures responses are appropriate, respectful, and non-cringe
"""

from typing import Dict, List, Optional
import re


class SafetyAgent:
    """Validates and filters responses for quality and appropriateness"""
    
    # Red flags that might make content inappropriate
    INAPPROPRIATE_PATTERNS = [
        r'\bsex\b', r'\bsexy\b', r'\bhot\b',
        r'\bbody\b', r'\bphysical\b.*\battraction\b',
    ]
    
    # Cringe indicators
    CRINGE_PATTERNS = [
        r'm\'lady', r'\*tips hat\*', r'\*blushes\*',
        r'uwu', r'owo', r'\*nuzzles\*',
        r'your highness', r'my queen'
    ]
    
    # Overly intense patterns
    INTENSITY_PATTERNS = [
        r'\bdie for you\b', r'\bcan\'t live without\b',
        r'\bobsessed\b', r'\bcrazily\b',
        r'\bdie without you\b'
    ]
    
    def __init__(self, strictness: str = "medium"):
        """
        Initialize safety agent
        
        Args:
            strictness: Level of filtering (low, medium, high)
        """
        self.strictness = strictness
        self.strictness_levels = {
            'low': 60,      # Allow most content
            'medium': 75,   # Balanced filtering
            'high': 85      # Strict filtering
        }
        self.threshold = self.strictness_levels.get(strictness, 75)
    
    def check_content(self, text: str) -> Dict:
        """
        Check content for safety and quality
        
        Args:
            text: Content to check
            
        Returns:
            Dict with safety assessment
        """
        issues = []
        score = 100
        
        # Check for inappropriate content
        inappropriate_count = self._check_patterns(text, self.INAPPROPRIATE_PATTERNS)
        if inappropriate_count > 0:
            issues.append(f"Contains {inappropriate_count} potentially inappropriate reference(s)")
            score -= inappropriate_count * 15
        
        # Check for cringe content
        cringe_count = self._check_patterns(text, self.CRINGE_PATTERNS)
        if cringe_count > 0:
            issues.append(f"Contains {cringe_count} cringe pattern(s)")
            score -= cringe_count * 10
        
        # Check for overly intense language
        intensity_count = self._check_patterns(text, self.INTENSITY_PATTERNS)
        if intensity_count > 0:
            issues.append(f"Contains {intensity_count} overly intense phrase(s)")
            score -= intensity_count * 8
        
        # Check length (too short might be low effort)
        if len(text.strip()) < 20:
            issues.append("Message is very short")
            score -= 10
        
        # Check for excessive caps
        caps_ratio = sum(1 for c in text if c.isupper()) / max(len(text), 1)
        if caps_ratio > 0.3:
            issues.append("Too many capital letters")
            score -= 5
        
        # Check for excessive punctuation
        punct_count = text.count('!') + text.count('?')
        if punct_count > 3:
            issues.append("Excessive punctuation")
            score -= 5
        
        # Ensure score is in valid range
        score = max(0, min(100, score))
        
        is_safe = score >= self.threshold
        
        return {
            'safe': is_safe,
            'score': score,
            'threshold': self.threshold,
            'issues': issues,
            'recommendation': self._get_recommendation(score, issues)
        }
    
    def _check_patterns(self, text: str, patterns: List[str]) -> int:
        """Check how many patterns match in text"""
        text_lower = text.lower()
        count = 0
        for pattern in patterns:
            if re.search(pattern, text_lower):
                count += 1
        return count
    
    def _get_recommendation(self, score: int, issues: List[str]) -> str:
        """Get recommendation based on score"""
        if score >= 85:
            return "✅ Great! This message is sweet and appropriate."
        elif score >= 75:
            return "👍 Good message, minor tweaks could make it better."
        elif score >= 60:
            return "⚠️  Decent but needs some improvements. Check the issues."
        else:
            return "❌ Message needs significant revision. Too many issues."
    
    def filter_response(self, text: str, auto_fix: bool = True) -> str:
        """
        Filter and optionally fix response
        
        Args:
            text: Text to filter
            auto_fix: Whether to attempt automatic fixes
            
        Returns:
            Filtered/fixed text
        """
        if not auto_fix:
            return text
        
        # Remove action text in asterisks
        text = re.sub(r'\*[^*]+\*', '', text)
        
        # Fix excessive punctuation
        text = re.sub(r'!{2,}', '!', text)
        text = re.sub(r'\?{2,}', '?', text)
        
        # Fix excessive caps (convert to title case)
        words = text.split()
        fixed_words = []
        for word in words:
            if word.isupper() and len(word) > 3:
                fixed_words.append(word.capitalize())
            else:
                fixed_words.append(word)
        text = ' '.join(fixed_words)
        
        return text.strip()
    
    def validate_and_fix(self, text: str) -> Dict:
        """
        Validate content and return fixed version if needed
        
        Args:
            text: Text to validate
            
        Returns:
            Dict with validation result and fixed text
        """
        # Check original
        check_result = self.check_content(text)
        
        # If not safe, try to fix
        if not check_result['safe']:
            fixed_text = self.filter_response(text, auto_fix=True)
            fixed_check = self.check_content(fixed_text)
            
            return {
                'original_safe': False,
                'original_score': check_result['score'],
                'fixed_text': fixed_text,
                'fixed_safe': fixed_check['safe'],
                'fixed_score': fixed_check['score'],
                'issues': check_result['issues'],
                'recommendation': 'Message was automatically improved'
            }
        
        return {
            'original_safe': True,
            'original_score': check_result['score'],
            'fixed_text': text,
            'fixed_safe': True,
            'fixed_score': check_result['score'],
            'issues': [],
            'recommendation': check_result['recommendation']
        }
    
    def get_improvement_suggestions(self, text: str) -> List[str]:
        """
        Get specific suggestions to improve the message
        
        Args:
            text: Text to analyze
            
        Returns:
            List of improvement suggestions
        """
        suggestions = []
        
        check = self.check_content(text)
        
        if check['score'] < 100:
            if 'inappropriate' in ' '.join(check['issues']).lower():
                suggestions.append("Keep it romantic, not physical")
            
            if 'cringe' in ' '.join(check['issues']).lower():
                suggestions.append("Avoid roleplay-style text (*blushes*, etc.)")
            
            if 'intense' in ' '.join(check['issues']).lower():
                suggestions.append("Tone down the intensity - keep it sweet, not desperate")
            
            if 'short' in ' '.join(check['issues']).lower():
                suggestions.append("Add more detail or emotion to your message")
            
            if 'capital' in ' '.join(check['issues']).lower():
                suggestions.append("Use normal capitalization")
            
            if 'punctuation' in ' '.join(check['issues']).lower():
                suggestions.append("Reduce exclamation marks and question marks")
        
        if not suggestions:
            suggestions.append("Your message looks good!")
        
        return suggestions
    
    def batch_check(self, texts: List[str]) -> Dict:
        """
        Check multiple texts at once
        
        Args:
            texts: List of texts to check
            
        Returns:
            Dict with batch results
        """
        results = []
        total_score = 0
        safe_count = 0
        
        for i, text in enumerate(texts):
            check = self.check_content(text)
            results.append({
                'index': i,
                'text': text[:50] + '...' if len(text) > 50 else text,
                'safe': check['safe'],
                'score': check['score']
            })
            total_score += check['score']
            if check['safe']:
                safe_count += 1
        
        return {
            'total': len(texts),
            'safe': safe_count,
            'unsafe': len(texts) - safe_count,
            'average_score': total_score / len(texts) if texts else 0,
            'results': results
        }


# Example usage
if __name__ == "__main__":
    agent = SafetyAgent(strictness="medium")
    
    print("🛡️  Safety Agent Demo\n")
    
    test_messages = [
        "I love you so much! You make every day better 💕",
        "I LOVE YOU!!! YOU'RE AMAZING!!!! ❤️❤️❤️",
        "*blushes* you're so beautiful m'lady",
        "I can't live without you, I'd die for you!",
        "You're wonderful 💙"
    ]
    
    for msg in test_messages:
        print(f"Message: {msg}")
        result = agent.check_content(msg)
        print(f"Score: {result['score']}/100")
        print(f"Safe: {'✅' if result['safe'] else '❌'}")
        if result['issues']:
            print(f"Issues: {', '.join(result['issues'])}")
        print(f"Recommendation: {result['recommendation']}")
        print()