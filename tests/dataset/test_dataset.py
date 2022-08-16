import os
import shutil

import pytest

from indoNLP.dataset import *
from indoNLP.dataset.downloader import DataDownloader
from indoNLP.dataset.list import DATASETS


def test_get_supported_dataset_list(capfd):
    get_supported_dataset_list()
    get_supported_dataset_list(filter_tags="unlabeled")
    get_supported_dataset_list(
        filter_tags=[
            "labeled",
            "hate speech",
            "abusive language detection",
            "multi-label",
            "twitter",
        ]
    )
    out, _ = capfd.readouterr()
    out = [x for x in out.split("Supported Datasets\n-----------------\n") if x != ""]

    for dataset in DATASETS.keys():
        assert dataset in out[0]

    assert "twitter-puisi" in out[1]
    assert "id-multi-label-hate-speech-and-abusive-language-detection" in out[2]


def test_get_supported_dataset_info(capfd):
    get_supported_dataset_info("twitter-puisi")

    out, _ = capfd.readouterr()
    assert out.split("\n")[0] == "📖 twitter-puisi"

    with pytest.raises(KeyError) as e:
        get_supported_dataset_info("test")

        assert e == "Dataset not found!"


class TestDataset:
    def test_supported_Dataset_available(self):
        for dataset in DATASETS.keys():
            data = Dataset(dataset, auto_download=False)
            for check in data.downloader.check():
                assert check["available"], f"{check['filename']} - {check['status']}"

    @pytest.mark.slow
    def test_supported_Dataset_download(self):
        data = Dataset("twitter-puisi")
        assert os.path.exists(os.path.join(data.file.download_dir, "twitter-puisi"))
        assert data.downloader._is_completed()
        shutil.rmtree(data.file.download_dir)  # clean up

        data = Dataset("id-abusive-language-detection", dataset_dir="temp")
        assert all(
            map(
                lambda x: x in ["re_dataset_two_labels.csv", "re_dataset_three_labels.csv"],
                os.listdir(os.path.join(data.file.download_dir, "id-abusive-language-detection")),
            )
        )
        dataset = data.read()
        assert len(dataset) == 2
        assert [*dataset[0].keys()] == ["Label", "Tweet"]
        assert dataset[1] == data.read("three-labels")
        shutil.rmtree(data.file.download_dir)  # clean up

        with pytest.raises(KeyError):
            Dataset("test")

    def test_unsupported_Dataset_download(self):
        downloader = DataDownloader(
            "msa-all-tab",
            files=[
                {
                    "filename": "Bahasa-Wordnet-master.zip",
                    "url": "https://codeload.github.com/limaginaire/Bahasa-Wordnet/zip/refs/heads/master",
                    "is_large": True,
                    "extract": True,
                }
            ],
            download_dir="temp",
        )
        downloader.download()
        assert os.path.exists(downloader.dataset_dir)
        assert all(
            map(
                lambda x: x in ["LICENSE", "Readme", "wn-ind-def.tab", "wn-msa-all.tab"],
                os.listdir(os.path.join(downloader.dataset_dir, "Bahasa-Wordnet-master")),
            )
        )
        shutil.rmtree(downloader.file.download_dir)
