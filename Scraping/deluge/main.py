import requests
from bs4 import BeautifulSoup
import re
import json

BASE_URL = "http://ftp.osuosl.org/pub/deluge/"
OUTPUT_JSON = "/home/yash-gaudani/R%D/patch/Scraping/deluge/deluge_latest.json"

def extract_files(url):
    resp = requests.get(url)
    resp.raise_for_status()
    soup = BeautifulSoup(resp.text, "html.parser")
    return [a["href"] for a in soup.find_all("a", href=True)]

def get_latest_version(files, pattern):
    versions = []
    for name in files:
        match = re.search(pattern, name)
        if match:
            versions.append(match.group(1))
    try:
        return sorted(set(versions), key=lambda v: [int(x) for x in v.split('.')])[-1]
    except Exception:
        return None

def detect_architecture(filename):
    filename = filename.lower()
    if "win64" in filename or "x64" in filename:
        return "x64"
    elif "win32" in filename or "x86" in filename:
        return "x86"
    elif "mac" in filename or "osx" in filename:
        return "x64" if "x64" in filename else "x86"
    return "Unknown"

def generate_json():
    result = []

    # 1. Windows
    windows_url = BASE_URL + "windows/"
    win_files = extract_files(windows_url)
    setup_files = [f for f in win_files if f.endswith(".exe") and "setup" in f and not f.endswith(".sha256")]
    
    # Extract versions from filenames
    version_pattern = r"deluge-([\d.]+)-win"
    all_versions = []
    for f in setup_files:
        match = re.search(version_pattern, f)
        if match:
            all_versions.append(match.group(1))

    # Detect latest version
    latest_version = sorted(set(all_versions), key=lambda v: [int(x) for x in v.split('.')])[-1] if all_versions else None

    for f in setup_files:
        if latest_version and latest_version in f:
            result.append({
                "product": "Deluge",
                "version": latest_version,
                "file_name": f,
                "url": windows_url + f,
                "platform": "Windows",
                "architecture": detect_architecture(f)
            })

    # 2. macOS
    mac_url = BASE_URL + "mac_osx/"
    mac_files = extract_files(mac_url)
    latest_mac_version = get_latest_version(mac_files, r"deluge-([\d.]+)[.-]mac")

    for f in mac_files:
        if latest_mac_version and latest_mac_version in f and (f.endswith(".dmg") or f.endswith(".tbz2")):
            result.append({
                "product": "Deluge",
                "version": latest_mac_version,
                "file_name": f,
                "url": mac_url + f,
                "platform": "macOS",
                "architecture": detect_architecture(f)
            })

    # 3. Source
    source_base_url = BASE_URL + "source/"
    src_versions = extract_files(source_base_url)
    latest_src_version = get_latest_version(src_versions, r"^([\d.]+)/$")

    if latest_src_version:
        full_source_url = source_base_url + latest_src_version + "/"
        src_files = extract_files(full_source_url)

        for f in src_files:
            if f.endswith(".tar.xz"):
                result.append({
                    "product": "Deluge",
                    "version": latest_src_version,
                    "file_name": f,
                    "url": full_source_url + f,
                    "platform": "Source",
                    "architecture": "Unknown"
                })

    # Save JSON
    with open(OUTPUT_JSON, "w") as f:
        json.dump(result, f, indent=2)

    print(f"✅ Saved {len(result)} entries to {OUTPUT_JSON}")

# Run
generate_json()
