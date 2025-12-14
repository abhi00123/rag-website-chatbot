from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import time

def crawl_with_selenium(url):
    options = Options()
    options.add_argument("--headless")  # runs without opening window
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")

    driver = webdriver.Chrome(
        service=Service(ChromeDriverManager().install()),
        options=options
    )

    driver.get(url)
    time.sleep(5)  # wait for JS to load

    html = driver.page_source
    driver.quit()

    soup = BeautifulSoup(html, "html.parser")

    for tag in soup(["script", "style", "noscript"]):
        tag.decompose()

    text = " ".join(
        t.get_text()
        for t in soup.find_all(["p", "h1", "h2", "h3"])
    )

    return text
