# agents/__init__.py
"""
HerAI Agents Package
"""
from .mood_detector import MoodDetector
from .memory_agent import MemoryAgent
from .romantic_agent import RomanticAgent
from .surprise_agent import SurpriseAgent
from .safety_agent import SafetyAgent
from .proactive_agent import ProactiveAgent  # ⭐ ADD THIS LINE

__all__ = [
    'MoodDetector',
    'MemoryAgent',
    'RomanticAgent',
    'SurpriseAgent',
    'SafetyAgent',
    'ProactiveAgent'  # ⭐ ADD THIS LINE
]