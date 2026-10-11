# SPDX-License-Identifier: GPL-3.0-or-later
# Copyright do codigo sob GPL-3.0 -- ver LICENSE e NOTICE.md na raiz do projeto.

"""
Confere o indice do projeto: cada documento do projeto aparece nele uma vez so.

O indice (no projeto.json, "indice") lista os documentos na ordem de leitura. Os
documentos sao os arquivos .md que o git guarda ou guardaria: os versionados e os novos
que a lista do que nao vai ao GitHub (o .gitignore) nao deixa de fora, menos o proprio
indice. Do indice contam os links pra arquivos .md, fora dos trechos de codigo; a parte do
link depois de "#" (a secao) nao conta.

Aparece FALTA pra documento que nao esta no indice, e ERRO pra documento que esta mais de
uma vez, pra link a um .md que nao existe ou que nao e documento do projeto, pra indice
que nao existe e pra projeto sem o git, porque sem ele nao ha como saber o que vai com o
projeto. Sem projeto.json (no proprio modelo, por exemplo), nao ha indice a conferir.

Roda tambem sozinho antes de cada versao gravada pelo git, chamado pelo verificador (o
arquivo pre-commit da pasta .githooks).

Uso (de qualquer pasta dentro do projeto):
    python scripts/confere_indice.py
    python scripts/confere_indice.py --projeto projeto.json
"""

import argparse
import os
import re
import sys
from collections import Counter
from pathlib import Path
from urllib.parse import unquote

sys.path.insert(0, str(Path(__file__).resolve().parent))
from comum import (EXTENSAO_DOCUMENTO, acha_projeto, caminho_do_alvo, documentos_do_projeto,  # noqa: E402
                   linhas_fora_de_codigo, procura_projeto, sem_codigo_na_linha)

LINK = re.compile(r"\[[^\]]*\]\(\s*(<[^>]*>|[^)\s]+)")
ESQUEMA = re.compile(r"^[A-Za-z][A-Za-z0-9+.-]*:")  # https:, mailto:... -- fora do projeto


def links_do_indice(indice, raiz):
    """[arquivo .md] de cada link do indice, na ordem, com o caminho inteiro."""
    links = []
    for _, linha in linhas_fora_de_codigo(indice.read_text(encoding="utf-8")):
        for alvo in LINK.findall(sem_codigo_na_linha(linha)):
            caminho = unquote(caminho_do_alvo(alvo).split("#", 1)[0])
            if not caminho or ESQUEMA.match(caminho) or not caminho.lower().endswith(EXTENSAO_DOCUMENTO):
                continue
            base = raiz if caminho.startswith("/") else indice.parent
            links.append((base / caminho.lstrip("/")).resolve())
    return links


def problemas(indice, docs, raiz):
    """[(caminho, linha)] de cada problema, cada linha ja com FALTA ou ERRO."""
    rel = lambda p: Path(os.path.relpath(p, raiz)).as_posix()  # noqa: E731
    contagem = Counter(links_do_indice(indice, raiz))
    saida = [(rel(d), f"FALTA: {rel(d)} não está no índice") for d in docs if d not in contagem]
    for alvo, n in contagem.items():
        if alvo == indice:
            saida.append((rel(alvo), f"ERRO: o índice aponta para {rel(alvo)}, que é o próprio índice"))
        elif not alvo.is_file():
            saida.append((rel(alvo), f"ERRO: o índice aponta para {rel(alvo)}, que não existe"))
        elif alvo not in docs:
            saida.append((rel(alvo), f"ERRO: o índice aponta para {rel(alvo)}, que não vai com o projeto "
                                     f"(a lista do que não vai ao GitHub o deixa de fora)"))
        elif n > 1:
            saida.append((rel(alvo), f"ERRO: {rel(alvo)} está {n} vezes no índice"))
    return sorted(saida)


def main(argv=None):
    p = argparse.ArgumentParser(description="Confere que cada documento do projeto está no índice uma vez só.")
    p.add_argument("--projeto", type=Path, help="projeto.json (padrao: o primeiro achado subindo a partir daqui)")
    a = p.parse_args(argv)
    if a.projeto is None and procura_projeto() is None:
        # sem projeto.json (no proprio modelo, por exemplo) nao ha indice de projeto a conferir
        print("Nenhum projeto.json aqui nem nas pastas acima: não há índice a conferir.")
        return 0
    projeto = acha_projeto(a.projeto)
    indice = projeto.caminho("indice").resolve()
    docs = documentos_do_projeto(projeto.raiz)
    if docs is None:
        print("ERRO: o projeto não usa o git (ou o git não está instalado): sem ele não há como saber quais "
              "documentos vão com o projeto")
        return 1
    if not indice.is_file():
        print(f"ERRO: o índice {indice} não existe: confira o caminho \"indice\" no projeto.json")
        return 1
    docs.discard(indice)
    lista = problemas(indice, docs, projeto.raiz)
    for _, linha in lista:
        print(linha)
    if lista:
        print(f"{len(lista)} problema(s) no índice, entre {len(docs)} documentos.")
        return 1
    print(f"{len(docs)} documentos, cada um uma vez no índice.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
