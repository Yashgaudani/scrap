from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import time
import re
import json
import os

# Setup headless Chrome
options = Options()
options.add_argument("--headless=new")  # Use new headless mode
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")

# Start browser
driver = webdriver.Chrome(options=options)

try:
    # Load Sejda Desktop page
    driver.get("https://www.sejda.com/desktop")
    time.sleep(5)  # Wait for JavaScript to load

    # Get full page HTML after rendering
    page_source = driver.page_source

finally:
    driver.quit()

# Parse with BeautifulSoup
soup = BeautifulSoup(page_source, "html.parser")

# Platform name helper
def get_platform(text):
    text = text.lower()
    if "mac" in text:
        return "macOS"
    elif "windows" in text:
        return "Windows"
    elif "linux" in text:
        return "Linux"
    return "Unknown"

# Collect download info
output = []
for a in soup.select("div.availability a.download-link"):
    text = a.get_text(strip=True)
    href = a.get("href")
    if href and href.startswith("http"):
        file_name = os.path.basename(href)

        # Try version from path
        version_match = re.search(r'/(\d+\.\d+\.\d+)/', href)
        if version_match:
            version = version_match.group(1)
        else:
            # Try version from file name like _7.8.8 or -7.8.8
            version_file = re.search(r'[_-](\d+\.\d+\.\d+)', file_name)
            version = version_file.group(1) if version_file else "unknown"

        output.append({
            "product": "sejda",
            "version": version,
            "text": file_name,
            "url": href,
            "platform": get_platform(text)
        })

# Save JSON file
save_path = "/home/yash-gaudani/R%D/patch/Scraping/sejdapdf/sejda_downloads.json"
os.makedirs(os.path.dirname(save_path), exist_ok=True)

with open(save_path, "w", encoding="utf-8") as f:
    json.dump(output, f, indent=2)

print(f"✅ Download info saved to: {save_path}")
