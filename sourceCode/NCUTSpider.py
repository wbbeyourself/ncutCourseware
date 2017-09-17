# coding=utf-8
# All Rights Reserved, Copyright (C) 2016, beyourself

import codecs
import cookielib
import os
import re
import sys
import time
import urllib
import urllib2

import requests
from lxml import etree

from MessagePrinter import *
from configReader import *

reload(sys)
sys.setdefaultencoding("utf-8")


class MySpider:
    def __init__(self, username, pw, choice):
        self.username = username
        self.pw = pw
        if choice[0] == 'y' or choice[0] == 'Y':
            self.downloadall = True
        else:
            self.downloadall = False
        self.loginUrl = 'http://e.ncut.edu.cn/eclass/index.php?mon_icampus=yes'
        self.cookie = cookielib.MozillaCookieJar('cookie.txt')
        self.opener = urllib2.build_opener(
            urllib2.HTTPCookieProcessor(self.cookie)
        )
        self.postdata = urllib.urlencode(
            {'login': self.username, 'password': self.pw, 'submitAuth': '%BD%F8%C8%EB'})

    def get_suffix(self, furl):
        suffix = furl.split('.')[1]
        return '.' + suffix

    def print_dict(self, mydict):
        for (k, v) in mydict.items():
            print 'Key:' + k + ", Value:" + v

    def print_list(self, mylist):
        i = 0
        for item in mylist:
            print '[' + str(i) + '] ', item
            i += 1

    def Login(self, url, data):
        result = self.opener.open(url, data)
        self.cookie.save(ignore_discard=True, ignore_expires=True)
        # print result.read()
        return result.read()

    def get_cdict(self, html):
        course_dict = {}
        out = re.findall('(<li>.*?</li>)', html, re.S)
        if out:
            for item in out:
                selector = etree.HTML(item)
                try:
                    cname = re.findall('">(.*?)<', item)[0]
                    curl = re.findall('href="(.*?)">', item)[0]

                    if cname in course_dict:
                        # 重名的课程数量不会超过10个
                        for i in xrange(1, 10):
                            cname_t = '%s%s' % (cname, i)
                            if cname_t not in course_dict:
                                cname = cname_t
                                break

                    course_dict[cname] = curl
                except:
                    continue
        else:
            MessagePrinter.print_errormessage(u'找不到课程!!!')
        return course_dict

    def get_dirUrlDict(self, html):
        dirUrlDict = {}
        out = re.findall('openDir=.*?</a>', html, re.S)

        if out:
            for item in out:
                try:
                    dirUrl = re.findall('openDir=(.*?)\'', item)

                    if dirUrl:
                        subdirname = re.findall('hspace=5>(.*?)</a>', item)
                        if subdirname:
                            dirUrlDict[subdirname[0]] = \
                                'http://e.ncut.edu.cn/eclass/eclass/document/document.php?openDir=' + dirUrl[0]
                except:
                    continue
        return dirUrlDict

    def get_fdict(self, html):
        fdic = {}
        out = re.findall('(<tr align="center">.*?</tr>)', html, re.S)
        if out:
            for item in out:
                # selector = etree.HTML(item)
                try:
                    furl = re.findall('doc_url=%252F(.*?)\'', item)
                    if furl:
                        # fname = selector.xpath('//td[@align="left"]/a/text()')[0]
                        fname = re.findall('hspace=5>(.*?)</a>', item)
                        if fname:
                            fdic[fname[0]] = furl[0]
                except:
                    continue
        return fdic

    def get_cnum(self, curl):
        cnum = re.findall('eclass/(.*?)/', curl, re.S)[0]
        return cnum

    def get_user_selected(self, maxlen):
        while (True):
            MessagePrinter.print_promptmessage(u'请输入课程编号：')
            try:
                # 获取用户输入
                num = int(raw_input())
            except:
                MessagePrinter.print_errormessage(u'输入有误，请重新输入!!!')
                continue
            if (-1 < num) and (num < maxlen):
                return num
            else:
                MessagePrinter.print_errormessage(u'输入有误，请重新输入!!!')

                continue

    def question(self, fsize):
        while (True):
            print fsize
            MessagePrinter.print_promptmessage(
                u'文件大小超过50M，是否继续下载?(1 下载， 0 不下载): ')
            try:
                yes = int(raw_input()[0])
                if not (yes == 0 or yes == 1):
                    MessagePrinter.print_errormessage(u'输入有误，请重新输入!!!')
                else:
                    break
            except:
                MessagePrinter.print_errormessage(u'输入有误，请重新输入!!!')
        if yes:
            return True
        else:
            return False

    def get_fsizedict(self, html):
        fsize_dic = {}
        out = re.findall('(<tr align="center">.*?</tr>)', html, re.S)
        if out:
            for item in out:
                # selector = etree.HTML(item)
                # fsize = selector.xpath('//td/small/text()')[0]
                fsize = re.findall('<small>(.*?)</small>', item)
                if fsize:
                    fname = re.findall('hspace=5>(.*?)</a>', item)
                    if fname:
                        try:
                            fsize_dic[fname[0]] = fsize[0]
                        except:
                            continue
                else:
                    MessagePrinter.print_errormessage(u'该文件大小获取失败!!!')
                    continue

        return fsize_dic

    def download_single_course(self, cname, curl):
        if not os.path.exists(cname):
            cdir = './' + cname + '/'
            try:
                os.mkdir(cdir)
            except:
                MessagePrinter.print_errormessage(u'新建文件夹出错!!!')
                return
            MessagePrinter.print_process_info(u'正在新建文件夹...')
            MessagePrinter.print_process_info(cname)
        cnum = self.get_cnum(curl)
        MessagePrinter.print_process_info(u'正在下载课程...')
        MessagePrinter.print_process_info(cname)
        self.visit(curl)
        dochtml = self.visit(
            'http://e.ncut.edu.cn/eclass/eclass/document/document.php')
        self.downloadfiles(dochtml, cname, cnum)

    def downloadfile(self, fname, furl, pathprefix, cnum, fsize):
        if '%252F' in furl:
            furl = re.sub('%252F', '/', furl)

        full_url = 'http://e.ncut.edu.cn/eclass/' + cnum + '/document/' + furl
        full_fname = pathprefix + fname
        if not os.path.isfile(full_fname):
            MessagePrinter.print_process_info(u'正在下载文件...')
            MessagePrinter.print_process_info(fname)
            fp = open(full_fname, 'wb')
            doc = requests.get(full_url)
            fp.write(doc.content)
            fp.close()
        else:
            MessagePrinter.print_warningmessage(fname)
            MessagePrinter.print_warningmessage(u'该文件已存在!!!')

    def downloadfiles(self, html, pathprefix, cnum, subPage=False):

        fdict = self.get_fdict(html)

        fnamelist = fdict.keys()
        # self.print_dict(fdict)
        fsizedict = self.get_fsizedict(html)
        dirurldict = self.get_dirUrlDict(html)
        # self.print_dict(fsizedict)
        if fsizedict:
            # self.print_dict(fsizedict)
            # self.print_list(fnamelist)
            for fname in fnamelist:
                furl = fdict[fname]
                each_size = fsizedict[fname]
                try:
                    suffix = self.get_suffix(furl)
                except:
                    continue
                if suffix not in fname:
                    fname += suffix
                self.downloadfile(fname, furl, pathprefix, cnum, each_size)

        if (not subPage) and dirurldict:

            dirlist = dirurldict.keys()
            for dirname in dirlist:
                fulldirname = pathprefix + dirname + '/'
                if not os.path.exists(fulldirname):
                    try:
                        os.mkdir(fulldirname)
                    except:
                        MessagePrinter.print_errormessage(u'新建子文件夹出错!!!')
                        continue
                    MessagePrinter.print_process_info(u'正在新建子文件夹...')

                dochtml = self.visit(dirurldict[dirname])
                try:
                    self.downloadfiles(dochtml, fulldirname, cnum, 1)
                except:
                    continue

    def visit(self, url):
        result = self.opener.open(url)
        return result.read()

    def main(self):
        response = self.Login(self.loginUrl, self.postdata)
        failed = re.findall('red', response)
        length = failed.__len__()
        if length == 3:
            MessagePrinter.print_errormessage(u'用户名或密码错误!')
        else:
            cdict = self.get_cdict(response)
            # self.print_dict(cdict)

            if cdict:
                cnamelist = cdict.keys()
                if self.downloadall:
                    for cname in cnamelist:
                        self.download_single_course(
                            './' + cname + '/', cdict[cname])
                else:
                    MessagePrinter.print_promptmessage(u'待选课程如下：')
                    self.print_list(cnamelist)
                    course_num = self.get_user_selected(len(cdict))
                    self.download_single_course(
                        './' + cnamelist[course_num] + '/', cdict[cnamelist[course_num]])
                return True

            else:
                MessagePrinter.print_errormessage(u'无法找到课程!!!')
                return False


def babyGoodBye():
    os.system('pause')
    os._exit(-1)


if __name__ == '__main__':
    print '*******************   '
    print u'欢迎使用NCUT课件爬虫!'
    print '                      '
    print u'    制作人: 王冰     '
    print '*******************   '
    print '                      '

    username = ''
    pw = ''
    CONFIGFILE = '_config.ini'
    try:
        # 获取脚本路径
        path = sys.path[0]
        # 判断为脚本文件还是py2exe编译后的文件，如果是脚本文件，则返回的是脚本的目录，
        # 如果是py2exe编译后的文件，则返回的是编译后的文件路径
        if os.path.isfile(path):
            path = os.path.dirname(path)
        # 若配置文件有记事本BOM头，则去掉BOM头
        conf = path + '/' + CONFIGFILE
        if not os.path.exists(conf):
            MessagePrinter.print_errormessage('no file ' + conf)
            babyGoodBye()
        with open(conf) as f:
            data = f.read()
        if data[:3] == codecs.BOM_UTF8:
            data = data[3:]
            with open(conf, 'w') as f:
                f.write(data + '\n')

        myCfgReader = configReader(os.path.join(path, CONFIGFILE))
        username = myCfgReader.readConfig('loginInfo', 'username')
        pw = myCfgReader.readConfig('loginInfo', 'password')
    except:
        MessagePrinter.print_errormessage(u'请检查配置文件!!!')
        babyGoodBye()
    if (not username.strip()) or (not pw.strip()):
        MessagePrinter.print_errormessage(u'用户名或密码不能为空!!!')
        babyGoodBye()

    MessagePrinter.print_promptmessage(u'下载全部输入y,下载单个课程输入n :')
    choice = raw_input()
    ncut = MySpider(username, pw, choice)
    if ncut.main():
        MessagePrinter.print_process_info(u'下载完成')
    else:
        MessagePrinter.print_errormessage(u'下载失败')
    babyGoodBye()
