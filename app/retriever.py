from .store import add_documents, search_documents, related_chunks
from .endee_client import health_check


class Retriever:
    def __init__(self):
        self.mode = "endee" if health_check() else "local"

    def current_mode(self):
        return self.mode

    def add(self, records, embeddings):
        if self.mode == "local":
            add_documents(records, embeddings)
            return {"status": "ok", "mode": "local"}
        else:
            return {"status": "ok", "mode": "endee-ready"}

    def search(self, query_embedding, top_k=5, collection=None, topic=None, file_type=None):
        if self.mode == "local":
            return search_documents(
                query_embedding,
                top_k=top_k,
                collection=collection,
                topic=topic,
                file_type=file_type
            )
        return []

    def related(self, chunk_id, top_k=3):
        if self.mode == "local":
            return related_chunks(chunk_id, top_k=top_k)
        return []