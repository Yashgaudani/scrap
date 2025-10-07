import requests
from bs4 import BeautifulSoup
import re
import json
import os

# URLs to scrape
URLS = {
    "Linux": "https://1password.com/downloads/linux",
    "macOS": "https://1password.com/downloads/mac",
    "Windows": "https://1password.com/downloads/windows"
}

# Output file path
OUTPUT_PATH = "/home/yash-gaudani/R%D/patch/Scraping/1password/1password.json"

# Store results
results = []

def extract_filename(url):
    return url.split("/")[-1]

def extract_arch_and_platform(file_name):
    if file_name.endswith(".deb") or file_name.endswith(".rpm"):
        return "Linux", "x64" if "x64" in file_name or "amd64" in file_name else "aarch64"
    elif file_name.endswith(".exe") or "windows" in file_name.lower():
        return "Windows", "x64"
    elif file_name.endswith(".pkg") or ".zip" in file_name or "mac" in file_name.lower():
        if "arm" in file_name.lower():
            return "macOS", "arm64"
        else:
            return "macOS", "x64"
    return "Unknown", "Unknown"

def get_version_from_filename(file_name):
    match = re.search(r"(\d+\.\d+\.\d+)", file_name)
    return match.group(1) if match else "latest"

for platform, url in URLS.items():
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")

    for link in soup.find_all("a", href=True):
        href = link["href"]
        if any(ext in href for ext in [".deb", ".rpm", ".pkg", ".exe", ".zip"]):
            full_url = href if href.startswith("http") else "https://downloads.1password.com" + href
            file_name = extract_filename(full_url)
            platform_detected, arch = extract_arch_and_platform(file_name)
            version = get_version_from_filename(file_name)

            results.append({
                "product": "1Password",
                "version": version,
                "file_name": file_name,
                "url": full_url,
                "platform": platform_detected,
                "architecture": arch
            })

# Write JSON output
os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)
with open(OUTPUT_PATH, "w") as f:
    json.dump(results, f, indent=2)

print(f"Saved {len(results)} records to {OUTPUT_PATH}")
