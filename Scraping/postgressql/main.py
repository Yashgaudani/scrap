import requests
from bs4 import BeautifulSoup
import re
import json
import os

# ====== Config ======
base_url = "https://www.postgresql.org/ftp/source/"
headers = {"User-Agent": "Mozilla/5.0"}
save_path = "/home/yash-gaudani/R%D/patch/Scraping/postgressql"
output_file = os.path.join(save_path, "postgresql_latest.json")

# ====== Utility to resolve EDB URLs ======
def resolve_final_url(edb_url):
    try:
        response = requests.head(edb_url, allow_redirects=True)
        final_url = response.url
        content_type = response.headers.get('Content-Type', '')
        content_disp = response.headers.get('Content-Disposition', '')
        filename = None

        if 'filename=' in content_disp:
            filename = content_disp.split("filename=")[-1].strip('"')
        elif '/' in final_url:
            filename = final_url.split('/')[-1]

        version_match = re.search(r"(\d+\.\d+)", filename or "")
        version = version_match.group(1) if version_match else "unknown"

        return {
            "product": "postgresql",
            "file_name": filename,
            "version": version,
            "download_url": final_url,
            "platform": detect_platform(filename)
        }
    except Exception as e:
        return {"error": str(e), "original_url": edb_url}

# ====== Platform detection helper ======
def detect_platform(filename):
    if not filename:
        return "Unknown"
    lower = filename.lower()
    if ".exe" in lower or ".msi" in lower:
        return "Windows"
    elif ".dmg" in lower or "mac" in lower:
        return "macOS"
    elif ".rpm" in lower or ".deb" in lower or ".tar" in lower:
        return "Linux"
    else:
        return "Unknown"

# ====== Step 1: Scrape official source files ======
def fetch_source_tarballs():
    response = requests.get(base_url, headers=headers)
    soup = BeautifulSoup(response.text, "html.parser")

    version_folders = []
    for link in soup.find_all("a", href=True):
        folder = link["href"].strip('/')
        if re.fullmatch(r"v17\.\d+", folder) and "beta" not in folder and "rc" not in folder:
            version_folders.append(folder)

    if not version_folders:
        print("❌ No valid v17.x versions found.")
        return []

    latest_version = sorted(version_folders, key=lambda v: list(map(int, v[1:].split('.'))))[-1]
    print(f"✅ Found latest stable v17 version: {latest_version}")

    version_url = f"{base_url}{latest_version}/"
    response = requests.get(version_url, headers=headers)
    soup = BeautifulSoup(response.text, "html.parser")

    file_patterns = [
        r"postgresql-\d+\.\d+\.tar\.(gz|bz2|xz)",         # source tar
        r"postgresql-\d+\.\d+-docs\.tar\.gz",             # docs
    ]

    results = []
    for link in soup.find_all("a", href=True):
        text = link.text.strip()
        href = link["href"].strip()

        for pattern in file_patterns:
            if re.fullmatch(pattern, text):
                version_match = re.search(r"postgresql-(\d+\.\d+)", text)
                if version_match:
                    version = version_match.group(1)
                    file_url = f"https://ftp.postgresql.org/pub/source/{latest_version}/{text}"
                    results.append({
                        "product": "postgresql",
                        "file_name": text,
                        "version": version,
                        "download_url": file_url,
                        "platform": "Linux"
                    })
    return results

# ====== Step 2: EDB redirect-based links ======
def fetch_enterprisedb_links():
    edb_urls = [
        "https://sbp.enterprisedb.com/getfile.jsp?fileid=1259560",
        "https://sbp.enterprisedb.com/getfile.jsp?fileid=1259622"
        # ➕ Add more if needed
    ]

    results = []
    for url in edb_urls:
        resolved = resolve_final_url(url)
        if 'error' not in resolved:
            print(f"✅ EDB link resolved: {resolved['file_name']}")
            results.append(resolved)
        else:
            print(f"❌ Failed: {url} — {resolved['error']}")
    return results

# ====== Step 3: Run everything and save ======
def main():
    os.makedirs(save_path, exist_ok=True)

    source_results = fetch_source_tarballs()
    edb_results = fetch_enterprisedb_links()

    all_results = source_results + edb_results

    with open(output_file, "w") as f:
        json.dump(all_results, f, indent=4)

    print(f"\n📝 JSON saved to: {output_file}")

if __name__ == "__main__":
    main()
