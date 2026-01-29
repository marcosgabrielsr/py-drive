"""This module provides Google Drive API v3 functionality"""
# src/core/drive.py

from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

def build_query(only_folders:bool=False,only_not_shared:bool=True,name:str=None,in_name:str=None) -> str:
    """Build the query to filter the search on google drive

    Args:
        only_folders: bool, option to pick up only folders.
        only_not_shared: bool, option to only retrieve files where I am one of the owners.
        name: str, Name of the file to be searched for.
        in_name: str, text that can be part of the file name.
    
    Returns:
        Return a string that is the query that will be used on the Google Drive API v3 request.
    """
    query = "trashed=false"

    query = (query,f"{query} and mimeType='application/vnd.google-apps.folder'")[only_folders]
    query = (query,f"{query} and 'me' in owners")[only_not_shared]
    query = (query,f"{query} and name = '{name}'")[name is not None]
    query = (query,f"{query} and name contains '{in_name}'")[in_name is not None]

    return query

def list_files(
        creds:Credentials,
        order:str=None,
        pg_size:int=None,
        folders:bool=False,
        not_shared:bool=True,
        name:str=None,
        in_name:str=None
    ) -> list:
    """List and search files from drive
    """
    query = build_query(only_folders=folders,only_not_shared=not_shared,name=name,in_name=in_name)
    files = []
    page_token = None

    try:
        print(f"\ncurrent query: {query}")
        service = build("drive","v3",credentials=creds)

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
            
            if not page_token:
                break
        
        if not files:
            print("No files found.")
            return

        return files
    
    except HttpError as error:
        print(f"An error ocurred: {error}")
        return