import requests
import urllib.parse
import threading


thread_lock =threading.BoundedSemaphore(value=10)#设置最大线程锁

def get_page(url):  #通过URL获取数据
    page = requests.get(url)
    page = page.content #将bytes 转成str字符串
    page = page.decode('utf-8')
    return page
#print(get_page('https://www.duitang.com/napi/blog/list/by_search/?kw=%E6%A0%A1%E8%8A%B1&&start=0&limit=1000'))
#36
#label:校花
def pages_from_duitang(label):  #获取其他页面链接
    pages = []
    url='https://www.duitang.com/napi/blog/list/by_search/?kw={}&start={}&limit=1000'
    label=urllib.parse.quote(label) #将中文转成url编码
    for index in range(0,3600,100):
        u = url.format(label,index)
        print(u)
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

def download_pics(url,n):
    r = requests.get(url)
    path = 'pics/'+str(n)+'.jpg'
    with open(path,'wb') as f:  #writebath
        f.write(r.content)
    thread_lock.release()   #下载完啦，解锁
        

def main(label):
    pages = pages_from_duitang(label)
    pic_urls = pic_urls_from_pages(pages)
    n=0
    for url in pic_urls:
        n+=1
        print("正在下载第{}张图片".format(n))
        thread_lock.acquire()
        t=threading.Thread(target=download_pics,args=(url,n))
        t.start()
        
main('头像')
        
