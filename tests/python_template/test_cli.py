import json
from pathlib import Path

import pytest

from python_template import __version__
from python_template.cli import PROG, main


def test_no_command_shows_status(capsys: pytest.CaptureFixture[str]) -> None:
    assert main([]) == 0
    assert capsys.readouterr().out == "Baby Python: hunger 5, happiness 5\n"


def test_feed_json(capsys: pytest.CaptureFixture[str]) -> None:
    assert main(["feed", "--times", "3", "--name", "Rex", "--json"]) == 0
    assert json.loads(capsys.readouterr().out) == {"name": "Rex", "hunger": 2, "happiness": 5}


def test_play(capsys: pytest.CaptureFixture[str]) -> None:
    assert main(["play"]) == 0
    assert "happiness 6" in capsys.readouterr().out


def test_times_out_of_range_is_an_error() -> None:
    with pytest.raises(SystemExit) as exc:
        main(["feed", "--times", "11"])
    assert exc.value.code == 2


def test_version(capsys: pytest.CaptureFixture[str]) -> None:
    with pytest.raises(SystemExit):
        main(["--version"])
    assert capsys.readouterr().out.strip() == f"python-template {__version__}"


def test_guide_prints_the_manual(capsys: pytest.CaptureFixture[str]) -> None:
    assert main(["guide"]) == 0
    out = capsys.readouterr().out
    assert out.startswith("# python-template")
    assert "## FOR AGENTS" in out


def test_man_raw_is_roff(capsys: pytest.CaptureFixture[str]) -> None:
    assert main(["man", "--raw"]) == 0
    out = capsys.readouterr().out
    assert out.startswith(f".TH {PROG.upper()} 1")
    assert ".SH NAME\npython-template \\- " in out


def test_man_install(tmp_path: Path, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]) -> None:
    monkeypatch.setenv("XDG_DATA_HOME", str(tmp_path))
    assert main(["man", "--install"]) == 0
    page = tmp_path / "man" / "man1" / "python-template.1"
    assert page.read_text(encoding="utf-8").startswith(f".TH {PROG.upper()} 1")
    assert "man python-template" in capsys.readouterr().out
