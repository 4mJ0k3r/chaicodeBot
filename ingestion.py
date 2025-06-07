# ingestion.py

import json
import requests
from bs4 import BeautifulSoup
from langchain.text_splitter import CharacterTextSplitter

# 1. List of all docs pages (manually maintained)
DOC_URLS = [
    "https://chaidocs.vercel.app/youtube/chai-aur-html/welcome/",
    "https://chaidocs.vercel.app/youtube/chai-aur-html/introduction/",
    "https://chaidocs.vercel.app/youtube/chai-aur-html/emmit-crash-course/",
    "https://chaidocs.vercel.app/youtube/chai-aur-html/html-tags/",
    "https://chaidocs.vercel.app/youtube/chai-aur-git/welcome/",
    "https://chaidocs.vercel.app/youtube/chai-aur-git/introduction/",
    "https://chaidocs.vercel.app/youtube/chai-aur-git/terminology/",
    "https://chaidocs.vercel.app/youtube/chai-aur-git/behind-the-scenes/",
    "https://chaidocs.vercel.app/youtube/chai-aur-git/branches/",
    "https://chaidocs.vercel.app/youtube/chai-aur-git/diff-stash-tags/",
    "https://chaidocs.vercel.app/youtube/chai-aur-git/managing-history/",
    "https://chaidocs.vercel.app/youtube/chai-aur-git/github/",
    "https://chaidocs.vercel.app/youtube/chai-aur-c/welcome/",
    "https://chaidocs.vercel.app/youtube/chai-aur-c/introduction/",
    "https://chaidocs.vercel.app/youtube/chai-aur-c/hello-world/",
    "https://chaidocs.vercel.app/youtube/chai-aur-c/variables-and-constants/",
    "https://chaidocs.vercel.app/youtube/chai-aur-c/data-types/",
    "https://chaidocs.vercel.app/youtube/chai-aur-c/operators/",
    "https://chaidocs.vercel.app/youtube/chai-aur-c/control-flow/",
    "https://chaidocs.vercel.app/youtube/chai-aur-c/loops/",
    "https://chaidocs.vercel.app/youtube/chai-aur-c/functions/",
    "https://chaidocs.vercel.app/youtube/chai-aur-django/welcome/",
    "https://chaidocs.vercel.app/youtube/chai-aur-django/getting-started/",
    "https://chaidocs.vercel.app/youtube/chai-aur-django/jinja-templates/",
    "https://chaidocs.vercel.app/youtube/chai-aur-django/tailwind/",
    "https://chaidocs.vercel.app/youtube/chai-aur-django/models/",
    "https://chaidocs.vercel.app/youtube/chai-aur-django/relationships-and-forms/",
    "https://chaidocs.vercel.app/youtube/chai-aur-sql/welcome/",
    "https://chaidocs.vercel.app/youtube/chai-aur-sql/introduction/",
    "https://chaidocs.vercel.app/youtube/chai-aur-sql/postgres/",
    "https://chaidocs.vercel.app/youtube/chai-aur-sql/normalization/",
    "https://chaidocs.vercel.app/youtube/chai-aur-sql/database-design-exercise/",
    "https://chaidocs.vercel.app/youtube/chai-aur-sql/joins-and-keys/",
    "https://chaidocs.vercel.app/youtube/chai-aur-sql/joins-exercise/",
    "https://chaidocs.vercel.app/youtube/chai-aur-devops/welcome/",
    "https://chaidocs.vercel.app/youtube/chai-aur-devops/setup-vpc/",
    "https://chaidocs.vercel.app/youtube/chai-aur-devops/setup-nginx/",
    "https://chaidocs.vercel.app/youtube/chai-aur-devops/nginx-rate-limiting/",
    "https://chaidocs.vercel.app/youtube/chai-aur-devops/nginx-ssl-setup/",
    "https://chaidocs.vercel.app/youtube/chai-aur-devops/node-nginx-vps/",
    "https://chaidocs.vercel.app/youtube/chai-aur-devops/postgresql-vps/",
    "https://chaidocs.vercel.app/youtube/chai-aur-devops/postgresql-docker/",
    "https://chaidocs.vercel.app/youtube/chai-aur-devops/node-logger/",
]


# 2. Fetch & parse HTML, return cleaned text
def fetch_page_text(url: str) -> str:
    resp = requests.get(url, timeout=10)
    resp.raise_for_status()  # fail early if bad response

    soup = BeautifulSoup(resp.text, "html.parser")
    # adjust the selector to match your docs’ main content
    container = soup.select_one("article") or soup.select_one("main")
    if not container:
        raise ValueError(f"Could not find content container on {url}")

    # Gather headings and paragraphs in reading order
    parts = []
    for elem in container.find_all(["h1", "h2", "h3", "p"]):
        text = elem.get_text(strip=True)
        if text:
            # prefix headings so reader sees structure
            if elem.name.startswith("h"):
                parts.append(f"\n\n## {text}\n\n")
            else:
                parts.append(text)
    return "\n".join(parts)


# 3. Chunk long text into smaller pieces
def chunk_text(text: str, url: str) -> list[dict]:
    splitter = CharacterTextSplitter(
        separator="\n",
        chunk_size=1000,
        chunk_overlap=200,
        length_function=len
    )
    raw_chunks = splitter.split_text(text)

    # Build metadata for each chunk
    chunks = []
    for i, chunk in enumerate(raw_chunks):
        chunks.append({
            "content": chunk,
            "source": url,
            "chunk_id": i
        })
    return chunks


def main():
    all_chunks = []
    for url in DOC_URLS:
        try:
            print(f"Fetching {url}")
            text = fetch_page_text(url)
            print(f" → Extracted {len(text)} characters")
            
            chunks = chunk_text(text, url)
            print(f" → Split into {len(chunks)} chunks")
            
            all_chunks.extend(chunks)
        except Exception as e:
            print(f"Error with {url}: {e}")

    # 4. Serialize to disk for downstream embedding
    with open("chunks.json", "w", encoding="utf-8") as f:
        json.dump(all_chunks, f, ensure_ascii=False, indent=2)

    print(f"✅ Completed ingestion: {len(all_chunks)} total chunks")


if __name__ == "__main__":
    main()
