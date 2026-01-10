import faiss
import numpy as np
import pickle
import os
from typing import Optional, Tuple

class FAISSStore:
    def __init__(self, dimension: int = 384, index_path: str = "faiss_index.bin"):
        """
        Initialize FAISS index for vector storage
        dimension: embedding vector size (384 for all-MiniLM-L6-v2)
        """
        self.dimension = dimension
        self.index_path = index_path
        self.metadata_path = index_path.replace(".bin", "_metadata.pkl")
        
        # Load existing index or create new
        if os.path.exists(self.index_path):
            self.index = faiss.read_index(self.index_path)
            with open(self.metadata_path, 'rb') as f:
                self.metadata = pickle.load(f)
        else:
            # IndexFlatL2 for exact L2 distance search
            self.index = faiss.IndexFlatL2(dimension)
            self.metadata = {}  # Maps index_id -> resume_id
    
    def add_embedding(self, resume_id: int, embedding: np.ndarray) -> int:
        """
        Add embedding to FAISS index
        Returns: FAISS index ID
        """
        # Reshape to (1, dimension) for single vector
        embedding = embedding.reshape(1, -1).astype('float32')
        
        # Add to index
        faiss_id = self.index.ntotal
        self.index.add(embedding)
        
        # Store metadata
        self.metadata[faiss_id] = resume_id
        
        # Persist to disk
        self._save()
        
        return faiss_id
    
    def search(self, query_embedding: np.ndarray, k: int = 5) -> list:
        """
        Search for k nearest neighbors
        Returns: list of (resume_id, distance)
        """
        query_embedding = query_embedding.reshape(1, -1).astype('float32')
        
        # Search
        distances, indices = self.index.search(query_embedding, k)
        
        # Map FAISS IDs to resume IDs
        results = []
        for i, idx in enumerate(indices[0]):
            if idx != -1:  # Valid result
                resume_id = self.metadata.get(idx)
                if resume_id:
                    results.append((resume_id, float(distances[0][i])))
        
        return results
    
    def get_embedding(self, faiss_id: int) -> Optional[np.ndarray]:
        """
        Retrieve embedding by FAISS ID
        """
        if faiss_id >= self.index.ntotal:
            return None
        
        # Reconstruct vector from index
        embedding = self.index.reconstruct(int(faiss_id))
        return embedding
    
    def _save(self):
        """
        Persist index and metadata to disk
        """
        faiss.write_index(self.index, self.index_path)
        with open(self.metadata_path, 'wb') as f:
            pickle.dump(self.metadata, f)

# Global instance
faiss_store = FAISSStore()