# indoNLP

[![PyPI version](https://badge.fury.io/py/indoNLP.svg)](https://badge.fury.io/py/indoNLP)
[![Python Version](https://img.shields.io/badge/python-≥3.7-blue?logo=python)](https://python.org)
[![Pypy Version](https://img.shields.io/badge/pypy-≥3.7-blue?logo=pypy)](https://www.pypy.org/)
[![Test](https://github.com/Hyuto/indo-nlp/actions/workflows/testing.yaml/badge.svg)](https://github.com/Hyuto/indo-nlp/actions/workflows/testing.yaml)
[![Lint](https://github.com/Hyuto/indo-nlp/actions/workflows/linting.yaml/badge.svg)](https://github.com/Hyuto/indo-nlp/actions/workflows/linting.yaml)
[![codecov](https://codecov.io/gh/Hyuto/indo-nlp/branch/master/graph/badge.svg?token=094QNPJ3X4)](https://codecov.io/gh/Hyuto/indo-nlp)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

---

[Bahasa](https://github.com/Hyuto/indo-nlp/blob/master/README.md) | English

indoNLP is a simple python library to make your Indonesian NLP project easier.

## Installation

The easiest way to install indoNLP is using `pip`:

```bash
$ pip install indoNLP
```

## Preprocessing

The `indoNLP.preprocessing` module provides several common utility functions to transform and
preparing raw text data for use in a specific context.

**Generics**

1. `remove_html`

   Removing html tags inside text

   ```python
   >>> from indoNLP.preprocessing import remove_html
   >>> remove_html("website <a href='https://google.com'>google</a>")
   >>> "website google"
   ```

2. `remove_url`

   Removing url inside text

   ```python
   >>> from indoNLP.preprocessing import remove_url
   >>> remove_url("retrieved from https://gist.github.com/gruber/8891611")
   >>> "retrieved from "
   ```

3. `remove_stopwords`

   Removing Indonesian stopwords inside text.
   Indonesian Block Word List retrived from https://stopwords.net/indonesian-id/

   ```python
   >>> from indoNLP.preprocessing import remove_stopwords
   >>> remove_stopwords("siapa yang suruh makan?!!")
   >>> "  suruh makan?!!"
   ```

4. `replace_slang`

   Replace slang words to formal words.
   Indonesian Slang Words List retrived from
   [Kamus Alay - Colloquial Indonesian Lexicon](https://github.com/nasalsabila/kamus-alay)
   by Salsabila, Ali, Yosef, and Ade

   ```python
   >>> from indoNLP.preprocessing import replace_slang
   >>> replace_slang("emg siapa yg nanya?")
   >>> "memang siapa yang bertanya?"
   ```

5. `replace_word_elongation`

   > Word Elongation is the act of adding extra letters to words, typically to the end of the word

   Handling word elongation

   ```python
   >>> from indoNLP.preprocessing import replace_word_elongation
   >>> replace_word_elongation("kenapaaa?")
   >>> "kenapa?"
   ```

**Emoji**

Preprocessing emoji containing text.

1. `emoji_to_words`

   Transform emoji to an understandable words with the same meaning as the emoji itself.

   ```python
   >>> from indoNLP.preprocessing import emoji_to_words
   >>> emoji_to_words("emoji 😀😁")
   >>> "emoji !wajah_gembira!!wajah_gembira_dengan_mata_bahagia!"
   ```

2. `words_to_emoji`

   Transform words code to an emoji.

   ```python
   >>> from indoNLP.preprocessing import words_to_emoji
   >>> words_to_emoji("emoji !wajah_gembira!")
   >>> "emoji 😀"
   ```

**Pipelining**

Create pipeline from sequence of preprocessing functions

```python
>>> from indoNLP.preprocessing import pipeline, replace_word_elongation, replace_slang
>>> pipe = pipeline([replace_word_elongation, replace_slang])
>>> pipe("Knp emg gk mw makan kenapaaa???")
>>> "kenapa memang enggak mau makan kenapa???"
```
