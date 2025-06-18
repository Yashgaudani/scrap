import requests
from bs4 import BeautifulSoup
import os
import json
from packaging.version import Version
from pathlib import Path

def scrape_gimp():
    """Scrape GIMP download information."""
    print("🔍 Fetching GIMP download information...")
    
    # Configuration
    base_url = "https://download.gimp.org/gimp/v3.0/"
    platform_dirs = {
        "Windows": "windows/",
        "macOS": "macos/",
        "Linux": "linux/"
    }

    results = []

    try:
        # Step 1: Loop through platform folders
        for platform, subdir in platform_dirs.items():
            url = base_url + subdir
            res = requests.get(url, timeout=10)
            res.raise_for_status()
            soup = BeautifulSoup(res.text, 'html.parser')
            
            for link in soup.find_all('a'):
                filename = link.get('href')
                if not filename or not filename.lower().endswith(('.exe', '.dmg', '.appimage')):
                    continue

                # Extract version from filename
                parts = filename.replace('-', '.').replace('_', '.').split('.')
                version_candidates = [p for p in parts if p.replace('v', '').replace('RC', '').isdigit()]
                if version_candidates:
                    version = None
                    for i in range(len(parts)):
                        try:
                            # Try forming a version number from chunks
                            version = Version(".".join(parts[i:i+3]).strip("-"))
                            break
                        except:
                            continue
                    if version:
                        results.append({
                            "product": "GIMP",
                            "version": str(version),
                            "text": filename,
                            "url": url + filename,
                            "platform": platform
                        })

        # Step 2: Filter only latest version
        if results:
            all_versions = {r["version"] for r in results}
            latest_version = max(all_versions, key=Version)
            print(f"✅ Keeping only latest version: {latest_version}")

            results = [r for r in results if r["version"] == latest_version]
        else:
            print("⚠️ No results found.")
            latest_version = "unknown"

        # Save to the expected location for the orchestrator
        output_path = Path(__file__).parent.parent / "gimp_info.json"
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(results, f, indent=2, ensure_ascii=False)

        print(f"✅ Saved GIMP {latest_version} download links to: {output_path}")
        return results
        
    except Exception as e:
        print(f"❌ Error fetching GIMP data: {e}")
        return []

def main():
    """Main function for standalone execution."""
    try:
        scrape_gimp()
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    main()
