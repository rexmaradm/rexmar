#!/usr/bin/env python3
"""Convierte front-matter YAML (---) a TOML (+++) para Zola."""
import frontmatter
import html
import pathlib
import sys

CONTENT_DIR = pathlib.Path(sys.argv[1] if len(sys.argv) > 1 else "content")

def convert(path: pathlib.Path) -> None:
    post = frontmatter.load(path)
    meta = post.metadata

    # Construye las líneas TOML
    lines = ["+++"]

    # Title (decodifica entidades HTML como &amp; → &)
    title = html.unescape(str(meta.get("title", "")))
    lines.append(f'title = "{title}"')

    # Date (normaliza a YYYY-MM-DD)
    date = meta.get("date")
    if date is not None:
        if hasattr(date, "strftime"):
            date_str = date.strftime("%Y-%m-%d")
        else:
            date_str = str(date)[:10]
        lines.append(f"date = {date_str}")

    # Author
    author = meta.get("author")
    if author:
        lines.append(f'author = "{author}"')

    # Aliases (lista)
    aliases = meta.get("aliases")
    if aliases:
        if isinstance(aliases, str):
            aliases = [aliases]
        aliases_toml = ", ".join(f'"{a}"' for a in aliases)
        lines.append(f"aliases = [{aliases_toml}]")

    # Tags (si existen)
    tags = meta.get("tags")
    if tags:
        if isinstance(tags, str):
            tags = [tags]
        tags_toml = ", ".join(f'"{t}"' for t in tags)
        lines.append(f"tags = [{tags_toml}]")

    # Excerpt (si existe y no está vacío)
    excerpt = meta.get("excerpt")
    if excerpt:
        lines.append(f'excerpt = "{excerpt}"')

    lines += ["+++", ""]

    # Escribe el archivo con el nuevo front-matter + contenido original
    new_content = "\n".join(lines) + post.content
    path.write_text(new_content, encoding="utf-8")
    print(f"✓ {path}")

# Recorre todos los .md recursivamente (excluye _index.md)
for md in CONTENT_DIR.rglob("*.md"):
    if md.name == "_index.md":
        continue
    try:
        convert(md)
    except Exception as e:
        print(f"✗ FALLÓ {md}: {e}", file=sys.stderr)

print("\n¡Conversión completada!")   
