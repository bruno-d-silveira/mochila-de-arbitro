"""O servidor MCP: as três primitivas registradas e a trava do acervo."""

import asyncio
import json

import pytest

from mochila import servidor


def rodar(corrotina):
    return asyncio.run(corrotina)


def test_tres_primitivas_registradas():
    ferramentas = rodar(servidor.mochila.list_tools())
    modelos = rodar(servidor.mochila.list_resource_templates())
    prompts = rodar(servidor.mochila.list_prompts())
    assert [f.name for f in ferramentas] == ["selar"]
    assert [m.uri_template for m in modelos] == ["cronologia://{pasta}"]
    assert [p.name for p in prompts] == ["registrar_o_dia"]


def test_selar_e_somente_leitura():
    ferramenta = rodar(servidor.mochila.list_tools())[0]
    assert ferramenta.annotations.read_only_hint is True


def test_selar_pelo_servidor(acervo):
    selo = servidor.selar("2026-11-27/b_manha.jpg")
    assert selo["data_exif"] == "2026:11:27 07:41:23"


def test_cronologia_pelo_servidor(acervo):
    lista = json.loads(servidor.cronologia("2026-11-27"))
    assert [s["arquivo"] for s in lista][:2] == ["b_manha.jpg", "a_tarde.jpg"]


@pytest.mark.parametrize("fuga", ["../segredo.txt", "..\\segredo.txt", "2026-11-27/../../segredo.txt"])
def test_caminho_fora_do_acervo_e_recusado(acervo, fuga):
    with pytest.raises(ValueError):
        servidor.selar(fuga)


def test_prompt_traz_o_metodo():
    texto = servidor.registrar_o_dia("27/11/2026")
    assert "27/11/2026" in texto
    assert "cronologia://" in texto and "selar" in texto
    assert "Não invente" in texto
