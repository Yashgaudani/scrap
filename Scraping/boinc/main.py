import requests
from bs4 import BeautifulSoup
import re
import json
import os
from urllib.parse import urljoin
from packaging.version import Version

# Constants
BOINC_DL_URL = "https://boinc.berkeley.edu/dl/"
GITHUB_API_URL = "https://api.github.com/repos/BOINC/boinc/releases"
OUTPUT_PATH = "/home/yash-gaudani/R%D/patch/Scraping/boinc/boinc.json"
PRODUCT = "BOINC"

# Platform detection
PLATFORM_EXTENSIONS = {
    "Windows": [".exe", ".msi"],
    "macOS": [".dmg", ".pkg"],
    "Linux": [".deb", ".rpm", ".sh", ".tar.gz"]
}

def detect_platform_arch(filename):
    for platform, extensions in PLATFORM_EXTENSIONS.items():
        if any(filename.endswith(ext) for ext in extensions):
            return platform, "x64"
    return "Unknown", "Unknown"

output = []

# ---- GitHub (Windows/Linux) ----
github_resp = requests.get(GITHUB_API_URL)
github_data = github_resp.json()

valid_releases = [rel for rel in github_data if rel.get("assets")]
versions = []

for release in valid_releases:
    tag = release.get("tag_name", "")
    match = re.search(r"(\d+\.\d+\.\d+)", tag)  # ✅ FIXED REGEX
    if match:
        versions.append(match.group(1))

if not versions:
    raise Exception("No versions found from GitHub.")

latest_version = str(max(Version(v) for v in versions))

# Find the corresponding release
latest_release = next(
    rel for rel in valid_releases
    if latest_version in rel.get("tag_name", "")
)

for asset in latest_release.get("assets", []):
    name = asset["name"]
    if name.endswith(".apk"):
        continue
    if not any(name.endswith(ext) for ext_list in PLATFORM_EXTENSIONS.values() for ext in ext_list):
        continue
    platform, arch = detect_platform_arch(name)
    output.append({
        "product": PRODUCT,
        "version": latest_version,
        "file_name": name,
        "url": asset["browser_download_url"],
        "platform": platform,
        "architecture": arch
    })

# ---- BOINC Website (macOS only) ----
resp = requests.get(BOINC_DL_URL)
soup = BeautifulSoup(resp.text, "html.parser")
links = [a['href'] for a in soup.find_all("a", href=True)]

mac_files = [
    f for f in links
    if any(f.endswith(ext) for ext in PLATFORM_EXTENSIONS["macOS"])
    and latest_version in f
    and not f.endswith(".apk")
]

for fname in mac_files:
    platform, arch = detect_platform_arch(fname)
    output.append({
        "product": PRODUCT,
        "version": latest_version,
        "file_name": fname,
        "url": urljoin(BOINC_DL_URL, fname),
        "platform": platform,
        "architecture": arch
    })

# ---- Save JSON ----
os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)
with open(OUTPUT_PATH, "w") as f:
    json.dump(output, f, indent=2)

print(f"Saved {len(output)} entries to {OUTPUT_PATH}")
