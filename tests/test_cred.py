# tests/test_cred.py

from src.core import Credentials,load_creds

def test_google_drive_creds():
    creds = load_creds()

    assert creds is not None
    assert isinstance(creds,Credentials)