
from bs4 import BeautifulSoup
from Spolszczenie import Spolszczenie
import requests
from scrapperInterface import get_shorte,spin_descriptions
import json
import sys
sys.setrecursionlimit(10000)
import pickle
class SpolszczeniaPL():
    def __init__(self):
        
        self.page_template = "http://www.spolszczenia.pl/gry/{0}/30/newest"
        self.next_page_selector = ".PaginationNext"
        self.base_image_url = "http://spolszczenia.pl"
        self.product_item = ".ProductItem"
    def downloadFromPage(self,page:int):
        out=[]
        url = self.page_template.format(page)
        soup = BeautifulSoup(requests.get(url).text)
        items = soup.select(self.product_item)
        for item in items:
            spolszczenie = Spolszczenie()
            spolszczenie.description = item.select("p:nth-of-type(2)")[0].string
            spolszczenie.game = item.select('.ProductItemTitle a')[0].string
            spolszczenie.link = item.select('.ProductItemTitle a')[0]['href'].replace("szczegoly", "pobierz")
            spolszczenie.image = self.base_image_url+item.select(".ProductItemImageField img")[0]['src']
            spolszczenie.affilate_link = get_shorte(spolszczenie.link)
            out.append(spolszczenie)
        return out
p=SpolszczeniaPL()
all_spolszczenia = []
counter=1
while True:
    spolszczenia = p.downloadFromPage(counter)
   
    counter+=1
    all_spolszczenia+=spolszczenia
    print(len(all_spolszczenia))
    if len(spolszczenia)==0:
        break

with open('spolszczeniapl.json', 'w') as f:
    # Pickle the 'data' dictionary using the highest protocol available.
    serialized = [x.__dict__ for x in all_spolszczenia]
    json.dump(serialized, f)
