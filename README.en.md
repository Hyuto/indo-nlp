# indoNLP

[![PyPI version](https://badge.fury.io/py/indoNLP.svg)](https://badge.fury.io/py/indoNLP)
[![Python Version](https://img.shields.io/badge/python-≥3.7-blue?logo=python)](https://python.org)
[![Test](https://github.com/Hyuto/indo-nlp/actions/workflows/testing.yaml/badge.svg)](https://github.com/Hyuto/indo-nlp/actions/workflows/testing.yaml)
[![Lint](https://github.com/Hyuto/indo-nlp/actions/workflows/linting.yaml/badge.svg)](https://github.com/Hyuto/indo-nlp/actions/workflows/linting.yaml)
[![codecov](https://codecov.io/gh/Hyuto/indo-nlp/branch/master/graph/badge.svg?token=094QNPJ3X4)](https://codecov.io/gh/Hyuto/indo-nlp)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

---

[Bahasa](https://github.com/Hyuto/indo-nlp/blob/master/README.md) | English

indoNLP is a simple python library with zero additional dependencies to make your Indonesian NLP project easier.

## Installation

The easiest way to install indoNLP is using `pip`:

```bash
$ pip install indoNLP
```

## Quick Start

**Accessing Indonesian NLP Open Dataset**

Accessing Indonesian NLP Open Dataset with no effort at lightning speed.

```python
from indoNLP.dataset import Dataset

handler = Dataset("twitter-puisi")
data = handler.read()
# out: Data(name='main', part_of='twitter-puisi')
```

Check if dataset is symmetric then load on `pandas.DataFrame`.

```python
import pandas as pd

assert data.is_table(), "Data tidak simetris, tidak dapat ditabulasi!"
df = pd.DataFrame(data.data)
df.head()
# out:
#                                                 text
# 0  Hanya karena sapa itu.\nKau tikam rasamu.\nSis...
# 1  Sedang di antrian panjang\nPada sebuah penanti...
# 2  Jika kau bukan tempat awal untuk berlabuh, mak...
# 3  Setiap waktu,\nAku masih mendengar getar dawai...
# 4  Sebait rindu yang kau bacakan\nMasih terdengar...
```

**Preprocessing Text Data**

Translate emoji and replace slang words.

```python
from indoNLP.preprocessing import emoji_to_words, replace_slang, pipeline

pipe = pipeline([emoji_to_words, replace_slang])
pipe("library yg membara 🔥")
# out: "library yang membara !api!"
```

## Development

Setup local dev environment. `indoNLP` uses [python-poetry](https://python-poetry.org/)
for packaging dan management dependencies.

```bash
$ make setup-dev
```
