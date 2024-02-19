# -*- coding: utf-8 -*-
# !/usr/bin/python
from bs4 import BeautifulSoup
import urllib3
import requests
import threading
from functools import lru_cache


# 汉译英
class WordGeekChinese:
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
        self.englishMeaning = ""

    def request(self):
        # 发起请求
        urllib3.disable_warnings()  # 忽略证书验证警告
        try:
            response_html = requests.get(url=self.url, headers=self.headers, verify=False, proxies=self.proxy).text
            soup = BeautifulSoup(response_html, 'html.parser').find('div', {"class": "results-content"})
            # 获取网页对象
            return soup
        except Exception as e:
            print("网络异常")

    def getKeyWord(self):
        kl = self.soup.find_all('span', {"class": "keyword"})
        if len(kl) >= 1:
            self.keyword = kl[0].string

    @lru_cache
    def getMeaning(self):
        res = ""
        tag = self.soup.find_all('p', {"class": "wordGroup"})
        lt = len(tag)
        if lt > 0:
            for i in tag[0].strings:
                res += i.strip()
            self.meaning = res.replace(";", " | ")

    def threadGet(self):
        t1 = threading.Thread(target=self.getKeyWord())
        t2 = threading.Thread(target=self.getMeaning())
        t1.start()
        t2.start()
