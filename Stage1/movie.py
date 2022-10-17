from array import array
from shutil import move
import requests
import json
from bs4 import BeautifulSoup
from tqdm import tqdm

movie_attrs = []
with open("Movie_id.txt") as f:
    str = f.readlines()
    for i in tqdm(range(10)):
        id = str[i][:-1]
        headers = {"User-Agent": "User-Agent: Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; 360SE)"}
        url = "https://movie.douban.com/subject/" + id
        r = requests.get(url,headers=headers)
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
        movie_attrs[-1]['name'] = movie_name.attrs['content']
        movie_attrs[-1]['id'] = id
        movie_attrs[-1]['info'] = info.text
        movie_attrs[-1]['staff'] = []
        for i in range(len(staff_name)):
            movie_attrs[-1]['staff'].append(staff_name[i].text + ":" + staff_role[i].text)
        movie_attrs[-1]['intro'] = intro.text
        movie_attrs[-1]['rating'] = rating.text
with open("movie.json", "w") as fp:
    json.dump(movie_attrs,fp,ensure_ascii=False,indent=4)
