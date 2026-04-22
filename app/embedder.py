from sentence_transformers import SentenceTransformer
from .config import EMBED_MODEL

model = SentenceTransformer(EMBED_MODEL)

def embed_texts(texts):
    return model.encode(texts, convert_to_numpy=True)

def embed_query(query):
    return model.encode([query], convert_to_numpy=True)[0]