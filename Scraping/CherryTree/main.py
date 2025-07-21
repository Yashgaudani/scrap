import requests
import json

# GitHub API URL for latest CherryTree release
url = "https://api.github.com/repos/giuspen/cherrytree/releases/latest"

# Output file path
output_path = "/home/yash-gaudani/R%D/patch/Scraping/CherryTree/cherrytree_latest.json"

# Detect platform from file name
def detect_platform(name):
    name = name.lower()
    if "win64" in name or "win32" in name or name.endswith((".exe", ".msi", ".7z")):
        return "Windows"
    elif "appimage" in name or name.endswith((".deb", ".rpm", ".tar.xz")):
        return "Linux"
    elif "macos" in name or name.endswith(".dmg"):
        return "macOS"
    else:
        return "Unknown"

# Detect architecture from file name
def detect_architecture(name):
    name = name.lower()
    if "win64" in name or "x64" in name or "x86_64" in name or "amd64" in name:
        return "x64"
    elif "win32" in name or "x86" in name or "i386" in name:
        return "x86"
    elif "arm64" in name or "aarch64" in name:
        return "arm64"
    else:
        return "Unknown"

# Fetch and parse GitHub API response
response = requests.get(url)
release = response.json()
version = release.get("tag_name", "Unknown")

output = []

for asset in release.get("assets", []):
    name = asset["name"]
    # Focus only on distributable formats
    if not name.endswith((".exe", ".msi", ".deb", ".rpm", ".tar.xz", ".appimage", ".7z")):
        continue

    output.append({
        "product": "CherryTree",
        "version": version,
        "file_name": name,
        "url": asset["browser_download_url"],
        "platform": detect_platform(name),
        "architecture": detect_architecture(name)
    })

# Save to JSON file
with open(output_path, "w") as f:
    json.dump(output, f, indent=2)

print(f"✔ Metadata saved to: {output_path}")
