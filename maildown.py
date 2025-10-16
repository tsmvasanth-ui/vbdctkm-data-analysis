import imaplib, email, os

IMAP_HOST = "imap.gmail.com"
USERNAME = "tsmvasanth@gmail.com"
PASSWORD = "mcua ovof ecjl haqs"  # 16-character App Password

MAILBOX = "INBOX"
SENDER = "dfrsda@gmail.com"
SINCE = "01-Jul-2025"   # DD-Mon-YYYY
BEFORE = "31-Jul-2025"  # DD-Mon-YYYY
OUT_DIR = r"C:\Vasanth\Fever\July"

os.makedirs(OUT_DIR, exist_ok=True)

# Connect and login
mail = imaplib.IMAP4_SSL(IMAP_HOST)
mail.login(USERNAME, PASSWORD)
mail.select(MAILBOX)

# Search emails
criteria = ['FROM', SENDER, 'SINCE', SINCE, 'BEFORE', BEFORE]
result, data = mail.search(None, *criteria)

if result != "OK":
    raise SystemExit("Search failed")

msg_ids = data[0].split()
print(f"Found {len(msg_ids)} messages.")

# Download Excel attachments only
for i, msg_id in enumerate(msg_ids, start=1):
    res, msg_data = mail.fetch(msg_id, "(RFC822)")
    raw = msg_data[0][1]
    msg = email.message_from_bytes(raw)

    for part in msg.walk():
        if part.get_content_maintype() == 'multipart':
            continue
        if part.get('Content-Disposition') is None:
            continue

        filename = part.get_filename()
        if filename and (filename.lower().endswith(".xls") or filename.lower().endswith(".xlsx")):
            # Clean filename
            safe_name = "".join(c for c in filename if c.isalnum() or c in "._- ")[:100]
            filepath = os.path.join(OUT_DIR, safe_name)

            # Save attachment
            with open(filepath, "wb") as f:
                f.write(part.get_payload(decode=True))
            print(f"Saved Excel: {safe_name}")

mail.logout()
print(f"✅ All Excel attachments saved to {OUT_DIR}")