from IndoNLP.preprocess import *


def test_remove_html():
    assert remove_html("teks <strong>ditebalkan</strong>") == "teks ditebalkan"
    assert remove_html("website <a href='https://google.com'>google</a>") == "website google"


def test_remove_url():
    assert (
        remove_url("terlampir di website google (https://google.com)")
        == "terlampir di website google ()"
    )
    assert remove_url("Contoh http://example.com/v1/AGYUGyugYJgygUGU") == "Contoh "


def test_replace_slang():
    assert replace_slang("") == ""
    assert replace_slang("gw gk mw makan!!") == "gue enggak mau makan!!"
    assert replace_slang("emg siapa yg nanya?") == "memang siapa yang bertanya?"
    assert replace_slang("emg siapa yg nanya?") == "memang siapa yang bertanya?"


def test_replace_word_elongation():
    assert replace_word_elongation("") == ""
    assert replace_word_elongation("kenapaa?") == "kenapa?"
    assert replace_word_elongation("kenapaaa?") == "kenapa?"
    assert replace_word_elongation("kenapaaaa?") == "kenapa?"
    assert replace_word_elongation("KENAPAAA?") == "KENAPA?"
