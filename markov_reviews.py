__author__ = 'amarilllis'
import pickle
import random

def generate_trigram(words):
    if len(words) < 3:
        return
    for i in range(len(words) - 2):
        yield (words[i], words[i+1], words[i+2])

def prepare_text(text):
    import re
    body = " ".join(word.lower() for word in text.split())
    body = re.sub("(\.\.)+|(\))+|(\()+", "", body)
    return ("begin now " + body + " end")


def gen_review(chain):
    new_review = []
    sword1 = "begin"
    sword2 = "now"

    while True:
        print(sword1, sword2)
        sword1, sword2 = sword2, random.choice(chain[(sword1, sword2)])
        if sword2 == "end":
            break
        new_review.append(sword2)

    return ' '.join(new_review)

def gen_chain(text):
    print(len(text))
    chain = {}
    for raw_line in text:
        line = prepare_text(raw_line)
        print(raw_line)
        print(line)
        print("++++++")
        words = line.split()
        for word1, word2, word3 in generate_trigram(words):
            key = (word1, word2)
            if key in chain:
                chain[key].append(word3)
            else:
                chain[key] = [word3]
    return chain

with open("many_pos.pkl", "rb") as pos:
    rev_pos = pickle.load(pos)
chain = gen_chain(rev_pos)
pickle.dump(chain, open("chain.p", "wb" ))

chain = pickle.load(open("chain.p", "rb"))
print(gen_review(chain))
'''

# print(rev)
print(len(rev_pos))



with open("many_neut.pkl", "rb") as neut:
    rev_neut = pickle.load(neut)
# print(rev_neut)
# print(len(rev_neut))

with open("many_neg.pkl", "rb") as neg:
    rev_neg = pickle.load(neg)
# print(rev_neg)
# print(len(rev_neg))
'''