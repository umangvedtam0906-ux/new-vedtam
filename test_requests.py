
import requests

session = requests.Session()
session.headers.update({
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.5",
    "Connection": "keep-alive",
})

print("Fetching homepage for cookies...")
try:
    r1 = session.get("https://www.cert-in.org.in", timeout=20)
    print("Homepage status:", r1.status_code)
    print("Cookies:", session.cookies.get_dict())
    
    print("\nFetching advisories...")
    r2 = session.get("https://www.cert-in.org.in/s2cMainServlet?pageid=PUBADVLIST02&year=2026", timeout=20)
    print("Advisories status:", r2.status_code)
    
    if "The requested URL is not found" in r2.text:
        print("WAF Blocked (Fake Not Found)")
    elif "CIVN" in r2.text or "CIAD" in r2.text:
        print("SUCCESS! Found advisories.")
        print(f"Content length: {len(r2.text)}")
    else:
        print("Unknown content...")
        print(r2.text[:500])

except Exception as e:
    print(f"Error: {e}")
