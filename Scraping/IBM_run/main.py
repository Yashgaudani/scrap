import requests
import re
import json
import os
from urllib.parse import urlparse

# Constants
REPO_API = "https://api.github.com/repos/ibmruntimes/semeru23-binaries/releases/latest"
PRODUCT_NAME = "IBM Semeru Runtime Open Edition"
SAVE_PATH = "/home/yash-gaudani/R%D/patch/Scraping/IBM_run/semeru_assets.json"

# Mappings
PLATFORM_MAP = {
    "windows": "Windows",
    "linux": "Linux",
    "mac": "macOS",
    "osx": "macOS",
    "aix": "AIX"
}
ARCH_MAP = {
    "x64": "x64",
    "x86_64": "x64",
    "aarch64": "aarch64",
    "ppc64": "ppc64",
    "ppc64le": "ppc64le",
    "s390x": "s390x"
}

# Extract the file extension safely (handles .tar.gz, etc.)
def get_file_extension(file_name):
    if file_name.endswith(".tar.gz"):
        return ".tar.gz"
    return os.path.splitext(file_name)[1]

# Parse asset metadata
def parse_asset(asset):
    file_name = asset["name"]
    url = asset["browser_download_url"]

    # Platform
    platform = next((v for k, v in PLATFORM_MAP.items() if k in file_name.lower()), "Unknown")

    # Architecture
    architecture = next((v for k, v in ARCH_MAP.items() if k in file_name.lower()), "Unknown")

    # Version (e.g., 23.0.2)
    version_match = re.search(r"(\d{2}\.\d+\.\d+)", file_name)
    version = version_match.group(1) if version_match else "Unknown"

    # Type: JDK, JRE, or other
    type_ = (
        "JDK" if "jdk" in file_name.lower()
        else "JRE" if "jre" in file_name.lower()
        else "TestImage" if "testimage" in file_name.lower()
        else "DebugImage" if "debugimage" in file_name.lower()
        else "Unknown"
    )

    return {
        "product": PRODUCT_NAME,
        "version": version,
        "file_name": file_name,
        "url": url,
        "platform": platform,
        "architecture": architecture,
        "type": type_,
        "extension": get_file_extension(file_name)
    }

# Fetch from GitHub API
response = requests.get(REPO_API)
release_data = response.json()
assets = release_data.get("assets", [])

# Parse and filter relevant extensions
allowed_extensions = (".zip", ".tar.gz", ".msi", ".pkg", ".rpm")
parsed_assets = [parse_asset(asset) for asset in assets if asset["name"].endswith(allowed_extensions)]

# Ensure directory exists
os.makedirs(os.path.dirname(SAVE_PATH), exist_ok=True)

# Save to JSON file
with open(SAVE_PATH, "w") as f:
    json.dump(parsed_assets, f, indent=2)

print(f"Saved {len(parsed_assets)} entries to {SAVE_PATH}")
