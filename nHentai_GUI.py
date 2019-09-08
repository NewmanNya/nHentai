# -*- coding:utf8 -*-
# 爬虫轻度爬取nHentai的数据，然后做可视化处理

import requests
from bs4 import BeautifulSoup
import time
import datetime
import sys
import os
import random
import re
import tkinter

# 提出请求
# flag 判定需不需要存储
def SoupInit(url,flag):
    text = ""
    WebName = Web2Name(url)
    if flag==2: # 不保存，直接抓
        headers = {
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.146 Safari/537.36'
        }
        res = requests.get(url, headers=headers)
        text = res.text
    elif flag==1: # 抓，保存
        headers = {
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.146 Safari/537.36'
        }
        res = requests.get(url, headers=headers)
        text = res.text
        f = open(WebName, "w+")
        f.write(text)
    else :  # 读取预留的文件
        f = open(WebName)
        line = f.readline()
        while line:
            text+=line
            line = f.readline()
        f.close()
    return BeautifulSoup(text,'lxml')


# DownloadPic from Web
# 这里发现封面图是可以直接用的
# 所以就直接在封面图的基础上做优化就行
# https://t.nhentai.net/galleries/1056819/thumb.png
# https://i.nhentai.net/galleries/1056819/1.png
def DownloadPic(url,num):
    ImgSite = url.replace("thumb",str(num))
    ImgSite = ImgSite.replace("t.nhentai.net","i.nhentai.net")
    imgNameList = Web2Name(ImgSite)
    # 没文件夹的话，要建一个文件夹
    if os.path.exists(imgNameList[0]):
        pass
    else:
        os.mkdir(imgNameList[0])
    # Pic 名字
    imgName = "./"+imgNameList[0]+"/"+imgNameList[1]
    # 已经下载过的话，就直接退出完事
    if os.path.exists(imgName):
        print("Have Downloaded Before")
    else:
        img = requests.get(ImgSite)
        print(ImgSite)
        print(img)
        open(imgName, 'wb').write(img.content)

# 解析url，获得本子信息列表
def AnalyzeWeb(url,flag):
    hentaiList = []
    WebIfo = SoupInit(url, flag)                                            # BS4解析
    WebIfo = WebIfo.find_all('div', attrs={"class": "gallery"})             # 本子信息
    for ifo in WebIfo:
        # noinspection PyBroadException
        try:
            hentaiID = ifo.a.get("href")
            hentaiWEB = "https://nhentai.net" + str(hentaiID)
            hentaiName = ifo.div.string                                                         # 获取本子名字
            hentaiCover = ifo.img.get('data-src')                                               # 获取本子封面地址
            hentaiList.append({"Name": hentaiName, "Cover": hentaiCover, "WEB": hentaiWEB })    # 归纳于List整理
        except:
            pass
    return hentaiList

# 输入网页，返回文件名字
def Web2Name(url):
    TextNameList = re.split('/', url)
    if "i.nhentai.net" in TextNameList:
        TextList = []
        HentaiID = TextNameList[-2]
        PageNum = TextNameList[-1]
        TextList.append(str(HentaiID))
        TextList.append(str(PageNum))
        return TextList
    # web列表命名
    else:
        TextName = "./"
        for i in range(TextNameList.index("nhentai.net") + 1,len(TextNameList)-1):
            TextName += (TextNameList[i]+'_')
        TextName += TextNameList[-1]
        TextName += ".html"
        return TextName

def GUI(url):
    HentaiList = AnalyzeWeb(url, 0)  # 分析后的列表

    i = 1
    for HentaiIfo in HentaiList:
        print(str(i)+"   ",end="")
        i+=1
        print(HentaiIfo)

    print("+++++++++++++++++++++++++++++++++++++++++++++++++++")
    hentai_select = int(input("Select hentai: "))
    print("+++++++++++++++++++++++++++++++++++++++++++++++++++")
    print("Your choice is: ")
    print(HentaiList[hentai_select - 1])
    print("---------------------------------------------------")
    gone = input("回车下一页 ")
    i = 1
    DownloadPic(HentaiList[hentai_select - 1]["Cover"], i)     # 先预渲染一页，这样的话，可以减少卡顿情况
    while gone == "":
        i = i + 1
        DownloadPic(HentaiList[hentai_select - 1]["Cover"], i)

        gone = input("回车下一页 ")
    print("---------------------------------------------------")


if __name__ =='__main__':
    LanguageDict = {"CH":"chinese","JP":"japanese","EN":"english"}      #可能会用到的语言选择功能
    nHentaiURL = "https://nhentai.net/language/chinese/popular"         #解析的链接
    GUI(nHentaiURL)







# GUI 1 选择哪个本子
# GUI 2 前一页/下一页  （收藏功能）

#



# 一个文件夹的内容

# 本子命名的文件夹
# ifo.txt 包含 名字  本子封面  以及本子网址
# photo数据