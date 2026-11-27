"""Fotos de teste geradas na hora, com e sem EXIF. Nenhum arquivo real é usado."""

import pytest
from PIL import Image

from mochila.selo import CAMERA, DATA_ORIGINAL, EXIF_IFD


def criar_foto(caminho, data=None, camera=None, cor="red"):
    imagem = Image.new("RGB", (8, 8), cor)
    exif = Image.Exif()
    if camera:
        exif[CAMERA] = camera
    if data:
        exif.get_ifd(EXIF_IFD)[DATA_ORIGINAL] = data
    imagem.save(caminho, exif=exif)
    return caminho


@pytest.fixture
def acervo(tmp_path, monkeypatch):
    """Um acervo com três fotos fora de ordem de nome, uma sem EXIF e um texto."""
    dia = tmp_path / "2026-11-27"
    dia.mkdir()
    criar_foto(dia / "a_tarde.jpg", data="2026:11:27 13:48:50", camera="SM-G781B", cor="blue")
    criar_foto(dia / "b_manha.jpg", data="2026:11:27 07:41:23", camera="SM-G781B", cor="green")
    criar_foto(dia / "c_print.png")
    (dia / "bloco.txt").write_text("7:41. Banks na varanda.", encoding="utf-8")
    monkeypatch.setenv("MOCHILA_ACERVO", str(tmp_path))
    return tmp_path
