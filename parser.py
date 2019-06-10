# coding=utf-8
import requests
from bs4 import BeautifulSoup
from pymongo import MongoClient
from datetime import datetime

URL = 'https://wnacg.net'
URL_PAGE = URL + '/albums-index-page-{}.html'
# 同人志
URL_PAGE_CATE1 = URL + '/albums-index-page-{}-cate-1.html'
# 单行本
URL_PAGE_CATE9 = URL + '/albums-index-page-{}-cate-9.html'

db_test = MongoClient().test
wnacg = db_test.wnacg


def parser(page=1):
    res = requests.get(URL_PAGE_CATE1.format(page))
    soup = BeautifulSoup(res.text, 'html5lib')

    pic_list = soup.find_all('div', 'pic_box')

    for pic in pic_list:
        href = pic.a['href']
        download_url = parser_down(href)
        author, category, size = parser_meta(href)
        result = wnacg.insert_one({
            'title': pic.a['title'],
            'cover': 'http:' + pic.find('img')['src'],
            'url': download_url,
            'author': author,
            'category': category,
            'size': size,
            'date': datetime.now()
        })
        print(result.inserted_id)


def parser_down(href):
    res = requests.get(URL + href.replace('photos-', 'download-'))
    soup = BeautifulSoup(res.text, 'html5lib')
    return soup.find('a', 'down_btn')['href']


def parser_meta(href):
    res = requests.get(URL + href)
    soup = BeautifulSoup(res.text, 'html5lib')
    uwconn = soup.find('div', 'asTBcell uwconn').find_all('label')
    uwuinfo = soup.find('div', 'asTBcell uwuinfo').find_all('p')
    return uwuinfo[0].string, uwconn[0].string.split('：')[1], uwconn[1].string.split('：')[1]


for i in range(1, 200):
    try:
        parser(i)
    except Exception as e:
        print('Error:', e)
        break
