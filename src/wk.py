# -*- coding: utf-8 -*-
# !/usr/bin/python
from bs4 import BeautifulSoup
from rich.console import Console
import urllib3
import requests
import sys
import time, threading
import sqlite3

console = Console()


class WordGeek:
    # 参数设置
    def __init__(self, w):
        self.url = 'https://dict.youdao.com/search?q=' + w + '&keyfrom=new-fanyi.smartResult'
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0'
                          'Safari/537.36 '
        }
        self.proxy = {"http": None, "https": None}
        self.soup = self.request()

        # 结果：
        self.keyword = ""
        self.pronounce = ""
        self.change = ""
        self.meaning = ""
        self.englishMeaning = ""

    def request(self):
        # 发起请求
        urllib3.disable_warnings()  # 忽略证书验证警告
        response_html = requests.get(url=self.url, headers=self.headers, verify=False, proxies=self.proxy).text
        soup = BeautifulSoup(response_html, 'html.parser').find('div', {"class": "results-content"})
        # 获取网页对象
        return soup

    def getKeyWord(self):
        kl = self.soup.find_all('span', {"class": "keyword"})
        if len(kl) >= 1:
            self.keyword = kl[0].string

    def getPronounce(self):
        res = ""
        tag = self.soup.find_all('span', {"class": "pronounce"})
        if len(tag) >= 2:
            tag_uk = tag[0].strings
            tag_us = tag[1].strings
            for i in tag_uk:
                res += i.strip()
            res += "  "
            for i in tag_us:
                res += i.strip()
            self.pronounce = res

    def getChange(self):
        res = ""
        tl = self.soup.find_all('p', {"class": "additional"})
        if len(tl) >= 1:
            tag = tl[0].get_text().strip().split("\n")
            for i in tag:
                res += i.strip() + " "
            if res[0] == '[':
                self.change = res

    def getMeaning(self):
        res = ""
        count = 0
        m = self.soup.find("ul")
        if m is not None:
            for i in m.children:
                s = i.string
                if s != '\n' and s is not None:
                    sl = s.split("；")
                    l = len(sl)
                    if l > 3:
                        for i in range(3):
                            res += sl[i].replace('\n', '')
                    else:
                        for i in range(l):
                            res += sl[i].replace('\n', '')
                    res += '\n'
                count += 1
            self.meaning = res.strip()

    def getEnglishMeaning(self):
        res = ""
        phrases = self.soup.find_all('div', {"class": "trans-container"})

    def threadGet(self):
        t1 = threading.Thread(target=self.getKeyWord())
        t2 = threading.Thread(target=self.getPronounce())
        t3 = threading.Thread(target=self.getChange())
        t4 = threading.Thread(target=self.getMeaning())
        t1.start()
        t2.start()
        t3.start()
        t4.start()


word = ""
for i in range(1, len(sys.argv)):
    print(sys.argv[i])
    word += sys.argv[i] + " "

wk = WordGeek(word.strip())
wk.threadGet()
if wk.keyword:
    console.print("* " + wk.keyword, style="rgb(236,125,225)")  # 紫
    if wk.pronounce != "":
        console.print(wk.pronounce, style="rgb(169,66,34)")  # 红
    if wk.meaning != "":
        console.print(wk.meaning, style="rgb(105,170,102)")  # 绿
    if wk.change != "":
        console.print(wk.change, style="rgb(55,95,173)")  # 蓝
else:
    console.print("Not find, try another word")

