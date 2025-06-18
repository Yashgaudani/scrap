import requests
from bs4 import BeautifulSoup
import re
import json
import urllib.parse

# Step 1: Access Base Page
BASE_URL = "https://mobaxterm.mobatek.net/download-home-edition.html"

# Step 2: Fetch Page Content
response = requests.get(BASE_URL)
response.raise_for_status()
soup = BeautifulSoup(response.text, "html.parser")

# Step 3: Scan for Links Ending with .zip, .exe, .msi
links = soup.find_all("a", href=True)
results = []

for link in links:
    href = link["href"]
    if href.endswith((".zip", ".exe", ".msi")) and "MobaXterm_Portable_v" in href:
        # Step 4: Parse version from filename
        file_name = href.split("/")[-1]
        match = re.search(r"MobaXterm_Portable_v(\d+(?:\.\d+)*)\.zip", file_name)
        if match:
            version = match.group(1)
            download_url = urllib.parse.urljoin(BASE_URL, href)

            results.append({
                "product" : "MobaXterm",
                "file_name": file_name,
                "version": version,
                "download_url": download_url,
                "platform": "Windows"
            })

# Step 5: Save to JSON
with open("mobaxterm_downloads.json", "w") as f:
    json.dump(results, f, indent=4)

print(f"✅ {len(results)} MobaXterm entries saved to mobaxterm_downloads.json")
