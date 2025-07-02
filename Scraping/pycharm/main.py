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

url = "https://www.jetbrains.com/pycharm/download/other.html"
driver.get(url)
time.sleep(5)
html = driver.page_source
driver.quit()

soup = BeautifulSoup(html, "html.parser")
links = soup.find_all("a", href=True)

# Regex to match PyCharm download links (both editions)
pattern = re.compile(
    r'(https://download.jetbrains.com/python/)(pycharm(?:-community)?)-(\d+\.\d+(?:\.\d+)?)(?:-[\w\d]+)?\.(exe|dmg|tar\.gz|sh|zip|msi|deb|rpm)',
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

        # Detect product name
        product = "PyCharm Community" if "community" in edition_code.lower() else "PyCharm Professional"

        # Determine platform
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

if json_data:
    # Get latest version
    all_versions = [parse_version(entry["version"]) for entry in json_data]
    latest_version = max(all_versions)

    # Filter latest version entries
    latest_entries = [e for e in json_data if parse_version(e["version"]) == latest_version]

    # Save as JSON
    with open("pycharm_latest_all_variants.json", "w") as f:
        json.dump(latest_entries, f, indent=4)

    # Print file names by edition
    print(f"\n✅ Total matched entries: {len(json_data)}")
    print(f"📦 Latest Version: {latest_version}\n")

    print("📁 PyCharm Professional files:")
    for e in latest_entries:
        if e['product'] == "PyCharm Professional":
            print("-", e["file_name"])

    print("\n📁 PyCharm Community files:")
    for e in latest_entries:
        if e['product'] == "PyCharm Community":
            print("-", e["file_name"])
else:
    print("❌ No valid PyCharm download links found.")
