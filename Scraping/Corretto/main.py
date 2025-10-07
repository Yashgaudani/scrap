import json
import re
import requests

# GitHub API URL
API_URL = "https://api.github.com/repos/corretto/corretto-24/releases/latest"
OUTPUT_PATH = "/home/yash-gaudani/R%D/patch/Scraping/Corretto/corretto.json"

# Known keyword map
PLATFORM_ARCH_MAP = {
    "linux-x64": ("Linux", "x64"),
    "linux-aarch64": ("Linux", "aarch64"),
    "windows-x64": ("Windows", "x64"),
    "macosx-x64": ("macOS", "x64"),
    "macosx-aarch64": ("macOS", "aarch64"),
    "alpine-linux-x64": ("Linux", "x64"),
    "alpine-linux-aarch64": ("Linux", "aarch64"),
}

def extract_platform_arch(filename):
    fname = filename.lower()

    # Match known keywords
    for key, value in PLATFORM_ARCH_MAP.items():
        if key in fname:
            return value

    # Fallback: infer from extension and arch hints
    ext_platform_map = {
        ".deb": "Linux",
        ".rpm": "Linux",
        ".tar.gz": "Linux",
        ".zip": "Windows",
        ".msi": "Windows",
        ".pkg": "macOS",
        ".dmg": "macOS"
    }

    arch_map = {
        "amd64": "x64",
        "x86_64": "x64",
        "aarch64": "aarch64",
        "arm64": "aarch64"
    }

    # Handle .tar.gz properly
    if fname.endswith(".tar.gz"):
        ext = ".tar.gz"
    else:
        parts = fname.split(".")
        ext = f".{parts[-1]}" if parts else ""

    platform = ext_platform_map.get(ext, "Unknown")

    arch = "Unknown"
    for key, val in arch_map.items():
        if key in fname:
            arch = val
            break

    return platform, arch

# Fetch release data
response = requests.get(API_URL)
response.raise_for_status()
data = response.json()

version = data.get("tag_name", "").lstrip("v").replace("jdk-", "")
body = data.get("body", "")
matches = re.findall(r'\[([^\]]+)\]\([^\)]+\).*?\[([^\]]+)\]\((https?://[^\s\)]+)\)', body)

results = []
for match in matches:
    file_name = match[1]
    url = match[2]
    platform, arch = extract_platform_arch(file_name)

    results.append({
        "product": "Amazon Corretto",
        "version": version,
        "file_name": file_name,
        "url": url,
        "platform": platform,
        "architecture": arch
    })

# Save JSON output
with open(OUTPUT_PATH, "w") as f:
    json.dump(results, f, indent=2)

print(f"✅ Extracted {len(results)} entries to {OUTPUT_PATH}")
