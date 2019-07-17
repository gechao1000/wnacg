from subprocess import call
from pymongo import MongoClient
import threading

db_test = MongoClient().test
wnacg = db_test.wnacg


def download(url, name):
    call(['you-get', url,
          '-o', 'D:\Downloads\PanDownload\wnacg', '-O', name + '.zip'])


for item in wnacg.find():
    try:
        download(item['url'], item['title'])
        # threading._start_new_thread(download, (item['url'], item['title']))
    except Exception as e:
        print("Error:", e)
