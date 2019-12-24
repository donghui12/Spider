# -*- coding: UTF-8 -*-
from urllib import request
from bs4 import BeautifulSoup
import urllib
import requests 
from lxml import html
import threading
import os
import random
import time
import sys
import argparse

UserAgent_List = [
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/22.0.1207.1 Safari/537.1",
    "Mozilla/5.0 (X11; CrOS i686 2268.111.0) AppleWebKit/536.11 (KHTML, like Gecko) Chrome/20.0.1132.57 Safari/536.11",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1092.0 Safari/536.6",
    "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1090.0 Safari/536.6",
    "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/19.77.34.5 Safari/537.1",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.9 Safari/536.5",
    "Mozilla/5.0 (Windows NT 6.0) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.36 Safari/536.5",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
    "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_0) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
    "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3",
    "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
    "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
    "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.0 Safari/536.3",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24",
    "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24"
]

#thread_lock =threading.BoundedSemaphore(value=10)#设置最大线程锁
#目标抓取网页
src = 'https://www.mzitu.com/all'
BASE_URL = 'https://www.mzitu.com/{}/page/{}/'
#浏览器请求头（大部分网站没有这个请求头可能会报错）
cookies = 'Hm_lvt_dbc355aef238b6c32b43eacbbf161c3c={}; Hm_lpvt_dbc355aef238b6c32b43eacbbf161c3c={}'
headers = {
	# 'accept-language': 'en-US,en;q=0.9,zh-CN;q=0.8,zh;q=0.7',
	# 'authority': 'www.mzitu.com',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.88 Safari/537.36',
        'referer': src,
        # 'cookie':cookies.format(str(time.time())[:10], str(int(str(time.time())[:10])+6400)),
        }
print(headers)
#读取一个网页

'''def getHtml(url):
    req = request.Request(url,headers=mheaders) #添加headers避免服务器拒绝非浏览器访问
    page = request.urlopen(req)
    html = page.read()
    return html.decode('utf-8')  # python3 python2版本直接返回html
'''
#从入口爬取所有的目标链接
def getallUrl(pageNum, picType): #get All url
    web_urls = []
    for index in range(1,int(pageNum)+1):
        baseUrl = BASE_URL.format(picType, str(index))
        # print(baseUrl)
        # print(requests.get(baseUrl, headers=headers).content)
        selector = html.fromstring(requests.get(baseUrl, headers=headers).content)
        for i in selector.xpath('//ul[@id="pins"]/li/a/@href'):
            web_urls.append(i)
    return web_urls  #返回一个url数组

def get_Pic(url):   #从一个网页中找到并下载图片
    sel = html.fromstring(requests.get(url, headers=headers).content) 
    # 图片总数 倒数第二项里 
    total = sel.xpath('//div[@class="pagenavi"]/a[last()-1]/span/text()')[0]
    # 标题
    print(total)
    title = sel.xpath('//h2[@class="main-title"]/text()')[0] 
    print(title)
    # 接下来的链接放到这个列表 
    jpgList = [] 
    jpgList.append(title)
    for i in range(int(total)): 
        # 每一页 
        link = '{}/{}'.format(url, i+1) 
        s = html.fromstring(requests.get(link, headers=headers).content) 
        # 图片地址在src标签中
        try:
            jpg = s.xpath('//div[@class="main-image"]/p/a/img/@src')[0]
        except Exception as e:
            time.sleep(5)
            jpg = s.xpath('//div[@class="main-image"]/p/a/img/@src')[0]
        # 图片链接放进列表 
        jpgList.append(jpg) 

    return jpgList

def Creat_folder(output, title):
    path = os.path.join(output,title)
    if not os.path.exists(path):
        os.makedirs(path)
        
    return path

def download_pics(path,url,n):
    r = requests.get(url,headers=headers)
    write_path = path+'/'+str(n)+'.jpg'
    print("开始下载第{}张图片".format(n))
    with open(write_path,"wb") as f:
        f.write(r.content)
        f.close()
n=0

def main(argv):
    # print(argv)  # args -->>type list
    parser = argparse.ArgumentParser(add_help=False, description='a Spider of the website "www.Mzitu.com"')
    parser.add_argument('--help', '-h', action='help', default=argparse.SUPPRESS, help='Show this help message and exit')
    parser.add_argument('--depth', '-d', help='The depth of pages to download')
    parser.add_argument('--picType', '-t', help='The type of Pictures')
    parser.add_argument('--output', '-o', help='Output diretory(if not exist, Create it)')

    try:
        args = parser.parse_args(argv)

        depth = args.depth
        picType = args.picType
        output = args.output

        arguments = (depth, picType, output)
        if not all(arguments):
            parser.print_usage()
            raise ValueError('you need to specify all the arguments')
        print('Downloading picture for type:', picType)

        if not os.path.exists(output):
            os.makedirs(output)
        web_urls = getallUrl(depth, picType)   # 获取的是all url
        for url in web_urls:
            jpgList = get_Pic(url)
            path = Creat_folder(output,jpgList[0])
            n = 1   
            for jpg in jpgList[1:]:
                download_pics(path,jpg,n)
                n+=1
        
    except Exception as e:
        print('Error:', str(e))
        sys.exit(1)

if __name__ == "__main__":
    main(sys.argv[1:])   # get args from command
