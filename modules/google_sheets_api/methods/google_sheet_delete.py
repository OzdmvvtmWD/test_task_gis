import requests
from googleapiclient.errors import HttpError
 

class DeleteMixin:

    def delete_sheet(self, spreadsheetId:str, spreadsheet_id):
        api_url = f'https://sheets.googleapis.com/v4/spreadsheets/{spreadsheetId}:batchUpdate'
        body = {         
                "requests": [
                    {
                    "deleteSheet": {
                        "sheetId": spreadsheet_id
                    }
                    }
                ]   
            }
        try:
            resp = requests.post(url = api_url, json=body, headers= self.headers)
            status_code = resp.status_code

            print(status_code)
            return resp.json()
            
        except HttpError as error:
            print(error)
            return error
        


