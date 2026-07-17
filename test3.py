with open(r"c:\Users\Manu\Downloads\new-vedtam\new-vedtam\python_debug_log.txt", "w", encoding="utf-8") as f:
    f.write("Starting test3.py\n")

try:
    import update_cert_data
    from selenium.webdriver.chrome.options import Options
    import undetected_chromedriver as webdriver
    import sys

    with open(r"c:\Users\Manu\Downloads\new-vedtam\new-vedtam\python_debug_log.txt", "a", encoding="utf-8") as f:
        try:
            chrome_options = Options()
            chrome_options.add_argument("--disable-gpu")
            chrome_options.add_argument("--no-sandbox")
            chrome_options.add_argument("--disable-dev-shm-usage")
            chrome_options.add_argument("--window-size=1920,1080")
            
            update_cert_data.driver = webdriver.Chrome(options=chrome_options)
            
            f.write("Driver initialized. Fetching URLs...\n")
            f.flush()
            
            urls = update_cert_data.collect_advisory_urls()
            
            f.write(f"Collected {len(urls)} URLs.\n")
            for u in urls[:5]:
                f.write(f"- {u}\n")
        except Exception as e:
            f.write(f"ERROR: {e}\n")
        finally:
            if update_cert_data.driver:
                update_cert_data.driver.quit()
except Exception as main_e:
    with open(r"c:\Users\Manu\Downloads\new-vedtam\new-vedtam\python_debug_log.txt", "a", encoding="utf-8") as f:
        f.write(f"MAIN ERROR: {main_e}\n")
