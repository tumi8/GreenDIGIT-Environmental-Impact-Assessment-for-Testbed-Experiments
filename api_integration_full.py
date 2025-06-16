"""Communicate with SoBigData API"""
import os
import json
import requests
from dotenv import load_dotenv
from rocrate.rocrate import ROCrate

load_dotenv()
BEARER_TOKEN = os.environ["SO_BIG_DATA"]
print(BEARER_TOKEN)
GCAT_PUBLISH_URL = "https://api.d4science.org/gcat/items"
WORKSPACE_API = "https://sobigdata.d4science.org/group/greendigit/workspace"
TIMEOUT = 10


def zip_rocrate(crate_path: str) -> str:
    """Zip RO-Crate to .zip archive."""
    crate = ROCrate(crate_path)
    zip_path = crate_path.rstrip("/") + ".zip"
    crate.write_zip(zip_path)
    return zip_path


def get_workspace_folder_id(token: str) -> str:
    """Get user's root Workspace folder ID."""
    headers = {"Authorization": f"Bearer {token}"}
    url = f"{WORKSPACE_API}/me"
    resp = requests.get(url, headers=headers, timeout=TIMEOUT)
    if resp.status_code != 200:
        raise RuntimeError(
            f"Failed to retrieve user info:\n{resp.text}"
        )
    return resp.json()["workspace"]["folderId"]


def upload_zip_to_workspace(zip_path: str, token: str) -> str:
    """Upload ZIP and return public Workspace URL."""
    folder_id = get_workspace_folder_id(token)
    upload_url = f"{WORKSPACE_API}/files/{folder_id}"
    headers = {"Authorization": f"Bearer {token}"}
    with open(zip_path, "rb") as f:
        files = {"file": f}
        resp = requests.post(
            upload_url, headers=headers, files=files, timeout=30
        )
    if resp.status_code != 200:
        raise RuntimeError(f"Upload failed:\n{resp.text}")
    return resp.json().get("publicUrl", resp.json().get("url"))


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
        creator.get("email", "") if creator and "email" in creator else ""
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
    if resp.status_code == 200:
        return resp.json()
    raise RuntimeError(
        f"gCat publish failed: {resp.status_code}\n{resp.text}"
    )


def main():
    """Run the GreenDIGIT ZIP + metadata publishing workflow."""
    crate_folder = "./result_folder_examples/2025-04-25_17-04-08_154131"
    token = BEARER_TOKEN

    print("Zipping RO-Crate...")
    zip_path = zip_rocrate(crate_folder)
    print(f"Zipped to: {zip_path}")

    print("Uploading ZIP to Workspace...")
    zip_url = upload_zip_to_workspace(zip_path, token)
    print(f"Uploaded to: {zip_url}")

    print("Extracting metadata...")
    entry = extract_gcat_metadata(crate_folder, zip_url)
    print(json.dumps(entry, indent=2))

    print("Publishing to gCat...")
    result = publish_to_gcat(entry, token)
    print("Published successfully:")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()