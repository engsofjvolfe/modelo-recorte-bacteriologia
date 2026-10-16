# SPDX-License-Identifier: GPL-3.0-or-later
# Copyright do codigo sob GPL-3.0 -- ver LICENSE e NOTICE.md na raiz do projeto.

"""
Confere os moldes do material de estudo contra as analises das aulas: cada trecho das
analises tem lugar num documento do formato e, dentro dele, numa parte do molde dele;
nenhuma parte de molde fica sem trecho; e cada parte diz de onde vem -- os tipos, quantos
trechos e de que aulas, e se a ordem dela e dada ou proposta. Grava o relatorio da
conferencia.

Os documentos em que o trecho cai vem das regras do formato (lugares.py): pelo grupo, pelo
caminho ou por receber todos; e elas o tiram do material pelo tipo. A tabela da leitura
(lidos.py) da o que as regras nao dao: a unidade e o eixo numa ficha, o documento do
trecho que as regras deixam em aberto -- o que espera o assunto e o marcado que nao cai em
documento de conteudo -- e o trecho que a leitura pos fora. Dentro do documento, a parte
vem do tipo de molde dele (MOLDES): no "partes_por_tipo", a parte da sequencia de cada
tipo do trecho, e o trecho sem tipo de parte nenhuma fica junto do assunto dele; no molde
com grade (comum.MOLDE_COM_GRADE), as linhas da tabela da leitura; no "formas", a forma de
pergunta de cada tipo, na aula do trecho; no "colunas", o cartao.

O trecho marcado (pelas marcas do formato) que nao tem lugar espera o lugar dele: cada
lugar que falta e uma linha FALTA. O resto que nao fecha e ERRO: a linha da tabela que nao
fecha com as analises ou com o formato; o trecho de estudo sem documento de conteudo, ou
sem eixo numa ficha; o grupo ou o tipo que o formato nao tem; o tipo sem forma de pergunta;
a parte de molde sem trecho; o trecho de fora com lugar. Cada um sai na tela e no fim do
relatorio, que e gravado assim mesmo.

Os caminhos vem do projeto.json: "formato", "forma_analise", "analises_das_aulas",
"lugares_lidos" e "conferencia_moldes". O formato e lido pela leitura dele
(comum.le_formato); a forma das analises, pela leitura de todo arquivo de dados
(validar_dados.le_dados), contra o molde dela; as analises, pelo analises.py, com as regras
do formato conferidas contra a forma. Com erro numa entrada -- arquivo que falta, que nao
se le ou fora do molde, regra que nao combina com a forma, tipo de molde que este script
nao conhece, ultima aula do formato que nao e a de nenhuma analise --, cada erro sai numa
linha ERRO e nada e gravado.

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
import lidos  # noqa: E402
import lugares  # noqa: E402
from comum import MOLDE_COM_GRADE, acha_projeto, le_formato, onde, unidades  # noqa: E402
from relatorio import por_chave, tabela, tabela_das_classes  # noqa: E402
from validar_dados import esquema, le_dados  # noqa: E402

ENTRADAS = ("formato", "forma_analise", "lugares_lidos")  # os arquivos que o script le, pelo nome no projeto.json
ERRO, FALTA = "ERRO", "FALTA"  # o que abre a linha do que nao fecha e a do lugar que um trecho marcado espera
JUNTO = (None, None)  # o lugar do trecho que vai junto do assunto dele, fora das partes da sequencia
NENHUM = "—"  # o que o relatorio mostra no lugar de uma lista vazia
SEM_LUGAR = "sem lugar nos documentos em que cai"  # a classe do trecho de estudo que nao tem lugar nenhum


class Conferencia:
    """O que a conferencia acha: a classe de cada trecho (as do lugares.py e ("lido", regra
    de fora)); os trechos de cada lugar de cada documento (cheio: {documento: {(unidade,
    parte): ids}}); os tipos dos trechos postos em cada documento de conteudo (tipos:
    {documento: {tipo: ids}}); a aula de cada trecho; e os avisos, (ERRO ou FALTA, id do
    trecho ou "", o que houve), na ordem em que se acham."""

    def __init__(self, formato):
        self.formato = formato
        self.documentos = {d["id"]: d for d in formato["documentos"]}
        self.de_conteudo = set(lugares.documentos_de_conteudo(formato))
        self.tipos_com_lugar = ({t for p in formato["partes_por_tipo"] for t in p["tipos"]}
                                | set(formato["tipos_junto"]))
        self.classes = collections.Counter()
        self.cheio = collections.defaultdict(lambda: collections.defaultdict(set))
        self.tipos = collections.defaultdict(lambda: collections.defaultdict(set))
        self.aula_de = {}
        self.avisos = []

    def avisa(self, tipo, trecho, mensagem):
        self.avisos.append((tipo, trecho["id"] if trecho else "", mensagem))


def trechos_em(cheio, partes=None, unidades_=None):
    """Os ids dos trechos dos lugares de 'cheio' que estao nas partes e nas unidades dadas
    (em todas, sem elas)."""
    return set().union(*(ids for (u, p), ids in cheio.items()
                         if (partes is None or p in partes) and (unidades_ is None or u in unidades_)))


def da_grade_do_documento(documento):
    """As unidades que usam a grade do proprio documento: as que nao tem eixos proprios, e a
    vazia, quando o documento nao lista as suas."""
    return {""} | {u["id"] for u in unidades(documento) if not u.get("eixos")}


# ---------- o lugar do trecho em cada tipo de molde: ([lugar], erros) ----------

def pelo_tipo(trecho, documento, linhas, formato):
    """A parte da sequencia de cada tipo do trecho; JUNTO, quando nenhum tipo dele tem parte."""
    tipos = set(lugares.valor(trecho, "tipo"))
    return [("", p["id"]) for p in formato["partes_por_tipo"] if tipos & set(p["tipos"])] or [JUNTO], []


def pela_tabela(trecho, documento, linhas, formato):
    """A unidade e a parte de cada linha da tabela da leitura do trecho no documento."""
    return [(linha["unidade"], linha["parte"]) for linha in linhas], []


def pela_forma(trecho, documento, linhas, formato):
    """A aula do trecho e o numero de cada forma de pergunta com um tipo dele; o tipo dele sem
    forma e erro."""
    tipos, formas = lugares.valor(trecho, "tipo"), list(enumerate(documento["formas"], 1))
    achados = [(trecho["aula"], n) for n, f in formas if set(tipos) & set(f["tipos"])]
    return achados, [f"tipo sem forma de pergunta em {documento['id']}: {t}"
                     for t in tipos if not any(t in f["tipos"] for _, f in formas)]


def no_cartao(trecho, documento, linhas, formato):
    """O cartao do trecho, um lugar so."""
    return [("", "")], []


# ---------- as partes de molde sem trecho: erros ----------

def sem_vazias(documento, cheio):
    """Nenhuma: o molde so tem as partes que os trechos dao."""
    return []


def vazias_da_grade(documento, cheio):
    """O eixo da grade do documento que nenhuma unidade que a usa preenche; o elo sem eixo com
    trecho; o eixo da grade de uma unidade com a sua; a abertura que recebe trechos e nao tem
    nenhum."""
    usam = da_grade_do_documento(documento)
    erros = [f"{onde(documento)}: o eixo {e['id']!r} não tem trecho"
             for e in documento.get("eixos", []) if not trechos_em(cheio, {e["id"]}, usam)]
    erros += [f"{onde(documento)}: o elo {elo['id']!r} não tem eixo com trecho"
              for elo in documento.get("elos", []) if not trechos_em(cheio, set(elo["eixos"]), usam)]
    erros += [f"{onde(documento, u)}: o eixo {e['id']!r} não tem trecho"
              for u in unidades(documento) for e in u.get("eixos", []) if not trechos_em(cheio, {e["id"]}, {u["id"]})]
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
    junto = cheio.get(JUNTO, set())
    if junto:
        saida += [f"{len(junto)} trechos só de tipos que se ensinam junto de outro trecho "
                  f"({', '.join(formato['tipos_junto'])}): ficam junto do assunto deles.", ""]
    if documento.get("casos"):
        saida += [f"Cada caso, depois dos fatos de cada {documento['unidade']}:", ""]
        saida += tabela(["Parte do caso", "Ordem"], [(c["nome"], c["ordem"]) for c in documento["casos"]]) + [""]
    return saida


def secao_eixos(documento, formato, cheio, aula_de):
    """Cada abertura; a grade do documento, com quantos trechos cada eixo tem nas unidades que
    a usam, e os elos; e a grade de cada unidade com a sua."""
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
            linhas = [(e["nome"], len(trechos_em(cheio, {e["id"]}, {u["id"]})), e["ordem"]) for e in u["eixos"]]
            saida += [f"### {u['nome']} ({len(trechos_em(cheio, None, {u['id']}))} trechos)", ""]
            saida += tabela(["Eixo", "Trechos", "Ordem"], linhas, numericas=(1,)) + [""]
    return saida


def secao_perguntas(documento, formato, cheio, aula_de):
    """As partes de cada pergunta; cada forma de pergunta, com os tipos, quantos trechos e a
    ordem; e quantos trechos de cada aula."""
    saida = ["Cada pergunta: " + "; ".join(f"{p['nome']} ({p['ordem']})" for p in documento["pergunta"]) + ".", ""]
    linhas = [(f["verbo"], "; ".join(f["tipos"]), len(trechos_em(cheio, {n})), f["ordem"])
              for n, f in enumerate(documento["formas"], 1)]
    saida += tabela(["Forma", "Tipos", "Trechos", "Ordem"], linhas, numericas=(2,)) + [""]
    por_aula = collections.Counter({a: len(trechos_em(cheio, None, {a})) for a, _ in cheio})
    return saida + ["Trechos por aula: " + ("; ".join(f"{a} {n}" for a, n in por_chave(por_aula)) or NENHUM) + ".", ""]


def secao_cartoes(documento, formato, cheio, aula_de):
    """Quantos trechos viram cartao, e as colunas do cartao, com o lado e a ordem."""
    linhas = [(c["id"], c["lado"], c["ordem"]) for c in documento["colunas"]]
    return [f"{len(trechos_em(cheio))} trechos viram cartão.", ""] + tabela(["Coluna", "Lado", "Ordem"], linhas) + [""]


Molde = collections.namedtuple("Molde", "partes falta vazias secao")
# o que o script faz com cada tipo de molde de documento (esquemas/formato.schema.json): partes(trecho,
# documento, linhas da tabela do trecho no documento, formato) -> ([lugar], erros); falta, o nome do lugar
# que falta quando partes nao da nenhum (None, quando o molde sempre da um ou os erros dizem por que);
# vazias(documento, cheio) -> erros; secao(documento, formato, cheio, aula de cada trecho) -> linhas
MOLDES = {
    "partes_por_tipo": Molde(pelo_tipo, None, sem_vazias, secao_partes),
    MOLDE_COM_GRADE: Molde(pela_tabela, "eixo", vazias_da_grade, secao_eixos),
    "formas": Molde(pela_forma, None, vazias_das_formas, secao_perguntas),
    "colunas": Molde(no_cartao, None, sem_vazias, secao_cartoes),
}


# ---------- o lugar de cada trecho ----------

def partes_em(trecho, d, linhas, c):
    """([lugar], o que falta ou None): os lugares do trecho no documento d, pelo molde dele,
    com os erros que o molde acha em c."""
    documento = c.documentos[d]
    molde = MOLDES[documento["molde"]]
    achados, erros = molde.partes(trecho, documento, [linha for linha in linhas if linha["documento"] == d],
                                  c.formato)
    for e in erros:
        c.avisa(ERRO, trecho, e)
    return achados, (f"sem {molde.falta} em {d}" if molde.falta and not achados else None)


def documentos_do_trecho(trecho, classe, caidos, linhas, c):
    """Os documentos de conteudo onde o lugar do trecho se procura: os das regras; quando elas
    deixam o documento em aberto, os da tabela da leitura. A linha da tabela num documento em
    que as regras nao poem o trecho e erro."""
    pela_regra = [d for d in caidos if d in c.de_conteudo]
    na_tabela = list(dict.fromkeys(linha["documento"] for linha in linhas))
    if classe != ("estudo",):
        return na_tabela
    for d in na_tabela:
        if d not in pela_regra:
            c.avisa(ERRO, trecho, f"lugar na tabela da leitura em {d}, documento em que o trecho não cai")
    return pela_regra


def guarda(trecho, postos, caidos, c):
    """Guarda o trecho nos lugares dele em cada documento de conteudo, com os tipos dele, e nos
    dos documentos que recebem todos."""
    for d, achados in postos.items():
        for lugar in achados:
            c.cheio[d][lugar].add(trecho["id"])
        for tipo in lugares.valor(trecho, "tipo"):
            c.tipos[d][tipo].add(trecho["id"])
    for d in caidos:
        if c.documentos[d].get("todos"):
            achados, falta = partes_em(trecho, d, [], c)
            if falta:
                c.avisa(ERRO, trecho, falta)
            for lugar in achados:
                c.cheio[d][lugar].add(trecho["id"])


def classe_do_trecho(trecho, linhas, c):
    """A classe do trecho, depois de posto nos lugares dele, com os avisos dele em c. O trecho
    de estudo que nao tem lugar nenhum fica marcado, quando tem marca; senao, a espera do
    assunto, quando espera, ou sem lugar."""
    classe, caidos = lugares.lugar(trecho, c.formato)
    fora = [linha for linha in linhas if linha["documento"] == lidos.FORA]
    if classe[0] == "problema":
        c.avisa(ERRO, trecho, classe[1])
        return classe
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
    documentos = documentos_do_trecho(trecho, classe, caidos, linhas, c)
    postos, faltas = {}, ([] if documentos else ["sem documento de conteúdo"])
    for d in documentos:
        achados, falta = partes_em(trecho, d, linhas, c)
        if achados:
            postos[d] = achados
        if falta:
            faltas.append(falta)
    marcas = lugares.marcas(trecho, c.formato)
    nomes = ", ".join(m["nome"] for m in c.formato["marcas"] if m["id"] in marcas)
    for falta in faltas:
        c.avisa(FALTA if marcas else ERRO, trecho, f"marcado ({nomes}), {falta}" if marcas else falta)
    if not postos:
        return ("marca", marcas[0]) if marcas else (classe if classe == ("assunto",) else ("problema", SEM_LUGAR))
    guarda(trecho, postos, caidos, c)
    return ("estudo",)


def colocar(trechos, linhas, c):
    """Poe cada trecho no lugar dele e acha as partes de molde sem trecho; tudo vai para c."""
    da_tabela = lidos.por_trecho(linhas)
    for trecho in trechos:
        c.aula_de[trecho["id"]] = trecho["aula"]
        c.classes[classe_do_trecho(trecho, da_tabela.get(trecho["id"], []), c)] += 1
    for d in c.formato["documentos"]:
        for e in MOLDES[d["molde"]].vazias(d, c.cheio[d["id"]]):
            c.avisa(ERRO, None, e)


# ---------- o relatorio ----------

def linhas_dos_avisos(avisos):
    return [f"{tipo}: {f'{i}: ' if i else ''}{mensagem}" for tipo, i, mensagem in avisos]


def secao_onde(formato, tipos):
    """Para cada tipo de onde_se_ensina, os documentos onde ele se ensina e os outros em que
    trechos dele caem, com quantos."""
    nomes = {d["id"]: d["nome"] for d in formato["documentos"]}
    linhas = [(tipo, "; ".join(nomes[d] for d in docs),
               "; ".join(f"{nomes[d]} {len(tipos[d][tipo])}" for d in nomes if d not in docs and tipos[d].get(tipo))
               or NENHUM)
              for tipo, docs in formato["onde_se_ensina"].items()]
    return tabela(["Tipo", "Se ensina em", "Também cai em (trechos)"], linhas) + [""]


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
    saida += ["## Problemas", ""] + ([f"- {linha}" for linha in linhas_dos_avisos(c.avisos)] or ["Nenhum."])
    return "\n".join(saida) + "\n"


# ---------- as entradas ----------

def le_entradas(projeto):
    """((formato, trechos, notas por aula, linhas da tabela), []) das entradas, ou (None,
    erros) quando alguma tem erro."""
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
    if erros:
        return None, erros
    trechos = notas = aulas_ = linhas = None
    try:
        trechos, notas, aulas_ = lugares.trechos_das_analises(projeto.caminho("analises_das_aulas"), forma, formato)
    except lugares.ErroDeRegras as e:
        erros.append(f"{nome}: {e}")
    except ValueError as e:  # a forma das analises, ou um arquivo de analise, que nao se le
        erros.append(str(e))
    try:
        linhas = lidos.ler_tabela(projeto.caminho("lugares_lidos"))
    except ValueError as e:
        erros.append(str(e))
    if aulas_ is not None and formato["ultima_aula"] not in aulas_:
        erros.append(f"{nome}: a ultima_aula {formato['ultima_aula']!r} não é a aula de nenhuma análise "
                     f"({', '.join(aulas_)})")
    return (None if erros else (formato, trechos, notas, linhas)), erros


def main(argv=None):
    p = argparse.ArgumentParser(description="Confere os moldes do material contra as análises das aulas.")
    p.add_argument("--projeto", type=Path, help="projeto.json (padrao: o primeiro achado subindo a partir daqui)")
    a = p.parse_args(argv)
    projeto = acha_projeto(a.projeto)
    entradas, erros = le_entradas(projeto)
    if erros:
        for e in erros:
            print(f"{ERRO}: {e}")
        print("Nada foi gravado.")
        return 1
    formato, trechos, notas, linhas = entradas
    c = Conferencia(formato)
    validas, erros_da_tabela = lidos.conferidas(linhas, {t["id"] for t in trechos}, formato)
    for e in erros_da_tabela:
        c.avisa(ERRO, None, f"{projeto.caminho('lugares_lidos').name}, {e}")
    colocar(trechos, validas, c)
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
