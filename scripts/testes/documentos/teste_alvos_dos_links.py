# SPDX-License-Identifier: GPL-3.0-or-later
# Copyright do codigo sob GPL-3.0 -- ver LICENSE e NOTICE.md na raiz do projeto.

"""Confere que nenhum script de uma pasta escreve o alvo de um link Markdown sem passar por
alvo_markdown (do comum.py), que poe entre <> o caminho com espaco: um "]({" num texto do
script tem de seguir com "alvo_markdown(". Um molde com "{}" vazio fica com quem o
preenche. Mostra cada linha que nao segue e sai com codigo 0 quando nenhuma aparece. Uso:
    python3 -I teste_alvos_dos_links.py <pasta dos scripts>
"""
import re
import sys
from pathlib import Path

ALVO_SEM_FUNCAO = re.compile(r"\]\(\{(?!alvo_markdown\(|\})")

falhas = [f"{arquivo.name}:{n}: {linha.strip()}"
          for arquivo in sorted(Path(sys.argv[1]).glob("*.py"))
          for n, linha in enumerate(arquivo.read_text(encoding="utf-8").split("\n"), 1)
          if ALVO_SEM_FUNCAO.search(linha)]
print("\n".join(falhas) or "nenhum alvo de link fora do alvo_markdown")
sys.exit(1 if falhas else 0)
