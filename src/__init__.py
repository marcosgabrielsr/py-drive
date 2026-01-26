"""Top-level package for py-drive"""
# src/__init__.py

__app_name__ = "py-drive"
__version__ = "0.1.0"

(
    SUCCESS,
    UPLOAD_DIR_ERROR,
    DOWNLOAD_DIR_ERROR,
    UPLOAD_ERROR,
    DOWNLOAD_ERROR,
    CONNECTION_ERROR,
    INTERNET_ERROR,
    CREDENTIALS_ERROR,
    TOKEN_ERROR
) = range(9)

ERRORS = {
    UPLOAD_DIR_ERROR: "config upload directory error",
    DOWNLOAD_DIR_ERROR: "config dowload directory error",
    UPLOAD_ERROR: "files upload error",
    DOWNLOAD_ERROR: "files download error",
    CONNECTION_ERROR: "internet connection error",
    CREDENTIALS_ERROR: "credentials config file error",
    TOKEN_ERROR: "token config file error",
}