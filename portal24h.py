
from bs4 import BeautifulSoup
from Spolszczenie import Spolszczenie
import requests
import re
from scrapperInterface import get_shorte,spin_descriptions
import json
import sys
sys.setrecursionlimit(10000)
import pickle
class OutOfPages(Exception):
    pass
class Portal24H():
    def __init__(self):
        self.base_url = "http://www.portal24h.pl/spolszczenia-gier/"
    def getCategories(self):
        soup = BeautifulSoup(requests.get(self.base_url).text)
        links = soup.select('h3 a')
        return [x['href']+"orderby-2/page-{0}/" for x in links]
    def downloadFromCategory(self,category):
        counter =1
        out=[]
       
        while True:
            link = category.format(counter)
            try:
                spolszczenia = self.downloadFromPage(link)
            except OutOfPages:
                break
            out+=spolszczenia
            counter+=1
        return out 
    def downloadFromPage(self,link):
        print("Page: ",link)
        out=[]
        text=requests.get(link).text
        
        if """404""" in text:raise OutOfPages()
        soup = BeautifulSoup(text)
        links = soup.select(".remositoryfileblock a")
       
        for link in links:
            res=self.downloadSingle(link['href'])
            if res!=None:
                out.append(res)
        return out
    def downloadSingle(self,link):
    
        soup =BeautifulSoup(requests.get(link).text)
        
        entry = soup.select("#remository")[0]
        spolszczenie = Spolszczenie()
        try:
            spolszczenie.game = re.search('<h2>(.+)<a', str(soup.select("#remositoryfileinfo")[0])).group(1)
        except:
            return None
        spolszczenie.link = link
        spolszczenie.affilate_link=get_shorte(link)
        try:
            spolszczenie.description = re.search('(?s)<dl>\s*<dt>Opis:</dt>\s*<dd>\s*(.*?)</dd>\s*<dt>[A-Z]', str(soup.select("#remositoryfileinfo")[0])).group(1)
        except:
            spolszczenie.description=''
        print(spolszczenie.game)
        print(spolszczenie.description)
        return spolszczenie
p=Portal24H()
all_spolszczenia = []
categories = p.getCategories()
for category in categories:
    all_spolszczenia+=p.downloadFromCategory(category)
    print(len(all_spolszczenia))
with open('portal24h.json', 'w') as f:
    # Pickle the 'data' dictionary using the highest protocol available.
    serialized = [x.__dict__ for x in all_spolszczenia]
    json.dump(serialized, f)
