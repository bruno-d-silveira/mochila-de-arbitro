"""Servidor MCP da Mochila de Árbitro: uma tool, um resource e um prompt.

- tool `selar`: o selo de um arquivo (peixe);
- resource `cronologia://{pasta}`: as fotos da pasta em ordem (peixe);
- prompt `registrar_o_dia`: o método do caderno de campo (ensinar a pescar).

Tudo local: nada sai da máquina e o servidor só lê, nunca escreve.
O servidor só enxerga o que está dentro da pasta MOCHILA_ACERVO.

Rodar:  MOCHILA_ACERVO=/caminho/do/acervo  uv run python -m mochila.servidor
"""

import json
import os
from pathlib import Path

from mcp.server.mcpserver import MCPServer
from mcp.types import ToolAnnotations

from mochila.cronologia import cronologia as montar_cronologia
from mochila.selo import selar as selar_arquivo

mochila = MCPServer(
    "mochila-de-arbitro",
    instructions=(
        "Prova de origem de arquivos do acervo, local e somente leitura. "
        "Use selar para o hash e a data EXIF de um arquivo, cronologia://<pasta> "
        "para pôr as fotos em ordem e registrar_o_dia para o método do caderno de campo."
    ),
)


def acervo() -> Path:
    return Path(os.getenv("MOCHILA_ACERVO", ".")).resolve()


def no_acervo(relativo: str) -> Path:
    """Resolve um caminho dentro do acervo e recusa qualquer saída dele (ex.: ../)."""
    raiz = acervo()
    alvo = (raiz / relativo).resolve()
    if alvo != raiz and raiz not in alvo.parents:
        raise ValueError("Caminho fora do acervo.")
    return alvo


@mochila.tool(
    name="selar",
    description=(
        "Sela um arquivo do acervo: SHA-256, tamanho, data EXIF de quando a foto foi tirada "
        "e câmera. Recebe o caminho relativo à pasta do acervo. Não usa a data de modificação."
    ),
    annotations=ToolAnnotations(readOnlyHint=True, openWorldHint=False),
)
def selar(caminho: str) -> dict:
    return selar_arquivo(no_acervo(caminho))


@mochila.resource(
    "cronologia://{pasta}",
    mime_type="application/json",
    description="Fotos de uma pasta do acervo em ordem de EXIF, cada uma com seu selo. Use '.' para a raiz.",
)
def cronologia(pasta: str) -> str:
    return json.dumps(montar_cronologia(no_acervo(pasta)), ensure_ascii=False, indent=2)


@mochila.prompt(
    name="registrar_o_dia",
    description="O método do caderno de campo para registrar um dia com fatos, horas e fotos seladas.",
)
def registrar_o_dia(data: str) -> str:
    return f"""Vamos registrar o dia {data} como um caderno de campo.

1. Cada linha começa com a hora (HH:MM) e traz um fato: o que aconteceu, com nome, lugar ou objeto.
   Parágrafo sem nome, data ou objeto dentro é ar: corte ou pergunte ao autor.
2. As fotos entram pela ordem de quando foram tiradas: leia o resource cronologia://<pasta>.
   Nunca use a data de modificação do arquivo.
3. Cada foto citada leva o selo: use a tool selar e anote os 12 primeiros caracteres do hash.
4. Não invente. Se faltar hora, fato ou foto, pergunte.
5. O texto é do autor: organize e aponte lacunas, não reescreva a voz dele."""


if __name__ == "__main__":
    mochila.run()
