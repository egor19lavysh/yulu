import gspread
from google.oauth2.service_account import Credentials
from config import settings
import logging


class GoogleSheetsClient:
    def __init__(self, credentials_file, spreadsheet_id):
        self.scope = ["https://www.googleapis.com/auth/spreadsheets"]
        self.creds = Credentials.from_service_account_file(credentials_file, scopes=self.scope)
        self.client = gspread.authorize(self.creds)
        self.sheet = self.client.open_by_key(spreadsheet_id).sheet1

    def user_exists(self, user_id: int) -> bool:
        try:
            cell = self.sheet.find(str(user_id))
            print(cell)
            return cell is None
        except Exception as e:
            return False
    
    def append_user(self, data: dict) -> None:
        print(data.get("user_id", False))
        if user_id := data.get("user_id", False):
            if self.user_exists(user_id=user_id):
                    self.sheet.append_row([
                            data['user_id'],
                            data.get('username', ''),
                            data.get('first_name', ''),
                            data.get('last_name', ''),
                            data['registration_date'],
                        ])
                        
                    logging.info(f"User {data['user_id']} added to Google Sheet")