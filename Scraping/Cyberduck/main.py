import requests
from bs4 import BeautifulSoup
import re
import os
import json
from collections import defaultdict

BASE_URL = "https://cyberduck.io/changelog/"
OUTPUT_PATH = "/home/yash-gaudani/R%D/patch/Scraping/Cyberduck/cyberduck_latest.json"

EXTENSION_OS_MAP = {
    'exe': 'Windows',
    'msi': 'Windows',
    'zip': 'macOS',
    'dmg': 'macOS',
    'pkg': 'macOS',
    'tar.gz': 'Linux',
    'deb': 'Linux',
    'rpm': 'Linux'
}

def get_file_type(href):
    if href.endswith('.tar.gz'):
        return 'tar.gz'
    match = re.search(r'\.([a-z0-9]+)$', href)
    return match.group(1).lower() if match else None

def extract_file_info():
    response = requests.get(BASE_URL)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, "html.parser")
    links = [a['href'] for a in soup.find_all("a", href=True)]

    file_data = []

    for href in links:
        file_type = get_file_type(href)
        if not file_type or file_type not in EXTENSION_OS_MAP:
            continue

        full_url = href if href.startswith("http") else f"https://cyberduck.io{href}"
        version_match = re.search(r'(\d+\.\d+\.\d+)', href)
        if not version_match:
            continue

        version = version_match.group(1)
        os_name = EXTENSION_OS_MAP[file_type]
        file_data.append({
            "product": "Cyberduck",
            "version": version,
            "text": f"Download for {os_name} – {file_type.upper()}",
            "url": full_url,
            "platform": os_name
        })

    return file_data

def find_latest_by_os(file_data):
    latest_per_os = defaultdict(lambda: ("0.0.0", []))

    for entry in file_data:
        os_name = entry['platform']
        current_version = latest_per_os[os_name][0]
        new_version = entry['version']

        def version_key(v): return list(map(int, v.split(".")))
        if version_key(new_version) > version_key(current_version):
            latest_per_os[os_name] = (new_version, [entry])
        elif new_version == current_version:
            latest_per_os[os_name][1].append(entry)

    return [file for _, files in latest_per_os.values() for file in files]

def main():
    file_data = extract_file_info()
    latest_files = find_latest_by_os(file_data)

    os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)
    with open(OUTPUT_PATH, "w") as f:
        json.dump(latest_files, f, indent=4)

    print(f"✅ Saved {len(latest_files)} latest Cyberduck download entries to: {OUTPUT_PATH}")

if __name__ == "__main__":
    main()
