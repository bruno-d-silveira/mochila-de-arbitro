# Mochila de Árbitro

*A referee's kit for file provenance: an MCP server that proves where a file came from and when, locally and read-only.*

[Read in English](README.md)

O árbitro observa, registra e prova, sem decidir no lugar de ninguém. A Mochila de Árbitro faz isso com arquivos: diz qual é o conteúdo exato (SHA-256), quando a foto foi tirada (EXIF) e em que ordem as fotos de um dia aconteceram. Tudo na tua máquina, sem rede e sem escrever nada.

É para quem trabalha em campo com um caderno: árbitro, voluntário, professor, pesquisador, repórter.

## As três peças

| peça MCP | nome | o que faz |
|---|---|---|
| tool | `selar` | SHA-256, tamanho, data EXIF e câmera de um arquivo |
| resource | `cronologia://{pasta}` | as fotos de uma pasta em ordem de quando foram tiradas, cada uma com seu selo |
| prompt | `registrar_o_dia` | o método do caderno de campo: hora, fato, foto selada, sem inventar |

A tool e o resource entregam o peixe. O prompt ensina a pescar.

### Por que a data vem do EXIF

A data de modificação de um arquivo muda quando ele é copiado, baixado ou enviado. Ela não prova nada. A data EXIF é gravada pela câmera no momento da foto. Quando não existe EXIF (um print de tela, um texto), o selo diz `"origem_da_data": "sem_exif"` e não chuta.

## Instalar

Precisa de Python 3.12+ e do [uv](https://docs.astral.sh/uv/).

```bash
git clone https://github.com/bruno-d-silveira/mochila-de-arbitro
cd mochila-de-arbitro
uv sync
```

## Ligar no Claude

O servidor só enxerga a pasta que você indicar em `MOCHILA_ACERVO`.

**Claude Code, como plugin** (servidor e skill juntos, sem clonar):

```
/plugin install mochila-de-arbitro --marketplace bruno-d-silveira/mochila-de-arbitro
```

Defina `MOCHILA_ACERVO` antes de abrir o Claude Code; sem ela, o acervo é a pasta onde o Claude Code foi aberto.

**Claude Code, manual:**

```bash
claude mcp add mochila-de-arbitro -e MOCHILA_ACERVO=/caminho/do/acervo -- uv --directory /caminho/da/mochila-de-arbitro run python -m mochila.servidor
```

**Claude Desktop** (`claude_desktop_config.json`):

```json
{
  "mcpServers": {
    "mochila-de-arbitro": {
      "command": "uv",
      "args": ["--directory", "/caminho/da/mochila-de-arbitro", "run", "python", "-m", "mochila.servidor"],
      "env": { "MOCHILA_ACERVO": "/caminho/do/acervo" }
    }
  }
}
```

Depois é só pedir: *"Monta a cronologia das fotos de hoje"*, ou usar o prompt `registrar_o_dia`.

## Exemplo

```
cronologia://2026-11-27

2026:11:27 07:41:23  2F7E05DF63B2  074123_2F7E05DF63B2.jpg
2026:11:27 08:22:49  E53BABE149CB  082249_E53BABE149CB.jpg
2026:11:27 08:37:33  F3E845CAEC90  083733_F3E845CAEC90.jpg
```

## Segurança

- **Somente leitura.** Nenhuma peça escreve, apaga ou move arquivo. A tool `selar` se declara `readOnlyHint`.
- **Presa ao acervo.** Caminhos com `../` ou que saem de `MOCHILA_ACERVO` são recusados.
- **Sem rede.** Nada sai da máquina. Os arquivos de quem usa continuam sendo de quem usa.

## Testes

```bash
uv run pytest -q
```

As fotos de teste são geradas na hora, com e sem EXIF. Nenhum arquivo real entra nos testes.

## O que está aqui e o que não está

Esta é a v1 aberta da Mochila de Árbitro. O motor do BRAIN, o film reel, o data lake, a fábula, a trilha de cuidado com memória e o carteiro de duas testemunhas são obras separadas do autor e **não** fazem parte deste repositório nem desta licença.

A ideia da mochila nasceu em abril de 2026, numa manhã na Joaquina, e virou episódio da fábula: [A Mochila do Árbitro](https://github.com/bruno-d-silveira/brain-project/blob/main/fabulas/s02e03_a_mochila_do_arbitro.md).

## Licença

[Apache-2.0](LICENSE). O nome "Mochila de Árbitro" não é licenciado (ver [NOTICE](NOTICE)).
