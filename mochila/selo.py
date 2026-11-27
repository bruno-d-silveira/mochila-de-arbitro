"""Selo: a prova de origem de um arquivo.

Lê só o que está no próprio arquivo: o SHA-256 do conteúdo, a data em que a
foto foi tirada (EXIF) e a câmera. A data de modificação do sistema não entra,
porque muda quando o arquivo é copiado e não prova nada.
"""

import hashlib
from pathlib import Path

from PIL import Image, UnidentifiedImageError

EXIF_IFD = 0x8769       # bloco onde a câmera guarda os detalhes da foto
DATA_ORIGINAL = 36867   # DateTimeOriginal: quando a foto foi tirada
DATA_IMAGEM = 306       # DateTime: data gravada na imagem (reserva)
CAMERA = 272            # Model


def sha256(caminho: Path, bloco: int = 1 << 20) -> str:
    """SHA-256 do conteúdo, lido em blocos para não carregar arquivo grande na memória."""
    resumo = hashlib.sha256()
    with open(caminho, "rb") as arquivo:
        for pedaco in iter(lambda: arquivo.read(bloco), b""):
            resumo.update(pedaco)
    return resumo.hexdigest().upper()


def ler_exif(caminho: Path) -> dict:
    """Data e câmera do EXIF; None quando o arquivo não é imagem ou não tem EXIF."""
    try:
        with Image.open(caminho) as imagem:
            exif = imagem.getexif()
    except (UnidentifiedImageError, OSError):
        return {"data_exif": None, "camera": None}

    data = exif.get_ifd(EXIF_IFD).get(DATA_ORIGINAL) or exif.get(DATA_IMAGEM)
    camera = exif.get(CAMERA)
    return {
        "data_exif": str(data).strip("\x00 ") if data else None,
        "camera": str(camera).strip("\x00 ") if camera else None,
    }


def selar(caminho: Path) -> dict:
    """O selo completo de um arquivo."""
    caminho = Path(caminho)
    if not caminho.is_file():
        raise FileNotFoundError(f"Arquivo não encontrado: {caminho.name}")

    exif = ler_exif(caminho)
    return {
        "arquivo": caminho.name,
        "sha256": sha256(caminho),
        "tamanho_bytes": caminho.stat().st_size,
        "data_exif": exif["data_exif"],
        "camera": exif["camera"],
        "origem_da_data": "exif" if exif["data_exif"] else "sem_exif",
    }
