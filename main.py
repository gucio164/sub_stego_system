import nltk
import random
import math
from nltk.corpus import wordnet as wn
from nltk.stem.snowball import SnowballStemmer
import spacy
import re
import queue
import requests
from bitarray import bitarray
from itertools import product
import random

sp = spacy.load('en_core_web_sm')
stemmer = SnowballStemmer(language="english")

random.seed(9001)

'freq of english alphabet letters '
alphabet = [(0.1, ' '), (0.082, 'a'), (0.015, 'b'), (0.027, 'c'), (0.043, 'd'), (0.13, 'e'), (0.022, 'f'), (0.021, 'g'),
            (0.061, 'h'), (0.07, 'i'),
            (0.0015, 'j'), (0.0077, 'k'), (0.04, 'l'), (0.024, 'm'), (0.067, 'n'), (0.075, 'o'), (0.019, 'p'),
            (0.00095, 'q'), (0.06, 'r'),
            (0.063, 's'), (0.091, 't'), (0.028, 'u'), (0.0098, 'v'), (0.024, 'w'), (0.0015, 'x'), (0.02, 'y'),
            (0.00074, 'z')]
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


def dic_bin_codes_decode(freq):
    node = create_tree(freq)
    code = walk_tree(node)
    dic = {}
    for i in sorted(freq, reverse=True):
        try:
            dic[i[1]] = bitarray(code[i[1]])
        except:
            KeyError
    return dic


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
    for word in text:
        a = stemmer.stem(word)
        res.append(a)
    return res


def add_suffix(text, orginal):
    res = []
    if len(text) == len(orginal):
        for word, org in zip(text, orginal):
            a = stemmer.stem(org)
            if word == a:
                res.append(org)
            else:
                print('')

    return res


def pos_tag(text):
    res = []
    sen = sp(text)
    for word in sen:
        a = word.pos_
        res.append(a)
    return res


def decode(message):
    alp_decode = dic_bin_codes_decode(alphabet)
    temp = ''.join(message)
    msg_decode = bitarray(temp).decode(alp_decode)
    print(''.join(msg_decode))


def list_synonyms(word, pos):
    synonyms = []
    if pos == 'NOUN':
        pos = wn.NOUN
    if pos == 'VERB':
        pos = wn.VERB
    for syn in wn.synsets(word, pos):
        for i in syn.lemmas():
            if i.name() == word:
                continue
            synonyms.append(i.name())
    return synonyms


def check_similarity(word, synon):
    dic = {}
    for syn in synon:
        doc_1 = sp(word)
        doc_2 = sp(syn)
        similarity = doc_1.similarity(doc_2)
        dic.update({syn: similarity})
    return dic



if __name__ == "__main__":
    'coding alphabet and secret message letters'

    alp_code = dic_bin_codes(alphabet)
    #print(alp_code)
    secret = "text to split into sentences"
    secret_list = list(secret)
    #print(secret_list)
    msg = hd_msg(secret_list, alp_code)
    msg = ''.join(msg)
    print(msg)

    '''
    print(list_synonyms('love', 'NOUN'))
    similarity = check_similarity('text', list_synonyms('text', 'NOUN'))
    similarity = {y: x for x, y in similarity.items()}
    print(similarity)
    similarity_code = dic_bin_codes(list(similarity.items()))
    print(similarity_code)
    '''

    'suffix removal and pos tagging'
    secret = "friday's child is loving and giving"
    tokens = nltk.word_tokenize(secret)
    suff_less_secret = remove_suffix(tokens)
    #print(suff_less_secret)
    #print(pos_tag(' '.join(suff_less_secret)))

    orig_text = open('covert.txt', 'r')
    words = nltk.word_tokenize(orig_text.read())

    while(1):
        rand_nr = random.randint(0, len(words))
        suff_less_word = stemmer.stem(words[rand_nr])
        word_pos = pos_tag(suff_less_word)
        if word_pos[0] == 'NOUN':
            print("")
            similarity = check_similarity(suff_less_word, list_synonyms(suff_less_word, 'NOUN'))
            similarity = {y: x for x, y in similarity.items()}
            similarity_code = dic_bin_codes(list(similarity.items()))
            similarity_code = {y: x for x, y in similarity_code.items()}
            print(similarity_code)
            break
        elif word_pos[0] == 'VERB':
            print("")
            similarity = check_similarity(suff_less_word, list_synonyms(suff_less_word, 'VERB'))
            similarity = {y: x for x, y in similarity.items()}
            similarity_code = dic_bin_codes(list(similarity.items()))
            similarity_code = {y: x for x, y in similarity_code.items()}
            print(similarity_code)
            break
        else:
            print("")
