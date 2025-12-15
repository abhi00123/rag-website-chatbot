import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse

def crawl_website(
    base_url,
    max_depth=2,
    max_pages=60,
    max_chars=150000
):
    visited = set()
    texts = []
    total_chars = 0

    base_domain = urlparse(base_url).netloc

    def crawl(url, depth):
        nonlocal total_chars

        if (
            depth > max_depth
            or url in visited
            or len(visited) >= max_pages
            or total_chars >= max_chars
        ):
            return

        visited.add(url)

        try:
            response = requests.get(
                url,
                timeout=4,
                headers={"User-Agent": "Mozilla/5.0"}
            )

            if "text/html" not in response.headers.get("Content-Type", ""):
                return

            soup = BeautifulSoup(response.text, "html.parser")

            for tag in soup(["script", "style", "noscript", "img", "svg"]):
                tag.decompose()

            page_text = soup.get_text(separator=" ", strip=True)

            if page_text:
                texts.append(page_text)
                total_chars += len(page_text)

            for link in soup.find_all("a", href=True):
                if total_chars >= max_chars:
                    break

                href = urljoin(base_url, link["href"])
                parsed = urlparse(href)

                if (
                    parsed.netloc == base_domain
                    and not parsed.fragment
                    and not href.endswith((".pdf", ".jpg", ".png", ".zip"))
                ):
                    crawl(href, depth + 1)

        except Exception:
            return

    crawl(base_url, 0)
    return texts
