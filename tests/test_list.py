# tests/test_list.py

from src.core import load_creds, list_files

def test_google_drive_list_files():
    creds = load_creds()
    files = list_files(creds=creds)

    assert files is not None
    assert isinstance(files,list)
    