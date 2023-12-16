#!/usr/bin/env python3
# -*- coding:utf-8 -*-
import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="src",  # 项目名称，保证它的唯一性，不要跟已存在的包名冲突即可
    version="0.0.4",  # 程序版本
    author="Husile",  # 项目作者
    author_email="18947336207@163.com",  # 作者邮件
    description="windows命令行查词",  # 项目的一句话描述
    long_description=long_description,  # 加长版描述？
    long_description_content_type="text/markdown",  # 描述使用Markdown
    url="https://github.com/Bsheepcoder/wordgeek",  # 项目地址
    packages=setuptools.find_packages(),  # 无需修改
    classifiers=[
        "Programming Language :: Python :: 3",  # 使用Python3
        "License :: OSI Approved :: Apache Software License",  # 开源协议
        "Operating System :: OS Independent",
    ],
)
