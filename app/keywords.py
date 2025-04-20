import os
import gspread
from oauth2client.service_account import ServiceAccountCredentials

def get_opening_keywords():
    scope = ['https://spreadsheets.google.com/feeds',
             'https://www.googleapis.com/auth/drive']
    
    creds_path = os.path.join(os.path.dirname(__file__), '..', 'gspread-creds.json')
    creds_path = os.path.abspath(creds_path)
    
    creds = ServiceAccountCredentials.from_json_keyfile_name(creds_path, scope)
    client = gspread.authorize(creds)

    sheet = client.open("use_case").sheet1
    data = sheet.col_values(1)  # First column
    return [keyword.strip().lower() for keyword in data if keyword.strip()]


#print(get_opening_keywords())
