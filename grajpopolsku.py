
from bs4 import BeautifulSoup
from Spolszczenie import Spolszczenie
import requests
from scrapperInterface import get_shorte,spin_descriptions
import json
import sys
sys.setrecursionlimit(10000)
import pickle
class GrajPoPolsku():
    def __init__(self):
        self.page_template = "https://grajpopolsku.pl/downloads/page/{0}/"
    def downloadFromPage(self,page:int):
        out=[]
        url = self.page_template.format(page)
        soup = BeautifulSoup(requests.get(url).text)
        links = soup.select(".title16 a")
        for link in links:
            out.append(self.downloadSingle(link['href']))
        return out
    def downloadSingle(self,url):
        soup = BeautifulSoup(requests.get(url).text)
        spolszczenie = Spolszczenie()
        spolszczenie.game = soup.select(".single-title")[0].string
        print(spolszczenie.game)
        try:
            spolszczenie.description = soup.select(".single-post-content header")[0].string
        except IndexError:
            spolszczenie.description = soup.select(".single-post-content .w3eden")[0].string
        spolszczenie.link = url
        try:
            spolszczenie.image = soup.select(".single-post-content .img-rounded")[0]['src']
        except IndexError:
            pass
        spolszczenie.affilate_link = get_shorte(url)
        return spolszczenie

p=GrajPoPolsku()
all_spolszczenia = []
counter=1
while True:
    spolszczenia = p.downloadFromPage(counter)
   
    counter+=1
    all_spolszczenia+=spolszczenia
    print(len(all_spolszczenia))
    if len(spolszczenia)==0:
        break

with open('grajpopolsku.json', 'w') as f:
    # Pickle the 'data' dictionary using the highest protocol available.
    serialized = [x.__dict__ for x in all_spolszczenia]
    json.dump(serialized, f)
