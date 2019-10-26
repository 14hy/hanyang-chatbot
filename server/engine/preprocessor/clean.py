"""\
https://github.com/google-research/bert
tokenization.py 전처리 코드 포함
"""
import unicodedata
from utils import *


def _is_punctuation(char):
    """Checks whether `chars` is a punctuation character."""
    cp = ord(char)
    # We treat all non-letter/number ASCII as punctuation.
    # Characters such as "^", "$", and "`" are not in the Unicode
    # Punctuation class but we treat them as punctuation anyways, for
    # consistency.
    if ((cp >= 33 and cp <= 47) or (cp >= 58 and cp <= 64) or
            (cp >= 91 and cp <= 96) or (cp >= 123 and cp <= 126)):
        return True
    cat = unicodedata.category(char)
    if cat.startswith("P"):
        return True
    return False


def _is_control(char):
    """Checks whether `chars` is a control character."""
    # These are technically control characters but we count them as whitespace
    # characters.
    if char == "\t" or char == "\n" or char == "\r":
        return False
    cat = unicodedata.category(char)
    if cat.startswith("C"):
        return True
    return False


def _is_whitespace(char):
    """Checks whether `chars` is a whitespace character."""
    # \t, \n, and \r are technically contorl characters but we treat them
    # as whitespace since they are generally considered as such.
    if char == " " or char == "\t" or char == "\n" or char == "\r":
        return True
    cat = unicodedata.category(char)
    if cat == "Zs":
        return True
    return False


def whitespace_tokenize(text):
    """Runs basic whitespace cleaning and splitting on a piece of chat."""
    text = text.strip()
    if not text:
        return []
    tokens = text.split()
    return tokens


# TODO Lemmatization
@basic_timer
@debug_logger
def clean(text, token=False):
    """전처리 함수

    1. 컨트롤 문자
    2. 구두 문자
    3. 빈칸

    :param str text:
    :param bool token:

    :return:
    """

    output = []
    for char in text:
        if _is_control(char) | _is_punctuation(char):
            continue
        if _is_whitespace(char):
            output.append(' ')
        else:
            output.append(char)

    output = ''.join(output)
    tokens = whitespace_tokenize(output)
    if not token:
        return ' '.join(tokens)
    return tokens
