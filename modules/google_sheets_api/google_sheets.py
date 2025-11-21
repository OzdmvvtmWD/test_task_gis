import os.path
import requests
from pprint import pprint

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

from modules.google_sheets_api.methods.google_sheet_read import ReadMixin
from modules.google_sheets_api.methods.google_sheet_update import UpdateMixin
from modules.google_sheets_api.methods.google_sheet_create import CreateMixin
from modules.google_sheets_api.methods.google_sheet_delete import DeleteMixin

SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]


class GoogleSheet(
    CreateMixin,
    UpdateMixin,
    ReadMixin,
    DeleteMixin
):
    def __init__(self, credentials_folder_path):
        self._creds = None
        self._service = None

        self._init_token(credentials_folder_path)
        self._headers = {}
        self._headers['Authorization'] = f"Bearer {self.creds.token}"
        self._headers['Content-Type'] =  "application/json"
        
    
    @property
    def creds(self):
        return self._creds
    
    @creds.setter
    def creds(self, value):
        self._creds = value

    @property
    def service(self):
        return self._service

    @service.setter
    def service(self, value):
        self._service = value

    @property
    def headers(self):
        return self._headers
    
    @headers.setter
    def headers(self, value):
        self._headers = value

    

    def _init_token(self, credentials_folder_path:str):
        token_path = os.path.join(credentials_folder_path, "token.json")
        creds_path = os.path.join(credentials_folder_path, "credentials.json")

        if os.path.exists(token_path):
            self.creds = Credentials.from_authorized_user_file(token_path, SCOPES)

        if not self.creds or not self.creds.valid:
            if self.creds and self.creds.expired and self.creds.refresh_token:
                self.creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    creds_path, SCOPES
                )
                self.creds = flow.run_local_server(port=8080)

            with open(token_path, "w") as token:
                token.write(self.creds.to_json())

        self.service = build("sheets", "v4", credentials=self.creds)



    



    


    