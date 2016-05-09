__author__ = 'amarilllis'

import pickle
import random
import pymorphy2

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

    words["person"] = []
    words["verb_right"] = []
    words["verb_left"] = []
    words["property"] = []
    words["adjective"] = []
    
    return words

template = gen_template()
pickle.dump(template, open("template_v1.p", "wb"))

'''
template = pickle.load(open("template_v1.p", "rb"))

'''