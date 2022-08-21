# indoNLP

[![PyPI version](https://badge.fury.io/py/indoNLP.svg)](https://badge.fury.io/py/indoNLP)
[![Python Version](https://img.shields.io/badge/python-≥3.7-blue?logo=python)](https://python.org)
[![Test](https://github.com/Hyuto/indo-nlp/actions/workflows/testing.yaml/badge.svg)](https://github.com/Hyuto/indo-nlp/actions/workflows/testing.yaml)
[![Lint](https://github.com/Hyuto/indo-nlp/actions/workflows/linting.yaml/badge.svg)](https://github.com/Hyuto/indo-nlp/actions/workflows/linting.yaml)
[![codecov](https://codecov.io/gh/Hyuto/indo-nlp/branch/master/graph/badge.svg?token=094QNPJ3X4)](https://codecov.io/gh/Hyuto/indo-nlp)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

---

Bahasa | [English](https://github.com/Hyuto/indo-nlp/blob/master/README.en.md)

indoNLP adalah library python sederhana tanpa dependency tambahan yang bertujuan untuk memudahkan proyek NLP anda.

## Installasi

indoNLP dapat diinstall dengan mudah dengan menggunakan `pip`:

```bash
$ pip install indoNLP
```

## Quick Start

**Mengakses Indonesian NLP Open Dataset**

Mengakses Indonesian NLP Open Dataset dengan cepat dan mudah.

```python
from indoNLP.dataset import Dataset

handler = Dataset("id-multi-label-hate-speech-and-abusive-language-detection")
data = handler.read()
```

Jika data bersifat simetrik maka data dapat ditabelisasi menggunakan `pandas.DataFrame`

```python
import pandas as pd

df = pd.DataFrame(data)
```

**Preprocessing Data Teks**

Menerjemahkan emoji dan mengganti kata gaul (_slang words_)

```python
from indoNLP.preprocessing import emoji_to_words, replace_slang, pipeline

pipe = pipeline([emoji_to_words, replace_slang])
pipe("library yg membara 🔥")
# "library yang membara !api!"
```

## Development

Setup local dev environment. `indoNLP` menggunakan [python-poetry](https://python-poetry.org/)
untuk packaging dan management dependencies.

```bash
$ make setup-dev
```
