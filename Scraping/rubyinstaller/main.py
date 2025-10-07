import requests
import json
import os

# GitHub API URL for latest release
API_URL = "https://api.github.com/repos/oneclick/rubyinstaller2/releases/latest"

# Destination JSON file path
OUTPUT_PATH = "/home/yash-gaudani/R%D/patch/Scraping/rubyinstaller/rubyinstaller.json"

# Fetch latest release data
response = requests.get(API_URL)
response.raise_for_status()
release = response.json()

version = release.get("tag_name", "")
assets = release.get("assets", [])

# Build JSON list
json_data = []
for asset in assets:
    name = asset["name"]
    url = asset["browser_download_url"]

    # Skip signature files
    if name.endswith(".asc"):
        continue

    # Determine architecture
    if "x64" in name:
        architecture = "x64"
    elif "x86" in name:
        architecture = "x86"
    elif "arm" in name:
        architecture = "arm64"
    else:
        architecture = "unknown"

    # Determine platform from file extension
    if name.endswith(".exe"):
        platform = "Windows"
    elif name.endswith(".dmg"):
        platform = "macOS"
    elif name.endswith(".tar.gz") or name.endswith(".tgz"):
        platform = "Linux"
    else:
        platform = "Unknown"

    # Filter for supported formats only
    if platform == "Unknown":
        continue

    json_data.append({
        "product": "RubyInstaller",
        "version": version,
        "file_name": name,
        "url": url,
        "platform": platform,
        "architecture": architecture
    })

# Create directory if not exists
os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)

# Save JSON to file
with open(OUTPUT_PATH, "w") as f:
    json.dump(json_data, f, indent=2)

print(f"JSON saved to: {OUTPUT_PATH}")
