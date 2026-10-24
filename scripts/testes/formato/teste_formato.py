# SPDX-License-Identifier: GPL-3.0-or-later
# Copyright do codigo sob GPL-3.0 -- ver LICENSE e NOTICE.md na raiz do projeto.

"""
Teste dos scripts de um projeto que leem o arquivo de formato: a leitura dele, no comum.py
(o molde, as ligacoes de dentro dele e o que se acha nele: as unidades e os conjuntos de um
documento, os itens e a grade de cada unidade, o que cada id quer dizer e a unidade pelo
id); a leitura de todo arquivo de dados, no validar_dados.py, nas partes do molde que o
formato usa; a base do material de fora, no base_externa.py, que usa a grade da unidade de
cada base; a conferencia dos moldes, no confere_moldes.py, com a tabela da leitura (no
lidos.py), a tabela dos destinos e o limite das aulas; a conferencia do material escrito,
no confere_material.py; a lista de trabalho de cada texto, no lista_de_trabalho.py; e o
documento das divergencias, no divergencias.py, com a citacao das fontes do
confere_cartoes.py.

Monta, na pasta de trabalho, um projeto pequeno com a pasta de scripts dada e um
projeto.json feito do modelo dado, com os caminhos dele. Tudo e sorteado, sempre igual,
porque a semente e fixa (outra vem com --semente), com nomes que nao sao os de nenhum
projeto. O formato tem o numero de partes para tratar, as fontes dos documentos, grupos,
partes da sequencia, tipos, regras de fora, marcas e documentos dos quatro tipos de molde,
com uma grade do documento com elos, unidades sem eixos proprios e com eles, unidades com
itens e sem eles (com itens, com eixos proprios e sem eles), conjuntos de unidades e de
itens (um so das unidades com itens e um so das unidades e itens que usam a grade do
documento), as aulas que tratam de unidades e de itens, abertura que recebe trechos e que nao
recebe, eixo que se divide em subtopicos e eixo que nao se divide. As bases sao de tres
unidades -- uma que usa a grade do documento, uma com grade propria no mesmo documento e uma
de um documento sem grade dele --, lidas numa fonte HTML inventada, na pasta das copias do
material de fora que o modelo da.

As analises sao de tres a cinco aulas e seguem uma forma sorteada, com os papeis dos campos
que o molde dela declara, o destino em pedacos, as vezes com um separador entre
parenteses, e o campo das paginas, em pedacos, com a fonte das paginas que ele cita. As
transcricoes inventadas, na pasta das transcricoes, sao as registradas com essa fonte (de
nomes cuja ordem natural nao e a do texto, uma com a pagina cujo numero comeca o de uma
pagina de outra, e uma que nenhum trecho cita), uma registrada com outra fonte e uma sem
registro; os pedacos do campo das paginas citam uma ou duas transcricoes da fonte, ou
nenhuma (um nome, um com um separador entre parenteses, o rotulo com uma letra colada
antes ou depois e o de uma pagina da outra fonte ou da sem registro). A tabela dos
destinos diz o que cada pedaco nomeia: uma unidade, um item ou um conjunto (cada um
escrito de um ou dois jeitos), duas unidades, ou nada. As tabelas vao gravadas com a
linha de colunas vazias no fim as vezes sem as tabulacoes delas, como a deixa o editor
que tira os espacos do fim da linha. Cada trecho e de um caso, e o caso diz, por
construcao, os documentos que cada fonte da a ele e a entrada e a parte dele em cada
documento: pelo tipo, junto de outro trecho (tambem por um conjunto), por um conjunto, pelo
caminho (e pelo destino em outro documento), num eixo da grade do documento (na unidade sem
eixos proprios ou num item de uma unidade sem eles, tambem pelo conjunto deles) ou na de
uma unidade, com a entrada da linha no lugar da do destino, so pelas regras num documento e
so pelo destino em outro, num item ou na abertura de cada familia, na abertura das
familias com itens pelo conjunto delas, a espera do assunto, marcado sem lugar, marcado com lugar pela tabela (sem
grupo, e com o grupo de outro documento, que a linha troca), marcado sem eixo, marcado com
grupo, com um pedaco sem linha, de fora pelo tipo e posto fora pela leitura (os dois com um
pedaco sem linha, que nao conta). Cada parte de molde e cada entrada tem trecho, e todos
ficam em aulas ate a ultima do limite, que vem antes da ultima das analises.

O mundo do limite junta a esse, com a ultima aula do limite, as fontes so pelas regras, um
numero de partes para tratar de 2 para cima e as aulas que tratam das entradas dele
decididas no formato (a primeira aula com lugar direto em cada uma), entradas novas: uma
tratada pela conta, uma so mencionada, uma tratada pela decisao e mencionada por outra
aula, uma que a decisao deixa sem aula, uma so com lugar indireto (pelo conjunto dela), uma
com eixos proprios e sem trecho e uma familia com um item tratado e um so mencionado;
trechos de depois da ultima aula numa entrada tratada, numa so mencionada, num item so
mencionado e na abertura da familia, e um marcado sem lugar; trechos ate a ultima aula que
o limite deixa sem lugar, um sem lugar novo, um com lugar novo numa entrada com material e
um numa sem; e trechos a que as fontes nao dao documento, sem marca e com linha na tabela da
leitura: dois de uma aula ate a ultima, com o lugar novo numa entrada com material e numa
sem, e um de depois dela.

O material escrito fica no mundo da conferencia sem avisos (com lugar para os trechos
marcados e linha para os pedacos) e com uma aula depois da ultima, com trechos nas unidades
de que uma aula ate a ultima trata: o texto de cada unidade com material e de cada aula do
documento de formas, com os codigos escondidos de cada parte, de cada item e de cada trecho,
em arquivos dentro e fora de subpastas, com blocos de codigo, codigo na linha e comentarios
que nao sao marca, a parte sem trecho as vezes fora e as que nao recebem trechos em todos os
textos ou em nenhum; e a planilha de cada texto de unidade, com os codigos dos trechos em
cartoes e a aula, nas colunas de nomes sorteados de um projeto.json a mais. O arquivo de
chamadas da uma chamada inventada a cada fonte registrada nas transcricoes, e o arquivo das
divergencias tem, numa ordem sorteada, uma divergencia com dois trechos de um texto, uma com
um deles e um de outro texto e uma com um trecho que nenhum texto tem, cada uma com uma ou
duas outras formas, e cada forma com uma ou duas chamadas e paginas das transcricoes; no
documento, as planilhas ganham a coluna da pergunta, com um cartao sem pergunta, e um cartao
com os dois trechos da primeira.

O teste confere regras, nunca uma frase pronta:
  - os moldes declaram os tipos de molde, os papeis, as formas de campo, a fonte das paginas
    de um campo e as fontes dos documentos que o teste monta;
  - o formato certo passa no molde e na leitura, e o base_externa.py roda sem erro;
  - o modelo em branco do formato (o arquivo com o nome do formato, na pasta do
    projeto.json modelo) falha na validacao so onde espera um valor -- cada texto vazio,
    cada numero abaixo do minimo e cada lista vazia que pede itens --, com um erro em cada
    lugar, e preenchido pelo molde passa;
  - o molde pede pelo menos uma parte para tratar, e cada campo do topo do formato e
    obrigatorio: sem ele, um erro so, que diz o campo;
  - um texto onde o molde pede uma lista e erro, que diz o lugar;
  - campo que o molde nao conhece, campo de outro tipo de molde (tambem a grade e os itens
    de uma unidade), campo que o tipo de molde pede e falta, tipo de molde desconhecido,
    numero de partes para tratar abaixo do minimo ou que nao e inteiro, fonte dos
    documentos que o molde nao conhece, repetida ou nenhuma, aulas que tratam numa unidade
    com itens, aula repetida entre as que tratam, e conjunto sem membros ou com membro
    repetido sao erro, que diz o lugar;
  - cada ligacao quebrada e um erro so, que diz o arquivo e o lugar: unidade em dois
    documentos, item com o id de uma unidade ou de um item de outra unidade, conjunto com
    o id de um item, membro de conjunto que o formato nao tem, de outro documento ou que e
    um conjunto, id repetido na ficha do documento ou na de uma unidade, elo com eixo que o
    documento nao tem, unidade e documento sem grade, grupo que nao existe, tipo em duas
    partes ou em duas formas, tipo e documento de onde_se_ensina que nao existem, id em
    fora e em marcas, documento que nao recebe nenhum trecho;
  - com erro no formato, a base e a conferencia dos moldes dao esse erro so, e nada e
    gravado;
  - cada unidade se acha no documento dela, e um id que nenhum documento tem nao se acha;
    os itens de cada unidade e os conjuntos de cada documento sao os deles; o id de uma
    unidade ou de um item quer dizer ela ou ele, como lugar direto, e o de um conjunto,
    cada membro, na ordem, como lugar indireto; item e conjunto nao se acham como unidade;
    um id que o formato nao tem nao quer dizer nada;
    a grade da unidade com eixos proprios sao os dela, e a da sem eles, os do documento;
    as linhas de um eixo sao os subtopicos dele, ou ele mesmo;
  - a base de cada unidade tem o titulo dela e, na ordem, um titulo para cada eixo da
    grade dela e um, mais fundo, para cada subtopico; a frase usada fica embaixo da linha
    dela; a cobertura de uma linha de outra grade e erro;
  - unidade que nenhum documento tem, e unidade de documento sem grade, sao um erro so, que
    diz a unidade, e a base dela fica so com o titulo;
  - na conferencia dos moldes, com cada valor das fontes dos documentos, cada trecho cai nos
    documentos e nas entradas e partes que o caso dele diz: a tabela das classes; quantos
    trechos cada parte de cada molde tem e de que aulas, quantos ficam junto do assunto e em
    que documentos cai cada tipo de onde_se_ensina; as aulas que tratam de cada unidade e de
    cada item (o item com o nome da unidade dele), com as partes na ordem do molde e o aviso
    de que quem decide e o formato so quando ele decide, as que so mencionam e quantos
    trechos de depois da ultima aula ficam ali; os membros de cada conjunto; as unidades so
    mencionadas; onde as fontes discordam, nos dois sentidos, pelo nome de cada fonte; e
    cada pedaco sem linha, com os trechos e as aulas;
  - o limite, pela peca dele (limite.py), e as regras dele vistas no relatorio: o trecho de
    depois da ultima aula so fica numa entrada tratada, a aula que trata pela conta diz pelo
    menos as partes pedidas, e nenhuma aula trata e so menciona a mesma entrada; as
    perguntas de prova na aula do trecho, ou nas aulas que tratam das entradas em que ele
    ficou; e cada trecho ate a ultima aula que o limite deixa sem lugar, com os lugares que
    perdeu (o documento, a entrada e a parte), ou com o lugar novo, como o trecho dessas
    aulas a que as fontes nao dao documento;
  - cada aviso esperado, e so ele: FALTA no pedaco sem linha, no trecho marcado sem lugar,
    no sem eixo, no sem entrada e no sem lugar depois do limite; ERRO na linha num documento
    que as fontes nao dao e no lugar novo numa entrada sem material; cada um diz o trecho ou
    o lugar, na tela e no relatorio; o trecho que a FALTA deixa sem lugar sai das classes de
    estudo com lugar para a dele (o sem entrada, a espera de unidade); sem FALTA nem ERRO, a
    conferencia sai com codigo 0;
  - cada linha da tabela que nao fecha, cada id da tabela dos destinos que o formato nao
    tem (com o pedaco), cada parte que nao e da entrada, cada trecho de estudo sem
    documento e sem marca que nao fica no lugar novo (que nao e FALTA, e fica a espera do
    assunto, com o grupo que o espera, ou com problema, sem ele), cada parte de molde sem
    trecho (o eixo da grade de uma unidade com a sua, so quando ela tem trecho no material)
    e cada tipo ou grupo que o formato nao tem sao ERRO, que diz o trecho ou o lugar, na
    tela e no relatorio, que e gravado;
  - cada entrada errada (a forma das analises, as regras contra ela, uma analise, a tabela
    da leitura, a tabela dos destinos, o destino que nao esta em pedacos, a ultima aula, a
    decisao com aula depois da ultima ou que nao e de analise nenhuma, um tipo de molde ou
    uma fonte que o script nao conhece, um arquivo que falta) e ERRO, que diz o que, e nada
    e gravado; as analises, a tabela dos destinos, o relatorio e as listas de trabalho fora
    da pasta protegida sao erro do projeto.json, mesmo com o que esta no caminho levado junto;
  - duas rodadas dao os mesmos arquivos;
  - no material certo, o conferidor do material nao da aviso e sai com codigo 0, e cada texto
    fica pronto, na ordem de escrita, com a aula, o documento e o nome; duas rodadas dao a
    mesma saida; com so os primeiros textos escritos, os outros ficam sem texto e sem aviso, o
    proximo a escrever e o primeiro deles, as perguntas que pedem so textos prontos ja podem
    ser escritas, e, com --unidade, o texto sem texto e FALTA, e o das perguntas diz os que
    ele pede e ainda nao estao prontos;
  - cada estrago do material da o aviso dele, com o trecho, a parte, o arquivo e a linha,
    quando os tem, e o estado de cada texto; o texto pedido que nao existe, a conferencia dos
    moldes com aviso, duas partes com o mesmo id num texto e o mesmo codigo em dois textos sao
    ERRO, sem a tabela dos textos; sem a coluna dos trechos, os cartoes nao se conferem, e,
    sem a da aula, a aula deles tambem nao;
  - no material certo, com uma unidade que nenhum texto tem e o codigo de um trecho das
    perguntas de prova nela, a lista de trabalho de cada texto, na ordem de escrita, sai com
    codigo 0 e tem o comeco (o nome, o codigo, o documento, a aula; numa unidade, as aulas
    que tratam e as que so mencionam, a planilha, com as colunas, e a prova; no texto que
    depende de outros, esses), os codigos escondidos das regioes na ordem do molde, os
    trechos de cada regiao e os que vao junto, cada um com o texto, cada campo da forma menos
    o do destino, as marcas e, so quando e assim, que ele esta ali por um conjunto, que e de
    uma aula depois da ultima, cada divergencia com o codigo dele, na ordem do arquivo, com o
    fato e o que cada forma diz e a citacao dela, a ensinada primeiro, e onde ele esta nos
    textos de que o texto depende (nunca na
    unidade que nenhum texto tem), o aviso da regiao que nao recebe trechos e da que nao tem
    nenhum, as transcricoes a ler, na ordem natural dos nomes, e os pedacos sem pagina, com os
    trechos; duas rodadas, a mesma lista;
  - o texto que depende de outros, um deles sem texto, o codigo que nenhum texto tem, o
    arquivo das divergencias que falta, fora do molde ou fora do UTF-8 e a conferencia dos
    moldes com aviso sao ERRO, e nenhuma lista e gravada; a lista do texto que nao comecou e
    gravada; na forma sem a fonte das paginas, a lista diz que nenhum campo a tem; e, com o
    campo das paginas na forma de texto, o campo inteiro de cada trecho e um pedaco;
  - o documento das divergencias sai com codigo 0 e tem um titulo de segundo nivel para cada
    divergencia, na ordem do arquivo, com a forma ensinada e as outras, na ordem, cada uma
    com o que diz e a citacao, e, so quando ha, uma linha para cada parte do material que
    trata do fato: cada linha de texto com a marca de um trecho dele, uma vez so, com o link
    para a linha, o titulo do arquivo e os nomes do item e da parte, e, depois, cada cartao
    com um trecho dele, uma vez so, com o link para a planilha, o numero e a pergunta, cada
    grupo na ordem dos caminhos e das linhas ou dos cartoes; duas rodadas, o mesmo
    documento; o --conferir, com o documento em dia, codigo 0 e, com uma linha a mais antes
    de uma parte que trata de um fato, FALTA, codigo 1, e nada gravado;
  - o arquivo das divergencias que falta, fora do molde ou fora do UTF-8, o fato repetido
    com outras maiusculas e outros espacos, o codigo de trecho que nao existe, a citacao
    com texto que nao e chamada, a chamada sem lugar, o lugar que a fonte nao tem, o arquivo
    de chamadas que falta, a planilha fora do UTF-8 e a conferencia dos moldes com aviso sao
    ERRO, que diz o que, e nada e gravado; sem divergencia, o documento sai sem titulo de
    divergencia; e, sem a coluna dos trechos, as partes do material sao so as dos textos.
O codigo de saida da rodada certa do base_externa.py nao se confere: no fim, ele roda as
referencias, que este teste nao monta. Uso:
    python3 -I teste_formato.py <pasta scripts do projeto> <projeto.json modelo> <pasta de trabalho nova> [--semente N]
Diz "0 falha(s)" quando passa; senao, uma linha FALHA para cada conferencia que nao
passou, e sai com codigo 1.
"""
import argparse
import collections
import copy
import csv
import itertools
import json
import os
import random
import re
import shutil
import string
import subprocess
import sys
from pathlib import Path


def argumentos():
    p = argparse.ArgumentParser(description="Teste dos scripts de um projeto que leem o arquivo de formato.")
    p.add_argument("scripts", type=Path, help="a pasta de scripts do projeto")
    p.add_argument("modelo", type=Path, help="o projeto.json do modelo")
    p.add_argument("trabalho", type=Path, help="uma pasta de trabalho nova")
    p.add_argument("--semente", type=int, default=1, help="a semente do sorteio")
    return p.parse_args()


ARGS = argumentos()
SCRIPTS, MODELO, TRABALHO = (a.resolve() for a in (ARGS.scripts, ARGS.modelo, ARGS.trabalho))
SORTEIO = random.Random(ARGS.semente)
PROJ = TRABALHO / "projeto"
PROJ_SCRIPTS = PROJ / SCRIPTS.name  # a pasta de scripts do projeto pequeno, com o nome da pasta dada
shutil.copytree(SCRIPTS, PROJ_SCRIPTS, ignore=shutil.ignore_patterns("__pycache__"))
sys.path.insert(0, str(PROJ_SCRIPTS))
import analises  # noqa: E402
import base_externa  # noqa: E402
import comum  # noqa: E402
import confere_material  # noqa: E402
import confere_moldes  # noqa: E402
import destinos  # noqa: E402
import divergencias  # noqa: E402
import lidos  # noqa: E402
import limite  # noqa: E402
import lista_de_trabalho  # noqa: E402
import lugares  # noqa: E402
import registrar_fonte  # noqa: E402
import relatorio  # noqa: E402
import tabela  # noqa: E402
import validar_dados  # noqa: E402

(PROJ / comum.ARQUIVO_PROJETO).write_text(MODELO.read_text(encoding="utf-8"), encoding="utf-8")
PROJETO = comum.acha_projeto(PROJ / comum.ARQUIVO_PROJETO)
ARQUIVO_FORMATO = PROJETO.caminho("formato")
TABELA_DOS_DESTINOS = PROJETO.caminho("destinos")
ESQUEMA_FORMATO = validar_dados.esquema("formato")
MOLDE = json.loads(ESQUEMA_FORMATO.read_text(encoding="utf-8"))
MOLDE_BASE = json.loads(validar_dados.esquema("base").read_text(encoding="utf-8"))
MOLDE_FORMA = json.loads(validar_dados.esquema("forma-analise").read_text(encoding="utf-8"))
RELATORIO = PROJETO.caminho("conferencia_moldes")
MATERIAL = PROJETO.caminho("material_gerado")  # a pasta dos textos e das planilhas que o conferidor do material le
DIVERGENCIAS, DOCUMENTO = PROJETO.caminho("divergencias"), PROJETO.caminho("documento_das_divergencias")
VERSAO_DIVERGENCIAS = json.loads(validar_dados.esquema("divergencias").read_text(encoding="utf-8"))["properties"][
    "versao_schema"]["const"]
VERSAO_CHAMADAS = json.loads(validar_dados.esquema("chamadas").read_text(encoding="utf-8"))["properties"][
    "versao_schema"]["const"]

# os tipos de molde de documento que o teste monta
TIPOS_DE_MOLDE = (PARTES, GRADE, FORMAS, COLUNAS) = ("partes_por_tipo", "eixos", "formas", "colunas")
# os papeis dos campos das analises, as formas de campo e as fontes dos documentos que o teste usa
PAPEIS_DO_TESTE = (TIPO, GRUPO, CAMINHO, DESTINO) = ("tipo", "grupo", "caminho", "destino")
FORMAS_DE_CAMPO = (LISTA, PEDACOS, PRESENCA, TEXTO) = ("lista", "pedacos", "presenca", "texto")
FONTES_DO_TESTE = (PELAS_REGRAS, PELO_DESTINO) = ("regras", "destino")
USA, DA_FONTE = "usa", "fonte"  # a classe da frase que vai para a base e a cobertura da linha dela
ERRO, FALTA = "ERRO", "FALTA"  # o comeco da linha do script que pede alguma coisa (README dos scripts)
LETRAS, ACENTOS = string.ascii_lowercase, "áâãçéêíóôõú"
SEPARADORES_LISTA, SEPARADORES_CAMPOS = [";", "+", "&"], [" ¦ ", " ‖ ", " // "]
SEPARADORES_TEXTO, ITENS, VAZIOS = [" :: ", " => ", " ~ "], ["- ", "* ", "• "], ["∅", "n/a", "·"]
SEPARADORES_PEDACOS = [" + ", " ^ ", " ; "]
# os casos dos trechos da conferencia dos moldes
CASOS_DOS_TRECHOS = ["tipo", "junto", "conjunto", "caminho", "grade", "propria", "linha_vence", "so_regras",
                     "unidades", "abertura", "abertura_por_conjunto", "eixo_por_conjunto", "assunto", "sem_linha",
                     "marca_sem_lugar", "marca_com_linha", "marca_com_linha_e_grupo", "marca_sem_eixo",
                     "marca_com_grupo", "fora", "lido"]
FORA_DO_MATERIAL = ("fora", "lido")  # os casos de fora: pelo tipo e pela leitura
JUNTO = None  # a parte esperada do trecho que vai junto do assunto dele, fora das partes da sequencia
DESTINOS = ("partes", "grade", "unidades")  # os documentos para onde a tabela leva o trecho que espera lugar
FALHAS = []
SORTEADAS = set()


def confere(condicao, descricao):
    if not condicao:
        FALHAS.append(descricao)
        print(f"FALHA: {descricao}")
    return condicao


def termina():
    print(f"{len(FALHAS)} falha(s)")
    sys.exit(1 if FALHAS else 0)


def aceitos(molde, *chaves):
    """Os valores que o molde aceita no lugar dado pelas chaves; nenhum, se o lugar nao diz."""
    for chave in chaves:
        molde = molde.get(chave, {})
    return molde.get("enum", [])


ORDENS = aceitos(MOLDE, "$defs", "ordem")
LADOS = aceitos(MOLDE, "$defs", "coluna", "properties", "lado")
COBERTURAS = aceitos(MOLDE_BASE, "properties", "cobertura", "additionalProperties")
CLASSES = aceitos(MOLDE_BASE, "$defs", "classe", "properties", "classe")
AFIRMACOES = aceitos(MOLDE_BASE, "$defs", "classe", "properties", "afirmacao")
COM_CAMPO = {a["if"]["properties"]["classe"]["const"] for a in MOLDE_BASE["$defs"]["classe"].get("allOf", [])}
OUTRAS_CLASSES = [c for c in CLASSES if c not in COM_CAMPO]  # as que nao pedem outro campo
OUTRAS_COBERTURAS = [c for c in COBERTURAS if c != DA_FONTE]
VERSAO_BASE = MOLDE_BASE["properties"]["versao_schema"]["const"]
PAPEIS = aceitos(MOLDE_FORMA, "$defs", "campo", "properties", "papel")
VERSAO_FORMA = MOLDE_FORMA["properties"]["versao_schema"]["const"]
FONTES = aceitos(MOLDE, "properties", "documentos_vem_de", "items")  # as fontes dos documentos do trecho
MINIMO_PARTES = MOLDE["properties"].get("partes_para_tratar", {}).get("minimum")


# ---------- o sorteio ----------

def palavra(alfabeto=LETRAS + ACENTOS, minimo=4, maximo=8):
    """Uma palavra sorteada, que nao esta dentro de nenhuma outra ja sorteada nem tem uma
    delas dentro."""
    while True:
        p = "".join(SORTEIO.choice(alfabeto) for _ in range(SORTEIO.randint(minimo, maximo)))
        if not any(p in s or s in p for s in SORTEADAS):
            SORTEADAS.add(p)
            return p


def ident():
    """Um id: so letras sem acento, porque vai no nome de arquivo, e comprido, para nao
    aparecer por acaso dentro de outro texto."""
    return palavra(LETRAS, 7, 10)


def nome():
    return " ".join(palavra() for _ in range(SORTEIO.randint(1, 3)))


def frase():
    return " ".join(palavra() for _ in range(SORTEIO.randint(3, 6))).capitalize() + "."


def ordem():
    return SORTEIO.choice(ORDENS)


def partes(minimo, maximo):
    return [{"id": ident(), "nome": nome(), "ordem": ordem()} for _ in range(SORTEIO.randint(minimo, maximo))]


def eixos():
    """De tres a cinco eixos: pelo menos um que se divide em subtopicos e um que nao se divide."""
    n = SORTEIO.randint(3, 5)
    divididos = set(SORTEIO.sample(range(n), SORTEIO.randint(1, n - 1)))
    saida = partes(n, n)
    for i in divididos:
        saida[i]["subtopicos"] = [{"id": ident(), "nome": nome()} for _ in range(SORTEIO.randint(2, 3))]
    return saida


def unidade(eixos_=None):
    return {"id": ident(), "nome": nome(), **({"eixos": eixos_} if eixos_ else {})}


def item():
    return {"id": ident(), "nome": nome()}


def tratada_em(aulas):
    """As aulas que tratam de uma entrada, sorteadas entre as dadas, sem repetir; as vezes nenhuma."""
    return SORTEIO.sample(aulas, SORTEIO.randint(0, len(aulas)))


def conjunto(membros):
    return {"id": ident(), "nome": nome(), "membros": SORTEIO.sample(membros, len(membros))}


def familias(aulas):
    """De tres a quatro unidades com eixos proprios, pelo menos duas com itens e uma sem eles,
    com as aulas que tratam da unidade sem itens e de um item de cada unidade com itens, e um
    conjunto delas com pelo menos uma unidade e um item."""
    saida = [unidade(eixos()) for _ in range(SORTEIO.randint(3, 4))]
    com_itens = set(SORTEIO.sample(range(len(saida)), SORTEIO.randint(2, len(saida) - 1)))
    for k, u in enumerate(saida):
        if k in com_itens:
            u["itens"] = [item() for _ in range(SORTEIO.randint(2, 3))]
            u["itens"][0]["tratada_em"] = tratada_em(aulas)
        else:
            u["tratada_em"] = tratada_em(aulas)
    itens_ = [i["id"] for u in saida for i in u.get("itens", [])]
    todos = [u["id"] for u in saida] + itens_
    membros = [SORTEIO.choice(itens_), SORTEIO.choice(saida)["id"]] + SORTEIO.sample(todos, SORTEIO.randint(0, 2))
    return saida, conjunto(list(dict.fromkeys(membros)))


def abertura(recebe):
    return {"id": ident(), "nome": nome(), "ordem": ordem(), "recebe_trechos": recebe}


def elo(eixos_):
    return {"id": ident(), "nome": nome(), "eixos": [e["id"] for e in SORTEIO.sample(eixos_, SORTEIO.randint(1, 2))],
            "ordem": ordem()}


def documento(molde, **campos):
    return {"id": ident(), "nome": nome(), "unidade": palavra(), "molde": molde, **campos}


def em_pedacos(itens, n):
    """Os itens em n pedacos seguidos, nenhum vazio."""
    cortes = sorted(SORTEIO.sample(range(1, len(itens)), n - 1))
    return [itens[a:b] for a, b in zip([0] + cortes, cortes + [len(itens)])]


def chaves_de_aula():
    """Chaves de tres a cinco aulas, em ordem natural: o numero da aula, ou dois numeros
    seguidos com hifen, como a aula dada em dois dias."""
    numeros_ = sorted(SORTEIO.sample(range(1, 40), SORTEIO.randint(3, 5)))
    return [f"{n}-{n + 1}" if SORTEIO.random() < 0.3 else str(n) for n in numeros_]


def ate_a(aulas, ultima):
    """As aulas ate a ultima dada, em ordem."""
    return aulas[:aulas.index(ultima) + 1]


def sorteia_formato():
    """(formato, ids): ids diz o id de cada documento pelo papel dele no teste, o de cada grupo
    pelo papel dele ("grupos") e as chaves das aulas, em ordem natural ("aulas")."""
    grupos = {papel: {"id": ident(), "nome": nome()} for papel in ("partes", "grade", "unidades", "assunto", "orfao")}
    grupos["assunto"]["pelo_assunto"] = True
    lista_de_grupos = list(grupos.values()) + [{"id": ident(), "nome": nome()} for _ in range(SORTEIO.randint(0, 1))]
    SORTEIO.shuffle(lista_de_grupos)
    sequencia = [{"id": ident(), "nome": nome(), "tipos": [nome() for _ in range(SORTEIO.randint(1, 2))],
                  "ordem": ordem()} for _ in range(SORTEIO.randint(3, 5))]
    junto = [nome() for _ in range(SORTEIO.randint(2, 3))]
    fora = [{"id": ident(), "nome": nome(), "tipos": [nome() for _ in range(SORTEIO.randint(1, 2))]}
            for _ in range(SORTEIO.randint(1, 2))]
    marcas = [{"id": ident(), "nome": nome(), "texto": nome(), "papeis": SORTEIO.sample(PAPEIS, SORTEIO.randint(1, 2))}
              for _ in range(SORTEIO.randint(1, 2))]
    da_sequencia = [t for p in sequencia for t in p["tipos"]]
    # onde_se_ensina tem um tipo de cada lugar que so esta nesse lugar -- a sequencia, os que vao
    # junto, as regras de fora e as formas de pergunta --, e tipos que os trechos usam, que estao
    # na sequencia ou nos que vao junto e numa forma de pergunta
    so_da_sequencia, so_de_junto, so_das_formas = SORTEIO.choice(da_sequencia), SORTEIO.choice(junto), nome()
    usaveis = [t for t in da_sequencia + junto if t not in (so_da_sequencia, so_de_junto)]
    embaralhados = SORTEIO.sample(usaveis, len(usaveis))
    verbos = [nome(), nome()]  # menos verbos que formas: o mesmo verbo pode voltar
    formas = [{"verbo": SORTEIO.choice(verbos), "tipos": pedaco_, "ordem": ordem()}
              for pedaco_ in em_pedacos(embaralhados, SORTEIO.randint(2, min(3, len(embaralhados))))]
    SORTEIO.choice(formas)["tipos"].append(so_das_formas)
    da_grade = eixos()
    aulas = chaves_de_aula()
    ultima = SORTEIO.choice(aulas)
    ate_a_ultima = ate_a(aulas, ultima)
    sem_eixos_com_itens = unidade()  # os itens dela usam a grade do documento
    sem_eixos_com_itens["itens"] = [item() for _ in range(SORTEIO.randint(1, 2))]
    das_partes, da_ficha = [unidade(), unidade()], [unidade(), unidade(eixos()), sem_eixos_com_itens]
    # o conjunto das entradas que usam a grade do documento: o lugar dele e um eixo dela
    da_grade_do_documento = conjunto([da_ficha[0]["id"]] + [i["id"] for i in sem_eixos_com_itens["itens"]])
    das_partes[0]["tratada_em"] = tratada_em(ate_a_ultima)
    das_familias, conjunto_das_familias = familias(ate_a_ultima)
    das_com_itens = conjunto([u["id"] for u in das_familias if u.get("itens")])  # o lugar dele e a abertura
    docs = {
        "partes": documento(PARTES, grupos=[grupos["partes"]["id"]], caminhos=[], unidades=das_partes,
                            conjuntos=[conjunto([u["id"] for u in das_partes])]),
        "casos": documento(PARTES, grupos=[], caminhos=[ident()], casos=partes(2, 4)),
        "grade": documento(GRADE, grupos=[grupos["grade"]["id"]], caminhos=[], abertura=[abertura(False)],
                           eixos=da_grade, elos=[elo(da_grade) for _ in range(SORTEIO.randint(2, 3))],
                           unidades=da_ficha, conjuntos=[conjunto([u["id"] for u in da_ficha]), da_grade_do_documento]),
        "unidades": documento(GRADE, grupos=[grupos["unidades"]["id"]], caminhos=[], abertura=[abertura(True)],
                              unidades=das_familias, conjuntos=[conjunto_das_familias, das_com_itens]),
        "formas": documento(FORMAS, todos=True, pergunta=partes(2, 3), formas=formas),
        "colunas": documento(COLUNAS, todos=True, colunas=[{"id": ident(), "lado": SORTEIO.choice(LADOS),
                                                           "ordem": ordem()} for _ in range(SORTEIO.randint(2, 4))]),
    }
    lista = list(docs.values())
    SORTEIO.shuffle(lista)
    ids = [d["id"] for d in lista]
    onde = {t: SORTEIO.sample(ids, SORTEIO.randint(1, 2))
            for t in (so_da_sequencia, so_de_junto, SORTEIO.choice(fora)["tipos"][0], so_das_formas)}
    # os tipos que os trechos usam se ensinam, pelo formato, em outro documento de conteudo que nao o
    # de partes por tipo, onde os trechos de cada um deles tambem caem
    outros = [d["id"] for d in lista if not d.get("todos") and d is not docs["partes"]]
    onde.update({t: SORTEIO.sample(outros, 1) for t in SORTEIO.sample(usaveis, SORTEIO.randint(1, 2))})
    formato = {"versao_schema": MOLDE["properties"]["versao_schema"]["const"],
               "cursos": [nome() for _ in range(SORTEIO.randint(1, 3))], "disciplina": nome(), "nivel": nome(),
               "idioma": palavra(), "ultima_aula": ultima,
               "partes_para_tratar": SORTEIO.randint(MINIMO_PARTES, MINIMO_PARTES + 3),
               "documentos_vem_de": SORTEIO.sample(FONTES, SORTEIO.randint(1, len(FONTES))), "grupos": lista_de_grupos,
               "partes_por_tipo": sequencia, "tipos_junto": junto, "fora": fora, "marcas": marcas,
               "onde_se_ensina": onde, "documentos": lista}
    papeis = {papel: d["id"] for papel, d in docs.items()}
    papeis.update(grupos={papel: g["id"] for papel, g in grupos.items()}, aulas=aulas)
    return formato, papeis


def pelo_id(formato, d):
    return next(x for x in formato["documentos"] if x["id"] == d)


def doc(formato, ids, papel):
    return pelo_id(formato, ids[papel])


def indice(formato, ids, papel):
    return formato["documentos"].index(doc(formato, ids, papel))


def com_eixos(d):
    return next(u for u in d["unidades"] if u.get("eixos"))


def sem_eixos(d):
    return next(u for u in d["unidades"] if not u.get("eixos"))


def linhas(eixo):
    """As linhas da grade que o eixo da: os subtopicos dele, ou ele mesmo, quando nao se divide."""
    return eixo.get("subtopicos") or [eixo]


def ids_da_unidade(u):
    """O id da unidade e os dos itens dela."""
    return {u["id"]} | {i["id"] for i in u.get("itens", [])}


def unidades_e_itens(formato):
    """[(documento, unidade, item ou None)] de cada unidade e de cada item do formato, na ordem
    dele."""
    return [(d, u, i) for d in formato["documentos"] for u in d.get("unidades", [])
            for i in [None] + u.get("itens", [])]


def unidade_e_item(formato, d, i):
    """(unidade, item ou None) do id dado, no documento dado: a unidade com o id, ou o item com
    ele e a unidade dele; ({}, None), com o id vazio, no documento que nao lista unidades."""
    return next(((u, x) for doc_, u, x in unidades_e_itens(formato) if doc_["id"] == d and (x or u)["id"] == i),
                ({}, None))


def entidade(formato, d, i):
    """A unidade ou o item com o id dado, no documento dado."""
    u, x = unidade_e_item(formato, d, i)
    return x or u


def grade_da(d, u):
    """A grade da unidade no documento: os eixos dela, ou os do documento."""
    return u.get("eixos") or d.get("eixos", [])


# ---------- rodar e guardar ----------

def escreve(arquivo, dados):
    arquivo.parent.mkdir(parents=True, exist_ok=True)
    arquivo.write_text(json.dumps(dados, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")


def escreve_tsv(arquivo, cabecalho, linhas_):
    """Grava a tabela; a linha com as ultimas colunas vazias vai as vezes sem as tabulacoes
    delas, como a deixa o editor que tira os espacos do fim da linha."""
    arquivo.parent.mkdir(parents=True, exist_ok=True)
    sep = tabela.SEPARADOR
    escritas = [sep.join(linha).rstrip(sep) if SORTEIO.random() < 0.5 else sep.join(linha) for linha in linhas_]
    arquivo.write_text("\n".join([sep.join(cabecalho)] + escritas) + "\n", encoding="utf-8")


def roda_tela(script, *args):
    """(codigo de saida, linhas da tela) de um script da pasta de scripts do projeto pequeno."""
    r = subprocess.run([sys.executable, "-I", "-B", str(PROJ_SCRIPTS / script), *args], cwd=PROJ,
                       capture_output=True, text=True)
    return r.returncode, (r.stdout + r.stderr).splitlines()


def roda(script, *args):
    """(codigo de saida, [linhas ERRO]) de um script da pasta de scripts do projeto pequeno."""
    codigo, tela = roda_tela(script, *args)
    return codigo, [linha for linha in tela if linha.startswith(ERRO)]


def roda_base():
    return roda("base_externa.py", "--projeto", str(PROJ / comum.ARQUIVO_PROJETO))


def roda_conferencia(projeto=None):
    return roda_tela("confere_moldes.py", "--projeto", str(projeto or PROJ / comum.ARQUIVO_PROJETO))


def valida(arquivo):
    return roda("validar_dados.py", str(arquivo), "--schema", str(ESQUEMA_FORMATO))


def gravados():
    """{arquivo: bytes} de cada arquivo do projeto pequeno, fora os scripts e o formato, que o
    teste escreve."""
    return {p: p.read_bytes() for p in sorted(PROJ.rglob("*"))
            if p.is_file() and PROJ_SCRIPTS not in p.parents and p != ARQUIVO_FORMATO}


def preenche(valor, molde, trocados, caminho="$"):
    """O valor do modelo em branco preenchido pelo molde dele, com o caminho de cada valor
    trocado anotado em trocados, como a validacao o escreve: cada texto vazio com uma palavra
    sorteada; cada numero abaixo do minimo do molde, com um numero sorteado a partir dele; e
    cada lista vazia que o molde pede com itens, com valores sorteados entre os que ele aceita."""
    molde = validar_dados.resolve(molde, MOLDE)
    if isinstance(valor, dict):
        return {k: preenche(v, molde.get("properties", {}).get(k, {}), trocados, f"{caminho}.{k}")
                for k, v in valor.items()}
    if isinstance(valor, list):
        valores = validar_dados.resolve(molde.get("items", {}), MOLDE).get("enum", [])
        if not valor and molde.get("minItems") and valores:
            trocados.append(caminho)
            return SORTEIO.sample(valores, SORTEIO.randint(molde["minItems"], len(valores)))
        return [preenche(v, molde.get("items", {}), trocados, f"{caminho}[{i}]") for i, v in enumerate(valor)]
    if valor == "":
        trocados.append(caminho)
        return palavra()
    if validar_dados.tipo_confere(valor, "number") and valor < molde.get("minimum", valor):
        trocados.append(caminho)
        return SORTEIO.randint(molde["minimum"], molde["minimum"] + 3)
    return valor


def titulos(texto):
    """[(numero da linha, linha)] dos titulos do texto."""
    return [(n, linha) for n, linha in enumerate(texto.splitlines()) if linha.startswith("#")]


def fundura(titulo):
    return len(titulo) - len(titulo.lstrip("#"))


# ---------- a fonte e as bases ----------

def fonte_inventada():
    """(lugar, {codigo: frase}): uma fonte HTML inventada na pasta das copias do material de
    fora, com uma frase por paragrafo, e as frases que o base_externa.py le nela."""
    chave = ident().upper()
    fonte = PROJETO.caminho("fontes_externas") / f"{chave}.html"
    frases = [frase() for _ in range(SORTEIO.randint(4, 6))]
    fonte.parent.mkdir(parents=True, exist_ok=True)
    fonte.write_text("<html><body>" + "".join(f"<p>{f}</p>" for f in frases) + "</body></html>", encoding="utf-8")
    lugar = {"fonte": chave, "arquivo": fonte.relative_to(PROJ).as_posix()}
    lidas = {c: f for _, _, fs in base_externa.partes_do_lugar(lugar, PROJ) for c, f in fs}
    confere(sorted(lidas.values()) == sorted(frases), f"cada parágrafo da fonte inventada é uma frase: {lidas}")
    return lugar, lidas


def base_vazia(item_, lugar, lidas):
    """Os dados da base de uma unidade sem frase usada e sem cobertura."""
    return {"versao_schema": VERSAO_BASE, "item": item_, "lugares": [lugar], "juntar": [], "cobertura": {},
            "classes": {c: {"classe": SORTEIO.choice(OUTRAS_CLASSES)} for c in sorted(lidas)}}


def base_com_grade(item_, eixos_, lugar, lidas):
    """(dados, linha usada, frase usada): a base de uma unidade com cada linha da grade
    marcada, uma linha que a fonte cobre e uma frase usada nela."""
    todas = [linha for e in eixos_ for linha in linhas(e)]
    usada, codigo = SORTEIO.choice(todas), SORTEIO.choice(sorted(lidas))
    dados = base_vazia(item_, lugar, lidas)
    dados["cobertura"] = {linha["id"]: SORTEIO.choice(OUTRAS_COBERTURAS) for linha in todas}
    dados["cobertura"][usada["id"]] = DA_FONTE
    dados["classes"][codigo] = {"classe": USA, "subtopico": usada["id"], "afirmacao": SORTEIO.choice(AFIRMACOES)}
    return dados, usada, lidas[codigo]


def bases_de(formato, ids):
    """[(unidade, eixos da grade dela)] das tres unidades com base: a que usa a grade do
    documento, a com grade propria no mesmo documento e a de um documento sem grade dele."""
    da_grade, das_unidades = doc(formato, ids, "grade"), doc(formato, ids, "unidades")["unidades"][0]
    return [(sem_eixos(da_grade), da_grade["eixos"]), (com_eixos(da_grade), com_eixos(da_grade)["eixos"]),
            (das_unidades, das_unidades["eixos"])]


def confere_base(unidade_, eixos_, usada, frase_usada):
    gravada = PROJETO.caminho_com("base_externa", unidade_["id"])
    if not confere(gravada.exists(), f"a base de {unidade_['id']} é gravada"):
        return
    texto = gravada.read_text(encoding="utf-8")
    ts, linhas_do_texto = titulos(texto), texto.splitlines()
    esperados = [(parte, e) for e in eixos_ for parte in [e] + e.get("subtopicos", [])]  # (parte, eixo dela)
    confere(len(ts) == 1 + len(esperados) and unidade_["nome"] in ts[0][1]
            and all(parte["nome"] in t for (_, t), (parte, _) in zip(ts[1:], esperados)),
            f"a base de {unidade_['id']} tem o título dela e um por eixo e subtópico da grade dela, na ordem: {ts}")
    fundos = [fundura(t) for _, t in ts[1:]]
    do_eixo = [next(k for k, (p, _) in enumerate(esperados) if p is e) for _, e in esperados]
    confere(len(fundos) == len(esperados) and all(fundos[k] > fundos[j] for k, ((p, e), j)
                                                  in enumerate(zip(esperados, do_eixo)) if p is not e),
            f"na base de {unidade_['id']}, o título do subtópico fica mais fundo que o do eixo dele: {ts}")
    n0 = next((n for n, t in ts if usada["nome"] in t), None)
    n1 = next((n for n, _ in ts if n0 is not None and n > n0), len(linhas_do_texto))
    confere(n0 is not None and sum(frase_usada in linha for linha in linhas_do_texto[n0 + 1:n1]) == 1
            and sum(frase_usada in linha for linha in linhas_do_texto) == 1,
            f"na base de {unidade_['id']}, a frase usada fica embaixo da linha dela, uma vez só")


def com_base_a_mais(dados):
    """(codigo, erros, titulos da base) da rodada com uma base a mais, que sai depois dela."""
    entrada, saida = PROJETO.caminho_com("bases", dados["item"]), PROJETO.caminho_com("base_externa", dados["item"])
    escreve(entrada, dados)
    codigo, erros = roda_base()
    ts = titulos(saida.read_text(encoding="utf-8")) if saida.exists() else []
    entrada.unlink()
    saida.unlink(missing_ok=True)
    return codigo, erros, ts


# ---------- o mundo da conferencia: a forma, os destinos e os casos dos trechos ----------

def sorteia_forma(formato):
    """A forma das analises: os quatro papeis em campos de nomes sorteados -- o destino em
    pedacos, com um ou dois separadores --, mais um ou dois campos sem papel, o campo das
    paginas, em pedacos, com a fonte das paginas que ele cita, e o caminho com os valores que
    os documentos usam e um a mais."""
    caminhos = [c for d in formato["documentos"] for c in d.get("caminhos", [])] + [ident()]
    campos = [{"nome": ident(), "forma": LISTA, "papel": TIPO, "separadores": [SORTEIO.choice(SEPARADORES_LISTA)]},
              {"nome": ident(), "forma": LISTA, "papel": GRUPO, "separadores": [SORTEIO.choice(SEPARADORES_LISTA)]},
              {"nome": ident(), "forma": PRESENCA, "papel": CAMINHO, "valores": caminhos},
              {"nome": ident(), "forma": PEDACOS, "papel": DESTINO,
               "separadores": SORTEIO.sample(SEPARADORES_PEDACOS, SORTEIO.randint(1, 2))},
              {"nome": ident(), "forma": PEDACOS, "separadores": SORTEIO.sample(SEPARADORES_PEDACOS, 2),
               "fonte": ident().upper()}]
    campos += [{"nome": ident(), "forma": TEXTO} for _ in range(SORTEIO.randint(1, 2))]
    SORTEIO.shuffle(campos)
    prefixo = ident() + SORTEIO.choice(["-", "_"])
    return {"versao_schema": VERSAO_FORMA, "arquivos": f"{prefixo}*{SORTEIO.choice(['.md', '.txt'])}",
            "prefixo_arquivo": prefixo, "prefixo_titulo": SORTEIO.choice(["#", "%"]),
            "prefixo_slide": f"{SORTEIO.choice(['##', '@@'])} {palavra(LETRAS)} ", "marca_item": SORTEIO.choice(ITENS),
            "separador_texto": SORTEIO.choice(SEPARADORES_TEXTO),
            "separador_campos": SORTEIO.choice(SEPARADORES_CAMPOS), "vazio": SORTEIO.choice(VAZIOS),
            "nota_sem_campos": palavra(), "campos": campos}


def separadores_do_destino(forma):
    return next(c for c in forma["campos"] if c.get("papel") == DESTINO)["separadores"]


def campo_das_paginas(forma):
    """O campo da forma com a fonte das paginas que ele cita."""
    return next(c for c in forma["campos"] if "fonte" in c)


def pedaco(m):
    """Um pedaco de destino sorteado: um nome, as vezes com um texto entre parenteses que tem
    um separador do destino dentro e conta como parte do pedaco."""
    texto = nome()
    if SORTEIO.random() < 0.4:
        texto += f" ({palavra()}{SORTEIO.choice(separadores_do_destino(m['forma']))}{palavra()})"
    return texto


def nomeia(m, ids_):
    """Da a cada id um ou dois pedacos que o nomeiam, com as linhas deles na tabela dos destinos."""
    for i in ids_:
        m["vocabulario"][i] = [pedaco(m) for _ in range(SORTEIO.randint(1, 2))]
        m["destinos"] += [(p, i) for p in m["vocabulario"][i]]


def ids_nomeaveis(formato):
    """Os ids de cada unidade e de cada item do formato, e depois os de cada conjunto, na ordem dele."""
    return ([(i or u)["id"] for _, u, i in unidades_e_itens(formato)]
            + [c["id"] for d in formato["documentos"] for c in d.get("conjuntos", [])])


def unidades_do_mundo(m):
    """As duas unidades do documento de partes no formato sorteado (o mundo do limite poe outras
    depois delas)."""
    return doc(m["formato"], m["ids"], "partes")["unidades"][:2]


def unidade_do_mundo(m):
    """O id de uma das duas unidades do documento de partes, sorteada."""
    return SORTEIO.choice(unidades_do_mundo(m))["id"]


def sorteia_destinos(m):
    """Os pedacos do mundo e a tabela dos destinos: os pedacos de cada unidade, item e conjunto;
    um que nomeia as duas unidades do documento de partes ("dois"); dois que nao nomeiam nada; e
    o texto de cada marca, que tambem nao nomeia nada."""
    m["vocabulario"], m["destinos"] = {}, []
    nomeia(m, ids_nomeaveis(m["formato"]))
    m["dois"], m["nada"] = pedaco(m), [pedaco(m) for _ in range(2)]
    m["destinos"] += [(m["dois"], u["id"]) for u in unidades_do_mundo(m)]
    m["destinos"] += [(p, "") for p in m["nada"]] + [(mk["texto"], "") for mk in m["formato"]["marcas"]]
    SORTEIO.shuffle(m["destinos"])


Transcricao = collections.namedtuple("Transcricao", "arquivo chave rotulos")
# uma transcricao inventada: o arquivo; a chave da fonte registrada nela, ou None, sem registro; e o rotulo de cada
# pagina


def grava_transcricao(arquivo, rotulos, chave):
    """Grava uma transcricao com uma secao por rotulo, na convencao das transcricoes, e, com a chave, o registro de uma
    fonte inventada na pasta protegida, pelo registrar_fonte.py."""
    corpo = [linha for k, r in enumerate(rotulos, 1) for linha in (f"## {r} (arquivo p. {k})", "", frase(), "")]
    arquivo.write_text("\n".join(corpo), encoding="utf-8")
    if chave:
        fonte = PROJETO.caminho("material_base") / ident() / f"{ident()}.html"
        fonte.parent.mkdir(parents=True)
        fonte.write_text(f"<html><body><p>{frase()}</p></body></html>", encoding="utf-8")
        registrar_fonte.registra(arquivo, fonte, chave, PROJ)
    return Transcricao(arquivo, chave, rotulos)


def sorteia_paginas(m):
    """As transcricoes inventadas, na pasta das transcricoes, e os pedacos do campo das paginas. As registradas com a
    fonte do campo tem nomes com numeros de um e de dois algarismos (a ordem natural nao e a do texto); a primeira tem
    a pagina cujo numero comeca o da unica pagina da segunda; a ultima nao e citada. Ha tambem uma registrada com outra
    fonte e uma sem registro, cada uma com paginas que os pedacos citam. Os pedacos: os que citam uma pagina de cada
    transcricao da fonte que e citada (um entre parenteses), um que cita duas, e os que nao citam nenhuma -- um nome,
    um com um separador do campo entre parenteses, o rotulo com uma letra colada antes, o rotulo com uma letra colada
    depois e os rotulos da outra fonte e da sem registro. Guarda m["paginas"], [Transcricao], e m["pedacos"],
    [(texto, arquivos que ele cita)]."""
    campo, pasta, prefixo = campo_das_paginas(m["forma"]), PROJETO.caminho("gerados"), palavra(LETRAS)
    pasta.mkdir(parents=True, exist_ok=True)
    rotulo = comum.ROTULO_PAGINA.format
    numeros_ = sorted([SORTEIO.randint(2, 9), SORTEIO.randint(10, 19)] + SORTEIO.sample(range(30, 60), 2))
    inicio = SORTEIO.randint(2, 9)
    soltas = iter(SORTEIO.sample(range(100, 999), 20))
    paginas_ = [[inicio], [10 * inicio + SORTEIO.randint(0, 9)]] + [[next(soltas) for _ in range(SORTEIO.randint(1, 3))]
                                                                      for _ in numeros_[2:]]
    da_fonte = [grava_transcricao(pasta / f"{prefixo}{n}.md", [rotulo(p) for p in ps], campo["fonte"])
                for n, ps in zip(numeros_, paginas_)]
    alheias = [grava_transcricao(pasta / f"{ident()}.md", [rotulo(next(soltas)) for _ in range(2)], chave)
               for chave in (ident().upper(), None)]
    citadas = da_fonte[:-1]
    pedacos_ = [(f"{palavra()}, {r}", {t.arquivo}) for t in citadas for r in SORTEIO.sample(t.rotulos, 1)]
    pedacos_.append((f"{palavra()} ({SORTEIO.choice(citadas[0].rotulos)})", {citadas[0].arquivo}))
    uma, outra = citadas[:2]  # a de nome com um algarismo e a de nome com dois, que o texto poe antes dela
    pedacos_.append((f"{palavra()}, {uma.rotulos[0]} e {outra.rotulos[-1]}", {uma.arquivo, outra.arquivo}))
    pedacos_ += [(nome(), set()), (f"{nome()} ({palavra()}{campo['separadores'][0]}{palavra()})", set()),
                 (f"{palavra()}, {SORTEIO.choice(LETRAS)}{citadas[0].rotulos[0]}", set()),
                 (f"{palavra()}, {citadas[0].rotulos[0]}{SORTEIO.choice(LETRAS)}", set())]
    pedacos_ += [(f"{palavra()}, {SORTEIO.choice(t.rotulos)}", set()) for t in alheias]
    m["paginas"], m["pedacos"] = da_fonte + alheias, pedacos_


def tipos_do_mundo(formato, ids):
    """(com parte, junto): os tipos que os trechos usam, cada um com uma forma de pergunta --
    os de uma parte da sequencia e os que vao junto de outro trecho."""
    com_forma = {t for f in doc(formato, ids, "formas")["formas"] for t in f["tipos"]}
    return ([t for p in formato["partes_por_tipo"] for t in p["tipos"] if t in com_forma],
            [t for t in formato["tipos_junto"] if t in com_forma])


def partes_dos_tipos(tipos, formato):
    """As partes da sequencia dos tipos, na ordem do formato; JUNTO, quando nenhum tem parte."""
    return [p["id"] for p in formato["partes_por_tipo"] if set(tipos) & set(p["tipos"])] or [JUNTO]


def das_fontes(caso, regras, destino):
    caso["fontes"] = {PELAS_REGRAS: regras, PELO_DESTINO: destino}


def nomeando(caso, m, ids_):
    """O destino do caso nomeia os ids, cada um por um dos pedacos dele."""
    caso["pedacos"] += [SORTEIO.choice(m["vocabulario"][i]) for i in ids_]


def na_linha(caso, d, unidade_, parte):
    caso["linhas"].append((d, unidade_, parte))


def no_documento_de_partes(caso, m, alvo=None, pelo_conjunto=False):
    """O caso cai no documento de partes pelo grupo, e o destino nomeia a entrada: a unidade
    dada (ou uma sorteada), as duas pelo pedaco que nomeia as duas, ou, pelo conjunto (o dado,
    ou o primeiro do documento), cada membro, como lugar indireto."""
    f, ids = m["formato"], m["ids"]
    d, partes_ = doc(f, ids, "partes"), partes_dos_tipos(caso["tipos"], f)
    caso["grupos"] = [ids["grupos"]["partes"]]
    if pelo_conjunto:
        conj = alvo or d["conjuntos"][0]
        nomeando(caso, m, [conj["id"]])
        entradas = [(mb, False) for mb in conj["membros"]]
    elif alvo is None and SORTEIO.random() < 0.3:
        caso["pedacos"].append(m["dois"])
        entradas = [(u["id"], True) for u in unidades_do_mundo(m)]
    else:
        u = alvo or unidade_do_mundo(m)
        nomeando(caso, m, [u])
        entradas = [(u, True)]
    caso["no_doc"][ids["partes"]] = [(u, p, direto) for u, direto in entradas for p in partes_]
    das_fontes(caso, [ids["partes"]], [ids["partes"]])


def pela_linha(caso, m, papel, unidade_, parte, entrada, nomeada):
    """O caso cai pelo grupo no documento do papel dado (o grupo tem o mesmo papel), com a linha
    da unidade e da parte dadas, e o destino nomeia 'nomeada', do mesmo documento: o lugar dele
    e a entrada dada, direto."""
    ids = m["ids"]
    caso["grupos"] = [ids["grupos"][papel]]
    na_linha(caso, ids[papel], unidade_, parte)
    nomeando(caso, m, [nomeada])
    caso["no_doc"][ids[papel]] = [(entrada, parte, True)]
    das_fontes(caso, [ids[papel]], [ids[papel]])


def na_grade(caso, m, unidade_, eixo, nomeada):
    """No documento de grade, com a linha da unidade e do eixo: a entrada e a da linha, que vale
    no lugar da que o destino nomeia."""
    pela_linha(caso, m, "grade", unidade_, eixo, unidade_, nomeada)


def na_familia(caso, m, familia, parte, item_=None):
    """No documento das familias, com a linha da familia e da parte (um eixo ou a abertura): a
    entrada e a familia, ou o item dado dela, que o destino nomeia."""
    pela_linha(caso, m, "unidades", familia["id"], parte, item_ or familia["id"], item_ or familia["id"])


def lugar_lido(caso, m, qual=None):
    """Da ao caso uma linha da tabela da leitura com o lugar dele, num dos DESTINOS: no
    documento de partes, uma unidade; no de grade, a unidade sem eixos proprios e um eixo; no
    das familias, uma familia e um eixo dela -- na familia com itens, um item, pelo id dele."""
    f, ids = m["formato"], m["ids"]
    qual = qual or SORTEIO.choice(DESTINOS)
    if qual == "partes":
        u = unidade_do_mundo(m)
        lugar = (ids["partes"], u, "")
        lugares_ = [(u, p, True) for p in partes_dos_tipos(caso["tipos"], f)]
    elif qual == "grade":
        d = doc(f, ids, "grade")
        lugar = (ids["grade"], sem_eixos(d)["id"], SORTEIO.choice(d["eixos"])["id"])
        lugares_ = [(lugar[1], lugar[2], True)]
    else:
        fam = SORTEIO.choice(doc(f, ids, "unidades")["unidades"])
        entrada = SORTEIO.choice(fam["itens"])["id"] if fam.get("itens") else fam["id"]
        lugar = (ids["unidades"], entrada, SORTEIO.choice(fam["eixos"])["id"])
        lugares_ = [(entrada, lugar[2], True)]
    na_linha(caso, *lugar)
    caso["no_doc"][lugar[0]] = lugares_


def monta_caminho(caso, m, alvo):
    """Pelo caminho, no documento dos casos (que nao lista unidades); o destino nomeia uma
    unidade do documento de partes."""
    f, ids = m["formato"], m["ids"]
    caso["grupos"], caso["caminhos"] = [ids["grupos"]["orfao"]], list(doc(f, ids, "casos")["caminhos"])
    u = unidade_do_mundo(m)
    nomeando(caso, m, [u])
    partes_ = partes_dos_tipos(caso["tipos"], f)
    caso["no_doc"] = {ids["casos"]: [("", p, True) for p in partes_], ids["partes"]: [(u, p, True) for p in partes_]}
    das_fontes(caso, [ids["casos"]], [ids["partes"]])


def monta_so_regras(caso, m, alvo):
    """Pelo grupo, num eixo da grade do documento, com a linha; o destino nomeia so uma unidade
    do documento de partes."""
    f, ids = m["formato"], m["ids"]
    d, p = doc(f, ids, "grade"), unidade_do_mundo(m)
    u = sem_eixos(d)["id"]
    pela_linha(caso, m, "grade", u, SORTEIO.choice(d["eixos"])["id"], u, p)
    caso["no_doc"][ids["partes"]] = [(p, parte, True) for parte in partes_dos_tipos(caso["tipos"], f)]
    das_fontes(caso, [ids["grade"]], [ids["partes"]])


def monta_unidades(caso, m, alvo):
    """Pelo grupo, num eixo de uma familia, com a linha da familia; na familia com itens, o
    destino nomeia o item. 'alvo' e (familia, eixo, item)."""
    fam, eixo, item_ = alvo or (SORTEIO.choice(doc(m["formato"], m["ids"], "unidades")["unidades"]), None, None)
    eixo = eixo or SORTEIO.choice(fam["eixos"])["id"]
    if fam.get("itens") and item_ is None:
        item_ = SORTEIO.choice(fam["itens"])["id"]
    na_familia(caso, m, fam, eixo, item_)


def monta_abertura(caso, m, alvo):
    d = doc(m["formato"], m["ids"], "unidades")
    na_familia(caso, m, alvo or SORTEIO.choice(d["unidades"]), d["abertura"][0]["id"])


def monta_eixo_por_conjunto(caso, m, alvo):
    """Num eixo da grade do documento, pela linha do conjunto das entradas que a usam, que o destino tambem nomeia: o
    lugar em cada uma e indireto."""
    ids = m["ids"]
    d = doc(m["formato"], ids, "grade")
    conj, eixo = d["conjuntos"][1], SORTEIO.choice(d["eixos"])["id"]
    caso["grupos"] = [ids["grupos"]["grade"]]
    na_linha(caso, ids["grade"], conj["id"], eixo)
    nomeando(caso, m, [conj["id"]])
    caso["no_doc"][ids["grade"]] = [(mb, eixo, False) for mb in conj["membros"]]
    das_fontes(caso, [ids["grade"]], [ids["grade"]])


def monta_abertura_por_conjunto(caso, m, alvo):
    """Na abertura das familias com itens, pela linha do conjunto delas, que o destino tambem nomeia: o lugar em cada
    uma e indireto."""
    ids = m["ids"]
    d = doc(m["formato"], ids, "unidades")
    conj, abertura_ = d["conjuntos"][1], d["abertura"][0]["id"]
    caso["grupos"] = [ids["grupos"]["unidades"]]
    na_linha(caso, ids["unidades"], conj["id"], abertura_)
    nomeando(caso, m, [conj["id"]])
    caso["no_doc"][ids["unidades"]] = [(mb, abertura_, False) for mb in conj["membros"]]
    das_fontes(caso, [ids["unidades"]], [ids["unidades"]])


def monta_grade(caso, m, alvo):
    """Num eixo da grade do documento, com a linha da entrada, que o destino nomeia: 'alvo' e
    (entrada, eixo), a entrada sendo a unidade sem eixos proprios ou um item de uma unidade sem
    eles; sem ele, essa unidade e um eixo sorteado."""
    d = doc(m["formato"], m["ids"], "grade")
    entrada, eixo = alvo or (sem_eixos(d)["id"], SORTEIO.choice(d["eixos"])["id"])
    na_grade(caso, m, entrada, eixo, entrada)


def monta_propria(caso, m, alvo):
    u = com_eixos(doc(m["formato"], m["ids"], "grade"))
    na_grade(caso, m, u["id"], alvo or SORTEIO.choice(u["eixos"])["id"], u["id"])


def monta_linha_vence(caso, m, alvo):
    d = doc(m["formato"], m["ids"], "grade")
    na_grade(caso, m, sem_eixos(d)["id"], SORTEIO.choice(d["eixos"])["id"], com_eixos(d)["id"])


def monta_espera(caso, m, alvo):
    """A espera do assunto: o grupo que espera, o destino que nao nomeia nada e a linha da leitura."""
    caso["grupos"], caso["assunto"] = [m["ids"]["grupos"]["assunto"]], True
    caso["pedacos"].append(SORTEIO.choice(m["nada"]))
    lugar_lido(caso, m, alvo)


def monta_sem_documento(caso, m, alvo):
    """Sem documento pelas fontes: so o grupo que nenhum documento recebe, sem marca, e o
    destino que nao nomeia nada."""
    caso["grupos"], caso["pedacos"] = [m["ids"]["grupos"]["orfao"]], [SORTEIO.choice(m["nada"])]
    das_fontes(caso, [], [])


def monta_marca_sem_eixo(caso, m, alvo):
    """Marcado, pelo grupo no documento de grade, com o destino que nomeia a unidade e sem a
    linha que da o eixo: falta o eixo."""
    ids = m["ids"]
    u = sem_eixos(doc(m["formato"], ids, "grade"))["id"]
    caso["grupos"] = [ids["grupos"]["grade"]]
    nomeando(caso, m, [u])
    caso["no_doc"][ids["grade"]], caso["falta_no_doc"][ids["grade"]] = [], [u]
    das_fontes(caso, [ids["grade"]], [ids["grade"]])


def monta_nada(caso, m, alvo):
    caso["pedacos"].append(SORTEIO.choice(m["nada"]))


def monta_marca_com_linha(caso, m, alvo):
    monta_nada(caso, m, alvo)
    lugar_lido(caso, m, alvo)


def monta_marca_com_linha_e_grupo(caso, m, alvo):
    """Marcado, pelo grupo no documento de partes, com o destino que nomeia uma unidade dele, e
    com a linha da leitura no documento de grade: os documentos dele sao os da linha."""
    no_documento_de_partes(caso, m, alvo)
    lugar_lido(caso, m, "grade")


def monta_fora(caso, m, alvo):
    """De fora pelo tipo, com um pedaco do destino sem linha, que nao conta: o trecho de fora nao
    vai para o material."""
    caso["grupos"] = SORTEIO.sample([m["ids"]["grupos"]["partes"]], SORTEIO.randint(0, 1))
    caso["pedacos"].append(pedaco(m))


def monta_lido(caso, m, alvo):
    caso["grupos"] = [m["ids"]["grupos"]["partes"]]
    na_linha(caso, lidos.FORA, caso["regra"], "")
    caso["pedacos"].append(pedaco(m))


def monta_sem_linha(caso, m, alvo):
    no_documento_de_partes(caso, m, alvo)
    caso["sem_linha"].append(pedaco(m))


MONTA = {  # o que cada caso faz com o trecho: monta(caso, mundo, alvo)
    "tipo": lambda c, m, a: no_documento_de_partes(c, m, a), "junto": lambda c, m, a: no_documento_de_partes(c, m, a),
    "conjunto": lambda c, m, a: no_documento_de_partes(c, m, a, pelo_conjunto=True), "caminho": monta_caminho,
    "grade": monta_grade, "propria": monta_propria, "linha_vence": monta_linha_vence, "so_regras": monta_so_regras,
    "unidades": monta_unidades, "abertura": monta_abertura, "abertura_por_conjunto": monta_abertura_por_conjunto,
    "eixo_por_conjunto": monta_eixo_por_conjunto,
    "assunto": monta_espera, "sem_linha": monta_sem_linha,
    "sem_documento": monta_sem_documento, "marca_sem_lugar": monta_nada, "marca_com_linha": monta_marca_com_linha,
    "marca_com_linha_e_grupo": monta_marca_com_linha_e_grupo, "marca_sem_eixo": monta_marca_sem_eixo,
    "marca_com_grupo": lambda c, m, a: no_documento_de_partes(c, m, a), "fora": monta_fora, "lido": monta_lido,
}
COM_TIPOS_DE_PARTE = ("tipo", "conjunto", "caminho", "so_regras", "sem_linha", "marca_com_grupo",
                      "marca_com_linha_e_grupo")


def sorteia_caso(caso, m, tipos=None, alvo=None):
    """Um trecho do caso dado, com o que a conferencia tem de achar dele, por construcao: o
    texto, os tipos, os grupos, os caminhos, as marcas (o id e o papel em que o texto dela
    vai), os pedacos do destino e os que nao tem linha, as linhas da tabela da leitura
    (documento, unidade, parte), a regra de fora, o texto dos campos sem papel, os pedacos do
    campo das paginas e o separador deles, se ele espera o assunto, os documentos que cada
    fonte da ("fontes") e, em cada documento em que ele pode cair, os lugares dele --
    (entrada, parte, direto) -- ("no_doc") e o que falta ali ("falta_no_doc"). 'tipos' troca
    os tipos sorteados; 'alvo' diz a entrada, ou o eixo."""
    f, com_parte, junto = m["formato"], m["com_parte"], m["junto"]
    paginas = m["campo_paginas"]
    novo = {"caso": caso, "texto": frase(), "tipos": SORTEIO.sample(com_parte + junto, SORTEIO.randint(1, 2)),
            "grupos": [], "caminhos": [], "marcas": [], "linhas": [], "regra": None, "pedacos": [], "sem_linha": [],
            "assunto": False, "fontes": {PELAS_REGRAS: [], PELO_DESTINO: []}, "no_doc": {}, "falta_no_doc": {},
            "separador": SORTEIO.choice(separadores_do_destino(m["forma"])),
            "extras": {c["nome"]: palavra() for c in m["forma"]["campos"] if "papel" not in c and c["nome"] != paginas},
            "paginas": [p for p, _ in SORTEIO.sample(m["pedacos"], SORTEIO.randint(0, 3))],
            "separador_das_paginas": SORTEIO.choice(campo_das_paginas(m["forma"])["separadores"])}
    if caso in COM_TIPOS_DE_PARTE:
        novo["tipos"] = SORTEIO.sample(com_parte, SORTEIO.randint(1, 2)) + SORTEIO.sample(junto, SORTEIO.randint(0, 1))
    elif caso == "junto":
        novo["tipos"] = SORTEIO.sample(junto, 1)
    elif caso in FORA_DO_MATERIAL:
        regra = SORTEIO.choice(f["fora"])
        novo["regra"] = regra["id"]
        if caso == "fora":
            novo["tipos"] = SORTEIO.sample(regra["tipos"], SORTEIO.randint(1, len(regra["tipos"])))
    novo["tipos"] = novo["tipos"] if tipos is None else tipos
    if caso.startswith("marca"):
        novo["marcas"] = [(mk["id"], SORTEIO.choice(mk["papeis"]))
                          for mk in SORTEIO.sample(f["marcas"], SORTEIO.randint(1, len(f["marcas"])))]
    MONTA[caso](novo, m, alvo)
    return novo


def casos_do_mundo(m):
    """Os trechos do mundo: um de cada caso; um a espera do assunto para cada destino; um que
    vai junto do assunto por um conjunto; um de cada tipo que os trechos usam e que
    onde_se_ensina diz; os que cada forma de pergunta, cada eixo de cada grade, cada unidade e
    cada item pedem para nao ficarem vazios; e outros sorteados."""
    f, ids, usaveis = m["formato"], m["ids"], m["com_parte"] + m["junto"]
    casos = [sorteia_caso(c, m) for c in CASOS_DOS_TRECHOS]
    casos += [sorteia_caso("assunto", m, alvo=qual) for qual in DESTINOS]
    casos.append(sorteia_caso("conjunto", m, tipos=SORTEIO.sample(m["junto"], 1)))
    tipos = [t for t in f["onde_se_ensina"] if t in usaveis]
    tipos += [SORTEIO.choice([t for t in forma["tipos"] if t in usaveis]) for forma in doc(f, ids, "formas")["formas"]]
    casos += [sorteia_caso("junto" if t in m["junto"] else "tipo", m, tipos=[t]) for t in tipos]
    casos += [sorteia_caso("tipo", m, alvo=u["id"]) for u in doc(f, ids, "partes")["unidades"]]
    da_grade = doc(f, ids, "grade")
    casos += [sorteia_caso("grade", m, alvo=(sem_eixos(da_grade)["id"], e["id"])) for e in da_grade["eixos"]]
    casos += [sorteia_caso("grade", m, alvo=(i["id"], SORTEIO.choice(da_grade["eixos"])["id"]))
              for u in da_grade["unidades"] if not u.get("eixos") for i in u.get("itens", [])]
    casos += [sorteia_caso("propria", m, alvo=e["id"]) for e in com_eixos(da_grade)["eixos"]]
    for fam in doc(f, ids, "unidades")["unidades"]:
        itens_ = [i["id"] for i in fam.get("itens", [])]
        casos += [sorteia_caso("unidades", m, alvo=(fam, e["id"], SORTEIO.choice(itens_) if itens_ else None))
                  for e in fam["eixos"]]
        casos += [sorteia_caso("unidades", m, alvo=(fam, None, i)) for i in itens_]
        casos.append(sorteia_caso("abertura", m, alvo=fam))
    return casos + [sorteia_caso(SORTEIO.choice(CASOS_DOS_TRECHOS), m) for _ in range(SORTEIO.randint(3, 10))]


def texto_do_campo(caso, campo, m):
    """O texto de um campo do trecho na forma das analises, com o texto de cada marca no campo
    do papel dela (entre parenteses, num campo em lista, onde nao conta; como um pedaco a mais,
    no destino); no campo das paginas, os pedacos dele."""
    forma, papel = m["forma"], campo.get("papel")
    textos = {mk["id"]: mk["texto"] for mk in m["formato"]["marcas"]}
    no_papel = [textos[marca] for marca, p in caso["marcas"] if p == papel]
    if papel in (TIPO, GRUPO):
        valor = campo["separadores"][0].join(caso["tipos"] if papel == TIPO else caso["grupos"]) or forma["vazio"]
        return valor + "".join(f" ({t})" for t in no_papel)
    if papel == CAMINHO:
        return (" ".join(caso["caminhos"]) or forma["vazio"]) + "".join(f" ({t})" for t in no_papel)
    if papel == DESTINO:
        return caso["separador"].join(caso["pedacos"] + caso["sem_linha"] + no_papel) or forma["vazio"]
    if campo["nome"] == m["campo_paginas"]:
        return caso["separador_das_paginas"].join(caso["paginas"]) or forma["vazio"]
    return caso["extras"][campo["nome"]]


def linha_do_trecho(caso, m):
    """A linha do trecho na forma das analises: o texto e cada campo (texto_do_campo)."""
    forma = m["forma"]
    campos = [f"{c['nome']}: {texto_do_campo(caso, c, m)}" for c in forma["campos"]]
    return forma["marca_item"] + caso["texto"] + forma["separador_texto"] + forma["separador_campos"].join(campos)


def arquivo_da_aula(m, aula):
    forma = m["forma"]
    return PROJETO.caminho("analises_das_aulas") / f"{forma['prefixo_arquivo']}{aula}{forma['arquivos'].split('*')[1]}"


def escreve_tabela(linhas_, cabecalho=lidos.CABECALHO):
    escreve_tsv(PROJETO.caminho("lugares_lidos"), cabecalho, linhas_)


def escreve_destinos(linhas_, cabecalho=destinos.CABECALHO):
    escreve_tsv(TABELA_DOS_DESTINOS, cabecalho, linhas_)


def escreve_mundo(m):
    """Grava o formato, a forma das analises, a analise de cada aula, a tabela da leitura e a
    tabela dos destinos."""
    escreve(ARQUIVO_FORMATO, m["formato"])
    escreve(PROJETO.caminho("forma_analise"), m["forma"])
    for aula in m["ids"]["aulas"]:
        texto, slide = [f"{m['forma']['prefixo_titulo']} {m['titulos'][aula]}"], None
        for caso in m["casos"]:
            if caso["aula"] == aula:
                if caso["slide"] != slide:
                    slide = caso["slide"]
                    texto.append(f"{m['forma']['prefixo_slide']}{slide}")
                texto.append(linha_do_trecho(caso, m))
        arquivo = arquivo_da_aula(m, aula)
        arquivo.parent.mkdir(parents=True, exist_ok=True)
        arquivo.write_text("\n".join(texto) + "\n", encoding="utf-8")
    escreve_tabela(m["tabela"])
    escreve_destinos(m["destinos"])


def le_ids(m):
    """Grava o mundo, le o id de cada trecho pelo analises.py, com a ordem da leitura, e grava
    de novo, com a tabela da leitura numa ordem sorteada."""
    m["tabela"] = []
    escreve_mundo(m)
    trechos, _, _ = analises.ler_analises(PROJETO.caminho("analises_das_aulas"), m["forma"])
    pelo_texto = {t["texto"]: t["id"] for t in trechos}
    confere(len(trechos) == len(m["casos"]) and all(c["texto"] in pelo_texto for c in m["casos"]),
            "cada trecho sorteado é lido nas análises")
    for caso in m["casos"]:
        caso["id"] = pelo_texto.get(caso["texto"], "")
    m["ordem"] = [t["id"] for t in trechos]
    m["tabela"] = [(caso["id"], *linha) for caso in m["casos"] for linha in caso["linhas"]]
    SORTEIO.shuffle(m["tabela"])
    escreve_mundo(m)


def sem_decisoes(formato):
    """Uma copia do formato sem as aulas que tratam das unidades e dos itens."""
    f = copy.deepcopy(formato)
    for _, u, i in unidades_e_itens(f):
        (i or u).pop("tratada_em", None)
    return f


def com_todos_os_pedacos(casos, m):
    """Poe cada pedaco do campo das paginas que nenhum trecho de estudo tem num trecho de estudo sorteado."""
    de_estudo = [c for c in casos if c["caso"] not in FORA_DO_MATERIAL]
    usados = {p for c in de_estudo for p in c["paginas"]}
    for p, _ in m["pedacos"]:
        if p not in usados:
            SORTEIO.choice(de_estudo)["paginas"].append(p)


def sorteia_mundo(formato, ids):
    """O mundo da conferencia dos moldes: o formato sem as aulas que tratam, a forma das
    analises, as transcricoes inventadas e os pedacos do campo das paginas, os pedacos do
    destino e a tabela dos destinos, os trechos, cada um numa aula ate a ultima do limite (que
    vem antes da ultima das analises) e num slide, com o id de cada um lido pelo analises.py,
    e a tabela da leitura."""
    f = sem_decisoes(formato)
    m = {"formato": f, "ids": ids, "forma": sorteia_forma(f)}
    m["campo_paginas"] = campo_das_paginas(m["forma"])["nome"]
    m["com_parte"], m["junto"] = tipos_do_mundo(f, ids)
    sorteia_paginas(m)
    sorteia_destinos(m)
    casos = casos_do_mundo(m)
    com_todos_os_pedacos(casos, m)
    SORTEIO.shuffle(casos)
    aulas = ids["aulas"]
    m["ultima_do_limite"] = SORTEIO.choice(aulas[1:-1])  # duas aulas ate ela, pelo menos, e uma depois
    ate = ate_a(aulas, m["ultima_do_limite"])
    m["casos"], m["titulos"] = casos, {aula: nome() for aula in aulas}
    for aula, pedaco_ in zip(ate, em_pedacos(casos, len(ate))):
        slide = SORTEIO.randint(1, 5)
        for k, caso in enumerate(pedaco_):
            slide += SORTEIO.randint(1, 3) if k and SORTEIO.random() < 0.5 else 0
            caso["aula"], caso["slide"] = aula, slide
    le_ids(m)
    return m


def com_fontes(m, fontes):
    """O mundo com a ultima aula na ultima das analises, o menor numero de partes para tratar e
    as fontes dadas: como cada entrada tem lugar direto, o limite nao tira lugar nenhum."""
    v = copy.deepcopy(m)
    v["formato"].update(ultima_aula=v["ids"]["aulas"][-1], partes_para_tratar=MINIMO_PARTES,
                        documentos_vem_de=list(fontes))
    return v


def valores_das_fontes():
    """Cada valor que as fontes dos documentos podem ter: as listas sem repetir, com pelo menos uma."""
    return [list(p) for k in range(1, len(FONTES) + 1) for p in itertools.permutations(FONTES, k)]


def sem_avisos(m):
    """Uma copia do mundo sem FALTA nem ERRO na conferencia dos moldes: o trecho marcado sem lugar ganha uma linha da
    tabela da leitura num dos DESTINOS; o marcado sem eixo, a linha da unidade sem eixos proprios do documento de grade,
    num eixo dela; e cada pedaco sem linha, a linha dele na tabela dos destinos, que nao nomeia nada."""
    v = copy.deepcopy(m)
    d = doc(v["formato"], v["ids"], "grade")
    for caso in v["casos"]:
        if caso["caso"] == "marca_sem_lugar":
            lugar_lido(caso, v)
        elif caso["caso"] == "marca_sem_eixo":
            u, eixo = sem_eixos(d)["id"], SORTEIO.choice(d["eixos"])["id"]
            na_linha(caso, d["id"], u, eixo)
            caso["no_doc"][d["id"]], caso["falta_no_doc"] = [(u, eixo, True)], {}
        v["destinos"] += [(p, "") for p in caso["sem_linha"]]
        caso["pedacos"], caso["sem_linha"] = caso["pedacos"] + caso["sem_linha"], []
    v["tabela"] = [(caso["id"], *linha) for caso in v["casos"] for linha in caso["linhas"]]
    SORTEIO.shuffle(v["tabela"])
    return v


def com_aula_depois(m):
    """Uma copia do mundo com uma aula a mais, depois de todas as das analises e da ultima do limite, com um trecho de
    cada uma das duas unidades do documento de partes, pelo tipo: o limite os deixa nelas, porque uma aula ate a ultima
    trata de cada uma, e eles vao para as perguntas de prova dessas aulas."""
    v = copy.deepcopy(m)
    nova = str(max(int(n) for a in v["ids"]["aulas"] for n in re.findall(r"\d+", a)) + 1)
    v["ids"]["aulas"].append(nova)
    v["titulos"][nova] = nome()
    for slide, u in enumerate(unidades_do_mundo(v), 1):
        caso = sorteia_caso("tipo", v, alvo=u["id"])
        caso["aula"], caso["slide"] = nova, slide
        v["casos"].append(caso)
    le_ids(v)
    return v


# ---------- o mundo do limite ----------

def primeiras_aulas(m):
    """{(documento, id): aula} de cada unidade sem itens e de cada item com lugar direto no
    mundo: a primeira aula, em ordem, com lugar direto nele."""
    f, aulas = m["formato"], m["ids"]["aulas"]
    decidiveis = {(d["id"], (i or u)["id"]) for d, u, i in unidades_e_itens(f) if i or not u.get("itens")}
    ate = set(ate_a(aulas, f["ultima_aula"]))
    saida = {}
    for caso in sorted(m["casos"], key=lambda c: aulas.index(c["aula"])):
        if caso["caso"] not in FORA_DO_MATERIAL:
            for d, ent, _, direto in caminho_do_caso(caso, f, ate)[1]:
                if direto and (d, ent) in decidiveis:
                    saida.setdefault((d, ent), caso["aula"])
    return saida


def lugar_novo(caso, m, unidade_):
    """Da ao caso uma linha da tabela da leitura no documento de grade, que as fontes dele nao
    dao: o lugar novo dele, na unidade dada e num eixo da grade dela."""
    d = doc(m["formato"], m["ids"], "grade")
    eixo = SORTEIO.choice(grade_da(d, unidade_))["id"]
    na_linha(caso, d["id"], unidade_["id"], eixo)
    caso["no_doc"][d["id"]] = [(unidade_["id"], eixo, True)]


def mundo_do_limite(m):
    """O mundo do limite (o comeco deste arquivo): o da conferencia, com a ultima aula do
    limite, as fontes so pelas regras, as aulas que tratam de cada unidade e de cada item dele
    decididas -- a primeira aula com lugar direto ali --, um numero de partes para tratar de 2
    para cima e entradas novas, com os trechos que poem a prova as regras do limite."""
    v = copy.deepcopy(m)
    f, ids, aulas = v["formato"], v["ids"], v["ids"]["aulas"]
    f.update(ultima_aula=v["ultima_do_limite"], documentos_vem_de=[PELAS_REGRAS], partes_para_tratar=MINIMO_PARTES)
    for (d, i), aula in primeiras_aulas(v).items():
        entidade(f, d, i)["tratada_em"] = [aula]
    ate = ate_a(aulas, f["ultima_aula"])
    depois = aulas[len(ate):]
    das_partes, da_grade, das_familias = (doc(f, ids, papel) for papel in DESTINOS)
    novas = {papel: unidade() for papel in ("trata", "menciona", "decidida", "nunca", "indireta")}
    das_partes["unidades"] += novas.values()
    so_indireto = conjunto([novas["indireta"]["id"]])
    das_partes["conjuntos"].append(so_indireto)
    sem_trecho, fam = unidade(eixos()), unidade(eixos())
    fam["itens"] = [item(), item()]
    da_grade["unidades"].append(sem_trecho)
    das_familias["unidades"].append(fam)
    nomeia(v, [x["id"] for x in [*novas.values(), so_indireto, sem_trecho, fam, *fam["itens"]]])
    um_por_parte = {}  # um tipo com forma de cada parte da sequencia
    for t in v["com_parte"]:
        um_por_parte.setdefault(partes_dos_tipos([t], f)[0], t)
    n = SORTEIO.randint(max(2, MINIMO_PARTES), min(len(um_por_parte), len(fam["eixos"])))
    f["partes_para_tratar"] = n
    (l1, l2), d1, t = SORTEIO.sample(ate, 2), SORTEIO.choice(depois), SORTEIO.choice(v["com_parte"])
    novas["decidida"]["tratada_em"], novas["nunca"]["tratada_em"] = [l1], []
    proximo = {a: max([c["slide"] for c in v["casos"] if c["aula"] == a] + [0]) + 1 for a in aulas}

    def caso_novo(tipo_de_caso, aula, tipos=None, alvo=None):
        c = sorteia_caso(tipo_de_caso, v, tipos=tipos, alvo=alvo)
        c["aula"], c["slide"] = aula, proximo[aula]
        proximo[aula] += 1
        v["casos"].append(c)
        return c
    for papel in ("trata", "nunca"):
        for t_ in SORTEIO.sample(sorted(um_por_parte.values()), n):
            caso_novo("tipo", l1, [t_], novas[papel]["id"])
    for t_ in SORTEIO.sample(sorted(um_por_parte.values()), n):
        caso_novo("conjunto", l1, [t_], so_indireto)
    for papel in ("menciona", "decidida"):
        caso_novo("tipo", l1, [t], novas[papel]["id"])
    caso_novo("tipo", l2, [t], novas["decidida"]["id"])
    for papel in ("trata", "menciona", "decidida"):
        caso_novo("tipo", d1, [t], novas[papel]["id"])
    for u in (sem_eixos(da_grade), sem_trecho):
        lugar_novo(caso_novo("tipo", l1, [t], novas["menciona"]["id"]), v, u)
    for aula, u in ((l1, sem_eixos(da_grade)), (l1, sem_trecho), (d1, sem_eixos(da_grade))):
        lugar_novo(caso_novo("sem_documento", aula, [t]), v, u)
    tratado, mencionado = (i["id"] for i in fam["itens"])
    for e in fam["eixos"]:
        caso_novo("unidades", l1, alvo=(fam, e["id"], tratado))
    for aula in (l1, d1):
        caso_novo("unidades", aula, alvo=(fam, SORTEIO.choice(fam["eixos"])["id"], mencionado))
    caso_novo("abertura", d1, alvo=fam)
    caso_novo("marca_sem_lugar", d1)
    le_ids(v)
    return v


# ---------- o que a conferencia tem de achar ----------

def caminho_do_caso(caso, f, ate):
    """(documentos, postos, pendentes, faltas) do caso antes do limite: os documentos das fontes
    que o formato diz, ou os da tabela da leitura, no marcado que tem linha nela e no que espera
    o assunto; os postos, (documento, entrada, parte, direto), nesses documentos; os documentos
    em que so a tabela o poe -- no caso a que as fontes nao dao documento, sem marca e sem o
    assunto, os da tabela, que sao o do lugar novo, quando ele e de uma aula ate a ultima --;
    e, para cada falta, o documento, ou None no trecho marcado sem documento de uma aula ate a
    ultima."""
    ordem_ = [d["id"] for d in f["documentos"]]
    pelas_fontes = [d for d in ordem_ if any(d in caso["fontes"][x] for x in f["documentos_vem_de"])]
    na_tabela = list(dict.fromkeys(d for d, _, _ in caso["linhas"]))
    if pelas_fontes and not (caso["marcas"] and na_tabela):
        documentos, pendentes = pelas_fontes, [d for d in na_tabela if d not in pelas_fontes]
    elif caso["marcas"] or caso["assunto"]:
        documentos, pendentes = na_tabela, []
    else:
        documentos, pendentes = [], na_tabela if caso["aula"] in ate else []
    postos = [(d, *lugar) for d in documentos for lugar in caso["no_doc"].get(d, [])]
    faltas = [d for d in documentos for _ in caso["falta_no_doc"].get(d, [])]
    if not documentos and caso["marcas"] and caso["aula"] in ate:
        faltas.append(None)
    return documentos, postos, pendentes, faltas


def itens_e_decisoes(formato):
    """({(documento, item): (documento, unidade)}, {(documento, id): aulas que tratam}) do formato."""
    itens_, decisoes = {}, {}
    for d, u, i in unidades_e_itens(formato):
        x = i or u
        if i:
            itens_[(d["id"], i["id"])] = (d["id"], u["id"])
        if "tratada_em" in x:
            decisoes[(d["id"], x["id"])] = x["tratada_em"]
    return itens_, decisoes


def nomes_das_marcas(caso, f):
    postas = {x for x, _ in caso["marcas"]}
    return [mk["nome"] for mk in f["marcas"] if mk["id"] in postas]


def guarda_esperado(caso, postos, e, f):
    """Poe o caso no material esperado: nos postos dele, com os tipos, e, no posto que so e
    indireto, entre os que estao ali por um conjunto; nas perguntas de prova, na aula dele ou
    nas aulas que tratam das entradas em que ele ficou, em cada forma com um tipo dele; e no
    cartao."""
    i = caso["id"]
    for d, ent, p, direto in postos:
        e["lugares"][d][(ent, p)].add(i)
        if not direto and (d, ent, p, True) not in postos:
            e["por_conjunto"][d][(ent, p)].add(i)
        for t in caso["tipos"]:
            e["tipos"][d][t].add(i)
    das_perguntas = [caso["aula"]] if caso["aula"] in e["ate"] else e["limite"].perguntas.get(i, [])
    for d in f["documentos"]:
        if d["molde"] == FORMAS:
            for aula in das_perguntas:
                for n, forma in enumerate(d["formas"], 1):
                    if set(caso["tipos"]) & set(forma["tipos"]):
                        e["lugares"][d["id"]][(aula, n)].add(i)
        elif d["molde"] == COLUNAS:
            e["lugares"][d["id"]][("", "")].add(i)
    e["classes"][("estudo",)] += 1


def esperado(m):
    """O que a conferencia tem de achar no mundo m, pelo formato dele (a ultima aula, as partes
    para tratar, as fontes e as decisoes) e pelo que cada caso diz: as classes; os postos de
    cada trecho antes do limite; o limite, pela peca dele; os lugares de cada documento no
    material ({documento: {(entrada, parte): ids}}, a aula nas perguntas de prova) e, entre eles,
    os que estao num lugar por um conjunto (na mesma forma); os tipos dos trechos postos em cada
    documento; os avisos ([(id ou None, o que a linha tem de dizer)]); os trechos sem lugar
    depois do limite, com os postos que perderam; onde as fontes discordam; os pedacos sem
    linha; e o caso de cada id."""
    f, aulas = m["formato"], m["ids"]["aulas"]
    caso_de = {c["id"]: c for c in m["casos"]}
    e = {"ate": set(ate_a(aulas, f["ultima_aula"])), "classes": collections.Counter(), "postos": {},
         "erros": [], "faltas": [], "perdidos": {}, "caso": caso_de, "sem_linha": {},
         "discordam": {x: {} for x in FONTES_DO_TESTE},
         "lugares": collections.defaultdict(lambda: collections.defaultdict(set)),
         "por_conjunto": collections.defaultdict(lambda: collections.defaultdict(set)),
         "tipos": collections.defaultdict(lambda: collections.defaultdict(set))}
    casos, pendentes, sem_documento = [caso_de[i] for i in m["ordem"]], {}, set()
    for caso in casos:
        i = caso["id"]
        if caso["caso"] in FORA_DO_MATERIAL:
            e["classes"][(caso["caso"], caso["regra"])] += 1
            continue
        for p in caso["sem_linha"]:
            e["sem_linha"].setdefault(p, []).append(i)
        for x in FONTES_DO_TESTE:
            das_outras = {d for y in FONTES_DO_TESTE if y != x for d in caso["fontes"][y]}
            for d in caso["fontes"][x]:
                if d not in das_outras:
                    e["discordam"][x].setdefault(d, []).append(i)
        documentos, postos, pendentes[i], faltas = caminho_do_caso(caso, f, e["ate"])
        e["faltas"] += [(i, [d] if d else nomes_das_marcas(caso, f)) for d in faltas]
        if postos:
            e["postos"][i] = postos
        elif caso["marcas"]:
            primeira = next(mk["id"] for mk in f["marcas"] if mk["id"] in {x for x, _ in caso["marcas"]})
            e["classes"][("depois",) if not documentos and caso["aula"] not in e["ate"] else ("marca", primeira)] += 1
        elif not documentos and not caso["assunto"]:
            sem_documento.add(i)
    itens_, decisoes = itens_e_decisoes(f)
    lim = e["limite"] = limite.aplicar(
        [limite.Lugar(i, caso_de[i]["aula"], (d, ent), p, direto) for i, ps in e["postos"].items()
         for d, ent, p, direto in ps], itens_, aulas, f["ultima_aula"], f["partes_para_tratar"], decisoes)
    ficam = {(lugar.trecho, lugar.entrada, lugar.parte) for lugar in lim.ficam}
    for caso in casos:
        i = caso["id"]
        if caso["caso"] in FORA_DO_MATERIAL:
            continue
        postos = [p for p in e["postos"].get(i, []) if (i, p[:2], p[2]) in ficam]
        if not postos and (i in lim.sem_lugar_ate or i in sem_documento) and pendentes[i]:
            for d in pendentes[i]:
                for ent, p, direto in caso["no_doc"].get(d, []):
                    if itens_.get((d, ent), (d, ent)) in lim.com_material:
                        postos.append((d, ent, p, direto))
                    else:
                        e["erros"].append((i, [ent]))
        else:
            e["erros"] += [(i, [d]) for d in pendentes[i]]
        if postos:
            guarda_esperado(caso, postos, e, f)
        elif i in sem_documento:
            e["erros"].append((i, [lugares.SEM_DOCUMENTO]))
            e["classes"][("problema", lugares.SEM_DOCUMENTO)] += 1
        elif i in lim.sem_lugar_ate:
            e["perdidos"][i] = e["postos"][i]
            e["faltas"].append((i, []))
            e["classes"][("limite",)] += 1
        elif i in e["postos"]:
            e["classes"][("depois",)] += 1
    return e


def em(lugares_do_documento, partes_=None, entradas=None):
    """Os ids dos trechos dos lugares dados que estao nas partes e nas entradas dadas (em todas,
    sem elas)."""
    return {i for (e, p), ids in lugares_do_documento.items()
            if (partes_ is None or p in partes_) and (entradas is None or e in entradas) for i in ids}


# ---------- a leitura do relatorio ----------

def celulas(linha):
    return [c.strip().replace("\\|", "|") for c in re.split(r"(?<!\\)\|", linha)[1:-1]]


def linhas_de_tabela(linhas_do_texto):
    """As celulas de cada linha de tabela, sem as linhas de alinhamento."""
    return [celulas(linha) for linha in linhas_do_texto
            if linha.startswith("|") and not re.fullmatch(r"\|(\s*:?-+:?\s*\|)+", linha)]


def tabelas_do(texto):
    """As celulas de cada linha de tabela do texto inteiro."""
    return linhas_de_tabela(texto.splitlines())


def nomes_dos_documentos(formato):
    return {d["id"]: d["nome"] for d in formato["documentos"]}


def tem_as_classes(texto, classes, formato):
    """Se o relatorio tem a tabela das classes com os trechos dados em cada uma."""
    return "\n".join(relatorio.tabela_das_classes(classes, formato)) in texto


def secao(texto, nome_):
    """As linhas da secao de segundo nivel do relatorio cujo titulo tem o nome dado."""
    saida, dentro = [], False
    for linha in texto.splitlines():
        if linha.startswith("## "):
            dentro = nome_ in linha
        elif dentro:
            saida.append(linha)
    return saida


def tabela_depois(texto, marca):
    """As celulas das linhas da tabela logo depois da primeira linha que tem a marca, sem o
    cabecalho: nenhuma, quando o que vem depois dela, fora as linhas em branco, nao e tabela."""
    linhas_ = texto.splitlines()
    n = next((k for k, linha in enumerate(linhas_) if marca in linha), len(linhas_))
    resto = list(itertools.dropwhile(lambda linha: not linha.strip(), linhas_[n + 1:]))
    return linhas_de_tabela(list(itertools.takewhile(lambda linha: linha.startswith("|"), resto)))[1:]


def numeros(linha):
    return [int(n) for n in re.findall(r"(?<![\w-])\d+(?![\w-])", linha)]


def tem_id(linha, i):
    return re.search(rf"(?<![\w/-]){re.escape(i)}(?![\w/-])", linha) is not None


def no_topo(texto, separador):
    """Os pedacos do texto entre os separadores que ficam fora dos parenteses, sem os espacos."""
    saida, nivel, atual = [], 0, ""
    for ch in texto:
        nivel += (ch == "(") - (ch == ")")
        if ch == separador and nivel == 0:
            saida.append(atual.strip())
            atual = ""
        else:
            atual += ch
    return saida + [atual.strip()]


def comeco(celula):
    """(comeco, resto) de uma celula de aulas: o que vem antes de ':', fora dos parenteses -- o
    aviso que a celula pode ter antes das aulas --, e o que vem depois; sem ':', o comeco e
    vazio e o resto e a celula."""
    antes = celula.split("(")[0]
    if ":" not in antes:
        return "", celula
    k = antes.index(":")
    return celula[:k], celula[k + 1:]


def aulas_da_celula(celula, aulas):
    """[(aula, [nomes entre parenteses depois dela])] de uma celula de aulas, ou None quando um
    pedaco dela nao e de aula nenhuma e nao e a celula vazia; o comeco da celula nao conta."""
    _, celula = comeco(celula)
    saida = []
    for pedaco_ in no_topo(celula, ","):
        aula, _, resto = pedaco_.partition("(")
        saida.append((aula.strip(), no_topo(resto.rstrip(")"), ";") if resto else []))
    if [a for a, _ in saida if a in aulas] or len(saida) != 1:
        return saida if all(a in aulas for a, _ in saida) else None
    return []


def aulas_de(ids, m, e):
    return ", ".join(a for a in m["ids"]["aulas"] if any(e["caso"][i]["aula"] == a for i in ids))


def nome_da_coisa(f, d, i):
    """O nome da unidade ou do item com o id dado no documento; o do documento, com o id vazio."""
    return entidade(f, d, i)["nome"] if i else pelo_id(f, d)["nome"]


# ---------- a secao de cada tipo de molde ----------

def confere_partes(d, sec, m, e):
    """A secao de um documento de partes por tipo: cada parte com trecho, com os tipos, quantos
    trechos, de que aulas e a ordem, e nenhuma sem trecho; quantos ficam junto; os casos."""
    lugares, tabela = e["lugares"][d["id"]], linhas_de_tabela(sec)
    for p in m["formato"]["partes_por_tipo"]:
        ids = em(lugares, {p["id"]})
        esperada = [[p["nome"], "; ".join(p["tipos"]), str(len(ids)), aulas_de(ids, m, e), p["ordem"]]] if ids else []
        confere([c for c in tabela if c[0] == p["nome"]] == esperada,
                f"{d['id']}: a parte {p['id']}, com {len(ids)} trecho(s), das aulas certas")
    junto = em(lugares, {JUNTO})
    com_os_tipos = [linha for linha in sec if all(t in linha for t in m["formato"]["tipos_junto"])]
    confere([numeros(linha) for linha in com_os_tipos] == ([[len(junto)]] if junto else []),
            f"{d['id']}: os {len(junto)} trecho(s) que ficam junto do assunto: {com_os_tipos}")
    confere(all(any(c[0] == caso_["nome"] for c in tabela) for caso_ in d.get("casos", [])),
            f"{d['id']}: as partes de cada caso")


def confere_grade(d, sec, m, e):
    """A secao de um documento com grade: quantos trechos cada eixo da grade do documento tem,
    nas entradas que a usam, e cada elo; cada unidade com eixos proprios, com o total e cada
    eixo, nela e nos itens dela; a abertura, com o total e o de cada unidade, quando recebe
    trechos."""
    lugares, tabela, lista = e["lugares"][d["id"]], linhas_de_tabela(sec), d.get("unidades", [])
    usam = {""}.union(*(ids_da_unidade(u) for u in lista if not u.get("eixos")))
    for eixo in d.get("eixos", []):
        n = len(em(lugares, {eixo["id"]}, usam))
        confere([eixo["nome"], str(n), eixo["ordem"]] in tabela, f"{d['id']}: o eixo {eixo['id']} com {n} trecho(s)")
    nomes = {eixo["id"]: eixo["nome"] for eixo in d.get("eixos", [])}
    for elo_ in d.get("elos", []):
        n = len(em(lugares, set(elo_["eixos"]), usam))
        achados = [c[1:] for c in tabela if c[0].endswith(elo_["nome"])]
        confere(achados == [["; ".join(nomes[i] for i in elo_["eixos"]), str(n), elo_["ordem"]]],
                f"{d['id']}: o elo {elo_['id']}, com os eixos dele e {n} trecho(s): {achados}")
    for u in lista:
        if u.get("eixos"):
            cabeca = [linha for linha in sec if linha.startswith("#") and u["nome"] in linha]
            n = len(em(lugares, None, ids_da_unidade(u)))
            confere([numeros(linha) for linha in cabeca] == [[n]], f"{d['id']}: a unidade {u['id']}, com {n} trecho(s)")
            for eixo in u["eixos"]:
                n = len(em(lugares, {eixo["id"]}, ids_da_unidade(u)))
                confere([eixo["nome"], str(n), eixo["ordem"]] in tabela,
                        f"{d['id']}: o eixo {eixo['id']} da unidade {u['id']}, com {n} trecho(s)")
    for a in d.get("abertura", []):
        achadas = [linha for linha in sec if a["nome"] in linha]
        if a["recebe_trechos"]:
            certo = (len(achadas) == 1 and numeros(achadas[0])[:1] == [len(em(lugares, {a["id"]}))]
                     and all(f"{u['id']} {len(em(lugares, {a['id']}, {u['id']}))}" in achadas[0] for u in lista))
        else:
            certo = len(achadas) == 1 and not numeros(achadas[0])
        confere(certo, f"{d['id']}: a abertura {a['id']}: {achadas}")


def confere_formas(d, sec, m, e):
    """A secao de um documento de formas de pergunta: quantos trechos cada forma tem, e quantos
    em cada aula."""
    lugares, tabela = e["lugares"][d["id"]], linhas_de_tabela(sec)
    for n, forma in enumerate(d["formas"], 1):
        k = len(em(lugares, {n}))
        confere([forma["verbo"], "; ".join(forma["tipos"]), str(k), forma["ordem"]] in tabela,
                f"{d['id']}: a forma {forma['verbo']!r} com {k} trecho(s)")
    corrido = "\n".join(sec)
    for aula in m["ids"]["aulas"]:
        k = len(em(lugares, None, {aula}))
        achado = re.search(rf"(?<![\w-]){re.escape(aula)} (\d+)", corrido)
        confere((int(achado.group(1)) if achado else 0) == k, f"{d['id']}: {k} trecho(s) na aula {aula}")


def confere_colunas(d, sec, m, e):
    """A secao de um documento de colunas: quantos trechos viram cartao, e cada coluna."""
    k = len(em(e["lugares"][d["id"]]))
    confere([n for linha in sec for n in numeros(linha)] == [k], f"{d['id']}: {k} trechos viram cartão")
    tabela = linhas_de_tabela(sec)
    confere(all([c["id"], c["lado"], c["ordem"]] in tabela for c in d["colunas"]), f"{d['id']}: as colunas")


CONFERE_SECAO = {PARTES: confere_partes, GRADE: confere_grade, FORMAS: confere_formas, COLUNAS: confere_colunas}


def confere_onde(texto, m, e):
    """Para cada tipo de onde_se_ensina, os documentos onde ele se ensina e os outros em que
    trechos dele caem, com quantos."""
    nomes, tabela = nomes_dos_documentos(m["formato"]), tabelas_do(texto)
    for tipo, docs in m["formato"]["onde_se_ensina"].items():
        alem = [(nomes[d], len(e["tipos"][d][tipo])) for d in nomes if d not in docs and e["tipos"][d].get(tipo)]
        achadas = [c for c in tabela if c[0] == tipo]
        certo = len(achadas) == 1 and achadas[0][1] == "; ".join(nomes[d] for d in docs)
        if certo and alem:
            certo = achadas[0][2] == "; ".join(f"{n} {k}" for n, k in alem)
        elif certo:
            certo = not numeros(achadas[0][2]) and not any(n in achadas[0][2] for n in nomes.values())
        confere(certo, f"onde se ensina o tipo {tipo!r}, e onde ele cai: {achadas}")


# ---------- as secoes das unidades, das fontes e do limite ----------

def partes_esperadas(d, u, partes_, f):
    """(nomes, quantas): os nomes das partes dadas de uma entrada do documento d, cuja unidade e
    u ({} no documento que nao lista unidades), na ordem do molde, sem a do trecho que vai junto
    do assunto, que o teste nao nomeia; e quantas partes ha."""
    ordem_ = d.get("abertura", []) + grade_da(d, u) if d["molde"] == GRADE else f["partes_por_tipo"]
    return [x["nome"] for x in ordem_ if x["id"] in partes_], len(partes_)


def linha_da_entrada(tabela, u, i):
    """As linhas da tabela cuja primeira celula e a da entrada: a que tem o nome do item e o da
    unidade dele, ou a que tem o nome da unidade e nao o de um item dela."""
    if i:
        return [c for c in tabela if i["nome"] in c[0] and u["nome"] in c[0]]
    return [c for c in tabela if u["nome"] in c[0] and not any(x["nome"] in c[0] for x in u.get("itens", []))]


def confere_unidades(texto, m, e, rotulo):
    """Em cada documento que lista unidades, a linha de cada unidade e de cada item (a do item
    com o nome da unidade dele): as aulas que tratam, com as partes na ordem do molde, e o aviso
    antes delas so quando quem decide e o formato; as que so mencionam; e quantos trechos de
    depois da ultima aula ficam ali. E a linha de cada conjunto, com os membros na ordem."""
    f, lim, aulas = m["formato"], e["limite"], m["ids"]["aulas"]
    tabela, (_, decisoes) = tabelas_do(texto), itens_e_decisoes(f)
    de_depois = collections.Counter(entrada for _, entrada in {(lugar.trecho, lugar.entrada) for lugar in lim.ficam
                                                              if lugar.aula not in e["ate"]})
    for d, u, i in unidades_e_itens(f):
        k, achadas = (d["id"], (i or u)["id"]), linha_da_entrada(tabela, u, i)
        if not confere(len(achadas) == 1 and len(achadas[0]) == 4, f"{rotulo}: uma linha de {k}: {achadas}"):
            continue
        c = achadas[0]
        tratam = aulas_da_celula(c[1], aulas)
        certas = [(a, partes_esperadas(d, u, lim.partes.get(k, {}).get(a, []), f)) for a in lim.tratam.get(k, [])]
        confere(tratam is not None and [a for a, _ in tratam] == [a for a, _ in certas]
                and all(nomes[:len(ps)] == ps and len(nomes) == n
                        for (_, nomes), (_, (ps, n)) in zip(tratam, certas)),
                f"{rotulo}: as aulas que tratam de {k}, com as partes: {c[1]} ({certas})")
        confere(bool(comeco(c[1])[0]) == (k in decisoes),
                f"{rotulo}: o aviso de que o formato decide quem trata de {k}, só quando ele decide: {c[1]}")
        mencionam = aulas_da_celula(c[2], aulas)
        confere(mencionam is not None and [a for a, _ in mencionam] == lim.mencionam.get(k, []),
                f"{rotulo}: as aulas que só mencionam {k}: {c[2]}")
        confere(numeros(c[3]) == [de_depois[k]], f"{rotulo}: {de_depois[k]} trecho(s) de depois em {k}: {c[3]}")
    for d in f["documentos"]:
        for cj in d.get("conjuntos", []):
            achadas = [c for c in tabela if c[0] == cj["nome"]]
            membros = [nome_da_coisa(f, d["id"], mb) for mb in cj["membros"]]
            pedacos_ = no_topo(achadas[0][1], ";") if len(achadas) == 1 else []
            confere(len(pedacos_) == len(membros) and all(nm in p for nm, p in zip(membros, pedacos_)),
                    f"{rotulo}: os membros do conjunto {cj['id']}, na ordem: {achadas}")


def confere_so_mencionadas(texto, m, e, rotulo):
    """As unidades sem material de que alguma aula ate a ultima fala, com as aulas que as
    mencionam, e so elas."""
    f, lim = m["formato"], e["limite"]
    esperadas = {}
    for d in f["documentos"]:
        for u in d.get("unidades", []):
            mencionam = lim.mencionam.get((d["id"], u["id"]), [])
            if (d["id"], u["id"]) not in lim.tratadas and e["ate"] & set(mencionam):
                esperadas[(d["nome"], u["nome"])] = mencionam
    unidades = {d["nome"]: {u["nome"] for u in d.get("unidades", [])} for d in f["documentos"]}
    achadas = {(c[0], c[1]): [a for a, _ in aulas_da_celula(c[2], m["ids"]["aulas"]) or []]
               for c in tabelas_do(texto) if len(c) == 3 and c[1] in unidades.get(c[0], ())}
    confere(achadas == esperadas, f"{rotulo}: as unidades só mencionadas: {achadas} ({esperadas})")


def confere_fontes(texto, m, e, rotulo):
    """Para cada fonte, pelo nome dela, os documentos que so ela da: quantos trechos, de que
    aulas e o primeiro."""
    nomes = nomes_dos_documentos(m["formato"])
    for x in FONTES_DO_TESTE:
        so_dela = e["discordam"][x]
        esperadas = [[nomes[d], str(len(so_dela[d])), aulas_de(so_dela[d], m, e), so_dela[d][0]]
                     for d in nomes if d in so_dela]
        confere(tabela_depois(texto, repr(x)) == esperadas, f"{rotulo}: os documentos que só a fonte {x!r} dá")


def confere_sem_linha(texto, m, e, rotulo):
    """Cada pedaco sem linha na tabela dos destinos, com quantos trechos, de que aulas e o
    primeiro; e nenhum pedaco com linha."""
    tabela = tabelas_do(texto)
    for p, ids in e["sem_linha"].items():
        confere([c for c in tabela if c[0] == p] == [[p, str(len(ids)), aulas_de(ids, m, e), ids[0]]],
                f"{rotulo}: o pedaço sem linha {p!r}")
    com_linha = {p for p, _ in m["destinos"]}
    confere(not [c for c in tabela if c[0] in com_linha], f"{rotulo}: nenhum pedaço com linha sai como sem linha")


def confere_sem_lugar(texto, m, e, rotulo):
    """Cada trecho ate a ultima aula sem lugar depois do limite, com o documento, a entrada e a
    parte de cada lugar que perdeu, e so eles."""
    f, ids = m["formato"], {c["id"] for c in m["casos"]}
    achadas = {c[0]: c[1] for c in tabelas_do(texto) if len(c) == 2 and c[0] in ids}
    confere(set(achadas) == set(e["perdidos"]), f"{rotulo}: os trechos sem lugar: {sorted(achadas)}")
    for i, postos in e["perdidos"].items():
        celula = achadas.get(i, "")
        confere(all(x in celula for d, ent, p, _ in postos for x in [d, nome_da_coisa(f, d, ent)]
                    + partes_esperadas(pelo_id(f, d), unidade_e_item(f, d, ent)[0], [p], f)[0]),
                f"{rotulo}: os lugares que {i} perdeu: {celula}")


def confere_avisos(linhas_, esperados, rotulo):
    """Cada aviso esperado, (id do trecho ou None, o que a linha diz), numa linha que tem o id e
    o que ela diz; tantas linhas de cada id quantos avisos dele; e nenhuma linha a mais."""
    for i, palavras in esperados:
        confere(any((i is None or tem_id(linha, i)) and all(p in linha for p in palavras) for linha in linhas_),
                f"{rotulo}: um aviso que diz {i} {palavras}: {linhas_}")
    por_id = collections.Counter(i for i, _ in esperados if i)
    confere(all(sum(tem_id(linha, i) for linha in linhas_) == n for i, n in por_id.items())
            and len(linhas_) == len(esperados), f"{rotulo}: {len(esperados)} aviso(s), e só eles: {linhas_}")


def roda_mundo(m):
    """(codigo, tela, relatorio) da conferencia no mundo m, gravado no projeto pequeno."""
    escreve_mundo(m)
    RELATORIO.unlink(missing_ok=True)
    codigo, tela = roda_conferencia()
    return codigo, tela, RELATORIO.read_text(encoding="utf-8") if RELATORIO.exists() else ""


def confere_rodada(m, rotulo):
    """A conferencia no mundo m: cada aviso esperado, e so ele, na tela e no relatorio; o
    codigo de saida; e cada secao do relatorio. Devolve o relatorio."""
    e = esperado(m)
    codigo, tela, texto = roda_mundo(m)
    confere(texto, f"{rotulo}: o relatório é gravado: {tela}")
    erros, faltas = ([linha for linha in tela if linha.startswith(x)] for x in (ERRO, FALTA))
    confere_avisos(erros, e["erros"], f"{rotulo}: ERRO")
    confere_avisos(faltas, e["faltas"] + [(None, [p]) for p in e["sem_linha"]], f"{rotulo}: FALTA")
    confere(all(linha in texto for linha in erros + faltas), f"{rotulo}: cada aviso está também no relatório")
    confere(codigo == (1 if erros or faltas else 0), f"{rotulo}: o código de saída {codigo}")
    confere(tem_as_classes(texto, e["classes"], m["formato"]), f"{rotulo}: a tabela das classes: {dict(e['classes'])}")
    for d in m["formato"]["documentos"]:
        sec = secao(texto, d["nome"])
        if confere(sec, f"{rotulo}: o relatório tem a seção do documento {d['id']}"):
            CONFERE_SECAO[d["molde"]](d, sec, m, e)
    confere_onde(texto, m, e)
    for confere_secao in (confere_unidades, confere_so_mencionadas, confere_fontes, confere_sem_linha,
                          confere_sem_lugar):
        confere_secao(texto, m, e, rotulo)
    return texto


def confere_regras_do_limite(texto, m):
    """As regras do limite vistas no relatorio, em cada linha de unidade e de item: a entrada
    em que ficam trechos de depois da ultima aula tem uma aula ate a ultima que trata dela; a
    aula que trata pela conta diz pelo menos as partes pedidas; e nenhuma aula trata e so
    menciona a mesma entrada."""
    f, aulas = m["formato"], m["ids"]["aulas"]
    ate, n = set(ate_a(aulas, f["ultima_aula"])), f["partes_para_tratar"]
    tabela = tabelas_do(texto)
    for _, u, i in unidades_e_itens(f):
        achadas, x = linha_da_entrada(tabela, u, i), i or u
        if len(achadas) != 1:
            continue
        c = achadas[0]
        tratam, mencionam = aulas_da_celula(c[1], aulas) or [], aulas_da_celula(c[2], aulas) or []
        confere(numeros(c[3]) == [0] or any(a in ate for a, _ in tratam),
                f"limite: trecho de depois só fica em entrada tratada: {x['id']} {c}")
        confere("tratada_em" in x or (i is None and u.get("itens")) or all(len(ps) >= n for _, ps in tratam),
                f"limite: a aula que trata de {x['id']} pela conta diz pelo menos {n} partes: {c[1]}")
        confere(not {a for a, _ in tratam} & {a for a, _ in mencionam},
                f"limite: nenhuma aula trata e só menciona {x['id']}: {c}")


# ---------- o formato errado: cada caso estraga uma copia e diz o lugar do erro ----------

def caso_campo_no_topo(f, ids):
    campo = ident()
    f[campo] = nome()
    return "campo que o molde não conhece, no topo", [campo]


def caso_campo_no_documento(f, ids):
    campo = ident()
    doc(f, ids, "colunas")[campo] = nome()
    return "campo que o molde não conhece, num documento", [campo, f"documentos[{indice(f, ids, 'colunas')}]"]


def caso_campo_de_outro_molde(f, ids):
    doc(f, ids, "partes")["formas"] = copy.deepcopy(doc(f, ids, "formas")["formas"])
    return "campo de outro tipo de molde", [f"documentos[{indice(f, ids, 'partes')}].formas"]


def caso_grade_fora_do_molde(f, ids):
    doc(f, ids, "colunas")["eixos"] = eixos()
    return "grade num documento cujo molde não tem grade", [f"documentos[{indice(f, ids, 'colunas')}].eixos"]


def caso_unidade_com_grade_fora_do_molde(f, ids):
    doc(f, ids, "partes")["unidades"][0]["eixos"] = eixos()
    return "unidade com grade num documento cujo molde não tem grade", [
        f"documentos[{indice(f, ids, 'partes')}].unidades[0]", "eixos"]


def caso_falta_campo_do_molde(f, ids):
    del doc(f, ids, "formas")["formas"]
    return "campo que o tipo de molde pede e falta", [f"documentos[{indice(f, ids, 'formas')}]", "formas"]


def caso_molde_desconhecido(f, ids):
    tipo = ident()
    doc(f, ids, "colunas")["molde"] = tipo
    return "tipo de molde desconhecido", [tipo]


def caso_texto_no_lugar_de_lista(f, ids):
    f["cursos"] = nome()
    return "texto onde o molde pede uma lista", ["cursos"]


def caso_unidade_em_dois_documentos(f, ids):
    u = doc(f, ids, "partes")["unidades"][0]
    doc(f, ids, "casos")["unidades"] = [copy.deepcopy(u)]
    return "unidade em dois documentos", [u["id"], ids["partes"], ids["casos"]]


def caso_id_repetido_na_ficha_do_documento(f, ids):
    eixos_ = doc(f, ids, "grade")["eixos"]
    dividido = next(e for e in eixos_ if e.get("subtopicos"))
    outro = next(e for e in eixos_ if e is not dividido)
    dividido["subtopicos"][0]["id"] = outro["id"]
    return "id repetido na ficha do documento", [outro["id"], ids["grade"]]


def caso_id_repetido_na_ficha_da_unidade(f, ids):
    d = doc(f, ids, "unidades")
    u = d["unidades"][0]
    u["eixos"][0]["id"] = d["abertura"][0]["id"]
    return "id repetido na ficha de uma unidade", [d["abertura"][0]["id"], ids["unidades"], u["id"]]


def caso_elo_com_eixo_que_nao_ha(f, ids):
    elo_, eixo = doc(f, ids, "grade")["elos"][0], ident()
    elo_["eixos"].append(eixo)
    return "elo com eixo que o documento não tem", [ids["grade"], elo_["id"], eixo]


def caso_unidade_sem_grade(f, ids):
    """Sem a grade do documento, a unidade sem eixos proprios fica sem grade; as outras sem eles
    ganham eixos, para que o erro seja um so."""
    d = doc(f, ids, "grade")
    del d["eixos"], d["elos"]
    sem = sem_eixos(d)
    for u in d["unidades"]:
        if u is not sem and not u.get("eixos"):
            u["eixos"] = eixos()
    return "unidade sem grade", [ids["grade"], sem["id"]]


def caso_documento_sem_grade(f, ids):
    d = doc(f, ids, "grade")
    del d["eixos"], d["elos"], d["unidades"], d["conjuntos"]  # sem as unidades, sai o conjunto delas
    return "documento sem grade num molde que pede grade", [ids["grade"]]


def caso_grupo_que_nao_existe(f, ids):
    grupo = ident()
    doc(f, ids, "partes")["grupos"].append(grupo)
    return "grupo que não existe", [ids["partes"], grupo]


def caso_tipo_em_duas_partes(f, ids):
    uma, outra = SORTEIO.sample(f["partes_por_tipo"], 2)
    outra["tipos"].append(uma["tipos"][0])
    return "tipo em duas partes da sequência", [uma["tipos"][0], uma["id"], outra["id"]]


def caso_tipo_em_duas_formas(f, ids):
    uma, outra = SORTEIO.sample(doc(f, ids, "formas")["formas"], 2)
    outra["tipos"].append(uma["tipos"][0])
    return "tipo em duas formas de pergunta", [ids["formas"], uma["tipos"][0]]


def caso_onde_com_tipo_que_nao_existe(f, ids):
    tipo = nome()
    f["onde_se_ensina"][tipo] = [ids["partes"]]
    return "onde_se_ensina com tipo que não existe", [tipo]


def caso_onde_com_documento_que_nao_existe(f, ids):
    tipo, documento_ = SORTEIO.choice(sorted(f["onde_se_ensina"])), ident()
    f["onde_se_ensina"][tipo].append(documento_)
    return "onde_se_ensina com documento que não existe", [tipo, documento_]


def caso_id_em_fora_e_em_marcas(f, ids):
    f["marcas"][0]["id"] = f["fora"][0]["id"]
    return "id em fora e em marcas", [f["fora"][0]["id"]]


def caso_documento_sem_trecho(f, ids):
    doc(f, ids, "partes")["grupos"] = []
    return "documento que não recebe nenhum trecho", [ids["partes"]]


def com_itens(f, ids):
    """As unidades com itens do documento de unidades com eixos proprios."""
    return [u for u in doc(f, ids, "unidades")["unidades"] if u.get("itens")]


def muda_id(documento_, coisa, novo):
    """Troca o id de uma unidade, de um item ou de um conjunto do documento, tambem nos membros
    dos conjuntos dele, sem repetir membro."""
    velho, coisa["id"] = coisa["id"], novo
    for c in documento_.get("conjuntos", []):
        c["membros"] = list(dict.fromkeys(novo if m == velho else m for m in c["membros"]))


def caso_item_com_id_de_unidade(f, ids):
    u = SORTEIO.choice(doc(f, ids, "partes")["unidades"])
    muda_id(doc(f, ids, "unidades"), SORTEIO.choice(SORTEIO.choice(com_itens(f, ids))["itens"]), u["id"])
    return "item com o id de uma unidade de outro documento", [u["id"], ids["partes"], ids["unidades"]]


def caso_item_em_duas_unidades(f, ids):
    uma, outra = SORTEIO.sample(com_itens(f, ids), 2)
    i = SORTEIO.choice(uma["itens"])
    muda_id(doc(f, ids, "unidades"), SORTEIO.choice(outra["itens"]), i["id"])
    return "item com o id de um item de outra unidade", [i["id"], ids["unidades"], uma["id"], outra["id"]]


def caso_conjunto_com_id_de_item(f, ids):
    i = SORTEIO.choice(SORTEIO.choice(com_itens(f, ids))["itens"])
    muda_id(doc(f, ids, "grade"), doc(f, ids, "grade")["conjuntos"][0], i["id"])
    return "conjunto com o id de um item de outro documento", [i["id"], ids["grade"], ids["unidades"]]


def caso_membro_que_nao_ha(f, ids):
    c, membro = doc(f, ids, "unidades")["conjuntos"][0], ident()
    c["membros"].append(membro)
    return "membro de conjunto que o formato não tem", [ids["unidades"], c["id"], membro]


def caso_membro_de_outro_documento(f, ids):
    c, membro = doc(f, ids, "unidades")["conjuntos"][0], SORTEIO.choice(doc(f, ids, "partes")["unidades"])["id"]
    c["membros"].append(membro)
    return "membro de conjunto que é de outro documento", [ids["unidades"], c["id"], membro]


def caso_membro_que_e_conjunto(f, ids):
    c = doc(f, ids, "unidades")["conjuntos"][0]
    c["membros"].append(c["id"])
    return "membro de conjunto que é um conjunto", [ids["unidades"], c["id"]]


def caso_partes_abaixo_do_minimo(f, ids):
    f["partes_para_tratar"] = MINIMO_PARTES - SORTEIO.randint(1, 3)
    return "número de partes para tratar abaixo do mínimo", ["partes_para_tratar"]


def caso_partes_que_nao_e_inteiro(f, ids):
    f["partes_para_tratar"] += 0.5
    return "número de partes para tratar que não é inteiro", ["partes_para_tratar"]


def caso_fonte_desconhecida(f, ids):
    fonte = ident()
    f["documentos_vem_de"].append(fonte)
    return "fonte dos documentos que o molde não conhece", ["documentos_vem_de", fonte]


def caso_sem_fonte(f, ids):
    f["documentos_vem_de"] = []
    return "nenhuma fonte dos documentos", ["documentos_vem_de"]


def caso_fonte_repetida(f, ids):
    f["documentos_vem_de"].append(SORTEIO.choice(f["documentos_vem_de"]))
    return "fonte dos documentos repetida", ["documentos_vem_de"]


def caso_tratada_em_na_unidade_com_itens(f, ids):
    u = SORTEIO.choice(com_itens(f, ids))
    u["tratada_em"] = tratada_em(ids["aulas"])
    i, j = indice(f, ids, "unidades"), doc(f, ids, "unidades")["unidades"].index(u)
    return "aulas que tratam numa unidade com itens", [f"documentos[{i}].unidades[{j}].tratada_em"]


def caso_itens_fora_da_grade(f, ids):
    doc(f, ids, "partes")["unidades"][0]["itens"] = [item()]
    return "itens numa unidade de documento cujo molde não tem grade", [
        f"documentos[{indice(f, ids, 'partes')}].unidades[0]", "itens"]


def caso_aula_repetida(f, ids):
    aula = SORTEIO.choice(ids["aulas"])
    doc(f, ids, "partes")["unidades"][0]["tratada_em"] = [aula, aula]
    return "aula repetida entre as que tratam", [f"documentos[{indice(f, ids, 'partes')}].unidades[0].tratada_em"]


def caso_conjunto_sem_membros(f, ids):
    doc(f, ids, "grade")["conjuntos"][0]["membros"] = []
    return "conjunto sem membros", [f"documentos[{indice(f, ids, 'grade')}].conjuntos[0].membros"]


def caso_membro_repetido(f, ids):
    membros = doc(f, ids, "grade")["conjuntos"][0]["membros"]
    membros.append(SORTEIO.choice(membros))
    return "membro repetido num conjunto", [f"documentos[{indice(f, ids, 'grade')}].conjuntos[0].membros"]


CASOS = [caso_campo_no_topo, caso_campo_no_documento, caso_campo_de_outro_molde, caso_grade_fora_do_molde,
         caso_unidade_com_grade_fora_do_molde, caso_falta_campo_do_molde, caso_molde_desconhecido,
         caso_texto_no_lugar_de_lista, caso_unidade_em_dois_documentos, caso_id_repetido_na_ficha_do_documento,
         caso_id_repetido_na_ficha_da_unidade, caso_elo_com_eixo_que_nao_ha, caso_unidade_sem_grade,
         caso_documento_sem_grade, caso_grupo_que_nao_existe, caso_tipo_em_duas_partes, caso_tipo_em_duas_formas,
         caso_onde_com_tipo_que_nao_existe, caso_onde_com_documento_que_nao_existe, caso_id_em_fora_e_em_marcas,
         caso_documento_sem_trecho, caso_item_com_id_de_unidade, caso_item_em_duas_unidades,
         caso_conjunto_com_id_de_item, caso_membro_que_nao_ha, caso_membro_de_outro_documento,
         caso_membro_que_e_conjunto, caso_partes_abaixo_do_minimo, caso_partes_que_nao_e_inteiro,
         caso_fonte_desconhecida, caso_sem_fonte, caso_fonte_repetida, caso_tratada_em_na_unidade_com_itens,
         caso_itens_fora_da_grade, caso_aula_repetida, caso_conjunto_sem_membros, caso_membro_repetido]


# ---------- o mundo com problema: cada caso muda uma copia e diz o que o aviso tem de dizer ----------

def caso_do(v, caso):
    return next(c for c in v["casos"] if c["caso"] == caso)


def unidade_das_partes(v):
    return doc(v["formato"], v["ids"], "partes")["unidades"][0]["id"]


def linha_nova(v, linha):
    """Poe a linha no fim da tabela e devolve o comeco do erro dela, com o numero dela (o
    cabecalho e a linha 1)."""
    v["tabela"].append(linha)
    return f"linha {len(v['tabela']) + 1}:"


def tira_linhas(v, caso):
    v["tabela"] = [linha for linha in v["tabela"] if linha[0] != caso["id"]]


def muda_parte(v, documento_, de, para, unidade_=None):
    """Leva as linhas da tabela de uma parte do documento para outra (so as da unidade dada)."""
    v["tabela"] = [(i, d, u, para if d == documento_ and p == de and unidade_ in (None, u) else p)
                   for i, d, u, p in v["tabela"]]


def familias_do(v):
    return doc(v["formato"], v["ids"], "unidades")["unidades"]


def p_id_desconhecido(v):
    i = ident()
    return [linha_nova(v, (i, v["ids"]["partes"], unidade_das_partes(v), "")), i]


def p_linha_repetida(v):
    return [linha_nova(v, SORTEIO.choice(v["tabela"]))]


def p_documento_de_todos(v):
    return [linha_nova(v, (caso_do(v, "tipo")["id"], v["ids"]["formas"], "", "")), v["ids"]["formas"]]


def p_documento_desconhecido(v):
    d = ident()
    return [linha_nova(v, (caso_do(v, "tipo")["id"], d, "", "")), d]


def p_unidade_desconhecida(v):
    u, d = ident(), doc(v["formato"], v["ids"], "grade")
    return [linha_nova(v, (caso_do(v, "grade")["id"], v["ids"]["grade"], u, d["eixos"][0]["id"])), u]


def p_unidade_de_outro_documento(v):
    """A linha no documento de grade com uma familia, do documento das familias, e um eixo dela:
    so a unidade, que nao e do documento da linha, esta errada."""
    fam = SORTEIO.choice(familias_do(v))
    linha = (caso_do(v, "grade")["id"], v["ids"]["grade"], fam["id"], fam["eixos"][0]["id"])
    return [linha_nova(v, linha), fam["id"]]


def p_parte_de_outra_grade(v):
    d = doc(v["formato"], v["ids"], "grade")
    parte = com_eixos(d)["eixos"][0]["id"]
    return [linha_nova(v, (caso_do(v, "grade")["id"], v["ids"]["grade"], sem_eixos(d)["id"], parte)), parte]


def p_abertura_que_nao_recebe(v):
    d = doc(v["formato"], v["ids"], "grade")
    parte = d["abertura"][0]["id"]
    return [linha_nova(v, (caso_do(v, "grade")["id"], v["ids"]["grade"], sem_eixos(d)["id"], parte)), parte]


def p_parte_sem_grade(v):
    parte = ident()
    return [linha_nova(v, (caso_do(v, "tipo")["id"], v["ids"]["partes"], unidade_das_partes(v), parte)), parte]


def p_item_com_abertura(v):
    d = doc(v["formato"], v["ids"], "unidades")
    item_, parte = next(u for u in d["unidades"] if u.get("itens"))["itens"][0]["id"], d["abertura"][0]["id"]
    return [linha_nova(v, (caso_do(v, "tipo")["id"], v["ids"]["unidades"], item_, parte)), parte]


def p_conjunto_com_parte_de_um_membro(v):
    d = doc(v["formato"], v["ids"], "unidades")
    parte = d["abertura"][0]["id"]  # a unidade do conjunto tem a abertura; o item dele, nao
    return [linha_nova(v, (caso_do(v, "tipo")["id"], v["ids"]["unidades"], d["conjuntos"][0]["id"], parte)), parte]


def p_parte_que_nao_e_da_entrada(v):
    """A linha sem unidade, com o eixo da ultima familia que nao e a sem itens que o destino
    nomeia: um eixo que a linha pode dar no documento, mas nao nessa entrada."""
    sem_itens = next(u for u in familias_do(v) if not u.get("itens"))
    eixo = [u for u in familias_do(v) if u is not sem_itens][-1]["eixos"][0]["id"]
    caso = caso_do(v, "unidades")
    v["tabela"] = [(i, d, "" if i == caso["id"] else u, eixo if i == caso["id"] else p) for i, d, u, p in v["tabela"]]
    caso["pedacos"] = [SORTEIO.choice(v["vocabulario"][sem_itens["id"]])]
    return [caso["id"], sem_itens["id"], eixo]


def p_fora_sem_regra(v):
    regra = ident()
    return [linha_nova(v, (caso_do(v, "tipo")["id"], lidos.FORA, regra, "")), regra]


def p_fora_com_parte(v):
    parte = ident()
    return [linha_nova(v, (caso_do(v, "lido")["id"], lidos.FORA, caso_do(v, "lido")["regra"], parte)), parte]


def p_documento_em_que_nao_cai(v):
    caso = caso_do(v, "tipo")
    v["tabela"].append((caso["id"], v["ids"]["casos"], "", ""))
    return [caso["id"], v["ids"]["casos"]]


def p_fora_e_com_lugar(v):
    caso = caso_do(v, "lido")
    v["tabela"].append((caso["id"], v["ids"]["partes"], unidade_das_partes(v), ""))
    return [caso["id"]]


def p_de_fora_com_lugar(v):
    caso = caso_do(v, "fora")
    v["tabela"].append((caso["id"], v["ids"]["partes"], unidade_das_partes(v), ""))
    return [caso["id"]]


def p_assunto_sem_linha(v):
    caso = caso_do(v, "assunto")
    tira_linhas(v, caso)
    return [caso["id"]]


def p_sem_documento(v):
    """Um trecho de estudo sem documento pelas fontes (monta_sem_documento) e sem linha na
    tabela da leitura: nao cai em documento de conteudo, nem espera o assunto."""
    caso = caso_do(v, "tipo")
    monta_sem_documento(caso, v, None)
    return [caso["id"]]


def p_eixo_vazio(v):
    eixo, outro = SORTEIO.sample(doc(v["formato"], v["ids"], "grade")["eixos"], 2)
    muda_parte(v, v["ids"]["grade"], eixo["id"], outro["id"])
    return [eixo["id"], v["ids"]["grade"]]


def p_eixo_vazio_da_unidade(v):
    u = com_eixos(doc(v["formato"], v["ids"], "grade"))
    eixo, outro = SORTEIO.sample(u["eixos"], 2)
    muda_parte(v, v["ids"]["grade"], eixo["id"], outro["id"], u["id"])
    return [eixo["id"], u["id"]]


def p_elo_sem_trecho(v):
    d = doc(v["formato"], v["ids"], "grade")
    elo_ = SORTEIO.choice(d["elos"])
    fora_do_elo = next(e["id"] for e in d["eixos"] if e["id"] not in elo_["eixos"])
    for eixo in elo_["eixos"]:
        muda_parte(v, v["ids"]["grade"], eixo, fora_do_elo)
    return [elo_["id"]]


def p_abertura_vazia(v):
    """A abertura das familias sem trecho: as linhas dela vao para um eixo de cada familia, e o trecho que fica nela
    por um conjunto perde a linha."""
    d = doc(v["formato"], v["ids"], "unidades")
    abertura_ = d["abertura"][0]["id"]
    for u in d["unidades"]:
        muda_parte(v, v["ids"]["unidades"], abertura_, u["eixos"][0]["id"], u["id"])
    for caso in v["casos"]:
        if caso["caso"] == "abertura_por_conjunto":
            tira_linhas(v, caso)
    return [abertura_]


def p_forma_sem_trecho(v):
    forma = {"verbo": nome(), "tipos": [nome()], "ordem": ordem()}
    doc(v["formato"], v["ids"], "formas")["formas"].append(forma)
    return [forma["verbo"], v["ids"]["formas"]]


def tipos_de_um_lugar(v, so_em, nao_em):
    """Os tipos do formato que estao em 'so_em' e em nenhum de 'nao_em': as partes da
    sequencia, os que vao junto e as formas de pergunta."""
    f = v["formato"]
    lugares = {"partes": {t for p in f["partes_por_tipo"] for t in p["tipos"]}, "junto": set(f["tipos_junto"]),
               "formas": {t for x in doc(f, v["ids"], "formas")["formas"] for t in x["tipos"]}}
    return sorted(lugares[so_em] - set().union(*(lugares[n] for n in nao_em)))


def p_tipo_sem_forma(v):
    caso, tipo = caso_do(v, "tipo"), tipos_de_um_lugar(v, "partes", ["formas"])[0]
    caso["tipos"].append(tipo)
    return [caso["id"], tipo]


def p_tipo_sem_lugar(v):
    caso, tipo = caso_do(v, "tipo"), tipos_de_um_lugar(v, "formas", ["partes", "junto"])[0]
    caso["tipos"].append(tipo)
    return [caso["id"], tipo]


def p_grupo_desconhecido(v):
    caso, grupo = caso_do(v, "tipo"), ident()
    caso["grupos"].append(grupo)
    return [caso["id"], grupo]


def p_tipo_de_fora_com_outro(v):
    caso = caso_do(v, "tipo")
    caso["tipos"].append(v["formato"]["fora"][0]["tipos"][0])
    return [caso["id"]]


def p_sem_grupo_e_sem_marca(v):
    caso = caso_do(v, "tipo")
    caso["grupos"] = []
    return [caso["id"]]


def p_documento_fora(v):
    v["formato"]["documentos"].append(documento(PARTES, id=lidos.FORA, grupos=[v["ids"]["grupos"]["orfao"]]))
    return [repr(lidos.FORA)]


def p_destino_com_id_desconhecido(v):
    """Uma linha a mais na tabela dos destinos: um pedaco que ja nomeia ids, com um id que o
    formato nao tem."""
    pedaco_, i = next(p for p, u in v["destinos"] if u), ident()
    v["destinos"].append((pedaco_, i))
    return [TABELA_DOS_DESTINOS.name, repr(pedaco_), repr(i)]


PROBLEMAS = [p_id_desconhecido, p_linha_repetida, p_documento_de_todos, p_documento_desconhecido,
             p_unidade_desconhecida, p_unidade_de_outro_documento, p_parte_de_outra_grade, p_abertura_que_nao_recebe,
             p_parte_sem_grade,
             p_item_com_abertura, p_conjunto_com_parte_de_um_membro, p_parte_que_nao_e_da_entrada, p_fora_sem_regra,
             p_fora_com_parte, p_documento_em_que_nao_cai, p_fora_e_com_lugar, p_de_fora_com_lugar,
             p_assunto_sem_linha, p_sem_documento, p_eixo_vazio, p_eixo_vazio_da_unidade, p_elo_sem_trecho,
             p_abertura_vazia, p_forma_sem_trecho, p_tipo_sem_forma, p_tipo_sem_lugar, p_grupo_desconhecido,
             p_tipo_de_fora_com_outro, p_sem_grupo_e_sem_marca, p_documento_fora, p_destino_com_id_desconhecido]


# ---------- o que falta: cada caso muda uma copia e diz o que a FALTA tem de dizer ----------

def f_sem_eixo(v):
    caso = caso_do(v, "grade")
    tira_linhas(v, caso)
    return [caso["id"], v["ids"]["grade"]]


def f_sem_entrada(v):
    caso = caso_do(v, "grade")
    v["tabela"] = [(i, d, "" if i == caso["id"] else u, p) for i, d, u, p in v["tabela"]]
    caso["pedacos"] = [SORTEIO.choice(v["nada"])]
    return [caso["id"], v["ids"]["grade"]]


def f_destino_sem_linha(v):
    pedaco_ = caso_do(v, "grade")["pedacos"][0]
    v["destinos"] = [linha for linha in v["destinos"] if linha[0] != pedaco_]
    return [pedaco_]


FALTAS = [f_sem_eixo, f_sem_entrada, f_destino_sem_linha]
# a classe em que o caso poe o trecho, tirado das de estudo com lugar; a falta do pedaco sem linha nao muda a classe
CLASSE_DO_CASO = {
    p_assunto_sem_linha: ("assunto",), p_sem_documento: ("problema", lugares.SEM_DOCUMENTO),
    f_sem_eixo: ("problema", confere_moldes.SEM_LUGAR), f_sem_entrada: ("unidade",)}


# ---------- a entrada errada: cada caso estraga uma entrada e diz o que o ERRO tem de dizer ----------

def e_campo_na_forma(v):
    campo = ident()
    v["forma"][campo] = nome()
    return [campo], None


def e_forma_sem_papel(v):
    campo = next(c for c in v["forma"]["campos"] if c.get("papel") == CAMINHO)
    del campo["papel"]
    for caso in v["casos"]:  # o campo continua com o texto que tinha, agora sem papel
        caso["extras"][campo["nome"]] = " ".join(caso["caminhos"]) or v["forma"]["vazio"]
    return [repr(CAMINHO)], None


def e_marca_num_papel_que_a_forma_nao_da(v):
    papel = ident()
    v["formato"]["marcas"][0]["papeis"] = [papel]
    return [papel, ARQUIVO_FORMATO.name], None


def e_caminho_que_a_forma_nao_tem(v):
    caminho = ident()
    doc(v["formato"], v["ids"], "casos")["caminhos"].append(caminho)
    return [caminho, ARQUIVO_FORMATO.name], None


def e_linha_fora_da_forma(v):
    arquivo = arquivo_da_aula(v, v["ids"]["aulas"][0])

    def depois():
        arquivo.write_text(arquivo.read_text(encoding="utf-8") + frase() + "\n", encoding="utf-8")
    return [arquivo.name], depois


def e_cabecalho_da_tabela(v):
    return [PROJETO.caminho("lugares_lidos").name], lambda: escreve_tabela(v["tabela"], lidos.CABECALHO[::-1])


def e_linha_com_coluna_a_mais(v):
    v["tabela"].append(tuple(v["tabela"][0]) + (ident(),))
    return [f"linha {len(v['tabela']) + 1}"], None


def fora_do_utf8(arquivo):
    """O que estraga o arquivo: um texto a mais em outra codificacao."""
    return lambda: arquivo.write_bytes(arquivo.read_bytes() + "çã".encode("latin-1") + b"\n")


def e_tabela_fora_do_utf8(v):
    tabela = PROJETO.caminho("lugares_lidos")
    return [tabela.name], fora_do_utf8(tabela)


def e_falta_a_tabela_dos_destinos(v):
    return [TABELA_DOS_DESTINOS.name], TABELA_DOS_DESTINOS.unlink


def e_cabecalho_dos_destinos(v):
    return [TABELA_DOS_DESTINOS.name], lambda: escreve_destinos(v["destinos"], destinos.CABECALHO[::-1])


def e_destino_repetido(v):
    v["destinos"].append(SORTEIO.choice(v["destinos"]))
    return [TABELA_DOS_DESTINOS.name, f"linha {len(v['destinos']) + 1}"], None


def e_destino_vazio_e_com_unidade(v):
    v["destinos"].append((next(p for p, u in v["destinos"] if u), ""))
    return [TABELA_DOS_DESTINOS.name, f"linha {len(v['destinos']) + 1}"], None


def e_destinos_fora_do_utf8(v):
    return [TABELA_DOS_DESTINOS.name], fora_do_utf8(TABELA_DOS_DESTINOS)


def e_destino_em_texto(v):
    campo = next(c for c in v["forma"]["campos"] if c.get("papel") == DESTINO)
    campo["forma"] = TEXTO
    del campo["separadores"]
    return [PROJETO.caminho("forma_analise").name], None


def e_ultima_aula(v):
    aula = ident()
    v["formato"]["ultima_aula"] = aula
    return [aula, ARQUIVO_FORMATO.name], None


def e_decisao_depois_da_ultima(v):
    aulas = v["ids"]["aulas"]
    v["formato"]["ultima_aula"] = aulas[0]
    doc(v["formato"], v["ids"], "partes")["unidades"][0]["tratada_em"] = [aulas[-1]]
    return [aulas[-1], ARQUIVO_FORMATO.name], None


def e_decisao_com_aula_desconhecida(v):
    aula = ident()
    doc(v["formato"], v["ids"], "partes")["unidades"][0]["tratada_em"] = [aula]
    return [aula, ARQUIVO_FORMATO.name], None


def com_valor_no_molde(chaves, valor):
    """O que grava o molde do formato com mais um valor aceito no lugar dado pelas chaves."""
    molde = json.loads(ESQUEMA_FORMATO.read_text(encoding="utf-8"))
    alvo = molde
    for chave in chaves:
        alvo = alvo[chave]
    alvo["enum"].append(valor)
    return lambda: escreve(ESQUEMA_FORMATO, molde)


def e_molde_que_o_script_nao_conhece(v):
    novo = ident()
    doc(v["formato"], v["ids"], "colunas")["molde"] = novo
    return [novo, ARQUIVO_FORMATO.name], com_valor_no_molde(("$defs", "documento", "properties", "molde"), novo)


def e_fonte_que_o_script_nao_conhece(v):
    nova = ident()
    v["formato"]["documentos_vem_de"].append(nova)
    return [nova, ARQUIVO_FORMATO.name], com_valor_no_molde(("properties", "documentos_vem_de", "items"), nova)


def e_falta_a_forma(v):
    forma = PROJETO.caminho("forma_analise")
    return [forma.name], forma.unlink


ENTRADAS_ERRADAS = [e_campo_na_forma, e_forma_sem_papel, e_marca_num_papel_que_a_forma_nao_da,
                    e_caminho_que_a_forma_nao_tem, e_linha_fora_da_forma, e_cabecalho_da_tabela,
                    e_linha_com_coluna_a_mais,
                    e_tabela_fora_do_utf8, e_falta_a_tabela_dos_destinos, e_cabecalho_dos_destinos,
                    e_destino_repetido, e_destino_vazio_e_com_unidade, e_destinos_fora_do_utf8, e_destino_em_texto,
                    e_ultima_aula, e_decisao_depois_da_ultima, e_decisao_com_aula_desconhecida,
                    e_molde_que_o_script_nao_conhece, e_fonte_que_o_script_nao_conhece, e_falta_a_forma]


# ---------- o material escrito: o que o conferidor do material tem de achar ----------

TextoEsperado = collections.namedtuple("TextoEsperado", "documento codigo nome aula regioes junto chave por_conjunto")
# um texto que o conferidor tem de achar: o documento, o codigo, o nome, a aula, as regioes, cada uma (item ou None, id
# da parte, trechos dela, se recebe trechos), os trechos que vao junto, a chave da unidade no limite (None, numa aula
# do documento de formas) e os trechos que estao numa regiao por um conjunto, cada um (item ou None, id da parte ou
# JUNTO, id do trecho)
AvisoEsperado = collections.namedtuple("AvisoEsperado", "tipo palavras estados")
# o que um caso do material errado tem de dar: uma linha do tipo, com as palavras, e o estado de cada texto que o caso
# muda ({codigo: estado}); os outros ficam prontos


def regioes_das_partes(d, u, entrada, f, trechos):
    """As regioes do texto de um documento de partes por tipo: cada parte da sequencia e, no documento com casos, a
    dos casos, que nao recebe trechos; e os trechos que vao junto."""
    regioes = [(None, p["id"], trechos(entrada, p["id"]), True) for p in f["partes_por_tipo"]]
    if d.get("casos"):
        regioes.append((None, confere_moldes.PARTE_DOS_CASOS, [], False))
    return regioes, trechos(entrada, JUNTO)


def regioes_da_grade(d, u, entrada, f, trechos):
    """As regioes do texto de um documento com grade: a abertura; e, na unidade sem itens, cada eixo da grade dela e,
    com a grade do documento, cada elo, que nao recebe trechos -- na unidade com itens, o mesmo em cada item com
    trecho."""
    u = u or {}
    regioes = [(None, a["id"], trechos(entrada, a["id"]) if a["recebe_trechos"] else [], a["recebe_trechos"])
               for a in d.get("abertura", [])]
    eixos_, elos = grade_da(d, u), ([] if u.get("eixos") else d.get("elos", []))
    coisas = ([i["id"] for i in u["itens"] if any(trechos(i["id"], x["id"]) for x in eixos_)] if u.get("itens")
              else [None])
    for i in coisas:
        regioes += [(i, x["id"], trechos(i or entrada, x["id"]), True) for x in eixos_]
        regioes += [(i, elo["id"], [], False) for elo in elos]
    return regioes, []


REGIOES_DO_TEXTO = {PARTES: regioes_das_partes, GRADE: regioes_da_grade}  # por tipo de molde dos documentos de conteudo


def textos_esperados(v, e):
    """Os textos que o conferidor tem de achar no mundo v, pelo que a conferencia dos moldes tem de achar nele (e), na
    ordem do formato: o de cada unidade com material de um documento de conteudo (o do documento inteiro, quando ele
    nao lista unidades), com a primeira aula, ate a ultima, que trata dela; e o de cada aula com trecho no documento
    de formas. Os trechos de cada regiao vem na ordem da leitura."""
    f, lim = v["formato"], e["limite"]
    na_leitura, saida = {i: k for k, i in enumerate(v["ordem"])}, []
    for d in f["documentos"]:
        lugares_, indiretos = e["lugares"][d["id"]], e["por_conjunto"][d["id"]]

        def trechos(entrada, parte):
            return sorted(lugares_.get((entrada, parte), ()), key=na_leitura.__getitem__)
        if d["molde"] == FORMAS:
            for aula in v["ids"]["aulas"]:
                regioes = [(None, str(n), trechos(aula, n), True) for n in range(1, len(d["formas"]) + 1)]
                if any(r[2] for r in regioes):
                    saida.append(TextoEsperado(d, aula, f"{d['unidade']} {aula}", aula, regioes, [], None,
                                               frozenset()))
        elif not d.get("todos"):
            for u in d.get("unidades") or [None]:
                chave_ = (d["id"], u["id"] if u else "")
                if chave_ in lim.com_material:
                    regioes, junto = REGIOES_DO_TEXTO[d["molde"]](d, u, chave_[1], f, trechos)
                    aula = next(a for a in lim.tratam[chave_] if a in e["ate"])
                    lugares_das_regioes = [(r[0], r[1], r[0] or chave_[1], r[1]) for r in regioes]
                    lugares_das_regioes.append((None, JUNTO, chave_[1], JUNTO))
                    por_conjunto = frozenset((item, parte, i) for item, parte, ent, p in lugares_das_regioes
                                             for i in indiretos.get((ent, p), ()))
                    saida.append(TextoEsperado(d, chave_[1] or d["id"], (u or d)["nome"], aula, regioes, junto, chave_,
                                               por_conjunto))
    return saida


def trechos_do(t):
    """Os trechos do texto t, sem repetir: os de cada regiao, na ordem, e os que vao junto."""
    return list(dict.fromkeys([i for r in t.regioes for i in r[2]] + list(t.junto)))


def em_ordem_de_escrita(textos, aulas):
    """[(texto, textos de que ele depende)] na ordem de escrita: os das unidades pela aula de cada um e, na mesma aula,
    na ordem do formato; o de cada aula do documento de formas logo depois do ultimo deles com trecho dela."""
    das_unidades, saida = sorted((t for t in textos if t.chave), key=lambda t: aulas.index(t.aula)), []
    for t in das_unidades:
        saida.append((t, []))
        for x in textos:
            deps = [y for y in das_unidades if set(trechos_do(y)) & set(trechos_do(x))]
            if not x.chave and deps and deps[-1] is t:
                saida.append((x, deps))
    return saida


# ---------- o material escrito: os textos, os arquivos e as planilhas ----------

def marca(nivel, codigo=None):
    """Um codigo escondido: o comentario com o nivel e o codigo, ou so com o nivel."""
    return f"<!-- {nivel} {codigo} -->" if codigo is not None else f"<!-- {nivel} -->"


def comentario():
    """Um comentario que nao e codigo escondido: o texto dele nao comeca por um nivel."""
    niveis = [*confere_material.NIVEIS.abrem, confere_material.NIVEIS.dentro]
    while True:
        p = palavra()
        if p not in niveis:
            return f"<!-- {p} {palavra()} -->"


def ruido():
    """Linhas que nao dao codigo nenhum: nada, um paragrafo, um bloco de codigo com uma marca de trecho, um paragrafo
    com uma marca de trecho em codigo na linha ou um comentario que nao e marca; o codigo dessas marcas nao existe."""
    falsa = marca(confere_material.TRECHO, ident())
    return SORTEIO.choice([[], [frase()], ["```", falsa, "```"], [f"{frase()} `{falsa}` {frase()}"], [comentario()]])


def linhas_do_texto(t, abre_as_que_nao_recebem=None):
    """As linhas do texto certo t: a marca da unidade, um titulo e, em cada regiao, na ordem, a marca dela -- a do item
    antes da primeira do item --, um paragrafo e a marca de cada trecho dela, as vezes no fim de um paragrafo; cada um
    dos que vao junto numa regiao sorteada que recebe trechos. A regiao sem trecho que recebe trechos fica de fora as
    vezes; a que nao recebe, tambem, ou sempre entra (True), ou nunca (False)."""
    cm = confere_material
    receptoras, do_junto = [k for k, r in enumerate(t.regioes) if r[3]], collections.defaultdict(list)
    for i in t.junto:
        do_junto[SORTEIO.choice(receptoras)].append(i)
    linhas_, item_aberto = [marca(cm.UNIDADE, t.codigo), f"# {nome()}", frase()], None
    for k, (item_, parte, trechos, recebe) in enumerate(t.regioes):
        codigos, sorteada = list(trechos) + do_junto[k], SORTEIO.random() < 0.5
        if not codigos and not (sorteada if recebe or abre_as_que_nao_recebem is None else abre_as_que_nao_recebem):
            continue
        if item_ is not None and item_ != item_aberto:
            linhas_ += [marca(cm.ITEM, item_), f"## {nome()}"]
            item_aberto = item_
        linhas_ += [marca(cm.PARTE, parte), frase()]
        for i in codigos:
            no_fim = SORTEIO.random() < 0.3  # a marca do trecho no fim de um paragrafo, ou numa linha so
            linhas_ += [f"{frase()} {marca(cm.TRECHO, i)}"] if no_fim else [marca(cm.TRECHO, i), frase()]
        linhas_ += ruido()
    return linhas_


def planilha_do(codigo):
    """A planilha do texto: o prefixo das planilhas, o codigo e .csv, na pasta do material gerado."""
    return MATERIAL / f"{PROJETO.valor('prefixo_planilhas')}{codigo}.csv"


def planilha_certa(t, colunas):
    """(cabecalho, cartoes) da planilha certa do texto t: os trechos dele em cartoes, as vezes com espacos a mais, um
    cartao a mais que repete um codigo, a aula do texto em cada cartao (com a coluna da aula) e colunas a mais, numa
    ordem sorteada."""
    da_coluna, da_aula = colunas
    trechos, extras = trechos_do(t), [ident() for _ in range(SORTEIO.randint(1, 2))]
    SORTEIO.shuffle(trechos)
    cartoes = em_pedacos(trechos, SORTEIO.randint(max(1, len(trechos) // 2), len(trechos)))
    cartoes.append([SORTEIO.choice(trechos)])
    linhas_ = [{da_coluna: SORTEIO.choice([" ", "  "]).join(c) + SORTEIO.choice(["", " "]),
                **({da_aula: t.aula} if da_aula else {}), **{x: frase() for x in extras}} for c in cartoes]
    cabecalho = [c for c in colunas if c] + extras
    return SORTEIO.sample(cabecalho, len(cabecalho)), linhas_


def material_certo(textos, colunas, abre_as_que_nao_recebem):
    """O material certo: {"textos": {codigo: linhas}, "arquivos": {caminho na pasta do material: [codigos]},
    "cabecas" e "fim": {caminho: linhas do comeco e do fim}, "planilhas": {codigo: (cabecalho, cartoes)}}. Os textos
    ficam em dois a quatro arquivos, cada texto num so -- um, pelo menos, num arquivo de uma subpasta e outro num
    arquivo fora delas --, e ha um arquivo sem texto; as regioes que nao recebem trechos entram em todos os textos
    (True) ou em nenhum (False); com a coluna dos trechos, cada texto de unidade tem a planilha dele."""
    nomes = [f"{ident()}/{ident()}.md", f"{ident()}.md"]
    for _ in range(SORTEIO.randint(0, 2)):
        nomes.append(f"{ident()}.md" if SORTEIO.random() < 0.5 else f"{ident()}/{ident()}.md")
    arquivos = {n: [] for n in nomes + [f"{ident()}/{ident()}.md"]}
    for k, t in enumerate(SORTEIO.sample(textos, len(textos))):  # um texto, pelo menos, numa subpasta e outro fora
        arquivos[nomes[k] if k < 2 else SORTEIO.choice(nomes)].append(t.codigo)
    return {"textos": {t.codigo: linhas_do_texto(t, abre_as_que_nao_recebem) for t in textos}, "arquivos": arquivos,
            "cabecas": {n: [f"# {nome()}", frase()] for n in arquivos}, "fim": {n: [] for n in arquivos},
            "planilhas": {t.codigo: planilha_certa(t, colunas) for t in textos if t.chave and colunas[0]}}


def linhas_do_arquivo(mat, n):
    """As linhas do arquivo n do material: o comeco, cada texto dele, com uma linha em branco depois, e o fim."""
    return mat["cabecas"][n] + [x for c in mat["arquivos"][n] for x in mat["textos"][c] + [""]] + mat["fim"][n]


def no_projeto(n):
    """O caminho do arquivo n do material a partir da pasta do projeto pequeno, como os avisos o mostram."""
    return (MATERIAL / n).relative_to(PROJ).as_posix()


def escreve_material(mat):
    """Grava o material numa pasta do material gerado nova: cada arquivo, um .txt com uma marca de trecho, que nao se
    le, e cada planilha."""
    if MATERIAL.exists():
        shutil.rmtree(MATERIAL)
    for n in mat["arquivos"]:
        (MATERIAL / n).parent.mkdir(parents=True, exist_ok=True)
        (MATERIAL / n).write_text("\n".join(linhas_do_arquivo(mat, n)) + "\n", encoding="utf-8")
    (MATERIAL / f"{ident()}.txt").write_text(marca(confere_material.TRECHO, ident()) + "\n", encoding="utf-8")
    for codigo, (cabecalho, cartoes) in mat["planilhas"].items():
        with open(planilha_do(codigo), "w", encoding="utf-8", newline="") as f:
            escritor = csv.DictWriter(f, fieldnames=cabecalho, extrasaction="ignore")
            escritor.writeheader()
            escritor.writerows(cartoes)


def projeto_com(**valores):
    """Um projeto.json a mais, na pasta do projeto pequeno, com os valores dados no lugar dos do modelo."""
    dados = json.loads((PROJ / comum.ARQUIVO_PROJETO).read_text(encoding="utf-8"))
    dados.update(valores)
    arquivo = PROJ / f"{ident()}.json"
    escreve(arquivo, dados)
    return arquivo


def roda_conferidor(projeto, *args):
    """(codigo de saida, linhas da tela) do conferidor do material, com o projeto.json dado."""
    return roda_tela("confere_material.py", "--projeto", str(projeto), *args)


def avisos_da_tela(tela):
    return [linha for linha in tela if linha.startswith((f"{ERRO}:", f"{FALTA}:"))]


def textos_da_tela(tela):
    """As linhas da tabela dos textos, sem o cabecalho: a aula, o documento, a unidade, o codigo e o estado."""
    return linhas_de_tabela(tela)[1:]


def estados_da_tela(tela):
    return {c[3]: c[4] for c in textos_da_tela(tela) if len(c) == 5}


def depois_do_rotulo(tela, rotulo):
    """O que vem depois do rotulo, em cada linha que comeca por ele."""
    return [linha[len(rotulo) + 2:] for linha in tela if linha.startswith(f"{rotulo}: ")]


def codigos_do_rotulo(tela, rotulo):
    """O codigo de cada linha que comeca pelo rotulo: o que vem logo depois dele."""
    return [resto.split(" ")[0] for resto in depois_do_rotulo(tela, rotulo)]


def linha_do_texto(t, estado):
    """A linha que a tabela dos textos tem de ter para o texto t, no estado dado."""
    return [t.aula or confere_material.NENHUM, t.documento["nome"], t.nome, t.codigo, estado]


# ---------- o material errado: cada caso muda uma copia do material e diz o aviso que ela tem de dar ----------

def um_texto(ctx, condicao=lambda t: True):
    """Um texto sorteado entre os que passam na condicao."""
    return SORTEIO.choice([t for t in ctx["textos"] if condicao(t)])


def abertas(linhas_, t):
    """[(indice da linha, item, id da parte, se recebe trechos)] das regioes que as linhas do texto t abrem, na ordem;
    o recebe e None na parte que o texto nao tem."""
    cm, recebe = confere_material, {(r[0], r[1]): r[3] for r in t.regioes}
    saida, item_ = [], None
    for k, linha in enumerate(linhas_):
        for nivel in (cm.ITEM, cm.PARTE):
            if linha.startswith(f"<!-- {nivel} ") and linha.endswith(" -->"):
                codigo = linha[len(f"<!-- {nivel} "):-len(" -->")]
                if nivel == cm.ITEM:
                    item_ = codigo
                else:
                    saida.append((k, item_, codigo, recebe.get((item_, codigo))))
    return saida


def regiao_aberta(mat, t, recebe=True):
    """(indice da linha da marca, item, id da parte) de uma regiao aberta do texto t, sorteada, que recebe trechos (ou
    que nao recebe, com recebe False); None, sem nenhuma."""
    achadas = [(k, i, p) for k, i, p, r in abertas(mat["textos"][t.codigo], t) if r is recebe]
    return SORTEIO.choice(achadas) if achadas else None


def alheios(ctx, t):
    """Os trechos dos outros textos que o texto t nao tem, em ordem."""
    return sorted({i for x in ctx["textos"] if x is not t for i in trechos_do(x)} - set(trechos_do(t)))


def poe_trecho(mat, t, codigo, recebe=True):
    """Poe a marca do trecho de codigo dado (sem codigo, com None) logo depois da marca de uma regiao aberta do texto
    t, sorteada, que recebe trechos (ou nao); devolve o id da parte."""
    k, _, parte = regiao_aberta(mat, t, recebe)
    mat["textos"][t.codigo].insert(k + 1, marca(confere_material.TRECHO, codigo))
    return parte


def m_falta(mat, ctx):
    t = um_texto(ctx)
    i, linhas_ = SORTEIO.choice(trechos_do(t)), mat["textos"][t.codigo]
    k = next(k for k, linha in enumerate(linhas_) if marca(confere_material.TRECHO, i) in linha)
    linhas_[k] = linhas_[k].replace(marca(confere_material.TRECHO, i), "")
    return AvisoEsperado(FALTA, [i, t.codigo], {t.codigo: FALTA}), None


def m_outra_regiao(mat, ctx):
    for t in SORTEIO.sample(ctx["textos"], len(ctx["textos"])):
        for k, item_, parte, recebe in abertas(mat["textos"][t.codigo], t):
            ali = next(r[2] for r in t.regioes if (r[0], r[1]) == (item_, parte))
            fora = [i for i in trechos_do(t) if i not in ali and i not in t.junto] if recebe else []
            if fora:
                i = SORTEIO.choice(fora)
                mat["textos"][t.codigo].insert(k + 1, marca(confere_material.TRECHO, i))
                return AvisoEsperado(ERRO, [i, parte, t.codigo], {t.codigo: ERRO}), None
    confere(False, "o material tem uma região aberta que recebe trechos e não espera um trecho do texto dela")
    return None, None


def m_parte_que_nao_recebe(mat, ctx):
    t = um_texto(ctx, lambda t: any(not r[3] for r in t.regioes))
    if regiao_aberta(mat, t, False) is None:
        mat["textos"][t.codigo] = linhas_do_texto(t, True)
    i = SORTEIO.choice(trechos_do(t))
    return AvisoEsperado(ERRO, [i, poe_trecho(mat, t, i, False), t.codigo], {t.codigo: ERRO}), None


def m_outra_unidade(mat, ctx):
    t = um_texto(ctx, lambda t: alheios(ctx, t))
    i = SORTEIO.choice(alheios(ctx, t))
    poe_trecho(mat, t, i)
    return AvisoEsperado(ERRO, [i, t.codigo], {t.codigo: ERRO}), None


def m_nao_existe(mat, ctx):
    t, i = um_texto(ctx), ident()
    poe_trecho(mat, t, i)
    return AvisoEsperado(ERRO, [i, t.codigo], {t.codigo: ERRO}), None


def m_fora_da_forma(mat, ctx):
    t = um_texto(ctx)
    poe_trecho(mat, t, SORTEIO.choice([None, f"{ident()} {ident()}"]))
    return AvisoEsperado(ERRO, [confere_material.TRECHO, t.codigo], {t.codigo: ERRO}), None


def m_parte_desconhecida(mat, ctx):
    t, parte = um_texto(ctx), ident()
    mat["textos"][t.codigo].append(marca(confere_material.PARTE, parte))
    return AvisoEsperado(ERRO, [parte, t.codigo], {t.codigo: ERRO}), None


def m_parte_repetida(mat, ctx):
    t = um_texto(ctx)
    linhas_ = mat["textos"][t.codigo]
    k, _, parte, _ = abertas(linhas_, t)[-1]
    linhas_.append(linhas_[k])
    return AvisoEsperado(ERRO, [parte, t.codigo], {t.codigo: ERRO}), None


def m_fora_de_ordem(mat, ctx):
    cm = confere_material
    for t in SORTEIO.sample(ctx["textos"], len(ctx["textos"])):
        linhas_ = mat["textos"][t.codigo]
        regioes = abertas(linhas_, t)
        dos_itens = [k for k, linha in enumerate(linhas_) if linha.startswith(f"<!-- {cm.ITEM} ")]
        cortes = [k for k, *_ in regioes] + dos_itens
        for (a, item_a, parte_a, _), (b, item_b, _, _) in zip(regioes, regioes[1:]):
            if item_a == item_b and not [k for k in cortes if a < k < b]:
                fim = min([k for k in cortes if k > b] + [len(linhas_)])
                linhas_[a:fim] = linhas_[b:fim] + linhas_[a:b]
                return AvisoEsperado(ERRO, [parte_a, t.codigo], {t.codigo: ERRO}), None
    confere(False, "o material tem um texto com duas regiões abertas seguidas no mesmo item")
    return None, None


def no_fim_de_um_arquivo(mat, linhas_):
    """Poe as linhas no fim de um arquivo sorteado do material; devolve o caminho dele, com a linha da primeira, como
    os avisos o mostram, e o ultimo texto do arquivo (None, sem texto)."""
    n = SORTEIO.choice(sorted(mat["arquivos"]))
    linha = len(linhas_do_arquivo(mat, n)) + 1
    mat["fim"][n] += linhas_
    return f"{no_projeto(n)}:{linha}", (mat["arquivos"][n] or [None])[-1]


def m_unidade_em_dois_lugares(mat, ctx):
    t = um_texto(ctx)
    onde, _ = no_fim_de_um_arquivo(mat, [marca(confere_material.UNIDADE, t.codigo)])
    return AvisoEsperado(ERRO, [onde, t.codigo], {t.codigo: ERRO}), None


def m_unidade_desconhecida(mat, ctx):
    cm, codigo = confere_material, ident()
    linhas_ = [marca(cm.UNIDADE, codigo), marca(cm.PARTE, ident()), marca(cm.TRECHO, ident())]
    onde, _ = no_fim_de_um_arquivo(mat, linhas_)
    return AvisoEsperado(ERRO, [onde, codigo], {}), None


def m_comentario_sem_fim(mat, ctx):
    onde, ultimo = no_fim_de_um_arquivo(mat, [f"{frase()} <!-- {palavra()}"])
    return AvisoEsperado(ERRO, [onde], {ultimo: ERRO} if ultimo else {}), None


def m_fora_de_unidade(mat, ctx):
    n, i = SORTEIO.choice(sorted(mat["arquivos"])), SORTEIO.choice(trechos_do(um_texto(ctx)))
    mat["cabecas"][n].insert(0, marca(confere_material.TRECHO, i))
    return AvisoEsperado(ERRO, [f"{no_projeto(n)}:1", i], {}), None


def m_texto_fora_do_utf8(mat, ctx):
    """O arquivo fora do UTF-8 nao se le: os textos dele ficam sem texto -- o de unidade com planilha, com FALTA."""
    n = SORTEIO.choice(sorted(x for x, codigos in mat["arquivos"].items() if codigos))
    estados = {c: FALTA if c in mat["planilhas"] else confere_material.SEM_TEXTO for c in mat["arquivos"][n]}
    return AvisoEsperado(ERRO, [no_projeto(n)], estados), fora_do_utf8(MATERIAL / n)


CASOS_DOS_TEXTOS = [m_falta, m_outra_regiao, m_parte_que_nao_recebe, m_outra_unidade, m_nao_existe, m_fora_da_forma,
                    m_parte_desconhecida, m_parte_repetida, m_fora_de_ordem, m_unidade_em_dois_lugares,
                    m_unidade_desconhecida, m_comentario_sem_fim, m_fora_de_unidade, m_texto_fora_do_utf8]


def com_os_cartoes(mat, t, mudar):
    """Troca os cartoes da planilha do texto t pelo que mudar(cabecalho, cartoes) da: (cabecalho, cartoes)."""
    mat["planilhas"][t.codigo] = mudar(*copy.deepcopy(mat["planilhas"][t.codigo]))


def p_sem_cartao(mat, ctx):
    da_coluna, t = ctx["colunas"][0], um_texto(ctx, lambda t: t.chave)
    i = SORTEIO.choice(trechos_do(t))

    def sem_ele(cabecalho, cartoes):
        com_outros = [{**c, da_coluna: " ".join(x for x in c[da_coluna].split() if x != i)} for c in cartoes]
        return cabecalho, [c for c in com_outros if c[da_coluna]]
    com_os_cartoes(mat, t, sem_ele)
    return AvisoEsperado(FALTA, [i, t.codigo], {t.codigo: FALTA}), None


def p_sem_planilha(mat, ctx):
    t = um_texto(ctx, lambda t: t.chave)
    del mat["planilhas"][t.codigo]
    return AvisoEsperado(FALTA, [planilha_do(t.codigo).name, t.codigo], {t.codigo: FALTA}), None


def p_com_codigo(mat, ctx, t, codigo):
    """Poe o codigo dado num cartao sorteado da planilha do texto t."""
    da_coluna, k = ctx["colunas"][0], SORTEIO.randrange(len(mat["planilhas"][t.codigo][1]))
    com_os_cartoes(mat, t, lambda cab, cartoes: (cab, [{**c, da_coluna: f"{c[da_coluna]} {codigo}"} if j == k else c
                                                      for j, c in enumerate(cartoes)]))


def p_outra_unidade(mat, ctx):
    t = um_texto(ctx, lambda t: t.chave and alheios(ctx, t))
    i = SORTEIO.choice(alheios(ctx, t))
    p_com_codigo(mat, ctx, t, i)
    return AvisoEsperado(ERRO, [i, t.codigo], {t.codigo: ERRO}), None


def p_nao_existe(mat, ctx):
    t, i = um_texto(ctx, lambda t: t.chave), ident()
    p_com_codigo(mat, ctx, t, i)
    return AvisoEsperado(ERRO, [i, t.codigo], {t.codigo: ERRO}), None


def p_sem_trecho(mat, ctx):
    (da_coluna, da_aula), t = ctx["colunas"], um_texto(ctx, lambda t: t.chave)
    sem_trecho = {da_coluna: SORTEIO.choice(["", " "]), da_aula: t.aula}
    com_os_cartoes(mat, t, lambda cab, cartoes: (cab, cartoes + [sem_trecho]))
    return AvisoEsperado(ERRO, [planilha_do(t.codigo).name, t.codigo], {t.codigo: ERRO}), None


def p_outra_aula(mat, ctx):
    da_aula, t = ctx["colunas"][1], um_texto(ctx, lambda t: t.chave)
    aula = SORTEIO.choice([a for a in ctx["aulas"] if a != t.aula])
    k = SORTEIO.randrange(len(mat["planilhas"][t.codigo][1]))
    com_os_cartoes(mat, t, lambda cab, cartoes: (cab, [{**c, da_aula: aula} if j == k else c
                                                      for j, c in enumerate(cartoes)]))
    return AvisoEsperado(ERRO, [repr(aula), t.codigo], {t.codigo: ERRO}), None


def p_sem_coluna(mat, ctx, coluna):
    t = um_texto(ctx, lambda t: t.chave)
    com_os_cartoes(mat, t, lambda cab, cartoes: ([c for c in cab if c != coluna], cartoes))
    return AvisoEsperado(ERRO, [repr(coluna), t.codigo], {t.codigo: ERRO}), None


def p_sem_coluna_dos_trechos(mat, ctx):
    return p_sem_coluna(mat, ctx, ctx["colunas"][0])


def p_sem_coluna_da_aula(mat, ctx):
    return p_sem_coluna(mat, ctx, ctx["colunas"][1])


def p_planilha_fora_do_utf8(mat, ctx):
    t = um_texto(ctx, lambda t: t.chave)
    return AvisoEsperado(ERRO, [planilha_do(t.codigo).name], {t.codigo: ERRO}), fora_do_utf8(planilha_do(t.codigo))


CASOS_DAS_PLANILHAS = [p_sem_cartao, p_sem_planilha, p_outra_unidade, p_nao_existe, p_sem_trecho, p_outra_aula,
                       p_sem_coluna_dos_trechos, p_sem_coluna_da_aula, p_planilha_fora_do_utf8]


# ---------- a lista de trabalho: o que a lista tem de ter e a leitura dela ----------

Bloco = collections.namedtuple("Bloco", "item parte trecho linhas")
# um trecho na lista: o item e a parte abertos ali (JUNTO, depois do titulo dos que vao junto), o codigo e as linhas
MARCA_ESCONDIDA = re.compile(r"`(<!-- (\S+) (\S+) -->)`")  # um codigo escondido mostrado em codigo na linha, na lista


def lugares_no_material(mat, existem):
    """{trecho: [(arquivo, linha, unidade, item, parte)]} de cada marca dos trechos que existem nos textos do material,
    pelo arquivo, pela linha e pelas marcas de regiao que o teste escreveu antes dela no arquivo."""
    cm, saida = confere_material, collections.defaultdict(list)
    for n in sorted(mat["arquivos"]):
        unidade_ = item_ = parte = None
        for k, linha in enumerate(linhas_do_arquivo(mat, n), 1):
            regiao = re.fullmatch(r"<!-- (\S+) (\S+) -->", linha)
            if regiao and regiao.group(1) == cm.UNIDADE:
                unidade_, item_, parte = regiao.group(2), None, None
            elif regiao and regiao.group(1) == cm.ITEM:
                item_, parte = regiao.group(2), None
            elif regiao and regiao.group(1) == cm.PARTE:
                parte = regiao.group(2)
            for i in existem:
                if marca(cm.TRECHO, i) in linha:
                    saida[i].append((no_projeto(n), k, unidade_, item_, parte))
    return saida


def le_lista(texto):
    """(identidade, marcas, blocos, textos das regioes, capitulos) da lista gravada: as linhas antes da primeira secao;
    os codigos escondidos das regioes, em ordem, cada um (nivel, codigo); cada trecho, como Bloco; as linhas de cada
    regiao que nao sao de trecho, {(item, parte): linhas}; e as linhas da secao dos capitulos."""
    lt, cm = lista_de_trabalho, confere_material
    linhas_ = texto.splitlines()
    inicio = next((k for k, x in enumerate(linhas_) if x.startswith("## ")), len(linhas_))
    marcas_, blocos, textos_, item_, parte = [], [], collections.defaultdict(list), None, None
    for linha in secao(texto, lt.PARTES):
        achadas = [(nivel, codigo) for _, nivel, codigo in MARCA_ESCONDIDA.findall(linha)]
        if linha == f"### {lt.JUNTO}":
            item_, parte = None, JUNTO
        elif linha.startswith("- ") and achadas and achadas[0][0] == cm.TRECHO:
            blocos.append(Bloco(item_, parte, achadas[0][1], []))
        elif linha.startswith("  - ") and blocos:
            blocos[-1].linhas.append(linha)
        elif achadas:
            marcas_ += achadas
            for nivel, codigo in achadas:
                if nivel == cm.ITEM:
                    item_, parte = codigo, None
                elif nivel == cm.PARTE:
                    parte = codigo
        elif linha.strip():
            textos_[(item_, parte)].append(linha)
    return linhas_[:inicio], marcas_, blocos, textos_, secao(texto, lt.CAPITULOS)


def marcas_esperadas(t):
    """Os codigos escondidos das regioes que a lista do texto t tem de mostrar, em ordem: o da unidade e, em cada
    regiao, o do item quando ele muda, e o da parte."""
    cm, saida, aberto = confere_material, [(confere_material.UNIDADE, t.codigo)], None
    for item_, parte, _, _ in t.regioes:
        if item_ is not None and item_ != aberto:
            saida.append((cm.ITEM, item_))
            aberto = item_
        saida.append((cm.PARTE, parte))
    return saida


def valor_esperado(caso, campo, v):
    """O valor de um campo do trecho na lista: o do campo com papel, os valores dele, separados por virgula, ou o vazio
    da forma; o do campo sem papel, o texto dele na analise."""
    papel, forma = campo.get("papel"), v["forma"]
    if papel is None:
        return texto_do_campo(caso, campo, v).strip()
    valores = {TIPO: caso["tipos"], GRUPO: caso["grupos"],
               CAMINHO: [x for x in campo.get("valores", []) if x in caso["caminhos"]]}[papel]
    return ", ".join(valores) or forma["vazio"]


def em_ordem_no(texto, pedacos_):
    """Se cada pedaco esta no texto, cada um depois do anterior."""
    k = 0
    for p in pedacos_:
        k = texto.find(p, k)
        if k < 0:
            return False
        k += len(p)
    return True


def formas_da(d):
    """As formas da divergencia d, a ensinada primeiro."""
    return [d["ensinada"]] + d["outras"]


def diz_a_divergencia(linha, d):
    """Se a linha tem o fato da divergencia d e, na ordem, o que cada forma diz e a citacao dela, a ensinada
    primeiro."""
    return em_ordem_no(linha, [d["fato"]] + [x for f in formas_da(d) for x in (f["diz"], f["fonte"])])


def confere_bloco(b, t, v, e, onde, divs, rotulo):
    """As linhas de um trecho na lista: o texto; cada campo da forma, menos o do destino, com o valor dele; as marcas do
    caso, so quando ele tem; e, so quando e assim, que ele esta ali por um conjunto, que e de uma aula depois da ultima,
    cada divergencia de divs com o codigo dele, na ordem do arquivo, e onde ele esta no material de que o texto
    depende."""
    lt, caso, forma = lista_de_trabalho, e["caso"][b.trecho], v["forma"]
    suas = [d for d in divs if b.trecho in d["trechos"]]
    da_lista = [x for x in b.linhas if x.startswith(f"  - {lt.DIVERGENCIA}: ")]
    confere(len(da_lista) == len(suas) and all(diz_a_divergencia(x, d) for x, d in zip(da_lista, suas)),
            f"{rotulo}: as divergências do trecho {b.trecho}, na ordem do arquivo: {da_lista} ({suas})")
    confere(b.linhas[:1] == [f"  - {caso['texto']}"], f"{rotulo}: o texto do trecho {b.trecho}: {b.linhas[:1]}")
    for campo in forma["campos"]:
        do_campo = [x for x in b.linhas if x.startswith(f"  - {campo['nome']}:")]
        certo = [] if campo.get("papel") == DESTINO else [f"  - {campo['nome']}: {valor_esperado(caso, campo, v)}"]
        confere(do_campo == certo, f"{rotulo}: o campo {campo['nome']} do trecho {b.trecho}: {do_campo} ({certo})")
    postas = {x for x, _ in caso["marcas"]}
    nomes = [mk["nome"] for mk in v["formato"]["marcas"] if mk["id"] in postas]
    confere([x for x in b.linhas if x.startswith(f"  - {lt.MARCAS}:")]
            == ([f"  - {lt.MARCAS}: {', '.join(nomes)}"] if nomes else []),
            f"{rotulo}: as marcas do trecho {b.trecho}, só quando ele tem: {b.linhas}")
    por_conjunto = (b.item, b.parte, b.trecho) in t.por_conjunto
    confere((f"  - {lt.POR_CONJUNTO}" in b.linhas) == por_conjunto,
            f"{rotulo}: o trecho {b.trecho} está ali por um conjunto ({por_conjunto}): {b.linhas}")
    depois = caso["aula"] not in e["ate"]
    confere((f"  - {lt.DEPOIS.format(v['formato']['ultima_aula'])}" in b.linhas) == depois,
            f"{rotulo}: o trecho {b.trecho} é de uma aula depois da última ({depois}): {b.linhas}")
    ensinado = [x for x in b.linhas if x.startswith(f"  - {lt.ENSINADO_EM}: ")]
    confere(len(ensinado) == len(onde.get(b.trecho, [])) and all(
        sum(f"`{arq}`" in x and numeros(x) == [k] and all(tem_id(x, y) for y in (u, item_, parte) if y)
            for x in ensinado) == 1 for arq, k, u, item_, parte in onde.get(b.trecho, [])),
            f"{rotulo}: onde o trecho {b.trecho} está no material: {ensinado} ({onde.get(b.trecho, [])})")


def capitulos_esperados(t, v, e, inteiro=False):
    """(transcricoes, {pedaco: ids}) que a lista do texto t tem de mostrar: as transcricoes da fonte do campo das
    paginas citadas em algum pedaco de um trecho do texto, na ordem natural dos nomes; e os pedacos que nao citam
    nenhuma, com os trechos de cada um, na ordem em que aparecem. Com inteiro, o campo inteiro de cada trecho e um
    pedaco so."""
    cita, citadas, sem_pagina = {p: arqs for p, arqs in v["pedacos"]}, set(), {}
    for i in trechos_do(t):
        caso = e["caso"][i]
        pedacos_ = ([(caso["separador_das_paginas"].join(caso["paginas"]), caso["paginas"])] if inteiro
                    else [(p, [p]) for p in caso["paginas"]])
        for texto, partes_ in pedacos_:
            arqs = set().union(*(cita[p] for p in partes_))
            citadas |= arqs
            if texto and not arqs:
                sem_pagina.setdefault(texto, []).append(i)
    return [x.arquivo for x in v["paginas"] if x.arquivo in citadas], sem_pagina


def confere_capitulos(linhas_, t, v, e, rotulo, inteiro=False):
    """A secao dos capitulos da lista do texto t: as transcricoes a ler, na ordem, e os pedacos sem pagina, cada um com
    os trechos dele, em ordem."""
    lt, campo = lista_de_trabalho, campo_das_paginas(v["forma"])
    arquivos, sem_pagina = capitulos_esperados(t, v, e, inteiro)
    k = next((j for j, x in enumerate(linhas_) if x == f"{lt.SEM_PAGINA}:"), len(linhas_))
    listadas = [x for x in linhas_[:k] if x.startswith("- ")]
    certas = [f"- `{a.relative_to(PROJ).as_posix()}`" for a in arquivos]
    confere(any(x == f"### {lt.DO_CAMPO.format(campo['nome'], campo['fonte'])}" for x in linhas_)
            and listadas == certas,
            f"{rotulo}: as transcrições a ler, na ordem natural dos nomes: {listadas} ({certas})")
    pedacos_ = [x for x in linhas_[k + 1:] if x.startswith("- ")]
    confere(len(pedacos_) == len(sem_pagina) and all(
        x.startswith(f"- {p} ") and [i for i in ids if tem_id(x, i)] == ids
        and all(x.index(f"`{a}`") < x.index(f"`{b}`") for a, b in zip(ids, ids[1:]))
        for x, (p, ids) in zip(pedacos_, sem_pagina.items())),
            f"{rotulo}: os pedaços sem página, com os trechos: {pedacos_} ({sem_pagina})")


def confere_identidade(linhas_, t, deps, e, colunas, rotulo):
    """O comeco da lista do texto t: o nome e o codigo, o documento e a aula; no texto de uma unidade, as aulas que
    tratam e as que so mencionam, na ordem, a planilha, com as colunas, e a prova; no que depende de outros, esses."""
    lt, lim = lista_de_trabalho, e["limite"]

    def do_rotulo(r):
        return [x[len(f"- {r}: "):] for x in linhas_ if x.startswith(f"- {r}: ")]
    unidade_, documento_, aula_ = do_rotulo(lt.UNIDADE), do_rotulo(lt.DOCUMENTO), do_rotulo(lt.AULA)
    confere(len(unidade_) == 1 and t.nome in unidade_[0] and f"`{t.codigo}`" in unidade_[0]
            and documento_ == [t.documento["nome"]] and aula_ == [t.aula],
            f"{rotulo}: o nome, o código, o documento e a aula: {linhas_}")
    planilha_, prova_ = do_rotulo(lt.PLANILHA), do_rotulo(lt.PROVA)
    if t.chave:
        arquivo = planilha_do(t.codigo)
        tratam = [a.split(", ") for a in do_rotulo(lt.TRATAM)]
        mencionam = [a.split(", ") for a in do_rotulo(lt.MENCIONAM)]
        confere(tratam == [lim.tratam[t.chave]] and mencionam == [lim.mencionam.get(t.chave) or [lt.NENHUM]],
                f"{rotulo}: as aulas que tratam e as que só mencionam: {linhas_}")
        prova_certa = PROJETO.caminho_com("provas", arquivo.stem).relative_to(PROJ).as_posix()
        confere(len(planilha_) == 1 and f"`{arquivo.relative_to(PROJ).as_posix()}`" in planilha_[0]
                and all(f"`{c}`" in planilha_[0] for c in colunas if c) and tem_id(planilha_[0], t.aula)
                and prova_ == [f"`{prova_certa}`"],
                f"{rotulo}: a planilha, com as colunas e a aula, e a prova: {linhas_}")
    else:
        confere(not planilha_ and not prova_, f"{rotulo}: sem planilha nem prova: {linhas_}")
    depende = do_rotulo(lt.DEPENDE)
    confere(depende == ([", ".join(f"`{d.codigo}`" for d in deps)] if deps else []),
            f"{rotulo}: os textos de que ele depende: {depende}")


def confere_lista(t, deps, ctx, onde, rotulo):
    """A lista gravada do texto t: o comeco; os codigos escondidos das regioes, na ordem do molde; os trechos de cada
    regiao, na ordem, e os que vao junto, cada um com as linhas dele; o aviso das regioes que nao recebem trechos e das
    que recebem e nao tem nenhum; e os capitulos. Devolve o texto da lista."""
    lt, v, e = lista_de_trabalho, ctx["mundo"], ctx["esperado"]
    arquivo = PROJETO.caminho_com("listas_de_trabalho", f"{t.documento['id']}-{t.codigo}")
    if not confere(arquivo.is_file(), f"{rotulo}: a lista é gravada em {arquivo}"):
        return ""
    texto = arquivo.read_text(encoding="utf-8")
    identidade_, marcas_, blocos, textos_, capitulos_ = le_lista(texto)
    confere_identidade(identidade_, t, deps, e, ctx["colunas"], rotulo)
    confere(marcas_ == marcas_esperadas(t), f"{rotulo}: os códigos escondidos das regiões, na ordem do molde: "
            f"{marcas_} ({marcas_esperadas(t)})")
    certos = [(item_, parte, i) for item_, parte, trechos, _ in t.regioes for i in trechos]
    certos += [(None, JUNTO, i) for i in t.junto]
    confere([(b.item, b.parte, b.trecho) for b in blocos] == certos, f"{rotulo}: os trechos de cada região, na ordem")
    for b in blocos:
        confere_bloco(b, t, v, e, onde, ctx["divergencias"], rotulo)
    for item_, parte, trechos, recebe in t.regioes:
        aviso_ = [] if trechos else [lt.NAO_RECEBE if not recebe else lt.SEM_TRECHO]
        confere(textos_.get((item_, parte), []) == aviso_, f"{rotulo}: o aviso da região {parte}: "
                f"{textos_.get((item_, parte))} ({aviso_})")
    confere_capitulos(capitulos_, t, v, e, rotulo)
    return texto


# ---------- as divergencias: as chamadas, o arquivo delas e o documento ----------

def sorteia_chamadas(v):
    """{chave: nucleo} de cada fonte registrada nas transcricoes do mundo v, com uma chamada inventada, gravadas no
    arquivo de chamadas."""
    nucleos = {c: f"{palavra().capitalize()}, {SORTEIO.randint(1900, 2099)}"
               for c in sorted({t.chave for t in v["paginas"] if t.chave})}
    escreve(PROJETO.caminho("chamadas"), {"versao_schema": VERSAO_CHAMADAS,
                                          "chamadas": [{"chave": c, "chamada": f"({n})"} for c, n in nucleos.items()]})
    return nucleos


def citacao_inventada(v, nucleos):
    """Uma citacao das fontes do mundo v, como a coluna fonte: uma ou duas chamadas, cada uma com uma pagina que uma
    transcricao registrada com a fonte dela tem."""
    lugares_ = [(t.chave, r) for t in v["paginas"] if t.chave for r in t.rotulos]
    return "(" + "; ".join(f"{nucleos[c]}, {r}" for c, r in SORTEIO.sample(lugares_, SORTEIO.randint(1, 2))) + ")"


def divergencia_inventada(codigos_, v, nucleos, fonte_da_outra=None):
    """Uma divergencia dos trechos de codigos dados: o fato, a forma ensinada e uma ou duas outras, cada uma com uma
    citacao das fontes do mundo v; com fonte_da_outra, uma outra so, com essa citacao."""
    def forma(fonte=None):
        return {"diz": nome(), "fonte": fonte or citacao_inventada(v, nucleos)}
    outras = [forma(fonte_da_outra)] if fonte_da_outra else [forma() for _ in range(SORTEIO.randint(1, 2))]
    return {"fato": frase(), "trechos": list(codigos_), "ensinada": forma(), "outras": outras}


def grava_divergencias(lista):
    escreve(DIVERGENCIAS, {"versao_schema": VERSAO_DIVERGENCIAS, "divergencias": lista})


def sorteia_divergencias(ctx, nucleos):
    """Grava as divergencias do mundo, numa ordem sorteada: uma com dois trechos de um texto, guardados em
    ctx["dois_do_cartao"] para um cartao que tenha os dois; uma com um deles e um trecho de outro texto, para que um
    trecho fique em duas; e uma com um trecho que nenhum texto tem. Guarda a lista em ctx["divergencias"]."""
    v, textos = ctx["mundo"], ctx["textos"]
    um = SORTEIO.choice([t for t in textos if len(trechos_do(t)) > 1] or textos)
    dois = SORTEIO.sample(trechos_do(um), min(2, len(trechos_do(um))))
    outro = SORTEIO.choice(trechos_do(SORTEIO.choice([t for t in textos if t is not um] or textos)))
    nos_textos_ = {i for t in textos for i in trechos_do(t)}
    soltos = [i for i in v["ordem"] if i not in nos_textos_]
    confere(soltos, "o mundo tem trecho que nenhum texto tem")
    lista = [divergencia_inventada(dois, v, nucleos),
             divergencia_inventada(dict.fromkeys([dois[0], outro]), v, nucleos)]
    lista += [divergencia_inventada([SORTEIO.choice(soltos)], v, nucleos) for _ in soltos[:1]]
    SORTEIO.shuffle(lista)
    grava_divergencias(lista)
    ctx["divergencias"], ctx["dois_do_cartao"] = lista, dois


def com_perguntas(mat, dois, coluna):
    """Uma copia do material com a coluna da pergunta em cada planilha e uma pergunta em cada cartao, menos num
    sorteado, e um cartao a mais com os dois codigos dados, numa planilha sorteada."""
    copia = copy.deepcopy(mat)
    for cabecalho, cartoes in copia["planilhas"].values():
        cabecalho.append(comum.COLUNA_PERGUNTA)
        for c in cartoes:
            c[comum.COLUNA_PERGUNTA] = frase()
    _, cartoes = copia["planilhas"][SORTEIO.choice(sorted(copia["planilhas"]))]
    cartoes.append({coluna: " ".join(dois), comum.COLUNA_PERGUNTA: frase()})
    SORTEIO.choice([c for _, cs in copia["planilhas"].values() for c in cs])[comum.COLUNA_PERGUNTA] = ""
    return copia


def roda_divergencias(projeto, *args):
    """(codigo de saida, linhas da tela) do documento das divergencias, com o projeto.json dado."""
    return roda_tela("divergencias.py", "--projeto", str(projeto), *args)


def documento_gravado():
    return DOCUMENTO.read_bytes() if DOCUMENTO.is_file() else None


def regioes_esperadas(ctx):
    """{(unidade, item, parte): [nome do item, nome da parte]} de cada regiao dos textos do material, como o conferidor
    do material as da; o item fica de fora na parte que nao esta num item."""
    conferido, erros = confere_material.confere(comum.acha_projeto(ctx["projeto"]))
    confere(not erros, f"o conferidor do material dá as regiões dos textos: {erros}")
    if erros:
        return {}
    return {(t.codigo, p.item["id"] if p.item else None, p.id): ([p.item["nome"]] if p.item else []) + [p.nome]
            for t, _ in conferido.lista for p in t.partes}


Uso = collections.namedtuple("Uso", "arquivo posicao nomes")
# uma parte do material que o documento tem de mostrar: o arquivo; a linha, num texto, ou o numero do cartao; e os nomes
# que a linha dela tem de ter (o titulo do arquivo e os da regiao, ou a pergunta do cartao)


def usos_esperados(d, mat, regioes, ctx, com_cartoes=True):
    """([Uso] dos textos, [Uso] dos cartoes) que o documento tem de mostrar para a divergencia d no material mat: cada
    linha de texto com a marca de um trecho dela, sem repetir, na ordem dos caminhos e das linhas; e, com os cartoes,
    cada cartao com um trecho dela na coluna dos trechos, na ordem das planilhas e dos cartoes."""
    lugares_, vistos, textos = lugares_no_material(mat, ctx["mundo"]["ordem"]), set(), []
    for c in d["trechos"]:
        for arq, n, unidade_, item_, parte in lugares_.get(c, []):
            if (arq, n) not in vistos:
                vistos.add((arq, n))
                titulo = mat["cabecas"][(PROJ / arq).relative_to(MATERIAL).as_posix()][0].lstrip("# ")
                textos.append(Uso(PROJ / arq, n, [titulo] + regioes.get((unidade_, item_, parte), [])))
    coluna, cartoes = ctx["colunas"][0], []
    for codigo, (_, cartoes_) in mat["planilhas"].items() if com_cartoes else []:
        cartoes += [Uso(planilha_do(codigo), k, [c.get(comum.COLUNA_PERGUNTA) or ""])
                    for k, c in enumerate(cartoes_, 1) if set(c[coluna].split()) & set(d["trechos"])]
    return (sorted(textos, key=lambda u: (u.arquivo, u.posicao)), sorted(cartoes, key=lambda u: (u.arquivo, u.posicao)))


def linha_do_uso(linhas_, uso, texto):
    """O indice da unica linha das partes do material que mostra o uso, ou None: num texto, o link para a linha e os
    nomes; num cartao, o link para a planilha, o numero do cartao e a pergunta."""
    alvo = Path(os.path.relpath(uso.arquivo, DOCUMENTO.parent)).as_posix()
    if texto:
        achadas = [k for k, x in enumerate(linhas_)
                   if f"]({alvo}#L{uso.posicao})" in x and all(n in x for n in uso.nomes)]
    else:
        rotulo = re.compile(rf"{re.escape(divergencias.CARTAO.format(uso.posicao))}(?!\d)")
        achadas = [k for k, x in enumerate(linhas_) if f"]({alvo})" in x and rotulo.search(x)
                   and all(n in x for n in uso.nomes)]
    return achadas[0] if len(achadas) == 1 else None


def confere_documento(lista, mat, ctx, regioes, rotulo, com_cartoes=True):
    """O documento gravado: um titulo de segundo nivel para cada divergencia, na ordem do arquivo; em cada um, a forma
    ensinada e as outras, na ordem, cada uma com o que diz e a citacao; e, so quando ha, as partes do material que
    tratam do fato, uma linha cada: as linhas dos textos, com o link e os nomes, e, depois, os cartoes, com a planilha,
    o numero e a pergunta, cada grupo em ordem."""
    texto = DOCUMENTO.read_text(encoding="utf-8") if DOCUMENTO.is_file() else ""
    titulos_ = [x[3:] for x in texto.splitlines() if x.startswith("## ")]
    confere(titulos_ == [d["fato"] for d in lista],
            f"{rotulo}: um título para cada divergência, na ordem do arquivo: {titulos_}")
    for d in lista:
        linhas_ = secao(texto, d["fato"])
        formas_ = [x for x in linhas_ if x.startswith("- ") and not x.startswith(f"- {divergencias.TRATAM}")]
        confere(len(formas_) == len(formas_da(d))
                and all(em_ordem_no(x, [f["diz"], f["fonte"]]) for x, f in zip(formas_, formas_da(d))),
                f"{rotulo}: as formas de {d['fato']!r}, a ensinada primeiro: {formas_}")
        textos, cartoes = usos_esperados(d, mat, regioes, ctx, com_cartoes)
        usos_ = [x for x in linhas_ if x.startswith("  - ")]
        posicoes = [linha_do_uso(usos_, u, True) for u in textos] + [linha_do_uso(usos_, u, False) for u in cartoes]
        confere((f"- {divergencias.TRATAM}:" in linhas_) == bool(posicoes) and len(usos_) == len(posicoes)
                and None not in posicoes and posicoes == sorted(posicoes),
                f"{rotulo}: as partes do material que tratam de {d['fato']!r}, só quando há, uma linha cada, na ordem: "
                f"{usos_} ({textos}; {cartoes})")


def divergencias_que_param(ctx, rotulo, palavras, projeto=None):
    """O documento das divergencias sai com codigo 1, com uma linha ERRO que diz as palavras, e nada e gravado."""
    antes = documento_gravado()
    codigo, tela = roda_divergencias(projeto or ctx["projeto"])
    confere(codigo == 1 and any(x.startswith(f"{ERRO}:") and all(p in x for p in palavras) for x in tela)
            and documento_gravado() == antes, f"{rotulo}: ERRO que diz {palavras}, e nada é gravado: {tela}")


# ---------- os testes ----------

def teste_moldes_declaram():
    """Se o molde do formato declara os tipos de molde e as fontes dos documentos que o teste
    monta; o da forma das analises, os papeis e as formas de campo que ele usa; e os moldes do
    formato e da base, os valores que ele sorteia."""
    return all([
        confere(set(aceitos(MOLDE, "$defs", "documento", "properties", "molde")) == set(TIPOS_DE_MOLDE),
                "o molde do formato declara os tipos de molde que o teste monta"),
        confere(set(FONTES) == set(FONTES_DO_TESTE), "o molde do formato declara as fontes que o teste monta"),
        confere(set(PAPEIS_DO_TESTE) <= set(PAPEIS)
                and set(FORMAS_DE_CAMPO) <= set(aceitos(MOLDE_FORMA, "$defs", "campo", "properties", "forma"))
                and "fonte" in MOLDE_FORMA["$defs"]["campo"]["properties"],
                "o molde da forma das análises declara os papéis, as formas de campo e a fonte das páginas que o "
                "teste usa"),
        confere(ORDENS and LADOS and AFIRMACOES and OUTRAS_CLASSES and OUTRAS_COBERTURAS and USA in CLASSES
                and DA_FONTE in COBERTURAS,
                "os moldes do formato e da base declaram os valores que o teste sorteia"),
        confere(isinstance(MINIMO_PARTES, int) and MINIMO_PARTES >= 1,
                f"o molde do formato pede pelo menos uma parte para tratar: {MINIMO_PARTES!r}")])


def teste_formato_certo(formato):
    escreve(ARQUIVO_FORMATO, formato)
    codigo, erros = valida(ARQUIVO_FORMATO)
    confere(codigo == 0 and not erros, f"o formato certo passa no molde: {erros}")
    branco = MODELO.parent / ARQUIVO_FORMATO.name
    codigo, erros = valida(branco)
    trocados = []
    preenchido = preenche(json.loads(branco.read_text(encoding="utf-8")), MOLDE, trocados)
    confere(codigo != 0 and trocados and len(erros) == len(trocados)
            and all(any(f"{c}:" in e for e in erros) for c in trocados),
            f"o modelo em branco do formato falha na validação só onde espera um valor, com um erro em cada "
            f"lugar ({', '.join(trocados)}): {erros}")
    escreve(ARQUIVO_FORMATO, preenchido)
    codigo, erros = valida(ARQUIVO_FORMATO)
    confere(codigo == 0 and not erros, f"preenchido pelo molde, o modelo em branco passa: {erros}")


def teste_campos_do_topo(formato):
    """Cada campo do topo do formato e obrigatorio: sem ele, um erro so, que diz o campo."""
    for campo in formato:
        f = copy.deepcopy(formato)
        del f[campo]
        escreve(ARQUIVO_FORMATO, f)
        codigo, erros = valida(ARQUIVO_FORMATO)
        confere(codigo != 0 and len(erros) == 1 and campo in erros[0],
                f"sem o campo {campo!r} do topo, um erro só, que diz o campo: {erros}")


def entradas_montadas(formato, d):
    """{id: (unidade, item)} de cada unidade do documento (com o item None) e de cada item dela."""
    return {(i or u)["id"]: (u, i) for doc_, u, i in unidades_e_itens(formato) if doc_ is d}


def campos_das_entradas(entradas):
    return [(e.documento, e.unidade, e.item, e.direto) for e in entradas]


def teste_listas_do_formato(formato):
    """Se o comum.py da as listas do formato sorteado: as unidades de cada documento, os itens
    de cada unidade e os conjuntos de cada documento. O resto do teste se apoia nelas."""
    documentos = formato["documentos"]
    return all(
        [confere(comum.unidades(d) == d.get("unidades", []), f"as unidades do documento {d['id']} são as dele")
         for d in documentos]
        + [confere(comum.itens(u) == u.get("itens", []), f"os itens da unidade {u['id']} são os dela")
           for d in documentos for u in d.get("unidades", [])]
        + [confere(comum.conjuntos(d) == d.get("conjuntos", []), f"os conjuntos do documento {d['id']} são os dele")
           for d in documentos])


def teste_o_que_se_acha(formato):
    for d in formato["documentos"]:
        montadas = entradas_montadas(formato, d)
        for i, (u, item_) in montadas.items():
            confere(campos_das_entradas(comum.o_que_e(formato, i)) == [(d, u, item_, True)],
                    f"o id {i} quer dizer a unidade ou o item dele, no documento {d['id']}, como lugar direto")
        for c in d.get("conjuntos", []):
            confere(campos_das_entradas(comum.o_que_e(formato, c["id"]))
                    == [(d, *montadas[m], False) for m in c["membros"]],
                    f"o conjunto {c['id']} quer dizer cada membro dele, na ordem, como lugar indireto")
            confere(comum.acha_unidade(formato, c["id"]) == (None, None),
                    f"o conjunto {c['id']} não se acha como unidade")
        for u in d.get("unidades", []):
            confere(comum.acha_unidade(formato, u["id"]) == (d, u), f"a unidade {u['id']} se acha no documento dela")
            for item_ in u.get("itens", []):
                confere(comum.acha_unidade(formato, item_["id"]) == (None, None),
                        f"o item {item_['id']} não se acha como unidade")
            confere(comum.grade(d, u) == grade_da(d, u),
                    f"a grade da unidade {u['id']}: os eixos dela, ou, sem eles, os do documento")
        for e in d.get("eixos", []) + [e for u in d.get("unidades", []) for e in u.get("eixos", [])]:
            confere(comum.linhas_do_eixo(e) == linhas(e),
                    f"as linhas do eixo {e['id']} são os subtópicos dele, ou ele mesmo")
    desconhecido = ident()
    confere(comum.acha_unidade(formato, desconhecido) == (None, None), "um id que nenhum documento tem não se acha")
    confere(comum.o_que_e(formato, desconhecido) == [], "um id que o formato não tem não quer dizer nada")


def teste_bases(formato, bases, lugar, lidas):
    """A base de cada unidade com a grade dela, e duas rodadas iguais."""
    escreve(ARQUIVO_FORMATO, formato)
    usadas = []
    for u, eixos_ in bases:
        dados, usada, frase_usada = base_com_grade(u["id"], eixos_, lugar, lidas)
        escreve(PROJETO.caminho_com("bases", u["id"]), dados)
        usadas.append((usada, frase_usada))
    codigo, erros = roda_base()
    confere(not erros, f"o formato certo e as bases certas não dão erro: {erros}")
    for (u, eixos_), (usada, frase_usada) in zip(bases, usadas):
        confere_base(u, eixos_, usada, frase_usada)
    certos = gravados()
    roda_base()
    confere(gravados() == certos, "duas rodadas dão os mesmos arquivos")


def teste_conferencia(m):
    """A conferencia dos moldes no mundo da conferencia, com cada valor das fontes dos
    documentos, e duas rodadas iguais."""
    for fontes in valores_das_fontes():
        texto = confere_rodada(com_fontes(m, fontes), f"fontes {fontes}")
    roda_conferencia()
    confere(RELATORIO.exists() and RELATORIO.read_text(encoding="utf-8") == texto, "duas rodadas, o mesmo relatório")


def teste_limite(m):
    """A conferencia no mundo do limite, e as regras do limite vistas no relatorio dele."""
    v = mundo_do_limite(m)
    confere_regras_do_limite(confere_rodada(v, "limite"), v)


def teste_formato_errado(formato, ids, certos):
    """Cada erro do formato, na base e na conferencia dos moldes."""
    for caso in CASOS:
        f = copy.deepcopy(formato)
        descricao, lugar = caso(f, ids)
        escreve(ARQUIVO_FORMATO, f)
        for script, (codigo, erros) in [("base_externa.py", roda_base()),
                                        ("confere_moldes.py", roda("confere_moldes.py"))]:
            confere(codigo != 0 and len(erros) == 1 and all(t in erros[0] for t in lugar + [ARQUIVO_FORMATO.name]),
                    f"{descricao}, no {script}: um erro só, que diz o arquivo e o lugar ({', '.join(lugar)}): {erros}")
        confere(gravados() == certos, f"{descricao}: nada é gravado")


def teste_texto_no_lugar_de_lista(formato, ids):
    """Um texto no lugar de cada lista: as do topo, as de um documento e a de um tipo em
    onde_se_ensina."""
    i, tipo = indice(formato, ids, "grade"), sorted(formato["onde_se_ensina"])[0]
    listas = [((campo,), campo) for campo, v in formato.items() if isinstance(v, list)]
    listas += [(("documentos", i, campo), f"documentos[{i}].{campo}") for campo, v in formato["documentos"][i].items()
               if isinstance(v, list)]
    listas.append((("onde_se_ensina", tipo), f"onde_se_ensina.{tipo}"))
    for chaves, lugar in listas:
        f = copy.deepcopy(formato)
        alvo = f
        for chave in chaves[:-1]:
            alvo = alvo[chave]
        alvo[chaves[-1]] = nome()
        escreve(ARQUIVO_FORMATO, f)
        codigo, erros = valida(ARQUIVO_FORMATO)
        confere(codigo != 0 and len(erros) == 1 and lugar in erros[0],
                f"um texto onde o molde pede uma lista é um erro só, que diz o lugar ({lugar}): {erros}")


def teste_unidade_errada(formato, ids, bases, lugar, lidas):
    """A base de uma unidade que nenhum documento tem, a de uma unidade de documento sem
    grade e a cobertura de uma linha de outra grade."""
    escreve(ARQUIVO_FORMATO, formato)
    item_ = ident()
    codigo, erros, ts = com_base_a_mais(base_vazia(item_, lugar, lidas))
    confere(len(erros) == 1 and item_ in erros[0] and len(ts) == 1,
            f"unidade que nenhum documento tem: um erro só, que diz a unidade, e a base só com o título: {erros} {ts}")
    sem_grade = doc(formato, ids, "partes")["unidades"][0]
    codigo, erros, ts = com_base_a_mais(base_vazia(sem_grade["id"], lugar, lidas))
    confere(len(erros) == 1 and sem_grade["id"] in erros[0] and ids["partes"] in erros[0] and len(ts) == 1,
            f"unidade de documento sem grade: um erro só, que diz a unidade e o documento: {erros} {ts}")
    propria = bases[2][0]
    entrada = PROJETO.caminho_com("bases", propria["id"])
    antes = entrada.read_text(encoding="utf-8")
    dados = json.loads(antes)
    alheia = SORTEIO.choice([linha for e in doc(formato, ids, "grade")["eixos"] for linha in linhas(e)])
    dados["cobertura"][alheia["id"]] = SORTEIO.choice(OUTRAS_COBERTURAS)
    escreve(entrada, dados)
    codigo, erros = roda_base()
    confere(len(erros) == 1 and propria["id"] in erros[0] and alheia["id"] in erros[0],
            f"a cobertura de uma linha de outra grade é um erro só, que diz a base e a linha: {erros}")
    entrada.write_text(antes, encoding="utf-8")


def teste_com_lugar(m):
    """Com a linha da tabela que da lugar a cada trecho marcado sem lugar e a linha de cada
    pedaco sem linha, nenhuma FALTA nem ERRO, e a conferencia sai com codigo 0."""
    v = sem_avisos(m)
    e = esperado(v)
    confere(not e["erros"] and not e["faltas"] and not e["sem_linha"], "o mundo sem avisos não espera aviso nenhum")
    codigo, tela, _ = roda_mundo(v)
    confere(codigo == 0 and not [linha for linha in tela if linha.startswith((ERRO, FALTA))],
            f"o trecho marcado com lugar e o pedaço com linha não são FALTA, e sem FALTA nem ERRO o código é 0: {tela}")
    escreve_mundo(m)


def confere_classe(texto, m, classes, caso):
    """A tabela das classes do relatorio: as do mundo m, com o trecho que o caso muda fora das de
    estudo com lugar, na classe que o caso diz."""
    novas = classes.copy()
    novas[("estudo",)] -= 1
    novas[CLASSE_DO_CASO[caso]] += 1
    confere(tem_as_classes(texto, novas, m["formato"]),
            f"{caso.__name__}: o trecho fica na classe {CLASSE_DO_CASO[caso]}, fora das de estudo com lugar")


def avisos_do_caso(m, caso, prefixo):
    """(o que o aviso tem de dizer, tela, relatorio) da conferencia numa copia do mundo que o
    caso muda, conferindo que ela sai com codigo 1 e que ha linha com o prefixo que diz o que o
    caso diz, tambem no relatorio gravado."""
    v = copy.deepcopy(m)
    esperados = caso(v)
    codigo, tela, texto = roda_mundo(v)
    achadas = [linha for linha in tela if linha.startswith(prefixo) and all(x in linha for x in esperados)]
    confere(codigo == 1 and achadas and all(linha in texto for linha in achadas),
            f"{caso.__name__}: {prefixo} que diz {esperados}, também no relatório gravado: {tela}")
    return esperados, tela, texto


def teste_problemas(m):
    """Cada problema do mundo e um ERRO, que diz o trecho ou o lugar, na tela e no relatorio,
    que e gravado; o trecho sem documento e sem marca nao e FALTA, e fica na classe que o caso
    diz."""
    classes = esperado(m)["classes"]
    for problema in PROBLEMAS:
        esperados, tela, texto = avisos_do_caso(m, problema, ERRO)
        if problema in CLASSE_DO_CASO:
            confere(not [linha for linha in tela if linha.startswith(FALTA) and esperados[0] in linha],
                    f"{problema.__name__}: o trecho sem documento e sem marca não é FALTA")
            confere_classe(texto, m, classes, problema)
    escreve_mundo(m)


def teste_faltas(m):
    """Cada falta do mundo e uma FALTA, que diz o trecho ou o lugar, na tela e no relatorio; o
    trecho que ela deixa sem lugar fica na classe que o caso diz."""
    classes = esperado(m)["classes"]
    for falta in FALTAS:
        _, _, texto = avisos_do_caso(m, falta, FALTA)
        if falta in CLASSE_DO_CASO:
            confere_classe(texto, m, classes, falta)
    escreve_mundo(m)


def teste_entradas_erradas(m):
    """Cada entrada errada e ERRO, que diz o que, e nada e gravado."""
    molde = ESQUEMA_FORMATO.read_text(encoding="utf-8")
    for entrada in ENTRADAS_ERRADAS:
        v = copy.deepcopy(m)
        esperados, depois = entrada(v)
        escreve_mundo(v)
        if depois:
            depois()
        antes = gravados()
        codigo, tela = roda_conferencia()
        erros = [linha for linha in tela if linha.startswith(ERRO)]
        confere(codigo == 1 and any(all(x in linha for x in esperados) for linha in erros),
                f"{entrada.__name__}: ERRO que diz {esperados}: {tela}")
        confere(gravados() == antes, f"{entrada.__name__}: nada é gravado")
        ESQUEMA_FORMATO.write_text(molde, encoding="utf-8")
    escreve_mundo(m)


def teste_caminhos_protegidos():
    """As analises das aulas, a tabela dos destinos, o relatorio da conferencia e as listas de
    trabalho fora da pasta protegida sao erro do projeto.json, que diz o caminho. O que esta no
    caminho vai junto para o lugar novo, para que o erro seja so esse."""
    for chave in ("analises_das_aulas", "destinos", "conferencia_moldes", "listas_de_trabalho"):
        dados = json.loads((PROJ / comum.ARQUIVO_PROJETO).read_text(encoding="utf-8"))
        velho = PROJETO.caminho(chave)
        dados["caminhos"][chave] = f"{ident()}/{velho.name}"
        novo = PROJ / dados["caminhos"][chave]
        novo.parent.mkdir(parents=True)
        if velho.exists():
            (shutil.copytree if velho.is_dir() else shutil.copyfile)(velho, novo)
        outro = PROJ / f"{ident()}.json"
        outro.write_text(json.dumps(dados, ensure_ascii=False), encoding="utf-8")
        codigo, tela = roda_conferencia(outro)
        confere(codigo != 0 and any(linha.startswith(ERRO) and chave in linha for linha in tela),
                f"{chave} fora da pasta protegida é ERRO que diz o caminho: {tela}")
        outro.unlink()
        shutil.rmtree(novo.parent)


def teste_material_certo(ctx):
    """O material certo, com as regioes que nao recebem trechos em todos os textos e em nenhum: nenhum aviso e codigo
    0; cada texto pronto, na ordem de escrita, com a aula, o documento e o nome; nenhum proximo a escrever e nenhum que
    so agora possa ser escrito; duas rodadas, a mesma saida; e, com --unidade, so o texto pedido, e, no que depende de
    outros, nenhum que ainda nao esteja pronto. Devolve o material com aquelas regioes em todos os textos."""
    cm = confere_material
    ordem_ = em_ordem_de_escrita(ctx["textos"], ctx["aulas"])
    certas = [linha_do_texto(t, cm.PRONTA) for t, _ in ordem_]
    for abre in (False, True):
        mat = material_certo(ctx["textos"], ctx["colunas"], abre)
        escreve_material(mat)
        codigo, tela = roda_conferidor(ctx["projeto"])
        confere(codigo == 0 and not avisos_da_tela(tela) and textos_da_tela(tela) == certas,
                f"o material certo (com as regiões que não recebem trechos: {abre}) não dá aviso, o código é 0, e "
                f"cada texto fica pronto, na ordem de escrita, com a aula, o documento e o nome: {tela} ({certas})")
    confere(codigos_do_rotulo(tela, cm.PROXIMA) == [cm.NENHUM] and not depois_do_rotulo(tela, cm.PODE),
            f"com tudo pronto, nenhum próximo a escrever e nenhum que só agora possa ser escrito: {tela}")
    confere(roda_conferidor(ctx["projeto"]) == (codigo, tela), "duas rodadas do conferidor, a mesma saída")
    for t in (um_texto(ctx, lambda t: t.chave), um_texto(ctx, lambda t: not t.chave)):
        codigo, tela = roda_conferidor(ctx["projeto"], "--unidade", t.codigo)
        confere(codigo == 0 and not avisos_da_tela(tela) and textos_da_tela(tela) == [linha_do_texto(t, cm.PRONTA)],
                f"com --unidade {t.codigo}, só o texto dele, pronto: {tela}")
        confere(depois_do_rotulo(tela, cm.PEDE) == ([] if t.chave else [cm.NENHUM]),
                f"com --unidade {t.codigo}, num texto que depende de outros, nenhum que falte: {tela}")
    return mat


def teste_ordem_de_escrita(ctx, mat):
    """Com so os primeiros textos da ordem de escrita: eles prontos, os outros sem texto e sem aviso, e codigo 0; o
    proximo a escrever, o primeiro sem texto; os que dependem de outros, todos escritos, ja podem ser escritos; com
    --unidade, o proximo e FALTA; e o que depende de outros diz os que ainda nao estao prontos."""
    cm = confere_material
    ordem_ = em_ordem_de_escrita(ctx["textos"], ctx["aulas"])
    for k in sorted({0, SORTEIO.randrange(len(ordem_)), SORTEIO.randrange(len(ordem_))}):
        feitos = {t.codigo for t, _ in ordem_[:k]}
        parcial = copy.deepcopy(mat)
        parcial["arquivos"] = {n: [c for c in codigos if c in feitos] for n, codigos in mat["arquivos"].items()}
        parcial["planilhas"] = {c: p for c, p in mat["planilhas"].items() if c in feitos}
        escreve_material(parcial)
        codigo, tela = roda_conferidor(ctx["projeto"])
        certos = {t.codigo: cm.PRONTA if t.codigo in feitos else cm.SEM_TEXTO for t, _ in ordem_}
        confere(codigo == 0 and not avisos_da_tela(tela) and estados_da_tela(tela) == certos,
                f"com os {k} primeiros textos: eles prontos, os outros sem texto e sem aviso, código 0: {tela}")
        proximo = ordem_[k][0]
        confere(codigos_do_rotulo(tela, cm.PROXIMA) == [proximo.codigo],
                f"com os {k} primeiros textos, o próximo a escrever é {proximo.codigo}: {tela}")
        podem = [t.codigo for t, deps in ordem_[k:] if not t.chave and all(d.codigo in feitos for d in deps)]
        confere(codigos_do_rotulo(tela, cm.PODE) == podem,
                f"com os {k} primeiros textos, os que já podem ser escritos são {podem}: {tela}")
        codigo, tela = roda_conferidor(ctx["projeto"], "--unidade", proximo.codigo)
        confere(codigo == 1 and estados_da_tela(tela) == {proximo.codigo: FALTA}
                and any(linha.startswith(f"{FALTA}:") and tem_id(linha, proximo.codigo) for linha in tela),
                f"com --unidade {proximo.codigo}, o texto que não está escrito é FALTA: {tela}")
        pendentes = [(t, deps) for t, deps in ordem_[k:] if not t.chave]
        if pendentes:
            t, deps = SORTEIO.choice(pendentes)
            _, tela = roda_conferidor(ctx["projeto"], "--unidade", t.codigo)
            faltam = ", ".join(d.codigo for d in deps if d.codigo not in feitos) or cm.NENHUM
            confere(depois_do_rotulo(tela, cm.PEDE) == [faltam],
                    f"com --unidade {t.codigo}, os que ele pede e ainda não estão prontos: {faltam}: {tela}")


def teste_material_errado(ctx, mat):
    """Cada caso do material errado: codigo 1, uma linha do aviso que ele da, com o que ela diz, e o estado de cada
    texto -- o do que o caso muda, o que o caso diz; o dos outros, pronto."""
    for caso in CASOS_DOS_TEXTOS + CASOS_DAS_PLANILHAS:
        copia = copy.deepcopy(mat)
        esperado_, depois = caso(copia, ctx)
        if esperado_ is None:
            continue
        escreve_material(copia)
        if depois:
            depois()
        codigo, tela = roda_conferidor(ctx["projeto"])
        achadas = [linha for linha in avisos_da_tela(tela)
                   if linha.startswith(f"{esperado_.tipo}:") and all(p in linha for p in esperado_.palavras)]
        certos = {t.codigo: esperado_.estados.get(t.codigo, confere_material.PRONTA) for t in ctx["textos"]}
        confere(codigo == 1 and achadas and estados_da_tela(tela) == certos,
                f"{caso.__name__}: {esperado_.tipo} que diz {esperado_.palavras}, com os estados {esperado_.estados}: "
                f"{tela}")


def com_codigo_de_aula(v, ctx):
    """(mundo, aula): uma copia do mundo em que uma unidade com texto do documento de partes tem o id de uma aula com
    texto no documento de formas, tambem na tabela dos destinos e na da leitura."""
    w, codigos = copy.deepcopy(v), {t.codigo for t in ctx["textos"]}
    d = doc(w["formato"], w["ids"], "partes")
    aula = um_texto(ctx, lambda t: not t.chave).codigo
    u = SORTEIO.choice([u for u in d["unidades"] if u["id"] in codigos])
    velho = u["id"]
    muda_id(d, u, aula)
    w["destinos"] = [(p, aula if i == velho else i) for p, i in w["destinos"]]
    w["tabela"] = [(i, x, aula if y == velho else y, p) for i, x, y, p in w["tabela"]]
    return w, aula


def confere_que_para(ctx, rotulo, palavras, *args):
    """O conferidor, com os argumentos dados, sai com codigo 1, com uma linha ERRO que diz as palavras, e sem a tabela
    dos textos."""
    codigo, tela = roda_conferidor(ctx["projeto"], *args)
    confere(codigo == 1 and not textos_da_tela(tela)
            and any(linha.startswith(f"{ERRO}:") and all(p in linha for p in palavras) for linha in tela),
            f"{rotulo}: ERRO que diz {palavras}, sem a tabela dos textos: {tela}")


def teste_o_que_para_o_conferidor(ctx, v, base, mat):
    """O texto pedido que nao existe, a conferencia dos moldes com aviso, duas partes com o mesmo id no texto de uma
    unidade e o mesmo codigo em dois textos sao ERRO, sem a tabela dos textos; e o texto de unidade que nao comecou
    fica sem texto, sem aviso, e, pedido com --unidade, e FALTA, sem o texto e sem a planilha."""
    cm, desconhecido = confere_material, ident()
    confere_que_para(ctx, "o texto pedido que não existe", [desconhecido], "--unidade", desconhecido)
    escreve_mundo(base)
    confere_que_para(ctx, "a conferência dos moldes com aviso", [])
    w = copy.deepcopy(v)
    d = doc(w["formato"], w["ids"], "grade")
    d["elos"][0]["id"] = d["eixos"][0]["id"]
    escreve_mundo(w)
    confere_que_para(ctx, "um elo com o id de um eixo, no texto de uma unidade com a grade do documento",
                     [d["eixos"][0]["id"]])
    w, aula = com_codigo_de_aula(v, ctx)
    escreve_mundo(w)
    confere_que_para(ctx, "uma unidade com o código de uma aula com texto", [repr(aula)])
    escreve_mundo(v)
    t = um_texto(ctx, lambda t: t.chave)
    sem_ele = copy.deepcopy(mat)
    sem_ele["arquivos"] = {n: [c for c in codigos if c != t.codigo] for n, codigos in mat["arquivos"].items()}
    del sem_ele["planilhas"][t.codigo]
    escreve_material(sem_ele)
    codigo, tela = roda_conferidor(ctx["projeto"])
    certos = {x.codigo: cm.SEM_TEXTO if x is t else cm.PRONTA for x in ctx["textos"]}
    confere(codigo == 0 and not avisos_da_tela(tela) and estados_da_tela(tela) == certos,
            f"o texto que não começou fica sem texto, e sem aviso: {tela}")
    codigo, tela = roda_conferidor(ctx["projeto"], "--unidade", t.codigo)
    faltas = [linha for linha in tela if linha.startswith(f"{FALTA}:") and tem_id(linha, t.codigo)]
    confere(codigo == 1 and len(faltas) == 2 and estados_da_tela(tela) == {t.codigo: FALTA},
            f"com --unidade {t.codigo}, o texto que não começou é FALTA, sem o texto e sem a planilha: {tela}")


def teste_sem_cartoes(ctx, mat):
    """Sem a coluna dos trechos no projeto.json, os cartoes nao se conferem: sem planilha nenhuma, cada texto fica
    pronto; e, sem a coluna da aula, a planilha sem ela tambem."""
    da_coluna, da_aula = ctx["colunas"]
    sem_aula = {c: ([x for x in cab if x != da_aula], cartoes) for c, (cab, cartoes) in mat["planilhas"].items()}
    for valores, planilhas in [({"coluna_trechos": None, "coluna_subdecks": None}, {}),
                               ({"coluna_trechos": da_coluna, "coluna_subdecks": None}, sem_aula)]:
        projeto = projeto_com(**valores)
        escreve_material({**mat, "planilhas": planilhas})
        codigo, tela = roda_conferidor(projeto)
        confere(codigo == 0 and estados_da_tela(tela) == {t.codigo: confere_material.PRONTA for t in ctx["textos"]},
                f"com {valores}, cada texto pronto, e código 0: {tela}")
        projeto.unlink()


def roda_lista(projeto, codigo):
    """(codigo de saida, linhas da tela) da lista de trabalho do texto de codigo dado, com o projeto.json dado."""
    return roda_tela("lista_de_trabalho.py", "--projeto", str(projeto), "--unidade", codigo)


def listas_gravadas():
    """{arquivo: bytes} das listas de trabalho que existem."""
    return {p: p.read_bytes() for p in PROJETO.todos_com("listas_de_trabalho")}


def sem_listas():
    for p in PROJETO.todos_com("listas_de_trabalho"):
        p.unlink()


def lista_que_para(ctx, rotulo, palavras, codigo):
    """A lista do texto de codigo dado sai com codigo 1, com uma linha ERRO que diz as palavras, e nada e gravado."""
    antes = listas_gravadas()
    codigo_, tela = roda_lista(ctx["projeto"], codigo)
    confere(codigo_ == 1 and any(x.startswith(f"{ERRO}:") and all(p in x for p in palavras) for x in tela)
            and listas_gravadas() == antes, f"{rotulo}: ERRO que diz {palavras}, e nada é gravado: {tela}")


def teste_listas_certas(ctx, mat):
    """No material certo, com uma unidade que nenhum texto tem e o codigo de um trecho das perguntas de prova nela, a
    lista de cada texto, na ordem de escrita: codigo 0, sem ERRO, e o que ela tem de ter, com onde cada trecho esta nos
    textos de que o texto depende, no que depende de outros; e duas rodadas, a mesma lista."""
    cm, com_estranha = confere_material, copy.deepcopy(mat)
    i = SORTEIO.choice(trechos_do(um_texto(ctx, lambda t: not t.chave)))
    no_fim_de_um_arquivo(com_estranha, [marca(cm.UNIDADE, ident()), marca(cm.PARTE, ident()), marca(cm.TRECHO, i)])
    escreve_material(com_estranha)
    lugares_ = lugares_no_material(com_estranha, ctx["mundo"]["ordem"])
    for t, deps in em_ordem_de_escrita(ctx["textos"], ctx["aulas"]):
        dos_deps = {d.codigo for d in deps}
        onde = {i: [x for x in lugares_.get(i, []) if x[2] in dos_deps] for i in trechos_do(t)} if deps else {}
        codigo, tela = roda_lista(ctx["projeto"], t.codigo)
        confere(codigo == 0 and not [x for x in tela if x.startswith(ERRO)],
                f"a lista de {t.codigo}: código 0, sem ERRO: {tela}")
        confere_lista(t, deps, ctx, onde, f"a lista de {t.codigo}")
    t = um_texto(ctx)
    antes = listas_gravadas()
    roda_lista(ctx["projeto"], t.codigo)
    confere(listas_gravadas() == antes, f"a lista de {t.codigo}: duas rodadas, a mesma lista")


def teste_listas_que_param(ctx, mat, base):
    """O texto que depende de outros que ainda nao estao prontos -- um deles sem texto --, o codigo que nenhum texto
    tem, o arquivo das divergencias que falta, fora do molde ou fora do UTF-8 e a conferencia dos moldes com aviso sao
    ERRO, e nada e gravado; e a lista do texto que nao comecou e gravada."""
    v = ctx["mundo"]
    t, deps = SORTEIO.choice([(x, deps) for x, deps in em_ordem_de_escrita(ctx["textos"], ctx["aulas"]) if deps])
    falta = SORTEIO.choice(deps)
    sem_ele = copy.deepcopy(mat)
    sem_ele["arquivos"] = {n: [c for c in codigos if c != falta.codigo] for n, codigos in mat["arquivos"].items()}
    del sem_ele["planilhas"][falta.codigo]
    escreve_material(sem_ele)
    sem_listas()
    lista_que_para(ctx, f"a lista de {t.codigo}, que depende de {falta.codigo}, sem texto", [t.codigo, falta.codigo],
                   t.codigo)
    codigo, tela = roda_lista(ctx["projeto"], falta.codigo)
    confere(codigo == 0 and len(listas_gravadas()) == 1,
            f"a lista de {falta.codigo}, que não começou, é gravada: {tela}")
    escreve_material(mat)
    desconhecido = ident()
    lista_que_para(ctx, "o texto pedido que não existe", [desconhecido], desconhecido)
    guardado = DIVERGENCIAS.read_bytes()
    DIVERGENCIAS.unlink()
    lista_que_para(ctx, "o arquivo das divergências que falta", [DIVERGENCIAS.name], t.codigo)
    grava_divergencias([{k: x for k, x in d.items() if k != "outras"} for d in ctx["divergencias"]])
    lista_que_para(ctx, "o arquivo das divergências fora do molde", [DIVERGENCIAS.name], t.codigo)
    DIVERGENCIAS.write_bytes(guardado + "çã".encode("latin-1"))
    lista_que_para(ctx, "o arquivo das divergências fora do UTF-8", [DIVERGENCIAS.name], t.codigo)
    DIVERGENCIAS.write_bytes(guardado)
    escreve_mundo(base)
    lista_que_para(ctx, "a conferência dos moldes com aviso", [], t.codigo)
    escreve_mundo(v)


def teste_listas_das_formas(ctx):
    """Na forma das analises sem a fonte das paginas, a lista de cada texto de unidade diz que nenhum campo tem a fonte;
    com o campo das paginas na forma de texto, o campo inteiro de cada trecho e um pedaco."""
    lt, v, e = lista_de_trabalho, ctx["mundo"], ctx["esperado"]
    das_unidades = [t for t in ctx["textos"] if t.chave]
    sem_fonte, inteira = copy.deepcopy(v["forma"]), copy.deepcopy(v["forma"])
    del campo_das_paginas(sem_fonte)["fonte"]
    campo = campo_das_paginas(inteira)
    campo["forma"] = TEXTO
    del campo["separadores"]
    for forma, rotulo in ((sem_fonte, "sem a fonte das páginas"), (inteira, "com o campo das páginas inteiro")):
        escreve(PROJETO.caminho("forma_analise"), forma)
        for t in das_unidades:
            codigo, tela = roda_lista(ctx["projeto"], t.codigo)
            arquivo = PROJETO.caminho_com("listas_de_trabalho", f"{t.documento['id']}-{t.codigo}")
            capitulos_ = secao(arquivo.read_text(encoding="utf-8"), lt.CAPITULOS) if arquivo.is_file() else []
            if forma is sem_fonte:
                confere(codigo == 0 and lt.NENHUM_CAMPO in capitulos_,
                        f"{rotulo}, a lista de {t.codigo} diz que nenhum campo tem a fonte: {tela} {capitulos_}")
            else:
                confere(codigo == 0, f"{rotulo}, a lista de {t.codigo}: código 0: {tela}")
                confere_capitulos(capitulos_, t, {**v, "forma": forma}, e, f"{rotulo}, a lista de {t.codigo}",
                                  inteiro=True)
    escreve_mundo(v)


def teste_listas(ctx, mat, base):
    """Com as divergencias do mundo gravadas, a lista de trabalho de cada texto (teste_listas_certas), o que para a
    lista (teste_listas_que_param) e as formas das analises sem a fonte das paginas e com o campo das paginas inteiro
    (teste_listas_das_formas)."""
    escreve_mundo(ctx["mundo"])
    sorteia_divergencias(ctx, ctx["nucleos"])
    teste_listas_certas(ctx, mat)
    teste_listas_que_param(ctx, mat, base)
    teste_listas_das_formas(ctx)


def teste_documento_certo(ctx, mat):
    """No material com a coluna da pergunta e um cartao com dois trechos da mesma divergencia: codigo 0, sem ERRO, e o
    documento com o que ele tem de ter; duas rodadas, o mesmo documento; o --conferir, em dia, codigo 0 e, com uma linha
    a mais antes de uma parte que trata de um fato, FALTA, codigo 1 e nada gravado. Devolve o material."""
    lista, coluna = ctx["divergencias"], ctx["colunas"][0]
    certo = com_perguntas(mat, ctx["dois_do_cartao"], coluna)
    escreve_material(certo)
    regioes = regioes_esperadas(ctx)
    codigo, tela = roda_divergencias(ctx["projeto"])
    confere(codigo == 0 and DOCUMENTO.is_file() and not [x for x in tela if x.startswith(ERRO)],
            f"o documento das divergências: código 0, sem ERRO, e gravado: {tela}")
    confere_documento(lista, certo, ctx, regioes, "o documento das divergências")
    gravado = documento_gravado()
    roda_divergencias(ctx["projeto"])
    confere(documento_gravado() == gravado, "o documento das divergências: duas rodadas, o mesmo documento")
    codigo, tela = roda_divergencias(ctx["projeto"], "--conferir")
    confere(codigo == 0 and not avisos_da_tela(tela) and documento_gravado() == gravado,
            f"--conferir com o documento em dia: código 0, sem aviso, e nada gravado: {tela}")
    usados = [u.arquivo for d in lista for u in usos_esperados(d, certo, regioes, ctx)[0]]
    mudado = copy.deepcopy(certo)
    mudado["cabecas"][SORTEIO.choice(usados).relative_to(MATERIAL).as_posix()].append(frase())
    escreve_material(mudado)
    DOCUMENTO.parent.mkdir(parents=True, exist_ok=True)
    DOCUMENTO.write_bytes(gravado)
    codigo, tela = roda_divergencias(ctx["projeto"], "--conferir")
    confere(codigo == 1 and any(x.startswith(f"{FALTA}:") for x in tela) and documento_gravado() == gravado,
            f"--conferir com uma linha a mais antes de uma parte que trata de um fato: FALTA, código 1, e nada "
            f"gravado: {tela}")
    escreve_material(certo)
    roda_divergencias(ctx["projeto"])
    return certo


def teste_documento_que_para(ctx, certo, base):
    """O arquivo das divergencias que falta, fora do molde ou fora do UTF-8, o fato repetido com outras maiusculas e
    outros espacos, o codigo de trecho que nao existe, a citacao com texto que nao e chamada, a chamada sem lugar, o
    lugar que a fonte nao tem, o arquivo de chamadas que falta, a planilha fora do UTF-8 e a conferencia dos moldes com
    aviso sao ERRO, que diz o que, e nada e gravado."""
    v, lista, nucleos = ctx["mundo"], ctx["divergencias"], ctx["nucleos"]
    guardado = DIVERGENCIAS.read_bytes()
    DIVERGENCIAS.unlink()
    divergencias_que_param(ctx, "o arquivo das divergências que falta", [DIVERGENCIAS.name])
    grava_divergencias([{k: x for k, x in d.items() if k != "ensinada"} for d in lista])
    divergencias_que_param(ctx, "o arquivo das divergências fora do molde", [DIVERGENCIAS.name])
    DIVERGENCIAS.write_bytes(guardado + "çã".encode("latin-1"))
    divergencias_que_param(ctx, "o arquivo das divergências fora do UTF-8", [DIVERGENCIAS.name])
    d = SORTEIO.choice(lista)
    repetida = {**copy.deepcopy(d), "fato": " " + "  ".join(d["fato"].upper().split()) + " "}
    grava_divergencias(lista + [repetida])
    divergencias_que_param(ctx, "o fato repetido, com outras maiúsculas e outros espaços", [repetida["fato"]])
    estranho = ident()
    grava_divergencias(lista + [divergencia_inventada([estranho], v, nucleos)])
    divergencias_que_param(ctx, "o código de trecho que não existe", [estranho])
    chave, nucleo = SORTEIO.choice(sorted(nucleos.items()))
    sobra, lugar = palavra(), f"{comum.ROTULO_PAGINA.format(ident())}"
    erradas = [("a citação com texto que não é chamada", f"{sobra} {citacao_inventada(v, nucleos)}", [sobra]),
               ("a chamada sem lugar", f"({nucleo})", [chave]),
               ("o lugar que a fonte não tem", f"({nucleo}, {lugar})", [chave, lugar])]
    for rotulo, fonte, palavras in erradas:
        grava_divergencias(lista + [divergencia_inventada(d["trechos"], v, nucleos, fonte)])
        divergencias_que_param(ctx, rotulo, palavras)
    DIVERGENCIAS.write_bytes(guardado)
    chamadas = PROJETO.caminho("chamadas")
    das_chamadas = chamadas.read_bytes()
    chamadas.unlink()
    divergencias_que_param(ctx, "o arquivo de chamadas que falta", [chamadas.name])
    chamadas.write_bytes(das_chamadas)
    planilha = planilha_do(SORTEIO.choice(sorted(certo["planilhas"])))
    da_planilha = planilha.read_bytes()
    planilha.write_bytes(da_planilha + "çã".encode("latin-1"))
    divergencias_que_param(ctx, "a planilha fora do UTF-8", [planilha.name])
    planilha.write_bytes(da_planilha)
    escreve_mundo(base)
    divergencias_que_param(ctx, "a conferência dos moldes com aviso", [])
    escreve_mundo(v)


def teste_documento_sem(ctx, certo):
    """Sem divergencia, o documento sai so com o titulo e a abertura, sem titulo de divergencia; e, sem a coluna dos
    trechos no projeto.json, as partes do material sao so as dos textos."""
    grava_divergencias([])
    codigo, tela = roda_divergencias(ctx["projeto"])
    texto = DOCUMENTO.read_text(encoding="utf-8") if DOCUMENTO.is_file() else ""
    confere(codigo == 0 and DOCUMENTO.is_file() and not [x for x in texto.splitlines() if x.startswith("## ")],
            f"sem divergência, o documento sai sem título de divergência, e o código é 0: {tela}")
    grava_divergencias(ctx["divergencias"])
    projeto = projeto_com(coluna_trechos=None, coluna_subdecks=None)
    codigo, tela = roda_divergencias(projeto)
    confere(codigo == 0, f"sem a coluna dos trechos, o documento das divergências: código 0: {tela}")
    confere_documento(ctx["divergencias"], certo, ctx, regioes_esperadas(ctx), "sem a coluna dos trechos",
                      com_cartoes=False)
    projeto.unlink()


def teste_documento(ctx, mat, base):
    """O documento das divergencias certo (teste_documento_certo), o que para o documento (teste_documento_que_para) e o
    documento sem divergencia e sem a coluna dos trechos (teste_documento_sem)."""
    certo = teste_documento_certo(ctx, mat)
    teste_documento_que_para(ctx, certo, base)
    teste_documento_sem(ctx, certo)
    escreve_material(mat)


def teste_material(base):
    """O conferidor do material e a lista de trabalho, no mundo sem avisos com uma aula depois da ultima, com os textos
    e as planilhas inventados e as colunas dos trechos e da aula com nomes sorteados."""
    v = com_aula_depois(sem_avisos(base))
    escreve_mundo(v)
    colunas, e = (ident(), ident()), esperado(v)
    ctx = {"textos": textos_esperados(v, e), "colunas": colunas, "aulas": v["ids"]["aulas"], "mundo": v,
           "esperado": e, "projeto": projeto_com(coluna_trechos=colunas[0], coluna_subdecks=colunas[1]),
           "nucleos": sorteia_chamadas(v)}
    mat = teste_material_certo(ctx)
    teste_ordem_de_escrita(ctx, mat)
    teste_material_errado(ctx, mat)
    teste_o_que_para_o_conferidor(ctx, v, base, mat)
    teste_sem_cartoes(ctx, mat)
    teste_listas(ctx, mat, base)
    teste_documento(ctx, mat, base)
    ctx["projeto"].unlink()


def main():
    if not teste_moldes_declaram():
        termina()
    formato, ids = sorteia_formato()
    teste_formato_certo(formato)
    teste_campos_do_topo(formato)
    if not teste_listas_do_formato(formato):
        termina()
    teste_o_que_se_acha(formato)
    lugar, lidas = fonte_inventada()
    bases = bases_de(formato, ids)
    teste_bases(formato, bases, lugar, lidas)
    mundo = sorteia_mundo(formato, ids)
    teste_conferencia(mundo)
    teste_limite(mundo)
    base = com_fontes(mundo, [PELAS_REGRAS])
    escreve_mundo(base)
    teste_formato_errado(formato, ids, gravados())
    teste_texto_no_lugar_de_lista(formato, ids)
    teste_unidade_errada(formato, ids, bases, lugar, lidas)
    teste_com_lugar(base)
    teste_problemas(base)
    teste_faltas(base)
    teste_entradas_erradas(base)
    teste_caminhos_protegidos()
    teste_material(base)
    termina()


if __name__ == "__main__":
    main()
