# -*- coding:utf8 -*-
# 爬虫轻微爬取n-Hentai的数据，然后做可视化处理

import requests
from bs4 import BeautifulSoup
import time
import datetime
import sys
import os
import random
import re

# Send request and collect back
# flag 是不是是第一次抓数据，减轻服务器压力
def SoupInit(url,flag):
    text = ""
    WebName = Web2Name(url)
    if flag==2: # 第一次抓 不保存
        headers = {
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.146 Safari/537.36'
        }
        res = requests.get(url, headers=headers)
        text = res.text
    elif flag==1: # 第一次抓
        headers = {
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.146 Safari/537.36'
        }
        res = requests.get(url, headers=headers)
        text = res.text
        f = open(WebName, "w+")
        f.write(text)
    else :  # 之前已经抓过一次了
        f = open(WebName)
        line = f.readline()
        while line:
            text+=line
            line = f.readline()
        f.close()
    return BeautifulSoup(text,'lxml')

# Generate WebList from first web
def SelectWeb(url,PageNum):
    WebList = []
    for i in range(1,PageNum+1): # 这里暂时跳过第一页
        Pageurl = url+'&page='+str(i)
        soup  = SoupInit(Pageurl)
        FirstWeb = soup.find('section',{'class','thumb-listing-page'})
        FirstWeb = FirstWeb.findAll('li')
        for SecondWeb in FirstWeb:
            SecondWeb = SecondWeb.find('a').attrs
            WebList.append(SecondWeb['href'])
        RandTime(10)
        print("Page "+str(i)+" Has been collected")
    print("WebList Collected")
    print(WebList)
    return WebList


# https://i.nhentai.net/galleries/1056819/1.png
# https://t.nhentai.net/galleries/1056819/1.png
# DownloadPic from Web
def DownloadPic(url,num):
    ImgSite = url.replace("thumb",str(num))
    ImgSite = ImgSite.replace("t.nhentai.net","i.nhentai.net")
    print(ImgSite)
    img = requests.get(ImgSite)
    print(img)
    imgNameList = Web2Name(ImgSite)
    print(imgNameList)
    try:
        os.mkdir(imgNameList[0])
    except:
        pass
    imgName = "./"+imgNameList[0]+"/"+imgNameList[1]

    open(imgName, 'wb').write(img.content)

# 解析url，获得本子信息列表
# flag用来指定需不需要刷新html
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
# 指定存储文件夹
# 利用 "g" 字符实现自适应判定
def Web2Name(url):
    # 如果指定的子文件夹不为空
    TextNameList = re.split('/', url)
    # if Subfile=="web":
    #     TextName = "./"+Subfile+'/'
    #     for i in range(TextNameList.index("nhentai.net") + 2,len(TextNameList)-2):
    #         TextName += (TextNameList[i]+'_')
    #     TextName += TextNameList[i+1]
    #     TextName += ".html"
    # 下载的图片命名
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

# 获取真实ID，但是似乎可以直接从小图获取信息
def GetTrueID(url):
    SoupTemp = SoupInit(url, 2)
    SoupTemp = SoupTemp.find('img', attrs={"class": "fit-horizontal"}).get("src")
    return SoupTemp

if __name__ =='__main__':
    LanguageDict = {"CH":"chinese","JP":"japanese","EN":"english"}      #可能会用到的语言选择功能
    nHentaiURL = "https://nhentai.net/language/chinese/popular"         #解析的链接
    HentaiList = AnalyzeWeb(nHentaiURL,0)                               #分析后的列表
    # DownloadPic(tempurl,0)
    # print(Web2Name(nHentaiURL))
    # print(Web2Name(tempurl))
    #
    for i in HentaiList:
        print(i)

    print("+++++++++++++++++++++++++++++++++++++++++++++++++++")
    hentai_select = int(input("Select hentai: "))
    print("+++++++++++++++++++++++++++++++++++++++++++++++++++")
    print("Your choice is: ")
    print(HentaiList[hentai_select-1])
    # print(DownloadWeb)
    DownloadPic(HentaiList[hentai_select-1]["Cover"], 1)


    # tempurl = "https://nhentai.net/g/177392/2/"
    # temp = SoupInit(tempurl,0)
    # print(temp.find('img',attrs={"class": "fit-horizontal"}).get("src"))
    # # print (TextName)






# GUI 1 选择哪个本子
# GUI 2 前一页/下一页  （收藏功能）

#



# 一个文件夹的内容

# 本子命名的文件夹
# ifo.txt 包含 名字  本子封面  以及本子网址
# photo数据