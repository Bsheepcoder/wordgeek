# -*- coding: utf-8 -*-
# !/usr/bin/python
from bs4 import BeautifulSoup
from rich.console import Console
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
        tag = self.soup.find_all('p', {"class": "wordGroup"})
        lt = len(tag)
        if lt > 0:
            for i in tag[0].strings:
                res += i.strip()
            self.pronounce = res.replace(";", "  ")

    def threadGet(self):
        t1 = threading.Thread(target=self.getKeyWord())
        t2 = threading.Thread(target=self.getPronounce())
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
        sys.exit()

    def getInput(self):
        word = ""
        if len(sys.argv) > 0:
            if sys.argv[1] > 'z':
                self.isChinese = True
            for i in range(1, len(sys.argv)):
                word += sys.argv[i] + " "
        return word.strip()

    def printAll(self, wk):
        # 黄 rgb(237,247,75)
        # 紫 rgb(236,125,225)
        # 红 rgb(169,66,34)
        # 绿 rgb(105,170,102)
        # 深蓝 rgb(55,95,173)
        # 浅蓝 rgb(112,174,255)
        # 橘 rgb(252,154,3)

        self.console.print("* " + wk.keyword, style="rgb(252,154,3)")
        if wk.pronounce != "":
            self.console.print(wk.pronounce, style="rgb(105,170,102)")
        if wk.meaning != "":
            self.console.print(wk.meaning, style="rgb(236,125,225)")
        if wk.change != "":
            self.console.print(wk.change, style="rgb(112,174,255)")

    def printNull(self):
        self.console.print("* 错误：请输入单词或短语", style="rgb(237,247,75)")

    def printNotFind(self):
        self.console.print("Not find, try another word")


m = Main()
