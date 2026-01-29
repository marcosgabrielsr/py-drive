"""This module provides Google Drive API v3 functionality"""
# src/core/drive.py

from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

def build_query(only_folders:bool=False) -> str:
    query = "trashed=false"

    if only_folders:
        query = f"{query} and mimeType='application/vnd.google-apps.folder'"

    return query


def list_files(creds:Credentials,order:str=None,pg_size:int=None,folders:bool=False) -> list:
    """
    List and search files from drive
    """
    query = build_query(only_folders=folders)
    files = []
    page_token = None

    try:
        print(f"\ncurrent query: {query}")
        service = build("drive", "v3", credentials=creds)

        while True:
            results = (
                service.files()
                .list(
                    orderBy=order,
                    pageSize=pg_size,
                    fields="nextPageToken, files (id, name,mimeType)",
                    q=query,
                    pageToken=page_token
                )
                .execute()
            )
            files.extend(results.get("files", []))
            page_token = results.get('nextPageToken')

            if not files:
                print("No files found.")
                return
            
            if not page_token:
                break
        
        return files
    
    except HttpError as error:
        print(f"An error ocurred: {error}")
        return