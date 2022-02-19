import concurrent.futures
import requests
from bs4 import BeautifulSoup
from time import sleep
import os
import json
from requests_html import HTMLSession
from itertools import repeat

MAX_THREADS = 30
retailer_path = os.path.join(os.path.dirname(os.path.abspath(__file__)),'retailers')


def get_command(l):
    if isinstance(l, list):
        return f'({",".join([get_command(i) for i in l])})'
    if isinstance(l, str):
        return f"'{l}'"
    return str(l)


def get_html(url, js=False):
    try:
        if js:
            session = HTMLSession()
            t = session.get(
                url).html.raw_html
            session.close()
            return t
        return requests.get(url).content
    except (requests.exceptions.ConnectionError, requests.exceptions.ConnectTimeout,requests.exceptions.Timeout) as e:
        print(e, type(e), 'in gethtml')
        sleep(1)
        return get_html(url, js)


def download_url(url, son, js=False):
    try:
        x = BeautifulSoup(get_html(url, js), "html.parser")
        for i in son:
            if isinstance(i, int):
                x = x[i]
            else:
                x = eval(f'x.{i[0]}{get_command(i[1])}')
        sleep(0.25)
        return x.text.strip()
    except Exception as e:
        print(e, 'in download_url')
        sleep(0.25)
        return e


def multi_scrap(retailer,urls):
    with open(os.path.join(retailer_path, retailer, 'scrape.json'), 'r') as inst:
        son = json.load(inst)
        threads = min(MAX_THREADS, len(urls))
        with concurrent.futures.ThreadPoolExecutor(max_workers=threads) as executor:
            if son[0] == 'js':
                return list(executor.map(download_url, urls, repeat(son[1:]), repeat(True)))
            else:
                return list(executor.map(download_url, urls, repeat(son)))

def multi_scrap_with_thread_count(retailer,urls,threadcount):
    with open(os.path.join(retailer_path, retailer, 'scrape.json'), 'r') as inst:
        son = json.load(inst)
        threads = min(threadcount, len(urls))
        with concurrent.futures.ThreadPoolExecutor(max_workers=threads) as executor:
            if son[0] == 'js':
                return list(executor.map(download_url, urls, repeat(son[1:]), repeat(True)))
            else:
                return list(executor.map(download_url, urls, repeat(son)))


if __name__ == '__main__':
    x = ['terminalx', ['https://www.terminalx.com/women/pants-skirts/jeans/z280796027?color=10106'] * 500]
    # print(x)
    results = multi_scrap(x[1])
    print([i for i in results], len(list(results)))
    # print('end', len(exp), exp, len(exp))
