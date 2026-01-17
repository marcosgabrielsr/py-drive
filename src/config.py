import os.path
from core import Credentials, SCOPES

def load_creds(path: str = "token.json"):
    if os.path.exists(path):
        return Credentials.from_authorized_user_file("token.json", SCOPES)