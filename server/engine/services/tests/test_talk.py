from engine.services.talk import _calc_jaacard, get_response


def test__calc_jaccard():
    assert _calc_jaacard('안녕!', '안녕!') == 3
