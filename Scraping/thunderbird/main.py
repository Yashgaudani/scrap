import requests
from bs4 import BeautifulSoup
import json
import urllib.parse
import os
from pathlib import Path

def scrape_thunderbird():
    """Scrape Thunderbird download information."""
    print("🔍 Fetching Thunderbird download information...")
    
    BASE_HOST = "https://download-installer.cdn.mozilla.net"
    BASE_PATH = "/pub/thunderbird/releases/"
    VERSION = "139.0.2"
    LANGUAGE = "uk"

    PLATFORMS = {
        "win64": "Windows 64-bit",
        "win32": "Windows 32-bit",
        "mac": "macOS",
        "linux-x86_64": "Linux 64-bit"
    }

    results = []

    for folder, platform_name in PLATFORMS.items():
        relative_path = f"{BASE_PATH}{VERSION}/{folder}/{LANGUAGE}/"
        full_url_path = urllib.parse.urljoin(BASE_HOST, relative_path)

        try:
            response = requests.get(full_url_path, timeout=10)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, "html.parser")

            for link in soup.find_all("a"):
                href = link.get("href")
                if href and not href.startswith("?") and not href.endswith("/"):
                    # ✅ Get only the file name (not the path)
                    file_name = os.path.basename(href.strip())
                    download_url = urllib.parse.urljoin(full_url_path, file_name)

                    results.append({
                        "product": "Thunderbird",
                        "version": VERSION,
                        "file_name": file_name,
                        "text": file_name,
                        "url": download_url,
                        "platform": platform_name
                    })

        except Exception as e:
            print(f"❌ Error accessing {full_url_path}: {e}")

    # Save to the expected location for the orchestrator
    output_path = Path(__file__).parent.parent / "thunderbird_info.json"
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2, ensure_ascii=False)

    print(f"✅ {len(results)} Thunderbird files saved to: {output_path}")
    return results

def main():
    """Main function for standalone execution."""
    try:
        scrape_thunderbird()
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    main()
