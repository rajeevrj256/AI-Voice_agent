import gspread
import json
import time
from oauth2client.service_account import ServiceAccountCredentials
from notifcation import send_appointment_notification
# Google Sheets Setup
SHEET_ID = "1yIMGvFs5vAH7aqvyCpvEAIzmbom8ykygtNcj3xLvrHk"
SHEET_NAME = "Sheet1"

# Authenticate with Google Sheets
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
credentials = ServiceAccountCredentials.from_json_keyfile_name("credentials.json", scope)
client = gspread.authorize(credentials)
sheet = client.open_by_key(SHEET_ID).worksheet(SHEET_NAME)

EXPECTED_COLUMNS = [
    "Call ID", "Assistant ID", "Phone Number ID", "Type", "Started At",
    "Ended At", "Recording URL", "Summary", "Created At", "Updated At",
    "Cost", "Status", "Ended Reason", "Messages"
]

def ensure_columns_exist():
    """Ensure the first row contains the expected column headers."""
    try:
        existing_headers = sheet.row_values(1)  # Get first row (headers)
        if existing_headers != EXPECTED_COLUMNS:
            sheet.insert_row(EXPECTED_COLUMNS, index=1)
            print("Column headers updated.")
        else:
            print("Column headers already present.")
    except Exception as e:
        print("Error ensuring column headers:", e)

def is_duplicate(call_id):
    """Check if a call ID already exists in the sheet."""
    try:
        existing_records = sheet.col_values(1)  # Fetch all call IDs from the first column
        return call_id in existing_records
    except Exception as e:
        print("Error checking for duplicates:", e)
        return False

def log_call_to_sheets(call_data,LLM_response):
    """Logs Vapi call data to Google Sheets with duplicate check."""
    call_id = call_data.get("id", "N/A")
    print(call_id)
    
    ensure_columns_exist()
    
    # Check if this call ID already exists
    if is_duplicate(call_id):
        print(f"Duplicate detected: Call ID {call_id} already logged.")
        return

    messages_str = json.dumps(call_data.get("messages", "N/A"))  # Convert messages to a string
    
    log_entry = [
        call_id,
        call_data.get("assistantId", "N/A"),
        call_data.get("phoneNumberId", "N/A"),
        call_data.get("type", "N/A"),
        call_data.get("startedAt", "N/A"),
        call_data.get("endedAt", "N/A"),
        call_data.get("recordingUrl", "N/A"),
        call_data.get("summary", "N/A"),
        call_data.get("createdAt", "N/A"),
        call_data.get("updatedAt", "N/A"),
        call_data.get("cost", "N/A"),
        call_data.get("status", "N/A"),
        call_data.get("endedReason", "N/A"),
        messages_str
    ]
    
    try:
        sheet.append_row(log_entry)
        print(f"Call data logged successfully: {call_id}")
        recipient_email = LLM_response.get("email", "N/A")
        if recipient_email and recipient_email != "N/A":
            send_appointment_notification(LLM_response, recipient_email)
        else:
            print(f"Warning: Skipping email notification, invalid email: {recipient_email}")

    except Exception as e:
        print("Error logging call data:", e)
        time.sleep(1)  
