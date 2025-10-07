import requests
from bs4 import BeautifulSoup
import re
import json
import os

BASE_URL = "https://packages.element.io/desktop/install/"
PRODUCT = "Element Desktop"
OUTPUT_PATH = "/home/yash-gaudani/R%D/patch/Scraping/Element/element.json"

PLATFORM_ARCH_MAP = {
    "win32": {
        "x64": ("Windows", "x64"),
        "ia32": ("Windows", "x86"),
        "arm64": ("Windows", "ARM64"),
    },
    "macos": {
        "": ("macOS", "Universal")
    },
    "linux": {
        "glibc-x86-64": ("Linux", "x64"),
        "glibc-aarch64": ("Linux", "ARM64"),
    }
}

def get_file_list(url):
    resp = requests.get(url)
    resp.raise_for_status()
    soup = BeautifulSoup(resp.text, "html.parser")
    return [
        link.get("href") for link in soup.find_all("a")
        if link.get("href") and not link.get("href").startswith("..")
    ]

def extract_version(filename):
    match = re.search(r"(\d+\.\d+\.\d+)", filename)
    return match.group(1) if match else None

results = []

for platform, arch_map in PLATFORM_ARCH_MAP.items():
    for arch_folder, (plat_name, arch_name) in arch_map.items():
        url = f"{BASE_URL}{platform}/" + (f"{arch_folder}/" if arch_folder else "")
        print(f"Fetching: {url}")
        try:
            files = get_file_list(url)

            # Filter based on platform
            if plat_name == "Windows":
                filtered = [f for f in files if f.startswith("Element Setup") and f.endswith(".exe")]
            elif plat_name == "macOS":
                filtered = [f for f in files if f.endswith(".dmg")]
            elif plat_name == "Linux":
                filtered = [f for f in files if f.endswith(".tar.gz") and f.startswith("element-desktop")]
            else:
                filtered = []

            versioned_files = [(f, extract_version(f)) for f in filtered if extract_version(f)]
            versioned_files.sort(key=lambda x: list(map(int, x[1].split("."))), reverse=True)

            if versioned_files:
                latest_file, version = versioned_files[0]
                results.append({
                    "product": PRODUCT,
                    "version": version,
                    "file_name": latest_file,
                    "url": url + latest_file,
                    "platform": plat_name,
                    "architecture": arch_name
                })

        except Exception as e:
            print(f"[ERROR] Failed to fetch from {url}: {e}")

# Save to JSON
os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)
with open(OUTPUT_PATH, "w") as f:
    json.dump(results, f, indent=2)

print(f"✅ Saved {len(results)} entries to {OUTPUT_PATH}")
