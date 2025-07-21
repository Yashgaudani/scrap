import requests
import json

# GitHub API URL for latest Draw.io Desktop release
url = "https://api.github.com/repos/jgraph/drawio-desktop/releases/latest"

# Output file path
output_path = "/home/yash-gaudani/R%D/patch/Scraping/Drawio/drawio_latest.json"

# Detect platform
def detect_platform(name):
    name = name.lower()
    if name.endswith((".exe", ".msi", ".zip")) or "windows" in name:
        return "Windows"
    elif name.endswith(".dmg") or "mac" in name:
        return "macOS"
    elif name.endswith((".appimage", ".deb", ".rpm")) or "linux" in name:
        return "Linux"
    else:
        return "Unknown"

# Detect architecture
def detect_architecture(name):
    name = name.lower()
    if "x64" in name or "x86_64" in name or "amd64" in name:
        return "x64"
    elif "ia32" in name or "x86" in name or "32bit" in name or "win32" in name or "i386" in name:
        return "x86"
    elif "arm64" in name or "aarch64" in name:
        return "arm64"
    elif "universal" in name:
        return "universal"
    else:
        return "32-bit"

# Fetch latest release data
response = requests.get(url)
release = response.json()
version = release.get("tag_name", "Unknown")

output = []

# Process each asset in the release
for asset in release.get("assets", []):
    name = asset["name"]

    # Filter by valid formats only (skip .blockmap, .yml, etc.)
    if not name.endswith((".exe", ".msi", ".zip", ".dmg", ".deb", ".rpm", ".AppImage")):
        continue

    output.append({
        "product": "Draw.io",
        "version": version,
        "file_name": name,
        "url": asset["browser_download_url"],
        "platform": detect_platform(name),
        "architecture": detect_architecture(name)
    })

# Save output to JSON
with open(output_path, "w") as f:
    json.dump(output, f, indent=2)

print(f"✔ Metadata for Draw.io {version} saved to: {output_path}")
