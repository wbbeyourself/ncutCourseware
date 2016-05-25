# 开发者指南

## 开发环境

- Python版本：2.7
- 集成开发环境: Pycharm 5.0.3
- 浏览器: Chrome
- 打包发布：py2exe

## 依赖库

- import requests
- import os
- from lxml import etree
- import re
- import urllib2
- import urllib
- import cookielib
- import sys

**注：Python27.zip内已包含这些依赖库了！**

## Python 开发环境配置：
1. 解压Python27.zip, 您会看到名为Python27的文件夹，将此文件夹拷贝到C盘根目录(文件不大，只有66MB，如果您想拷贝到其他盘，以D盘为例，后面第三步也要做出相应改变，第二步不变)；
2. 将python27.dll拷贝到 C:\Windows\SysWOW64 目录下(该目录针对Windows 64位
操作系统，如果您的系统是32位的，则需拷贝到C:\Windows\System32下即可)；
3. 配置环境变量-----将 C:\Python27\;C:\Python27\Scripts 加入到系统变量Path
中（如果您已经知道怎么配置的话，直接跳到第四步即可，不会的请继续往下看）。
我的电脑>系统属性>高级系统设置>高级>环境变量  在系统变量里找到Path（木有的话新建一个）。然后将 C:\Python27\;C:\Python27\Scripts追加到末尾，如果Path原先有值的话，需先加一个分号分隔开。(如果第一步拷贝到D盘，则修改为 D:\Python27\;D:\Python27\Scripts)
4. 下载Pycharm,[官网地址][6]
5. 打包发布命令 
``` python
python mysetup.py py2exe
```

## 初学者相关教程
- Python官网: [https://www.python.org/][7]
- Python爬虫基础知识: [http://www.jikexueyuan.com/path/python/][1]
- Python爬虫实战：[http://ke.jikexueyuan.com/xilie/116][2]
- Python学习参考：[http://wiki.jikexueyuan.com/list/python/][3]
- Chrome开发者工具简介: [http://blog.csdn.net/ivan0609/article/details/45287535][4]
- 推荐博客 静觅：[http://cuiqingcai.com/category/technique/python][5]
- 推荐博客 廖雪峰: [http://www.liaoxuefeng.com/wiki/0014316089557264a6b348958f449949df42a6d3a2e542c000][8]
- py2exe用法: [http://blog.chinaunix.net/uid-25979788-id-3064613.html][9]
- py2exe打包路径问题解决方案: [http://www.blogjava.net/cpegtop/articles/384455.html][10]




## 爬虫开发三部曲：

1. 模拟登陆(post form data)
2. 抓取网页HTML文件，正则表达式提取关键信息(re.find)
3. request下载所需文件(搞定文件URL，搞定一切)

## NCUTSpider 3个关键点

- 文件URL组成：
- 多模式教学网的HTML分析
- Cookie识别

[1]:http://www.jikexueyuan.com/path/python/
[2]:http://ke.jikexueyuan.com/xilie/116
[3]:http://wiki.jikexueyuan.com/list/python/
[4]:http://blog.csdn.net/ivan0609/article/details/45287535
[5]:http://cuiqingcai.com/category/technique/python
[6]:http://www.jetbrains.com/pycharm/download/#section=windows
[7]:https://www.python.org/
[8]:http://www.liaoxuefeng.com/wiki/0014316089557264a6b348958f449949df42a6d3a2e542c000
[9]:http://blog.chinaunix.net/uid-25979788-id-3064613.html
[10]:http://www.blogjava.net/cpegtop/articles/384455.html