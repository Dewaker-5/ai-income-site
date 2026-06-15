import os
import re
import json
from datetime import date
import requests

OWNER = "Dewaker-5"
REPO = "ai-income-site"
BRANCH = "main"
API_BASE = f"https://api.github.com/repos/{OWNER}/{REPO}/contents"

HEADERS = {
    "Authorization": f"Bearer {os.environ['GITHUB_TOKEN']}",
    "Accept": "application/vnd.github.v3+json",
}

def extract_title(md_content):
    match = re.search(r"^#\s+(.+)$", md_content, re.MULTILINE)
    return match.group(1).strip() if match else "Untitled"

def strip_existing_front_matter(content):
    if content.startswith("---"):
        parts = content.split("---", 2)
        if len(parts) == 3:
            return parts[2].lstrip("\n")
    return content

def build_jekyll_post(content):
    body = strip_existing_front_matter(content)
    title = extract_title(body)
    today = date.today().isoformat()
    front_matter = f"---\nlayout: default\ntitle: \"{title}\"\ndate: {today}\n---\n\n"
    return front_matter + body

def get_existing_sha(path):
    url = f"{API_BASE}/{path}?ref={BRANCH}"
    r = requests.get(url, headers=HEADERS)
    if r.status_code == 200:
        return r.json()["sha"]
    return None

def push_file(path, content):
    sha = get_existing_sha(path)
    data = {
        "message": f"Publish {path}",
        "content": content,
        "branch": BRANCH,
    }
    if sha:
        data["sha"] = sha
    r = requests.put(f"{API_BASE}/{path}", headers=HEADERS, json=data)
    return r.status_code in (200, 201)

def publish():
    articles_dir = "articles"
    if not os.path.isdir(articles_dir):
        print(f"Error: '{articles_dir}' folder not found.")
        return

    files = sorted(f for f in os.listdir(articles_dir) if f.endswith(".md"))
    if not files:
        print("No markdown files found in articles/.")
        return

    success = 0
    failed = 0

    for fname in files:
        path = os.path.join(articles_dir, fname)
        with open(path) as f:
            raw = f.read()

        jekyll_content = build_jekyll_post(raw)
        encoded = jekyll_content.encode("utf-8")
        b64 = __import__("base64").b64encode(encoded).decode()

        remote_path = f"posts/{fname}"
        if push_file(remote_path, b64):
            print(f"  Published: posts/{fname}")
            success += 1
        else:
            print(f"  FAILED: posts/{fname}")
            failed += 1

    print(f"\nSummary: {success} published, {failed} failed")

if __name__ == "__main__":
    publish()
