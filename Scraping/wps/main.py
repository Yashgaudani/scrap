import re
import json
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager

# File types you care about
FILE_EXTENSIONS = ["exe", "apk", "deb", "rpm", "pkg", "dmg", "zip", "tar.gz", "msi"]

# Pages to visit — use product-specific paths too
ALL_PAGES = [
    "https://www.wps.com/download/",
   
   
]

# Regex pattern to find all downloadable URLs
pattern = re.compile(
    r"https?://[^\s\"'>]+\.(" + "|".join(FILE_EXTENSIONS) + r")(\?[^\s\"'>]*)?",
    re.IGNORECASE
)

# Setup Chrome headless
options = Options()
options.add_argument("--headless")
options.add_argument("--no-sandbox")
options.binary_location = "/usr/bin/google-chrome"

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

all_urls = set()

# Visit all pages
for url in ALL_PAGES:
    print(f"[+] Scraping: {url}")
    try:
        driver.get(url)
        time.sleep(5)  # Wait for full JS render

        html = driver.page_source
        for match in pattern.finditer(html):
            all_urls.add(match.group(0))
    except Exception as e:
        print(f"Failed to scrape {url}: {e}")

driver.quit()

# Final output
downloads = [{"download_url": url} for url in sorted(all_urls)]

with open("wps_downloads_full.json", "w") as f:
    json.dump(downloads, f, indent=4)

print(json.dumps(downloads, indent=4))
