import requests
from bs4 import BeautifulSoup
import lxml


def get_hindu_links():
    HI_URL = "https://www.thehindu.com/opinion/editorial/"

    response = requests.get(HI_URL)
    data = response.text

    soup = BeautifulSoup(data, "lxml")
    editorial_titles = soup.find_all(class_=["element", "wide-row-element"])

    hindu_article_links = []
    for article_tag in editorial_titles:
        links = [a_tag["href"] for a_tag in article_tag.find_all("a")]
        for index, link in enumerate(links):
            if (index == 0 or link != links[index - 1]) and len(hindu_article_links) < 2:
                hindu_article_links.append(link)

        if len(hindu_article_links) >= 2:
            break

    return hindu_article_links


def get_article(link):
    response = requests.get(link)
    data = response.text

    soup = BeautifulSoup(data, "lxml")
    content = [tag.text for tag in soup.find(class_="articlebodycontent").find_all("p")]
    content = ''.join(content[:2])
    title = soup.find(class_="title").text.strip("\n")
    return {title: content}
