import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse

visited_urls = set()

def is_valid_url(url, base_domain):
    parsed = urlparse(url)
    return parsed.netloc == base_domain and parsed.scheme in ["http", "https"]

def extract_text_from_page(url):
    try:
        response = requests.get(url, timeout=10)
        soup = BeautifulSoup(response.text, "html.parser")

        # Remove scripts and styles
        for tag in soup(["script", "style", "noscript"]):
            tag.decompose()

        title = soup.title.string if soup.title else ""
        text = " ".join([p.get_text() for p in soup.find_all(["p", "h1", "h2", "h3"])])

        return title + " " + text

    except Exception as e:
        return ""

def crawl_website(base_url, max_depth=2):
    base_domain = urlparse(base_url).netloc
    content = []

    def crawl(url, depth):
        if depth > max_depth or url in visited_urls:
            return

        visited_urls.add(url)

        page_text = extract_text_from_page(url)
        if page_text:
            content.append(page_text)

        try:
            response = requests.get(url)
            soup = BeautifulSoup(response.text, "html.parser")

            for link in soup.find_all("a", href=True):
                next_url = urljoin(url, link["href"])
                if is_valid_url(next_url, base_domain):
                    crawl(next_url, depth + 1)

        except:
            pass

    crawl(base_url, 0)
    return content
