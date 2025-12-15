from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from urllib.parse import urljoin, urlparse
import time


def crawl_website(base_url, max_depth=2):
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")

    driver = webdriver.Chrome(options=options)

    visited = set()
    results = []

    def crawl(url, depth):
        if depth > max_depth or url in visited:
            return

        visited.add(url)

        try:
            driver.get(url)
            time.sleep(3)

            text = driver.find_element(By.TAG_NAME, "body").text
            results.append(text)

            links = driver.find_elements(By.TAG_NAME, "a")
            for link in links:
                href = link.get_attribute("href")
                if href and urlparse(href).netloc == urlparse(base_url).netloc:
                    crawl(href, depth + 1)

        except Exception:
            pass

    crawl(base_url, 0)
    driver.quit()

    return results
