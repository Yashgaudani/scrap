import requests
from bs4 import BeautifulSoup
import re
import json
import os

# Config
base_url = "https://www.postgresql.org/ftp/source/"
headers = {"User-Agent": "Mozilla/5.0"}
save_path = "/home/yash-gaudani/R%D/patch/Scraping/postgressql"
output_file = os.path.join(save_path, "postgresql_latest.json")

# Step 1: Get all available version folders
response = requests.get(base_url, headers=headers)
soup = BeautifulSoup(response.text, "html.parser")

version_folders = []
for link in soup.find_all("a", href=True):
    folder = link["href"].strip('/')
    if re.fullmatch(r"v17\.\d+", folder) and "beta" not in folder and "rc" not in folder:
        version_folders.append(folder)

# Step 2: Pick latest version
if not version_folders:
    print("❌ No valid v17.x versions found.")
    exit()

latest_version = sorted(version_folders, key=lambda v: list(map(int, v[1:].split('.'))))[-1]
print(f"✅ Found latest stable v17 version: {latest_version}")

# Step 3: Open version folder
version_url = f"{base_url}{latest_version}/"
response = requests.get(version_url, headers=headers)
soup = BeautifulSoup(response.text, "html.parser")

# Step 4: Match all relevant file types
results = []
file_patterns = [
    r"postgresql-\d+\.\d+\.tar\.(gz|bz2|xz)",                 # source tar files
    r"postgresql-\d+\.\d+-docs\.tar\.gz",                     # docs file
    r"postgresql-\d+\.\d+\.tar\.(gz|bz2|xz)\.(md5|sha256)",   # checksum files
]

for link in soup.find_all("a", href=True):
    text = link.text.strip()
    href = link["href"].strip()

    for pattern in file_patterns:
        if re.fullmatch(pattern, text):
            version_match = re.search(r"postgresql-(\d+\.\d+)", text)
            if version_match:
                version = version_match.group(1)
                file_url = href if href.startswith("http") else f"https://ftp.postgresql.org/pub/source/{latest_version}/{text}"
                results.append({
                    "product": "postgresql",
                    "version": version,
                    "text": text,
                    "url": file_url,
                    "platform": "Linux"
                })

# Step 5: Save JSON
if results:
    os.makedirs(save_path, exist_ok=True)
    with open(output_file, "w") as f:
        json.dump(results, f, indent=4)
    print(f"✅ JSON saved to: {output_file}")
else:
    print("⚠️ No matching files found.")
