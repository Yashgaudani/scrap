import requests
from bs4 import BeautifulSoup
import json
import os
from pathlib import Path

def scrape_git():
    """Scrape Git for Windows download information."""
    print("🔍 Fetching Git for Windows download information...")
    
    # ---- Configuration ----
    BASE_URL = "https://github.com"
    RELEASES_URL = "https://github.com/git-for-windows/git/releases"
    HEADERS = {"User-Agent": "Mozilla/5.0"}
    PRODUCT = "Git for Windows"

    try:
        # ---- Step 1: Get Latest Version URL ----
        response = requests.get(RELEASES_URL, headers=HEADERS, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, "html.parser")

        latest_label = soup.find("span", string="Latest")
        if not latest_label:
            raise Exception("❌ Latest release label not found.")

        parent = latest_label.find_parent("div")
        release_link_tag = parent.find("a", href=True)
        if not release_link_tag:
            raise Exception("❌ Release link not found.")

        latest_version_href = release_link_tag["href"]
        latest_version_text = release_link_tag.get_text(strip=True)
        version = latest_version_href.split("/")[-1]
        expanded_assets_url = f"{BASE_URL}/git-for-windows/git/releases/expanded_assets/{version}"

        print(f"🔄 Latest Version: {version}")
        print(f"🔗 URL: {expanded_assets_url}")

        # ---- Step 2: Scrape Downloadable Assets ----
        response = requests.get(expanded_assets_url, headers=HEADERS, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")

        data = []

        for a in soup.find_all("a", href=True):
            href = a["href"]
            text = a.text.strip()
            
            if not href.endswith((".exe", ".zip", ".7z.exe", ".tar.bz2", ".tar.gz", ".tar.xz")):
                continue

            file_name = href.split("/")[-1]
            full_url = BASE_URL + href if href.startswith("/") else href

            if "64" in file_name or "x64" in file_name:
                platform = "Windows 64-bit"
            elif "32" in file_name or "x86" in file_name:
                platform = "Windows 32-bit"
            elif "arm64" in file_name:
                platform = "Windows ARM64"
            else:
                platform = "Unknown"

            entry = {
                "product": PRODUCT,
                "file_name": file_name,
                "version": version,
                "text": text or "Download",
                "url": full_url,
                "platform": platform
            }

            data.append(entry)

        # Save to the expected location for the orchestrator
        output_path = Path("/home/yash-gaudani/R%D/patch/Scraping/git/git_info.json")
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)

        print(f"✅ Download data saved to: {output_path}")
        return data
        
    except Exception as e:
        print(f"❌ Error fetching Git data: {e}")
        return []

def main():
    """Main function for standalone execution."""
    try:
        scrape_git()
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    main()
