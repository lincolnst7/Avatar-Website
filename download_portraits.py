import json
import os
import re
import requests
from urllib.parse import urlparse

# Input JSON file (with updated Image URLs)
INPUT_FILE = "database/avatar_characters_updated.json"

# Output folder for images
OUTPUT_DIR = "images/characters"

# Make sure the output folder exists
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Load JSON
with open(INPUT_FILE, "r", encoding="utf-8") as f:
    data = json.load(f)

for char in data:
    img_url = char.get("Image")
    name = char.get("Name")

    if not img_url or img_url == "IMAGE_URL_HERE":
        print(f"Skipping {name} (no image).")
        continue

    # Clean the filename: replace spaces/punctuation with underscores
    safe_name = re.sub(r"[^a-zA-Z0-9]", "_", name)

    # Extract extension from URL
    parsed = urlparse(img_url)
    _, ext = os.path.splitext(parsed.path)
    if not ext:  # fallback if URL has no extension
        ext = ".jpg"

    filename = f"{safe_name}{ext}"
    filepath = os.path.join(OUTPUT_DIR, filename)

    # Skip if already downloaded
    if os.path.exists(filepath):
        print(f"Already downloaded: {filename}")
        continue

    try:
        print(f"Downloading {name} → {filename}")
        res = requests.get(img_url, stream=True, headers={"User-Agent": "Mozilla/5.0"})
        res.raise_for_status()

        with open(filepath, "wb") as img_file:
            for chunk in res.iter_content(8192):
                img_file.write(chunk)

    except Exception as e:
        print(f"❌ Failed to download {img_url} for {name}: {e}")

print("\n✅ Done! All images saved in:", OUTPUT_DIR)
