import requests
from bs4 import BeautifulSoup
import re
import json
from packaging.version import Version

# Base URL and output path
BASE_URL = "https://www.heidisql.com/download.php"
OUTPUT_JSON = "/home/yash-gaudani/R%D/patch/Scraping/HeidiSQL/heidisql_latest.json"
PRODUCT = "heidisql"

# Map of file extensions to OS names
file_os_map = {
    "Windows": [".exe", ".zip", ".msi"],
    "Linux": [".tar.gz", ".gz",".deb"],
    "macOS": [".dmg"]
}

# Flatten all extensions
all_extensions = [ext for exts in file_os_map.values() for ext in exts]
pattern = re.compile(r"([\d]+\.[\d]+\.[\d]+\.[\d]+).*(" + "|".join(re.escape(ext) for ext in all_extensions) + r")$", re.IGNORECASE)

# Send GET request
response = requests.get(BASE_URL)
response.raise_for_status()
soup = BeautifulSoup(response.text, "html.parser")

# Track latest version per OS
latest_by_os = {}

for tag in soup.find_all("a", href=True):
    href = tag["href"]
    match = pattern.search(href)
    if not match:
        continue

    version_str = match.group(1)
    ext = match.group(2).lower()
    file_name = href.split("/")[-1]
    full_url = href if href.startswith("http") else f"{BASE_URL.rstrip('/')}/{href.lstrip('/')}"

    # Identify OS from extension
    os_name = None
    for os_key, extensions in file_os_map.items():
        if any(ext.endswith(e) for e in extensions):
            os_name = os_key
            break

    if os_name:
        try:
            version = Version(version_str)
        except:
            continue

        if os_name not in latest_by_os or version > latest_by_os[os_name]["version_obj"]:
            latest_by_os[os_name] = {
                "product": PRODUCT,
                "version": str(version),
                "text": file_name,
                "url": full_url,
                "platform": os_name,
                "version_obj": version  # use for internal comparison
            }


# Remove 'version_obj' before saving
for os_key in latest_by_os:
    del latest_by_os[os_key]["version_obj"]

# Save as JSON
with open(OUTPUT_JSON, "w") as f:
    json.dump(list(latest_by_os.values()), f, indent=2)

print(f"✅ JSON saved to {OUTPUT_JSON}")
