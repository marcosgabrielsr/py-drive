# tests/test_path.py

from src.config import DEFAULT_DOWNLOAD_DIR, Path

def test_path_verification():
    print(f"default download dir: {DEFAULT_DOWNLOAD_DIR}")
    
    assert DEFAULT_DOWNLOAD_DIR is not None
    assert isinstance(DEFAULT_DOWNLOAD_DIR,Path)