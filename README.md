# Mood of the Queue Logger 📊

The Mood of the Queue Logger is a straightforward Streamlit application designed to help you track and visualize the mood of your support ticket queue. It uses Google Sheets for data storage, making it easy to share and access your mood logs.

## How It Works

This tool simplifies mood tracking into three core steps:

1.  **Log a Mood**: You can select a mood (e.g., happy 😊 or angry 😠) and add an optional note to provide context.
2.  **Store Data**: Each submission—including the timestamp, mood, and note—is automatically appended to a designated Google Sheet.
3.  **Visualize Moods**: The application generates a bar chart that displays a real-time count of moods logged for the current day.

-----

## Setup Instructions

Follow these steps to get the Mood of the Queue Logger up and running on your local machine.

### 1\. Get the Code

First, you'll need to get the application's code. If you're using Git, you can clone the repository. Remember to replace `<your-repo-url>` with the actual URL of the repository:

```bash
git clone <your-repo-url>
cd name-of-the-project-folder
```

### 2\. Create Your `credentials.json` File

**This is a crucial security step.** The `credentials.json` file is necessary for the application to connect to Google Sheets. This file is **not** included in the GitHub repository for security reasons, so you **must** create or obtain your own.

Once you have your `credentials.json` file, place it in the same directory as `app.py` and `gsheet_utils.py`.

### 3\. Prepare Your Google Sheet

Next, you'll need to set up your Google Sheet:

  * **Create or Use an Existing Sheet**: Open Google Sheets and either create a new spreadsheet or select an existing one.
  * **Get the URL**: Copy the full URL of your Google Sheet from your browser's address bar (e.g., `https://docs.google.com/spreadsheets/d/your_sheet_id_here/edit#gid=0`).
  * **Set up the Tab**: Name one of the tabs (worksheets) in your Google Sheet (e.g., `MoodLog`). This name needs to match the `SHEET_TAB_NAME` in the script.

### 4\. Update Configuration in `gsheet_utils.py`

Open the `gsheet_utils.py` file in your project folder and update the following lines with your specific Google Sheet information:

```python
# Replace with YOUR actual Google Sheet URL
GOOGLE_SHEET_URL = 'YOUR_GOOGLE_SHEET_URL_HERE'
# Make sure this matches the tab name in your Google Sheet
SHEET_TAB_NAME = 'MoodLog'
```

### 5\. Install Required Python Libraries

You'll need to install the necessary Python libraries for the application to function. Run the following command in your terminal:

```bash
pip install streamlit gspread google-auth google-auth-oauthlib google-auth-httplib2 pandas matplotlib
```

### 6\. Run the Streamlit App

Once all the setup is complete, you can run the Streamlit application:

```bash
streamlit run app.py
```

#### First-Time Run:

When you run the app for the first time, your web browser will automatically open and prompt you to sign in with your Google account.

  * Sign in with the Google account that has access to the Google Sheet you configured.
  * Grant the requested permissions.

After successful authentication, a `token.json` file will be created in your project directory. This file securely stores your authorization, so you won't need to log in every time.

#### Subsequent Runs:

For future runs, the app should load directly without requiring browser authentication, as it will use the saved `token.json` file.

-----

## File Structure

After completing the setup, your project folder should resemble this structure:

```
your-project-folder/
├── app.py                 # Main Streamlit application
├── gsheet_utils.py        # Utilities for Google Sheets
├── credentials.json       # Your private Google API credentials (YOU ADD THIS)
├── token.json             # Generated after first successful login (DO NOT COMMIT)
├── requirements.txt       # Python dependencies
└── README.md              # This file
```
