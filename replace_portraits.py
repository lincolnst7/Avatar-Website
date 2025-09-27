import json
import os
import re
from urllib.parse import urlparse

# Input JSON file (with Fandom image URLs or "../images/... paths")
INPUT_FILE = "database/avatar_characters_updated.json"

# Output JSON file (with browser-friendly relative paths)
OUTPUT_FILE = "database/avatar_characters_local.json"

# Folder where images are stored (absolute on disk)
IMAGE_DIR = os.path.join("images", "characters")

# Relative path to use in the JSON (relative to your HTML root)
RELATIVE_DIR = "images/characters"

# Load JSON
with open(INPUT_FILE, "r", encoding="utf-8") as f:
    data = json.load(f)

for char in data:
    name = char.get("Name")
    img_url = char.get("Image")

    if not img_url or img_url == "IMAGE_URL_HERE":
        # No image → leave blank
        char["Image"] = ""
        continue

    # Sanitize filename to match your downloaded files
    safe_name = re.sub(r"[^a-zA-Z0-9]", "_", name)

    # Preserve original extension
    parsed = urlparse(img_url)
    _, ext = os.path.splitext(parsed.path)
    if not ext:
        ext = ".jpg"  # fallback if URL had no extension

    filename = f"{safe_name}{ext}"
    abs_path = os.path.join(IMAGE_DIR, filename)
    rel_path = f"{RELATIVE_DIR}/{filename}".replace("\\", "/")

    if os.path.exists(abs_path):
        char["Image"] = rel_path
    else:
        char["Image"] = ""

# Save updated JSON
with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
    json.dump(data, f, indent=2, ensure_ascii=False)

print(f"\n✅ Done! Localized JSON saved as {OUTPUT_FILE}")
