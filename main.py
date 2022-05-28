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

'Deleting suffix for words in given text'
def remove_suffix(text):
    res = []
    for word in text:
        a = stemmer.stem(word)
        res.append(a)
    return res


'Part of speech tagging'
def pos_tag(text):
    res = []
    sen = sp(text)
    for word in sen:
        a = word.pos_
        res.append(a)
    return res

'Decoding stego messaga bits to text'
def decode(message):
    alp_decode = dic_bin_codes_decode(alphabet)
    temp = ''.join(message)
    msg_decode = bitarray(temp).decode(alp_decode)
    print(''.join(msg_decode))

'Generating list of synonyms for given word and POS'
def list_synonyms(word, pos):
    synonyms = []
    if pos == 'NOUN':
        pos = wn.NOUN
    if pos == 'VERB':
        pos = wn.VERB
    for syn in wn.synsets(word, pos):
        for i in syn.lemmas():
            if word.lower() in i.name().lower():
                continue
            synonyms.append(i.name())
    return synonyms

'Generating similarity score for given word an its synonyms'
def check_similarity(word, synon):
    dic = {}
    for syn in synon:
        doc_1 = sp(word)
        doc_2 = sp(syn)
        similarity = doc_1.similarity(doc_2)
        dic.update({syn: similarity})
    return dic

'Finding all differeces between two tokenized texts'
def lists_diff(l1, l2):
    dic = []
    for i, j in zip(l1, l2):
        if i == j:
            continue
        else:
            dic.append((i, j))
    return dic


if __name__ == "__main__":
    'coding alphabet and secret message letters'

    alp_code = dic_bin_codes(alphabet)
    secret = "it is a secret message"
    secret_list = list(secret)
    msg = hd_msg(secret_list, alp_code)
    msg = ''.join(msg)
    print(msg)

    'suffix removal and pos tagging'
    tokens = nltk.word_tokenize(secret)
    suff_less_secret = remove_suffix(tokens)

    orig_text = open('covert.txt', 'r')
    words = nltk.word_tokenize(orig_text.read())
    i = 0
    for id, word in enumerate(words):
        suff_less_word = stemmer.stem(word)
        word_suf = word.replace(suff_less_word, '')
        word_pos = pos_tag(word)
        if len(msg) > 0:
            if word_pos[0] == 'NOUN':
                if i == 0 and len(word) > 3:
                    similarity = check_similarity(suff_less_word, list_synonyms(suff_less_word, 'NOUN'))
                    similarity = dict(sorted(similarity.items(), key=lambda x: x[1], reverse=True))
                    similarity = {y: x for x, y in similarity.items()}
                    if len(similarity) < 2:
                        continue
                    else:
                        similarity_code = dic_bin_codes(list(similarity.items())[:3])
                        similarity_code = {y: x for x, y in similarity_code.items()}
                        print(similarity_code)
                        for c in similarity_code:
                            if msg.startswith(c):
                                msg = msg[len(c):]
                                print("mamy slowo")
                                print(msg)
                                print(similarity_code.get(c) + '---' + words[id])
                                words[id] = similarity_code.get(c)
                                break
                            else:
                                continue

            elif word_pos[0] == 'VERB' and len(word) > 3:
                if i == 0:
                    similarity = check_similarity(suff_less_word, list_synonyms(suff_less_word, 'VERB'))
                    similarity = dict(sorted(similarity.items(), key=lambda x: x[1], reverse=True))
                    similarity = {y: x for x, y in similarity.items()}
                    if len(similarity) < 2:
                        continue
                    else:
                        similarity_code = dic_bin_codes(list(similarity.items())[:3])
                        similarity = sorted(similarity)
                        similarity_code = {y: x for x, y in similarity_code.items()}
                        print(similarity_code)
                        for c in similarity_code:
                            if msg.startswith(c):
                                msg = msg[len(c):]
                                print("mamy slowo")
                                print(msg)
                                print(similarity_code.get(c) + '---' + words[id])
                                words[id] = similarity_code.get(c)
                                break
                            else:
                                continue
            else:
                continue
        else:
            print("Szyfrowanie skonczone")
            steg_text = open('result.txt', 'w')
            stego = ' '.join(words)
            steg_text.write(stego)
            break
        i = (i + 1) % 2
    orig_text.close()
    steg_text.close()


    'Deszyfrowanie:'
    orig_text = open('covert.txt', 'r')
    stego_text = open('result.txt', 'r')

    words = nltk.word_tokenize(orig_text.read())
    stego_words = nltk.word_tokenize(stego_text.read())
    #print(words)
    #print(stego_words)
    diff = lists_diff(words, stego_words)
    print(diff)
    res_bin_code = ''
    for word in diff:
        temp = stemmer.stem(word[0])
        word_pos = pos_tag(word[0])
        if word_pos[0] == 'NOUN':
            similarity = check_similarity(temp, list_synonyms(temp, 'NOUN'))
        elif word_pos[0] == 'VERB':
            similarity = check_similarity(temp, list_synonyms(temp, 'VERB'))
        similarity = dict(sorted(similarity.items(), key=lambda x: x[1], reverse=True))
        similarity = {y: x for x, y in similarity.items()}
        similarity_code = dic_bin_codes(list(similarity.items())[:3])
        res_bin_code += similarity_code[word[1]]
    print(res_bin_code)
    decode(res_bin_code)
