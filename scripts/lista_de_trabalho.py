# SPDX-License-Identifier: GPL-3.0-or-later
# Copyright do codigo sob GPL-3.0 -- ver LICENSE e NOTICE.md na raiz do projeto.

"""
Grava a lista de trabalho de um texto do material: o que escrever nele e o que ler antes de
escrever. O texto, as partes dele, os trechos de cada parte e a ordem de escrita sao os do
conferidor do material (confere_material.confere), que os tira da conferencia dos moldes. A
lista e um arquivo Markdown na pasta protegida, porque traz o texto das aulas: o caminho
"listas_de_trabalho" do projeto.json, com o id do documento e o codigo do texto, separados
por hifen, no lugar da variavel.

A lista diz, nesta ordem:
  - o texto: o nome e o codigo dele, o documento e a aula em que ele se escreve; no texto de
    uma unidade, as aulas que tratam dela e as que so a mencionam, a planilha dos cartoes
    (comum.planilha), com as colunas que o conferidor confere nela ("coluna_trechos" e
    "coluna_subdecks", no projeto.json), e a prova dos cartoes (comum.arquivo_da_prova); no
    texto que depende de outros, esses outros;
  - os codigos escondidos, na ordem do molde (confere_material.marca): o que abre o texto e,
    em cada parte, o do item em que ela fica, quando fica num, e o dela, com os trechos que
    ela recebe. De cada trecho: o codigo escondido, a aula, o slide, o texto; cada campo da
    forma das analises, menos o do papel DESTINO (o lugar do trecho e o da propria lista, e
    as marcas dizem do que ele fala) -- o campo com papel pelo valor, o sem papel como a
    analise o escreve --; as marcas do formato que ele tem; e, quando e assim, que ele esta
    ali por um conjunto, que e de uma aula depois da ultima, cada divergencia do arquivo das
    divergencias que tem o codigo dele (divergencias.em_linha: o fato, a forma que o material
    ensina e as outras, com as fontes) e, no texto que depende de outros, onde o codigo dele
    esta nesses textos: o arquivo, a linha e a unidade, o item e a parte. A parte que nao
    recebe trechos, e a que recebe e nao tem nenhum, dizem isso.
    Depois, os trechos que vao junto do assunto, em qualquer parte que recebe trechos;
  - os capitulos a ler inteiros: para cada campo da forma que diz a fonte das paginas que
    cita ("fonte"), as transcricoes da pasta "gerados" registradas com essa fonte
    (conferencia.fonte_da_transcricao) que tem um titulo de pagina -- o rotulo inteiro, como
    "p. 12", sem letra, numero ou sublinhado colado antes ou depois -- num pedaco desse campo
    de algum trecho do texto, na ordem natural dos nomes delas (9 antes de 10); e, como
    estao, os pedacos em que nenhum rotulo aparece, cada um com os trechos que o tem. Os
    pedacos sao os da forma em lista do campo, ou o campo inteiro, numa forma que nao da
    lista, sem o valor vazio da forma;
  - as duvidas abertas: do arquivo das duvidas, a secao de cada aula com trecho no texto e,
    inteiras, as secoes que nao sao de nenhuma aula das analises, na ordem do arquivo. Cada
    secao comeca num titulo SECAO, fora do codigo, e vai ate o proximo; ela e de uma aula
    quando a primeira palavra do titulo e o comeco do nome dos arquivos das analises
    ("prefixo_arquivo", na forma) com a chave da aula, como "aula-3". Os titulos copiados
    descem um nivel, para ficar dentro da secao da lista.

O texto que depende de outros -- o de uma entrada de um documento que recebe todos os
trechos, como as perguntas de prova de uma aula -- so tem lista quando todos os textos de
que ele depende estao prontos no conferidor.

Com erro, cada um sai numa linha ERRO e nada e gravado: o que o conferidor recusa (a
conferencia dos moldes com aviso, o codigo que nenhum texto tem), o texto que depende de
outros que ainda nao estao prontos, o arquivo das duvidas que falta ou que nao esta em
UTF-8 e o arquivo das divergencias que falta, fora do UTF-8 ou fora do molde
(divergencias.le_divergencias). Sem erro, o script diz o arquivo gravado e quantas partes, trechos, transcricoes a
ler, pedacos sem pagina e secoes das duvidas a lista tem.

Uso (de qualquer pasta dentro do projeto):
    python scripts/lista_de_trabalho.py --unidade <codigo> --duvidas <arquivo das duvidas>
    python scripts/lista_de_trabalho.py --unidade <codigo> --duvidas <arquivo> --projeto projeto.json
"""

import argparse
import collections
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import confere_material  # noqa: E402
import divergencias  # noqa: E402
import lugares  # noqa: E402
import marcas  # noqa: E402
from analises import nfc, ordem_natural  # noqa: E402
from comum import acha_projeto, arquivo_da_prova, linhas_fora_de_codigo, no_projeto, planilha  # noqa: E402
from conferencia import fonte_da_transcricao, secoes, transcricoes_da_pasta  # noqa: E402
from confere_moldes import nada_gravado  # noqa: E402
from validar_dados import esquema, le_dados, le_texto  # noqa: E402

DESTINO = "destino"  # o papel do campo das analises que a lista nao mostra
SECAO = "## "  # o comeco do titulo de cada secao do arquivo das duvidas
NIVEL = "#"  # o que um titulo ganha na frente para descer um nivel: o de uma parte de item e o copiado das duvidas
NENHUM = confere_material.NENHUM  # o que fica no lugar de um valor que falta
SEM_TRANSCRICAO, SEM_PEDACO, SEM_SECAO = "Nenhuma transcrição.", "Nenhum pedaço.", "Nenhuma seção."  # as listas vazias
# os titulos e os rotulos da lista
TITULO = "Lista de trabalho"
UNIDADE, DOCUMENTO, AULA = "Unidade", "Documento", "Aula em que se escreve"
TRATAM, MENCIONAM = "Aulas que tratam dela", "Aulas que só a mencionam"
PLANILHA, PROVA, DEPENDE = "Planilha dos cartões", "Prova dos cartões", "Depende dos textos, todos prontos"
CODIGOS_NA_COLUNA = "os códigos dos trechos de cada cartão na coluna `{}`"
AULA_NA_COLUNA = "a aula {} na coluna `{}` de cada cartão"
PARTES = "Os códigos escondidos e os trechos, na ordem do molde"
ABRE = "O texto abre com {}."
NAO_RECEBE, SEM_TRECHO = "Não recebe trechos das aulas.", "Nenhum trecho das aulas."
JUNTO = "Junto do assunto, em qualquer parte que recebe trechos"
NA_AULA = "aula {}, slide {}"
MARCAS = "marcas"
POR_CONJUNTO = "está aqui por um conjunto: o destino dele nomeia um grupo do qual esta unidade, ou este item, faz parte"
DEPOIS = "é de uma aula depois da última ({})"
ENSINADO_EM = "ensinado em"
DIVERGENCIA = "divergência"
NA_LINHA = "`{}`, linha {} ({})"
CAPITULOS = "Os capítulos a ler inteiros"
DO_CAMPO = "Campo `{}`, fonte {}"
SEM_PAGINA = "Pedaços em que nenhum título de página aparece"
NENHUM_CAMPO = "Nenhum campo da forma das análises diz a fonte das páginas que cita."
DUVIDAS = "As dúvidas abertas"
DE_ONDE = "Copiadas de `{}`."
Contexto = collections.namedtuple("Contexto", "projeto c forma trechos paginas onde divergencias")
# o que a lista usa: o projeto; a Conferencia dos moldes; a forma das analises; {id: trecho}; {fonte: [(transcricao,
# [padrao de cada titulo de pagina])]}; {id: [onde o codigo do trecho esta nos textos de que o texto depende]}; e
# {id: [divergencia que tem o codigo do trecho]}
Lista = collections.namedtuple("Lista", "arquivo linhas partes trechos transcricoes sem_pagina secoes")
# a lista pronta para gravar: o arquivo, as linhas e quantas partes, trechos, transcricoes a ler, pedacos sem pagina
# e secoes das duvidas ela tem


# ---------- os trechos ----------

def linhas_do_trecho(trecho, ctx, por_conjunto):
    """As linhas de um trecho na lista: o codigo escondido, a aula e o slide; o texto; cada campo da forma menos o do
    destino -- o com papel pelo valor, o sem papel como a analise o escreve --; as marcas; e, quando e assim, que ele
    esta ali por um conjunto, que e de uma aula depois da ultima, cada divergencia que tem o codigo dele e onde o codigo
    dele esta nos textos de que o texto depende."""
    cm, forma, formato = confere_material, ctx.forma, ctx.c.formato
    saida = [f"- `{cm.marca(cm.TRECHO, trecho['id'])}` — {NA_AULA.format(trecho['aula'], trecho['slide'])}",
             f"  - {trecho['texto']}"]
    for campo in forma["campos"]:
        if campo.get("papel") == DESTINO:
            continue
        nome = campo["nome"]
        valor = (", ".join(trecho["valores"][nome]) or forma["vazio"]) if "papel" in campo else trecho["brutos"][nome]
        saida.append(f"  - {nome}: {valor.strip()}")
    suas = lugares.marcas(trecho, formato)
    if suas:
        saida.append(f"  - {MARCAS}: " + ", ".join(m["nome"] for m in formato["marcas"] if m["id"] in suas))
    if por_conjunto:
        saida.append(f"  - {POR_CONJUNTO}")
    if trecho["aula"] not in ctx.c.ate_a_ultima:
        saida.append(f"  - {DEPOIS.format(formato['ultima_aula'])}")
    saida += [f"  - {DIVERGENCIA}: {divergencias.em_linha(d)}" for d in ctx.divergencias.get(nfc(trecho["id"]), [])]
    return saida + [f"  - {ENSINADO_EM}: {lugar}" for lugar in ctx.onde.get(nfc(trecho["id"]), [])]


def linhas_das_partes(texto, ctx):
    """As linhas dos codigos escondidos, na ordem do molde: o que abre o texto e, em cada parte, o do item dela, quando
    ela fica num, e o dela, com os trechos dela, ou o aviso de que ela nao recebe trechos ou nao tem nenhum; e os
    trechos que vao junto do assunto."""
    cm = confere_material
    saida, aberto = [f"## {PARTES}", "", ABRE.format(f"`{cm.marca(cm.UNIDADE, texto.codigo)}`"), ""], None
    for p in texto.partes:
        titulo = "###"
        if p.item is not None:
            if p.item["id"] != aberto:
                saida += [f"### {p.item['nome']} — `{cm.marca(cm.ITEM, p.item['id'])}`", ""]
                aberto = p.item["id"]
            titulo += NIVEL
        saida += [f"{titulo} {p.nome} — `{cm.marca(cm.PARTE, p.id)}`", ""]
        if not p.recebe or not p.trechos:
            saida += [NAO_RECEBE if not p.recebe else SEM_TRECHO, ""]
            continue
        for i in p.trechos:
            saida += linhas_do_trecho(ctx.trechos[i], ctx, i in p.por_conjunto)
        saida.append("")
    if texto.junto:
        saida += [f"### {JUNTO}", ""]
        for i in texto.junto:
            saida += linhas_do_trecho(ctx.trechos[i], ctx, i in texto.junto_por_conjunto)
        saida.append("")
    return saida


def onde_cada_um(projeto, deps):
    """{id: [lugar]} de cada trecho nos textos dados: o arquivo, a linha e a unidade, o item e a parte de cada codigo
    escondido dele ali, na ordem dos arquivos e das linhas."""
    cm, codigos, saida = confere_material, {d.codigo for d in deps}, {}
    if not codigos:
        return saida
    for i, lugares_ in cm.lugares_dos_trechos(projeto).items():
        nos_deps = [NA_LINHA.format(m.arquivo, m.linha, marcas.mostra(caminho, cm.NIVEIS))
                    for m, caminho in lugares_ if caminho[0] in codigos]
        if nos_deps:
            saida[i] = nos_deps
    return saida


# ---------- os capitulos a ler ----------

def rotulo_inteiro(rotulo):
    """O padrao que acha o rotulo de uma pagina inteiro num texto, em NFC: sem letra, numero ou sublinhado colado
    antes ou depois dele."""
    return re.compile(rf"(?<!\w){re.escape(nfc(rotulo))}(?!\w)")


def paginas_das_fontes(projeto, fontes, saida):
    """{fonte: [(transcricao, [padrao de cada titulo de pagina])]} das transcricoes da pasta "gerados" registradas com
    cada uma das fontes dadas, na ordem natural dos nomes delas, sem o arquivo de saida."""
    achadas = {f: [] for f in fontes}
    for arquivo, texto in transcricoes_da_pasta(projeto.caminho("gerados"), saida):
        chave, _, _ = fonte_da_transcricao(texto, projeto.raiz)
        if chave in achadas:
            achadas[chave].append((arquivo, [rotulo_inteiro(r) for r, _, _ in secoes(texto)]))
    return {f: sorted(lista, key=lambda x: (ordem_natural(x[0].name), x[0].name)) for f, lista in achadas.items()}


def pedacos(trecho, campo, vazio):
    """Os pedacos do campo do trecho, em NFC: os da forma em lista, ou o campo inteiro, numa forma que nao da lista;
    sem o pedaco em branco e sem o valor vazio."""
    valor = trecho["valores"][campo["nome"]]
    brutos = [p.strip() for p in (valor if isinstance(valor, list) else [valor])]
    return [nfc(p) for p in brutos if p and p != vazio]


def capitulos(texto, ctx):
    """[(campo, transcricoes, {pedaco: ids})] de cada campo da forma que diz a fonte das paginas que cita: as
    transcricoes registradas com a fonte que tem um titulo de pagina num pedaco do campo de algum trecho do texto, na
    ordem natural dos nomes delas; e os pedacos em que nenhum titulo aparece, com os trechos de cada um, na ordem em
    que aparecem."""
    saida = []
    for campo in [x for x in ctx.forma["campos"] if "fonte" in x]:
        paginas, achadas, sem_pagina = ctx.paginas[campo["fonte"]], set(), {}
        for i in confere_material.trechos_do_texto(texto):
            for pedaco in pedacos(ctx.trechos[i], campo, ctx.forma["vazio"]):
                suas = {arquivo for arquivo, rotulos in paginas if any(r.search(pedaco) for r in rotulos)}
                achadas |= suas
                if not suas:
                    sem_pagina.setdefault(pedaco, []).append(i)
        saida.append((campo, [arquivo for arquivo, _ in paginas if arquivo in achadas], sem_pagina))
    return saida


def linhas_dos_capitulos(texto, ctx):
    """(linhas, quantas transcricoes, quantos pedacos sem pagina) dos capitulos a ler inteiros, campo por campo."""
    saida, transcricoes, sem_paginas = [f"## {CAPITULOS}", ""], 0, 0
    achados = capitulos(texto, ctx)
    if not achados:
        return saida + [NENHUM_CAMPO, ""], 0, 0
    for campo, arquivos, sem_pagina in achados:
        saida += [f"### {DO_CAMPO.format(campo['nome'], campo['fonte'])}", ""]
        saida += [f"- `{no_projeto(arquivo, ctx.projeto)}`" for arquivo in arquivos] or [SEM_TRANSCRICAO]
        saida += ["", f"{SEM_PAGINA}:", ""]
        saida += ([f"- {pedaco} — " + ", ".join(f"`{i}`" for i in ids) for pedaco, ids in sem_pagina.items()]
                  or [SEM_PEDACO])
        saida.append("")
        transcricoes, sem_paginas = transcricoes + len(arquivos), sem_paginas + len(sem_pagina)
    return saida, transcricoes, sem_paginas


# ---------- as duvidas ----------

def secoes_das_duvidas(texto):
    """[(titulo, [(linha, se ela esta fora do codigo)])] das secoes do arquivo das duvidas, na ordem: cada uma comeca
    num titulo SECAO, fora do codigo, e vai ate o proximo; o que vem antes do primeiro nao e secao."""
    fora, saida = {n for n, _ in linhas_fora_de_codigo(texto)}, []
    for n, linha in enumerate(texto.splitlines(), 1):
        if n in fora and linha.startswith(SECAO):
            saida.append((linha[len(SECAO):].strip(), []))
        if saida:
            saida[-1][1].append((linha, n in fora))
    return saida


def linhas_das_duvidas(arquivo, conteudo, texto, ctx):
    """(linhas, quantas secoes) das duvidas abertas: a secao de cada aula com trecho no texto e, inteiras, as que nao
    sao de nenhuma aula das analises, na ordem do arquivo, com os titulos um nivel abaixo."""
    das_aulas = {nfc(ctx.forma["prefixo_arquivo"] + a): a for a in ctx.c.aulas}
    suas = {ctx.trechos[i]["aula"] for i in confere_material.trechos_do_texto(texto)}
    saida, copiadas = [f"## {DUVIDAS}", "", DE_ONDE.format(arquivo.resolve()), ""], 0
    for titulo, linhas in secoes_das_duvidas(conteudo):
        aula = das_aulas.get(nfc(titulo.split()[0])) if titulo.split() else None
        if aula is not None and aula not in suas:
            continue
        corpo = [NIVEL + linha if fora and linha.startswith(NIVEL) else linha for linha, fora in linhas]
        while corpo and not corpo[-1].strip():
            corpo.pop()
        saida += corpo + [""]
        copiadas += 1
    return (saida if copiadas else saida + [SEM_SECAO, ""]), copiadas


# ---------- a lista ----------

def identidade(texto, deps, projeto, c):
    """As linhas do comeco da lista: o titulo; o texto, o documento e a aula; no texto de uma unidade, as aulas que
    tratam e as que so mencionam, a planilha, com as colunas que o conferidor confere nela, e a prova; no texto que
    depende de outros, esses outros."""
    saida = [f"# {TITULO}: {texto.nome}", "", f"- {UNIDADE}: {texto.nome} (`{texto.codigo}`)",
             f"- {DOCUMENTO}: {texto.documento['nome']}", f"- {AULA}: {texto.aula or NENHUM}"]
    if texto.chave is not None:
        arquivo = planilha(projeto, texto.codigo)
        colunas = [CODIGOS_NA_COLUNA.format(x) for x in [projeto.valor("coluna_trechos")] if x]
        colunas += [AULA_NA_COLUNA.format(texto.aula, x) for x in [projeto.valor("coluna_subdecks")] if x]
        saida += [f"- {TRATAM}: {', '.join(c.limite.tratam.get(texto.chave, [])) or NENHUM}",
                  f"- {MENCIONAM}: {', '.join(c.limite.mencionam.get(texto.chave, [])) or NENHUM}",
                  f"- {PLANILHA}: `{no_projeto(arquivo, projeto)}`" + "".join(f"; {x}" for x in colunas),
                  f"- {PROVA}: `{no_projeto(arquivo_da_prova(projeto, arquivo), projeto)}`"]
    if deps:
        saida.append(f"- {DEPENDE}: " + ", ".join(f"`{d.codigo}`" for d in deps))
    return saida + [""]


def monta(projeto, pedido, arquivo_das_duvidas):
    """(Lista, []) do texto de codigo pedido, ou (None, erros): o que o conferidor recusa, o texto que depende de outros
    que ainda nao estao prontos e o arquivo das duvidas que falta ou que nao esta em UTF-8."""
    conferido, erros = confere_material.confere(projeto, pedido)
    if erros:
        return None, erros
    texto, deps = next((t, d) for t, d in conferido.lista if t.codigo == pedido)
    faltam = [d.codigo for d in deps if conferido.estados[d.codigo] != confere_material.PRONTA]
    if faltam:
        return None, [f"o texto {pedido} depende de textos que ainda não estão prontos no conferidor: "
                      + ", ".join(faltam)]
    if not arquivo_das_duvidas.is_file():
        return None, [f"falta o arquivo das dúvidas: {arquivo_das_duvidas}"]
    conteudo, erros = le_texto(arquivo_das_duvidas, arquivo_das_duvidas)
    forma, erros_da_forma = le_dados(projeto.caminho("forma_analise"), esquema("forma-analise"))
    if erros or erros_da_forma:
        return None, erros + erros_da_forma
    registradas, erros = divergencias.le_divergencias(projeto)
    if erros:
        return None, erros
    c, trechos, _ = conferido.moldes
    saida = projeto.caminho_com("listas_de_trabalho", f"{texto.documento['id']}-{texto.codigo}")
    fontes = [campo["fonte"] for campo in forma["campos"] if "fonte" in campo]
    ctx = Contexto(projeto, c, forma, {t["id"]: t for t in trechos}, paginas_das_fontes(projeto, fontes, saida),
                   onde_cada_um(projeto, deps), divergencias.por_trecho(registradas))
    dos_capitulos, transcricoes, sem_pagina = linhas_dos_capitulos(texto, ctx)
    das_duvidas, secoes_copiadas = linhas_das_duvidas(arquivo_das_duvidas, conteudo, texto, ctx)
    linhas = identidade(texto, deps, projeto, c) + linhas_das_partes(texto, ctx) + dos_capitulos + das_duvidas
    return Lista(saida, linhas, len(texto.partes), len(confere_material.trechos_do_texto(texto)), transcricoes,
                 sem_pagina, secoes_copiadas), []


def main(argv=None):
    p = argparse.ArgumentParser(description="Grava a lista de trabalho de um texto do material.")
    p.add_argument("--unidade", required=True, help="o código de um texto do material")
    p.add_argument("--duvidas", type=Path, required=True, help="o arquivo das dúvidas abertas das análises")
    p.add_argument("--projeto", type=Path, help="projeto.json (padrao: o primeiro achado subindo a partir daqui)")
    a = p.parse_args(argv)
    projeto = acha_projeto(a.projeto)
    lista, erros = monta(projeto, marcas.nfc(a.unidade), a.duvidas)
    if erros:
        return nada_gravado(erros)
    lista.arquivo.parent.mkdir(parents=True, exist_ok=True)
    lista.arquivo.write_text("\n".join(lista.linhas).rstrip("\n") + "\n", encoding="utf-8")
    print(f"lista: {no_projeto(lista.arquivo, projeto)}")
    print(f"{lista.partes} partes, {lista.trechos} trechos, {lista.transcricoes} transcrições a ler inteiras, "
          f"{lista.sem_pagina} pedaços sem página, {lista.secoes} seções das dúvidas")
    return 0


if __name__ == "__main__":
    sys.exit(main())
