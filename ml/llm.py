from fastapi import HTTPException, status
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from nltk.tokenize import sent_tokenize
import numpy as np
import nltk

from api.documents.crud import DocumentCRUD
from asker.db import async_session


class DocumentLLM:
    def __init__(self):
        self.vectorizer = TfidfVectorizer()
        self.combined_text = ""
    
    def load_model(self):
        nltk.download("punkt")
        nltk.download('punkt_tab')
    
    def generate_answer(
        self,
        question: str,
    ):  
        document_texts = sent_tokenize(self.combined_text)
        if not document_texts:
            return "No data found. Maybe no document uploaded yet?"

        document_texts = [line for s in document_texts for line in s.split('\n')]
        texts = document_texts + [question]
        tfidf_matrix = self.vectorizer.fit_transform(texts)
        cosine_similarities = cosine_similarity(tfidf_matrix[-1], tfidf_matrix[:-1]).flatten()
        most_similar_index = np.argmax(cosine_similarities)
        return document_texts[most_similar_index]

    async def update_content(self):
        async with async_session() as session:
            docs = await DocumentCRUD(session).list()
            self.combined_text = "\n".join(doc.content for doc in docs)
            print(self.combined_text)
