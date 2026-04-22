# SmartDocs AI using Endee

SmartDocs AI is a semantic search and retrieval-augmented question answering system built using Endee Vector Database. It allows users to upload notes, code files, and documents, store embeddings in Endee, and search them using natural language queries.

## Overview
This project helps users find relevant information from large notes or document collections by meaning, not just exact keywords.

## Why this project
Keyword search often misses useful content when the wording is different. This project solves that problem with semantic retrieval and filtered search using Endee.

## Features
- Semantic search
- Document chunking
- Embedding generation
- Vector storage in Endee
- Metadata filtering
- Retrieval-augmented answers

## How Endee is used
Endee is the core retrieval engine in this project. Document chunks are converted into embeddings and stored in Endee along with metadata such as source file and chunk number. When a user enters a query, the app searches Endee for the most relevant chunks and returns them for search or answer generation.

## System Design
1. User uploads document.
2. Text is extracted and split into chunks.
3. Embeddings are created.
4. Chunks are stored in Endee.
5. Query is embedded.
6. Endee returns top matching chunks.
7. Results are shown to the user or passed to an LLM for grounded answers.

## Tech Stack
- Python
- Flask or FastAPI
- Endee Vector Database
- Sentence Transformers
- HTML/CSS or Streamlit

## Setup
```bash
git clone <your-repo-link>
cd <your-project-folder>
pip install -r requirements.txt
python app.py
```

## Screenshots
Add screenshots here.

## Future Improvements
- Better PDF parsing
- More filters
- Improved ranking
- Better UI

## License
This project is submitted for the Endee recruitment task.