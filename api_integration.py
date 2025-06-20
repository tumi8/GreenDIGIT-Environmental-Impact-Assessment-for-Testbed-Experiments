"""Communicate with SoBigData API"""
import json
import os
import requests
from rocrate.rocrate import ROCrate

# === CONFIG ===
BEARER_TOKEN = os.environ["SO_BIG_DATA"]
GCAT_PUBLISH_URL = "https://api.d4science.org/gcat/items"
PUBLIC_ZIP_URL = "https://data.d4science.net/2WMA"
TIMEOUT = 10


def extract_gcat_metadata(crate_path: str,
                          uploaded_file_url: str) -> dict:
    """Extract gCat metadata from RO-Crate."""
    crate = ROCrate(crate_path)
    dataset = crate.dereference("./")

    name = dataset.get("name", "unnamed-dataset").lower().replace(" ", "-")
    title = dataset.get("name", "")
    notes = dataset.get("description", "")
    keywords = dataset.get("keywords", [])

    creators = crate.get_by_type("Person")
    creator = next(
        (c for c in creators if "author" in c.get("tags", [])), None
    )
    creator_name = creator.get("name", "") if creator else ""
    creator_email = (
        creator.get("email", "") if creator and "email" in creator
        else "kilian.warmuth@tum.de"
    )

    tags = [{"name": kw} for kw in keywords]
    resources = [{
        "name": "RO-Crate ZIP Archive",
        "url": uploaded_file_url,
        "format": "zip"
    }]

    extras = [
        {"key": "Creation Date", "value": "2025-06-13"},
        {"key": "Creator", "value": creator_name},
        {"key": "Creator Email", "value": creator_email},
        {"key": "Creator Name PI (Principal Investigator)",
         "value": creator_name},
        {"key": "Environment OS", "value": "Linux"},
        {"key": "Environment Platform", "value": "D4Science GreenDIGIT"},
        {"key": "Experiment Dependencies", "value": "none"},
        {"key": "Experiment ID", "value": "exp-green-digit-001"},
        {"key": "GreenDIGIT Node", "value": "D4Science Pisa"},
        {"key": "Programming Language", "value": "Python"},
        {"key": "Project ID", "value": "GD-T5.2"},
        {"key": "Session reading metrics", "value": "enabled"},
        {"key": "system:type", "value": "Experiment"}
    ]

    return {
        "name": name,
        "title": title,
        "license_id": "CC-BY-4.0",
        "private": False,
        "notes": notes,
        "url": None,
        "tags": tags,
        "resources": resources,
        "extras": extras
    }


def publish_to_gcat(entry: dict, token: str) -> dict:
    """Publish metadata to gCat catalogue."""
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    resp = requests.post(
        GCAT_PUBLISH_URL, headers=headers, json=entry, timeout=TIMEOUT
    )
    if resp.status_code in (200, 201):
        return resp.json()
    raise RuntimeError(
        f"gCat publish failed: {resp.status_code}\n{resp.text}"
    )


def main():
    """Extract + publish only (manual ZIP upload assumed)."""
    crate_folder = "./result_folder_examples/2025-04-25_17-04-08_154131"
    zip_url = PUBLIC_ZIP_URL
    token = BEARER_TOKEN

    print("Extracting metadata...")
    entry = extract_gcat_metadata(crate_folder, zip_url)
    print(json.dumps(entry, indent=2))

    print("Publishing to gCat...")
    result = publish_to_gcat(entry, token)
    print("Published successfully:")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
