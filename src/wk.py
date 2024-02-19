# -*- coding: utf-8 -*-
# !/usr/bin/python
import time
from rich import print
import sys
from main import Main

start = time.time()
m = Main()
end = time.time()
running_time = end - start
print('用时: %.3f 秒' % running_time)
sys.exit()
