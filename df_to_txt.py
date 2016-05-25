__author__ = 'amarilllis'
import pandas as pd
df = pd.read_csv("irecommend.csv", sep=',', encoding='utf-8')
with open("irecommend_pos.txt", "w+") as f:
    f.write(df[df["rating"] > 3]["text"])
    f.close()