from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import time


def get_ht_links():
    HT_URL = "https://www.hindustantimes.com/editorials"

    # Set up Chrome options for headless mode
    chrome_options = Options()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    chrome_options.add_argument('--disable-gpu')

    # Use webdriver_manager to automatically manage ChromeDriver
    service = Service(ChromeDriverManager().install())

    driver = webdriver.Chrome(service=service, options=chrome_options)

    try:
        driver.get(HT_URL)
        WebDriverWait(driver, 5).until(
            EC.presence_of_element_located((By.CLASS_NAME, "cartHolder"))
        )
        data = driver.page_source
    finally:
        driver.quit()

    soup = BeautifulSoup(data, "lxml")
    editorial_titles = soup.find_all("div", class_=["cartHolder", "listView", "track", "timeAgo", "articleClick"])

    ht_article_links = []
    for title in editorial_titles:
        article_url = title.get("data-weburl")
        if article_url:
            ht_article_links.append(article_url)
        if len(ht_article_links) >= 3:
            ht_article_links = ht_article_links[:3]
            break

    return ht_article_links


def get_article(link):
    # Set up Chrome options for headless mode
    chrome_options = Options()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    chrome_options.add_argument('--disable-gpu')  # Optional but useful
    chrome_options.add_argument('--window-size=1920x1080')  # Optional but useful

    # Use webdriver_manager to automatically manage ChromeDriver
    service = Service(ChromeDriverManager().install())

    driver = webdriver.Chrome(service=service, options=chrome_options)

    try:
        driver.get(link)
        WebDriverWait(driver, 5).until(
            EC.presence_of_element_located((By.CLASS_NAME, "cartHolder"))
        )
        data = driver.page_source
    finally:
        driver.quit()

    soup = BeautifulSoup(data, "lxml")
    title = soup.find("h1", class_="hdg1").text.strip("\n")
    article = soup.find(class_="storyDetails").find_all("p")
    content = "".join([tag.text for tag in article])

    return {title: content.strip(" ")}
