from sentence_transformers import SentenceTransformer
import numpy as np
from typing import List
import logging

logger = logging.getLogger(__name__)

# Load model once (singleton pattern for performance)
class EmbeddingService:
    _instance = None
    _model = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(EmbeddingService, cls).__new__(cls)
            # Load lightweight, fast model (384 dimensions)
            cls._model = SentenceTransformer('all-MiniLM-L6-v2')
            logger.info("Sentence Transformer model loaded successfully")
        return cls._instance
    
    def generate_embedding(self, text: str) -> np.ndarray:
        """
        Generate embedding vector for text
        Returns: numpy array of shape (384,)
        """
        if not text or not text.strip():
            raise ValueError("Text cannot be empty")
        
        # Generate embedding
        embedding = self._model.encode(text, convert_to_numpy=True)
        return embedding
    
    def generate_batch_embeddings(self, texts: List[str]) -> np.ndarray:
        """
        Generate embeddings for multiple texts (faster)
        Returns: numpy array of shape (n, 384)
        """
        embeddings = self._model.encode(texts, convert_to_numpy=True)
        return embeddings
    
    def compute_similarity(self, embedding1: np.ndarray, embedding2: np.ndarray) -> float:
        """
        Compute cosine similarity between two embeddings
        Returns: float between 0 and 1
        """
        # Normalize vectors
        embedding1_norm = embedding1 / np.linalg.norm(embedding1)
        embedding2_norm = embedding2 / np.linalg.norm(embedding2)
        
        # Cosine similarity
        similarity = np.dot(embedding1_norm, embedding2_norm)
        
        # Convert to 0-1 range (from -1 to 1)
        similarity = (similarity + 1) / 2
        
        return float(similarity)

# Global instance
embedding_service = EmbeddingService()