import requests
from bs4 import BeautifulSoup
import json
import urllib.parse
import os

BASE_HOST = "https://download-installer.cdn.mozilla.net"
BASE_PATH = "/pub/thunderbird/releases/"
VERSION = "139.0.2"
LANGUAGE = "uk"

PLATFORMS = {
    "win64": "Windows 64-bit",
    "win32": "Windows 32-bit",
    "mac": "macOS",
    "linux-x86_64": "Linux 64-bit"
}

results = []

for folder, platform_name in PLATFORMS.items():
    relative_path = f"{BASE_PATH}{VERSION}/{folder}/{LANGUAGE}/"
    full_url_path = urllib.parse.urljoin(BASE_HOST, relative_path)

    try:
        response = requests.get(full_url_path)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")

        for link in soup.find_all("a"):
            href = link.get("href")
            if href and not href.startswith("?") and not href.endswith("/"):
                # ✅ Get only the file name (not the path)
                file_name = os.path.basename(href.strip())
                download_url = urllib.parse.urljoin(full_url_path, file_name)

                results.append({
                    "product": "Thunderbird",
                    "version": VERSION,
                    "file name": file_name,
                    "url": download_url,
                    "platform": platform_name
                })

    except Exception as e:
        print(f"❌ Error accessing {full_url_path}: {e}")

# Save to JSON
with open("thunderbird_downloads.json", "w") as f:
    json.dump(results, f, indent=4)

print(f"✅ {len(results)} Thunderbird files saved to thunderbird_downloads.json")
