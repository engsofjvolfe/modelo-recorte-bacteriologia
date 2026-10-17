# SPDX-License-Identifier: GPL-3.0-or-later
# Copyright do codigo sob GPL-3.0 -- ver LICENSE e NOTICE.md na raiz do projeto.

"""
Confere os moldes do material de estudo contra as analises das aulas, com as unidades e o
limite das aulas: cada trecho das analises tem lugar num documento do formato e, dentro
dele, numa entrada e numa parte do molde; o limite tira o que nao entra no material;
nenhuma parte de molde fica sem trecho; e cada parte diz de onde vem -- os tipos, quantos
trechos e de que aulas, e se a ordem dela e dada ou proposta. Grava o relatorio da
conferencia.

O documento. Os documentos do trecho vem das fontes que o formato diz em
"documentos_vem_de" (FONTES): "regras", os das regras do formato (lugares.py), pelo grupo e
pelo caminho; "destino", os das entradas que o destino do trecho nomeia, pela tabela dos
destinos (destinos.py). A tabela da leitura (lidos.py) poe o trecho num documento que as
fontes nao dao em tres casos: o que espera o assunto; o marcado, cujos documentos sao os da
tabela quando ela tem linha dele; e o trecho de uma aula ate a ultima sem lugar -- o limite
tirou todos os lugares dele, ou as fontes nao lhe dao documento -- (o lugar novo, que nao
entra na conta do limite). Fora disso, a linha num documento que as fontes nao dao e erro.

A entrada. Uma entrada e o que recebe trechos dentro de um documento (lidos.py): uma
unidade sem itens, um item, a unidade com itens (na abertura) ou o documento que nao lista
unidades. Ela vem da linha da tabela da leitura, quando a linha diz um id; senao, ou quando
a linha diz uma unidade com itens fora da abertura, das entradas que o destino do trecho
nomeia naquele documento e naquela unidade. Um conjunto vale por cada membro, como lugar
indireto.

A parte vem do tipo de molde do documento (MOLDES): no "partes_por_tipo", a parte da
sequencia de cada tipo do trecho, e o trecho sem tipo de parte nenhuma fica junto do assunto
dele; no molde com grade (comum.MOLDE_COM_GRADE), a parte da linha da tabela da leitura; no
"formas", a forma de pergunta de cada tipo; no "colunas", o cartao.

O limite (limite.py), com as aulas ate a "ultima_aula" do formato: uma aula trata de uma
entrada quando os lugares diretos dos trechos dela ali tem pelo menos "partes_para_tratar"
partes distintas, ou quando a entrada diz as aulas que tratam ("tratada_em"); com menos, so
a menciona. Ficam o lugar de uma aula ate a ultima numa unidade com material e o de uma
aula depois da ultima numa entrada tratada. As perguntas de prova recebem o trecho de uma
aula ate a ultima na aula dele, e o de depois nas aulas que tratam das entradas em que ele
ficou; os cartoes, todo trecho que fica.

FALTA e o que espera uma leitura ou uma decisao: o pedaco do destino sem linha na tabela
dos destinos; o trecho sem entrada num documento que lista unidades; o trecho sem eixo numa
ficha; o trecho marcado de uma aula ate a ultima sem documento; e o trecho de uma aula ate
a ultima sem lugar depois do limite. ERRO e o que se contradiz: a linha da tabela que nao
fecha com as analises ou com o formato; o id da tabela dos destinos que nao e unidade, item
nem conjunto do formato; a parte que nao e da entrada; o lugar novo numa entrada sem
material; o trecho de estudo sem documento de conteudo e sem lugar novo; o grupo ou o tipo
que o formato nao tem; o tipo sem forma de pergunta; a parte de molde sem trecho; o trecho
de fora com lugar. Cada um sai na tela e no fim do relatorio, que e gravado assim mesmo.

O relatorio mostra tambem, em cada documento que lista unidades, as aulas que tratam de cada
unidade e de cada item (com as partes), as que so mencionam e quantos trechos de depois da
ultima aula ficam ali, e os conjuntos; as unidades so mencionadas; onde as fontes do
documento discordam; os pedacos do destino sem linha na tabela dos destinos; e os trechos
ate a ultima aula sem lugar depois do limite, com os lugares que perderam.

Os caminhos vem do projeto.json: "formato", "forma_analise", "analises_das_aulas",
"lugares_lidos", "destinos" e "conferencia_moldes". O formato e lido pela leitura dele
(comum.le_formato); a forma das analises, pela leitura de todo arquivo de dados
(validar_dados.le_dados), contra o molde dela; as analises, pelo analises.py, com as regras
do formato conferidas contra a forma. Com erro numa entrada -- arquivo que falta, que nao
se le ou fora do molde, regra que nao combina com a forma, tipo de molde ou fonte que este
script nao conhece, tabela dos destinos que se contradiz, destino que nao esta em pedacos,
limite que se contradiz (a ultima aula que nao e a de nenhuma analise; a decisao com aula
que nao e de analise nenhuma, que vem depois da ultima ou que nao tem trecho na entrada) --,
cada erro sai numa linha ERRO e nada e gravado.

Uso (de qualquer pasta dentro do projeto):
    python scripts/confere_moldes.py
    python scripts/confere_moldes.py --projeto projeto.json
Sai com codigo 1 quando ha ERRO ou FALTA.
"""

import argparse
import collections
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import destinos  # noqa: E402
import lidos  # noqa: E402
import limite  # noqa: E402
import lugares  # noqa: E402
from analises import unicos  # noqa: E402
from comum import (MOLDE_COM_GRADE, acha_projeto, conjuntos, entradas_do_documento, grade,  # noqa: E402
                   ids_do_documento, itens, le_formato, o_que_e, onde, unidades)
from relatorio import por_chave, tabela, tabela_das_classes  # noqa: E402
from validar_dados import esquema, le_dados, le_texto  # noqa: E402

ENTRADAS = ("formato", "forma_analise", "lugares_lidos", "destinos")  # os arquivos que o script le, pelo projeto.json
ERRO, FALTA = "ERRO", "FALTA"  # o que abre a linha do que se contradiz e a do que espera uma leitura ou decisao
JUNTO = None  # a parte do trecho que vai junto do assunto dele, fora das partes da sequencia
NENHUM = "—"  # o que o relatorio mostra no lugar de uma lista vazia
ENTRADA = "entrada"  # o que falta ao trecho num documento que lista unidades, quando nem a linha nem o destino a dao
SEM_LUGAR = "sem lugar nos documentos em que cai"  # a classe do trecho de estudo que nao tem lugar nenhum
Posto = collections.namedtuple("Posto", "documento entrada parte")  # um lugar do trecho: documento, Entrada, parte
Falta = collections.namedtuple("Falta", "coisa documento")  # o que falta ao trecho e em que documento
NENHUM_DOCUMENTO = Falta(None, None)  # o que falta ao trecho de estudo que nao cai em documento de conteudo
Fonte = collections.namedtuple("Fonte", "documentos sozinha")
# uma fonte dos documentos do trecho: documentos(trecho, c) -> ids dos documentos de conteudo que ela da, na ordem
# do formato; sozinha, o titulo da lista dos documentos que so ela da


class Conferencia:
    """O que a conferencia acha. Antes do limite: o que o destino de cada trecho nomeia
    (nomeadas: {id: [Entrada]}); os postos de cada trecho que tem algum ({id: [Posto]}); os
    documentos de cada trecho em que so a tabela da leitura o poe (pendentes: {id:
    [documento]}); a classe de cada trecho de uma aula ate a ultima a que as fontes nao dao
    documento e a tabela da leitura da o lugar novo (sem_fonte: {id: classe}); onde as fontes
    discordam (discordam: {fonte: {documento: ids}}); e os pedacos do destino sem linha na
    tabela dos destinos (faltam: {pedaco: ids}). Depois do
    limite (limite.Limite): os trechos de cada lugar de cada documento, no material (cheio:
    {documento: {(entrada, parte): ids}}, a entrada pelo id dela -- vazio no documento que
    nao lista unidades, e a aula nas perguntas de prova); os tipos dos trechos postos em cada
    documento de conteudo (tipos: {documento: {tipo: ids}}); e os postos que cada trecho de
    uma aula ate a ultima perdeu sem ganhar outro (perdidos: {id: [Posto]}). E a classe de
    cada trecho, a aula de cada um e os avisos, (ERRO ou FALTA, id do trecho ou "", o que
    houve), na ordem em que se acham."""

    def __init__(self, formato, aulas):
        self.formato = formato
        self.documentos = {d["id"]: d for d in formato["documentos"]}
        self.de_conteudo = lugares.documentos_de_conteudo(formato)
        self.todos = [d["id"] for d in formato["documentos"] if d.get("todos")]
        self.tipos_com_lugar = ({t for p in formato["partes_por_tipo"] for t in p["tipos"]}
                                | set(formato["tipos_junto"]))
        self.aulas = aulas
        self.ate_a_ultima = set(aulas[:aulas.index(formato["ultima_aula"]) + 1])
        entradas = entradas_do_formato(formato)
        self.unidade_de = {chave(e): chave(e._replace(item=None)) for e in entradas if e.item is not None}
        self.decisoes = {chave(e): coisa(e)["tratada_em"] for e in entradas if "tratada_em" in coisa(e)}
        self.nomeadas, self.postos, self.pendentes, self.sem_fonte, self.faltam = {}, {}, {}, {}, {}
        self.discordam = {nome: collections.defaultdict(list) for nome in FONTES}
        self.limite, self.ficam = None, set()
        self.classes = collections.Counter()
        self.cheio = collections.defaultdict(lambda: collections.defaultdict(set))
        self.tipos = collections.defaultdict(lambda: collections.defaultdict(set))
        self.perdidos = {}
        self.aula_de = {}
        self.avisos = []

    def avisa(self, tipo, trecho, mensagem):
        self.avisos.append((tipo, trecho["id"] if trecho else "", mensagem))


# ---------- as entradas ----------

def coisa(entrada):
    """A unidade ou o item da entrada; None, no documento que nao lista unidades."""
    return entrada.item or entrada.unidade


def chave(entrada):
    """A chave de uma entrada: (id do documento, id do item ou da unidade; vazio, no documento
    que nao lista unidades)."""
    return entrada.documento["id"], coisa(entrada)["id"] if coisa(entrada) else ""


def entradas_do_formato(formato):
    """[Entrada] de cada unidade e de cada item do formato, na ordem dele."""
    return [e for d in formato["documentos"] for e in entradas_do_documento(d).values()]


def sem_repetir(entradas):
    """As entradas sem repetir, na ordem em que vem; a que vem como lugar direto e como
    indireto fica direta."""
    saida = {}
    for e in entradas:
        k = chave(e)
        saida[k] = e._replace(direto=e.direto or saida[k].direto) if k in saida else e
    return list(saida.values())


def postos_sem_repetir(postos):
    """Os postos sem repetir o documento, a entrada e a parte, na ordem em que vem; o direto
    fica."""
    saida = {}
    for p in postos:
        k = (p.documento, chave(p.entrada), p.parte)
        saida[k] = p._replace(entrada=sem_repetir([saida[k].entrada, p.entrada])[0]) if k in saida else p
    return list(saida.values())


def nome_da_entrada(entrada):
    """O nome de uma entrada no relatorio: o da unidade, com o do item depois; o do documento,
    no documento que nao lista unidades."""
    if entrada.item is not None:
        return f"{entrada.unidade['nome']} › {entrada.item['nome']}"
    return (entrada.unidade or entrada.documento)["nome"]


def quem(entrada):
    """O lugar de uma entrada numa frase de aviso."""
    return onde(entrada.documento, entrada.unidade, entrada.item)


def ids_da_unidade(unidade):
    """O id da unidade e os dos itens dela: as entradas em que ficam os trechos dela."""
    return {unidade["id"]} | {i["id"] for i in itens(unidade)}


def entradas_do_lugar(trecho, d, unidade, parte, c):
    """[Entrada] de um lugar do trecho no documento d, com a unidade da linha da tabela da
    leitura (vazia, sem linha ou sem id) e a parte: as que o id da linha quer dizer; sem id,
    as que o destino do trecho nomeia no documento, ou o proprio documento, quando ele nao
    lista unidades. A unidade com itens, fora da abertura, da os itens dela que o destino
    nomeia."""
    documento = c.documentos[d]
    no_documento = [e for e in c.nomeadas.get(trecho["id"], []) if e.documento["id"] == d]
    if unidade:
        base = lidos.entradas_da_linha(documento, unidade, c.formato)
    else:
        base = no_documento if unidades(documento) else [lidos.do_documento(documento)]
    saida = []
    for e in base:
        if e.item is None and e.unidade is not None and itens(e.unidade) and parte not in lidos.aberturas(documento):
            dela = ids_da_unidade(e.unidade)
            saida += [n._replace(direto=n.direto and e.direto) for n in no_documento
                      if n.item is not None and n.item["id"] in dela]
        else:
            saida.append(e)
    return sem_repetir(saida)


# ---------- as fontes dos documentos do trecho ----------

def pelas_regras(trecho, c):
    """Os documentos de conteudo em que as regras do formato poem o trecho: pelo grupo e pelo
    caminho."""
    caidos = lugares.documentos(trecho, c.formato)
    return [d for d in c.de_conteudo if d in caidos]


def pelo_destino(trecho, c):
    """Os documentos de conteudo das entradas que o destino do trecho nomeia."""
    nomeados = {e.documento["id"] for e in c.nomeadas.get(trecho["id"], [])}
    return [d for d in c.de_conteudo if d in nomeados]


FONTES = {  # as fontes que o formato pode dizer em documentos_vem_de (formato.schema.json)
    "regras": Fonte(pelas_regras,
                    "as regras (o grupo e o caminho) põem o trecho no documento, e o destino não o nomeia"),
    "destino": Fonte(pelo_destino, "o destino nomeia o documento, e as regras não põem o trecho nele"),
}


def documentos_das_fontes(trecho, c):
    """Os documentos de conteudo do trecho pelas fontes que o formato diz, na ordem do formato;
    guarda em c os que uma fonte da e as outras nao."""
    por_fonte = {nome: fonte.documentos(trecho, c) for nome, fonte in FONTES.items()}
    for nome, seus in por_fonte.items():
        dos_outros = {d for outro, docs in por_fonte.items() if outro != nome for d in docs}
        for d in seus:
            if d not in dos_outros:
                c.discordam[nome][d].append(trecho["id"])
    usados = {d for nome in c.formato["documentos_vem_de"] for d in por_fonte[nome]}
    return [d for d in c.de_conteudo if d in usados]


# ---------- a parte de cada tipo de molde: ([parte], erros) ----------

def pelo_tipo(trecho, documento, linha, formato):
    """A parte da sequencia de cada tipo do trecho; JUNTO, quando nenhum tipo dele tem parte."""
    tipos = set(lugares.valor(trecho, "tipo"))
    return [p["id"] for p in formato["partes_por_tipo"] if tipos & set(p["tipos"])] or [JUNTO], []


def pela_tabela(trecho, documento, linha, formato):
    """A parte da linha da tabela da leitura do trecho no documento; nenhuma, sem linha."""
    return ([linha["parte"]] if linha else []), []


def pela_forma(trecho, documento, linha, formato):
    """O numero de cada forma de pergunta com um tipo do trecho; o tipo dele sem forma e erro."""
    tipos, formas = lugares.valor(trecho, "tipo"), list(enumerate(documento["formas"], 1))
    achados = [n for n, f in formas if set(tipos) & set(f["tipos"])]
    return achados, [f"tipo sem forma de pergunta em {documento['id']}: {t}"
                     for t in tipos if not any(t in f["tipos"] for _, f in formas)]


def no_cartao(trecho, documento, linha, formato):
    """O cartao do trecho, uma parte so."""
    return [""], []


# ---------- as partes de molde sem trecho: erros ----------

def trechos_em(cheio, partes=None, entradas=None):
    """Os ids dos trechos dos lugares de 'cheio' que estao nas partes e nas entradas dadas (em
    todas, sem elas)."""
    return set().union(*(ids for (e, p), ids in cheio.items()
                         if (partes is None or p in partes) and (entradas is None or e in entradas)))


def da_grade_do_documento(documento):
    """As entradas que usam a grade do proprio documento: a vazia, quando ele nao lista
    unidades, e as unidades sem eixos proprios, com os itens delas."""
    return {""}.union(*(ids_da_unidade(u) for u in unidades(documento) if not u.get("eixos")))


def sem_vazias(documento, cheio):
    """Nenhuma: o molde so tem as partes que os trechos dao."""
    return []


def vazias_da_grade(documento, cheio):
    """O eixo da grade do documento que nenhuma entrada que a usa preenche; o elo sem eixo com
    trecho; o eixo da grade de uma unidade com a sua, quando ela tem trechos no material; a
    abertura que recebe trechos e nao tem nenhum."""
    usam = da_grade_do_documento(documento)
    erros = [f"{onde(documento)}: o eixo {e['id']!r} não tem trecho"
             for e in documento.get("eixos", []) if not trechos_em(cheio, {e["id"]}, usam)]
    erros += [f"{onde(documento)}: o elo {elo['id']!r} não tem eixo com trecho"
              for elo in documento.get("elos", []) if not trechos_em(cheio, set(elo["eixos"]), usam)]
    for u in unidades(documento):
        suas = ids_da_unidade(u)
        if u.get("eixos") and trechos_em(cheio, None, suas):
            erros += [f"{onde(documento, u)}: o eixo {e['id']!r} não tem trecho"
                      for e in u["eixos"] if not trechos_em(cheio, {e["id"]}, suas)]
    return erros + [f"{onde(documento)}: a abertura {a['id']!r} não tem trecho"
                    for a in documento.get("abertura", []) if a["recebe_trechos"] and not trechos_em(cheio, {a["id"]})]


def vazias_das_formas(documento, cheio):
    """As formas de pergunta sem trecho."""
    return [f"{onde(documento)}: a forma de pergunta {n} ({f['verbo']}) não tem trecho"
            for n, f in enumerate(documento["formas"], 1) if not trechos_em(cheio, {n})]


# ---------- a secao de cada tipo de molde no relatorio: linhas ----------

def aulas(ids, aula_de):
    """As aulas dos trechos, em ordem natural."""
    return ", ".join(a for a, _ in por_chave(collections.Counter(aula_de[i] for i in ids)))


def secao_partes(documento, formato, cheio, aula_de):
    """Cada parte da sequencia com trechos: os tipos, quantos trechos, de que aulas e a ordem;
    quantos trechos ficam junto do assunto; e as partes de cada caso, se o documento tem."""
    linhas = []
    for p in formato["partes_por_tipo"]:
        ids = trechos_em(cheio, {p["id"]})
        if ids:
            linhas.append((p["nome"], "; ".join(p["tipos"]), len(ids), aulas(ids, aula_de), p["ordem"]))
    saida = tabela(["Parte", "Tipos", "Trechos", "Aulas", "Ordem"], linhas, numericas=(2,)) + [""]
    junto = trechos_em(cheio, {JUNTO})
    if junto:
        saida += [f"{len(junto)} trechos só de tipos que se ensinam junto de outro trecho "
                  f"({', '.join(formato['tipos_junto'])}): ficam junto do assunto deles.", ""]
    if documento.get("casos"):
        saida += [f"Cada caso, depois dos fatos de cada {documento['unidade']}:", ""]
        saida += tabela(["Parte do caso", "Ordem"], [(c["nome"], c["ordem"]) for c in documento["casos"]]) + [""]
    return saida


def secao_eixos(documento, formato, cheio, aula_de):
    """Cada abertura; a grade do documento, com quantos trechos cada eixo tem nas entradas que
    a usam, e os elos; e a grade de cada unidade com a sua, com os trechos dela e dos itens."""
    lista, usam, saida = unidades(documento), da_grade_do_documento(documento), []
    for a in documento.get("abertura", []):
        if not a["recebe_trechos"]:
            saida += [f"Abertura: {a['nome']} ({a['ordem']}).", ""]
            continue
        por_unidade = ", ".join(f"{u['id']} {len(trechos_em(cheio, {a['id']}, {u['id']}))}" for u in lista)
        saida += [f"Abertura de cada {documento['unidade']}: {a['nome']} ({a['ordem']}); "
                  f"{len(trechos_em(cheio, {a['id']}))} trechos" + (f" ({por_unidade})" if por_unidade else "") + ".",
                  ""]
    if documento.get("eixos"):
        linhas = [(e["nome"], len(trechos_em(cheio, {e["id"]}, usam)), e["ordem"]) for e in documento["eixos"]]
        saida += tabela(["Eixo", "Trechos", "Ordem"], linhas, numericas=(1,)) + [""]
    if documento.get("elos"):
        nomes = {e["id"]: e["nome"] for e in documento["eixos"]}
        linhas = [(f"{elo['id']}. {elo['nome']}", "; ".join(nomes[e] for e in elo["eixos"]),
                   len(trechos_em(cheio, set(elo["eixos"]), usam)), elo["ordem"]) for elo in documento["elos"]]
        saida += ["Elos:", ""] + tabela(["Elo", "Eixos que o alimentam", "Trechos desses eixos", "Ordem"], linhas,
                                        numericas=(2,)) + [""]
    for u in lista:
        if u.get("eixos"):
            suas = ids_da_unidade(u)
            linhas = [(e["nome"], len(trechos_em(cheio, {e["id"]}, suas)), e["ordem"]) for e in u["eixos"]]
            saida += [f"### {u['nome']} ({len(trechos_em(cheio, None, suas))} trechos)", ""]
            saida += tabela(["Eixo", "Trechos", "Ordem"], linhas, numericas=(1,)) + [""]
    return saida


def secao_perguntas(documento, formato, cheio, aula_de):
    """As partes de cada pergunta; cada forma de pergunta, com os tipos, quantos trechos e a
    ordem; e quantos trechos em cada entrada do documento (nas perguntas de prova, a aula)."""
    saida = ["Cada pergunta: " + "; ".join(f"{p['nome']} ({p['ordem']})" for p in documento["pergunta"]) + ".", ""]
    linhas = [(f["verbo"], "; ".join(f["tipos"]), len(trechos_em(cheio, {n})), f["ordem"])
              for n, f in enumerate(documento["formas"], 1)]
    saida += tabela(["Forma", "Tipos", "Trechos", "Ordem"], linhas, numericas=(2,)) + [""]
    por_entrada = collections.Counter({e: len(trechos_em(cheio, None, {e})) for e, _ in cheio})
    return saida + [f"Trechos por {documento['unidade']}: "
                    + ("; ".join(f"{e} {n}" for e, n in por_chave(por_entrada)) or NENHUM) + ".", ""]


def secao_cartoes(documento, formato, cheio, aula_de):
    """Quantos trechos viram cartao, e as colunas do cartao, com o lado e a ordem."""
    linhas = [(c["id"], c["lado"], c["ordem"]) for c in documento["colunas"]]
    return [f"{len(trechos_em(cheio))} trechos viram cartão.", ""] + tabela(["Coluna", "Lado", "Ordem"], linhas) + [""]


Molde = collections.namedtuple("Molde", "partes falta por_aula vazias secao")
# o que o script faz com cada tipo de molde de documento (esquemas/formato.schema.json): partes(trecho, documento,
# linha da tabela da leitura do trecho no documento ou None, formato) -> ([parte], erros); falta, o nome do que falta
# quando partes nao da nenhuma (None, quando o molde sempre da uma ou os erros dizem por que); por_aula, se a entrada
# do lugar, num documento que recebe todos os trechos, e a aula das perguntas de prova do trecho; vazias(documento,
# cheio) -> erros; secao(documento, formato, cheio, aula de cada trecho) -> linhas
MOLDES = {
    "partes_por_tipo": Molde(pelo_tipo, None, False, sem_vazias, secao_partes),
    MOLDE_COM_GRADE: Molde(pela_tabela, "eixo", False, vazias_da_grade, secao_eixos),
    "formas": Molde(pela_forma, None, True, vazias_das_formas, secao_perguntas),
    "colunas": Molde(no_cartao, None, False, sem_vazias, secao_cartoes),
}


# ---------- o lugar de cada trecho, antes do limite ----------

def texto_da_falta(falta):
    """A frase do que falta ao trecho: o que falta e em que documento, ou que ele nao cai em
    documento de conteudo."""
    return f"sem {falta.coisa} em {falta.documento}" if falta != NENHUM_DOCUMENTO else lugares.SEM_DOCUMENTO


def partes_do_molde(trecho, documento, linha, c):
    """As partes do trecho no documento, pelo molde dele, com a linha da tabela da leitura (ou
    None); cada erro que o molde acha vai para c."""
    partes, erros = MOLDES[documento["molde"]].partes(trecho, documento, linha, c.formato)
    for e in erros:
        c.avisa(ERRO, trecho, e)
    return partes


def postos_em(trecho, d, linhas, c):
    """([Posto], [Falta]) do trecho no documento de conteudo d: para cada linha da tabela da
    leitura do trecho em d (ou sem linha), as partes que o molde do documento da e as entradas
    de cada parte, com os erros que o molde e as partes acham em c. Falta o que o molde pede
    da linha (o eixo), ou a entrada."""
    documento = c.documentos[d]
    molde = MOLDES[documento["molde"]]
    postos, faltas = [], []
    for linha in [linha for linha in linhas if linha["documento"] == d] or [None]:
        partes = partes_do_molde(trecho, documento, linha, c)
        if molde.falta and not partes:
            faltas.append(Falta(molde.falta, d))
        for parte in partes:
            entradas = entradas_do_lugar(trecho, d, linha["unidade"] if linha else "", parte, c)
            if not entradas:
                faltas.append(Falta(ENTRADA, d))
            for e in entradas:
                if documento["molde"] == MOLDE_COM_GRADE and parte not in lidos.partes_da_entrada(e):
                    c.avisa(ERRO, trecho, f"{quem(e)}: a parte {parte!r} não é dessa entrada")
                else:
                    postos.append(Posto(d, e, parte))
    return postos_sem_repetir(postos), unicos(faltas)


def avisa_o_que_falta(trecho, faltas, marcas, c):
    """Os avisos do que falta ao trecho: no marcado, FALTA que diz as marcas dele -- nada, sem
    documento, numa aula depois da ultima, porque ele fica fora do material; no outro, ERRO
    sem documento de conteudo e FALTA no resto."""
    nomes = ", ".join(m["nome"] for m in c.formato["marcas"] if m["id"] in marcas)
    for falta in faltas:
        if marcas and not (falta == NENHUM_DOCUMENTO and trecho["aula"] not in c.ate_a_ultima):
            c.avisa(FALTA, trecho, f"marcado ({nomes}), {texto_da_falta(falta)}")
        elif not marcas:
            c.avisa(ERRO if falta == NENHUM_DOCUMENTO else FALTA, trecho, texto_da_falta(falta))


def classe_sem_posto(trecho, documentos, faltas, marcas, c):
    """A classe do trecho de estudo sem posto nenhum: o marcado fica a espera de lugar, ou fora
    do material, numa aula depois da ultima e sem documento; o sem documento, a espera do
    assunto; o que espera a entrada, a espera de unidade; o resto, sem lugar."""
    if marcas:
        return ("depois",) if not documentos and trecho["aula"] not in c.ate_a_ultima else ("marca", marcas[0])
    if not documentos:
        return ("assunto",)
    return ("unidade",) if any(f.coisa == ENTRADA for f in faltas) else ("problema", SEM_LUGAR)


def com_erro(trecho, classe, c):
    """A classe do trecho com problema, com o ERRO que diz o problema dela em c."""
    c.avisa(ERRO, trecho, classe[1])
    return classe


def antes_do_limite(trecho, linhas, c):
    """Acha os postos do trecho antes do limite e os guarda em c; devolve a classe dele quando
    ela ja se sabe -- de fora, posto fora pela leitura, com problema ou sem posto nenhum --, ou
    None, quando ela se sabe depois do limite. Os documentos sao os das fontes; os da tabela da
    leitura, no marcado que tem linha nela e no que espera o assunto. No trecho de uma aula ate
    a ultima a que as fontes nao dao documento, sem marca e sem o grupo que espera o assunto,
    os documentos da tabela sao o do lugar novo, que se acha depois do limite; sem linha na
    tabela, ou numa aula depois da ultima, ele e erro."""
    classe = lugares.classe(trecho, c.formato)
    fora = [linha for linha in linhas if linha["documento"] == lidos.FORA]
    if classe[0] == "problema":
        return com_erro(trecho, classe, c)
    if fora:
        if len(fora) < len(linhas):
            c.avisa(ERRO, trecho, "posto fora pela leitura e com lugar na tabela dela ao mesmo tempo")
        return ("lido", fora[0]["unidade"])
    if classe[0] == "fora":
        if linhas:
            c.avisa(ERRO, trecho, "trecho de fora com lugar na tabela da leitura")
        return classe
    for g in lugares.grupos_desconhecidos(trecho, c.formato):
        c.avisa(ERRO, trecho, f"grupo desconhecido {g!r}")
    sem_parte = [t for t in lugares.valor(trecho, "tipo") if t not in c.tipos_com_lugar]
    if sem_parte:
        c.avisa(ERRO, trecho, f"tipo sem lugar no molde: {', '.join(sem_parte)}")
    das_fontes, marcas = documentos_das_fontes(trecho, c), lugares.marcas(trecho, c.formato)
    na_tabela = unicos(linha["documento"] for linha in linhas)
    if das_fontes and not (marcas and na_tabela):
        documentos = das_fontes
        c.pendentes[trecho["id"]] = [d for d in na_tabela if d not in das_fontes]
    else:
        sem = lugares.sem_documento(trecho, c.formato)
        if not das_fontes and sem[0] == "problema":
            if not (na_tabela and trecho["aula"] in c.ate_a_ultima):
                return com_erro(trecho, sem, c)
            c.pendentes[trecho["id"]], c.sem_fonte[trecho["id"]] = na_tabela, sem
            return None
        documentos = na_tabela
    postos, faltas = [], ([] if documentos else [NENHUM_DOCUMENTO])
    for d in documentos:
        achados, falta = postos_em(trecho, d, linhas, c)
        postos += achados
        faltas += falta
    avisa_o_que_falta(trecho, faltas, marcas, c)
    if postos:
        c.postos[trecho["id"]] = postos
        return None
    return classe_sem_posto(trecho, documentos, faltas, marcas, c)


# ---------- o limite e o material ----------

def lugares_do_limite(c):
    """Os postos de cada trecho, antes do limite, como o limite.py os recebe."""
    return [limite.Lugar(i, c.aula_de[i], chave(p.entrada), p.parte, p.entrada.direto)
            for i, postos in c.postos.items() for p in postos]


def lugares_novos(trecho, pendentes, linhas, c):
    """Os postos novos do trecho, nas linhas da tabela da leitura dele nos documentos em que
    so ela o poe, fora da conta do limite: ficam os que estao numa unidade com material; o
    outro e erro."""
    novos, faltas = [], []
    for d in pendentes:
        achados, falta = postos_em(trecho, d, linhas, c)
        faltas += falta
        for p in achados:
            k = chave(p.entrada)
            if c.unidade_de.get(k, k) in c.limite.com_material:
                novos.append(p)
            else:
                c.avisa(ERRO, trecho, f"{quem(p.entrada)}: lugar novo numa entrada que não tem material")
    avisa_o_que_falta(trecho, faltas, lugares.marcas(trecho, c.formato), c)
    return novos


def guarda(trecho, postos, c):
    """Poe o trecho no material: nos postos dele, com os tipos dele; e em cada documento que
    recebe todos os trechos, pelo molde dele -- nas perguntas de prova, na aula do trecho,
    quando ela vai ate a ultima, ou nas aulas que tratam das entradas em que ele ficou."""
    for p in postos_sem_repetir(postos):
        c.cheio[p.documento][(chave(p.entrada)[1], p.parte)].add(trecho["id"])
        for tipo in lugares.valor(trecho, "tipo"):
            c.tipos[p.documento][tipo].add(trecho["id"])
    das_perguntas = ([trecho["aula"]] if trecho["aula"] in c.ate_a_ultima
                     else c.limite.perguntas.get(trecho["id"], []))
    for d in c.todos:
        documento = c.documentos[d]
        molde = MOLDES[documento["molde"]]
        partes = partes_do_molde(trecho, documento, None, c)
        if molde.falta and not partes:
            c.avisa(ERRO, trecho, texto_da_falta(Falta(molde.falta, d)))
        for entrada in (das_perguntas if molde.por_aula else [""]):
            for parte in partes:
                c.cheio[d][(entrada, parte)].add(trecho["id"])


def depois_do_limite(trecho, linhas, c):
    """Poe no material os postos do trecho que ficam depois do limite e, no trecho de uma aula
    ate a ultima sem lugar -- o limite tirou todos os postos dele, ou as fontes nao lhe dao
    documento --, os lugares novos; devolve a classe do trecho que tinha postos ou esperava o
    lugar novo, ou None. A linha num documento em que so a tabela da leitura poe o trecho, fora
    desse caso, e erro; o trecho a que as fontes nao dao documento e que nao fica no lugar novo
    tambem."""
    i = trecho["id"]
    pendentes = c.pendentes.get(i, [])
    postos = [p for p in c.postos.get(i, []) if (i, chave(p.entrada), p.parte) in c.ficam]
    if not postos and (i in c.limite.sem_lugar_ate or i in c.sem_fonte) and pendentes:
        postos = lugares_novos(trecho, pendentes, linhas, c)
    else:
        for d in pendentes:
            c.avisa(ERRO, trecho, f"lugar na tabela da leitura em {d}, documento em que o trecho não cai")
    if postos:
        guarda(trecho, postos, c)
        return ("estudo",)
    if i in c.sem_fonte:
        return com_erro(trecho, c.sem_fonte[i], c)
    if i not in c.postos:
        return None
    if i in c.limite.sem_lugar_ate:
        c.perdidos[i] = c.postos[i]
        c.avisa(FALTA, trecho, "sem lugar depois do limite: espera um lugar novo")
        return ("limite",)
    return ("depois",)


def colocar(trechos, linhas, nomeia, c):
    """Poe cada trecho no lugar dele, aplica o limite e acha as partes de molde sem trecho;
    tudo vai para c. limite.ErroDeLimite quando o limite se contradiz, e
    destinos.ErroDeDestinos quando o destino nao esta em pedacos."""
    da_tabela = lidos.por_trecho(linhas)
    considerados = [t for t in trechos if lugares.classe(t, c.formato)[0] != "fora"
                    and not any(linha["documento"] == lidos.FORA for linha in da_tabela.get(t["id"], []))]
    ids, c.faltam = destinos.ids_dos_trechos(considerados, nomeia)
    c.nomeadas = {i: sem_repetir([e for nomeado in seus for e in o_que_e(c.formato, nomeado)])
                  for i, seus in ids.items()}
    for pedaco in c.faltam:
        c.avisa(FALTA, None, f"destino sem linha na tabela dos destinos: {pedaco!r}")
    for trecho in trechos:
        c.aula_de[trecho["id"]] = trecho["aula"]
        classe = antes_do_limite(trecho, da_tabela.get(trecho["id"], []), c)
        if classe:
            c.classes[classe] += 1
    f = c.formato
    c.limite = limite.aplicar(lugares_do_limite(c), c.unidade_de, c.aulas, f["ultima_aula"], f["partes_para_tratar"],
                              c.decisoes)
    c.ficam = {(lugar.trecho, lugar.entrada, lugar.parte) for lugar in c.limite.ficam}
    for trecho in trechos:
        classe = depois_do_limite(trecho, da_tabela.get(trecho["id"], []), c)
        if classe:
            c.classes[classe] += 1
    for d in f["documentos"]:
        for e in MOLDES[d["molde"]].vazias(d, c.cheio[d["id"]]):
            c.avisa(ERRO, None, e)


# ---------- o relatorio ----------

def linhas_dos_avisos(avisos):
    return [f"{tipo}: {f'{i}: ' if i else ''}{mensagem}" for tipo, i, mensagem in avisos]


def tabela_ou_nada(cabecalho, linhas, nada, numericas=()):
    """A tabela das linhas, ou a frase 'nada', quando nao ha linha."""
    return (tabela(cabecalho, linhas, numericas) if linhas else [nada]) + [""]


def secao_onde(formato, tipos):
    """Para cada tipo de onde_se_ensina, os documentos onde ele se ensina e os outros em que
    trechos dele caem, com quantos."""
    nomes = {d["id"]: d["nome"] for d in formato["documentos"]}
    linhas = [(tipo, "; ".join(nomes[d] for d in docs),
               "; ".join(f"{nomes[d]} {len(tipos[d][tipo])}" for d in nomes if d not in docs and tipos[d].get(tipo))
               or NENHUM)
              for tipo, docs in formato["onde_se_ensina"].items()]
    return tabela(["Tipo", "Se ensina em", "Também cai em (trechos)"], linhas) + [""]


def nomes_das_partes(entrada, formato):
    """{parte: nome} das partes que um lugar na entrada pode ter, na ordem do molde: num
    documento com grade, as aberturas e os eixos da grade da unidade; nos outros, as partes da
    sequencia e a do trecho que vai junto do assunto."""
    documento = entrada.documento
    if documento["molde"] == MOLDE_COM_GRADE:
        return {x["id"]: x["nome"] for x in documento.get("abertura", []) + grade(documento, entrada.unidade)}
    return {**{p["id"]: p["nome"] for p in formato["partes_por_tipo"]}, JUNTO: "junto do assunto"}


def tratam(entrada, c):
    """As aulas que tratam da entrada, cada uma com as partes dos lugares diretos dela ali, na
    ordem do molde; a frase diz quando quem decide e o formato."""
    k, nomes = chave(entrada), nomes_das_partes(entrada, c.formato)
    ordem = list(nomes)

    def com_partes(aula):
        suas = sorted(c.limite.partes.get(k, {}).get(aula, []),
                      key=lambda p: ordem.index(p) if p in ordem else len(ordem))
        return f"{aula} ({'; '.join(nomes.get(p, str(p)) for p in suas)})" if suas else aula
    textos = [com_partes(a) for a in c.limite.tratam.get(k, [])]
    return ("decisão do formato: " if k in c.decisoes else "") + (", ".join(textos) or NENHUM)


def secao_das_unidades(c):
    """Em cada documento que lista unidades, cada unidade e cada item, com as aulas que tratam
    dele (e as partes), as que so o mencionam e quantos trechos de depois da ultima aula ficam
    nele; e os conjuntos do documento, com os membros."""
    f = c.formato
    saida = [f"## O que cada aula trata e só menciona (a última aula é a {f['ultima_aula']})", "",
             f"Uma aula trata de uma unidade, ou de um item, quando os trechos dela ali ocupam pelo menos "
             f"{f['partes_para_tratar']} partes do molde, ou quando o formato decide que ela trata; com menos, só a "
             "menciona. Da unidade com itens tratam as aulas que tratam de algum item dela.", ""]
    de_depois = collections.defaultdict(set)
    for lugar in c.limite.ficam:
        if lugar.aula not in c.ate_a_ultima:
            de_depois[lugar.entrada].add(lugar.trecho)
    for d in f["documentos"]:
        if not unidades(d):
            continue
        entradas = list(entradas_do_documento(d).values())
        linhas = [(nome_da_entrada(e), tratam(e, c), ", ".join(c.limite.mencionam.get(chave(e), [])) or NENHUM,
                   len(de_depois[chave(e)])) for e in entradas]
        cabecalho = [d["unidade"].capitalize(), "Tratam (partes)", "Só mencionam", "Trechos de depois da última aula"]
        saida += [f"### {d['nome']}", ""] + tabela(cabecalho, linhas, numericas=(3,)) + [""]
        nomes = {coisa(e)["id"]: nome_da_entrada(e) for e in entradas}
        saida += tabela_ou_nada(["Conjunto", "Membros"],
                                [(cj["nome"], "; ".join(nomes[m] for m in cj["membros"])) for cj in conjuntos(d)],
                                "Nenhum conjunto.")
    return saida


def secao_so_mencionadas(c):
    """As unidades sem material de que alguma aula ate a ultima fala: as aulas so as
    mencionam."""
    tratadas, linhas = set(c.limite.tratadas), []
    for e in entradas_do_formato(c.formato):
        mencionam = c.limite.mencionam.get(chave(e), [])
        if e.item is None and chave(e) not in tratadas and c.ate_a_ultima & set(mencionam):
            linhas.append((e.documento["nome"], nome_da_entrada(e), ", ".join(mencionam)))
    return ["## Unidades só mencionadas", ""] + tabela_ou_nada(
        ["Documento", "Unidade", "Aulas que a mencionam"], linhas, "Nenhuma.")


def secao_das_fontes(c):
    """Para cada fonte dos documentos, pelo nome dela no formato, os documentos que so ela da:
    quantos trechos, de que aulas e o primeiro."""
    saida = ["## Onde as fontes do documento discordam", ""]
    for nome, fonte in FONTES.items():
        so_dela = c.discordam[nome]
        linhas = [(c.documentos[d]["nome"], len(so_dela[d]), aulas(so_dela[d], c.aula_de), so_dela[d][0])
                  for d in c.de_conteudo if so_dela.get(d)]
        saida += [f"Só a fonte {nome!r} dá o documento: {fonte.sozinha}.", ""] + tabela_ou_nada(
            ["Documento", "Trechos", "Aulas", "Primeiro trecho"], linhas, "Nenhum.", numericas=(1,))
    return saida


def secao_sem_linha(c):
    """Cada pedaco do destino sem linha na tabela dos destinos, uma vez: quantos trechos, de
    que aulas e o primeiro."""
    linhas = [(pedaco, len(ids), aulas(ids, c.aula_de), ids[0]) for pedaco, ids in c.faltam.items()]
    return ["## Pedaços do destino sem linha na tabela dos destinos", ""] + tabela_ou_nada(
        ["Pedaço", "Trechos", "Aulas", "Primeiro trecho"], linhas, "Nenhum.", numericas=(1,))


def nome_do_posto(posto, formato):
    """O lugar de um posto no relatorio: o documento, a entrada e a parte."""
    parte = nomes_das_partes(posto.entrada, formato).get(posto.parte, str(posto.parte))
    return f"{posto.documento}: {nome_da_entrada(posto.entrada)} ({parte})"


def secao_sem_lugar(c):
    """Os trechos de uma aula ate a ultima sem lugar depois do limite, com os lugares que
    perderam."""
    linhas = [(i, "; ".join(nome_do_posto(p, c.formato) for p in postos_sem_repetir(postos)))
              for i, postos in c.perdidos.items()]
    return ["## Trechos até a última aula sem lugar depois do limite", ""] + tabela_ou_nada(
        ["Trecho", "Lugares que perdeu"], linhas, "Nenhum.")


def texto_do_relatorio(trechos, notas, c):
    formato = c.formato
    saida = ["# Conferência dos moldes", "",
             f"{len(trechos)} trechos com campos e {sum(notas.values())} notas sem campos "
             "(as notas não são trechos e não vão para documento nenhum).", ""]
    saida += tabela_das_classes(c.classes, formato) + [""]
    for d in formato["documentos"]:
        saida += [f"## {d['nome']} (molde de cada {d['unidade']})", ""]
        saida += MOLDES[d["molde"]].secao(d, formato, c.cheio[d["id"]], c.aula_de)
    saida += ["## Onde cada tipo se ensina, e onde os trechos caem", ""] + secao_onde(formato, c.tipos)
    saida += secao_das_unidades(c) + secao_so_mencionadas(c) + secao_das_fontes(c) + secao_sem_linha(c)
    saida += secao_sem_lugar(c)
    saida += ["## Problemas", ""] + ([f"- {linha}" for linha in linhas_dos_avisos(c.avisos)] or ["Nenhum."])
    return "\n".join(saida) + "\n"


# ---------- as entradas ----------

def texto_de(caminho, ler):
    """O que 'ler' da do texto do arquivo, com o nome dele; ValueError, que diz o arquivo,
    quando o texto nao esta em UTF-8."""
    texto, erros = le_texto(caminho, caminho.name)
    if erros:
        raise ValueError(erros[0])
    return ler(texto, caminho.name)


def le_entradas(projeto):
    """((formato, trechos, notas por aula, aulas, linhas da tabela da leitura, tabela dos
    destinos), []) das entradas, ou (None, erros) quando alguma tem erro."""
    faltam = [f"falta o arquivo {projeto.caminho(n)} ({n!r} no projeto.json)"
              for n in ENTRADAS if not projeto.caminho(n).is_file()]
    if faltam:
        return None, faltam
    formato, erros = le_formato(projeto)
    forma, erros_da_forma = le_dados(projeto.caminho("forma_analise"), esquema("forma-analise"))
    erros += erros_da_forma
    if erros:
        return None, erros
    nome = projeto.caminho("formato").name
    erros = [f"{nome}: {onde(d)}: tipo de molde que este script não conhece: {d['molde']!r}"
             for d in formato["documentos"] if d["molde"] not in MOLDES]
    erros += [f"{nome}: documentos_vem_de: fonte que este script não conhece: {f!r}"
              for f in formato["documentos_vem_de"] if f not in FONTES]
    if erros:
        return None, erros
    lidas = {}
    try:
        lidas["analises"] = lugares.trechos_das_analises(projeto.caminho("analises_das_aulas"), forma, formato)
    except lugares.ErroDeRegras as e:
        erros.append(f"{nome}: {e}")
    except ValueError as e:  # a forma das analises, ou um arquivo de analise, que nao se le
        erros.append(str(e))
    for chave_, ler in (("lugares_lidos", lidos.ler), ("destinos", destinos.ler)):
        try:
            lidas[chave_] = texto_de(projeto.caminho(chave_), ler)
        except ValueError as e:
            erros.append(str(e))
    if "analises" in lidas:
        erros += [f"{nome}: o limite: {e}" for e in limite.erros_das_entradas(
            [], {}, lidas["analises"][2], formato["ultima_aula"], formato["partes_para_tratar"], {})]
    if erros:
        return None, erros
    return (formato, *lidas["analises"], lidas["lugares_lidos"], lidas["destinos"]), []


def nada_gravado(erros):
    """Mostra cada erro de entrada e que nada foi gravado; devolve o codigo de saida."""
    for e in erros:
        print(f"{ERRO}: {e}")
    print("Nada foi gravado.")
    return 1


def main(argv=None):
    p = argparse.ArgumentParser(description="Confere os moldes do material contra as análises das aulas.")
    p.add_argument("--projeto", type=Path, help="projeto.json (padrao: o primeiro achado subindo a partir daqui)")
    a = p.parse_args(argv)
    projeto = acha_projeto(a.projeto)
    entradas, erros = le_entradas(projeto)
    if erros:
        return nada_gravado(erros)
    formato, trechos, notas, aulas_, linhas, nomeia = entradas
    c = Conferencia(formato, aulas_)
    validas, erros_da_tabela = lidos.conferidas(linhas, {t["id"] for t in trechos}, formato)
    for e in erros_da_tabela:
        c.avisa(ERRO, None, f"{projeto.caminho('lugares_lidos').name}, {e}")
    do_formato = {i for d in formato["documentos"] for i, _ in ids_do_documento(d)}
    for pedaco, i in destinos.desconhecidos(nomeia, do_formato):
        c.avisa(ERRO, None, f"{projeto.caminho('destinos').name}: o pedaço {pedaco!r} nomeia {i!r}, que não é "
                "unidade, item nem conjunto do formato")
    try:
        colocar(trechos, validas, nomeia, c)
    except limite.ErroDeLimite as e:
        return nada_gravado([f"{projeto.caminho('formato').name}: {e}"])
    except destinos.ErroDeDestinos as e:
        return nada_gravado([f"{projeto.caminho('forma_analise').name}: {e}"])
    saida = projeto.caminho("conferencia_moldes")
    saida.parent.mkdir(parents=True, exist_ok=True)
    saida.write_text(texto_do_relatorio(trechos, notas, c), encoding="utf-8")
    for linha in linhas_dos_avisos(c.avisos):
        print(linha)
    quantos = collections.Counter(tipo for tipo, _, _ in c.avisos)
    print(f"{len(trechos)} trechos; {c.classes[('estudo',)]} com lugar; "
          f"{quantos[ERRO]} {ERRO}, {quantos[FALTA]} {FALTA}")
    print(f"conferência: {saida}")
    return 1 if c.avisos else 0


if __name__ == "__main__":
    sys.exit(main())
