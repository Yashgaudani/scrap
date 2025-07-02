import requests
import xml.etree.ElementTree as ET
from urllib.parse import urljoin

# Base S3 URL
base_url = "https://td-infra-prd-us-east-1-s3-atlaselectron.s3.amazonaws.com/"

# Fetch XML listing
response = requests.get(base_url)
response.raise_for_status()

# Parse XML
ns = {'s3': 'http://s3.amazonaws.com/doc/2006-03-01/'}
root = ET.fromstring(response.content)
keys = [elem.text for elem in root.findall(".//s3:Key", ns)]

# Find key containing 'latest.yml' (or just 'latest')
latest_keys = [key for key in keys if "latest" in key.lower() and key.lower().endswith(".yml")]

# Output full URL(s)
if latest_keys:
    print("🔍 Found 'latest' YAML files:\n")
    for key in latest_keys:
        print(urljoin(base_url, key))
else:
    print("❌ No 'latest.yml' file found.")
