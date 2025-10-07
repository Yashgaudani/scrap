import requests
import json
import os

# Constants
GITHUB_API = "https://api.github.com/repos/glpi-project/glpi-agent/releases/latest"
PRODUCT = "GLPI Agent"
OUTPUT_PATH = "/home/yash-gaudani/R%D/patch/Scraping/glpi-agent/glpi_agent.json"

# Detect platform and architecture from filename
def detect_platform_arch(filename):
    fname = filename.lower()
    platform = "Unknown"
    arch = "Unknown"

    # Platform detection
    if fname.endswith(('.msi', '.zip')):
        platform = "Windows"
    elif fname.endswith(('.dmg', '.pkg')):
        platform = "macOS"
    elif fname.endswith(('.rpm', '.pl', '.appimage', '.deb', '.tar.gz', '.snap')):
        platform = "Linux"

    # Architecture detection
    if 'x64' in fname or 'x86_64' in fname or 'amd64' in fname:
        arch = "x64"
    elif 'x86' in fname and 'x86_64' not in fname:
        arch = "x86"
    elif 'arm64' in fname or 'aarch64' in fname:
        arch = "ARM64"
    elif 'noarch' in fname or 'all' in fname:
        arch = "None"

    return platform, arch

# Fetch latest release data
response = requests.get(GITHUB_API)
data = response.json()

version = data["tag_name"].lstrip("v")
assets = data.get("assets", [])

# Prepare result list
results = []

for asset in assets:
    file_name = asset["name"]
    url = asset["browser_download_url"]
    platform, architecture = detect_platform_arch(file_name)

    results.append({
        "product": PRODUCT,
        "version": version,
        "file_name": file_name,
        "url": url,
        "platform": platform,
        "architecture": architecture
    })

# Create directory if not exists
os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)

# Save to JSON file
with open(OUTPUT_PATH, "w") as f:
    json.dump(results, f, indent=2)

print(f"✅ Saved {len(results)} entries to: {OUTPUT_PATH}")
