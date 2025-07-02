import json
import re
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup

# Setup headless Selenium
options = Options()
options.add_argument("--headless=new")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")
driver = webdriver.Chrome(options=options)

# Load Android Studio download page
url = "https://developer.android.com/studio"
driver.get(url)
time.sleep(5)
html = driver.page_source
driver.quit()

soup = BeautifulSoup(html, "html.parser")
links = soup.find_all("a", href=True)

# File types and platforms
file_exts = {
    ".exe": "Windows",
    ".dmg": "macOS",
    ".deb": "Linux (DEB)",
    ".rpm": "Linux (RPM)",
    ".tar.gz": "Linux (TAR.GZ)",
    ".sh": "Linux"
}

results = []

# Regex pattern for version: e.g. 2025.1.1.13 or 2024.1.1.21
version_pattern = re.compile(r"\b(\d{4}\.\d+\.\d+(?:\.\d+)?)\b")

for link in links:
    href = link["href"]
    for ext, platform in file_exts.items():
        if href.endswith(ext):
            full_url = href if href.startswith("http") else f"https://developer.android.com{href}"
            file_name = full_url.split("/")[-1]
            version_match = version_pattern.search(full_url)
            version = version_match.group(1) if version_match else ""

            results.append({
                "product": "android studio",
                "version": version,
                "text": file_name,
                "url": full_url,
                "platform": platform
            })

# Save to JSON
with open("android_studio_links.json", "w") as f:
    json.dump(results, f, indent=4)

# Output
print(f"✅ Found {len(results)} installer files:")
for item in results:
    print(f"- {item['text']} ({item['platform']}) → version: {item['version']}")
