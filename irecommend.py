__author__ = 'amarilllis'

import grab
import pickle
import pandas as pd

def gather_models(url):
    g = grab.Grab()
    # g.setup(hammer_mode=True, hammer_timeouts=((2, 5), (10, 15), (20, 30)))
    g.go(url)

    links = []
    flinks = g.doc.select("//*[@id='content']/div[2]/div[2]/div/div/div[3]/a")

    for fl in flinks:
        # print(fl.attr("href"))
        # g.go(fl.attr("href"))
        links.append("http://irecommend.ru"+ fl.attr("href"))

    # print(links)
    return links

def gather_reviews(url):
    g = grab.Grab()
    # g.setup(hammer_mode=True, hammer_timeouts=((2, 5), (10, 15), (20, 30)))
    g.go(url)

    links = []
    flinks = g.doc.select("//*[@id=\"quicktabs_tabpage_12388_myreviewinfo\"]/div/div/div/ul/li/div/div/p/nobr/a")
    "//*[@id=\"quicktabs_tabpage_12388_myreviewinfo\"]/div/div[1]/div/ul/li/div/div/p/nobr/a"
    for fl in flinks:
        print(fl)
        links.append("http://irecommend.ru"+ fl.attr("href"))

    return links

def parse_review(url, df):
    x_rating = "<span class='on rating' itemprop='ratingValue'>5</span>"
    x_text = ""
    x_pro = ""
    x_con = ""
    g = grab.Grab()
    g.setup(hammer_mode=True, hammer_timeouts=((2, 5), (10, 15), (20, 30)))
    g.go(url)

    rating = g.doc.select(x_rating)
    text = g.doc.select(x_text)
    pro = g.doc.select(x_pro)
    con = g.doc.select(x_con)

    df = df.append(pd.Series([rating, text, pro, con]),
              index = ["rating", "text", "pro", "con"], ignore_index = True)
    return df

def get_all_models():
    model_links = []
    for i in range(22):
        model_links.extend(gather_models("http://irecommend.ru/taxonomy/term/3929?page=%d" % i))

    import pickle
    pickle.dump(model_links, open("irecommend_models.p", "wb"))

model_links = pickle.load(open("irecommend_models.p", "rb"))
print(len(model_links))
print(model_links[0])


import time
start = 20
all_revs = []
df = pd.DataFrame(columns=["rating", "text", "pro", "con"])
for i, model in enumerate(model_links):
    if i < start:
        continue
    if (i + 1) % 10 == 0:
        time.sleep(30)
    revs = gather_reviews(model)
    print(revs)
    if len(revs) == 0:
        print("Stopped at %d" % i)
        if i != start:
            pickle.dump(all_revs, open("irecommend_links_(%d_%d].p" % (start, i), "wb"))
        break
    all_revs.extend(revs)

