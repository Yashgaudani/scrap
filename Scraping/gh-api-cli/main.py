import requests
import json
import re

# GitHub API URL for latest release
url = "https://api.github.com/repos/mh-cbon/gh-api-cli/releases/latest"

# Output JSON path
output_path = "/home/yash-gaudani/R%D/patch/Scraping/gh-api-cli/gh-api-cli_latest.json"

# Detect platform from filename
def detect_platform(name):
    name = name.lower()
    if "darwin" in name:
        return "macOS"
    elif name.endswith(".msi"):
        return "Windows"
    elif name.endswith(".deb") or name.endswith(".rpm"):
        return "Linux"
    else:
        return "Unknown"

# Detect architecture from filename
def detect_architecture(name):
    name = name.lower()
    if "amd64" in name:
        return "x64"
    elif "386" in name:
        return "x86"
    else:
        return "Unknown"

# Fetch latest release info
response = requests.get(url)
release = response.json()
version = release.get("tag_name", "Unknown")

output = []

for asset in release.get("assets", []):
    name = asset["name"]
    
    # Skip source code archives
    if name.lower().startswith("source code"):
        continue
    
    platform = detect_platform(name)
    arch = detect_architecture(name)
    
    output.append({
        "product": "gh-api-cli",
        "version": version,
        "file_name": name,
        "url": asset["browser_download_url"],
        "platform": platform,
        "architecture": arch
    })

# Save metadata to JSON
with open(output_path, "w") as f:
    json.dump(output, f, indent=2)

print(f"✔ Metadata saved to: {output_path}")
