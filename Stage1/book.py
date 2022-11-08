from array import array
from shutil import move
import requests
import json
from bs4 import BeautifulSoup
from tqdm import tqdm
book_attrs = []

proxyHost = "43.248.99.36"
proxyPort = 56129
proxyMeta = "http://%(host)s:%(port)s" % {

    "host": proxyHost,
    "port": proxyPort,
}
proxies = {
    "http": proxyMeta,
    "https": proxyMeta
}
ipaddr = ""
with open("ip.txt") as f:
    ipaddr = f.readlines()
j = -1
with open("Book_id.txt") as f:
    str = f.readlines()
    k = 0
    for i in tqdm(range(len(str))):
        k += 1
        id = str[i][:-1]
        headers = {"User-Agent": "User-Agent: Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; 360SE)"}
        url = "https://book.douban.com/subject/" + id
        if k % 30 == 0:
            j += 1
            proxyHost = ipaddr[j][:-7]
            proxyPort = int(ipaddr[j][-6:-1])
            proxyMeta = "http://%(host)s:%(port)s" % {
                
                "host": proxyHost,
                "port": proxyPort,
            }
            proxies = {
                "http": proxyMeta,
                "https": proxyMeta
            }
        r = requests.get(url, headers=headers, proxies=proxies)
        content = r.content.decode("utf-8")
        soup = BeautifulSoup(content,'html.parser')
        if len(soup.findAll('div',attrs={'class':'intro'})) >= 2:
            intro = soup.findAll('div',attrs={'class':'intro'})[-2]
            author_intro = soup.findAll('div',attrs={'class':'intro'})[-1]    
        else:
            intro = soup.find('div',attrs={'class':'intro'})
            author_intro = None
        book_name = soup.find('meta',attrs={'property':'og:title'})
        info = soup.find('div',attrs={'id':'info'})
        rating = soup.find('div',attrs={'class':"rating_self clearfix"})
        book_attrs.append({})
        if book_name != None:
            book_attrs[-1]['name'] = book_name.attrs['content']
        else:
            book_attrs[-1]['name'] = "Not Found"
        book_attrs[-1]['id'] = id
        if info != None:
            book_attrs[-1]['info'] = info.text
        else:
            book_attrs[-1]['info'] = "None"
        if intro != None:
            book_attrs[-1]['intro'] = intro.text
        else:
            book_attrs[-1]['intro'] = "None"
        if author_intro != None:
            book_attrs[-1]['author intro'] = author_intro.text
        else:
            book_attrs[-1]['author intro'] = "None"
        if rating != None:
            book_attrs[-1]['rating'] = rating.text
        else:
            book_attrs[-1]['rating'] = "由于某些原因没有评分"
with open("book.json", "w") as fp:
    json.dump(book_attrs,fp,ensure_ascii=False,indent=4)
