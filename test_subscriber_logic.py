#!/usr/bin/env python3
import os
import unittest
import email
from email.header import decode_header
from unittest.mock import patch, MagicMock

# Import the module to test
import update_cert_data

class TestSubscriptionAutomation(unittest.TestCase):
    def setUp(self):
        # Create a mock subscribers.csv file
        self.csv_path = "mock_subscribers_test.csv"
        with open(self.csv_path, "w", encoding="utf-8") as f:
            f.write("name,phone,organisation,email,status,subscribed_at\n")
            f.write("John Doe,1234567890,TestOrg,john.doe@example.com,confirmed,2026-07-17 12:00:00\n")
            f.write("Jane Doe,9876543210,TestOrg,jane.doe@example.com,pending,2026-07-17 12:00:00\n")

    def tearDown(self):
        # Clean up the mock CSV
        if os.path.exists(self.csv_path):
            os.remove(self.csv_path)

    @patch("update_cert_data.smtplib.SMTP")
    @patch("update_cert_data.os.environ")
    def test_email_subscribers_tls(self, mock_environ, mock_smtp):
        # Set up mock environment variables
        env_vars = {
            "SMTP_HOST": "smtp.testserver.com",
            "SMTP_PORT": "587",
            "SMTP_USER": "alert@testserver.com",
            "SMTP_PASSWORD": "securepassword",
            "SMTP_SECURE": "tls",
            "FROM_EMAIL": "certin-advisories@vedtam.io",
            "FROM_NAME": "Vedtam Test Alerts",
            "SUBSCRIBERS_CSV": self.csv_path,
            "SITE_URL": "https://vedtam.com",
            "SITE_NAME": "Vedtam Tech Solutions"
        }
        mock_environ.get.side_effect = lambda key, default="": env_vars.get(key, default)

        # Set up mock SMTP server instance
        mock_server_instance = MagicMock()
        mock_smtp.return_value = mock_server_instance

        # Test advisories
        mock_advisories = [
            {
                "title": "Multiple Vulnerabilities in Cisco Products",
                "severity": "high",
                "date": "2026-07-17",
                "code": "CIAD-2026-0099"
            }
        ]

        # Call the function under test
        update_cert_data.email_subscribers(mock_advisories)

        # Assert SMTP constructor was called with host and port
        mock_smtp.assert_called_once_with("smtp.testserver.com", 587, timeout=15)

        # Assert TLS was started
        mock_server_instance.starttls.assert_called_once()

        # Assert login was called
        mock_server_instance.login.assert_called_once_with("alert@testserver.com", "securepassword")

        # Assert mail was sent to the CONFIRMED subscriber only
        mock_server_instance.sendmail.assert_called_once()
        args, kwargs = mock_server_instance.sendmail.call_args
        
        # Verify sender and recipient
        self.assertEqual(args[0], "certin-advisories@vedtam.io")
        self.assertEqual(args[1], ["john.doe@example.com"])
        
        # Verify subject and content
        msg_body = args[2]
        msg = email.message_from_string(msg_body)
        
        # Decode the subject header
        subject_header = msg['Subject']
        decoded_parts = decode_header(subject_header)
        subject = "".join(
            part.decode(encoding or 'utf-8') if isinstance(part, bytes) else part
            for part, encoding in decoded_parts
        )
        
        self.assertEqual(subject, "CERT-In Alert: 1 New Security Advisory — Vedtam")
        
        # Extract payloads
        payloads = []
        for part in msg.walk():
            if part.get_content_maintype() == 'text':
                payloads.append(part.get_payload(decode=True).decode('utf-8'))
                
        # Check content in the decoded payloads
        full_content = "".join(payloads)
        self.assertIn("John Doe", full_content)
        self.assertIn("Multiple Vulnerabilities in Cisco Products", full_content)

        # Assert server connection was closed
        mock_server_instance.quit.assert_called_once()
        print("[test] TLS Email automation test passed successfully!")

    @patch("update_cert_data.smtplib.SMTP_SSL")
    @patch("update_cert_data.os.environ")
    def test_email_subscribers_ssl(self, mock_environ, mock_smtp_ssl):
        # Set up mock environment variables for SSL port 465
        env_vars = {
            "SMTP_HOST": "smtp.testserver.com",
            "SMTP_PORT": "465",
            "SMTP_USER": "alert@testserver.com",
            "SMTP_PASSWORD": "securepassword",
            "SMTP_SECURE": "ssl",
            "FROM_EMAIL": "certin-advisories@vedtam.io",
            "FROM_NAME": "Vedtam Test Alerts",
            "SUBSCRIBERS_CSV": self.csv_path,
            "SITE_URL": "https://vedtam.com",
            "SITE_NAME": "Vedtam Tech Solutions"
        }
        mock_environ.get.side_effect = lambda key, default="": env_vars.get(key, default)

        mock_server_instance = MagicMock()
        mock_smtp_ssl.return_value = mock_server_instance

        mock_advisories = [
            {
                "title": "Multiple Vulnerabilities in Cisco Products",
                "severity": "high",
                "date": "2026-07-17",
                "code": "CIAD-2026-0099"
            }
        ]

        # Call the function
        update_cert_data.email_subscribers(mock_advisories)

        # Assert SMTP_SSL was used
        mock_smtp_ssl.assert_called_once_with("smtp.testserver.com", 465, timeout=15)
        mock_server_instance.login.assert_called_once_with("alert@testserver.com", "securepassword")
        mock_server_instance.sendmail.assert_called_once()
        mock_server_instance.quit.assert_called_once()
        print("[test] SSL Email automation test passed successfully!")

if __name__ == "__main__":
    unittest.main()
