# Quick Start

## Mengakses Indonesian NLP Open Dataset

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

## Preprocessing Data Teks

Menerjemahkan emoji dan mengganti kata gaul (_slang words_)

```python
from indoNLP.preprocessing import emoji_to_words, replace_slang, pipeline

pipe = pipeline([emoji_to_words, replace_slang])
pipe("library yg membara 🔥")
# "library yang membara !api!"
```
