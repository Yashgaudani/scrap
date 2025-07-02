import time
import json
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup

# Setup headless Chrome
options = Options()
options.add_argument("--headless=new")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")

driver = webdriver.Chrome(options=options)
url = "https://learn.microsoft.com/en-us/ssms/release-notes-21"
driver.get(url)
time.sleep(5)

html = driver.page_source
driver.quit()

soup = BeautifulSoup(html, "html.parser")

exe_links = set()

# Extract all .exe links
for link in soup.find_all("a", href=True):
    href = link["href"]
    if href.endswith(".exe"):
        full_url = href if href.startswith("http") else "https://learn.microsoft.com" + href
        exe_links.add(full_url)

# Extract version from the URL (last number in the path)
version = url.rstrip("/").split("-")[-1]

# Create JSON output
data = []
for url in exe_links:
    file_name = url.split("/")[-1]
    data.append({
        "product": "SQL Server Management Studio",
        "version": version,
        "text": file_name,
        "url": url,
        "platform": "Windows"
    })

# Save to file
with open("ssms_download_links.json", "w") as f:
    json.dump(data, f, indent=4)

# Print results
print(f"✅ Found {len(data)} unique .exe download links with version {version}:")
for item in data:
    print("-", item["url"])
