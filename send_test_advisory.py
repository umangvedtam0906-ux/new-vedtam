#!/usr/bin/env python3
import os
from datetime import datetime
import update_cert_data

def main():
    print("Loading environment configurations...")
    update_cert_data.load_env()

    smtp_host = os.environ.get("SMTP_HOST", "")
    smtp_user = os.environ.get("SMTP_USER", "")
    
    if not smtp_host or not smtp_user:
        print("\n[Error] SMTP settings (SMTP_HOST, SMTP_USER, etc.) are missing from the local .env file.")
        print("Please create a '.env' file in this directory with the following variables:")
        print("SMTP_HOST=your_smtp_host")
        print("SMTP_PORT=587")
        print("SMTP_USER=your_email")
        print("SMTP_PASSWORD=your_password")
        print("SMTP_SECURE=tls")
        print("\nAlternatively, run this script on your live server where the .env is configured.")
        return

    print("Constructing test advisory...")
    mock_advisories = [
        {
            "title": "TEST ALERT: Subscriber Update Verification",
            "severity": "critical",
            "date": datetime.now().strftime("%Y-%m-%d"),
            "code": "TEST-2026-0001"
        }
    ]

    print("Attempting to send the test email...")
    try:
        update_cert_data.email_subscribers(mock_advisories)
        print("Execution finished. Check logs above for success or connection errors.")
    except Exception as e:
        print(f"[Error] Failed to run email sending: {e}")

if __name__ == "__main__":
    main()
