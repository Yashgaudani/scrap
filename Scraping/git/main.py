##################3333 find to latest version url @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@


import requests
from bs4 import BeautifulSoup

URL = "https://github.com/git-for-windows/git/releases"
HEADERS = {"User-Agent": "Mozilla/5.0"}

response = requests.get(URL, headers=HEADERS)
soup = BeautifulSoup(response.content, "html.parser")

latest_label = soup.find("span", string="Latest")
if latest_label:
    parent = latest_label.find_parent("div")
    release_link_tag = parent.find("a", href=True)
    if release_link_tag:
        release_text = release_link_tag.get_text(strip=True)
        release_url = "https://github.com" + release_link_tag["href"]
        print({
            "text": release_text,
            "url": release_url
        })


print("##############################################################")

########################### source url ############################33


import requests
from bs4 import BeautifulSoup
import json
import os

# Configuration
url = "https://github.com/git-for-windows/git/releases/expanded_assets/v2.49.0.windows.1"
product = "Git for Windows"
version = "2.49.0.windows.1"
base_url = "https://github.com"
save_path = "/home/yash-gaudani/R%D/Vlc/git/git_downloads.json"

# Request and parse
response = requests.get(url)
response.raise_for_status()
soup = BeautifulSoup(response.text, "html.parser")

data = []

# Extract download links
for a in soup.find_all("a", href=True):
    href = a["href"]
    text = a.text.strip()
    
    # Only download-related files
    if not href.endswith((".exe", ".zip", ".7z.exe", ".tar.bz2", ".tar.gz", ".tar.xz")):
        continue

    file_name = href.split("/")[-1]
    full_url = base_url + href if href.startswith("/") else href

    # Platform detection
    if "64" in file_name or "x64" in file_name:
        platform = "Windows 64-bit"
    elif "32" in file_name or "x86" in file_name:
        platform = "Windows 32-bit"
    elif "arm64" in file_name:
        platform = "Windows ARM64"
    else:
        platform = "Unknown"

    # JSON structure
    entry = {
        "product": product,
        "file_name": file_name,
        "version": version,
        "text": text if text else "Download",
        "url": full_url,
        "platform": platform
    }

    data.append(entry)

# Save to JSON file
os.makedirs(os.path.dirname(save_path), exist_ok=True)
with open(save_path, "w") as f:
    json.dump(data, f, indent=2)

print(f"✅ Data saved to: {save_path}")

