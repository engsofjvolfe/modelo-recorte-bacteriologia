# SPDX-License-Identifier: GPL-3.0-or-later
# Copyright do codigo sob GPL-3.0 -- ver LICENSE e NOTICE.md na raiz do projeto.

"""
A tabela da leitura: o lugar que uma leitura das analises deu a cada trecho que as regras
do formato nao poem sozinhas -- o eixo de cada trecho numa ficha, o documento do trecho que
as regras deixam em aberto e o trecho que a leitura pos fora do material. Nao e para rodar
sozinho: o confere_moldes.py le a tabela por aqui.

A tabela e um arquivo de texto com as colunas separadas por tabulacao (TSV): o cabecalho
"id, documento, unidade, parte" e uma linha por lugar, porque um trecho pode ter mais de
um. Cada linha diz:
  - id: o id do trecho, como o analises.py o da;
  - documento: um documento de conteudo do formato; ou "fora", quando a leitura pos o
    trecho fora do material;
  - unidade: uma das unidades do documento, ou vazia quando ele nao lista as suas; numa
    linha "fora", o id da regra de fora do formato;
  - parte: num documento cujo molde tem grade, um eixo da grade da unidade (comum.grade) ou
    uma parte de abertura que recebe trechos; num documento sem grade, e numa linha "fora",
    vazia.
"""

import csv
from pathlib import Path

import lugares
from comum import MOLDE_COM_GRADE, grade, unidades
from validar_dados import le_texto

CABECALHO = ["id", "documento", "unidade", "parte"]  # as colunas da tabela, na ordem
FORA = "fora"  # o documento da linha que poe o trecho fora do material


def ler_tabela(caminho):
    """[(numero da linha, {id, documento, unidade, parte})] da tabela, sem as linhas em
    branco e sem os espacos das pontas de cada valor. ValueError, que diz o arquivo e a
    linha, quando o texto nao esta em UTF-8, o cabecalho nao e o da tabela ou uma linha nao
    tem as colunas dele."""
    caminho = Path(caminho)
    texto, erros = le_texto(caminho, caminho.name)
    if erros:
        raise ValueError(erros[0])
    linhas = list(csv.reader(texto.splitlines(), delimiter="\t", quoting=csv.QUOTE_NONE))
    if not linhas or linhas[0] != CABECALHO:
        raise ValueError(f"{caminho.name}: o cabeçalho deve ser {', '.join(CABECALHO)}, separados por tabulação")
    saida = []
    for n, campos in enumerate(linhas[1:], 2):
        if not "".join(campos).strip():
            continue
        if len(campos) != len(CABECALHO):
            raise ValueError(f"{caminho.name}, linha {n}: {len(campos)} coluna(s); a tabela tem {len(CABECALHO)}")
        saida.append((n, dict(zip(CABECALHO, (c.strip() for c in campos)))))
    return saida


def partes_validas(documento, unidade):
    """As partes que uma linha pode dar na unidade do documento, ou None quando o documento
    nao tem a unidade. Num documento cujo molde tem grade, os eixos da grade da unidade e as
    partes de abertura que recebem trechos; num documento sem grade, so a parte vazia."""
    achada = next((u for u in unidades(documento) if u["id"] == unidade), None)
    if achada is None and (unidades(documento) or unidade):
        return None
    if documento["molde"] != MOLDE_COM_GRADE:
        return [""]
    return ([e["id"] for e in grade(documento, achada)]
            + [a["id"] for a in documento.get("abertura", []) if a["recebe_trechos"]])


def erro_da_linha(linha, ids_dos_trechos, documentos, de_conteudo, regras_de_fora):
    """O que a linha tem que nao fecha com as analises ou com o formato, ou None.
    'documentos' sao os do formato, pelo id; 'de_conteudo', os ids dos de conteudo;
    'regras_de_fora', os ids das regras de fora."""
    documento, unidade, parte = linha["documento"], linha["unidade"], linha["parte"]
    if linha["id"] not in ids_dos_trechos:
        return f"nenhum trecho tem o id {linha['id']!r}"
    if documento == FORA:
        if unidade not in regras_de_fora:
            return f"posto fora por uma regra que o formato não tem: {unidade!r}"
        return f"linha de fora com a parte {parte!r}" if parte else None
    if documento not in de_conteudo:
        return f"{documento!r} não é um documento de conteúdo do formato"
    validas = partes_validas(documentos[documento], unidade)
    if validas is None:
        return (f"o documento {documento!r} não tem a unidade {unidade!r}" if unidade
                else f"sem unidade, e o documento {documento!r} lista as unidades dele")
    if parte not in validas:
        return f"o documento {documento!r} não tem a parte {parte!r}" + (f" na unidade {unidade!r}" if unidade else "")
    return None


def conferidas(linhas, ids_dos_trechos, formato):
    """(validas, erros): as linhas que fecham com as analises e com o formato, na ordem da
    tabela, e uma frase para cada uma das outras, com o numero dela: a linha que repete outra,
    o id que nenhum trecho tem, a regra de fora que o formato nao tem, o documento que nao e
    de conteudo, a unidade que o documento nao tem e a parte que a unidade nao tem. Quando um
    documento do formato tem o nome que a tabela usa para o trecho posto fora, nenhuma linha
    vale, porque as dele e as de fora nao se distinguem."""
    documentos = {d["id"]: d for d in formato["documentos"]}
    if FORA in documentos:
        return [], [f"o formato tem um documento {FORA!r}, o nome que a tabela dá ao lugar do trecho posto fora"]
    de_conteudo, regras_de_fora = set(lugares.documentos_de_conteudo(formato)), {r["id"] for r in formato["fora"]}
    validas, erros, vistas = [], [], set()
    for n, linha in linhas:
        chave = tuple(linha[c] for c in CABECALHO)
        erro = ("repete uma linha de antes" if chave in vistas
                else erro_da_linha(linha, ids_dos_trechos, documentos, de_conteudo, regras_de_fora))
        vistas.add(chave)
        if erro:
            erros.append(f"linha {n}: {erro}")
        else:
            validas.append(linha)
    return validas, erros


def por_trecho(linhas):
    """{id: [linha]} das linhas, na ordem da tabela."""
    saida = {}
    for linha in linhas:
        saida.setdefault(linha["id"], []).append(linha)
    return saida
