from typing import List, Dict
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sentence_transformers import SentenceTransformer
from scipy.spatial.distance import cosine

class Ranker:
    def __init__(self, 
                 semantic_weight: float = 0.7,
                 lexical_weight: float = 0.3,
                 model_name: str = "all-MiniLM-L6-v2"):
        self.semantic_weight = semantic_weight
        self.lexical_weight = lexical_weight
        self.tfidf = TfidfVectorizer()
        self.encoder = SentenceTransformer(model_name)
        
    def rank(self, query: str, documents: List[Dict]) -> List[Dict]:
        if not documents:
            return []
            
        texts = [doc["text"] for doc in documents]
        
        try:
            tfidf_matrix = self.tfidf.fit_transform([query] + texts)
            lexical_scores = (tfidf_matrix[1:] @ tfidf_matrix[0].T).toarray().flatten()
        except:
            lexical_scores = np.zeros(len(texts))
            
        try:
            query_embedding = self.encoder.encode(query)
            doc_embeddings = self.encoder.encode(texts)
            semantic_scores = [1 - cosine(query_embedding, doc_emb) for doc_emb in doc_embeddings]
        except:
            semantic_scores = np.zeros(len(texts))
            
        final_scores = (
            self.semantic_weight * np.array(semantic_scores) +
            self.lexical_weight * np.array(lexical_scores)
        )
        
        ranked_pairs = sorted(zip(final_scores, documents), reverse=True)
        ranked_documents = [doc for _, doc in ranked_pairs]
        
        for score, doc in zip(final_scores, ranked_documents):
            doc["rank_score"] = float(score)
        
        return ranked_documents
