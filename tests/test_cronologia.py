import pytest

from mochila.cronologia import cronologia


def test_ordem_pela_data_exif_e_nao_pelo_nome(acervo):
    nomes = [s["arquivo"] for s in cronologia(acervo / "2026-11-27")]
    assert nomes == ["b_manha.jpg", "a_tarde.jpg", "c_print.png"]


def test_sem_exif_vai_para_o_fim_marcada(acervo):
    ultima = cronologia(acervo / "2026-11-27")[-1]
    assert ultima["origem_da_data"] == "sem_exif"


def test_texto_fica_fora_da_cronologia_de_fotos(acervo):
    nomes = [s["arquivo"] for s in cronologia(acervo / "2026-11-27")]
    assert "bloco.txt" not in nomes


def test_pasta_inexistente(acervo):
    with pytest.raises(NotADirectoryError):
        cronologia(acervo / "nao_existe")
