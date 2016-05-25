__author__ = 'amarilllis'

import grab
import pickle
import pandas as pd
import time
import random

user_agents = ["Chrome 37.0.2062.124", "Chrome 41.0.2228.0",
               "Chrome 11.0.697.0", "Firefox 36.0",
               "Firefox 33.0", "Firefox 40.1",
               "Opera 12.16", "Opera 12.14"]

def gather_models(url):
    g = grab.Grab()
    g.go(url)

    links = []
    flinks = g.doc.select("//*[@id='content']/div[2]/div[2]/div/div/div[3]/a")

    for fl in flinks:
        links.append("http://irecommend.ru"+ fl.attr("href"))

    # print(links)
    return links

def gather_reviews(url, proxy):
    g = grab.Grab()
    # g.setup(proxy=proxy)
    g.go(url)

    links = []
    flinks = g.doc.select("//*[@id=\"quicktabs_tabpage_12388_myreviewinfo\"]/div/div/div/ul/li/div/div/p/nobr/a")
    "//*[@id=\"quicktabs_tabpage_12388_myreviewinfo\"]/div/div[1]/div/ul/li/div/div/p/nobr/a"
    for fl in flinks:
        print(fl)
        links.append("http://irecommend.ru"+ fl.attr("href"))

    return links

def parse_review(url, df):
    x_rating = "//span[@itemprop=\"ratingValue\"]"
    x_text = "//div[@itemprop=\"reviewBody\"]"
    x_pro = "//span[@class=\"plus\"]"
    x_con = "//span[@class=\"minus\"]"

    g = grab.Grab()
    ua = random.choice(user_agents)
    print(ua)
    g.go(url, user_agent="%s" % ua)

    rating = g.doc.select(x_rating).text()
    text = " ".join(g.doc.select(x_text).text_list())

    text = text.replace(".", ". ")
    text = text.replace(",", ", ")
    text = text.replace("!", "! ")

    try:
        pro = " ".join(g.doc.select(x_pro).text_list())
        con = " ".join(g.doc.select(x_con).text_list())
    except Exception:
        pro = float('NaN')
        con = float('NaN')
    # time.sleep(120)

    df.loc[len(df)] = [rating, text, pro, con]
    return df

def get_all_models():
    model_links = []
    for i in range(22):
        model_links.extend(gather_models("http://irecommend.ru/taxonomy/term/3929?page=%d" % i))

    import pickle
    import time
    import random
    pickle.dump(model_links, open("irecommend_models.p", "wb"))

model_links = pickle.load(open("irecommend_models.p", "rb"))

df = pd.read_csv("irecommend.csv", sep=',', encoding='utf-8')
# df.drop("id", axis=1, inplace=True)

'''
all_revs = []
for i, model in enumerate(model_links):
    with open("proxy.txt", "r+") as prx:
        failed = True
        proxylist = prx.readlines()
        while failed:
            # try:
                num = random.randint(0, 1383)
                proxy = proxylist[num]
                print(proxy)
                time.sleep(num % 20)
                revs = gather_reviews(model, proxy)
                print(revs)

                all_revs.extend(revs)
                failed = False
            # except Exception:
            #     pass

pickle.dump(all_revs, open("irecommend_links_with_proxy.p", "wb"))
'''


revlinks = pickle.load(open("irecommend_links_with_proxy.p", "rb"))
print(len(revlinks))
# used_links = set()
used_links = pickle.load(open("used_links.p", "rb"))

for link in revlinks:
    if link in used_links:
        continue
    print(link)
    try:
    # if True:
        df = parse_review(link, df)
        print(df.tail())

        used_links.add(link)
        df.to_csv("irecommend.csv", columns=["rating", "text", "pro", "con"], index=False, sep=',', encoding='utf-8')
    except Exception:
        pickle.dump(used_links, open("used_links.p", "wb"))
        print("fuck it")
        break
    time.sleep(random.randint(1, 10))

df.to_csv("irecommend.csv", columns=["rating", "text", "pro", "con"], index=False, sep=',', encoding='utf-8')
