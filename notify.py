import json
import requests
import datetime

# ===============================
WEBEX_TOKEN = "NzBkMGFkMmUtZjBlMS00YTIwLWI1NmItZDI2OWFlYWJlOTE4MmVhOWRmYzktOTNi_P0A1_bac71010-7484-48b3-b7ce-a267353178c5"
ROOM_ID = "Y2lzY29zcGFyazovL3VybjpURUFNOnVzLXdlc3QtMl9yL1JPT00vMmYzOGZhOTAtYTdjMy0xMWYwLTg0MGQtOWZlZmM4MmJmYWE4"
SHEET_URL = "YOUR_APPS_SCRIPT_WEB_APP_URL"
# ===============================

def read_results():
    """Read pytest JSON results from results.json."""
    try:
        with open("results.json") as f:
            data = json.load(f)

        summary = data.get("summary", {})
        passed = summary.get("passed", 0)
        failed = summary.get("failed", 0)
        status = "SUCCESS" if failed == 0 else "FAILED"
        return status, passed, failed
    except Exception:
        # If something went wrong, still notify/log
        return "UNKNOWN", 0, 0

def send_webex(status, passed, failed):
    """Send a message to Webex space via bot."""
    text = (
        f"Build status: {status}\n"
        f"Tests passed: {passed}\n"
        f"Tests failed: {failed}"
    )

    headers = {
        "Authorization": f"Bearer {WEBEX_TOKEN}"
    }

    requests.post(
        "https://webexapis.com/v1/messages",
        headers=headers,
        json={"roomId": ROOM_ID, "text": text},
        timeout=10,
    )

def log_to_sheet(status, passed, failed):
    """Log build result into Google Sheet via Apps Script webhook."""
    payload = {
        "status": status,
        "passed": passed,
        "failed": failed,
        "timestamp": datetime.datetime.utcnow().isoformat()
    }

    requests.post(
        SHEET_URL,
        json=payload,
        timeout=10,
    )

if __name__ == "__main__":
    status, passed, failed = read_results()
    send_webex(status, passed, failed)
    log_to_sheet(status, passed, failed)
