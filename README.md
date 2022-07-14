# indoNLP

[![PyPI version](https://badge.fury.io/py/indoNLP.svg)](https://badge.fury.io/py/indoNLP)
[![Python Version](https://img.shields.io/badge/python-≥3.7-blue?logo=python)](https://python.org)
[![Test](https://github.com/Hyuto/indo-nlp/actions/workflows/testing.yaml/badge.svg)](https://github.com/Hyuto/indo-nlp/actions/workflows/testing.yaml)
[![Lint](https://github.com/Hyuto/indo-nlp/actions/workflows/linting.yaml/badge.svg)](https://github.com/Hyuto/indo-nlp/actions/workflows/linting.yaml)
[![codecov](https://codecov.io/gh/Hyuto/indo-nlp/branch/master/graph/badge.svg?token=094QNPJ3X4)](https://codecov.io/gh/Hyuto/indo-nlp)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

---

Bahasa | [English](https://github.com/Hyuto/indo-nlp/blob/master/README.en.md)

indoNLP adalah library python sederhana yang bertujuan untuk memudahkan proyek NLP anda.

## Installation

indoNLP dapat diinstall dengan mudah dengan menggunakan `pip`:

```bash
$ pip install indoNLP
```

## Preprocessing

Modul `indoNLP.preprocessing` menyediakan beberapa fungsi umum untuk menyiapkan dan melakukan
transformasi terhadap data teks mentah untuk digunakan pada konteks tertentu.

**Generics**

1. `remove_html`

   Menghapus html tag yang terdapat di dalam teks

   ```python
   >>> from indoNLP.preprocessing import remove_html
   >>> remove_html("website <a href='https://google.com'>google</a>")
   >>> "website google"
   ```

2. `remove_url`

   Menghapus url yang terdapat di dalam teks

   ```python
   >>> from indoNLP.preprocessing import remove_url
   >>> remove_url("retrieved from https://gist.github.com/gruber/8891611")
   >>> "retrieved from "
   ```

3. `remove_stopwords`

   > Stopwords merupakan kata yang diabaikan dalam pemrosesan dan biasanya disimpan di dalam stop lists. Stop list ini berisi daftar kata umum yang mempunyai fungsi tapi tidak mempunyai arti

   Menghapus stopwords yang terdapat di dalam teks.
   List stopwords bahasa Indonesia didapatkan dari https://stopwords.net/indonesian-id/

   ```python
   >>> from indoNLP.preprocessing import remove_stopwords
   >>> remove_stopwords("siapa yang suruh makan?!!")
   >>> "  suruh makan?!!"
   ```

4. `replace_slang`

   Mengganti kata gaul (_slang_) menjadi kata formal tanpa mengubah makna dari kata tersebut.
   List kata gaul (_slang words_) bahasa Indonesian didapatkan dari
   [Kamus Alay - Colloquial Indonesian Lexicon](https://github.com/nasalsabila/kamus-alay)
   oleh Salsabila, Ali, Yosef, and Ade

   ```python
   >>> from indoNLP.preprocessing import replace_slang
   >>> replace_slang("emg siapa yg nanya?")
   >>> "memang siapa yang bertanya?"
   ```

5. `replace_word_elongation`

   > Word elongation adalah tindakan untuk menambahkan huruf ke kata, biasanya di akhir kata

   Meghandle word elongation

   ```python
   >>> from indoNLP.preprocessing import replace_word_elongation
   >>> replace_word_elongation("kenapaaa?")
   >>> "kenapa?"
   ```

**Emoji**

Preproses teks yang mengandung emoji.

1. `emoji_to_words`

   Mengubah emoji yang berada dalam sebuah teks menjadi kata - kata yang sesuai dengan emoji
   tersebut.

   ```python
   >>> from indoNLP.preprocessing import emoji_to_words
   >>> emoji_to_words("emoji 😀😁")
   >>> "emoji !wajah_gembira!!wajah_gembira_dengan_mata_bahagia!"
   ```

2. `words_to_emoji`

   Mengubah kata - kata dengan kode emoji menjadi emoji.

   ```python
   >>> from indoNLP.preprocessing import words_to_emoji
   >>> words_to_emoji("emoji !wajah_gembira!")
   >>> "emoji 😀"
   ```

**Pipelining**

Membuat pipeline dari sequance fungsi preprocessing

```python
>>> from indoNLP.preprocessing import pipeline, replace_word_elongation, replace_slang
>>> pipe = pipeline([replace_word_elongation, replace_slang])
>>> pipe("Knp emg gk mw makan kenapaaa???")
>>> "kenapa memang enggak mau makan kenapa???"
```
