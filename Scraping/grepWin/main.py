import requests
import json
import re

# GitHub API URL for grepWin
url = "https://api.github.com/repos/stefankueng/grepWin/releases/latest"

# Output path
output_path = "/home/yash-gaudani/R%D/patch/Scraping/grepWin/grepWin_latest.json"

# Detect platform
def detect_platform(name):
    return "Windows" if name.lower().endswith((".exe", ".msi")) else "Unknown"

# Detect architecture
def detect_architecture(name):
    name = name.lower()
    if "x64" in name or "amd64" in name:
        return "x64"
    elif "x86" in name or "win32" in name:
        return "x86"
    else:
        return "x86"

# Fetch latest release
response = requests.get(url)
release = response.json()
version = release.get("tag_name", "Unknown")

output = []

# Process assets
for asset in release.get("assets", []):
    name = asset["name"]

    # Include only .exe and .msi
    if not name.lower().endswith((".exe", ".msi")):
        continue

    output.append({
        "product": "grepWin",
        "version": version,
        "file_name": name,
        "url": asset["browser_download_url"],
        "platform": detect_platform(name),
        "architecture": detect_architecture(name)
    })

# Save to JSON
with open(output_path, "w") as f:
    json.dump(output, f, indent=2)

print(f"✔ Only .exe and .msi metadata saved to: {output_path}")
