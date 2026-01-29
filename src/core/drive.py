"""This module provides Google Drive API v3 functionality"""
# src/core/drive.py

from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

def list_files(creds:Credentials,order:str=None,pg_size:int=None,folders:bool=False) -> list:
    """
    List and search files from drive
    """
    query = "mimeType='application/vnd.google-apps.folder'" if folders else None
    query = query+"trashed=false" if query is None else "trashed=false"

    try:
        service = build("drive", "v3", credentials=creds)

        results = (
            service.files()
            .list(orderBy=order,pageSize=pg_size,fields="nextPageToken, files (id, name,mimeType)",q=query)
            .execute()
        )
        items = results.get("files", [])

        if not items:
            print("No files found.")
            return
        
        return items
    
    except HttpError as error:
        print(f"An error ocurred: {error}")
        return