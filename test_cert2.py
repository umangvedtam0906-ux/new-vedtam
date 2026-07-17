import urllib.request
import urllib.error
import traceback

HOME_URL = "https://www.cert-in.org.in/"
url = "https://www.cert-in.org.in/s2cMainServlet?pageid=PUBWEL01"

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Referer": HOME_URL
}

req = urllib.request.Request(url, headers=headers)
with open("python_test_log.txt", "w") as f:
    try:
        with urllib.request.urlopen(req, timeout=20) as response:
            content_bytes = response.read()
            f.write(f"Success! Fetched {len(content_bytes)} bytes.\n")
    except urllib.error.HTTPError as e:
        f.write(f"HTTP Error: {e.code} {e.reason}\n")
        f.write(e.read().decode('utf-8', errors='ignore'))
    except Exception as e:
        f.write(f"Error: {type(e).__name__} - {str(e)}\n")
        f.write(traceback.format_exc())
