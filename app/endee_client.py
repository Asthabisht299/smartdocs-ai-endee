import requests

ENDEE_BASE_URL = "http://127.0.0.1:8080"


def health_check():
    try:
        response = requests.get(f"{ENDEE_BASE_URL}/health", timeout=3)
        return response.status_code == 200
    except Exception:
        return False


def upsert_vectors(index_name, items):
    payload = {
        "index": index_name,
        "items": items
    }
    try:
        response = requests.post(
            f"{ENDEE_BASE_URL}/indexes/{index_name}/upsert",
            json=payload,
            timeout=20
        )
        return response.status_code, response.text
    except Exception as e:
        return 500, str(e)


def search_vectors(index_name, vector, top_k=5, filters=None):
    payload = {
        "vector": vector,
        "top_k": top_k,
        "filters": filters or {}
    }
    try:
        response = requests.post(
            f"{ENDEE_BASE_URL}/indexes/{index_name}/search",
            json=payload,
            timeout=20
        )
        return response.status_code, response.json()
    except Exception as e:
        return 500, {"error": str(e)}