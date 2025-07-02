import re
import json
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time

# --- Headless browser setup ---
options = Options()
options.add_argument("--headless=new")
driver = webdriver.Chrome(options=options)

driver.get("https://www.enterprisedb.com/downloads/postgres-postgresql-downloads")
time.sleep(5)
html = driver.page_source
driver.quit()

# --- Try to extract JSON with URLs ---
pattern = r"https:\/\/get\.enterprisedb\.com\/postgresql\/[^\"]+"
matches = re.findall(pattern, html)

# Deduplicate and format
unique_links = sorted(set(matches))
data = [{"url": url, "file": url.split('/')[-1]} for url in unique_links]

# Save result
with open("edb_file_links.json", "w") as f:
    json.dump(data, f, indent=2)

print(f"✅ Extracted {len(data)} download links.")
