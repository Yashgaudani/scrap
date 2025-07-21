import requests
from bs4 import BeautifulSoup
import json
import re
from packaging.version import Version

# Base URL and output path
base_url = "https://download.geany.org/"
output_path = "/home/yash-gaudani/R%D/patch/Scraping/Geany/geany_latest.json"

# Helpers
def detect_version(name):
    match = re.search(r"geany[-_]v?(\d+(?:\.\d+)+)", name)
    return match.group(1) if match else None

def detect_platform(name):
    name = name.lower()
    if name.endswith(".exe") or name.endswith(".msi"):
        return "Windows"
    elif name.endswith(".dmg"):
        return "macOS"
    elif name.endswith(".deb") or name.endswith(".tar.gz") or name.endswith(".tar.xz"):
        return "Linux"
    elif name.endswith(".zip"):
        return "Cross-platform"
    else:
        return "Unknown"

def detect_architecture(name):
    name = name.lower()
    if "x86_64" in name or "amd64" in name:
        return "x64"
    elif "i386" in name or "x86" in name:
        return "x86"
    elif "arm64" in name or "aarch64" in name:
        return "arm64"
    else:
        return "Unknown"

# Scrape download directory
response = requests.get(base_url)
soup = BeautifulSoup(response.text, "html.parser")

# Parse versioned files
all_files = []
versions = set()

for link in soup.find_all("a", href=True):
    href = link["href"]
    if re.search(r"\.(tar\.gz|tar\.xz|deb|msi|exe|zip|dmg)$", href):
        version = detect_version(href)
        if version:
            versions.add(version)
            all_files.append((version, href))

# Find latest version
latest_version = str(max(Version(v) for v in versions))

# Filter files matching latest version
latest_files = []
for version, name in all_files:
    if version == latest_version:
        latest_files.append({
            "product": "Geany",
            "version": latest_version,
            "file_name": name,
            "url": base_url + name,
            "platform": detect_platform(name),
            "architecture": detect_architecture(name)
        })

# Save to JSON
with open(output_path, "w") as f:
    json.dump(latest_files, f, indent=2)

print(f"✔ Latest Geany version ({latest_version}) metadata saved to: {output_path}")
