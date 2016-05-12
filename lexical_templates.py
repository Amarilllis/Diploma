#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'amarilllis'

import pickle
import random
import pymorphy2
from bs4 import BeautifulSoup
import re

def gen_template():
    template = {}

    template["root"] = ("person", "property")
    template["person"] = ("verb_right", "property")

    template["verb_right"] = ("property","end")
    template["adjective"] = ("property", "end")
    template["property"] = ("person", "adjective", "end")

    return template

def gen_review(template, words):
    review = ""

    cur = random.choice(template["root"])

    while cur != "end":
        next_word = random.choice(words[cur])
        review += next_word + " "
        cur = random.choice(template[cur])

    return review


def gen_words():
    words = {}

    words["person"] = ["я", "я", "я", "я", "я", "муж", "мама", "родители"]
    # автор отзыва упоминается чаще, чем другие люди. потом можно сделать по-человечески с вероятностями, пока так

    words["verb_right"] = []
    words["verb_left"] = []

    words["property"] = ["мощность", "подошва",  "резервуар",  "пар", "шнур",
            "вес", "ручка", "кабель", "накипь", "парогенератор", "утюг", "утюг",
            "утюг", "утюг", "утюг"]
    # как автор, так и утюг

    words["adjective"] = []

    with open("PrettyOutput.html", "r+") as f:
        page_source = f.read()
        soup = BeautifulSoup(page_source, "html.parser")

        for tr in soup.findAll('tr'):
            try:
                l, r = tr.findAll('td')
                print(l)
                print(r)
                expr = l.findAll(text=True).split()
                print("expr:")
                print(expr)
                raw_gram = r.findAll(text=True)

                gram = re.split("\[\]", raw_gram)

                # потом можно научиться добавлять биграммы, это сильно повысит точность и выигрыш перед ЦМ
                # todo: впилить согласование
                if gram == "прилагательные":
                    words["adjective"].append(expr[-2])

                if gram == "левые_глаголы":
                    words["verb_left"].append(expr[-2])

                if gram == "правые_глаголы":
                    words["verb_right"].append(expr[-1])

            except Exception:
                continue

    return words


template = gen_template()
pickle.dump(template, open("template_v1.p", "wb"))

words = gen_words()
# print(words)
pickle.dump(words, open("words_v1.p", "wb"))

# template = pickle.load(open("template_v1.p", "rb"))
# words = pickle.load(open("words_v1.p", "rb"))

rev = gen_review(template, words)
print(rev)