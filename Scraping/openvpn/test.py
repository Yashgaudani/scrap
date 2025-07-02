import requests
from bs4 import BeautifulSoup
import re
import json
import os

url = "https://build.openvpn.net/downloads/releases/latest/"
response = requests.get(url)
response.raise_for_status()
soup = BeautifulSoup(response.text, "html.parser")

results = []

for link in soup.find_all("a"):
    href = link.get("href", "")
    text = link.get_text(strip=True)

    if "stable" in href and href.endswith((".msi", ".tar.gz", ".tar.gz.asc", ".msi.asc")):
        match = re.search(r'openvpn[-_](\d+\.\d+\.\d+)', href)
        version = match.group(1) if match else "unknown"

        if "amd64" in href or "x64" in href:
            platform = "Windows 64-bit"
        elif "x86" in href:
            platform = "Windows 32-bit"
        else:
            platform = "Windows"

        results.append({
            "product": "openvpn",
            "version": version,
            "text": text,
            "url": url + href,
            "platform": platform
        })

# Save to JSON file
output_path = "/home/yash-gaudani/R%D/patch/Scraping/openvpn/openvpn.json"
os.makedirs(os.path.dirname(output_path), exist_ok=True)

with open(output_path, "w") as f:
    json.dump(results, f, indent=4)

print(f"✅ JSON saved to: {output_path}")
