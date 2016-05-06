__author__ = 'amarilllis'

import pickle
import random

def gen_template():
    template = {}

    template["root"] = ("pronoun","property")
    template["person"] = ("verb_right","property")
    # maybe no property here

    template["verb_right"] = ("property",)
    template["adjective"] = ("property",)
    template["property"] = ("person",)

    return template