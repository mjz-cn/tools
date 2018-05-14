# coding: utf-8
#! /usr/local/bin/python3

import os
import sys
from urllib.parse import urljoin
import time

import requests
from bs4 import BeautifulSoup
from bottle import SimpleTemplate

from mailclient import MailClient

os.environ["PYTHONIOENCODING"] = "utf-8"

print(sys.getdefaultencoding())

headers = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.79 Safari/537.36",
}

g_data = {
    
}

f = os.path.realpath(__file__)
executeDir = os.path.dirname(f)
cachePath = os.path.join(executeDir, "cache.data")

def init():
    with open(cachePath, encoding='utf-8') as fd:
        for line in fd.readlines():
            pos = line.find("=")
            if pos == -1:
                continue
            key, val = line[0:pos].strip("\n "), line[pos+1:].strip("\n ")
            g_data[key] = val

def updateCache():
    with open(cachePath, 'w', encoding='utf-8') as fd:
        for key, val in g_data.items():
            fd.write(key+"="+val+"\n")

def biquge(params):
    li = []
    for url, name in params:
        book_url = url
        key = url + "_newest"
        data = requests.get(url, headers=headers).content
        soup = BeautifulSoup(data, 'html.parser')

        lis = soup.find(id="chapterlist")
        if not lis:
            continue
        for p in lis.findAll('p'):
            a = p.find("a")
        href = a.attrs.get('href')
        title = a.text
        val = href+title

        if key in g_data and val == g_data[key]:
            continue

        chapterUrl = urljoin(url, href)
        html = requests.get(chapterUrl, headers=headers).content.decode('utf-8')
        content = BeautifulSoup(html, 'html.parser').find(id="chaptercontent")
        # print(name, title)

        tpl = executeDir + "/mail_book.tpl"
        s = SimpleTemplate(name=tpl)
        htmlData = s.render(data=[[name, book_url, title, str(content)]])

        mail = MailClient()
        mail.sendMail(htmlData, name + '--' + title, to="369806726@qq.com")

        g_data[key] = val
        updateCache()

        li.append([name, book_url, title, str(content)])
    return li

def main():
    print(time.strftime('%Y%m%d %H:%M:%S'))

    init()

    params = [
        ["http://m.biquge.la/book/285/", "赘婿"],
        ["http://m.biquge.la/book/3820/", "俗人回档"],
        ["http://m.biquge.la/book/11298/", "五行天"],
        ["http://m.biquge.la/book/38882/", "重燃"],
        ["http://m.biquge.la/book/31024/", "逆流纯真年代"],
        ["http://m.biquge.la/book/24551/", "剑扣天门"],
        ["https://m.qu.la/book/34824/", "平天策"],
    ]

    li = biquge(params)
    if not li:
        return

    tpl = executeDir + "/mail_book.tpl"
    s = SimpleTemplate(name=tpl)
    htmlData = s.render(data=li)

    t = []
    for name, _, _, _ in li:
        t.append(name)

    mail = MailClient()
    # mail.sendMail(htmlData, "-".join(t),to="369806726@qq.com")
    print(t)

if __name__ == '__main__':

    for i in range(3):
        try:
            main()
            break
        except Exception as e:
            if i == 2:
                raise e
            print(e)

