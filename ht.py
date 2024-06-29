# import os
from bs4 import BeautifulSoup

import asyncio
from playwright.async_api import async_playwright


async def get_ht_links():
    HT_URL = "https://www.hindustantimes.com/editorials"

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        await page.goto(HT_URL)

        ht_article_links = await page.evaluate('''() => {
            let editorial_titles = document.querySelectorAll("div.cartHolder.listView.track.timeAgo.articleClick");

            let ht_article_links = [];
            editorial_titles.forEach(title => {
                let article_url = title.getAttribute("data-weburl");
                if (article_url) {
                    ht_article_links.push(article_url);
                }
                if (ht_article_links.length >= 3) {
                    return ht_article_links;
                }
            });
            return ht_article_links;
        }''')

        await browser.close()
        return ht_article_links


def fetch_links():
    return asyncio.run(get_ht_links())


# print(fetch_links())


async def get_article(link):
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        await page.goto(link)
        await page.wait_for_selector('.mainContainer', timeout=10000)
        data = await page.content()
        await browser.close()

    soup = BeautifulSoup(data, "lxml")
    title = soup.find("h1", class_="hdg1").text.strip("\n")
    article = soup.find(class_="storyDetails").find_all("p")
    content = "".join([tag.text for tag in article])

    return {title: content.strip(" ")}


def fetch_article(link):
    return asyncio.run(get_article(link))


# LINK = 'https://www.hindustantimes.com/editorials/challenge-and-an-opportunity-101719501023386.html'
# print(fetch_article(LINK))
