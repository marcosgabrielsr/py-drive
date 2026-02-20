"""This module provides Google Drive API v3 functionality"""
# src/core/drive.py

import io
import os
from pathlib import Path

from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from googleapiclient.http import MediaIoBaseDownload

from src.config import DEFAULT_DOWNLOAD_DIR
from src.core import load_creds

class GoogleDriveManager:
    def __init__(self):
        """
        Initialize the credentials and service a unique time
        for all tools
        """
        self.creds = load_creds()
        self.service = build("drive","v3",credentials=self.creds)

    def build_query(
        self,
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
            self,
            order:str=None,
            pg_size:int=None,
            folders:bool=False,
            my_own:bool=True,
            name:str=None,
            in_name:str=None,
            not_trashed:bool=False,
            show_query:bool=False
        ) -> list:
        """
        List and search files from drive

        Args:
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
        query = self.build_query(only_folders=folders,only_my_own=my_own,name=name,in_name=in_name,not_trashed=not_trashed)
        files = []
        page_token = None

        try:
            if show_query:
                print(f"\ncurrent query:\n===> {query}")

            while True:
                results = (
                    self.service.files()
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

    def list_downloads_options(
            self,
            files:list=None
        ) -> str:
        """
        List all of the options finded by the search_files on download_files function
        
        Args:
            files: list, list of the finded files.

        Returns:
            'id' of the selected optino
        """
        cancel_option = len(files)+1
        
        while True:
            try:
                print(f"Listing download options (total: {len(files)})")
                for file,i in files.append("Cancel"):
                    print(f"\t[{i}] {file}")

                selected = int(input("Type the number:"))

                if selected >= 0 and selected < cancel_option:
                    return (files[selected])['id']
                elif selected == cancel_option:
                    return None
                else:
                    print('Invalid option.')

            except TypeError:
                print('You must type integer numbers.')
            
            except Exception as e:
                print('Exeception: {e}')


    def get_id_by_name(
            self,
            file_name:str
        ) -> str:
        """
        Responsible for finding the ID by name

        Args: 
            creds: Credentials, access token for authentication.
            name: str, name of the file.

        Returns:
            Return the ID of the file.
        """
        file_data = self.search_files(name=file_name)

        if len(file_data) == 1:
            return (file_data[0])['id']
        else:
            return self.list_downloads_options(file_data)

    def execute_download(
            self,
            real_file_id:str,
            download_path:str
        ) -> io.BytesIO:
        """
        Make the download of a file from Google Drive
        
        Args:
            creds: Credentials, access token for authentication.
            _file_id: str, file id.
            download_path: str, path where the file will be saved.
        
        Returns:
            Return an IO object
        """
        dest_path = Path(download_path)

        try:
            file_metadata = self.service.files().get(fileId=real_file_id,fields="name, size")
            file_name, expected_size = file_metadata.get('name'), int(file_metadata.get('size'))
            save_path = dest_path/file_name

            print(f"Starting download of the file: {file_name}")

            with open(save_path, "wb") as f:
                request = self.service.files().get_media(fileId=real_file_id)
                downloader = MediaIoBaseDownload(f, request)
                done = False

            while done is False:
                status, done = downloader.next_chunk()
                print(f"\nDownload {int(status.progress() * 100)}")
        
            if save_path.exists():
                actual_size = save_path.stat().st_size

                if actual_size != expected_size:
                    return None

        except HttpError as error:
            print(f"An error occurred: {error}")
            file = None

        return file

    def download_file(
            self,
            file_name:str=None,
            real_file_id:str=None,
            final_path:str=DEFAULT_DOWNLOAD_DIR
        ) -> str:
        """
        Define the file id and makes the download of a file from google drive

        Args:
            creds: Credentials, access token for authentication.
            file_name: str, name of the file to download.
            real_file_id: str, id of the file to download.
            final_path: str, local path to download.
        
        Returns:
            IO object with location.
        """
        if file_name is None and real_file_id is None:
            print(f"Error: name and id not informed!")
            return None
        elif real_file_id is None:
            file_id = get_id_by_name(creds,file_name)
        else:
            file_id = real_file_id
        
        file = self.execute_download(file_id,final_path)

        if file is not None:
            return file.getvalue()
        else:
            return None