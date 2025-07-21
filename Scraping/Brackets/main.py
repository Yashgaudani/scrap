import requests
import json
import os

# GitHub API endpoint for Brackets latest release
API_URL = "https://api.github.com/repos/adobe/brackets/releases/latest"
PRODUCT_NAME = "Brackets"

# Output JSON path
OUTPUT_PATH = "/home/yash-gaudani/R%D/patch/Scraping/Brackets/brackets_latest.json"

# Fallback mapping of file extensions to platforms
EXTENSION_FALLBACK = {
    ".exe": "Windows",
    ".zip": "Windows",
    ".dmg": "macOS",
    ".pkg": "macOS",
    ".msi":"Windows"
}

# Keyword mapping for platform detection
PLATFORM_KEYWORDS = {
    "win": "Windows",
    "mac": "macOS",
    "dmg": "macOS",
    "pkg": "macOS"
}

# Architecture detection keywords
ARCHITECTURE_KEYWORDS = {
    "64": "x64",
    "32": "x86"
}

# Fetch release data
response = requests.get(API_URL)
response.raise_for_status()
data = response.json()
version = data.get("tag_name", "").lstrip("v")
assets = data.get("assets", [])

# Process assets
results = []
for asset in assets:
    name = asset.get("name", "")
    url = asset.get("browser_download_url", "")
    lower = name.lower()
    ext = os.path.splitext(lower)[1]

    # Detect platform
    platform = None
    for k, v in PLATFORM_KEYWORDS.items():
        if k in lower:
            platform = v
            break
    if not platform:
        platform = EXTENSION_FALLBACK.get(ext, "Unknown")

    # Detect architecture
    architecture = "Unknown"
    for k, arch in ARCHITECTURE_KEYWORDS.items():
        if k in lower:
            architecture = arch
            break

    results.append({
        "product": PRODUCT_NAME,
        "version": version,
        "file_name": name,
        "url": url,
        "platform": platform,
        "architecture": architecture
    })

# Save JSON
os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)
with open(OUTPUT_PATH, "w") as f:
    json.dump(results, f, indent=2)

print(f"✅ JSON saved to: {OUTPUT_PATH}")
