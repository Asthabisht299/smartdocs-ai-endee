import os
from dotenv import load_dotenv

load_dotenv()

APP_NAME = "SmartDocs AI"
TOP_K = int(os.getenv("TOP_K", "5"))
UPLOAD_DIR = "uploads"
DATA_DIR = "data"
EMBED_MODEL = os.getenv("EMBED_MODEL", "sentence-transformers/all-MiniLM-L6-v2")