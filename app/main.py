import os
from pathlib import Path

from fastapi import FastAPI, Request, UploadFile, File, Form
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from .config import APP_NAME, TOP_K, UPLOAD_DIR
from .parsers import parse_file
from .chunker import chunk_text
from .embedder import embed_texts, embed_query
from .store import get_stats
from .rag import build_answer
from .retriever import Retriever

BASE_DIR = Path(__file__).resolve().parent
STATIC_DIR = BASE_DIR / "static"
TEMPLATES_DIR = BASE_DIR / "templates"

os.makedirs(UPLOAD_DIR, exist_ok=True)

app = FastAPI(title=APP_NAME)
app.mount("/static", StaticFiles(directory=str(STATIC_DIR)), name="static")
templates = Jinja2Templates(directory=str(TEMPLATES_DIR))

retriever = Retriever()


def render_home(request, message="", results=None, answer="", query="", related=None):
    if results is None:
        results = []
    if related is None:
        related = []

    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={
            "message": message,
            "results": results,
            "answer": answer,
            "query": query,
            "related": related,
            "stats": get_stats(),
            "retriever_mode": retriever.current_mode(),
            "sample_queries": [
                "What is normalization in DBMS?",
                "Explain binary search time complexity",
                "What is overfitting in machine learning?",
                "Show notes about operating systems scheduling"
            ],
            "collections": ["Study", "Code", "Docs", "Support"]
        }
    )


@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return render_home(
        request,
        message="Upload your files and search them semantically."
    )


@app.post("/upload", response_class=HTMLResponse)
async def upload_file(
    request: Request,
    file: UploadFile = File(...),
    topic: str = Form("General"),
    collection: str = Form("Study")
):
    file_path = os.path.join(UPLOAD_DIR, file.filename)

    with open(file_path, "wb") as f:
        f.write(await file.read())

    text = parse_file(file_path)
    chunks = chunk_text(text)

    if not chunks:
        return render_home(
            request,
            message="No usable text found in this file."
        )

    vectors = embed_texts(chunks)

    records = []
    for i, chunk in enumerate(chunks):
        records.append({
            "id": f"{file.filename}-{i}",
            "text": chunk,
            "metadata": {
                "file_name": file.filename,
                "file_type": file.filename.split(".")[-1],
                "collection": collection,
                "topic": topic,
                "chunk_id": i
            }
        })

    result = retriever.add(records, vectors)

    return render_home(
        request,
        message=f"{file.filename} indexed successfully with {len(chunks)} chunks in collection '{collection}'. Retrieval mode: {result['mode']}."
    )


@app.post("/search", response_class=HTMLResponse)
async def search(
    request: Request,
    query: str = Form(...),
    collection: str = Form(""),
    topic: str = Form(""),
    file_type: str = Form("")
):
    qvec = embed_query(query)

    results = retriever.search(
        qvec,
        top_k=TOP_K,
        collection=collection or None,
        topic=topic or None,
        file_type=file_type or None
    )

    related = retriever.related(results[0]["id"], top_k=3) if results else []

    return render_home(
        request,
        message=f"Found {len(results)} result(s) for: {query}",
        results=results,
        query=query,
        related=related
    )


@app.post("/ask", response_class=HTMLResponse)
async def ask(
    request: Request,
    query: str = Form(...),
    collection: str = Form(""),
    topic: str = Form(""),
    file_type: str = Form("")
):
    qvec = embed_query(query)

    results = retriever.search(
        qvec,
        top_k=TOP_K,
        collection=collection or None,
        topic=topic or None,
        file_type=file_type or None
    )

    answer = build_answer(query, results)
    related = retriever.related(results[0]["id"], top_k=3) if results else []

    return render_home(
        request,
        message=f"Answer generated from top {len(results)} retrieved chunk(s).",
        results=results,
        answer=answer,
        query=query,
        related=related
    )