import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
from collections import deque

def crawl_website(
    base_url,
    max_depth=2,
    max_pages=60,
    max_chars=120000
):
    visited = set()
    texts = []
    total_chars = 0

    base_domain = urlparse(base_url).netloc
    queue = deque()
    queue.append((base_url, 0))

    headers = {"User-Agent": "Mozilla/5.0"}

    while queue:
        url, depth = queue.popleft()

        if (
            url in visited
            or depth > max_depth
            or len(visited) >= max_pages
            or total_chars >= max_chars
        ):
            continue

        visited.add(url)

        try:
            response = requests.get(url, timeout=4, headers=headers)

            if response.status_code != 200:
                continue

            if "text/html" not in response.headers.get("Content-Type", ""):
                continue

            soup = BeautifulSoup(response.text, "html.parser")

            for tag in soup(["script", "style", "noscript", "img", "svg"]):
                tag.decompose()

            page_text = soup.get_text(separator=" ", strip=True)

            if page_text:
                texts.append(page_text)
                total_chars += len(page_text)

            if depth < max_depth:
                for link in soup.find_all("a", href=True):
                    href = urljoin(base_url, link["href"])
                    parsed = urlparse(href)

                    if (
                        parsed.netloc == base_domain
                        and not parsed.fragment
                        and not href.endswith((".pdf", ".jpg", ".png", ".zip"))
                        and href not in visited
                    ):
                        queue.append((href, depth + 1))

        except Exception:
            continue

    return texts
