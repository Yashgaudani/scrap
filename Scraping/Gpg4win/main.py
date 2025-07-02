import requests
from bs4 import BeautifulSoup
import re
import json
from packaging.version import Version, InvalidVersion

# Constants
BASE_URL = "https://files.gpg4win.org"
OUTPUT_PATH = "/home/yash-gaudani/R%D/patch/Scraping/Gpg4win/gpg4win_latest.json"
PRODUCT_NAME = "gpg4win"
PLATFORM = "Windows"

# Allowed file extensions
file_extensions = [".exe", ".msi", ".zip"]
pattern = re.compile(r"gpg4win[-_]?(\d+\.\d+\.\d+)(?![a-zA-Z])[\w.-]*(" + "|".join(re.escape(ext) for ext in file_extensions) + r")")

# Fetch page
response = requests.get(BASE_URL)
response.raise_for_status()
soup = BeautifulSoup(response.text, "html.parser")

# Collect valid stable files
stable_files = []

for tag in soup.find_all("a", href=True):
    href = tag["href"]

    # Skip beta/pre-release candidates
    if any(x in href.lower() for x in ["beta", "rc", "alpha"]):
        continue

    match = pattern.search(href)
    if match:
        try:
            version = Version(match.group(1))
            if version.is_prerelease:
                continue  # Also skip semantically marked pre-releases
            full_url = href if href.startswith("http") else f"{BASE_URL}/{href.lstrip('/')}"
            stable_files.append({
                "version": version,
                "text": href.split("/")[-1],
                "url": full_url
            })
        except InvalidVersion:
            continue

# Find latest stable version
if stable_files:
    latest = max(stable_files, key=lambda x: x["version"])
    output = {
        "product": PRODUCT_NAME,
        "version": str(latest["version"]),
        "text": latest["text"],
        "url": latest["url"],
        "platform": PLATFORM
    }

    # Save to JSON
    with open(OUTPUT_PATH, "w") as f:
        json.dump(output, f, indent=2)
    print(f"✅ JSON saved at: {OUTPUT_PATH}")
else:
    print("❌ No stable version files found.")
