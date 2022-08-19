# Development

Untuk development `indoNLP` menggunakan [python-poetry](https://python-poetry.org/)
untuk packaging dan management dependencies.

**Install `python-poetry`**

Silahkan kunjungi [installation](https://python-poetry.org/docs/#installation) untuk melihat cara
installasi dari `python-poetry` berdasarkan OS yang digunakan.

## Setup

Setup development environment, dengan menggunakan command

```bash
$ make setup-dev
```

Command tersebut akan menginstall semua dependencies yang digunakan oleh `indoNLP` dalam tahap
development.

## Make Commands

Commands yang terdapat pada `Makefile` digunakan untuk memudahkan proses development yaitu:

- `setup-dev` digunakan untuk setup development environment.
- `format` digunakan untuk mengformat menggunakan `black` dan `isort`.
- `format-check` digunakan untuk melihat apakah project telah mengikuti ketentuan `black` dan `isort`.
- `typecheck` digunakan untuk _type checking_ menggunakan `mypy`
- `test` digunakan untuk melakukan testing menggunakan `pytest`

## Coverage Target

Code coverage yang ditargetkan pada `indoNLP` adalah lebih dari 95%.

## `pre-commit`

Sebelum melakukan `commit` pastikan code lolos `format-check` dan `typecheck` karena akan diujikan
oleh `pre-commit`, jika tidak lolos maka proses commit akan ditolak.

!!! note "Perhatian"
    Pastikan anda berada dalam environment poetry saat melakukan _commit_, cara mengaktifkannya
    adalah dengan menggunakan command

    ```bash
    poetry shell
    ```
