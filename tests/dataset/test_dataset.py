import shutil

import pytest

from indoNLP.dataset import *


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


def test_Dataset():
    data = Dataset("twitter-puisi")
    assert os.path.exists(os.path.join(data.file.download_dir, "twitter-puisi"))
    shutil.rmtree(data.file.download_dir)  # clean up

    data = Dataset(
        "id-multi-label-hate-speech-and-abusive-language-detection",
        dataset_dir="./temp",
    )
    assert os.path.exists(
        os.path.join(
            data.file.download_dir,
            "id-multi-label-hate-speech-and-abusive-language-detection",
        )
    )
    dataset = data.read()
    assert [*dataset.keys()] == [
        "Tweet",
        "HS",
        "Abusive",
        "HS_Individual",
        "HS_Group",
        "HS_Religion",
        "HS_Race",
        "HS_Physical",
        "HS_Gender",
        "HS_Other",
        "HS_Weak",
        "HS_Moderate",
        "HS_Strong",
    ]
    shutil.rmtree(data.file.download_dir)  # clean up

    with pytest.raises(KeyError):
        Dataset("test")
