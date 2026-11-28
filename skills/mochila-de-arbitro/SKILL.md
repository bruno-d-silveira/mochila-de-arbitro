---
name: mochila-de-arbitro
description: Prove where a file came from and when, locally and read-only. Use when the user asks to verify a file's origin or integrity, get the SHA-256 of a file, find when a photo was really taken (EXIF, never the modified date), put a day's photos in chronological order, or write a field-notebook log of a day with sealed photos. Works through the mochila-de-arbitro MCP server (tool selar, resource cronologia://{pasta}, prompt registrar_o_dia).
---

# Mochila de Árbitro: a referee's kit for file provenance

A referee observes, records and proves, without deciding for anyone. This skill does the same with files: it says what the exact content is (SHA-256), when a photo was taken (EXIF) and in what order a day's photos happened. Everything stays on the user's machine. Nothing is written, moved or sent anywhere.

## When to use it

- "Is this the same file I sent last week?" → seal it and compare hashes.
- "When was this photo actually taken?" → seal it and read the EXIF date.
- "Put today's photos in order" → read the chronology of the folder.
- "Help me log my day" → use the field-notebook method with sealed photos.

Do not use it to edit, rename, sort on disk or delete files. It only reads.

## The three pieces

| MCP piece | name | what it returns |
|---|---|---|
| tool | `selar` | SHA-256, size, EXIF date the photo was taken, camera, and `origem_da_data` |
| resource | `cronologia://{pasta}` | photos of a folder in EXIF order, each with its seal (`.` = the archive root) |
| prompt | `registrar_o_dia` | the field-notebook method: time, fact, sealed photo, nothing invented |

Paths are always **relative to the archive folder** (`MOCHILA_ACERVO`). The server refuses any path that leaves it, such as `../`.

## Rules the agent must follow

1. **Never use the file's modified date as evidence.** It changes on every copy, download or upload. The date comes from EXIF only.
2. **When there is no EXIF** (a screenshot, a text file), the seal says `"origem_da_data": "sem_exif"`. Report that plainly. Do not guess a date.
3. **Quote hashes, do not paraphrase them.** When citing a photo in a log, use the first 12 characters of its SHA-256.
4. **Two files are the same only if their SHA-256 is identical.** Same name, size or date proves nothing.
5. **Do not invent.** If a time, fact or photo is missing from the user's notes, ask.
6. **The text belongs to the author.** In a day log, organize and point out gaps; do not rewrite the author's voice.

## Typical flows

**Verify a file**
1. Call `selar` with the path relative to the archive.
2. Report the hash, the EXIF date (or `sem_exif`) and the camera, if any.
3. If the user has an earlier hash, compare all 64 characters.

**Order a day's photos**
1. Read `cronologia://<folder>` (for example `cronologia://2026-11-27`).
2. Present time, the first 12 characters of the hash and the file name, oldest first.
3. List separately the files without EXIF; they have no place on the timeline.

**Log a day**
1. Get the `registrar_o_dia` prompt with the date.
2. Match each line of the user's notes (HH:MM + fact) to the photos from the chronology.
3. Mark gaps: hours with no fact, photos with no line, lines with no photo.

## If the MCP server is not available

If the tool `selar` does not exist in this session, the server is not installed. Tell the user once and give these steps; do not try to compute hashes or EXIF another way and present them as the mochila's output.

Requirements: Python 3.12+ and [uv](https://docs.astral.sh/uv/).

**As a Claude Code plugin** (installs the server and this skill together):

```
/plugin install mochila-de-arbitro --marketplace bruno-d-silveira/mochila-de-arbitro
```

The first start downloads the server's two Python dependencies (`mcp`, `pillow`) from PyPI through uv. After that it runs offline.

Set the archive folder before starting Claude Code, for example `export MOCHILA_ACERVO=/path/to/archive` (PowerShell: `$env:MOCHILA_ACERVO = "C:\path\to\archive"`).

**Manually, in any MCP client:**

```
git clone https://github.com/bruno-d-silveira/mochila-de-arbitro
cd mochila-de-arbitro
uv sync
claude mcp add mochila-de-arbitro -e MOCHILA_ACERVO=/path/to/archive -- uv --directory /path/to/mochila-de-arbitro run python -m mochila.servidor
```

For Claude Desktop, Cursor and other clients, the same command goes in their MCP config: `uv --directory <mochila folder> run python -m mochila.servidor`, with `MOCHILA_ACERVO` in `env`.

## Security

- Read-only: no piece writes, deletes or moves a file; `selar` declares `readOnlyHint`.
- Locked to the archive folder set in `MOCHILA_ACERVO`.
- No network: the user's files stay with the user.

License: Apache-2.0. The name "Mochila de Árbitro" is not licensed (see NOTICE in the repository).
