import re
import json
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import time
from packaging.version import parse as parse_version

# Setup headless browser
options = Options()
options.add_argument("--headless=new")
driver = webdriver.Chrome(options=options)

url = "https://www.jetbrains.com/idea/download/other.html"
driver.get(url)
time.sleep(5)
html = driver.page_source
driver.quit()

soup = BeautifulSoup(html, "html.parser")
links = soup.find_all("a", href=True)

# Regex to match IntelliJ download URLs
pattern = re.compile(
    r'(https://.*?/)(ideaI[CU])-([\d.]+)[^/]*\.(exe|dmg|tar\.gz|sh|zip|msi|deb|rpm)',
    re.IGNORECASE
)

json_data = []

for link in links:
    href = link['href']
    match = pattern.search(href)
    if match:
        base_url, edition_code, version, ext = match.groups()
        version = version.rstrip(".")
        file_name = href.split("/")[-1]
        download_url = href if href.startswith("http") else "https://www.jetbrains.com" + href

        edition = edition_code.strip("-").lower()
        product = "IntelliJ IDEA Ultimate" if edition == "ideaiu" else "IntelliJ IDEA Community Edition"

        if ext == "exe":
            platform = "Windows"
        elif ext == "dmg":
            platform = "macOS"
        elif ext in ["tar.gz", "sh", "deb", "rpm"]:
            platform = "Linux"
        elif ext == "zip":
            platform = "Windows (Zip)"
        else:
            platform = "Other"

        json_data.append({
            "product": product,
            "file_name": file_name,
            "version": version,
            "download_url": download_url,
            "platform": platform
        })

# Step 1: Get the latest version number
all_versions = [parse_version(entry["version"]) for entry in json_data]
latest_version = max(all_versions)

# Step 2: Filter all entries that match the latest version
latest_entries = [entry for entry in json_data if parse_version(entry["version"]) == latest_version]



with open("intellij_latest_all_variants.json", "w") as f:
    json.dump(latest_entries, f, indent=4)

# Print the results
print(f"\n✅ Found total: {len(json_data)} entries.")

