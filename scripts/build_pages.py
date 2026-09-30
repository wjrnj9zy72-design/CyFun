"""Génère dans docs/ des pages HTML autonomes (hors de Claude) pour GitHub Pages.

Les fichiers source sont des fragments publiés comme artefacts Claude : la plateforme
ajoute elle-même doctype, <head> et <body>. Ce script ajoute cet habillage.
Usage : python3 scripts/build_pages.py
"""
import pathlib
import re

ROOT = pathlib.Path(__file__).resolve().parent.parent
PAGES = ["cyber-clash.html", "boisvert-grandit.html", "atelier-cyfun-small.html"]
HEAD = """<!doctype html>
<html lang="fr">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
{title}
<style>body{{margin:0}}img{{max-width:100%}}[hidden]{{display:none!important}}</style>
</head>
<body>
"""

for name in PAGES:
    src = (ROOT / name).read_text(encoding="utf-8")
    m = re.search(r"<title>.*?</title>", src, re.S)
    title = m.group(0) if m else "<title>CyFun</title>"
    body = src.replace(title, "", 1) if m else src
    (ROOT / "docs" / name).write_text(HEAD.format(title=title) + body + "\n</body>\n</html>\n", encoding="utf-8")
    print("docs/" + name)
