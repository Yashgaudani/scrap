import requests
from bs4 import BeautifulSoup
import re
import json

base_url = "https://archive.apache.org/dist/netbeans/netbeans-installers/"
latest_version = "25"
final_url = f"{base_url}{latest_version}/"

# File extensions to include
installer_extensions = {
    ".exe": "Windows",
    ".pkg": "macOS",
    ".rpm": "Linux (RPM)",
    ".deb": "Linux (DEB)"
}

response = requests.get(final_url)
soup = BeautifulSoup(response.text, "html.parser")

data = []

for link in soup.find_all("a", href=True):
    file_name = link['href']
    for ext, platform in installer_extensions.items():
        if file_name.endswith(ext) and not file_name.endswith(ext + ".asc") and not file_name.endswith(ext + ".sha512"):
            download_link = final_url + file_name
            data.append({
                "product": "Apache NetBeans",
                "version": latest_version,
                "text": file_name,
                "url": download_link,
                "platform": platform
            })

# Save to JSON file
with open("netbeans_latest.json", "w") as f:
    json.dump(data, f, indent=4)

# Print result
print(f"✅ Found {len(data)} installer files for NetBeans version {latest_version}")
