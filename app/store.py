import numpy as np
from sklearn.metrics.pairwise import cosine_similarity

DOCUMENTS = []
EMBEDDINGS = None
LAST_UPLOADED = None


def add_documents(records, embeddings):
    global DOCUMENTS, EMBEDDINGS, LAST_UPLOADED

    DOCUMENTS.extend(records)
    LAST_UPLOADED = records[0]["metadata"]["file_name"] if records else LAST_UPLOADED

    if EMBEDDINGS is None:
        EMBEDDINGS = embeddings
    else:
        EMBEDDINGS = np.vstack([EMBEDDINGS, embeddings])


def search_documents(query_embedding, top_k=5, collection=None, topic=None, file_type=None):
    global DOCUMENTS, EMBEDDINGS

    if EMBEDDINGS is None or len(DOCUMENTS) == 0:
        return []

    valid_indices = []
    for i, doc in enumerate(DOCUMENTS):
        meta = doc["metadata"]

        if collection and meta["collection"].lower() != collection.lower():
            continue
        if topic and meta["topic"].lower() != topic.lower():
            continue
        if file_type and meta["file_type"].lower() != file_type.lower():
            continue

        valid_indices.append(i)

    if not valid_indices:
        return []

    filtered_embeddings = EMBEDDINGS[valid_indices]
    scores = cosine_similarity([query_embedding], filtered_embeddings)[0]

    ranked = sorted(
        zip(valid_indices, scores),
        key=lambda x: x[1],
        reverse=True
    )[:top_k]

    results = []
    for idx, score in ranked:
        item = DOCUMENTS[idx].copy()
        item["score"] = float(score)
        results.append(item)

    return results


def related_chunks(base_chunk_id, top_k=3):
    global DOCUMENTS, EMBEDDINGS

    if EMBEDDINGS is None or len(DOCUMENTS) == 0:
        return []

    base_index = None
    for i, doc in enumerate(DOCUMENTS):
        if doc["id"] == base_chunk_id:
            base_index = i
            break

    if base_index is None:
        return []

    base_vector = EMBEDDINGS[base_index]
    scores = cosine_similarity([base_vector], EMBEDDINGS)[0]

    ranked = sorted(
        [(i, s) for i, s in enumerate(scores) if i != base_index],
        key=lambda x: x[1],
        reverse=True
    )[:top_k]

    related = []
    for idx, score in ranked:
        item = DOCUMENTS[idx].copy()
        item["score"] = float(score)
        related.append(item)

    return related


def get_stats():
    file_names = set(doc["metadata"]["file_name"] for doc in DOCUMENTS)
    collections = set(doc["metadata"]["collection"] for doc in DOCUMENTS)

    return {
        "total_documents": len(file_names),
        "total_chunks": len(DOCUMENTS),
        "total_collections": len(collections),
        "last_uploaded": LAST_UPLOADED or "None"
    }