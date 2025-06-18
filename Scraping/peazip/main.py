import requests
import json
import os
import re
from pathlib import Path

def scrape_peazip():
    """Scrape PeaZip download information."""
    print("🔍 Fetching PeaZip download information...")
    
    # Config
    target_tag = "10.5.0"  # You can make this dynamic if needed
    api_url = f"https://api.github.com/repos/peazip/PeaZip/releases/tags/{target_tag}"

    # Platform matchers
    platform_keywords = {
        "DARWIN.aarch64.dmg": "macOS (aarch64)",
        "DARWIN.x86_64.dmg": "macOS (Intel)",
        "WIN64.exe": "Windows x64",
        "WINDOWS.exe": "Windows x86",
        "LINUX.GTK2.x86_64.tar.gz": "Linux (x86_64 portable)",
        "LINUX.GTK2.aarch64.tar.gz": "Linux (aarch64 portable)"
    }

    try:
        # Fetch from GitHub API
        headers = {"Accept": "application/vnd.github.v3+json"}
        res = requests.get(api_url, headers=headers, timeout=10)
        if res.status_code != 200:
            raise Exception(f"❌ GitHub API Error: {res.status_code} - {res.text}")
        release_data = res.json()

        # Parse assets
        results = []
        for asset in release_data.get("assets", []):
            filename = asset.get("name", "")
            download_url = asset.get("browser_download_url", "")

            # Extract version from filename
            version_match = re.search(r'(\d+\.\d+\.\d+)', filename)
            if not version_match:
                continue
            version = version_match.group(1)

            for key, platform in platform_keywords.items():
                if key in filename:
                    results.append({
                        "product": "PeaZip",
                        "version": version,
                        "text": filename,
                        "url": download_url,
                        "platform": platform
                    })

        # Save to the expected location for the orchestrator
        output_path = Path(__file__).parent.parent / "peazip_info.json"
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(results, f, indent=2, ensure_ascii=False)

        print(f"✅ Saved PeaZip versioned download links to: {output_path}")
        return results
        
    except Exception as e:
        print(f"❌ Error fetching PeaZip data: {e}")
        return []

def main():
    """Main function for standalone execution."""
    try:
        scrape_peazip()
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    main()
