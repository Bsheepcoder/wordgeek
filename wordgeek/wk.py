# -*- coding: utf-8 -*-
# !/usr/bin/python
from bs4 import BeautifulSoup
from rich.console import Console
import urllib3
import requests
import sys

console = Console()
word = sys.argv[1]
if word == "wordgeek":
    console.print(" Congratulations! you found the painted eggshell !", style="bold red")
    console.print(" 好奇之心，改变之力！ Geek yyds！", style="bold red")
    exit()
# 参数设置
url_mian = 'https://dict.youdao.com/search?q=' + word + '&keyfrom=new-fanyi.smartResult'
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 '
                  'Safari/537.36 '
}
proxy = {"http": None, "https": None}
# 发起请求
urllib3.disable_warnings()  # 忽略证书验证警告
response_html = requests.get(url=url_mian, headers=headers, verify=False, proxies=proxy).text
# print(response_html)

# 获取网页对象
soup = BeautifulSoup(response_html, 'lxml')
# print(soup)

# 获取网页结果
# 判断输入是否正确
wordCorrect = soup.find_all('span', {"class": "keyword"})
if wordCorrect:
    # 输出所查单词
    console.print("【" + word + "】", style="rgb(255,237,204)")

    # 单词意思
    wordMean_div = soup.find_all('div', {"class": "trans-container"})
    wordMeanSoup = BeautifulSoup(str(wordMean_div[0]), 'lxml')
    wordMeanList = wordMeanSoup.find_all('li')

    # 获取例句
    wordSt = soup.find_all('div', {"class": "trans-container"})

    # 输出
    # 输出是倒叙的 释义-->单词
    # 输出释义
    for i in range(0, len(wordMeanList)):
        m = wordMeanList[i].text.split('；')
        # print(m)
        if len(m) > 1:
            console.print(" " + m[0], m[1], style="rgb(236,125,225)")
        else:
            console.print(" " + m[0].replace(" ", ""), style="rgb(236,125,225)")
else:
    console.print("Error not find！", style="bold red")
