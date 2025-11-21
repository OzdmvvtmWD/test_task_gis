import requests
from googleapiclient.errors import HttpError

class ReadMixin():
    
    def get_spread_sheet_info(self, spreadsheetId):
        
        api_url = f'https://sheets.googleapis.com/v4/spreadsheets/{spreadsheetId}'

        try:
            resp = requests.get(url = api_url,  headers= self.headers)
            status_code = resp.status_code

            print(status_code)
            return resp.json()
            
        except HttpError as error:
            print(error)
            return error
        
    def get_all_sheets(self, spreadsheetId):
        res = []
        try:
            spread_sheet = self.get_spread_sheet_info(spreadsheetId)
            sheets = spread_sheet.get('sheets')

            for sheet in sheets:
                properties = sheet.get('properties')
                res.append(properties)

            return res
               
        except Exception as error:
            print(error)
            return []
      
    def get_sheet_info_by_name(self, spreadsheetId, name):
        try:
            sheets = self.get_all_sheets(spreadsheetId)
            for properties in sheets:
                if properties.get('title') == name:     
                    return properties

        except Exception as error:
            print(error)
            return None
        
        return None
    
    def is_sheet_exist(self, spreadsheetId, name):
        return self.get_sheet_info_by_name(spreadsheetId, name) is not None
    
    def read_range(self, spreadsheet_id, range_names, sheet_name):
        range_names = f"{sheet_name}!{range_names}"

        try:
            result = (
                self.service.spreadsheets()
                .values()
                .get(spreadsheetId=spreadsheet_id, range=range_names)
                .execute()
            )
            rows = result.get("values", [])
            print(f"{len(rows)} rows retrieved")
            return result
        
        except HttpError as error:
            print(f"An error occurred: {error}")
            return error


    def read_row(self, spreadsheet_id, row, sheet_name):
        return self.read_range(spreadsheet_id, f"A{row}:O{row}", sheet_name)
    
    def read_col(self, spreadsheet_id, col, sheet_name):
        return self.read_range(spreadsheet_id, f"{col}:{col}", sheet_name)
