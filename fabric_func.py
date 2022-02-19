from sys import argv
from bs4 import BeautifulSoup
import requests
import json
from requests_html import HTMLSession
import os
from time import sleep

retailer_path = os.path.join(os.path.dirname(os.path.abspath(__file__)),'retailers')


def get_command(l):
    if isinstance(l, list):
        return f'({",".join([get_command(i) for i in l])})'
    if isinstance(l, str):
        return f"'{l}'"
    return str(l)


def scrap(retailer, url):
    with open(os.path.join(retailer_path, retailer, 'scrape.json'), 'r') as f:
        son = json.load(f)
        x = None
        try:
            if son[0] == "js":
                session = HTMLSession()
                x = BeautifulSoup(session.get(
                    url).html.raw_html, "html.parser")
                session.close()
                son = son[1:]
            else:
                x = BeautifulSoup(requests.get(url).content, "html.parser")
        except requests.exceptions.ConnectionError as e:
            print(e)
            sleep(0.25)
            scrap(url, retailer)
        try:
            for i in son:
                if isinstance(i, int):
                    x = x[i]
                else:
                    x = eval(f'x.{i[0]}{get_command(i[1])}')
            # if x.text.strip()=="יש לכבס בהתאם להנחיות שעל תווית הכביסה.":
            #     raise AttributeError
            return x.text.strip()
        except (AttributeError, IndexError) as e:
            return 'None'


if __name__ == '__main__':
    print(scrap('terminalx',
          'https://www.terminalx.com/catalog/product/view/id/810153/s/x976060017/'))
