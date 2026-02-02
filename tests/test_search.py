# tests/test_list.py

from src.core import load_creds, search_files

def test_google_drive_list_files():
    creds = load_creds()
    files = search_files(creds=creds)

    print(f"\nFiles: ")
    for file in files:
        print(f"-> {file}\n")
    print(f"Number of files: {len(files)}")

    assert files is not None
    assert isinstance(files,list)
    