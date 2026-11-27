"""Cronologia: as fotos de uma pasta em ordem de quando foram tiradas."""

from pathlib import Path

from mochila.selo import selar

EXTENSOES = {".jpg", ".jpeg", ".png", ".tif", ".tiff", ".webp", ".heic"}


def cronologia(pasta: Path) -> list[dict]:
    """Sela cada imagem da pasta e ordena pela data EXIF.

    As fotos sem EXIF vão para o fim, em ordem de nome, marcadas como
    "sem_exif": a ordem delas não é prova de nada.
    """
    pasta = Path(pasta)
    if not pasta.is_dir():
        raise NotADirectoryError(f"Pasta não encontrada: {pasta.name}")

    selos = [selar(f) for f in sorted(pasta.iterdir()) if f.is_file() and f.suffix.lower() in EXTENSOES]
    com_data = sorted((s for s in selos if s["data_exif"]), key=lambda s: s["data_exif"])
    sem_data = [s for s in selos if not s["data_exif"]]
    return com_data + sem_data
