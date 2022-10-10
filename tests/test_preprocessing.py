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
    assert (
        remove_stopwords("widi ngapain sih wkwk lagian kgk jelas wkwkwkkwk")
        == "widi ngapain sih   kgk"
    )


def test_replace_slang():
    assert replace_slang("") == ""
    assert replace_slang("orang gk diapa - apain") == "orang enggak diapa - apai"
    assert replace_slang("gw gk mw makan!!") == "gue enggak mau makan!!"
    assert replace_slang("emg siapa yg nanya?") == "memang siapa yang bertanya?"
    assert replace_slang("lg sma siapa?") == "lagi sama siapa?"


def test_replace_word_elongation():
    assert replace_word_elongation("") == ""
    assert replace_word_elongation("kenapaa?") == "kenapa?"
    assert replace_word_elongation("kenapaaa?") == "kenapa?"
    assert replace_word_elongation("kenapaaaa?") == "kenapa?"
    assert replace_word_elongation("KENAPAAA?") == "KENAPA?"
    assert replace_word_elongation("insha Allah") == "insha Allah"


def test_pipeline():
    pipe_1 = pipeline([replace_word_elongation, replace_slang])

    assert pipe_1("Knp emg gk mw makan kenapaaa???") == "kenapa memang enggak mau makan kenapa???"


def test_duplicate_slang():
    slangs = []
    for slang in SLANG_DATA.keys():
        assert slang not in slangs
        slangs.append(slang)


def test_duplicate_emoji():
    title = {"en": [], "id": [], "alias": []}
    for emoji in EMOJI_DATA.values():
        assert emoji["en"] not in title["en"]
        title["en"].append(emoji["en"])

        if emoji["id"] in title["id"]:
            assert (
                emoji.get("alias") is not None
                and emoji.get("alias") not in title["id"] + title["alias"]
            )

        title["id"].append(emoji["id"])
        if emoji.get("alias") is not None:
            title["alias"].append(emoji["alias"])


def test_emoji_to_words():
    assert emoji_to_words("emoji 😀") == "emoji !wajah_gembira!"
    assert emoji_to_words("emoji 😀😁") == "emoji !wajah_gembira!!wajah_gembira_dengan_mata_bahagia!"
    assert emoji_to_words("emoji 😀", use_alias=True) == "emoji !wajah_gembira_bahagia_muka_senang!"
    assert emoji_to_words("emoji 😀", lang="en") == "emoji !grinning_face!"
    assert emoji_to_words("emoji 😀", delimiter=("<", "!")) == "emoji <wajah_gembira!"
    assert emoji_to_words("emoji ⛹🏼‍♂️") == "emoji !pria_memantulkan_bola_warna_kulit_cerah-sedang!"


def test_words_to_emoji():
    assert words_to_emoji("emoji !wajah_gembira!") == "emoji 😀"
    assert words_to_emoji("emoji !grinning_face!", lang="en") == "emoji 😀"
    assert words_to_emoji("emoji <wajah_gembira!", delimiter=("<", "!")) == "emoji 😀"
    assert words_to_emoji("emoji !wajah_gembira_bahagia_muka_senang!", use_alias=True) == "emoji 😀"
    assert words_to_emoji("emoji !pria_memantulkan_bola_warna_kulit_cerah-sedang!") == "emoji ⛹🏼‍♂️"
    assert (
        words_to_emoji("sedang on!api! banget nih kayaknya!lengan_berotot!!lengan_berotot!")
        == "sedang on🔥 banget nih kayaknya💪💪"
    )
