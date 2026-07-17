#!/usr/bin/env python3
import os
import smtplib
from datetime import datetime

# Mimic the load_env function from update_cert_data.py
def load_env():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    env_path = os.path.join(script_dir, ".env")
    if os.path.exists(env_path):
        try:
            with open(env_path, "r", encoding="utf-8") as f:
                for line in f:
                    line = line.strip()
                    if not line or line.startswith("#"):
                        continue
                    if "=" in line:
                        key, val = line.split("=", 1)
                        key = key.strip()
                        val = val.strip().strip('"').strip("'")
                        os.environ[key] = val
            print("[test] .env file loaded successfully.")
        except Exception as e:
            print(f"[test] Error loading .env file: {e}")
    else:
        print("[test] .env file not found.")

def main():
    load_env()
    
    smtp_host = os.environ.get("SMTP_HOST", "")
    smtp_port_str = os.environ.get("SMTP_PORT", "587")
    smtp_user = os.environ.get("SMTP_USER", "")
    smtp_password = os.environ.get("SMTP_PASSWORD", "")
    smtp_secure = os.environ.get("SMTP_SECURE", "tls").lower()
    
    print("\n--- Configurations ---")
    print(f"SMTP Host: {smtp_host}")
    print(f"SMTP Port: {smtp_port_str}")
    print(f"SMTP User: {smtp_user}")
    print(f"SMTP Password Length: {len(smtp_password) if smtp_password else 0}")
    print(f"SMTP Secure: {smtp_secure}")
    
    if not smtp_host or not smtp_user or not smtp_password:
        print("\n❌ Error: SMTP configuration is incomplete in .env.")
        return
        
    try:
        smtp_port = int(smtp_port_str)
    except ValueError:
        smtp_port = 587
        
    print("\nConnecting to SMTP server...")
    try:
        if smtp_secure == "ssl":
            print(f"Connecting via SMTP_SSL to {smtp_host}:{smtp_port}...")
            server = smtplib.SMTP_SSL(smtp_host, smtp_port, timeout=15)
        else:
            print(f"Connecting via SMTP to {smtp_host}:{smtp_port}...")
            server = smtplib.SMTP(smtp_host, smtp_port, timeout=15)
            if smtp_secure == "tls":
                print("Starting TLS encryption...")
                server.starttls()
                
        print("Attempting to login...")
        server.login(smtp_user, smtp_password)
        print("✅ Success! SMTP Connection & Authentication succeeded.")
        server.quit()
    except Exception as e:
        print(f"❌ Failed to connect/authenticate with SMTP server: {e}")

if __name__ == "__main__":
    main()
