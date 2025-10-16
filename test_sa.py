import gspread
from google.oauth2.service_account import Credentials

# ---- Step 1: Service account JSON ----
SERVICE_ACCOUNT_FILE = "vbdctkm-2c5de101d3c0.JSON"

# ---- Step 2: Set proper scopes ----
SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]

# ---- Step 3: Authenticate ----
creds = Credentials.from_service_account_file(
    SERVICE_ACCOUNT_FILE,
    scopes=SCOPES
)
gc = gspread.authorize(creds)

# ---- Step 4: Spreadsheet ID ----
# Replace this with your spreadsheet's actual ID from the URL
SPREADSHEET_ID = "1efD5IUpzCSGAU1zmSi6uqIzqXNGCyyJyKPLQBIyOulw"

try:
    # Open the first sheet
    sheet = gc.open_by_key(SPREADSHEET_ID).sheet1

    # Get all records and print first 5 rows
    data = sheet.get_all_records()
    print("✅ Service account connected successfully! First 5 rows:")
    for row in data[:5]:
        print(row)

except gspread.exceptions.APIError as e:
    print("❌ API Error (likely sheet not shared or wrong scopes):", e)

except Exception as e:
    print("❌ Other Error:", e)
