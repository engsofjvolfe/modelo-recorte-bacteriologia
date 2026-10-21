# SPDX-License-Identifier: GPL-3.0-or-later
# Copyright do codigo sob GPL-3.0 -- ver LICENSE e NOTICE.md na raiz do projeto.

"""
Monta a lista dos trechos que uma IA escreveu no material, a partir das marcas nos textos.

Um texto do material marca o que uma IA escreveu, sem fonte, entre a abertura e o
fechamento de IA que o projeto.json da ("ia": "abre" e "fecha"), como "[IA: texto]", com a
marca inteira numa linha so. O script le cada .md da pasta do material gerado
("material_gerado") e das subpastas dela, fora dos trechos de codigo, e grava a lista
("trechos_de_ia", nos caminhos): cada marca num item numerado, na ordem dos arquivos e das
linhas, com o titulo do documento (o de nivel 1, ou o caminho dele quando nao tem), o link
para a linha da marca e o texto marcado. Quando uma marca sai do texto, porque alguem achou
a fonte e escreveu o trecho com ela, o item sai da lista na proxima rodada, e os outros se
renumeram. A mesma entrada da sempre o mesmo arquivo.

Aparece ERRO, e nada e gravado, para a marca que abre e nao fecha na mesma linha, para a
marca vazia e para o texto fora do UTF-8. Com --conferir, nada e gravado: aparece FALTA se
a lista gravada nao e a que o script gravaria agora. Sem "ia" no projeto.json, ou com ele
null, nao ha lista a montar.

Roda tambem sozinho, com --conferir, antes de cada versao gravada pelo git, chamado pelo
verificador (o arquivo pre-commit da pasta .githooks). Quem importa este script tem as
marcas de IA do material (marcas_de_ia), que o confere_cartoes.py usa para conferir os
cartoes escritos por IA.

Uso (de qualquer pasta dentro do projeto):
    python scripts/trechos_de_ia.py
    python scripts/trechos_de_ia.py --conferir
    python scripts/trechos_de_ia.py --projeto projeto.json
"""

import argparse
import collections
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from comum import (EXTENSAO_DOCUMENTO, acha_projeto, alvo_markdown, link, linhas_fora_de_codigo,  # noqa: E402
                   no_projeto, rodape_da_licenca, sem_codigo_na_linha)
from glossario import TITULO, texto_puro  # noqa: E402
from validar_dados import le_texto  # noqa: E402

CHAVE_IA = "ia"  # a chave do projeto.json com as marcas de IA ("abre", "fecha", "fonte"), ou null
CAMINHO_LISTA = "trechos_de_ia"  # o caminho da lista, nos caminhos do projeto.json
TITULO_LISTA = "# Trechos escritos por IA"
ABERTURA = ("Os trechos do material que uma inteligência artificial escreveu, sem fonte, e que precisam ser "
            "verificados, cada um com o documento e o link para a linha em que está. Quando alguém acha a fonte de "
            "um trecho e tira a marca dele do texto, o trecho sai desta lista.")
ALVO_DA_LINHA = "{}#L{}"  # o link para uma linha do arquivo
Marca = collections.namedtuple("Marca", "arquivo linha texto")  # uma marca de IA: o arquivo, a linha e o texto


def marcas_de_ia(projeto):
    """([Marca], erros) dos textos do material, na ordem dos arquivos e das linhas; (None, []) quando o projeto nao
    marca trechos de IA."""
    ia = projeto.dados.get(CHAVE_IA)
    if not ia:
        return None, []
    abre, fecha = ia["abre"], ia["fecha"]
    marca = re.compile(re.escape(abre) + "(.*?)" + re.escape(fecha))
    marcas, erros = [], []
    for arquivo in sorted(a for a in projeto.caminho("material_gerado").rglob(f"*{EXTENSAO_DOCUMENTO}")
                          if a.is_file()):
        nome = no_projeto(arquivo, projeto)
        texto, ruins = le_texto(arquivo, nome)
        erros += ruins
        for n, linha in ([] if texto is None else linhas_fora_de_codigo(texto)):
            linha = sem_codigo_na_linha(linha)
            achadas = list(marca.finditer(linha))
            if linha.count(abre) > len(achadas):
                erros.append(f"marca de IA que abre e não fecha na mesma linha em {nome}:{n}")
            for m in achadas:
                if not m.group(1).strip():
                    erros.append(f"marca de IA vazia em {nome}:{n}")
                marcas.append(Marca(arquivo, n, m.group(1).strip()))
    return marcas, erros


def titulo_do_documento(arquivo, projeto):
    """O titulo de nivel 1 do documento, ou o caminho dele, a partir da pasta do projeto, quando ele nao tem."""
    for _, linha in linhas_fora_de_codigo(arquivo.read_text(encoding="utf-8")):
        m = TITULO.match(linha)
        if m and len(m.group(1)) == 1:
            return texto_puro(m.group(2))
    return no_projeto(arquivo, projeto)


def lista(projeto, marcas):
    """O texto da lista dos trechos de IA."""
    saida = projeto.caminho(CAMINHO_LISTA)
    titulos = {m.arquivo: titulo_do_documento(m.arquivo, projeto) for m in marcas}
    corpo = [TITULO_LISTA, "", ABERTURA, ""]
    corpo += [f"{i}. {titulos[m.arquivo]}, [linha {m.linha}]"
              f"({alvo_markdown(ALVO_DA_LINHA.format(link(m.arquivo, saida), m.linha))}): {m.texto}"
              for i, m in enumerate(marcas, 1)]
    corpo += ([""] if marcas else []) + rodape_da_licenca(projeto.caminho("licenca_conteudo"),
                                                          projeto.valor("nome_licenca_conteudo"), saida)
    return "\n".join(corpo) + "\n"


def main(argv=None):
    p = argparse.ArgumentParser(description="Monta a lista dos trechos que uma IA escreveu no material.")
    p.add_argument("--conferir", action="store_true",
                   help="não grava: confere se a lista gravada é a que o script gravaria agora")
    p.add_argument("--projeto", type=Path, help="projeto.json (padrao: o primeiro achado subindo a partir daqui)")
    a = p.parse_args(argv)
    projeto = acha_projeto(a.projeto)
    marcas, erros = marcas_de_ia(projeto)
    if marcas is None:
        print(f"O projeto.json não marca trechos de IA (\"{CHAVE_IA}\"): não há lista a montar.")
        return 0
    for e in erros:
        print("ERRO:", e)
    if erros:
        print("A lista dos trechos de IA não foi gravada.")
        return 1
    texto, saida = lista(projeto, marcas), projeto.caminho(CAMINHO_LISTA)
    if a.conferir:
        if not saida.is_file() or saida.read_text(encoding="utf-8") != texto:
            print(f"FALTA: a lista {saida} não é a que as marcas de IA dão: rode python scripts/trechos_de_ia.py")
            return 1
        print(f"A lista dos trechos de IA está em dia: {len(marcas)} trecho(s).")
        return 0
    saida.parent.mkdir(parents=True, exist_ok=True)
    saida.write_text(texto, encoding="utf-8")
    print(f"{len(marcas)} trecho(s) de IA gravado(s) em {saida}.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
