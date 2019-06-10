# coding=utf-8
from urllib import request
import requests
from urllib.request import urlopen
from pymongo import MongoClient

DOWNLOAD_PATH = 'D:/Downloads/PanDownload/wnacg/{}.zip'
CHUNK_SIZE = 512

db_test = MongoClient().test
wnacg = db_test.wnacg


def download_zip(url, name):
    request.urlretrieve(url, DOWNLOAD_PATH.format(name))


def download_zip2(url, name):
    res = urlopen(url)
    with open(DOWNLOAD_PATH.format(name), 'wb') as f:
        while True:
            chunk = res.read(CHUNK_SIZE)
            if not chunk:
                break
            f.write(chunk)


def download_zip3(url, name):
    res = urlopen(url).read()
    with open(DOWNLOAD_PATH.format(name), 'wb') as f:
        f.write(res)


for item in wnacg.find():
    try:
        download_zip3(item['url'], item['title'])
    except Exception as e:
        print("Error:", e)


print('OK')
