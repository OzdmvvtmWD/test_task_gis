import os
import requests
from googleapiclient.errors import HttpError
 

class CreateMixin:

    def copy_sheeet(self, spreadsheetId:str, destinationSpreadsheetId:str, sheetId:int = 0 ):

        api_url = f'https://sheets.googleapis.com/v4/spreadsheets/{spreadsheetId}/sheets/{sheetId}:copyTo'
        body = {
            "destinationSpreadsheetId" : destinationSpreadsheetId
        }

        try:
            resp = requests.post(url = api_url, json= body, headers= self.headers)
            status_code = resp.status_code

            print(status_code)
            return resp.json()
            
        except HttpError as error:
            print(error)
            return error
        
    def create_spreadsheets(self, title):
        try:
            spreadsheet = {"properties": {"title": title}}
            spreadsheet = (
                self.service.spreadsheets()
                .create(body=spreadsheet, fields="spreadsheetId")
                .execute()
            )
            print(f"Spreadsheet ID: {(spreadsheet.get('spreadsheetId'))}")
            return spreadsheet.get("spreadsheetId")
        except HttpError as error:
            print(f"An error occurred: {error}")
            return error
        
    def download_sheet_as_csv(self, spreadsheetId: str, sheet_name: str, save_path: str, filename: str):
     
        url = f'https://docs.google.com/spreadsheets/d/{spreadsheetId}/gviz/tq?tqx=out:csv&sheet={sheet_name}'

        try:
            resp = requests.get(url, headers=self.headers)

            if resp.status_code != 200:
                print(f"Error: Response status {resp.status_code}")
                return None

            os.makedirs(save_path, exist_ok=True)

            full_path = os.path.join(save_path, f"{filename}.csv")

            with open(full_path, "wb") as f:
                f.write(resp.content)

            print(f"CSV saved: {full_path}")
            return full_path

        except HttpError as error:
            print(error)
            return None
