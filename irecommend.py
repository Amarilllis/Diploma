__author__ = 'amarilllis'

import grab
import pickle
import pandas as pd

def gather_models(url):
    g = grab.Grab()
    g.setup(hammer_mode=True, hammer_timeouts=((2, 5), (10, 15), (20, 30)))
    g.go(url)

    links = []
    flinks = g.doc.select("//*[@id='content']/div[2]/div[2]/div/div/div[3]/a")

    for fl in flinks:
        print(fl.attr("href"))
        # g.go(fl.attr("href"))
        links.append("http://irecommend.ru"+ fl.attr("href"))

    print(links)
    return links

def gather_reviews(url, df):
    g = grab.Grab()
    g.setup(hammer_mode=True, hammer_timeouts=((2, 5), (10, 15), (20, 30)))
    g.go(url)

    links = []
    flinks = g.doc.select("//*[@id='content']/div[2]/div[2]/div/div/div[3]/a")

    for fl in flinks:
        print(fl.attr("href"))
        links.append("http://irecommend.ru"+ fl.attr("href"))

    print(links)
    return links

def parse_review(url, df):
    x_rating = "<span class='on rating' itemprop='ratingValue'>5</span>"
    g = grab.Grab()
    g.setup(hammer_mode=True, hammer_timeouts=((2, 5), (10, 15), (20, 30)))
    g.go(url)

    pass

def get_all_models():
    model_links = []
    for i in range(22):
        model_links.extend(gather_models("http://irecommend.ru/taxonomy/term/3929?page=%d" % i))

    import pickle
    pickle.dump(model_links, open("irecommend_models.p", "wb"))

model_links = pickle.load(open("irecommend_models.p", "rb"))
print(len(model_links))

df = pd.DataFrame
for model in model_links:
    gather_reviews(model, df)
    break