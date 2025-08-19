# # backend/memory_manager.py

import faiss
import pickle

class MemoryManager:
    def __init__(self):
        self.vector_store = faiss.IndexFlatL2(384)
        self.contexts = []

    def add_context(self, embedding, text):
        self.vector_store.add(embedding)
        self.contexts.append(text)

    def retrieve(self, embedding, top_k=3):
        D, I = self.vector_store.search(embedding, top_k)
        return [self.contexts[i] for i in I[0]]

def save_to_memory(key, value):
    print(f"[Memory Saved] {key}: {value}")
