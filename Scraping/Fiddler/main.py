import requests
import json
from pathlib import Path

def get_latest_fiddler_version():
    """Fetch latest Fiddler Everywhere version from GitHub release-notes.json."""
    url = "https://api.github.com/repos/telerik/fiddler-everywhere-docs/contents/release-notes/release-notes.json"
    headers = {"Accept": "application/vnd.github.v3.raw"}  # Required to get raw content

    response = requests.get(url, headers=headers, timeout=10)
    if response.status_code == 200:
        data = response.json()
        versions = [entry["version"] for entry in data if "version" in entry]
        if versions:
            return versions[0]  # Latest version is the first item
    raise Exception("❌ No versions found. Check URL or format.")

def scrape_fiddler():
    """Scrape Fiddler Everywhere download links."""
    print("🔍 Fetching Fiddler Everywhere download information...")

    try:
        latest_version = get_latest_fiddler_version()
    except Exception as e:
        print(f"⚠️ Failed to fetch version. Using fallback. Error: {e}")
        latest_version = "5.0.0"

    print(f"📦 Using Fiddler Everywhere version: {latest_version}")
    
    formatted_data = {
        "product": "fiddler",
        "version": latest_version,
        "text": "Fiddler Everywhere",
        "platforms": {
            "windows": f"https://downloads.getfiddler.com/win/Fiddler%20Everywhere%20{latest_version}.exe",
            "mac_intel": f"https://downloads.getfiddler.com/mac/Fiddler%20Everywhere%20{latest_version}.dmg",
            "mac_arm64": f"https://downloads.getfiddler.com/mac-arm64/Fiddler%20Everywhere%20{latest_version}.dmg",
            "linux": f"https://downloads.getfiddler.com/linux/fiddler-everywhere-{latest_version}.AppImage"
        }
    }

    output_path = Path("/home/yash-gaudani/R%D/patch/Scraping/Fiddler/fiddler_info.json")
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(formatted_data, f, indent=2, ensure_ascii=False)

    print(f"✅ Fiddler Everywhere data saved to: {output_path}")
    return formatted_data

def main():
    try:
        scrape_fiddler()
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    main()
