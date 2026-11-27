import hashlib

import pytest

from mochila.selo import selar


def test_selo_de_foto_com_exif(acervo):
    foto = acervo / "2026-11-27" / "b_manha.jpg"
    selo = selar(foto)
    assert selo["sha256"] == hashlib.sha256(foto.read_bytes()).hexdigest().upper()
    assert selo["data_exif"] == "2026:11:27 07:41:23"
    assert selo["camera"] == "SM-G781B"
    assert selo["origem_da_data"] == "exif"
    assert selo["tamanho_bytes"] == foto.stat().st_size


def test_foto_sem_exif_e_marcada(acervo):
    selo = selar(acervo / "2026-11-27" / "c_print.png")
    assert selo["data_exif"] is None
    assert selo["origem_da_data"] == "sem_exif"


def test_texto_e_selado_sem_exif(acervo):
    selo = selar(acervo / "2026-11-27" / "bloco.txt")
    assert len(selo["sha256"]) == 64
    assert selo["origem_da_data"] == "sem_exif"


def test_mesmo_conteudo_mesmo_hash_em_qualquer_lugar(acervo, tmp_path):
    original = acervo / "2026-11-27" / "bloco.txt"
    copia = tmp_path / "copia.txt"
    copia.write_bytes(original.read_bytes())
    assert selar(original)["sha256"] == selar(copia)["sha256"]


def test_arquivo_inexistente(acervo):
    with pytest.raises(FileNotFoundError):
        selar(acervo / "nao_existe.jpg")
