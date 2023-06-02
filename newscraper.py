import requests
from bs4 import BeautifulSoup
from playwright.sync_api import sync_playwright
import time
import pandas as pd
url = 'https://gigatron.rs/prenosni-racunari/laptop-racunari'
response = requests.get(url)
response = response.content
soup = BeautifulSoup(response, 'html.parser')
def resp(url):
    response = requests.get(url)
    data = response.json()
    return data["totalPages"]


def scrape(data):
    articles = []
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()
        page.set_viewport_size({
            "width": 1280, "height": 1080
        })
        page.goto("https://gigatron.rs/prenosni-racunari/laptop-racunari", timeout=0)
        time.sleep(2)
        page.wait_for_load_state("networkidle")
        art = soup.find_all('div', class_='item')
        for i in range(1, data):
            page.evaluate("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(1)
            for article in art:
                title = article.find('h4').text
                previousPrice = article.find('div', class_='item__bottom__prices__old item__bottom__prices__old--retail').text[9:]
                currentPrice = article.find('div', class_='item__bottom__prices__price').text
                saving = article.find('div', class_='item__bottom__prices__saving').text[8:]
                prevPrice = int(float(previousPrice[:-4]))
                currPrice = int(float(currentPrice[:-4]))
                save = int(float(saving[:-4]))
                now = (save/prevPrice)*100
                percent = round(now,2)
                print(percent)
                articles.append([title, previousPrice, currentPrice, percent])
    df = pd.DataFrame(articles,columns=["Title","Previous Price","Current Price","Discount"])
    df.to_csv('articles.csv')

scrape(resp("https://search.gigatron.rs/v1/catalog/get/oprema-za-racunare/periferije/misevi?strana=1"))


