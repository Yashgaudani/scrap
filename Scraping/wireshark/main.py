from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import json
import os
import time

base_urls = {
    "Windows": "https://2.na.dl.wireshark.org/win64/",
    "macOS": "https://2.na.dl.wireshark.org/osx/"
}

results = []

# Setup headless Chrome
options = Options()
options.add_argument("--headless=new")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")
driver = webdriver.Chrome(options=options)

try:
    for platform, url in base_urls.items():
        print(f"Opening {platform} page...")
        driver.get(url)
        time.sleep(2)  # wait for page to load (adjust if needed)

        links = driver.find_elements(By.TAG_NAME, "a")
        for link in links:
            href = link.get_attribute("href")
            if not href:
                continue

            fname = href.split("/")[-1]
            if "latest" in fname.lower() and fname.lower().endswith((".exe", ".msi", ".dmg")):
                results.append({
                    "product": "Wireshark",
                    "version": "latest",
                    "text": fname,
                    "url": href,
                    "platform": platform
                })

finally:
    driver.quit()

# Save to JSON
output_dir = "/home/yash-gaudani/R%D/patch/Scraping/wireshark"
os.makedirs(output_dir, exist_ok=True)
output_file = os.path.join(output_dir, "wireshark_latest_downloads.json")

with open(output_file, "w") as f:
    json.dump(results, f, indent=4)

# Print summary
print(f"Saved {len(results)} entries to {output_file}")
for r in results:
    print(f"{r['platform']}: {r['url']}")
