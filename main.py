import nltk
import random
import math
from nltk.corpus import wordnet as wn
from nltk.stem.snowball import SnowballStemmer
import spacy
import re
import queue
import requests

sp = spacy.load('en_core_web_sm')

'freq of english alphabet letters '
alphabet = [(0.1, ' '), (0.082, 'a'),(0.015, 'b'),(0.027, 'c'),(0.043, 'd'),(0.13, 'e'),(0.022, 'f'),(0.021, 'g'),(0.061, 'h'),(0.07, 'i'),
             (0.0015, 'j'),(0.0077, 'k'),(0.04, 'l'),(0.024, 'm'),(0.067, 'n'),(0.075, 'o'),(0.019, 'p'),(0.00095, 'q'),(0.06, 'r'),
             (0.063, 's'),(0.091, 't'),(0.028, 'u'),(0.0098, 'v'),(0.024, 'w'),(0.0015, 'x'),(0.02, 'y'),(0.00074, 'z'),]
'Code responsible for creating Huffman tree'


class HuffmanNode(object):
    def __init__(self, left=None, right=None, root=None):
        self.left = left
        self.right = right
        self.root = root

    def children(self):
        return ((self.left, self.right))


def create_tree(frequencies):
    p = queue.PriorityQueue()
    for value in frequencies:
        p.put(value)
    while p.qsize() > 1:
        try:
            l, r = p.get(), p.get()
            node = HuffmanNode(l, r)
            p.put((l[0] + r[0], node))
        except:
            TypeError
    return p.get()


def walk_tree(node, prefix="", code={}):
    if isinstance(node[1].left[1], HuffmanNode):
        walk_tree(node[1].left, prefix + "0", code)
    else:
        code[node[1].left[1]] = prefix + "0"
    if isinstance(node[1].right[1], HuffmanNode):
        walk_tree(node[1].right, prefix + "1", code)
    else:
        code[node[1].right[1]] = prefix + "1"
    return (code)


def dic_bin_codes(freq):
    node = create_tree(freq)
    code = walk_tree(node)
    dic = {}
    for i in sorted(freq, reverse=True):
        try:
            dic[i[1]] = code[i[1]]
        except:
            KeyError
    return dic
'End of Huffman tree section'


def hd_msg(message, alph):
    res = []
    for a in message:
        a = alph[a]
        res.append(a)
    return res


def remove_suffix(text):
    res = []
    stemmer = SnowballStemmer(language="english")

    for word in text:
        a = stemmer.stem(word)
        res.append(a)
    return res


def pos_tag(text):
    res = []
    sen = sp(text)
    for word in sen:
        a = word.pos_
        res.append(a)
    return res


if __name__ == "__main__":
    '''
    'coding alphabet and secret message letters'
    alp_cl = dic_bin_codes(alphabet)
    print(alp_cl)
    secret = "text to split into sentences"
    secret_list = list(secret)
    print(secret_list)
    msg = hd_msg(secret_list, alp_cl)
    print(msg)
    '''

    '''
    'suffix removal and pos tagging'
    secret = "friday's child is loving and giving"
    tokens = nltk.word_tokenize(secret)
    suff_less = remove_suffix(tokens)
    print(suff_less)
    print(spacy.explain(pos_tag(' '.join(suff_less))))
    '''
    print(wn.synset('love.n.02').lemmas()[0].name())