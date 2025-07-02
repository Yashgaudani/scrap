import requests
from bs4 import BeautifulSoup

import json

url = "https://ftp.iij.ad.jp/pub/db/mysql/Downloads/"
resp = requests.get(url)
soup = BeautifulSoup(resp.text, "html.parser")

records = []
for link in soup.select("a"):
    href = link.get("href")
    if href and href.endswith("/"):
        version = href.strip("/")
        version_url = url + href
        sub = BeautifulSoup(requests.get(version_url).text, "html.parser")
        for file_link in sub.select("a"):
            fn = file_link.get("href")
            if fn and fn.lower().endswith((".msi", ".zip", ".tar.gz", ".dmg")):
                arch = ""
                if "x64" in fn:
                    arch = "x64"
                elif "x86" in fn or "winx" in fn:
                    arch = "x86"
                elif "arm" in fn:
                    arch = "ARM64"

                os_type = "Windows" if fn.endswith((".msi", ".zip")) else "Linux/macOS"
                dtype = fn.split('.')[-1].upper()
                if fn.endswith(".tar.gz"):
                    dtype = "TAR.GZ"

                records.append({
                    "Version": version,
                    "OS": os_type,
                    "Architecture": arch,
                    "Edition": "Community",
                    "Download Type": dtype,
                    "Download Link": version_url + fn
                })

# Convert to JSON and print
json_output = json.dumps(records, indent=4)
print(json_output)
