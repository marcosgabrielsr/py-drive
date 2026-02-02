"""This module provides Google Drive API v3 functionality"""
# src/core/drive.py

import io

from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from googleapiclient.http import MediaIoBaseDownload

from src.config import DEFAULT_DOWNLOAD_DIR

def build_query(
        only_folders:bool=False,
        only_my_own:bool=True,
        name:str=None,
        in_name:str=None,
        not_trashed:bool=False
    ) -> str:
    """Build the query to filter the search on google drive

    Args:
        only_folders: bool, option to pick up only folders.
        only_my_own: bool, option to only retrieve files where I am one of the owners.
        name: str, Name of the file to be searched for.
        in_name: str, text that can be part of the file name.
        not_trashed: str, option to pick up only files that not in trash.
    
    Returns:
        Return a string that is the query that will be used on the Google Drive API v3 request.
    """
    query = ("trashed=false","trashed=true")[not_trashed]
    query = (query,f"{query} and mimeType='application/vnd.google-apps.folder'")[only_folders]
    query = (query,f"{query} and 'me' in owners")[only_my_own]
    query = (query,f"{query} and name = '{name}'")[name is not None]
    query = (query,f"{query} and name contains '{in_name}'")[in_name is not None]

    return query

def search_files(
        creds:Credentials,
        order:str=None,
        pg_size:int=None,
        folders:bool=False,
        my_own:bool=True,
        name:str=None,
        in_name:str=None,
        not_trashed:bool=False,
        show_query:bool=False
    ) -> list:
    """List and search files from drive

    Args:
        creds: Credentials, access token for authentication.
        oder: str, query listing order.
        pg_size: int, number of files read per page.
        folder: bool, option to pick up only folders.
        my_own: bool, option to only retrieve files where I am one of the owners.
        name: str, Name of the file to be searched for.
        in_name: str, text that can be part of the file name.
        not_trashed: str, option to pick up only files that not in trash.
        show_query: bool, option to print or not the query used to search.

    Returns:
        Return a dictionary list where each element contain the files properties (id, name and mimeType in this case).
    """
    query = build_query(only_folders=folders,only_my_own=my_own,name=name,in_name=in_name,not_trashed=not_trashed)
    files = []
    page_token = None

    try:
        service = build("drive","v3",credentials=creds)

        if show_query:
            print(f"\ncurrent query:\n===> {query}")

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

def download_file(
        creds:Credentials,
        file_name:str=None,
        real_file_id:str=None,
        final_path:str=DEFAULT_DOWNLOAD_DIR
    ) -> str:
    """Make the download from google drive
    
    Args:
        creds: Credentials, access token for authentication.
        real_file_id: str, id of the file to download.
        final_path: str, local path to download.
    
    Returns:
        IO object with location
    """

    print(f"\nfinal path: {final_path}.")

    if file_name is None and real_file_id is None:
        print(f"Error: name and id not informed!")
        return

    elif real_file_id is None:
        print(f"Searching for the file id...")
        sfile = list_files(creds=creds,name=file_name)

        if sfile is None:
            print("Error: file not found on drive")
            return
        
        real_file_id = sfile['id']
    
    else:
        print(f"File ID informed. Checking if the file exists")
        files = search_files(creds)


    try:
        service = build("drive","v3",credentials=creds)
        file_id = real_file_id

        request = service.files().get_media(fileID=file_id)
        file = io.BytesIO()
        downloader = MediaIoBaseDownload(file,request)
        done = False

        while done is False:
            status, done = downloader.next_chunk()
            print(f"Download {int(status.progress() * 100)}")
    
    except HttpError as error:
        print(f"An error occurred: {error}")
        file = None

    return file.getvalue()