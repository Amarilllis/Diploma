__author__ = 'amarilllis'

import pickle
import random

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

    

    return review