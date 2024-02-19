# -*- coding: utf-8 -*-
# !/usr/bin/python
from bs4 import BeautifulSoup
import urllib3
import requests
import threading
from functools import lru_cache


# 英译汉
class WordGeek:
    # 参数设置
    def __init__(self, w):
        self.url = 'https://dict.youdao.com/search?q=' + w + '&keyfrom=new-fanyi.smartResult'
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                          'Chrome/105.0.0.0'
                          'Safari/537.36 '
        }
        self.proxy = {"http": None, "https": None}
        self.soup = self.request()

        # 结果：
        self.keyword = ""
        self.pronounce = ""
        self.change = ""
        self.meaning = ""
        self.wordGroup = ""

    def request(self):
        # 发起请求
        urllib3.disable_warnings()  # 忽略证书验证警告
        try:
            response_html = requests.get(url=self.url, headers=self.headers, verify=False, proxies=self.proxy).text
            soup = BeautifulSoup(response_html, 'html.parser').find('div', {"class": "results-content"})
            return soup
        except Exception as e:
            exit("网络异常，请检查网络连接")

    @lru_cache
    def getKeyWord(self):
        kl = self.soup.find_all('span', {"class": "keyword"})
        if len(kl) >= 1:
            self.keyword = kl[0].string

    @lru_cache
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
            if len(res) > 16:
                self.pronounce = res

    @lru_cache
    def getChange(self):
        res = ""
        tl = self.soup.find_all('p', {"class": "additional"})
        if len(tl) >= 1:
            tag = tl[0].get_text().strip().split("\n")
            for i in tag:
                res += i.strip() + " "
            if res[0] == '[':
                self.change = res

    @lru_cache
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

    @lru_cache()
    def getWordGroup(self):
        res = ""
        phrases = self.soup.find_all('div', {"class": "collinsMajorTrans"})
        l = len(phrases)
        if l > 0:
            for s in phrases[0].strings:
                if s == "":
                    pass
                else:
                    res += s.strip().replace("  ", "") + " "
        self.wordGroup = res

    def threadGet(self):
        t1 = threading.Thread(target=self.getKeyWord())
        t2 = threading.Thread(target=self.getPronounce())
        t3 = threading.Thread(target=self.getChange())
        t4 = threading.Thread(target=self.getMeaning())
        t5 = threading.Thread(target=self.getWordGroup())
        t1.start()
        t2.start()
        t3.start()
        t4.start()
        t5.start()
