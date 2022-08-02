import os
import shutil

from indoNLP.dataset.reader import *


def test_txt_table_reader():
    temp_dir = "temp"
    os.makedirs(temp_dir, exist_ok=True)
    with open(os.path.join(temp_dir, "test.txt"), "w") as writer:
        writer.write(
            "buah\tdeskripsi\n"
            + "mangga\tbuah yang berwarna hijau\n"
            + "apel\tbuah berwarna merah dan hijau\n"
        )
    data_with_header = txt_table_reader(os.path.join(temp_dir, "test.txt"))
    assert all(map(lambda x: x in ["buah", "deskripsi"], data_with_header.keys()))
    assert data_with_header["buah"] == ["mangga", "apel"]
    assert data_with_header["deskripsi"] == [
        "buah yang berwarna hijau",
        "buah berwarna merah dan hijau",
    ]

    data_without_header = txt_table_reader(os.path.join(temp_dir, "test.txt"), header=False)
    assert all(map(lambda x: x in [0, 1], data_without_header.keys()))
    assert data_without_header[0] == ["buah", "mangga", "apel"]
    assert data_without_header[1] == [
        "deskripsi",
        "buah yang berwarna hijau",
        "buah berwarna merah dan hijau",
    ]
    shutil.rmtree(temp_dir)


def test_jsonl_table_reader():
    temp_dir = "temp"
    os.makedirs(temp_dir, exist_ok=True)
    with open(os.path.join(temp_dir, "test.jsonl"), "w") as writer:
        writer.write(
            r'{"text": "Hanya karena sapa itu.\nKau tikam rasamu.\nSisakan, bulir-bulir sedu."}'
            + "\n"
            + r'{"text": "Sedang di antrian panjang\nPada sebuah penantian\nEntah kapan rindu memanggil\nSebab ada temu yang masih tertinggal"}'
            + "\n"
            + r'{"text": "Jika kau bukan tempat awal untuk berlabuh, maka kau yang terakhir \nDi mana aku terjatuh kemudian karam"}'
            + "\n"
        )
    data = jsonl_table_reader(os.path.join(temp_dir, "test.jsonl"))
    assert all(map(lambda x: x in ["text"], data.keys()))
    assert data["text"] == [
        "Hanya karena sapa itu.\nKau tikam rasamu.\nSisakan, bulir-bulir sedu.",
        "Sedang di antrian panjang\nPada sebuah penantian\nEntah kapan rindu memanggil\nSebab ada temu yang masih tertinggal",
        "Jika kau bukan tempat awal untuk berlabuh, maka kau yang terakhir \nDi mana aku terjatuh kemudian karam",
    ]
    shutil.rmtree(temp_dir)
