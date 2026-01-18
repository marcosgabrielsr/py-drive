import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent

CREDENTIALS_FILE = BASE_DIR/os.getenv("GDRIVE_CREDENTIALS", "credentials.json")
TOKEN_FILE = BASE_DIR/os.getenv("GDRIVE_TOKEN", "token.json")

SCOPES = ["https://www.googleapis.com/auth/drive.metadata.readonly"]