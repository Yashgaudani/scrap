import requests
from bs4 import BeautifulSoup
import re
from urllib.parse import urljoin
import json
import os

# Target URL
url = "https://learn.microsoft.com/en-us/power-bi/fundamentals/desktop-latest-update-archive?tabs=powerbi-desktop"

# Save path
save_dir = '/home/yash-gaudani/R%D/patch/Scraping/powerBI'
os.makedirs(save_dir, exist_ok=True)
save_file = os.path.join(save_dir, 'powerbi_downloads.json')

# Fetch HTML
resp = requests.get(url)
soup = BeautifulSoup(resp.text, 'html.parser')

# Step 1: Extract latest version from <h2>
version_pattern = re.compile(r"\((2\.\d+\.\d+\.\d+)\)")
latest_version = None

for h2 in soup.find_all("h2"):
    match = version_pattern.search(h2.text)
    if match:
        latest_version = match.group(1)
        break

if not latest_version:
    print("❌ No version found.")
    exit()

# Step 2: Find all file links and detect latest date from file names
valid_exts = ('.exe', '.msi', '.zip')
date_pattern = re.compile(r"(20\d{2}-\d{2})")  # e.g. 2025-05

# Extract all available YYYY-MM in filenames
dates_found = []
for a in soup.find_all('a', href=True):
    fname = os.path.basename(a['href'])
    match = date_pattern.search(fname)
    if match:
        dates_found.append(match.group(1))

if not dates_found:
    print("❌ No file names with dates like YYYY-MM found.")
    exit()

# Get latest date in YYYY-MM format
dates_found.sort(reverse=True)
latest_date = dates_found[0]

# Step 3: Extract only files containing that date
results = []

for a in soup.find_all('a', href=True):
    href = a['href']
    file_name = os.path.basename(href)
    if latest_date in file_name and any(ext in file_name.lower() for ext in valid_exts):
        full_url = href if href.startswith('http') else urljoin(url, href)
        fname_lower = file_name.lower()

        # Detect architecture
        if 'arm64' in fname_lower:
            arch = 'ARM64'
        elif 'x64' in fname_lower or 'win64' in fname_lower or '64' in fname_lower:
            arch = 'x64'
        elif 'x86' in fname_lower or '32' in fname_lower:
            arch = 'x86'
        else:
            arch = '32-bit'

        results.append({
            "product": "Power BI",
            "version": latest_version,
            "file_name": file_name,
            "url": full_url,
            "platform": f"Windows {arch}",
       
        })

# Step 4: Save to JSON
with open(save_file, 'w') as f:
    json.dump(results, f, indent=4)

print(f"✅ JSON saved to: {save_file}")
