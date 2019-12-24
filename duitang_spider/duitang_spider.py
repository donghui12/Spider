import requests
import urllib.parse
import threading
import os
import sys
import argparse
import time

thread_lock =threading.BoundedSemaphore(value=10)#设置最大线程锁

SEARCH_BASE_URL = 'https://www.duitang.com/napi/blog/list/by_search/?kw={}&type=feed&include_fields=top_comments%2Cis_root%2Csource_link%2Citem%2Cbuyable%2Croot_id%2Cstatus%2Clike_count%2Clike_id%2Csender%2Calbum%2Creply_count%2Cfavorite_blog_id&_type=&start={}&_={}&limit=1000'

CATEGORY_BASE_URL = 'https://www.duitang.com/napi/blog/list/by_filter_id/?include_fields=top_comments%2Cis_root%2Csource_link%2Citem%2Cbuyable%2Croot_id%2Cstatus%2Clike_count%2Csender%2Calbum%2Creply_count&filter_id={}&start={}&_={}&limit=1000'

def get_page(url):  #通过URL获取数据
    page = requests.get(url)
    page = page.content #将bytes 转成str字符串
    page = page.decode('utf-8')
    return page
#print(get_page('https://www.duitang.com/napi/blog/list/by_search/?kw=%E6%A0%A1%E8%8A%B1&&start=0&limit=1000'))
#36
#label:校花
def pages_from_search(label, nums, tag=None):  #获取其他页面链接
    pages = []
    url = SEARCH_BASE_URL
    if tag is None:
        label=urllib.parse.quote(label) #将中文转成url编码
    else:
        label=urllib.parse.quote(label)+"_"+ urllib.parse.quote(tag)

    for index in range(0,int(nums),100):
        u = url.format(label, index, str(time.time()).replace('.','')[:14])
        # print(u)
        page = get_page(u)
        pages.append(page)
    return pages


def pages_from_catagory(label, nums, tag=None):  #获取其他页面链接
    pages = []
    url = CATEGORY_BASE_URL
    if tag is None:
        label=urllib.parse.quote(label) #将中文转成url编码
    else:
        label=urllib.parse.quote(label)+"_"+ urllib.parse.quote(tag)

    for index in range(0,int(nums),100):
        u = url.format(label, index, str(time.time()).replace('.','')[:14])
        # print(u)
        page = get_page(u)
        pages.append(page)
    return pages

    
def findall_in_page(page,startpart,endpart):
    all_strings=[]
    end = 0
    while page.find(startpart,end) != -1:
        start =page.find(startpart,end)+len(startpart)
        end = page.find(endpart,start)
        string= page[start:end]
        all_strings.append(string)
    return all_strings

def pic_urls_from_pages(pages):
    pic_urls=[]
    for page in pages:
        urls = findall_in_page(page,'path":"','"')
        pic_urls.extend(urls)
    return pic_urls

def download_pics(url,n, path):
    r = requests.get(url)

    if not os.path.exists(path):
        os.makedirs(path)
    with open(path+'/'+str(n)+'.jpg', 'wb') as f:  #writebath
        f.write(r.content)
    thread_lock.release()   #下载完啦，解锁
        

def main_(label, nums,tag=None, output=None, mode='category')  :
    if mode == 'category':
        pages = pages_from_catagory(label, nums, tag)
    else:
        pages = pages_from_search(label, nums)
    
    path = output or label

    pic_urls = pic_urls_from_pages(pages)
    n=0
    for url in pic_urls:
        n+=1
        print("正在下载第{}张图片".format(n))
        thread_lock.acquire()
        t=threading.Thread(target=download_pics,args=(url,n, path))
        t.start()

def main(argv):
    parser = argparse.ArgumentParser(add_help=False, description='duitang Spider')
    parser.add_argument('--help', '-h', action='help', default=argparse.SUPPRESS, help='duitang Spider help')
    parser.add_argument('--search', '-s', help='search mode, enter the key you want to search, high priority')
    parser.add_argument('--category', '-c', help='category mode, enter the kind of pic you want')
    parser.add_argument('--tag', '-t', help='in category mode, the tag of category')
    parser.add_argument('--nums', '-n', help='the nums of pic, default 500')
    parser.add_argument('--output', '-o', help='Output directory,default key name')
    try:
        args = parser.parse_args(argv)

        search_key = args.search
        category = args.category
        if search_key is None and category is None:
            parser.print_usage()
            raise TypeError('you need set the one of search or category')

        nums = args.nums or '500'
        tag = args.tag
        output = args.output
        
        if not search_key is None:
            main_(search_key,nums,tag, output, 'search')
        else:
            main_(category, nums,tag, output)
    except Exception as e:
        print("Error, :", str(e))
        sys.exit(1)


if __name__=="__main__":
    main(sys.argv[1:])
        
