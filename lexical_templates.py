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
    template["person"] = ("verb_right",) #, "property")

    template["verb_right"] = ("property", "property", "property", "property",
                              "property", "property", "property", "property", "end")
    template["adjective"] = ("property", "property", "property", "property",
                             "property", "property", "property", "property", "end")
    template["property"] = ("person", "adjective", "person", "adjective",
                            "person", "adjective", "person", "adjective", "end")

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

    words["person"] = [u"я", u"я", u"я", u"я", u"я", u"муж", u"мама", u"родители"]
    # автор отзыва упоминается чаще, чем другие люди. потом можно сделать по-человечески с вероятностями, пока так

    words["verb_right"] = []
    words["verb_left"] = []

    words["property"] = [u"мощность", u"подошва",  u"резервуар",  u"пар", u"шнур",
            u"вес", u"ручка", u"кабель", u"накипь", u"парогенератор", u"утюг", u"утюг",
            u"утюг", u"утюг", u"утюг"]
    # как автор, так и утюг

    words["adjective"] = []

    with open("PrettyOutput.html", "r+") as f:
        page_source = f.read()
        soup = BeautifulSoup(page_source, "html.parser")

        for tr in soup.findAll('tr'):
            try:
                l, r = tr.findAll('td')

                raw_expr = l.findAll(text=True)

                expr = raw_expr[0].split()

                raw_gram = r.findAll(text=True)

                gram = raw_gram[0].split()[-1]

                # потом можно научиться добавлять биграммы, это сильно повысит точность и выигрыш перед ЦМ
                # todo: впилить согласование
                if gram == u"[прилагательные]":
                    words["adjective"].append(expr[-2]).decode("utf-8")

                if gram == u"[левые_глаголы]":
                    words["verb_left"].append(expr[-2]).decode("utf-8")

                if gram == u"[правые_глаголы]":
                    words["verb_right"].append(expr[-1]).decode("utf-8")

            except Exception:
                continue

    return words


template = gen_template()
# print(template)
pickle.dump(template, open("template_v1.p", "wb"))

words = gen_words()
print(words)
pickle.dump(words, open("words_v1.p", "wb"))

# template = pickle.load(open("template_v1.p", "rb"))
# words = pickle.load(open("words_v1.p", "rb"))

rev = gen_review(template, words)
print(rev)