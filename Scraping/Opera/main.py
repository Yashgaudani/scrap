import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import json
import os

output_path = "/home/yash-gaudani/R%D/patch/Scraping/Opera/opera_downloads.json"

def get_links(url):
    res = requests.get(url)
    res.raise_for_status()
    soup = BeautifulSoup(res.text, "html.parser")
    return [urljoin(url, a['href']) for a in soup.find_all("a", href=True)]

def parse_version(url):
    folder = url.rstrip("/").split("/")[-1]
    try:
        return tuple(map(int, folder.split(".")))
    except:
        return (0, 0, 0, 0)

# Step-by-step navigation
base_url = "https://get.geo.opera.com/"
ftp_url = [l for l in get_links(base_url) if l.endswith("ftp/")][0]
pub_url = [l for l in get_links(ftp_url) if l.endswith("pub/")][0]
opera_url = [l for l in get_links(pub_url) if l.endswith("opera/")][0]
desktop_url = [l for l in get_links(opera_url) if l.endswith("desktop/")][0]

# Get latest version folder (sorted numerically)
version_links = get_links(desktop_url)
version_folders = [l for l in version_links if l.rstrip("/").split("/")[-1][0].isdigit()]
latest_version_url = sorted(version_folders, key=parse_version, reverse=True)[0]
latest_version = latest_version_url.rstrip("/").split("/")[-1]

# Get download links per OS
os_links = get_links(latest_version_url)
os_folders = [l for l in os_links if any(x in l for x in ["win/", "mac/", "linux/"])]

data = []

platform_map = {
    "win": "Windows",
    "mac": "macOS",
    "linux": "Linux"
}

for os_folder in os_folders:
    platform_key = os_folder.rstrip("/").split("/")[-1]
    platform = platform_map.get(platform_key, "Unknown")
    file_links = get_links(os_folder)

    for file_url in file_links:
        if not file_url.endswith("/"):
            file_name = file_url.split("/")[-1]
            entry = {
                "product": "opera",
                "version": latest_version,
                "text": file_name,
                "url": file_url,
                "platform": platform
            }
            data.append(entry)

# Ensure the directory exists
os.makedirs(os.path.dirname(output_path), exist_ok=True)

# Save to JSON
with open(output_path, "w") as f:
    json.dump(data, f, indent=4)

print(f"\n✅ Saved {len(data)} download links to:\n{output_path}")
