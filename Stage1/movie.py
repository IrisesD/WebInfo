from array import array
from shutil import move
import requests
import json
from bs4 import BeautifulSoup
from tqdm import tqdm

movie_attrs = []

proxyHost = "43.248.79.156"
proxyPort = 62906
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
with open("Movie_id.txt") as f:
    str = f.readlines()
    k = 0
    for i in tqdm(range(len(str))):
        k += 1
        id = str[i][:-1]
        headers = {"User-Agent": "User-Agent: Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; 360SE)"}
        url = "https://movie.douban.com/subject/" + id
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
        r = requests.get(url,headers=headers,proxies=proxies)
        content = r.content.decode("utf-8")
        soup = BeautifulSoup(content,'html.parser')
        intro = soup.find('div',attrs={'class':'intro'})
        if intro == None:
            intro = soup.find('span',attrs={'property':'v:summary'})
        staff_name = soup.findAll('span',attrs={'class':'name'})
        staff_role = soup.findAll('span',attrs={'class':'role'})
        movie_name = soup.find('meta',attrs={'property':'og:title'})
        info = soup.find('div',attrs={'id':'info'})
        rating = soup.find('div',attrs={'class':"rating_self clearfix"})
        movie_attrs.append({})
        if movie_name != None:
            movie_attrs[-1]['name'] = movie_name.attrs['content']
        else:
            movie_attrs[-1]['name'] = "未找到"
        movie_attrs[-1]['id'] = id
        if info != None:
            movie_attrs[-1]['info'] = info.text
        else:
            movie_attrs[-1]['info'] = "None"
        movie_attrs[-1]['staff'] = []
        if staff_name != None and staff_role != None:
            for i in range(len(staff_name)):
                movie_attrs[-1]['staff'].append(staff_name[i].text + ":" + staff_role[i].text)
        else:
            movie_attrs[-1]['staff'].append('None')
        if intro != None:
            movie_attrs[-1]['intro'] = intro.text
        else:
            movie_attrs[-1]['intro'] = "None"
        if rating != None:
            movie_attrs[-1]['rating'] = rating.text
        else:
            movie_attrs[-1]['rating'] = "由于某些原因没有评分"
with open("movie.json", "w") as fp:
    json.dump(movie_attrs,fp,ensure_ascii=False,indent=4)
