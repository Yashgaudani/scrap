import requests
import json
import os
import re
from urllib.parse import urlparse

# ==============================
# CONFIG
# ==============================
OUTPUT_PATH = "/home/yash-gaudani/R%D/patch/Scraping/vscode/vscode_links.json"
TIMEOUT = 25
BUILD = "stable"  # or "insider"

HEADERS = {
    "User-Agent": "Mozilla/5.0 (compatible; VSCodeLinkCollector/1.0)"
}

# Requested matrix of artifacts
OS_TOKENS = [
    # --- Windows: System installers ---
    "win32-x64",
    "win32-arm64",

    # --- Windows: User installers ---
    "win32-x64-user",
    "win32-arm64-user",

    # --- Windows: .zip (archives) ---
    "win32-x64-archive",
    "win32-arm64-archive",

    # --- Windows: CLI ---
    "cli-win32-x64",
    "cli-win32-arm64",

    # --- Linux: .deb ---
    "linux-deb-x64",
    "linux-deb-armhf",   # Arm32
    "linux-deb-arm64",

    # --- Linux: .rpm ---
    "linux-rpm-x64",
    "linux-rpm-armhf",   # Arm32
    "linux-rpm-arm64",

    # --- Linux: .tar.gz (archives) ---
    "linux-x64",
    "linux-armhf",       # Arm32
    "linux-arm64",

    # --- Linux: CLI ---
    "cli-linux-x64",
    "cli-linux-armhf",
    "cli-linux-arm64",

    # --- macOS: .zip ---
    "darwin-x64",        # Intel
    "darwin-arm64",      # Apple silicon
    "darwin-universal",  # Universal

    # --- macOS: CLI ---
    "cli-darwin-x64",
    "cli-darwin-arm64",
]

# Optional: Snap entry (no direct file URL)
SNAP_RECORD = {
    "platform": "linux",
    "product": "vscode",
    "version": "store-channel",
    "filename": "snap-store",
    "url": "https://snapcraft.io/code",
    "_meta": {
        "quality": BUILD,
        "installer_type": "store",
        "note": "Install from Snap Store (no direct file download URL)."
    }
}

# ==============================
# HELPERS
# ==============================
VERSION_IN_NAME = re.compile(r"[-_]((?:\d+\.){2}\d+)(?:[-_.]|$)", re.IGNORECASE)

def follow_redirects(url: str) -> tuple[str, dict, int]:
    """Return (final_url, headers, status_code). Try HEAD, fallback to GET."""
    try:
        r = requests.head(url, allow_redirects=True, timeout=TIMEOUT, headers=HEADERS)
        # Fallback to GET if HEAD is insufficient
        if r.status_code >= 400 or (not r.headers.get("Content-Length") and r.url == url):
            r = requests.get(url, allow_redirects=True, timeout=TIMEOUT, headers=HEADERS, stream=False)
        return r.url, dict(r.headers), r.status_code
    except requests.RequestException:
        try:
            r = requests.get(url, allow_redirects=True, timeout=TIMEOUT, headers=HEADERS, stream=False)
            return r.url, dict(r.headers), r.status_code
        except requests.RequestException:
            return url, {}, 0

def filename_from_url(u: str) -> str | None:
    path = urlparse(u).path
    return path.split("/")[-1] if "/" in path else None

def version_from_name(name: str | None) -> str | None:
    if not name:
        return None
    m = VERSION_IN_NAME.search(name)
    return m.group(1) if m else None

def platform_of(os_token: str) -> str:
    t = os_token.lower()
    if t.startswith("win32") or t.startswith("cli-win32"):
        return "win"
    if t.startswith("darwin") or t.startswith("cli-darwin"):
        return "mac"
    return "linux"

def infer_installer_type(os_token: str) -> str | None:
    """Tag entries as user/system/portable/package/store where applicable."""
    t = os_token.lower()
    # Windows
    if t.endswith("-user"):
        return "user"
    if t.endswith("-system") or t in ("win32-x64", "win32-arm64"):
        return "system"
    if "archive" in t or t.startswith("cli-"):
        return "portable"  # zip/cli artifacts
    # macOS & Linux packages/archives
    if t.startswith("darwin"):
        return "package"   # mac zip
    if "deb" in t or "rpm" in t or t.startswith("linux-"):
        return "package"   # linux packages & tar.gz
    return None

def build_record(os_token: str, build: str = BUILD) -> dict:
    sha_url = f"https://code.visualstudio.com/sha/download?build={build}&os={os_token}"
    final_url, headers, status = follow_redirects(sha_url)

    cdn_name = filename_from_url(final_url)
    version = version_from_name(cdn_name) or "unknown"

    record = {
        "platform": platform_of(os_token),
        "product": "vscode",
        "version": version,
        "filename": os_token,
        "url": final_url
    }

    meta = {
        "quality": build,
        "status_code": status,
        "installer_type": infer_installer_type(os_token)
    }
    if headers.get("Content-Length"):
        meta["content_length"] = headers["Content-Length"]
    if headers.get("Content-Type"):
        meta["content_type"] = headers["Content-Type"]
    if cdn_name:
        meta["cdn_filename"] = cdn_name

    record["_meta"] = meta
    return record

# ==============================
# MAIN
# ==============================
if __name__ == "__main__":
    results = []

    for token in OS_TOKENS:
        results.append(build_record(token, build=BUILD))

    # Add Snap logical record
    results.append(SNAP_RECORD)

    os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)
    with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2, ensure_ascii=False)

    print(f"✅ JSON saved to: {OUTPUT_PATH}")
    print(f"🔢 Total links captured: {len(results)}")
