# -*- coding: utf-8 -*-
# !/usr/bin/python
import time
from functools import lru_cache

from bs4 import BeautifulSoup
from rich.console import Console
from rich import print
import urllib3
import requests
import sys
import threading


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


class Main:

    def __init__(self):
        self.console = Console()
        self.isChinese = False
        self.run()

    def run(self):
        word = self.getInput()
        if word == "":
            self.printNotFind()
        else:
            if self.isChinese:
                # 汉译英
                wk = WordGeekChinese(word)
                wk.threadGet()
                if wk.keyword:
                    self.printAll(wk)
                else:
                    self.printNull()
            else:
                # 英译汉
                wk = WordGeek(word)
                wk.threadGet()
                if wk.keyword:
                    self.printAll(wk)
                else:
                    self.printNull()

    @lru_cache
    def getInput(self):
        word = ""
        if len(sys.argv) > 1:
            if sys.argv[1] > 'z':
                self.isChinese = True
            for i in range(1, len(sys.argv)):
                word += sys.argv[i] + " "
        return word.strip()

    # 黄 rgb(237,247,75)
    # 紫 rgb(236,125,225)
    # 红 rgb(169,66,34)
    # 绿 rgb(105,170,102)
    # 深蓝 rgb(55,95,173)
    # 浅蓝 rgb(112,174,255)
    # 橘 rgb(252,154,3)
    def printAll(self, wk):
        self.console.print("* " + wk.keyword, style="rgb(252,154,3)")
        if wk.pronounce != "":
            print(wk.pronounce)
            # self.console.print("* " + wk.pronounce, style="rgb(105,170,102)")
        if wk.meaning != "":
            self.console.print(wk.meaning, style="rgb(236,125,225)")
        if wk.change != "":
            self.console.print(wk.change, style="rgb(112,174,255)")
        if wk.wordGroup != "":
            self.console.print(wk.wordGroup, style="rgb(105,170,102)")

    def printNull(self):
        self.console.print("* 错误：请输入单词或短语", style="rgb(237,247,75)")

    def printNotFind(self):
        self.console.print("Not find, try another word")


start = time.time()
m = Main()
end = time.time()
running_time = end - start
print('用时: %.3f 秒' % running_time)
sys.exit()
