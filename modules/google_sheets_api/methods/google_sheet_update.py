import requests
from googleapiclient.errors import HttpError

class UpdateMixin:

    def _batch_update(self, spreadsheetId:str, body):
        api_url = f"https://sheets.googleapis.com/v4/spreadsheets/{spreadsheetId}:batchUpdate"

        body = {"requests" :[body]}
        
        try:
            resp = requests.post(url = api_url, json= body, headers= self.headers)
            status_code = resp.status_code
            print(status_code)

            return resp.json()
            
        except HttpError as error:
            print(error)
            return error



    def rename_spread_sheet(self, spreadsheetId:str, sheet_name:str):
        body = {
            "updateSpreadsheetProperties": {
                "properties": {"title": sheet_name},
                "fields": "title"
            }
        }

        return self._batch_update(spreadsheetId, body)
        
        
    def rename_sheet(self, spreadsheetId:str, sheet_name:str, sheetId:int = 0):
        body = {
            "updateSheetProperties": {
                "properties": {
                    "title": sheet_name,
                    "sheetId": sheetId,
                    },
                "fields": "title"
            }
        }

        return self._batch_update(spreadsheetId, body)
    
    def update_rows(self, spreadsheetId: str, rows, sheetId: int = 0):

        gs_rows = []
        for row in rows:
            gs_row = {
                "values": [
                    {"userEnteredValue": {"stringValue": str(cell)}}
                    for cell in row
                ]
            }
            gs_rows.append(gs_row)

        body = {
            "appendCells": {
                "sheetId": sheetId,
                "rows": gs_rows,
                "fields": "*"
            }
        }

        return self._batch_update(spreadsheetId, body)
    
    def clear_range(self, spreadsheetId: str, sheet_name:str , range:str):
        api_url = f'https://sheets.googleapis.com/v4/spreadsheets/{spreadsheetId}/values/{sheet_name}!{range}:clear'

        body = {}

        try:
            resp = requests.post(url = api_url, json= body, headers= self.headers)
            status_code = resp.status_code
            print(status_code)

            return resp.json()
            
        except HttpError as error:
            print(error)
            return error


    
    