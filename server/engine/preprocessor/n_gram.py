import unicodedata
from functools import partial


def _norm(text):
    return unicodedata.normalize('NFD', text)


def unigram(text):
    return text.split()


def bigram(text):
    text = _norm(text)
    return list(map(lambda x: ''.join(x), zip(text, text[1:])))


def trigram(text):
    text = _norm(text)
    return list(map(lambda x: ''.join(x), zip(text, text[1:], text[2:])))
