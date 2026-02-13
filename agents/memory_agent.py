"""
Memory Agent with RAG - FIXED for Girlfriend Identity
Retrieves relevant memories using enhanced keyword search
Supports both English and Romanized Nepali queries
SPECIAL: Prioritizes girlfriend identity when asked about "lalita" or "girlfriend"
"""

import json
import os
from typing import List, Dict, Optional
from datetime import datetime


class MemoryAgent:
    """Manages and retrieves relationship memories"""

    def __init__(self, memory_file: str = "memory/memories.json"):
        self.memory_file = memory_file
        self.memories = []
        self._load_memories()

    def _load_memories(self):
        """Load memories from JSON file"""
        if os.path.exists(self.memory_file):
            try:
                with open(self.memory_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    self.memories = data.get('memories', [])
                print(f"✅ Loaded {len(self.memories)} memories")
            except Exception as e:
                print(f"❌ Error loading memories: {e}")
                self.memories = []
        else:
            print(f"⚠️  Memory file not found: {self.memory_file}")
            self.memories = []

    def retrieve_memories(self, query: str, k: int = 3) -> List[Dict]:
        """
        Retrieve relevant memories using enhanced keyword search
        SPECIAL HANDLING for girlfriend identity questions

        Args:
            query: Search query (English or Romanized Nepali)
            k: Number of memories to retrieve

        Returns:
            List of relevant memories
        """
        query_lower = query.lower()
        
        # ══════════════════════════════════════════════════════════════════
        # SPECIAL: Direct girlfriend identity detection
        # ══════════════════════════════════════════════════════════════════
        gf_triggers = [
            'lalita oli', 'lalita', 'who is lalita',
            'my gf', 'my girlfriend', 'girlfriend ko', 
            'detail of my gf', 'detail of gf', 'gf ko detail',
            'tell me about her', 'about my girlfriend',
            'her name', 'girlfriend name', 'gf name',
            'girlfriend ki', 'premi ko', 'girlfriend baare',
            'usko naam', 'usle ko naam', 'ke ho girlfriend'
        ]
        
        # Check if asking specifically about girlfriend identity
        if any(trigger in query_lower for trigger in gf_triggers):
            # Get her_identity, her_family, her_personality
            identity_memories = []
            for m in self.memories:
                cat = m.get('category', '')
                if cat in ['her_identity', 'her_family', 'her_personality', 'personality_traits', 'her_personality']:
                    identity_memories.append(m)
            
            if identity_memories:
                # Sort by importance
                identity_memories.sort(key=lambda x: x.get('importance', 0), reverse=True)
                return identity_memories[:k]
        
        # ══════════════════════════════════════════════════════════════════
        # Otherwise use normal enhanced search
        # ══════════════════════════════════════════════════════════════════
        return self._enhanced_search(query, k)

    def _enhanced_search(self, query: str, k: int = 3) -> List[Dict]:
        """
        Enhanced keyword-based search with comprehensive matching.
        Supports both English and Romanized Nepali queries.
        """
        query_lower = query.lower()

        keyword_groups = {

            # ── Her identity (HIGHEST BOOST) ──────────────────────────────
            'her_identity': {
                'keywords': [
                    'lalita', 'girlfriend', 'your girlfriend', 'her name',
                    'who is she', 'bhadra', '2060', 'her birth',
                    'girlfriend ko naam', 'premi ko naam', 'usko naam',
                    'girlfriend baare', 'tero girlfriend', 'premi', 'saathini'
                ],
                'categories': ['her_identity'],
                'content_matches': [
                    'lalita', 'oli', 'bhadra', '2060', 'premi', 
                    'jeevan ko pyaar', 'saathini', 'chatbot', 'girlfriend'
                ],
                'boost': 100  # HIGHEST!
            },

            # ── How we first made contact ──────────────────────────────────
            'first_contact': {
                'keywords': [
                    'first', 'start', 'talking', 'message', 'friday', 'facebook',
                    'reply', 'began', 'messaged', 'contact', 'how did we',
                    'how we met', 'night', '7pm', 'lonely', 'ignore',
                    'kasto shuru', 'kasari chinu', 'pehilo palta', 'pahilo palta',
                    'pahilo message', 'pehilo message', 'kasari bheta',
                    'shuru bhayo', 'facebook ma', 'message gareko',
                    'friday ko raat', 'reply garyo', 'kati bajey',
                    'first time boleko', 'bolna shuru', 'ignore garla',
                    'socheko thiyo', 'pehilo palo', 'pahilo palo',
                    'kasari contact', 'kina message', 'message kina',
                    'pehilo din', 'pahilo din', 'raat ma message',
                    'eklo thiye', 'friday bela', 'facebook bata'
                ],
                'categories': ['first_contact', 'relationship_start', 'how_we_connected'],
                'content_matches': [
                    'facebook', 'friday', '7pm', 'messaged', 'lonely', 'ignore',
                    'eklo thiye', 'reply garyo', 'message gareko', 'badliyo',
                    'socheko thiyo', 'pahilo message'
                ],
                'boost': 35
            },

            # ── Common friend / video call introduction ────────────────────
            'how_connected': {
                'keywords': [
                    'common friend', 'mutual friend', 'video call', 'connected',
                    'introduced', 'friend connect', 'before we talked', 'weeks before',
                    'common saathi', 'mutual saathi', 'saathi le', 'saathi le connect',
                    'video call garyeko', 'video call ma', 'pehile nai', 'pahile nai',
                    'kasle milayo', 'kasle introduce', 'saathi ko madhyam',
                    'saathi le chinauko', 'saathi ko through', 'dui hapta agadi',
                    '2 hapta pahile', 'agaadi nai', 'pehile connect',
                    'video ma boleko', 'video call ko agadi'
                ],
                'categories': ['how_we_connected', 'relationship_start'],
                'content_matches': [
                    'common friend', 'video call', '2 weeks', 'casual', 'connected',
                    'common saathi', 'saathi le', 'video call maa', 'saadhaaran',
                    'chinaaudiyeko', 'pehile'
                ],
                'boost': 32
            },

            # ── Number of in-person meetings ───────────────────────────────
            'meetings': {
                'keywords': [
                    'met', 'meet', 'meeting', 'in person', 'times', 'saw', 'seen',
                    'how many times', 'physically', 'face to face', 'together',
                    'kati choti', 'kati palta', 'bheta', 'bheteko', 'bhet',
                    'physically bheto', 'aankha dekha', 'dekha bhayo',
                    'kati baar bheteko', 'samna', 'aamne saamne',
                    'face dekha', 'prataksha bheteko', 'kati din bheteko',
                    'kati palo bheteko', 'bhetna', 'bhet gare', 'bhetna gaye',
                    'sanga bheto', 'ma bheteko', 'hami bheteko',
                    'kati baar dekha', 'physically dekha'
                ],
                'categories': ['meetings'],
                'content_matches': [
                    '4 times', 'four times', 'only met', 'precious', 'distance',
                    'chaar palta', 'physically', 'bheteko chhau', 'kyaaro thiyo',
                    'kati choti', 'palta matra'
                ],
                'boost': 35
            },

            # ── Baby bet / Alisha ──────────────────────────────────────────
            'bet': {
                'keywords': [
                    'bet', 'alisha', 'baby', 'boy', 'girl', 'won', 'win', 'wins',
                    'argument', 'gender', 'niece', 'nephew', 'prediction', 'always wins',
                    'shart', 'bet lagyo', 'alisha ko', 'baby ko', 'chora ki chori',
                    'jitiyo', 'haari', 'argument jityo', 'jhagada jityo',
                    'bhanji', 'bhanja', 'gender kasto hola', 'sahi thiyo',
                    'galat thiyo', 'ma jite', 'usle jityo', 'usle jitchhe',
                    'hamesha jitchhe', 'jitna man parcha', 'shart ma jitiyo',
                    'baby chora hola', 'baby chori hola', 'kasto hola baby',
                    'alisha janmada', 'alisha ko janma', 'chhori thiyo',
                    'chora thiyo', 'usle sahi thiyo', 'ma galat thiyo'
                ],
                'categories': ['inside_jokes', 'special_moments'],
                'content_matches': [
                    'bet', 'alisha', 'boy', 'girl', 'won',
                    'shart', 'chora', 'chori', 'jitiyo', 'hamesha jitchhe',
                    'alisha ko janma', 'bhanji', 'maaya garcha'
                ],
                'boost': 40
            },

            # ── Gifts exchanged ────────────────────────────────────────────
            'gifts': {
                'keywords': [
                    'gift', 'gave', 'give', 'given', 'earring', 'rose', 'rupees',
                    'present', 'token', '100', 'one earring', 'flower', 'wrapped',
                    'uphaar', 'uphar', 'dieko', 'deko', 'diyeko', 'kaan ko',
                    'kaanmuni', 'kaanbali', 'phool', 'gulaab', 'gulab',
                    '100 rupiya', 'note ma', 'ek kaanbali', 'kasle ke diyo',
                    'maine ke diye', 'usle ke diye', 'ke uphaar diyo',
                    'ke diyo malai', 'ke diyo uslai', 'ek earring',
                    'ek matra', 'phool dieko', 'gulab dieko',
                    'rupiya wrapped', 'note ma gulab', 'paisa maa gulab',
                    'uphar ke thiyo', 'ke lyaeko', 'ke lyauthyo'
                ],
                'categories': ['gifts', 'gifts_exchanged'],
                'content_matches': [
                    'earring', 'rose', 'rupees', '100', 'awkward', 'wrapped',
                    'kaanbali', 'gulab', 'rupiya', 'uphaar', 'note maa',
                    'sambhaalera', 'wrap gareko'
                ],
                'boost': 35
            },

            # ── My / Her family ────────────────────────────────────────────
            'family': {
                'keywords': [
                    'family', 'father', 'dad', 'mother', 'mom', 'brother', 'sister',
                    'parents', 'mandir', 'pabitra', 'sunil', 'lokendra',
                    'middle child', 'siblings', 'elder brother', 'younger brother',
                    'pariwar', 'buba', 'buwa', 'aama', 'ama', 'bhai', 'daju',
                    'didi', 'bahini', 'mandir khadka', 'pabitra khadka',
                    'sunil dai', 'lokendra', 'maijhilo', 'majhilo chhora',
                    'mero pariwar', 'hamro ghar', 'tero buwa', 'tero aama',
                    'buba ko naam', 'aama ko naam', 'daju ko naam',
                    'bhai ko naam', 'ghar ma', 'ghar ko', 'pariwar ko',
                    'teen jana', 'teen bhai', 'majhilo', 'daju bhai'
                ],
                'categories': ['my_family', 'family', 'her_family'],
                'content_matches': [
                    'mandir', 'pabitra', 'sunil', 'lokendra', 'middle child',
                    'buwa', 'aama', 'daju', 'bhai', 'majhilo chhora',
                    'mandir khadka', 'pabitra khadka', 'teen jana'
                ],
                'boost': 35
            },

            # ── Nickname ───────────────────────────────────────────────────
            'nickname': {
                'keywords': [
                    'call', 'name', 'chuchi', 'ghosu', 'nickname', 'what do you call',
                    'pet name', 'term of endearment',
                    'ke bhanchu', 'ke bhanera', 'naam ke ho', 'ke naam',
                    'chuchi kina', 'ghosu kina', 'naamdhari', 'tapaai ko naam',
                    'tero naam', 'mero naam', 'ke boli', 'ke bolchhu',
                    'darling naam', 'pyaar ko naam', 'boli ko naam',
                    'chuchi bhanchhau', 'ghosu bhanchhau', 'kina chuchi',
                    'kina ghosu', 'tapaai le ke bhannu', 'usle ke bhancha'
                ],
                'categories': ['nickname'],
                'content_matches': [
                    'chuchi', 'ghosu', 'call', 'darpok',
                    'bhanchu', 'bhancha', 'pyaar ko naam', 'arkulai thaha'
                ],
                'boost': 35
            },

            # ── Personality ────────────────────────────────────────────────
            'personality': {
                'keywords': [
                    'scared', 'darpok', 'afraid', 'competitive', 'win', 'sensitive',
                    'feel', 'shy', 'brave', 'personality', 'nature', 'character',
                    'daraune', 'darauchhe', 'daraunchhe', 'darpok chhe',
                    'darpok chha', 'dar lagcha', 'darlagcha', 'harauna man pardaina',
                    'jitna man parcha', 'sensitive chhe', 'sensitive chha',
                    'man ko kura', 'swabhav', 'swabhaav', 'kasto chhe',
                    'kasto chha', 'personality kasto', 'kasri chhe',
                    'komal chhe', 'brave chhe', 'himmat', 'sachchi chhe',
                    'darpok thiyo', 'sensitive thiyo', 'kasto manchhe'
                ],
                'categories': ['personality', 'her_personality', 'my_personality', 'personality_traits'],
                'content_matches': [
                    'darpok', 'scared', 'competitive', 'sensitive', 'brave',
                    'dar lagchha', 'adorable', 'surakshit', 'himmatpan',
                    'joshilaaipan', 'komal', 'sachcho'
                ],
                'boost': 30
            },

            # ── Favorites ──────────────────────────────────────────────────
            'favorites': {
                'keywords': [
                    'favorite', 'favourite', 'love', 'likes', 'color', 'colour',
                    'purple', 'ice cream', 'chocolate', 'music', 'artist', 'song',
                    'romcom', 'romantic comedy', 'movie', 'film', 'food',
                    'man parcha', 'man pareko', 'rang', 'rang ke ho',
                    'kasto rang', 'purple rang', 'aayskrim', 'ice cream khana',
                    'chocolate', 'gana', 'geet', 'sangeet', 'gayak', 'gaayak',
                    'movie hercha', 'movie man parcha', 'romantic film',
                    'romantic movie', 'khana man parcha', 'kasto khana',
                    'cigarettes after sex', 'indie geet', 'indie music',
                    'favorite gana', 'favorite rang', 'favorite khana'
                ],
                'categories': ['favorites'],
                'content_matches': [
                    'purple', 'chocolate', 'cigarettes after sex', 'romcom', 'indie',
                    'rang', 'aayskrim', 'gayak', 'geet', 'sangeet',
                    'man paraaunchhe', 'man parcha'
                ],
                'boost': 25
            },

            # ── Relationship timeline / growth ─────────────────────────────
            'relationship': {
                'keywords': [
                    'relationship', 'year', 'together', 'talking', 'timeline',
                    '4 days', 'formal', 'grew', 'journey', 'how long',
                    'since when', 'duration', 'history',
                    'sambandha', 'rishta', 'kati din', 'kati barsadekhi',
                    'kati samay', 'ek barsadekhi', 'ek barsha', 'yati din',
                    'yati samay', 'kati din dekhi', 'kina bheteko',
                    'kasari chaliyo', 'kasari badyo', 'kasari sudhriyo',
                    'suru dekhi', 'aba samma', 'kitna time', 'kati arsa',
                    'ek barsama', 'saal bhari', 'din gaye', 'samay gayo',
                    'formal thiyo', 'formal thiye', 'har 4 din'
                ],
                'categories': [
                    'relationship_timeline', 'relationship_growth',
                    'relationship_dynamic', 'relationship_start'
                ],
                'content_matches': [
                    'year', 'formal', '4 days', 'beautiful', 'trust',
                    'sambandha', 'rishta', 'barsadekhi', 'har 4 din',
                    'sunaulo', 'formal thiyo', 'ek barsama'
                ],
                'boost': 30
            },

            # ── Promises ──────────────────────────────────────────────────
            'promises': {
                'keywords': [
                    'promise', 'promised', 'always there', 'commitment', 'vow',
                    'swear', 'never leave', 'forever', 'always be',
                    'vachan', 'vaada', 'vada', 'promise gareko', 'kasam',
                    'hamesha', 'hamesha rahnchhu', 'kabhi chhordina',
                    'satha hunchu', 'sanga rahnchhu', 'chhadna', 'chhadne chaina',
                    'sadhai satha', 'sadhai hunchu', 'kina promise',
                    'ke promise', 'vaada gareko', 'vachan gareko'
                ],
                'categories': ['promises'],
                'content_matches': [
                    'promised', 'always', 'deserves', 'world',
                    'vachan', 'vaada', 'sadhai satha', 'kabhi chhordina',
                    'hamesha usko satha', 'sachchi'
                ],
                'boost': 30
            },

            # ── Apologies / sorry ──────────────────────────────────────────
            'apologies': {
                'keywords': [
                    'sorry', 'apology', 'apologize', 'forgive', 'forgiveness',
                    'mistake', 'say sorry', 'always sorry',
                    'maaf', 'maafi', 'sorry bhanchu', 'sorry bhaneko',
                    'maaf garchhe', 'maaf garyo', 'galti', 'galti gareko',
                    'maafi magnu', 'maafi magchhu', 'kina sorry',
                    'sorry bhanchhau', 'sorry bhandaichu', 'maaf gardiye',
                    'hamro sorry', 'maafi ko kura'
                ],
                'categories': ['apologies'],
                'content_matches': [
                    'sorry', 'forgives', 'thing',
                    'maaf', 'maafi', 'galti', 'maaf gardiye',
                    'hamro afnai kura', 'sorry bhaniranchhu'
                ],
                'boost': 28
            },

            # ── My identity / personal info ────────────────────────────────
            'my_identity': {
                'keywords': [
                    'yamraj', 'khadka', 'your name', 'who are you', 'born',
                    'birthday', 'scorpio', 'zodiac', 'rashi', 'monday',
                    'december', '2001', 'middle child',
                    'yamraj', 'tero naam', 'tapaai ko naam', 'naam ke ho',
                    'ko ho timi', 'ko hau', 'janam', 'janma', 'birthday kab',
                    'janma din', 'rashifal', 'rashi ke ho', 'kasto rashi',
                    'scorpio rashi', 'december ma', 'december 15',
                    'sombar', 'somabara', 'majhilo chhora',
                    'tero parichay', 'tapaai ko parichay'
                ],
                'categories': ['my_identity', 'my_background', 'my_personality', 'my_hobbies'],
                'content_matches': [
                    'yamraj', 'khadka', 'december', 'scorpio', 'monday', '2001',
                    'sombar', 'janma', 'rashi', 'majhilo chhora', 'puuro naam'
                ],
                'boost': 35
            },

            # ── My hobbies / interests ─────────────────────────────────────
            'hobbies': {
                'keywords': [
                    'chess', 'hobby', 'hobbies', 'interest', 'passion', 'play',
                    'game', 'introvert', 'strategy',
                    'chess khelchhu', 'chess khelna', 'daam', 'satranj',
                    'man laagchha', 'ruchhi', 'khelna man parcha',
                    'chess man parcha', 'introvert', 'eklo basna', 'khel',
                    'khelkud', 'strategy khelna', 'dimag ko khel',
                    'tero hobby', 'ke man parcha', 'ke khelchhu',
                    'introvert hau', 'introvert ho'
                ],
                'categories': ['my_hobbies'],
                'content_matches': [
                    'chess', 'passion', 'strategy', 'introvert',
                    'satranj', 'ruchhi', 'khelna', 'dimag', 'ghantau ghanta'
                ],
                'boost': 30
            },

            # ── Education / background / location ─────────────────────────
            'education': {
                'keywords': [
                    'study', 'studying', 'engineer', 'engineering', 'computer',
                    'degree', 'college', 'university', 'final year', 'graduate',
                    'undergraduate', 'baijanath', 'banke',
                    'padhna', 'padhchhu', 'padhai', 'computer engineering',
                    'engineering padhchhu', 'final year ma', 'degree',
                    'college ma', 'university ma', 'padhera', 'padheko',
                    'baijanath', 'banke', 'ghar kaha', 'kaha baschhau',
                    'kaha padhchhu', 'ke padhchhu', 'tero padhai'
                ],
                'categories': ['my_background', 'my_identity', 'dreams', 'location'],
                'content_matches': [
                    'computer engineering', 'final year', 'baijanath', 'banke', 'degree',
                    'padhdaichhu', 'lagbhag degree', 'kaha baschhau', 'thaau'
                ],
                'boost': 30
            },

            # ── Her family ─────────────────────────────────────────────────
            'her_family': {
                'keywords': [
                    'her family', 'her brother', 'her sister', 'alisha',
                    'niece', 'nephew', 'her parents', 'her siblings',
                    'usko pariwar', 'uski pariwar', 'usko daju', 'usko bhai',
                    'usko didi', 'usko bahini', 'alisha', 'bhanji',
                    'ushni pariwar', 'uski ghar', 'ushni daju',
                    'ushni bhai', 'ushni didi', 'ushni aama', 'ushni buwa',
                    'girlfriend ko pariwar', 'uski niece', 'baby alisha'
                ],
                'categories': ['her_family'],
                'content_matches': [
                    'alisha', 'elder brothers', 'elder sister', '3-month',
                    'bhanji', 'usko daju', 'usko didi', 'daju ra didi',
                    'mahina ko chhori'
                ],
                'boost': 33
            },

            # ── Dreams / future ────────────────────────────────────────────
            'dreams': {
                'keywords': [
                    'dream', 'future', 'graduate', 'together forever', 'someday',
                    'hope', 'wish', 'plan', 'goal', 'aspire',
                    'sapana', 'sapna', 'bhabishya', 'bhavishya', 'aune din',
                    'ek din', 'sanga basna', 'sanga rahna',
                    'future ma', 'aagadi', 'life ma', 'sath ma basna',
                    'sapana ke ho', 'sapna ke ho', 'graduate bhayepachi',
                    'degree sakiepachi', 'aune din sath', 'hamesha sath'
                ],
                'categories': ['dreams'],
                'content_matches': [
                    'graduate', 'future', 'dream', 'together', 'someday',
                    'sapana', 'bhavishya', 'degree sakiyo', 'gannu paraina',
                    'sanga basnu', 'saadhaaran jeevan'
                ],
                'boost': 28
            },

            # ── Special moments / dates ────────────────────────────────────
            'special_moments': {
                'keywords': [
                    'date', 'restaurant', 'stargazing', 'night', 'stars',
                    'orion', 'special', 'moment', 'memory', 'remember',
                    'khana khaeko', 'restaurant gako', 'tara hereko',
                    'raat ma baseko', 'tara ko kura', 'orion belt',
                    'bistaar kura gareko', 'yaad chha', 'yaad cha',
                    'bisesh din', 'bisesh pal', 'bistaar boli',
                    'tara hereko bela', 'raat bistaar', 'din yaad cha'
                ],
                'categories': ['special_moments'],
                'content_matches': [
                    'restaurant', 'stargazing', 'orion', 'dreams', 'talked',
                    'tara hereko', 'bistaar kura', 'yaad chha', 'khana khaeko',
                    'raat bistaar'
                ],
                'boost': 28
            },

            # ── Inside jokes ───────────────────────────────────────────────
            'inside_jokes': {
                'keywords': [
                    'joke', 'funny', 'pineapple', 'pizza', 'laugh', 'tease',
                    'inside joke', 'argue',
                    'joke', 'hanso', 'hansaune', 'pineapple pizza',
                    'pizza ko kura', 'pizza ma pineapple', 'hasamkhel',
                    'chidhaaune', 'taunt', 'haasikhushi', 'ramilo kura',
                    'haami ko joke', 'ramro joke', 'jhagada ko kura',
                    'argue gareko', 'tarkibadi', 'kura gareko'
                ],
                'categories': ['inside_jokes'],
                'content_matches': [
                    'pineapple', 'pizza', 'team yes', 'team no',
                    'hasamkhel', 'argue gareko', 'pizza maa pineapple',
                    'hansaune'
                ],
                'boost': 25
            },
        }

        # ══════════════════════════════════════════════════════════════════
        # SCORING ENGINE
        # ══════════════════════════════════════════════════════════════════
        scored_memories = []
        for memory in self.memories:
            content = memory.get('content', '').lower()
            category = memory.get('category', '').lower()

            score = 0

            # Direct word matching (base score)
            for word in query_lower.split():
                if len(word) > 2:
                    if word in content:
                        score += 3

            # Check each keyword group
            for group_name, group_info in keyword_groups.items():
                has_keyword = any(kw in query_lower for kw in group_info['keywords'])

                if has_keyword:
                    # Category match boost
                    if category in group_info['categories']:
                        score += group_info['boost']

                    # Content match boost
                    content_matches = sum(
                        1 for cm in group_info['content_matches'] if cm in content
                    )
                    score += content_matches * 15

            # Importance boost
            importance = memory.get('importance', 5)
            score += importance * 0.5

            if score > 0:
                scored_memories.append((score, memory))

        scored_memories.sort(key=lambda x: x[0], reverse=True)
        return [m[1] for m in scored_memories[:k]]

    # ══════════════════════════════════════════════════════════════════════
    # UTILITY METHODS
    # ══════════════════════════════════════════════════════════════════════

    def get_memory_by_category(self, category: str) -> List[Dict]:
        """Get all memories of a specific category"""
        return [m for m in self.memories if m.get('category') == category]

    def get_recent_memories(self, n: int = 5) -> List[Dict]:
        """Get most recent memories"""
        return sorted(self.memories, key=lambda x: x.get('date', ''), reverse=True)[:n]

    def get_important_memories(self, threshold: int = 7) -> List[Dict]:
        """Get memories above importance threshold"""
        return [m for m in self.memories if m.get('importance', 0) >= threshold]

    def add_memory(self, content: str, category: str, importance: int = 5):
        """Add a new memory"""
        new_memory = {
            'id': len(self.memories) + 1,
            'category': category,
            'content': content,
            'date': datetime.now().strftime('%Y-%m-%d'),
            'importance': importance
        }
        self.memories.append(new_memory)
        self._save_memories()

    def _save_memories(self):
        """Save memories to JSON file"""
        try:
            with open(self.memory_file, 'w', encoding='utf-8') as f:
                json.dump({'memories': self.memories}, f, indent=2, ensure_ascii=False)
            print("✅ Memories saved")
        except Exception as e:
            print(f"❌ Error saving memories: {e}")

    def get_stats(self) -> Dict:
        """Get memory statistics"""
        categories = {}
        for memory in self.memories:
            cat = memory.get('category', 'unknown')
            categories[cat] = categories.get(cat, 0) + 1
        return {
            'total_memories': len(self.memories),
            'categories': categories,
            'oldest_memory': min((m.get('date', '') for m in self.memories), default='N/A'),
            'newest_memory': max((m.get('date', '') for m in self.memories), default='N/A')
        }


if __name__ == "__main__":
    agent = MemoryAgent()
    print("\n🧠 Memory Agent Test\n")
    print(f"Stats: {agent.get_stats()}\n")
    
    # Test girlfriend identity queries
    test_queries = [
        "who is lalita oli",
        "tell me about my girlfriend",
        "detail of my gf",
        "mero gf ko nam k ho",
        "lalita ko baare ma bata"
    ]
    
    for query in test_queries:
        results = agent.retrieve_memories(query, k=3)
        print(f"\nQuery: {query}")
        for i, r in enumerate(results, 1):
            print(f"  {i}. [{r['category']}] {r['content'][:80]}...")