"""This module provides the OAtuh 2.0 autentication functionality"""
# src/core/auth.py

import os

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow

from src.config import CREDENTIALS_FILE, TOKEN_FILE, SCOPES

def load_creds() -> Credentials:
    """
    Load the user credentials or starts the login flow if needed
    """
    creds = None

    if os.path.exists(TOKEN_FILE):
        creds = Credentials.from_authorized_user_file(str(TOKEN_FILE), SCOPES)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            try:
                creds.refresh(Request())
            except Exception:
                creds = None
        
        if not creds:
            creds = _new_login()

    with open(TOKEN_FILE, "w") as token:
        token.write(creds.to_json())

    return creds

def _new_login() -> Credentials:
    """
    Auxiliar intern function to open the browser and exec login
    """
    if not os.path.exists(CREDENTIALS_FILE):
        raise FileNotFoundError(f"Credentials file not found on: {CREDENTIALS_FILE}")
    
    flow = InstalledAppFlow.from_client_secrets_file(str(CREDENTIALS_FILE), SCOPES)
    return flow.run_local_server(port=0)