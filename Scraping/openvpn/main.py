import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from packaging import version
import re
import json
import os

# Target URL
url = "https://openvpn.net/community-downloads"
file_types = ('.msi', '.exe', '.tar.gz', '.dmg')

# Regex to extract version
version_pattern = re.compile(r'(\d+\.\d+\.\d+)')

# Mapping for platform names based on file extension
platform_map = {
    '.msi': 'Windows',
    '.exe': 'Windows',
    '.dmg': 'macOS',
    '.tar.gz': 'Linux'
}

# Storage for valid links
valid_links = []

# Fetch page
response = requests.get(url)
soup = BeautifulSoup(response.content, "html.parser")

# Extract all valid download links
for link in soup.find_all("a", href=True):
    href = link['href']
    text = link.get_text(strip=True)

    if not href.lower().endswith(file_types):
        continue
    if any(tag in href.lower() for tag in ['alpha', 'beta', 'rc']):
        continue

    match = version_pattern.search(href)
    if not match:
        continue

    ver = version.parse(match.group(1))
    full_url = urljoin(url, href)
    ext = next((ft for ft in file_types if href.lower().endswith(ft)), None)

    valid_links.append({
        "product": "openvpn",
        "version": str(ver),
        "text": text or href.split('/')[-1],
        "url": full_url,
        "platform": platform_map.get(ext, "Unknown")
    })

# Find the latest stable version
if valid_links:
    latest_version = max(version.parse(item['version']) for item in valid_links)

    # Filter only latest version entries
    latest_links = [item for item in valid_links if version.parse(item['version']) == latest_version]

    # Overwrite version field with 'latest'
    for item in latest_links:
        pass

    # Save to JSON
    output_path = "/home/yash-gaudani/R%D/patch/Scraping/openvpn/openvpn_downloads.json"
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, "w") as f:
        json.dump(latest_links, f, indent=4)

    print(f"✅ JSON file saved to: {output_path}")
else:
    print("❌ No stable versions found.")
