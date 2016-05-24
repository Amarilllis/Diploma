__author__ = 'amarilllis'

import grab
import pickle
import pandas as pd
from bs4 import BeautifulSoup

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
    # print(df.head())
    g = grab.Grab()
    g.go(url)
    page = g.response.body
    soup = BeautifulSoup(page, "html.parser")

    rating = soup.find_all("span", itemprop="ratingValue")[0].contents[0]
    rating = int(rating)

    text = soup.find_all("div", itemprop="reviewBody")[0].contents[0]
    try:
        pro = soup.find_all("span", class_="plus").contents[0]
        con = soup.find_all("span", class_="minus").contents[0]
    except Exception:
        pro = float('NaN')
        con = float('NaN')
    
    df.loc[len(df)] = [rating, text, pro, con]
    print(rating)
    print(text)
    print(pro)
    print(con)
    return df

def parse_review_grab_only(url, df):
    x_rating = "//*[@id=\"quicktabs_tabpage_12388_myreviewinfo\"]/div/div/div[3]/div/div[1]/span"

    "//*[@id=\"quicktabs_tabpage_12388_myreviewinfo\"]/div/div/div[3]/div/div[1]/span"

    x_text = "//*[@id=\"quicktabs_tabpage_12388_myreviewinfo\"]/div/div/div[6]/div[1]/p"

    x_pro = "//*[@id=\"quicktabs_tabpage_12388_myreviewinfo\"]/div/div/div[5]/div[1]/span"

    x_con = "//*[@id=\"quicktabs_tabpage_12388_myreviewinfo\"]/div/div/div[5]/div[2]/span"
    g = grab.Grab()
    g.go(url)
    page = g.request_body


    rating = g.doc.select(x_rating).text()
    text = " ".join(g.doc.select(x_text).text_list())

    try:
        pro = g.doc.select(x_pro).text()
        con = g.doc.select(x_con).text()
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
    pickle.dump(model_links, open("irecommend_models.p", "wb"))

model_links = pickle.load(open("irecommend_models.p", "rb"))

# print(len(model_links))
# print(model_links[0])


import time
import random

# df = pd.DataFrame(columns=["rating", "text", "pro", "con"])
df = pd.read_csv("irecommend.csv", sep=',', encoding='utf-8')

# print(list(df))
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


df = parse_review("http://irecommend.ru/content/blizok-k-sovershenstvu", df)

print("df:")
print(df.tail())

'''
revlinks = pickle.load(open("irecommend_links_with_proxy.p", "rb"))
used_links = set()


for link in revlinks:
    print(link)
    if link in used_links:
        continue
    # try:
    if True:
        df = parse_review(link, df)
        print(df.head())
        used_links.add(link)
        df.to_csv("irecommend.csv", columns=["id", "rating", "text", "pro", "con"], index=False, sep=',', encoding='utf-8')
        # print("success")
    # except Exception:
    #     pass
    time.sleep(random.randint(10, 60))

df.to_csv("irecommend.csv", sep=',', encoding='utf-8')

'''