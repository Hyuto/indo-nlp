# Request Penambahan Supported Dataset

## Menambahkan Dataset

Tambahkan informasi terkait dataset pada file `indoNLP/dataset/list.py` dengan ketentuan
sebagai berikut:

```python
    ...
    ,
    "{{ ID-DATASET-BARU  }}": {
        "info": {
            "description": str, # Deskripsi singkat tentang dataset
            "author": str,      # Orang - orang yang memiliki hak cipta terhadap dataset
            "year": int,        # Tahun dataset dipublish
            "citation": str,    # Cara mengutip dataset
            "homepage": str,    # Website atau halaman utama dataset
            "tags": List[str],  # Tag - tag yang berhubungan dengan dataset
        },
        "files": [   # Berisi file - file yang terdapat dalam dataset
            {
                "filename": str,   # Nama file
                "url": str,        # URL atau endpoint tempat file dapat didownload
                "is_large": bool,  # Apakah ukuran file besar?
                "extract": bool,   # Apakah file perlu dilakukan ekstraksi?
            },
            ...
        ],
        "reader": {  # Berisi keterangan tentang semua file yang terdapat di dataset
            "{{ ID-FILE }}": {  # id file dalam dataset agar dapat dikenali oleh method .read
                "path": str,        # path ke file yang akan dibaca relative terhadap `downloader.dataset_dir`
                "is_table": bool,   # Apakah data dalam file bersifat simetrik?
                "reader": Callable, # Fungsi yang digunakan untuk membaca data pada file terdapat
                                    # pada indoNLP/dataset/reader.py jika tidak terdapat fungsi yang
                                    # tersedia maka buat fungsi baru dengan format yang sama terhadap
                                    # fungsi reader yang lain [TANPA TAMBAHAN DEPENDENCIES].
                "args": Dict,       # kwargs yang perlu dipass kefungsi reader.
            },
            ...
        },
    },
}
```

## Ketentuan

Jika diperlukan untuk menambah fungsi reader baru pastikan untuk menambakan juga test case pada file
`tests/dataset/test_reader.py` untuk unit testing dan juga memperhatikan 
[ketentuan _code coverage_](../#coverage-target).

!!! warning
    Dalam pembuatan fungsi reader baru utamakan tidak menggunakan dependensi tambahan selain 
    _python standard library_.

## Membuat Pull Request

Setelah semua ketentuan tercapai buat Pull Request di [repository `indoNLP`](https://github.com/Hyuto/indo-nlp)
, akan dilakukan review apakah dataset dapat ditambahkan atau tidak.
