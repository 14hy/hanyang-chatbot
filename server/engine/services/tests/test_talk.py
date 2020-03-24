from engine.services.talk import _get_score


def test__calc_jaccard():
    assert _get_score("안녕!", "안녕!") == 3
