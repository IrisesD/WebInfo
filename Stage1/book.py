from array import array
from shutil import move
import requests
import json
from bs4 import BeautifulSoup
from tqdm import tqdm
book_attrs = []
with open("Book_id.txt") as f:
    str = f.readlines()
    for i in tqdm(range(len(str))):
        id = str[i][:-1]
        headers = {"User-Agent": "User-Agent: Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; 360SE)"}
        url = "https://book.douban.com/subject/" + id
        r = requests.get(url, headers=headers, verify=False)
        content = r.content.decode("utf-8")
        soup = BeautifulSoup(content,'html.parser')
        intro = soup.find('span',attrs={'class':'all hidden'})[-2]
        author_intro = soup.find('span',attrs={'class':'all hidden'})[-1]
        book_name = soup.find('meta',attrs={'property':'og:title'})
        info = soup.find('div',attrs={'id':'info'})
        rating = soup.find('div',attrs={'class':"rating_self clearfix"})
        book_attrs.append({})
        book_attrs[-1]['name'] = book_name.attrs['content']
        book_attrs[-1]['id'] = id
        book_attrs[-1]['info'] = info.text
        book_attrs[-1]['intro'] = intro.text
        book_attrs[-1]['author intro'] = author_intro.text
        book_attrs[-1]['rating'] = rating.text
with open("book.json", "w") as fp:
    json.dump(book_attrs,fp,ensure_ascii=False,indent=4)
