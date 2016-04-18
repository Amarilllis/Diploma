__author__ = 'amarilllis'

import grab
# from bs4 import BeautifulSoup

def gather_models(url):
    g = grab.Grab()
    g.go(url)

    links = g.doc.select("//*[@id='content']/div[2]/div[2]/div[2]/div/div[3]/a")
    print(links)
def gather_reviews(url):
    pass

def parse_review(url):
    pass


model_links = gather_models("http://irecommend.ru/taxonomy/term/3929")