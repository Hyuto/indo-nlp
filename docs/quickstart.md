# Quick Start

## Mengakses Indonesian NLP Open Dataset

Mengakses Indonesian NLP Open Dataset dengan cepat dan mudah.

```python
from indoNLP.dataset import Dataset

handler = Dataset("twitter-puisi")
data = handler.read()
# out: Data(name='main', part_of='twitter-puisi')
```

Mengecek kesimetrisan data, jika data bersifat simetrik maka data dapat ditabelisasi menggunakan `pandas.DataFrame`.

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

## Preprocessing Data Teks

Menerjemahkan emoji dan mengganti kata gaul (_slang words_).

```python
from indoNLP.preprocessing import emoji_to_words, replace_slang, pipeline

pipe = pipeline([emoji_to_words, replace_slang])
pipe("library yg membara 🔥")
# out: "library yang membara !api!"
```
