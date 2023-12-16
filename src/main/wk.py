# -*- coding: utf-8 -*-
# !/usr/bin/python
from bs4 import BeautifulSoup
from rich.console import Console
import urllib3
import requests
import sys
import time, threading

console = Console()


class Soup:
    # 参数设置
    def __init__(self, w):
        self.url = 'https://dict.youdao.com/search?q=' + w + '&keyfrom=new-fanyi.smartResult'
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0'
                          'Safari/537.36 '
        }
        self.proxy = {"http": None, "https": None}
        self.soup = self.request()

    def request(self):
        # 发起请求
        urllib3.disable_warnings()  # 忽略证书验证警告
        response_html = requests.get(url=self.url, headers=self.headers, verify=False, proxies=self.proxy).text
        soup = BeautifulSoup(response_html, 'html.parser').find('div', {"class": "results-content"})
        # 获取网页对象
        return soup


def getKeyWord(soup):
    return soup.find_all('span', {"class": "keyword"})[0].string


def getPronounce(soup):
    res = ""
    tag = soup.find_all('span', {"class": "pronounce"})
    tag_uk = tag[0].strings
    tag_us = tag[1].strings
    phonetic = soup.find_all('span', {"class": "phonetic"})
    for i in tag_uk:
        res += i.strip()
    res += "  "
    for i in tag_us:
        res += i.strip()
    return res

def getChange(soup):
    res = ""
    tag = soup.find_all('p', {"class": "additional"})[0].get_text().strip().split("\n")
    for i in tag:
        res += i.strip() + " "
    return res

def getMeaning(soup):
    res = ""
    count = 0
    m = soup.find("ul").children
    for i in m:
        s = i.string
        if count == 0:  # 去除换行
            pass
        elif count == 1:
            s = s.split("；")
            for i in range(0, 4):
                res += s[i]
        else:
            res += s
        count += 1
    return res.strip()


def getPhrases(soup):
    res = ""
    phrases = soup.find('ul', {"class": "ol"}).contents[1].get_text().strip().replace('/n', '')
    return phrases


# word = sys.argv[1]
soup = Soup("word").soup
print(getKeyWord(soup))
print(getPronounce(soup))
print(getMeaning(soup))
print(getChange(soup))
print(getPhrases(soup))



# 获取网页结果
# 判断输入是否正确
# wordCorrect = soup.find_all('span', {"class": "keyword"})
# if wordCorrect:
#     # 输出所查单词
#     console.print("【" + word + "】", style="rgb(255,237,204)")
#
#     # 单词意思
#     wordMean_div = soup.find_all('div', {"class": "trans-container"})
#     wordMeanSoup = BeautifulSoup(str(wordMean_div[0]), 'html.parser')
#     wordMeanList = wordMeanSoup.find_all('li')
#
#     # 获取例句
#     wordSt = soup.find_all('div', {"class": "trans-container"})
#
#     # 输出
#     # 输出是倒叙的 释义-->单词
#     # 输出释义
#     for i in range(0, len(wordMeanList)):
#         m = wordMeanList[i].text.split('；')
#         # print(m)
#         if len(m) > 1:
#             console.print(" " + m[0], m[1], style="rgb(236,125,225)")
#         else:
#             console.print(" " + m[0].replace(" ", ""), style="rgb(236,125,225)")
# else:
#     console.print("没有找到这个单词！", style="bold red")
