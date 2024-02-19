# -*- coding: utf-8 -*-
# !/usr/bin/python
from functools import lru_cache
from rich.console import Console
from analysis.chinese import WordGeekChinese
from analysis.english import WordGeek
import sys


# 主程序
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
        if type(wk) != WordGeekChinese and wk.wordGroup != "": # 判断是哪种类型
            self.console.print(wk.wordGroup, style="rgb(105,170,102)")

    def printNull(self):
        self.console.print("* 错误：请输入单词或短语", style="rgb(237,247,75)")

    def printNotFind(self):
        self.console.print("Not find, try another word")
