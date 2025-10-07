from selenium import webdriver
from selenium.webdriver.firefox.options import Options
import os
import re
import json
import time

BASE_URL = "https://filezilla-project.org/download.php?platform=linux64"
SAVE_PATH = "/home/yash-gaudani/R%D/patch/Scraping/filezilla"
OUTPUT_FILE = os.path.join(SAVE_PATH, "filezilla_latest.json")

def fetch_with_selenium():
    options = Options()
    options.headless = True
    driver = webdriver.Firefox(options=options)

    try:
        driver.get(BASE_URL)
        time.sleep(5)  # wait for JS to redirect

        cdn_url = driver.current_url
        print(f"✅ Final URL: {cdn_url}")

        file_name = os.path.basename(cdn_url)
        version_match = re.search(r'FileZilla[_-](\d+\.\d+\.\d+)', file_name)
        version = version_match.group(1) if version_match else "unknown"

        return [{
            "product": "filezilla",
            "version": version,
            "file_name": file_name,
            "download_url": cdn_url,
            "platform": "linux64"
        }]

    except Exception as e:
        print(f"❌ Selenium error: {e}")
        return []

    finally:
        driver.quit()

def save_data(data):
    os.makedirs(SAVE_PATH, exist_ok=True)
    with open(OUTPUT_FILE, "w") as f:
        json.dump(data, f, indent=4)
    print(f"✅ Data saved to {OUTPUT_FILE}")

if __name__ == "__main__":
    data = fetch_with_selenium()
    if data:
        save_data(data)
    else:
        print("❌ No data to save.")
