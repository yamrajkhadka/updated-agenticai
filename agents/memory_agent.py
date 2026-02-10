"""
Memory Agent with RAG
Retrieves relevant memories using vector search
"""

import json
import os
from typing import List, Dict, Optional
from datetime import datetime

try:
    from langchain_community.embeddings import HuggingFaceEmbeddings
    from langchain_community.vectorstores import FAISS
    from langchain_core.documents import Document
    VECTOR_AVAILABLE = True
except ImportError:
    VECTOR_AVAILABLE = False
    print("⚠️  Vector search not available. Install: pip install faiss-cpu sentence-transformers")


class MemoryAgent:
    """Manages and retrieves relationship memories using RAG"""
    
    def __init__(self, memory_file: str = "memory/memories.json"):
        """
        Initialize memory agent
        
        Args:
            memory_file: Path to JSON file containing memories
        """
        self.memory_file = memory_file
        self.memories = []
        self.vector_store = None
        
        # Load memories
        self._load_memories()
        
        # Initialize vector store if available
        if VECTOR_AVAILABLE and self.memories:
            self._initialize_vector_store()
    
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
    
    def _initialize_vector_store(self):
        """Initialize FAISS vector store with embeddings"""
        try:
            # Create embeddings model
            embeddings = HuggingFaceEmbeddings(
                model_name="sentence-transformers/all-MiniLM-L6-v2"
            )
            
            # Convert memories to documents
            documents = []
            for memory in self.memories:
                content = memory.get('content', '')
                metadata = {
                    'id': memory.get('id'),
                    'category': memory.get('category'),
                    'date': memory.get('date'),
                    'importance': memory.get('importance', 5)
                }
                doc = Document(page_content=content, metadata=metadata)
                documents.append(doc)
            
            # Create vector store
            if documents:
                self.vector_store = FAISS.from_documents(documents, embeddings)
                print("✅ Vector store initialized")
            else:
                print("⚠️  No documents to create vector store")
                
        except Exception as e:
            print(f"❌ Vector store initialization failed: {e}")
            self.vector_store = None
    
    def retrieve_memories(self, query: str, k: int = 3) -> List[Dict]:
        """
        Retrieve relevant memories using vector search
        
        Args:
            query: Search query
            k: Number of memories to retrieve
            
        Returns:
            List of relevant memories
        """
        if not self.vector_store:
            # Fallback to simple search
            return self._simple_search(query, k)
        
        try:
            # Vector similarity search
            docs = self.vector_store.similarity_search(query, k=k)
            
            # Convert back to memory format
            results = []
            for doc in docs:
                memory = {
                    'content': doc.page_content,
                    'category': doc.metadata.get('category'),
                    'date': doc.metadata.get('date'),
                    'importance': doc.metadata.get('importance')
                }
                results.append(memory)
            
            return results
            
        except Exception as e:
            print(f"❌ Vector search failed: {e}")
            return self._simple_search(query, k)
    
    def _simple_search(self, query: str, k: int = 3) -> List[Dict]:
        """
        Simple keyword-based search (fallback)
        
        Args:
            query: Search query
            k: Number of results
            
        Returns:
            List of matching memories
        """
        query_lower = query.lower()
        
        # Score memories by keyword matches
        scored_memories = []
        for memory in self.memories:
            content = memory.get('content', '').lower()
            score = sum(1 for word in query_lower.split() if word in content)
            if score > 0:
                scored_memories.append((score, memory))
        
        # Sort by score and importance
        scored_memories.sort(
            key=lambda x: (x[0], x[1].get('importance', 5)),
            reverse=True
        )
        
        return [m[1] for m in scored_memories[:k]]
    
    def get_memory_by_category(self, category: str) -> List[Dict]:
        """
        Get all memories of a specific category
        
        Args:
            category: Memory category
            
        Returns:
            List of memories in that category
        """
        return [m for m in self.memories if m.get('category') == category]
    
    def get_recent_memories(self, n: int = 5) -> List[Dict]:
        """
        Get most recent memories
        
        Args:
            n: Number of memories to retrieve
            
        Returns:
            List of recent memories
        """
        # Sort by date (newest first)
        sorted_memories = sorted(
            self.memories,
            key=lambda x: x.get('date', ''),
            reverse=True
        )
        return sorted_memories[:n]
    
    def get_important_memories(self, threshold: int = 7) -> List[Dict]:
        """
        Get memories above importance threshold
        
        Args:
            threshold: Minimum importance (1-10)
            
        Returns:
            List of important memories
        """
        return [
            m for m in self.memories 
            if m.get('importance', 0) >= threshold
        ]
    
    def add_memory(self, content: str, category: str, importance: int = 5):
        """
        Add a new memory
        
        Args:
            content: Memory content
            category: Memory category
            importance: Importance rating (1-10)
        """
        new_memory = {
            'id': len(self.memories) + 1,
            'category': category,
            'content': content,
            'date': datetime.now().strftime('%Y-%m-%d'),
            'importance': importance
        }
        
        self.memories.append(new_memory)
        
        # Save to file
        self._save_memories()
        
        # Reinitialize vector store
        if VECTOR_AVAILABLE:
            self._initialize_vector_store()
    
    def _save_memories(self):
        """Save memories to JSON file"""
        try:
            with open(self.memory_file, 'w', encoding='utf-8') as f:
                json.dump({'memories': self.memories}, f, indent=2)
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
            'oldest_memory': min(
                (m.get('date', '') for m in self.memories),
                default='N/A'
            ),
            'newest_memory': max(
                (m.get('date', '') for m in self.memories),
                default='N/A'
            )
        }


# Example usage
if __name__ == "__main__":
    agent = MemoryAgent()
    
    print("\n🧠 Memory Agent Demo\n")
    print(f"Stats: {agent.get_stats()}\n")
    
    # Test retrieval
    query = "first time we met"
    print(f"Query: '{query}'")
    results = agent.retrieve_memories(query, k=2)
    
    for i, memory in enumerate(results, 1):
        print(f"\n{i}. {memory['content']}")
        print(f"   Category: {memory['category']}")
        print(f"   Date: {memory['date']}")