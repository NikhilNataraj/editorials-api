import requests
from bs4 import BeautifulSoup
import lxml


def get_toi_links():
    TOI_URL = "https://timesofindia.indiatimes.com/blogs/toi-editorials/"

    response = requests.get(TOI_URL)
    data = response.text

    soup = BeautifulSoup(data, "lxml")
    editorial_titles = soup.find_all(class_="detail")

    toi_article_links = []
    for article_tag in editorial_titles:
        links = [a_tag["href"] for a_tag in article_tag.find_all("a") if "/toi-edit-page/" in a_tag["href"] and
                 a_tag["href"][-14:-1] != "toi-edit-page"]

        for link in links:
            if len(toi_article_links) < 5:
                toi_article_links.append(link)

        if len(toi_article_links) >= 5:
            break

    return toi_article_links


def get_article(link):
    response = requests.get(link)
    data = response.text

    soup = BeautifulSoup(data, "lxml")
    article_content = soup.find(class_="main-content").find_all("p", recursive=False)
    content = [tag.text for tag in article_content if len(tag.text) > 50]
    content = " ".join(content)
    title = soup.find(class_="show-header").find("h1").text.strip("\n")
    return {title: content}
