import gspread
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import pandas as pd
from datetime import datetime, date
import os

# --- Configuration ---
SCOPES = ['https://www.googleapis.com/auth/spreadsheets', 'https://www.googleapis.com/auth/drive.file']
GOOGLE_SHEET_URL = 'https://docs.google.com/spreadsheets/d/19c6CZ_LhvVnNalobdBsTYm4pJM9AGt7vPSXpB2fbMBE/edit?usp=sharing'
SHEET_TAB_NAME = 'MoodLog' 
CREDENTIALS_FILE = 'credentials.json'
GOOGLE_SHEET_NAME = 'Mood Tracker' 
TOKEN_FILE = 'token.json' # File to store the access and refresh tokens for efficiency

# --- Mood Options ---
MOOD_OPTIONS = {
    "😊 Happy": "😊",
    "😠 Frustrated": "😠",
    "😕 Confused": "😕",
    "🎉 Joyful": "🎉",
    "🤔 Thinking": "🤔",
    "😟 Worried": "😟"
}

def authenticate_gsheet():
    """Authenticates with Google Sheets using OAuth 2.0. Handles token loading, refresh, and saving."""
    creds = None
    if os.path.exists(TOKEN_FILE):
        creds = Credentials.from_authorized_user_file(TOKEN_FILE, SCOPES)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                CREDENTIALS_FILE, SCOPES)
            creds = flow.run_local_server(port=0) 
        with open(TOKEN_FILE, 'w') as token:
            token.write(creds.to_json())

    client = gspread.authorize(creds)
    return client

def append_to_sheet(client, data_row):
    """Appends a new row to the Google Sheet, opening by URL."""
    spreadsheet = client.open_by_url(GOOGLE_SHEET_URL)
    sheet = spreadsheet.worksheet(SHEET_TAB_NAME)
    sheet.append_row(data_row)
    return True 

def load_data_from_sheet(client):
    """Loads data from the Google Sheet into a pandas DataFrame, opening by URL."""
    spreadsheet = client.open_by_url(GOOGLE_SHEET_URL)
    sheet = spreadsheet.worksheet(SHEET_TAB_NAME)
    records = sheet.get_all_records()
    df = pd.DataFrame(records)

    expected_columns = ['Timestamp', 'Mood', 'Note']
    for col in expected_columns:
        if col not in df.columns:
            df[col] = pd.NA

    if 'Timestamp' in df.columns:
        df['Timestamp'] = pd.to_datetime(df['Timestamp'], errors='coerce')
    return df[expected_columns]