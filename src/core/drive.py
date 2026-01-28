"""This module provides Google Drive API v3 functionality"""
# src/core/drive.py

from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

def list_files(creds:Credentials,order:str=None,pg_size:int=10) -> list:
    """
    List the number of files passed as a parameter, 10 by default
    """
    try:
        service = build("drive", "v3", credentials=creds)

        results = (
            service.files()
            .list(orderBy=order,pageSize=pg_size,fields="nextPageToken, files (id, name)")
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