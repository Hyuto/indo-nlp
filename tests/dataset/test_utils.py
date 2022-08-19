from indoNLP.dataset.utils import *


def test_logger(caplog):
    logger.info("test info!")
    logger.warning("test warning!")
    logger.error("test error!")

    info, warning, error = [
        list(filter(lambda y: y != "", x.split(" "))) for x in caplog.text.split("\n") if x != ""
    ]

    assert info == ["INFO", "indoNLP:test_utils.py:5", "test", "info!"]
    assert warning == ["WARNING", "indoNLP:test_utils.py:6", "test", "warning!"]
    assert error == ["ERROR", "indoNLP:test_utils.py:7", "test", "error!"]


def test_sizeof_fmt():
    assert _sizeof_fmt(24) == "24.00 B"
    assert _sizeof_fmt(1024) == "1.00 KiB"
    assert _sizeof_fmt(2**80) == "1.00 YiB"


def test_progress_text(capsys):
    filename = "test"
    _progress_text(filename, 100, False)
    _progress_text(filename, 200, True)

    out, _ = capsys.readouterr()
    out = [x for x in out.split("\r") if x != ""]
    assert out[0].strip() == f"Downloading : {filename} [{_sizeof_fmt(100)}]"
    assert out[-1].strip() == f"📖 {filename} saved [{_sizeof_fmt(200)}]"
