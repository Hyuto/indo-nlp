from indoNLP.preprocessing import *


def test_remove_html():
    assert remove_html("teks <strong>ditebalkan</strong>") == "teks ditebalkan"
    assert remove_html("website <a href='https://google.com'>google</a>") == "website google"
    assert remove_html("<div><strong>teks tebal</strong>") == "teks tebal"


def test_remove_url():
    assert (
        remove_url("terlampir di website google (https://google.com)")
        == "terlampir di website google ()"
    )
    assert remove_url("test google.co.id") == "test"
    assert remove_url("google Indonesia www.google.co.id") == "google Indonesia"
    assert remove_url("retrieved from https://gist.github.com/gruber/8891611") == "retrieved from"
    assert remove_url("Contoh http://www.example.org/default.html?ct=32&op=92&item=98") == "Contoh"


def test_remove_stopwords():
    assert remove_stopwords("siapa yang suruh makan?!!") == "suruh makan?!!"


def test_replace_slang():
    assert replace_slang("") == ""
    assert replace_slang("gw gk mw makan!!") == "gue enggak mau makan!!"
    assert replace_slang("emg siapa yg nanya?") == "memang siapa yang bertanya?"


def test_replace_word_elongation():
    assert replace_word_elongation("") == ""
    assert replace_word_elongation("kenapaa?") == "kenapa?"
    assert replace_word_elongation("kenapaaa?") == "kenapa?"
    assert replace_word_elongation("kenapaaaa?") == "kenapa?"
    assert replace_word_elongation("KENAPAAA?") == "KENAPA?"


def test_pipeline():
    pipe_1 = pipeline([replace_word_elongation, replace_slang])

    assert pipe_1("Knp emg gk mw makan kenapaaa???") == "kenapa memang enggak mau makan kenapa???"


def test_duplicate_slang():
    slangs = []
    for slang in SLANG_DATA.keys():
        assert slang not in slangs
        slangs.append(slang)
