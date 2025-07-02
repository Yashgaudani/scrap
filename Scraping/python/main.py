import requests
from bs4 import BeautifulSoup
import re
import json
import os

# Constants
base_url = 'https://www.python.org/ftp/python/'
save_dir = '/home/yash-gaudani/R%D/patch/Scraping/python'
save_file = os.path.join(save_dir, 'python_downloads.json')

# Step 1: Get version directories
resp = requests.get(base_url)
soup = BeautifulSoup(resp.text, 'html.parser')
versions = [
    a['href'].strip('/')
    for a in soup.find_all('a')
    if re.match(r'^\d+\.\d+\.\d+/$', a['href'])
]

# Step 2: Sort and find second latest stable version
versions.sort(key=lambda v: list(map(int, v.split('.'))), reverse=True)
second_latest = versions[1]
version_url = f"{base_url}{second_latest}/"

# Step 3: Fetch file list from version folder
resp = requests.get(version_url)
soup = BeautifulSoup(resp.text, 'html.parser')

# Step 4: Only keep valid installer file types
valid_exts = ('.exe', '.msi', '.pkg', '.dmg', '.tar.xz', '.tgz', '.zip')

# Helper to extract platform + architecture
def detect_platform_arch(fname):
    fname_lower = fname.lower()
    if fname_lower.endswith('.exe') or 'win' in fname_lower:
        platform = "Windows"
    elif fname_lower.endswith('.pkg') or fname_lower.endswith('.dmg') or 'mac' in fname_lower or 'osx' in fname_lower:
        platform = "macOS"
    elif fname_lower.endswith(('.tar.xz', '.tgz', '.zip')):
        platform = "Linux"
    else:
        platform = "Unknown"

    if 'amd64' in fname_lower or 'x86_64' in fname_lower:
        arch = 'x64'
    elif 'arm64' in fname_lower or 'aarch64' in fname_lower:
        arch = 'ARM64'
    elif 'win32' in fname_lower or 'x86' in fname_lower:
        arch = 'x86'
    else:
        arch = 'Unknown'

    return platform, arch

# Step 5: Build structured JSON
output = []
for a in soup.find_all('a'):
    fname = a['href']
    if fname.endswith(valid_exts):
        platform, arch = detect_platform_arch(fname)
        output.append({
            "product": "Python",
            "file_name": fname,
            "version": second_latest,
            "download_url": version_url + fname,
            "platform": platform,
            "architecture": arch
        })

# Step 6: Save JSON to file
os.makedirs(save_dir, exist_ok=True)
with open(save_file, 'w') as f:
    json.dump(output, f, indent=4)

print(f"✅ JSON saved to: {save_file}")
