from bs4 import BeautifulSoup as bs
import requests


def get(url):
    req = requests.get(url)
    soup = bs(req.text, 'html.parser')

    tabContent = soup.select(
        '#tabContent > div.tab_body'
    )

    num = len(tabContent)

    a_tag = soup.select(
        '#tabContent > div:nth-child({}) > div:nth-child(3) > ul > li > div.wrap_thumb > a'.format(num)

    )
    img = soup.select(
        '#tabContent > div:nth-child({}) > div:nth-child(3) > ul > li > div.wrap_thumb > a > img'.format(num)
    )

    name = soup.select(
        '#tabContent > div:nth-child({}) > div:nth-child(3) > ul > li > a'.format(num)
    )

    price = soup.select(
        '#tabContent > div:nth-child({}) > div:nth-child(3) > ul > li > div.wrap_price > em'.format(num)
    )

    btn = soup.select(
        '#tabContent > div:nth-child({}) > div:nth-child(3) > ul > li > div.wrap_btn > a'.format(num)
    )

    result = []
    for item in zip(a_tag, img, name, price, btn):
        result.append([item[0]['href'],
                       item[1]['src'],
                       item[2]['href'],
                       item[2].text,
                       item[3].text,
                       item[4]['href']])

    return result