# from khaiii import KhaiiiApi
# from mecab import MeCab
# from utils import basic_logger, basic_timer
#
# KA = KhaiiiApi()
# MA = MeCab()

dict_khaiii = {}


class Text(object):
    """형태소 분석한 텍스트"""

    def __init__(self, orig, tags, morphs):
        self.morphs = morphs
        self.tags = tags
        self.orig = orig

    def __repr__(self):
        return f'<Text object, morphs: {self.morphs}, tags: {self.tags}, orig: {self.orig}'


@basic_timer
@basic_logger
def analyze(text):
    """형태소 분석

    :param str text:
    :return:
    """
    morphs = []
    tags = {}

    morph_mecab = MA.pos(text)
    for each in morph_mecab:
        word, tag = each
        if '+' in tag:
            # 여러 형태소가 섞였다면 khaiii를 사용해서 분리
            if word in dict_khaiii:
                morph_khaiii = dict_khaiii[word]
            else:
                morph_khaiii = KA.analyze(word)[0].morphs
                dict_khaiii[word] = morph_khaiii
            for morph in morph_khaiii:
                morphs.append(morph.lex)
                tags[morph.lex] = morph.tag
        else:
            tags[word] = tag
            morphs.append(word)
    morphs = ' '.join(morphs)

    return Text(orig=text, tags=tags, morphs=morphs)
