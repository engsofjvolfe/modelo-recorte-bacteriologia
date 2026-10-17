# SPDX-License-Identifier: GPL-3.0-or-later
# Copyright do codigo sob GPL-3.0 -- ver LICENSE e NOTICE.md na raiz do projeto.

"""
A tabela da leitura: o lugar que uma leitura das analises deu a cada trecho que as regras
do formato nao poem sozinhas -- a entrada e o eixo de cada trecho numa ficha, o documento do
trecho que as fontes do formato deixam em aberto, o lugar novo do trecho de uma aula ate a
ultima sem lugar (o limite tirou todos os dele, ou as fontes nao lhe dao documento) e o
trecho que a leitura pos fora do material. Nao e para rodar sozinho: o confere_moldes.py le
a tabela por aqui.

A tabela e um texto com as colunas separadas por tabulacao (TSV), lido pelo tabela.py: o
cabecalho "id, documento, unidade, parte" e uma linha por lugar, porque um trecho pode ter
mais de um. Cada linha diz:
  - id: o id do trecho, como o analises.py o da;
  - documento: um documento de conteudo do formato; ou "fora", quando a leitura pos o
    trecho fora do material;
  - unidade: um id do documento -- de uma unidade, de um item ou de um conjunto --, ou
    vazia, quando a entrada vem do destino do trecho ou o documento nao lista unidades;
    numa linha "fora", o id da regra de fora do formato;
  - parte: num documento cujo molde tem grade, uma parte da grade do id (comum.grade) ou
    uma parte de abertura que recebe trechos; num documento sem grade, e numa linha "fora",
    vazia.

Uma entrada e o que recebe trechos dentro de um documento (comum.Entrada): uma unidade sem
itens, um item, a unidade com itens (a entrada da abertura dela) ou o documento que nao
lista unidades. As partes de cada entrada ficam aqui, num lugar so, e valem tambem para o
lugar que o confere_moldes.py acha pelo destino do trecho.
"""

import lugares
import tabela
from comum import MOLDE_COM_GRADE, Entrada, entradas_do_documento, grade, itens, o_que_e

CABECALHO = ("id", "documento", "unidade", "parte")  # as colunas da tabela, na ordem
FORA = "fora"  # o documento da linha que poe o trecho fora do material


def ler(texto, nome):
    """[(numero da linha, {id, documento, unidade, parte})] da tabela, pelo tabela.py: sem as
    linhas em branco e sem os espacos das pontas de cada valor. ValueError, que diz o nome e
    a linha, quando o cabecalho nao e o da tabela ou uma linha nao tem as colunas dele."""
    return tabela.ler(texto, CABECALHO, nome)


def do_documento(documento):
    """A entrada do documento que nao lista unidades: o documento inteiro."""
    return Entrada(documento, None, None, True)


def aberturas(documento):
    """As partes de abertura do documento que recebem trechos."""
    return [a["id"] for a in documento.get("abertura", []) if a["recebe_trechos"]]


def eixos(documento, unidade=None):
    """Os ids dos eixos da grade da unidade do documento (comum.grade)."""
    return [e["id"] for e in grade(documento, unidade)]


def eixos_e_aberturas(documento, unidade=None):
    """Os eixos da grade da unidade do documento e as partes de abertura que recebem trechos."""
    return eixos(documento, unidade) + aberturas(documento)


def partes_da_entrada(entrada):
    """As partes que um lugar pode ter na entrada, num documento cujo molde tem grade: no item,
    os eixos da grade da unidade dele; na unidade com itens, as partes de abertura, porque a
    entrada dela e a da abertura; na unidade sem itens e no documento que nao lista
    unidades, os eixos da grade e as partes de abertura."""
    documento, unidade = entrada.documento, entrada.unidade
    if entrada.item is not None:
        return eixos(documento, unidade)
    if unidade is not None and itens(unidade):
        return aberturas(documento)
    return eixos_e_aberturas(documento, unidade)


def partes_da_linha(entrada):
    """As partes que uma linha pode dar para a entrada: as dela e, na unidade com itens,
    tambem os eixos da grade dela, porque a entrada desse eixo e o item que o destino do
    trecho nomeia."""
    if entrada.item is None and entrada.unidade is not None:
        return eixos_e_aberturas(entrada.documento, entrada.unidade)
    return partes_da_entrada(entrada)


def entradas_da_linha(documento, unidade, formato):
    """[Entrada] que a unidade de uma linha quer dizer no documento: com um id, as do
    comum.o_que_e que sao do documento (nenhuma, quando ele nao tem o id); sem id, cada
    entrada do documento, ou o proprio documento, quando ele nao lista unidades."""
    if unidade:
        return [e for e in o_que_e(formato, unidade) if e.documento["id"] == documento["id"]]
    return list(entradas_do_documento(documento).values()) or [do_documento(documento)]


def partes_validas(documento, unidade, formato):
    """As partes que uma linha pode dar com a unidade dela no documento, ou None quando o
    documento nao tem a unidade. Num documento sem grade, so a parte vazia. Num com grade:
    com um id, as partes que a linha pode dar para a entrada dele -- num conjunto, as que ela
    pode dar para todos os membros; sem id, as de qualquer entrada do documento, porque a
    entrada vem do destino do trecho."""
    entradas = entradas_da_linha(documento, unidade, formato)
    if not entradas:
        return None
    if documento["molde"] != MOLDE_COM_GRADE:
        return [""]
    listas = [partes_da_linha(e) for e in entradas]
    if unidade:
        return [p for p in listas[0] if all(p in outra for outra in listas[1:])]
    return list(dict.fromkeys(p for lista in listas for p in lista))


def erro_da_linha(linha, ids_dos_trechos, formato):
    """O que a linha tem que nao fecha com as analises ou com o formato, ou None."""
    documento, unidade, parte = linha["documento"], linha["unidade"], linha["parte"]
    if linha["id"] not in ids_dos_trechos:
        return f"nenhum trecho tem o id {linha['id']!r}"
    if documento == FORA:
        if unidade not in {r["id"] for r in formato["fora"]}:
            return f"posto fora por uma regra que o formato não tem: {unidade!r}"
        return f"linha de fora com a parte {parte!r}" if parte else None
    if documento not in lugares.documentos_de_conteudo(formato):
        return f"{documento!r} não é um documento de conteúdo do formato"
    validas = partes_validas(next(d for d in formato["documentos"] if d["id"] == documento), unidade, formato)
    if validas is None:
        return f"o documento {documento!r} não tem a unidade {unidade!r}"
    if parte not in validas:
        return f"o documento {documento!r} não tem a parte {parte!r}" + (f" na unidade {unidade!r}" if unidade else "")
    return None


def conferidas(linhas, ids_dos_trechos, formato):
    """(validas, erros): as linhas que fecham com as analises e com o formato, na ordem da
    tabela, e uma frase para cada uma das outras, com o numero dela: a linha que repete outra,
    o id que nenhum trecho tem, a regra de fora que o formato nao tem, o documento que nao e
    de conteudo, a unidade que o documento nao tem e a parte que a linha nao pode dar. Quando
    um documento do formato tem o nome que a tabela usa para o trecho posto fora, nenhuma
    linha vale, porque as dele e as de fora nao se distinguem."""
    if any(d["id"] == FORA for d in formato["documentos"]):
        return [], [f"o formato tem um documento {FORA!r}, o nome que a tabela dá ao lugar do trecho posto fora"]
    validas, erros, vistas = [], [], set()
    for n, linha in linhas:
        chave = tuple(linha[c] for c in CABECALHO)
        erro = "repete uma linha de antes" if chave in vistas else erro_da_linha(linha, ids_dos_trechos, formato)
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
