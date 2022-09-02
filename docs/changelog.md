# Changelog

## v0.3.1 { .changelog-versions }

22 Agustus 2022
{ .changelog-dates }

**Documentation 📝**

Membuat website dokumentasi untuk `indoNLP` menggunakan [mkdocs](https://www.mkdocs.org/) dengan
tema [mkdocs-material](https://squidfunk.github.io/mkdocs-material/) dan menggenerasi kode
referensi secara otomatis menggunakan [mkdocstring](https://mkdocstrings.github.io/).

- Mengubah kode docstring ke Bahasa Indonesia.
- Merge [#3](https://github.com/Hyuto/indo-nlp/pull/3) ke master dan deploy dokumentasi menggunakan github action.

**Bug Fixing**

- Memperbaiki top level import pada `indoNLP/__init__.py`
- Memperbaiki inconsistent return pada fungsi `indoNLP.dataset.reader.txt_table_reader`

## v0.3.0 { .changelog-versions }

17 Agustus 2022
{ .changelog-dates }

**New Features : Dataset 📖**

Modul baru yaitu `indoNLP.dataset` yang memudahkan cara mengakses _open dataset_ pada kasus NLP
dalam Bahasa Indonesia.

## v0.2.0 { .changelog-versions }

14 Juli 2022
{ .changelog-dates }

**Bug Fixing**

Memperbaiki bug pada fungsi `preprocessing.replace_word_elongation` yang mengganti kata berulang
disetiap posisi pada sebuah kata menjadi di akhir kata saja.

**New Feature : Emoji Supports 🤗**

Preproses teks yang mengandung emoji kedalam Bahasa Indonesia dan sebaliknya.

1. `emoji_to_words`
2. `words_to_emoji`

## v0.1.1 { .changelog-versions }

30 Juni 2022
{ .changelog-dates }

**Fixing**

Membenarkan typo `preprocessing.pipline` menjadi `preprocessing.pipeline`

## v0.1.0 { .changelog-versions }

28 Juni 2022
{ .changelog-dates }

**Initial Release**

Membuat modul `preprocessing` yang terdiri dari beberapa fungsi.

1. `preprocessing.remove_html`
2. `preprocessing.remove_url`
3. `preprocessing.remove_stopwords`
4. `preprocessing.replace_slang`
5. `preprocessing.replace_word_elongation`
6. `preprocessing.pipeline`
