from bs4 import BeautifulSoup
import requests
import json
from requests_html import HTMLSession
import os
from time import sleep
import concurrent.futures
from itertools import repeat
import validators
import lxml
import cchardet

retailer_path = os.path.join(os.path.dirname(
    os.path.abspath(__file__)), 'retailers')
MAX_THREADS = 40


def get_command(l):
    if isinstance(l, list):
        return f'({",".join([get_command(i) for i in l])})'
    if isinstance(l, str):
        return f"'{l}'"
    return str(l)


# def scrap(retailer, url):
#     with open(os.path.join(retailer_path, retailer, 'scrape.json'), 'r') as f:
#         son = json.load(f)
#         x = None
#         try:
#             if son[0] == "js":
#                 session = HTMLSession()
#                 x = BeautifulSoup(session.get(
#                     url).html.raw_html, "html.parser")
#                 session.close()
#                 son = son[1:]
#             else:
#                 x = BeautifulSoup(requests.get(url).content, "html.parser")
#             # print(x.prettify())
#         except requests.exceptions.ConnectionError as e:
#             print(e)
#             sleep(0.25)
#             scrap(retailer, url)
#         try:
#             for i in son:
#                 if isinstance(i, int):
#                     x = x[i]
#                 else:
#                     x = eval(f'x.{i[0]}{get_command(i[1])}')
#             # if x.text.strip()=="יש לכבס בהתאם להנחיות שעל תווית הכביסה.":
#             #     raise AttributeError
#             return x.text.strip()
#         except (AttributeError, IndexError) as e:
#             return 'None'


def get_html(url):
    try:
        return requests.get(url, headers={
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Safari/537.36"}).content
    except (requests.exceptions.ConnectionError, requests.exceptions.ConnectTimeout, requests.exceptions.Timeout) as e:
        print(e, type(e), 'in gethtml')
        sleep(2)
        return get_html(url)


def download_url(url, son):
    if not validators.url(url):
        return 'Bad URL'
    try:
        x = BeautifulSoup(get_html(url), 'lxml')
        # print(x.prettify())
        for i in son:
            if isinstance(i, int):
                x = x[i]
            else:
                x = eval(f'x.{i[0]}{get_command(i[1])}')
        # if x.text.strip()=="יש לכבס בהתאם להנחיות שעל תווית הכביסה.":
        #     raise AttributeError
        sleep(0.25)
        return x.text.strip()
    except (AttributeError, IndexError) as e:
        print(e, 'in download_url', url)
        sleep(0.25)
        return 'Not found'


# def download_url_ses(url, son, ses):
#     if not validators.url(url):
#         return 'Bad URL'
#     try:
#         x = BeautifulSoup(ses.get(url).content, 'lxml')
#         # print(x.prettify())
#         for i in son:
#             if isinstance(i, int):
#                 x = x[i]
#             else:
#                 x = eval(f'x.{i[0]}{get_command(i[1])}')
#         # if x.text.strip()=="יש לכבס בהתאם להנחיות שעל תווית הכביסה.":
#         #     raise AttributeError
#         sleep(0.25)
#         return x.text.strip()
#     except (AttributeError, IndexError, requests.exceptions.ConnectionError, requests.exceptions.ConnectTimeout,
#             requests.exceptions.Timeout) as e:
#         if isinstance(AttributeError, IndexError):
#             print(e, 'in download_url', url)
#             sleep(0.25)
#             return 'None'
#         print(e, type(e), 'in gethtml')
#         sleep(2)
#         return get_html(url)


# def multi_scrap(retailer, url, threadcount=MAX_THREADS):
#     with open(os.path.join(retailer_path, retailer, 'scrape.json'), 'r') as inst:
#         son = json.load(inst)
#         threads = min(threadcount, len(url))
#         with concurrent.futures.ThreadPoolExecutor(max_workers=threads) as executor:
#             if son[0] == 'js':
#                 return list(executor.map(download_url, url, repeat(son[1:]), repeat(True)))
#             else:
#                 return list(executor.map(download_url, url, repeat(son)))


# def multi_scrap_with_thread_count(retailer, url, threadcount):
#     with open(os.path.join(retailer_path, retailer, 'scrape.json'), 'r') as inst:
#         son = json.load(inst)
#         threads = min(threadcount, len(url))
#         with concurrent.futures.ThreadPoolExecutor(max_workers=threads) as executor:
#             if son[0] == 'js':
#                 return list(executor.map(download_url, url, repeat(son[1:]), repeat(True)))
#             else:
#                 return list(executor.map(download_url, url, repeat(son)))


def scrap_manager(retailer, url):
    with open(os.path.join(retailer_path, retailer, 'scrape.json'), 'r') as son:
        inst = json.load(son)
        return list(concurrent.futures.ThreadPoolExecutor(max_workers=min(MAX_THREADS, len(url))).map(download_url, url,
                                                                                                      repeat(
                                                                                                          inst))) if isinstance(
            url, list) else download_url(url, inst)


# def scrap_manager_ses(retailer, url):
#     if not url:
#         return 'url is empty'
#     with open(os.path.join(retailer_path, retailer, 'scrape.json'), 'r') as son:
#         ses = requests.Session()
#         ses.headers.update({
#             "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Safari/537.36"})
#         inst = json.load(son)
#         return list(
#             concurrent.futures.ThreadPoolExecutor(max_workers=min(MAX_THREADS, len(url))).map(download_url_ses, url,
#                                                                                               repeat(
#                                                                                                   inst), repeat(
#                     ses))) if isinstance(
#             url, list) else download_url(url, inst)


if __name__ == '__main__':
    # print(scrap_manager('bonobos',
    #                     ['https://bonobos.com/products/jetsetter-stretch-wool-suit-pant'] * 50))
    print(scrap_manager('bonobos',
                        'https://bonobos.com/products/jetsetter-stretch-wool-suit-pant'))
    print(scrap_manager('terminalx',
                        'https://www.terminalx.com/women/pants-skirts/jeans/z280796027'))
    # print(scrap_manager_ses('bonobosnew',
    #                         'https://bonobos.com/products/jetsetter-stretch-wool-suit-pant'))
