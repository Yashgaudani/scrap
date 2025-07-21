import requests
from bs4 import BeautifulSoup
import re
import json
import os

BASE_URL = "https://download.blender.org/release/"
PRODUCT_NAME = "Blender"
OUTPUT_PATH = "/home/yash-gaudani/R%D/patch/Scraping/Blender/blender_downloads.json"

IGNORE_PATTERNS = re.compile(r"(beta|alpha|rc)", re.IGNORECASE)
ARCHITECTURE_PATTERN = re.compile(r"(x64|x86|arm64|aarch64|intel)", re.IGNORECASE)

PLATFORM_EXTENSIONS = {
    "Windows": (".msi", ".zip", ".exe"),
    "macOS": (".dmg",),
    "Linux": (".tar.xz", ".tar.bz2"),
}


def infer_platform_and_architecture(file_name):
    platform = None
    architecture = "Unknown"

    for key, exts in PLATFORM_EXTENSIONS.items():
        if file_name.endswith(exts):
            platform = key
            break

    match = ARCHITECTURE_PATTERN.search(file_name)
    if match:
        architecture = match.group(1).lower()

    return platform, architecture


def get_latest_version_folder():
    res = requests.get(BASE_URL)
    res.raise_for_status()
    soup = BeautifulSoup(res.text, "html.parser")

    version_dirs = []
    for link in soup.find_all("a", href=True):
        href = link["href"]
        if re.match(r"Blender\d+\.\d+/?", href):
            version_str = href.strip("/").replace("Blender", "")
            try:
                version_parts = list(map(int, version_str.split(".")))
                version_dirs.append((version_parts, version_str, href))
            except ValueError:
                continue  # skip folders like Blender2.27-newpy/

    if not version_dirs:
        raise Exception("No valid version folders found.")

    # Sort by version number (descending)
    version_dirs.sort(reverse=True)
    latest_version_str = version_dirs[0][1]
    latest_href = version_dirs[0][2]
    return BASE_URL + latest_href, latest_version_str


def fetch_files(version_url, version_number):
    res = requests.get(version_url)
    res.raise_for_status()
    soup = BeautifulSoup(res.text, "html.parser")

    entries = []

    for link in soup.find_all("a", href=True):
        file_name = link["href"]

        # Skip unwanted/beta/alpha/rc files
        if IGNORE_PATTERNS.search(file_name):
            continue

        platform, architecture = infer_platform_and_architecture(file_name)
        if not platform:
            continue

        download_url = version_url + file_name

        entry = {
            "product": PRODUCT_NAME,
            "version": f"{version_number}",
            "file_name": file_name,
            "url": download_url,
            "platform": platform,
            "architecture": architecture
        }

        entries.append(entry)

    return entries


def main():
    try:
        version_url, version_number = get_latest_version_folder()
        files = fetch_files(version_url, version_number)

        # Ensure the output directory exists
        os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)

        # Save to JSON
        with open(OUTPUT_PATH, "w") as f:
            json.dump(files, f, indent=2)

        print(f"✅ JSON saved to: {OUTPUT_PATH}")
    except Exception as e:
        print(f"❌ Error: {e}")


if __name__ == "__main__":
    main()
