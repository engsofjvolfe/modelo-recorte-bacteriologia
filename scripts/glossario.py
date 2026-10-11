# SPDX-License-Identifier: GPL-3.0-or-later
# Copyright do codigo sob GPL-3.0 -- ver LICENSE e NOTICE.md na raiz do projeto.

"""
Monta o glossario do projeto a partir das definicoes marcadas nos documentos.

Um documento define um termo marcando-o, no lugar onde diz o que ele quer dizer, com
<dfn>termo</dfn>, a marca do HTML pra "aqui este termo e definido". O script recolhe cada
marca dos documentos do projeto (os mesmos que o confere_indice.py confere: os .md que vao
com o projeto), fora dos trechos de codigo, e grava o glossario (no projeto.json,
"glossario"): cada termo numa linha, em ordem alfabetica (sem contar acentos nem
maiusculas), com o link pra secao onde ele e definido. Nada do texto da definicao e
copiado: o glossario so aponta. A mesma entrada da sempre o mesmo arquivo.

Aparece ERRO, e nada e gravado, pra termo definido em mais de um lugar (sem contar
maiusculas), pra marca vazia e pra projeto sem o git. Com --conferir, nada e gravado:
aparece FALTA se o glossario gravado nao e o que o script gravaria agora. Sem
projeto.json (no proprio modelo, por exemplo), nao ha glossario a montar.

Roda tambem sozinho, com --conferir, antes de cada versao gravada pelo git, chamado pelo
verificador (o arquivo pre-commit da pasta .githooks).

Uso (de qualquer pasta dentro do projeto):
    python scripts/glossario.py
    python scripts/glossario.py --conferir
    python scripts/glossario.py --projeto projeto.json
"""

import argparse
import os
import re
import sys
import unicodedata
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from comum import (acha_projeto, alvo_markdown, ancora, documentos_do_projeto, link,  # noqa: E402
                   linhas_fora_de_codigo, procura_projeto, rodape_da_licenca, sem_codigo_na_linha)

TITULO_GLOSSARIO = "# Glossário"
ABERTURA = ("As palavras que os documentos do projeto definem, em ordem alfabética, cada uma com o link para "
            "o lugar onde ela é definida.")
SEPARADOR = " › "  # entre o documento e a secao, no texto do link
DFN = re.compile(r"<dfn(?:\s[^>]*)?>(.*?)</dfn>", re.IGNORECASE | re.DOTALL)
TITULO = re.compile(r"^ {0,3}(#{1,6})[ \t]+(.*?)(?:[ \t]+#+)?[ \t]*$")
LINK_MD = re.compile(r"!?\[([^\]]*)\]\([^)]*\)")
TAG = re.compile(r"<[^>]+>")
ENFASE = re.compile(r"(\*{1,3}|_{1,3})(.+?)\1")
CODIGO = re.compile(r"(`+)(.+?)\1")


def texto_puro(markdown):
    """O texto como ele aparece pra quem le: sem links (fica o texto deles), sem marcas de
    HTML, de enfase nem de codigo, com os espacos juntados."""
    texto = TAG.sub("", LINK_MD.sub(r"\1", markdown))
    texto = CODIGO.sub(r"\2", ENFASE.sub(r"\2", texto))
    return " ".join(texto.split())


def chave_alfabetica(termo):
    sem_acento = "".join(c for c in unicodedata.normalize("NFKD", termo) if not unicodedata.combining(c))
    return sem_acento.casefold(), termo


def definicoes(documento):
    """(titulo do documento, [(termo, linha, ancora da secao ou None, nome da secao ou None)]).
    A secao de uma marca e o titulo mais perto acima dela; o titulo de nivel 1 e o do
    documento, e a marca debaixo dele, ou antes de qualquer titulo, aponta o documento."""
    titulos, linhas, vistas = [], {}, {}
    for n, linha in linhas_fora_de_codigo(documento.read_text(encoding="utf-8")):
        linhas[n] = sem_codigo_na_linha(linha)
        m = TITULO.match(linha)
        if m:
            nome = texto_puro(m.group(2))
            base = ancora(nome)
            vistas[base] = vistas.get(base, -1) + 1  # o segundo titulo igual ganha -1, o terceiro -2...
            titulos.append((n, len(m.group(1)), nome, base + (f"-{vistas[base]}" if vistas[base] else "")))
    nivel1 = next((nome for _, nivel, nome, _ in titulos if nivel == 1), None)
    texto = "\n".join(linhas.get(n, "") for n in range(1, max(linhas, default=0) + 1))
    achadas = []
    for m in DFN.finditer(texto):
        n = texto.count("\n", 0, m.start()) + 1
        secao = next(((nome, anc) for t, nivel, nome, anc in reversed(titulos) if t <= n and nivel > 1), None)
        acima = [nivel for t, nivel, _, _ in titulos if t <= n]
        if secao is not None and acima and acima[-1] == 1:
            secao = None  # a marca esta direto debaixo do titulo do documento
        achadas.append((texto_puro(m.group(1)), n, secao[1] if secao else None, secao[0] if secao else None))
    return nivel1, achadas


def glossario(projeto, docs):
    """(linhas do glossario, erros)."""
    saida = projeto.caminho("glossario").resolve()
    rel = lambda p: Path(os.path.relpath(p, projeto.raiz)).as_posix()  # noqa: E731
    termos, erros = {}, []
    for doc in sorted(docs - {saida}):
        titulo, achadas = definicoes(doc)
        for termo, n, anc, secao in achadas:
            if not termo:
                erros.append(f"marca <dfn> vazia em {rel(doc)}:{n}")
                continue
            onde = (doc, n, anc, (titulo or rel(doc)) + (SEPARADOR + secao if secao else ""))
            termos.setdefault(termo.casefold(), []).append((termo, onde))
    for lugares in termos.values():
        if len(lugares) > 1:
            erros.append(f"o termo \"{lugares[0][0]}\" é definido em mais de um lugar: "
                         + ", ".join(f"{rel(doc)}:{n}" for _, (doc, n, _, _) in lugares))
    entradas = sorted(((lugares[0][0], lugares[0][1]) for lugares in termos.values()),
                      key=lambda e: chave_alfabetica(e[0]))
    corpo = [TITULO_GLOSSARIO, "", ABERTURA, ""]
    corpo += [f"- **{termo}** — [{nome}]({alvo_markdown(link(doc, saida) + (f'#{anc}' if anc else ''))})"
              for termo, (doc, _, anc, nome) in entradas]
    corpo += ([""] if entradas else []) + rodape_da_licenca(projeto.caminho("licenca_conteudo"),
                                                             projeto.valor("nome_licenca_conteudo"), saida)
    return "\n".join(corpo) + "\n", sorted(erros), len(entradas)


def main(argv=None):
    p = argparse.ArgumentParser(description="Monta o glossário a partir das definições marcadas nos documentos.")
    p.add_argument("--conferir", action="store_true",
                   help="não grava: confere se o glossário gravado é o que o script gravaria agora")
    p.add_argument("--projeto", type=Path, help="projeto.json (padrao: o primeiro achado subindo a partir daqui)")
    a = p.parse_args(argv)
    if a.projeto is None and procura_projeto() is None:
        # sem projeto.json (no proprio modelo, por exemplo) nao ha glossario de projeto a montar
        print("Nenhum projeto.json aqui nem nas pastas acima: não há glossário a montar.")
        return 0
    projeto = acha_projeto(a.projeto)
    docs = documentos_do_projeto(projeto.raiz)
    if docs is None:
        print("ERRO: o projeto não usa o git (ou o git não está instalado): sem ele não há como saber quais "
              "documentos vão com o projeto")
        return 1
    texto, erros, n = glossario(projeto, docs)
    for e in erros:
        print("ERRO:", e)
    if erros:
        print("O glossário não foi gravado.")
        return 1
    saida = projeto.caminho("glossario")
    if a.conferir:
        if not saida.is_file() or saida.read_text(encoding="utf-8") != texto:
            print(f"FALTA: o glossário {saida} não é o que os documentos definem: rode python scripts/glossario.py")
            return 1
        print(f"O glossário está em dia: {n} termo(s).")
        return 0
    saida.parent.mkdir(parents=True, exist_ok=True)
    saida.write_text(texto, encoding="utf-8")
    print(f"{n} termo(s) gravado(s) em {saida}.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
