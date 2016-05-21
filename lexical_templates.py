#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'amarilllis'

import pickle
import random
from pymorphy2 import MorphAnalyzer
from bs4 import BeautifulSoup
import re

dative_verbs = set([u"нравиться", u"подарить", u"советовать", u"понравиться",
                    u"посоветовать", u"рекомендовать", u"порекомендовать"])

stop_words = set([u"был", u"такой", u"сей", u"этот", u"данный", u"есть", u"сам"])

ok_words = set(["start"])

def gen_template():
    template = {}

    template["root"] = ("property_1", "person_2", "property_3", "adjective_4")

    template["property_1"] = ("person_1",)
    template["person_1"] = ("verb_right_1",)
    template["verb_right_1"] = ("end",)

    template["person_2"] = ("verb_right_2",)
    template["verb_right_2"] = ("property_2",)
    template["property_2"] = ("end",)

    template["property_3"] = ("adjective_3",)
    template["adjective_3"] = ("end", "end", "comma_0")

    template["adjective_4"] = ("property_4",)
    template["property_4"] = ("end", "end", "comma_0")

    template["comma_0"] = ("property_3","adjective_4")

    # template["end"] = (".",)

    return template

def agree(w1, w2, t1, t2):
    if t1 == "comma" or t2 == "comma":
        return w1, w2

    morph = MorphAnalyzer()
    raw_cur_tags = morph.tag(w1)[-1]
    raw_next_tags = morph.tag(w1)[-1]

    cur_tags = re.findall(r"\w+", str(raw_cur_tags))
    next_tags = re.findall(r"\w+", str(raw_next_tags))

    if t1[:-2] == "person":
        if t2[:-2] == "verb_right":
            if morph.normal_forms(w2)[0] in dative_verbs:
                w1 = morph.parse(w1)[0].inflect({"datv"}).word

    if t1[:-2] == "verb_right":
        if t2[:-2] == "property":
            pass
        if t2[:-2] == "person":
            if cur_tags[3] == "tran":
                w2 = morph.parse(w2)[0].inflect({"accs"}).word
            else:
                w2 = morph.parse(w2)[0].inflect({"nomn"}).word
                #gender with nomn only
                gender = next_tags[2]
                if gender == "inan":
                    gender = next_tags[3]
                w1 = morph.parse(w1)[0].inflect({gender}).word

    if t1[:-2] == "adjective":
        if t2[:-2] == "property":
            #gender
            gender = next_tags[2]
            if gender == "inan":
                gender = next_tags[3]
            try:
                w1 = morph.parse(w1)[0].inflect({gender}).word
            except Exception:
                print("fuck")
                print(w1, w2)

    if t1[:-2] == "property":
        if t2[:-2] == "person":
            pass
        if t2[:-2] == "adjective":
            gender = cur_tags[2]
            if gender == "inan":
                gender = cur_tags[3]
            try:
                w2 = morph.parse(w2)[0].inflect({gender}).word
            except Exception:
                print("fuck")
                print(w1, w2)


    #w1 = morph.parse(w1)[0].inflect({}).word
    return w1, w2

def gen_review(template, words):
    review = []
    types = []

    cur = random.choice(template["root"])
    prev = ""

    while cur != "end":
        expr = ""
        while expr not in ok_words:
            word = random.choice(words[cur[:-2]])
            if prev == "" or prev == "," or cur == ",":
                expr = "start"
            else:
                expr = prev + " " + cur

        review += [word]
        types += [cur]
        cur = random.choice(template[cur])

    for i in range(1, len(review)):
        review[i-1], review[i] = agree(review[i-1], review[i], types[i-1], types[i])

    return " ".join(review)


def gen_words():
    words = {}

    words["person"] = [u"я", u"я", u"я", u"муж", u"мама", u"родители"]
    # автор отзыва упоминается чаще, чем другие люди. потом можно сделать по-человечески с вероятностями, пока так

    words["verb_right"] = []
    words["verb_left"] = []
    words["comma"] = [","]

    words["property"] = [u"мощность", u"подошва",  u"резервуар",  u"пар", u"шнур",
            u"вес", u"ручка", u"кабель", u"накипь", u"парогенератор", u"утюг", u"утюг",
            u"утюг", u"утюг", u"утюг", u"провод", u"инструкция"]
    # как автор, так и утюг

    words["adjective"] = []

    with open("PrettyOutput.html", "r+") as f:
        page_source = f.read()
        soup = BeautifulSoup(page_source, "html.parser")

        for tr in soup.findAll('tr'):
            try:
                l, r = tr.findAll('td')

                raw_expr = l.findAll(text=True)

                ok_words.add(raw_expr)

                expr = raw_expr[0].split()

                raw_gram = r.findAll(text=True)

                gram = raw_gram[0].split()[-1]

                if gram == u"[прилагательные]":
                    if not expr[-2] in stop_words:
                        words["adjective"].append(expr[-2]).decode("utf-8")

                if gram == u"[левые_глаголы]":
                    if not expr[-2] in stop_words:
                        words["verb_left"].append(expr[-2]).decode("utf-8")

                if gram == u"[правые_глаголы]":
                    if not expr[-1] in stop_words:
                        words["verb_right"].append(expr[-1]).decode("utf-8")

            except Exception:
                continue

    return words

template = gen_template()

pickle.dump(template, open("template_v1.p", "wb"))

words = gen_words()
print(words)
pickle.dump(words, open("words_v1.p", "wb"))
'''

template = pickle.load(open("template_v1.p", "rb"))
words = pickle.load(open("words_v1.p", "rb"))
'''

for i in range(3):
    rev = gen_review(template, words)
    print(rev)