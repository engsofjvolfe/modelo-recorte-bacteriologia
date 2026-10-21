# SPDX-License-Identifier: GPL-3.0-or-later
# Copyright do codigo sob GPL-3.0 -- ver LICENSE e NOTICE.md na raiz do projeto.

"""
Teste do baralho do Anki e da conferencia dos cartoes de um projeto: o montar_deck.py, que
gera os pacotes das planilhas de pergunta, e o confere_cartoes.py, que confere cada cartao
contra a prova dele, com a leitura das planilhas do comum.py.

Monta, na pasta de trabalho, um projeto pequeno com a pasta de scripts dada, sem o
referencias.py, e um projeto.json feito do modelo dado, com os caminhos dele e sem arquivo de
fontes. Tudo e sorteado, sempre igual, porque a semente e fixa (outra vem com --semente), com
nomes que nao sao os de nenhum projeto: o prefixo das planilhas; as colunas ocultas, as vezes
com espaco no nome, e a que divide o baralho, oculta ou do molde; um formato so com o
documento dos cartoes, com a coluna da pergunta, as que a conferencia dos cartoes le e outras,
de ids com sublinhado e hifen, em qualquer lado, e uma coluna de imagem em cada lado; o estilo
dos cartoes; as imagens, de bytes sorteados, uma com '&', aspas, apostrofo e espaco no nome; e de tres
a quatro planilhas, com as colunas em qualquer ordem, valores com espacos nas pontas, campos
vazios, uma planilha sem uma das colunas ocultas, a mesma pergunta em duas planilhas, imagens
em algumas planilhas e nenhuma nas outras, e a mesma imagem em dois cartoes.

As fontes tambem sao inventadas: duas transcricoes, uma de paginas e uma de slides, com os
rotulos do comum.py, o titulo de pagina tirado da expressao dele, uma marca de destaque e uma
quebra de linha em cada frase, e o registro da fonte feito pelo registrar_fonte.py; e a base do
material de fora gravada pelo base_externa.py, com duas paginas de uma fonte, uma com frases
que ela trata como possibilidade e uma com frases que ela afirma, e o texto inteiro de outra
fonte, sem paginas. As duas transcricoes tem o mesmo autor e o mesmo ano, com a letra depois
do ano; as chamadas, no arquivo delas. Cada cartao cita um ou dois lugares, numa chamada so ou
numa para cada um, e a prova dele tem um trecho de cada lugar e a pergunta, com outros espacos
e quebras de linha.

O teste confere regras, nunca uma frase pronta:
  - os moldes declaram os lados, a coluna de imagem, as afirmacoes e a classe da frase usada
    da base que o teste usa, e a conferencia dos cartoes le as colunas que ele usa;
  - no mundo certo, o baralho sai sem erro, com um pacote por planilha, na pasta dos baralhos
    com imagens quando ela tem imagem e na dos baralhos quando nao tem; um modelo de cartao so
    para todas, com um campo para cada coluna do molde, na ordem dele, e um para cada coluna
    oculta, com o nome da coluna sem o sublinhado e com cada palavra em maiuscula, o estilo e
    a pergunta como campo de ordenar; cada campo com o valor da planilha sem os espacos das
    pontas, e o oculto vazio quando a planilha nao tem a coluna; a imagem pelo nome do arquivo,
    que vai no pacote com os mesmos bytes, sem nenhuma a mais; o cartao mostrado pelo modelo
    (com o motor de modelo que o genanki usa): na frente, um bloco com a classe do id de cada
    coluna da frente com valor, na ordem do molde, e nenhum da vazia; no verso, a frente, a
    marca da resposta e os blocos das colunas do verso; os campos ocultos, mesmo com valor, em
    lado nenhum; o baralho de cada cartao com a disciplina, o rotulo da coluna que divide e o
    valor dela, e o nome da planilha; os cartoes novos na ordem das linhas; a mesma pergunta
    com outro codigo em outra planilha; duas rodadas, o mesmo conteudo, com os mesmos ids do
    modelo e dos baralhos; e nenhuma rodada do baralho, em nenhum caso, deixa nada na pasta
    temporaria (a do teste, no lugar da do sistema);
  - o codigo de um cartao fica quando mudam a resposta, os outros campos, a imagem e os espacos
    da pergunta, e muda quando muda a pergunta, sem mudar o dos outros; com as linhas em outra
    ordem, os cartoes novos seguem as linhas; com outra coluna oculta, o modelo muda de id;
  - sem a coluna que divide, o baralho e o da disciplina e da planilha;
  - a planilha que perde as imagens leva o pacote para a pasta dos baralhos, e a que ganha uma
    imagem, para a dos baralhos com imagens; sai o pacote dela da outra pasta, e so ele;
  - com --listar, a lista das planilhas, sem gerar nada; com um trecho, so as planilhas com ele
    no nome, sem diferenca de maiuscula; o trecho que nenhuma tem nao gera nada;
  - cada erro de uma planilha e ERRO, que diz a planilha, e so ela fica sem pacote: a coluna do
    molde que falta, a que nao e do molde nem oculta, a repetida, o texto fora do UTF-8, o
    cartao com mais valores que colunas, o sem pergunta, a pergunta repetida com outros
    espacos, a imagem que nao e so o nome de um arquivo (com uma pasta, mesmo com o arquivo
    nela, com barra invertida, mesmo com o arquivo, "." e "..") e a que nao esta na pasta, o
    cartao sem valor na coluna que divide; e duas planilhas com o mesmo nome no Anki sao ERRO
    das duas, tambem quando o trecho deixa uma de fora;
  - cada erro do formato, das colunas ou do estilo e ERRO, que nao diz planilha nenhuma, e
    nenhum pacote e gerado: nenhum
    documento dos cartoes, dois, sem a coluna da pergunta, sem coluna na frente, lado que o
    molde nao conhece, coluna oculta que e do molde, coluna que divide que nao e do molde nem
    oculta, duas colunas do molde que dao o mesmo campo sem contar maiuscula, uma oculta que da
    o campo de uma do molde, cada campo que o proprio Anki preenche (numa coluna do molde ou
    oculta), cada caractere que o Anki tira do nome do campo e cada um que ele tira do comeco,
    coluna oculta sem nenhuma palavra, campo que o molde do formato nao conhece e estilo fora do
    UTF-8; sem o estilo ou sem o formato, nada e gerado;
  - no mundo certo, sem o arquivo de fontes nem o referencias.py, a conferencia dos cartoes sai
    sem erro, com um bloco por cartao, o que mostra que a comparacao nao conta os espacos, as
    quebras de linha e as marcas de destaque, que a chamada sem lugar acha o texto inteiro, e
    que a prova que diz possibilidade aceita o trecho que a base trata assim; duas rodadas, o
    mesmo arquivo;
  - o tique da pessoa volta quando nada mudou, e sai quando muda o cartao, a prova ou o texto
    do lugar citado;
  - cada erro de um cartao e ERRO, que diz a planilha, no bloco dele e em nenhum outro: sem
    prova; a coluna fonte sem chamada; texto nela antes da chamada; a chamada sem lugar de uma
    fonte sem texto inteiro; o lugar que a fonte nao tem; um trecho a mais na prova, com uma
    letra trocada ou com uma virgula a mais; o lugar citado sem trecho; a prova que diz que a
    fonte afirma, com um trecho que a base trata como possibilidade; o trecho vazio; o cartao
    sem pergunta;
  - cada erro de uma planilha na conferencia e ERRO, que diz a planilha, sem erro nos blocos das
    outras: sem o arquivo de prova e a prova fora do molde (todos os cartoes dela com erro); sem
    uma das colunas que a conferencia le e o texto fora do UTF-8 (sem bloco nenhum); a prova sem
    cartao; a pergunta repetida na planilha e na prova; o cartao com mais valores que colunas;
  - sem o arquivo de chamadas, com ele fora do molde (campo desconhecido numa chamada e no topo,
    chamada sem parenteses, chave repetida) ou com duas fontes com a mesma chamada sem contar os
    espacos, e ERRO, e nada e gravado;
  - o cartao escrito por IA, com a marca de fonte de IA do projeto.json, inventada, e a prova
    tirada de uma marca de IA de um texto do material, com outros espacos, sai sem erro, e so
    ele tem o aviso de IA; o tique dele volta quando nada mudou e sai quando muda o texto da
    marca; e ERRO, no bloco dele e em nenhum outro, quando a marca sai do texto e quando o
    projeto nao tem marcas de IA; a marca de IA que abre e nao fecha, e a vazia, sao ERRO, e
    nada e gravado.
Precisa do genanki: roda com o Python que o tem. Uso:
    python3 -I teste_cartoes.py <pasta scripts do projeto> <projeto.json modelo> <pasta de trabalho nova> [--semente N]
Diz "0 falha(s)" quando passa; senao, uma linha FALHA para cada conferencia que nao passou, e
sai com codigo 1.
"""
import argparse
import copy
import csv
import importlib.util
import io
import json
import os
import random
import re
import shutil
import sqlite3
import string
import subprocess
import sys
import zipfile
from collections import namedtuple
from html.parser import HTMLParser
from pathlib import Path


def argumentos():
    p = argparse.ArgumentParser(description="Teste do baralho do Anki e da conferência dos cartões de um projeto.")
    p.add_argument("scripts", type=Path, help="a pasta de scripts do projeto")
    p.add_argument("modelo", type=Path, help="o projeto.json do modelo")
    p.add_argument("trabalho", type=Path, help="uma pasta de trabalho nova")
    p.add_argument("--semente", type=int, default=1, help="a semente do sorteio")
    return p.parse_args()


ARGS = argumentos()
if importlib.util.find_spec("genanki") is None:
    sys.exit(f"ERRO: o Python que roda o teste ({sys.executable}) não tem o genanki, de que o montar_deck.py precisa: "
             "rode o teste com o Python que tem o genanki")
SCRIPTS, MODELO, TRABALHO = (a.resolve() for a in (ARGS.scripts, ARGS.modelo, ARGS.trabalho))
SORTEIO = random.Random(ARGS.semente)
PROJ = TRABALHO / "projeto"
TEMPORARIA = TRABALHO / "temporaria"  # a pasta temporaria dos scripts que o teste roda
VARIAVEL_TEMPORARIA = "TMPDIR"  # a variavel do ambiente em que o tempfile do Python acha a pasta temporaria
PROJ_SCRIPTS = PROJ / SCRIPTS.name  # a pasta de scripts do projeto pequeno, com o nome da pasta dada
REFERENCIAS = PROJ_SCRIPTS / "referencias.py"  # o script das referencias: a conferencia dos cartoes funciona sem ele
shutil.copytree(SCRIPTS, PROJ_SCRIPTS, ignore=shutil.ignore_patterns("__pycache__"))
REFERENCIAS.unlink(missing_ok=True)
sys.path.insert(0, str(PROJ_SCRIPTS))
import chevron  # noqa: E402  -- o motor de modelo que o genanki usa para ver o que a frente do cartao mostra
import base_externa  # noqa: E402
import comum  # noqa: E402
import confere_cartoes  # noqa: E402
import montar_deck  # noqa: E402
import registrar_fonte  # noqa: E402
import validar_dados  # noqa: E402

ERRO = "ERRO"  # o comeco da linha do script que diz um erro (README dos scripts)
PESSOA = "pessoa"  # a caixa de tique da pessoa (comum.TIQUE)
PERGUNTA, RESPOSTA, FONTE = comum.COLUNA_PERGUNTA, confere_cartoes.COLUNA_RESPOSTA, confere_cartoes.COLUNA_FONTE
FRENTE, VERSO = montar_deck.FRENTE, montar_deck.VERSO
AFIRMA, POSSIBILIDADE = confere_cartoes.CATEGORICA, confere_cartoes.POSSIBILIDADE  # o que a prova diz da fonte
USA = "usa"  # a classe da frase que vai para a base do material de fora (esquemas/base.schema.json)
# do Anki (o manual dele): o que separa o baralho de dentro do de fora, o campo do verso que mostra a frente e o id do
# elemento ate onde o verso rola; e, no pacote, o banco, a lista das midias e o que separa os campos de uma nota
ANKI_NIVEL, ANKI_FRENTE, ANKI_RESPOSTA = "::", "FrontSide", "answer"
PACOTE_BANCO, PACOTE_MIDIAS, PACOTE_CAMPOS = "collection.anki2", "media", "\x1f"
# as marcas de destaque que as transcricoes usam, que a comparacao dos trechos nao conta
DESTAQUES = [("*", "*"), ("<i>", "</i>"), ("<em>", "</em>"), ("<b>", "</b>"), ("<strong>", "</strong>")]
LETRAS, ACENTOS = string.ascii_lowercase, "áâãçéêíóôõú"
CONSOANTES = "bcdfghjklmnpqrstvwxz"  # sem vogal, um nome nao forma palavra nenhuma, nem a que diz o erro
FALHAS = []


def confere(condicao, descricao):
    if not condicao:
        FALHAS.append(descricao)
    return condicao


def palavra(minimo=3, maximo=8, letras=LETRAS):
    return "".join(SORTEIO.choice(letras) for _ in range(SORTEIO.randint(minimo, maximo)))


def frase(minimo=2, maximo=6):
    return " ".join(palavra(letras=LETRAS + ACENTOS) for _ in range(SORTEIO.randint(minimo, maximo)))


def sentenca():
    """Uma frase de fonte, com virgula e ponto, que a comparacao dos trechos conta."""
    palavras = [palavra(letras=LETRAS + ACENTOS) for _ in range(SORTEIO.randint(4, 9))]
    meio = SORTEIO.randrange(1, len(palavras) - 1)
    return " ".join(palavras[:meio]) + ", " + " ".join(palavras[meio:]) + "."


def com_destaque(texto):
    """A frase como a transcricao a escreve: uma palavra com marca de destaque e uma quebra de linha no meio."""
    palavras = texto.split(" ")
    i = SORTEIO.randrange(len(palavras))
    abre, fecha = SORTEIO.choice(DESTAQUES)
    palavras[i] = abre + palavras[i] + fecha
    j = SORTEIO.randrange(1, len(palavras))
    return " ".join(palavras[:j]) + "\n" + " ".join(palavras[j:])


def espacos(texto):
    """O texto com outros espacos: cada espaco vira um, dois ou uma quebra de linha."""
    return "".join(SORTEIO.choice((" ", "  ", "\n")) if c == " " else c for c in texto)


def nas_pontas(texto):
    """O texto com espacos nas pontas, as vezes."""
    return SORTEIO.choice(("", " ", "  ")) + texto + SORTEIO.choice(("", " "))


def junta(texto):
    return " ".join(texto.split())


def ficha():
    """Um texto unico, so de letras, para achar um campo no cartao mostrado."""
    return "f" + palavra(12, 12, CONSOANTES)


def versao(nome):
    """A versao que o molde de um tipo de arquivo de dados pede."""
    return json.loads(validar_dados.esquema(nome).read_text(encoding="utf-8"))["properties"]["versao_schema"]["const"]


def grava_json(arquivo, dados):
    arquivo.parent.mkdir(parents=True, exist_ok=True)
    arquivo.write_text(json.dumps(dados, ensure_ascii=False, indent=1), encoding="utf-8")


# ---------- os moldes ----------
MOLDE_FORMATO = json.loads(validar_dados.esquema("formato").read_text(encoding="utf-8"))
MOLDE_PROVA = json.loads(validar_dados.esquema("prova").read_text(encoding="utf-8"))
DA_COLUNA = MOLDE_FORMATO["$defs"]["coluna"]["properties"]
ORDENS = MOLDE_FORMATO["$defs"]["ordem"]["enum"]
confere(set(DA_COLUNA["lado"].get("enum", [])) == {FRENTE, VERSO},
        f"o molde do formato declara os lados do cartão: {DA_COLUNA['lado']}")
confere(DA_COLUNA.get("imagem", {}).get("type") == "boolean", "o molde do formato declara a coluna de imagem")
confere(set(MOLDE_PROVA["$defs"]["prova"]["properties"]["afirmacao"].get("enum", [])) == {AFIRMA, POSSIBILIDADE},
        "o molde da prova declara as afirmações que o teste usa")
confere(set(confere_cartoes.COLUNAS) == {PERGUNTA, RESPOSTA, FONTE},
        f"a conferência dos cartões lê as colunas que o teste usa: {confere_cartoes.COLUNAS}")
confere(USA in json.loads(validar_dados.esquema("base").read_text(encoding="utf-8"))["$defs"]["classe"]["properties"]
        ["classe"].get("enum", []), "o molde da base declara a classe da frase usada, que o teste usa")

# o titulo de pagina tirado da expressao do comum.py: o primeiro grupo e o rotulo, o segundo, a posicao no arquivo;
# o resto e o texto fixo dele
MODELO_TITULO = comum.TITULO_PAGINA.pattern.strip("^$").replace(r"\s*", "").replace("(.+?)", "{rotulo}", 1) \
    .replace(r"(\d+)", "{arquivo}", 1).replace("\\", "")
if not comum.TITULO_PAGINA.match(MODELO_TITULO.format(rotulo="x", arquivo=1)):
    sys.exit(f"o modelo tirado do comum.py ({MODELO_TITULO!r}) não faz um título que ele reconhece: "
             f"o teste precisa ler a expressão de outro jeito")


# ---------- as colunas ----------

def campo(coluna):
    """O nome do campo da coluna no Anki: sem o sublinhado e com cada palavra em maiuscula."""
    return "".join(p.capitalize() for p in re.split(r"[_\s]+", coluna) if p)


def rotulo(coluna):
    """O nome da coluna no nome de um baralho: com espaco no lugar do sublinhado e a primeira letra em maiuscula."""
    texto = " ".join(p for p in re.split(r"[_\s]+", coluna) if p)
    return texto[:1].upper() + texto[1:]


USADOS = {campo(c).casefold() for c in confere_cartoes.COLUNAS}  # os campos ja sorteados, sem contar maiuscula


def nova(gera):
    """Um nome de coluna sorteado por gera(), que nao da o campo de nenhuma outra nem um dos que o Anki preenche."""
    while True:
        nome = gera()
        if campo(nome).casefold() not in USADOS and campo(nome) not in montar_deck.CAMPOS_DO_ANKI:
            USADOS.add(campo(nome).casefold())
            return nome


def id_de_coluna():
    """Um id que o molde do formato aceita: palavras ligadas por sublinhado ou hifen."""
    return "".join(palavra(2, 6) + SORTEIO.choice("__-") for _ in range(SORTEIO.randint(0, 2))) + palavra(2, 6)


def nome_oculto():
    """Um nome de coluna oculta: palavras ligadas por sublinhado ou, as vezes, por espaco."""
    return SORTEIO.choice("__ ").join(palavra(2, 6) for _ in range(SORTEIO.randint(1, 3)))


Coluna = namedtuple("Coluna", "id lado imagem ordem diz_imagem")  # diz_imagem: o formato escreve o "imagem" dela


def coluna(id_, lado, imagem=False):
    return Coluna(id_, lado, imagem, SORTEIO.choice(ORDENS), imagem or SORTEIO.random() < 0.5)


MOLDE = ([coluna(c, FRENTE if c == PERGUNTA else SORTEIO.choice((FRENTE, VERSO))) for c in confere_cartoes.COLUNAS]
         + [coluna(nova(id_de_coluna), SORTEIO.choice((FRENTE, VERSO))) for _ in range(SORTEIO.randint(1, 3))]
         + [coluna(nova(id_de_coluna), lado, True) for lado in (FRENTE, VERSO)])
SORTEIO.shuffle(MOLDE)
I_PERGUNTA = [c.id for c in MOLDE].index(PERGUNTA)
EXTRAS = [c for c in MOLDE if not c.imagem and c.id not in confere_cartoes.COLUNAS]
IMAGENS = [c for c in MOLDE if c.imagem]
OCULTAS = [nova(nome_oculto) for _ in range(SORTEIO.randint(2, 3))]
SUBDECKS = SORTEIO.choice(OCULTAS + [c.id for c in EXTRAS])  # a coluna que divide o baralho
SEM_OCULTA = SORTEIO.choice([o for o in OCULTAS if o != SUBDECKS])  # a coluna oculta que uma planilha nao tem
VALORES_DO_BARALHO = list(dict.fromkeys(SORTEIO.choice((str(SORTEIO.randint(1, 30)), palavra())) for _ in range(3)))
DISCIPLINA, PREFIXO = frase(1, 3), palavra() + "-"

# ---------- o projeto pequeno ----------
ARQUIVO_PROJETO = PROJ / comum.ARQUIVO_PROJETO
BASE_DO_PROJETO = json.loads(MODELO.read_text(encoding="utf-8"))


def projeto_com(**valores):
    """O projeto.json do modelo, com o prefixo, as colunas ocultas e a que divide o baralho do teste, e os valores
    dados no lugar dos dele."""
    dados = copy.deepcopy(BASE_DO_PROJETO)
    dados.update(prefixo_planilhas=PREFIXO, colunas_ocultas=OCULTAS, coluna_subdecks=SUBDECKS)
    dados.update(valores)
    return dados


grava_json(ARQUIVO_PROJETO, projeto_com())
PROJETO = comum.acha_projeto(ARQUIVO_PROJETO)
ARQUIVO_FORMATO, ARQUIVO_ESTILO = PROJETO.caminho("formato"), PROJETO.caminho("estilo_cartao")
ARQUIVO_CHAMADAS, IMAGENS_DOS_CARTOES = PROJETO.caminho("chamadas"), PROJETO.caminho("imagens_cartoes")
BARALHOS, COM_IMAGENS = PROJETO.caminho("baralhos"), PROJETO.caminho("baralhos_com_imagens")
SAIDA = PROJETO.caminho("conferencia_cartoes")

# o formato: so o documento dos cartoes, que recebe todos os trechos (um documento tem de receber algum)
DOCUMENTO = {"id": palavra(), "nome": frase(), "unidade": palavra(), "molde": comum.MOLDE_DOS_CARTOES, "todos": True}
TOPO = {"versao_schema": versao("formato"), "cursos": [frase()], "disciplina": DISCIPLINA, "nivel": palavra(),
        "idioma": palavra(2, 2), "ultima_aula": palavra(), "partes_para_tratar": SORTEIO.randint(1, 3),
        "documentos_vem_de": [SORTEIO.choice(MOLDE_FORMATO["properties"]["documentos_vem_de"]["items"]["enum"])],
        "grupos": [], "partes_por_tipo": [], "tipos_junto": [], "fora": [], "marcas": [], "onde_se_ensina": {}}


def no_formato(c):
    return {"id": c.id, "lado": c.lado, "ordem": c.ordem, **({"imagem": c.imagem} if c.diz_imagem else {})}


def formato_com(colunas=None, documentos=None):
    """O formato do teste, com as colunas dadas no documento dos cartoes, ou os documentos dados."""
    documento = {**DOCUMENTO, "colunas": [no_formato(c) for c in (MOLDE if colunas is None else colunas)]}
    return {**TOPO, "documentos": [documento] if documentos is None else documentos}


grava_json(ARQUIVO_FORMATO, formato_com())
ESTILO = f"/* {frase()} ção */\n" + "".join(f".{c.id} {{ color: #{SORTEIO.randrange(16 ** 6):06x}; }}\n"
                                            for c in MOLDE)
ARQUIVO_ESTILO.parent.mkdir(parents=True, exist_ok=True)
ARQUIVO_ESTILO.write_text(ESTILO, encoding="utf-8")

# ---------- as imagens ----------
IMAGENS_DA_PASTA = list(dict.fromkeys([f"{palavra()}.{palavra(3, 4)}" for _ in range(SORTEIO.randint(2, 3))]
                                      + [f"{palavra()} & \"{palavra()}\"'{palavra()}.{palavra(3, 4)}"]))
IMAGENS_DOS_CARTOES.mkdir(parents=True, exist_ok=True)
for nome in IMAGENS_DA_PASTA:
    (IMAGENS_DOS_CARTOES / nome).write_bytes(SORTEIO.randbytes(SORTEIO.randint(20, 200)))


# ---------- as fontes ----------

def chave():
    return f"{palavra(3, 6, CONSOANTES).upper()}-{SORTEIO.randint(1, 99)}"


def autor():
    return palavra(4, 9, LETRAS + ACENTOS).capitalize()


def arquivo_de_fonte():
    """Um arquivo de fonte inventado, na pasta protegida."""
    arquivo = PROJETO.caminho("material_base") / palavra() / f"{palavra()}.{palavra(3, 4)}"
    arquivo.parent.mkdir(parents=True, exist_ok=True)
    arquivo.write_bytes(SORTEIO.randbytes(SORTEIO.randint(20, 200)))
    return arquivo


CHAVES = []
while len(CHAVES) < 4:
    CHAVES.append(chave())
    CHAVES = list(dict.fromkeys(CHAVES))
T1, T2, B1, B2 = CHAVES  # as transcricoes, de paginas e de slides; as fontes da base, com paginas e sem elas
AUTOR, ANO = autor(), SORTEIO.randint(1950, 2030)
NUCLEOS = {T1: f"{AUTOR}, [{ANO}]a", T2: f"{AUTOR}, [{ANO}]b",
           B1: "; ".join(autor() for _ in range(3)) + f", {SORTEIO.randint(1950, 2030)}",
           B2: f"{autor()}, {SORTEIO.randint(1950, 2030)}"}
CHAMADAS = {"versao_schema": versao("chamadas"),
            "chamadas": [{"chave": k, "chamada": f"({n})"} for k, n in NUCLEOS.items()]}
grava_json(ARQUIVO_CHAMADAS, CHAMADAS)
LUGARES = {}  # (chave, rotulo, vazio no texto inteiro): [(frase sem marcas, afirmacao da base ou None)]
ESCRITAS = {}  # (chave, rotulo): o texto da pagina como a transcricao o escreve
TRANSCRICOES = {}  # chave: o arquivo da transcricao


def transcricao(chave_, rotulos):
    """Grava a transcricao de uma fonte inventada, uma secao por pagina, com duas ou tres frases, e o registro da
    fonte, pelo registrar_fonte.py."""
    secoes = []
    for k, r in enumerate(rotulos, 1):
        frases = [sentenca() for _ in range(SORTEIO.randint(2, 3))]
        LUGARES[(chave_, r)] = [(f, None) for f in frases]
        ESCRITAS[(chave_, r)] = "\n\n".join(com_destaque(f) for f in frases)
        secoes.append(f"{MODELO_TITULO.format(rotulo=r, arquivo=k)}\n\n{ESCRITAS[(chave_, r)]}\n")
    arquivo = PROJETO.caminho("gerados") / f"{palavra()}{comum.EXTENSAO_DOCUMENTO}"
    arquivo.parent.mkdir(parents=True, exist_ok=True)
    arquivo.write_text("\n".join(secoes), encoding="utf-8")
    registrar_fonte.registra(arquivo, arquivo_de_fonte(), chave_, PROJ)
    TRANSCRICOES[chave_] = arquivo


PAGINAS_T1 = sorted(SORTEIO.sample(range(1, 400), SORTEIO.randint(2, 4)))
transcricao(T1, [comum.ROTULO_PAGINA.format(n) for n in PAGINAS_T1])
transcricao(T2, [comum.ROTULO_SLIDE.format(k) for k in range(1, SORTEIO.randint(2, 4) + 1)])

# a base do material de fora: as duas paginas de B1 (a primeira que ela trata como possibilidade, a segunda que ela
# afirma) e o texto inteiro de B2, gravados pelo base_externa.py; o codigo de cada frase, como o do base_externa.py
ITEM, EIXO = palavra(), palavra()
PAGINAS_B1 = dict(zip((1, 2), sorted(SORTEIO.sample(range(1, 400), 2))))  # a pagina no arquivo e a impressa
LUGARES_DA_BASE = [{"fonte": B1, "arquivo": comum.no_projeto(arquivo_de_fonte(), PROJETO),
                    "impressas": {str(p): n for p, n in PAGINAS_B1.items()}},
                   {"fonte": B2, "arquivo": comum.no_projeto(arquivo_de_fonte(), PROJETO)}]
PARTES_DA_BASE, CLASSES = [], {}
for (p, n), afirmacao in zip(PAGINAS_B1.items(), (POSSIBILIDADE, AFIRMA)):
    frases_da_pagina = [sentenca() for _ in range(2)]
    codigos = base_externa.com_codigos(f"{B1}:p{p}", frases_da_pagina)
    PARTES_DA_BASE.append((f"{B1}:p{p}", p, codigos))
    CLASSES.update({c: {"classe": USA, "subtopico": EIXO, "afirmacao": afirmacao} for c, _ in codigos})
    LUGARES[(B1, comum.ROTULO_PAGINA.format(n))] = [(f, afirmacao) for f in frases_da_pagina]
frases_da_pagina, afirmacoes = [sentenca() for _ in range(2)], [AFIRMA, POSSIBILIDADE]
SORTEIO.shuffle(afirmacoes)
codigos = base_externa.com_codigos(B2, frases_da_pagina)
PARTES_DA_BASE.append((B2, None, codigos))
CLASSES.update({c: {"classe": USA, "subtopico": EIXO, "afirmacao": a} for (c, _), a in zip(codigos, afirmacoes)})
LUGARES[(B2, "")] = list(zip(frases_da_pagina, afirmacoes))
ARQUIVO_BASE = PROJETO.caminho_com("base_externa", ITEM)
base_externa.grava_base({"item": ITEM, "cobertura": {}, "classes": CLASSES}, {"nome": frase()},
                        [{"id": EIXO, "nome": frase()}], PARTES_DA_BASE, LUGARES_DA_BASE, PROJ, ARQUIVO_BASE, False)


def cita(lugares):
    """(coluna fonte, trechos, afirmacao): a citacao dos lugares, numa chamada so ou numa para cada um; um trecho de
    cada lugar; e a afirmacao da prova, que e possibilidade quando a base trata um dos trechos assim."""
    partes = [f"{NUCLEOS[c]}, {r}" if r else NUCLEOS[c] for c, r in lugares]
    if len(partes) > 1 and SORTEIO.random() < 0.5:
        fonte = SORTEIO.choice((" ", "; ")).join(f"({p})" for p in partes)
    else:
        fonte = f"({'; '.join(partes)})"
    escolhidos = [SORTEIO.choice(LUGARES[lugar]) for lugar in lugares]
    afirmacao = (POSSIBILIDADE if any(a == POSSIBILIDADE for _, a in escolhidos)
                 else SORTEIO.choice((AFIRMA, POSSIBILIDADE)))
    return fonte, [t for t, _ in escolhidos], afirmacao


def de(chave_):
    return SORTEIO.choice([lugar for lugar in LUGARES if lugar[0] == chave_])


B1_POSSIBILIDADE, B1_AFIRMA = ((B1, comum.ROTULO_PAGINA.format(n)) for n in PAGINAS_B1.values())
# o que os primeiros cartoes da primeira planilha citam: uma pagina de T1, a pagina de B1 que ela trata como
# possibilidade, o texto inteiro de B2, e dois lugares de duas fontes, duas vezes
PRIMEIROS = [[de(T1)], [B1_POSSIBILIDADE], [(B2, "")], [de(T2), de(T1)], [B1_AFIRMA, de(T2)]]


# ---------- as planilhas ----------

def nome_no_anki(arquivo):
    """O nome da planilha no Anki: o do arquivo sem o prefixo, com cada palavra em maiuscula."""
    return "-".join(p.capitalize() for p in arquivo.stem[len(PREFIXO):].split("-") if p)


def cartao(pergunta, lugares, com_imagem):
    """(cartao, prova): o valor de cada coluna, com espacos nas pontas as vezes, e a prova dele."""
    fonte, trechos, afirmacao = cita(lugares)
    valores = {PERGUNTA: nas_pontas(pergunta), RESPOSTA: nas_pontas(frase()) if SORTEIO.random() < 0.8 else "",
               FONTE: nas_pontas(fonte)}
    for nome in [c.id for c in EXTRAS] + OCULTAS:
        valores[nome] = (nas_pontas(SORTEIO.choice(VALORES_DO_BARALHO)) if nome == SUBDECKS
                         else nas_pontas(frase()) if SORTEIO.random() < 0.7 else "")
    for c in IMAGENS:
        valores[c.id] = SORTEIO.choice(IMAGENS_DA_PASTA) if com_imagem and SORTEIO.random() < 0.5 else ""
    return valores, {"pergunta": espacos(pergunta), "trechos": [espacos(t) for t in trechos], "afirmacao": afirmacao}


N_PLANILHAS = SORTEIO.randint(3, 4)
COM_IMAGEM = set(SORTEIO.sample(range(N_PLANILHAS), SORTEIO.randint(1, N_PLANILHAS - 1)))
I_SEM_OCULTA = SORTEIO.randrange(N_PLANILHAS)
PLANILHAS, NA_PRIMEIRA = [], None  # NA_PRIMEIRA: a pergunta da primeira planilha que a segunda tambem tem
while len(PLANILHAS) < N_PLANILHAS:
    arquivo = comum.planilha(PROJETO, "-".join(palavra(3, 7) for _ in range(SORTEIO.randint(1, 3))))
    if nome_no_anki(arquivo) in {nome_no_anki(p["arquivo"]) for p in PLANILHAS}:
        continue
    i, perguntas = len(PLANILHAS), []
    while len(perguntas) < (SORTEIO.randint(5, 7) if i == 0 else SORTEIO.randint(3, 6)):
        q = frase() + "?"
        perguntas += [] if junta(q) in map(junta, perguntas) else [q]
    if i == 1:
        perguntas[SORTEIO.randrange(len(perguntas))] = NA_PRIMEIRA
    NA_PRIMEIRA = NA_PRIMEIRA or SORTEIO.choice(perguntas)
    pares = [cartao(q, PRIMEIROS[k] if i == 0 and k < len(PRIMEIROS) else
                    SORTEIO.sample(sorted(LUGARES), SORTEIO.randint(1, 2)), i in COM_IMAGEM)
             for k, q in enumerate(perguntas)]
    cartoes = [c for c, _ in pares]
    if i in COM_IMAGEM:  # a imagem do nome com '&', aspas e apostrofo, em dois cartoes, uma em cada lado
        cartoes[0][IMAGENS[0].id] = cartoes[1][IMAGENS[1].id] = IMAGENS_DA_PASTA[-1]
    colunas = [c.id for c in MOLDE] + [o for o in OCULTAS if not (i == I_SEM_OCULTA and o == SEM_OCULTA)]
    SORTEIO.shuffle(colunas)
    PLANILHAS.append({"arquivo": arquivo, "colunas": colunas, "cartoes": cartoes, "provas": [p for _, p in pares]})


def linhas_de(colunas, cartoes):
    return [[c.get(coluna_, "") for coluna_ in colunas] for c in cartoes]


def grava(p, colunas=None, cartoes=None, linhas=None, codificacao="utf-8"):
    """Grava a planilha com as colunas e os cartoes dela, ou os dados no lugar deles, ou as linhas dadas."""
    colunas = p["colunas"] if colunas is None else colunas
    linhas = linhas_de(colunas, p["cartoes"] if cartoes is None else cartoes) if linhas is None else linhas
    saida = io.StringIO(newline="")
    escritor = csv.writer(saida)
    escritor.writerow(colunas)
    escritor.writerows(linhas)
    p["arquivo"].parent.mkdir(parents=True, exist_ok=True)
    p["arquivo"].write_bytes(saida.getvalue().encode(codificacao))


def arquivo_da_prova(p):
    return comum.arquivo_da_prova(PROJETO, p["arquivo"])


def grava_provas(p, provas=None):
    grava_json(arquivo_da_prova(p), {"versao_schema": versao("prova"), "provas": p["provas"] if provas is None
                                     else provas})


for p in PLANILHAS:
    grava(p)
    grava_provas(p)
ORIGINAIS = {a: a.read_bytes() for a in [ARQUIVO_PROJETO, ARQUIVO_FORMATO, ARQUIVO_ESTILO, ARQUIVO_CHAMADAS,
                                         ARQUIVO_BASE, *TRANSCRICOES.values(), *(p["arquivo"] for p in PLANILHAS),
                                         *(arquivo_da_prova(p) for p in PLANILHAS)]}


def restaura():
    """Grava de novo cada arquivo do mundo certo."""
    for arquivo, conteudo in ORIGINAIS.items():
        arquivo.parent.mkdir(parents=True, exist_ok=True)
        arquivo.write_bytes(conteudo)


# ---------- rodar e ler ----------

def roda(script, *args):
    """Roda o script do projeto pequeno, com a pasta temporaria do teste no lugar da do sistema."""
    TEMPORARIA.mkdir(exist_ok=True)
    r = subprocess.run([sys.executable, "-I", str(PROJ_SCRIPTS / script), "--projeto", str(ARQUIVO_PROJETO), *args],
                       capture_output=True, text=True, env={**os.environ, VARIAVEL_TEMPORARIA: str(TEMPORARIA)})
    return r.returncode, r.stdout + r.stderr


def montar(*args):
    """Roda o baralho; o que ele deixa na pasta temporaria e uma falha, e sai dela."""
    cod, out = roda("montar_deck.py", *args)
    sobra = sorted(TEMPORARIA.iterdir())
    confere(not sobra, f"o baralho não deixa nada na pasta temporária: {[a.name for a in sobra]}")
    shutil.rmtree(TEMPORARIA)
    return cod, out


def conferir():
    return roda("confere_cartoes.py")


def erros(saida):
    return [linha for linha in saida.split("\n") if linha.startswith(ERRO)]


def le_pacote(arquivo):
    """O que o pacote leva, sem os ids das notas e dos cartoes e sem as horas: os modelos das notas; as notas, na
    ordem das posicoes, cada uma com o codigo, o modelo, os campos, o baralho e a posicao; e as midias, pelo nome. O
    pacote que nao se le e uma falha, e vem vazio."""
    try:
        with zipfile.ZipFile(arquivo) as z:
            midias = {nome: z.read(i) for i, nome in json.loads(z.read(PACOTE_MIDIAS)).items()}
            banco = sqlite3.connect(":memory:")
            banco.deserialize(z.read(PACOTE_BANCO))
        modelos, baralhos = (json.loads(t) for t in banco.execute("SELECT models, decks FROM col").fetchone())
        notas = [{"codigo": g, "modelo": str(m), "campos": f.split(PACOTE_CAMPOS), "id_baralho": d,
                  "baralho": baralhos[str(d)]["name"], "cartao": o, "posicao": p}
                 for g, m, f, d, o, p in banco.execute("SELECT n.guid, n.mid, n.flds, c.did, c.ord, c.due FROM notes "
                                                        "n JOIN cards c ON c.nid = n.id ORDER BY c.due, n.guid")]
        banco.close()
    except (KeyError, ValueError, zipfile.BadZipFile, sqlite3.Error) as e:
        confere(False, f"{arquivo.name}: o pacote se lê como pacote do Anki: {e!r}")
        return {"modelos": {}, "notas": [], "midias": {}}
    usados = {n["modelo"] for n in notas}
    return {"modelos": {i: {k: v for k, v in m.items() if k != "mod"} for i, m in modelos.items() if i in usados},
            "notas": notas, "midias": midias}


def pacotes():
    """{arquivo: conteudo} de cada pacote nas duas pastas dos baralhos."""
    return {a: le_pacote(a) for pasta in (BARALHOS, COM_IMAGENS) if pasta.is_dir()
            for a in sorted(pasta.iterdir()) if a.is_file()}


def limpa():
    """Tira os pacotes das duas pastas dos baralhos."""
    for pasta in (BARALHOS, COM_IMAGENS):
        if pasta.is_dir():
            shutil.rmtree(pasta)


def pergunta_da(nota):
    """O campo da pergunta da nota; vazio, quando ela nao tem campos que cheguem ate ele."""
    return nota["campos"][I_PERGUNTA] if len(nota["campos"]) > I_PERGUNTA else ""


def perguntas_de(p):
    return sorted(c[PERGUNTA].strip() for c in p["cartoes"])


def pacotes_da(p, todos):
    """Os pacotes que tem os cartoes da planilha: os que tem as perguntas dela, e so elas."""
    return [a for a, conteudo in todos.items() if sorted(map(pergunta_da, conteudo["notas"])) == perguntas_de(p)]


def imagens_de(p):
    return {c[i.id].strip() for c in p["cartoes"] for i in IMAGENS if c[i.id].strip()}


def codigos_de(conteudo):
    """{pergunta, com os espacos juntados: codigo do cartao} das notas de um pacote."""
    return {junta(pergunta_da(n)): n["codigo"] for n in conteudo["notas"]}


class Html(HTMLParser):
    """O que o teste olha num trecho de HTML: as marcas de abrir, com os atributos; o texto de fora delas; e os blocos
    com classe, na ordem, cada um com a classe e o texto de dentro."""

    def __init__(self, trecho):
        super().__init__(convert_charrefs=True)
        self.marcas, self.texto, self.blocos, self.abertos = [], "", [], []
        self.feed(trecho)
        self.close()

    def handle_starttag(self, tag, attrs):
        atributos = dict(attrs)
        self.marcas.append((tag, atributos))
        if tag in comum.VAZIOS:
            return
        if atributos.get("class"):
            self.blocos.append((atributos["class"], []))
        self.abertos.append(len(self.blocos) - 1 if atributos.get("class") else None)

    def handle_endtag(self, tag):
        if tag not in comum.VAZIOS and self.abertos:
            self.abertos.pop()

    def handle_data(self, data):
        self.texto += data
        for i in self.abertos:
            if i is not None:
                self.blocos[i][1].append(data)

    def dos_blocos(self):
        return [(classe, "".join(texto)) for classe, texto in self.blocos]


def mostra(modelo, valores):
    """(frente, verso, marca): o cartao como o Anki mostra, pelo modelo, com o valor dado de cada campo; no verso, a
    frente aparece como a marca."""
    molde, marca = modelo["tmpls"][0], ficha()
    return (chevron.render(molde["qfmt"], valores), chevron.render(molde["afmt"], {**valores, ANKI_FRENTE: marca}),
            marca)


def confere_o_que_mostra(modelo, nota, onde):
    """A frente e o verso do cartao, mostrado com uma ficha no lugar de cada campo com valor e de cada campo oculto."""
    nomes = [f["name"] for f in modelo["flds"]]
    valores = {nome: (ficha() if valor else "") for nome, valor in zip(nomes, nota["campos"])}
    ocultos = {nome: ficha() for nome in nomes[len(MOLDE):]}
    valores.update(ocultos)
    frente, verso, marca = mostra(modelo, valores)
    da_frente = [(c.id, valores[campo(c.id)]) for c in MOLDE if c.lado == FRENTE and valores.get(campo(c.id))]
    do_verso = [(c.id, valores[campo(c.id)]) for c in MOLDE if c.lado == VERSO and valores.get(campo(c.id))]
    confere(Html(frente).dos_blocos() == da_frente,
            f"{onde}: a frente mostra um bloco com a classe de cada coluna da frente com valor, na ordem do molde, e "
            f"nenhum da vazia: {frente!r}")
    resto = verso[len(marca):] if verso.startswith(marca) else None
    confere(resto is not None and re.match(rf'\s*<\w+\b[^>]*\bid="{ANKI_RESPOSTA}"', resto)
            and Html(resto).dos_blocos() == do_verso,
            f"{onde}: o verso mostra a frente, a marca da resposta e os blocos das colunas do verso: {verso!r}")
    confere(not any(f in frente + verso for f in ocultos.values()), f"{onde}: os campos ocultos não aparecem")


def confere_campos(p, cartao_, nota, onde):
    """Cada campo da nota com o valor da planilha sem os espacos das pontas, a imagem pelo nome do arquivo, e cada
    oculto vazio quando a planilha nao tem a coluna."""
    if not confere(len(nota["campos"]) == len(MOLDE) + len(OCULTAS), f"{onde}: um campo para cada coluna"):
        return
    for c, dado in zip(MOLDE, nota["campos"]):
        valor = cartao_[c.id].strip()
        if c.imagem and valor:
            html_ = Html(dado)
            confere(html_.marcas == [("img", {"src": valor})] and not html_.texto.strip(),
                    f"{onde}, coluna {c.id!r}: a imagem pelo nome do arquivo: {dado!r}")
        else:
            confere(dado == valor, f"{onde}, coluna {c.id!r}: o valor da planilha sem os espaços das pontas: {dado!r}")
    ocultos = [cartao_[o].strip() if o in p["colunas"] else "" for o in OCULTAS]
    confere(nota["campos"][len(MOLDE):] == ocultos,
            f"{onde}: cada coluna oculta com o valor da planilha, vazio quando ela não a tem: {nota['campos']}")


def baralho(p, cartao_, divide):
    meio = [f"{rotulo(divide)} {cartao_[divide].strip()}"] if divide else []
    return ANKI_NIVEL.join([DISCIPLINA, *meio, nome_no_anki(p["arquivo"])])


def confere_pacote(p, todos, divide=SUBDECKS, contexto=""):
    """O pacote da planilha, como ele sai no mundo certo (ver o comeco)."""
    onde = f"{contexto}{p['arquivo'].name}"
    seus = pacotes_da(p, todos)
    if not confere(len(seus) == 1, f"{onde}: a planilha tem um pacote só: {[a.name for a in seus]}"):
        return
    conteudo, imagens = todos[seus[0]], sorted(imagens_de(p))
    confere(seus[0].parent == (COM_IMAGENS if imagens else BARALHOS),
            f"{onde}: o pacote fica na pasta {'dos baralhos com imagens' if imagens else 'dos baralhos'}: {seus[0]}")
    confere(sorted(conteudo["midias"]) == imagens
            and all(conteudo["midias"][m] == (IMAGENS_DOS_CARTOES / m).read_bytes() for m in imagens),
            f"{onde}: as imagens dos cartões vão no pacote, com os mesmos bytes, e nenhuma a mais: "
            f"{sorted(conteudo['midias'])}")
    modelos = {n["modelo"] for n in conteudo["notas"]}
    if not confere(len(modelos) == 1, f"{onde}: um modelo de cartão só: {modelos}"):
        return
    modelo = conteudo["modelos"][modelos.pop()]
    nomes = [f["name"] for f in modelo["flds"]]
    confere(nomes == [campo(c.id) for c in MOLDE] + [campo(o) for o in OCULTAS],
            f"{onde}: um campo para cada coluna do molde, na ordem dele, e um para cada oculta, com o nome da coluna "
            f"sem o sublinhado e com cada palavra em maiúscula: {nomes}")
    confere(modelo["css"] == ESTILO and modelo["sortf"] == I_PERGUNTA,
            f"{onde}: o modelo tem o estilo dos cartões e ordena pela pergunta")
    notas = conteudo["notas"]
    confere([pergunta_da(n) for n in notas] == [c[PERGUNTA].strip() for c in p["cartoes"]]
            and all(a["posicao"] < b["posicao"] for a, b in zip(notas, notas[1:])),
            f"{onde}: os cartões novos entram na ordem das linhas")
    for k, (c, nota) in enumerate(zip(p["cartoes"], notas), 1):
        confere_campos(p, c, nota, f"{onde}, cartão {k}")
        confere_o_que_mostra(modelo, nota, f"{onde}, cartão {k}")
        confere(nota["baralho"] == baralho(p, c, divide),
                f"{onde}, cartão {k}: o baralho é {baralho(p, c, divide)!r}: {nota['baralho']!r}")


def confere_pastas(planilhas, descricao):
    """Cada planilha com o pacote so na pasta certa: a dos baralhos com imagens, quando ela tem imagem."""
    todos = pacotes()
    for p in planilhas:
        pasta = COM_IMAGENS if imagens_de(p) else BARALHOS
        confere([a.parent for a in pacotes_da(p, todos)] == [pasta],
                f"{descricao}: {p['arquivo'].name}: o pacote só na pasta {pasta.name}: "
                f"{[str(a) for a in pacotes_da(p, todos)]}")


# ---------- o baralho no mundo certo ----------
cod, out = montar()
confere(cod == 0 and not erros(out), f"no mundo certo, o baralho sai sem erro: {out}")
CERTO = pacotes()
confere(len(CERTO) == len(PLANILHAS), f"um pacote para cada planilha: {[a.name for a in CERTO]}")
for p in PLANILHAS:
    confere_pacote(p, CERTO)
MODELOS_CERTOS = {n["modelo"] for c in CERTO.values() for n in c["notas"]}
confere(len(MODELOS_CERTOS) == 1, f"um modelo de cartão só para todas as planilhas: {MODELOS_CERTOS}")
mesma = [n["codigo"] for c in CERTO.values() for n in c["notas"] if junta(pergunta_da(n)) == junta(NA_PRIMEIRA)]
confere(len(mesma) == 2 and len(set(mesma)) == 2, f"a mesma pergunta em duas planilhas tem dois códigos: {mesma}")
montar()
confere(pacotes() == CERTO, "duas rodadas dão o mesmo conteúdo, com os mesmos ids do modelo e dos baralhos")

# ---------- o codigo e a posicao de cada cartao ----------

def confere_os_codigos(p):
    """O codigo de cada cartao da planilha, com um cartao mudado em tudo menos a pergunta (que so muda de espacos),
    outro com outra pergunta e as linhas em outra ordem; e a posicao dos cartoes novos."""
    seus = pacotes_da(p, CERTO)
    if not confere(len(seus) == 1, f"{p['arquivo'].name}: a planilha tem um pacote, para conferir os códigos"):
        return
    antes, variante = codigos_de(CERTO[seus[0]]), copy.deepcopy(p)
    a, b = SORTEIO.sample(range(len(p["cartoes"])), 2)
    mudado, outra_pergunta = variante["cartoes"][a], variante["cartoes"][b]
    mudado[PERGUNTA] = "  " + "  ".join(junta(mudado[PERGUNTA]).split(" ")) + " "
    mudado[RESPOSTA] = frase()
    for c in EXTRAS:
        mudado[c.id] = mudado[c.id] if c.id == SUBDECKS else frase()
    for c in IMAGENS:
        mudado[c.id] = SORTEIO.choice(IMAGENS_DA_PASTA + [""])
    outra_pergunta[PERGUNTA] = outra_pergunta[PERGUNTA].strip() + " " + palavra()
    SORTEIO.shuffle(variante["cartoes"])
    grava(variante)
    montar()
    todos = pacotes()
    seus = pacotes_da(variante, todos)
    if not confere(len(seus) == 1, "a planilha mudada tem um pacote"):
        return
    depois, nova_pergunta = codigos_de(todos[seus[0]]), junta(outra_pergunta[PERGUNTA])
    qa, qb = junta(p["cartoes"][a][PERGUNTA]), junta(p["cartoes"][b][PERGUNTA])
    confere(depois.get(qa) == antes[qa],
            "o código do cartão fica quando mudam a resposta, os outros campos, a imagem e os espaços da pergunta")
    confere(nova_pergunta in depois and depois[nova_pergunta] not in antes.values(),
            "o código do cartão muda quando muda a pergunta")
    confere(all(depois.get(q) == c for q, c in antes.items() if q != qb), "o código dos outros cartões não muda")
    confere([pergunta_da(n) for n in todos[seus[0]]["notas"]] == [c[PERGUNTA].strip() for c in variante["cartoes"]],
            "com as linhas em outra ordem, os cartões novos seguem as linhas")


confere_os_codigos(PLANILHAS[0])
restaura()
limpa()
grava_json(ARQUIVO_PROJETO, projeto_com(colunas_ocultas=OCULTAS + [nova(nome_oculto)]))
montar()
outros = {n["modelo"] for c in pacotes().values() for n in c["notas"]}
confere(outros and outros.isdisjoint(MODELOS_CERTOS),
        f"com outra coluna oculta, o modelo do cartão muda de id: {outros}")
restaura()

# ---------- sem a coluna que divide o baralho ----------
limpa()
grava_json(ARQUIVO_PROJETO, projeto_com(coluna_subdecks=None))
cod, out = montar()
confere(cod == 0 and not erros(out), f"sem a coluna que divide, o baralho sai sem erro: {out}")
todos = pacotes()
for p in PLANILHAS:
    confere_pacote(p, todos, divide=None, contexto="sem a coluna que divide: ")
restaura()

# ---------- a pasta do pacote ----------
limpa()
montar()
p = PLANILHAS[min(COM_IMAGEM)]
sem_imagem = copy.deepcopy(p)
for c in sem_imagem["cartoes"]:
    c.update({i.id: "" for i in IMAGENS})
grava(sem_imagem)
montar()
confere_pastas([sem_imagem] + [q for q in PLANILHAS if q is not p], "a planilha que perde as imagens")
grava(p)
montar()
confere_pastas(PLANILHAS, "a planilha que volta a ter imagem")
p = PLANILHAS[min(set(range(N_PLANILHAS)) - COM_IMAGEM)]
com_imagem = copy.deepcopy(p)
com_imagem["cartoes"][SORTEIO.randrange(len(p["cartoes"]))][SORTEIO.choice(IMAGENS).id] = IMAGENS_DA_PASTA[0]
grava(com_imagem)
montar()
confere_pastas([com_imagem] + [q for q in PLANILHAS if q is not p], "a planilha que ganha uma imagem")
restaura()

# ---------- a lista e o trecho ----------
limpa()
cod, out = montar("--listar")
confere(cod == 0 and not pacotes() and all(p["arquivo"].name in out for p in PLANILHAS),
        f"com --listar, a lista das planilhas, sem gerar nada: {out}")
p = SORTEIO.choice(PLANILHAS)
trecho = p["arquivo"].stem[len(PREFIXO):].upper()
esperadas = [q for q in PLANILHAS if trecho.lower() in q["arquivo"].name.lower()]
cod, out = montar(trecho)
todos = pacotes()
confere(cod == 0 and len(todos) == len(esperadas) and all(len(pacotes_da(q, todos)) == 1 for q in esperadas),
        f"com um trecho, só as planilhas com ele no nome, sem diferença de maiúscula: {[a.name for a in todos]}")
limpa()
cod, out = montar(palavra(12, 12, CONSOANTES))
confere(cod != 0 and not pacotes(), f"o trecho que nenhuma planilha tem não gera nada: {out}")


# ---------- os erros de uma planilha no baralho ----------

def erro_no_baralho(descricao, afetadas, gera=None, extra=()):
    """Roda o baralho com o estrago ja gravado: ERRO, que diz cada planilha afetada, e so elas ficam sem pacote (das
    que o trecho deixa gerar, quando ha trecho)."""
    cod, out = montar(*extra)
    linhas, nomes = erros(out), [a.name for a in afetadas]
    confere(cod == 1 and linhas and all(any(n in linha for n in nomes) for linha in linhas)
            and all(any(n in linha for linha in linhas) for n in nomes),
            f"{descricao}: ERRO, que diz a planilha: {linhas or out}")
    todos = pacotes()
    outras = [q for q in (PLANILHAS if gera is None else gera) if q["arquivo"] not in afetadas]
    confere(len(todos) == len(outras) and all(len(pacotes_da(q, todos)) == 1 for q in outras),
            f"{descricao}: só a planilha com erro fica sem pacote: {[a.name for a in todos]}")
    restaura()
    limpa()


def uma_planilha():
    return SORTEIO.choice(PLANILHAS)


def um_cartao(p):
    return SORTEIO.randrange(len(p["cartoes"]))


def com_cartao(p, k, **valores):
    """Os cartoes da planilha, com os valores dados no cartao k."""
    cartoes = copy.deepcopy(p["cartoes"])
    cartoes[k].update(valores)
    return cartoes


limpa()
p, falta = uma_planilha(), SORTEIO.choice([c.id for c in MOLDE if c.id not in (PERGUNTA, SUBDECKS)])
grava(p, colunas=[c for c in p["colunas"] if c != falta])  # sem a pergunta ou o valor que divide, o erro seria outro
erro_no_baralho("a coluna do molde que falta", [p["arquivo"]])
p, estranha = uma_planilha(), nova(id_de_coluna)
grava(p, colunas=p["colunas"] + [estranha], cartoes=[{**c, estranha: frase()} for c in p["cartoes"]])
erro_no_baralho("a coluna que não é do molde nem oculta", [p["arquivo"]])
p = uma_planilha()
grava(p, colunas=p["colunas"] + [SORTEIO.choice(p["colunas"])])
erro_no_baralho("a coluna repetida", [p["arquivo"]])
p = uma_planilha()
grava(p, cartoes=com_cartao(p, um_cartao(p), **{RESPOSTA: f"ção {frase()}"}), codificacao="latin-1")
erro_no_baralho("o texto fora do UTF-8", [p["arquivo"]])
p = uma_planilha()
linhas = linhas_de(p["colunas"], p["cartoes"])
linhas[um_cartao(p)].append(frase())
grava(p, linhas=linhas)
erro_no_baralho("o cartão com mais valores que colunas", [p["arquivo"]])
p = uma_planilha()
grava(p, cartoes=com_cartao(p, um_cartao(p), **{PERGUNTA: " " * SORTEIO.randint(0, 2)}))
erro_no_baralho("o cartão sem pergunta", [p["arquivo"]])
p = uma_planilha()
i, j = SORTEIO.sample(range(len(p["cartoes"])), 2)
grava(p, cartoes=com_cartao(p, j, **{PERGUNTA: espacos(junta(p["cartoes"][i][PERGUNTA]))}))
erro_no_baralho("a pergunta repetida, com outros espaços", [p["arquivo"]])
PASTA_NAS_IMAGENS, BARRA_INVERTIDA = palavra(), f"{palavra()}\\{IMAGENS_DA_PASTA[0]}"
(IMAGENS_DOS_CARTOES / PASTA_NAS_IMAGENS).mkdir()
(IMAGENS_DOS_CARTOES / PASTA_NAS_IMAGENS / IMAGENS_DA_PASTA[0]).write_bytes(SORTEIO.randbytes(30))
(IMAGENS_DOS_CARTOES / BARRA_INVERTIDA).write_bytes(SORTEIO.randbytes(30))
for nome in (f"{PASTA_NAS_IMAGENS}/{IMAGENS_DA_PASTA[0]}", BARRA_INVERTIDA, ".", ".."):
    p = uma_planilha()
    grava(p, cartoes=com_cartao(p, um_cartao(p), **{SORTEIO.choice(IMAGENS).id: nome}))
    erro_no_baralho(f"a imagem que não é só o nome de um arquivo ({nome!r})", [p["arquivo"]])
p = uma_planilha()
grava(p, cartoes=com_cartao(p, um_cartao(p), **{SORTEIO.choice(IMAGENS).id: f"{palavra(9, 9, CONSOANTES)}.png"}))
erro_no_baralho("a imagem que não está na pasta", [p["arquivo"]])
p = uma_planilha()
grava(p, cartoes=com_cartao(p, um_cartao(p), **{SUBDECKS: " " * SORTEIO.randint(0, 2)}))
erro_no_baralho("o cartão sem valor na coluna que divide o baralho", [p["arquivo"]])
p = uma_planilha()
outra = {"arquivo": comum.planilha(PROJETO, "-" + p["arquivo"].stem[len(PREFIXO):]), "colunas": p["colunas"],
         "cartoes": p["cartoes"]}
grava(outra)
erro_no_baralho("duas planilhas com o mesmo nome no Anki", [p["arquivo"], outra["arquivo"]])
grava(outra)
trecho = p["arquivo"].stem.upper()
erro_no_baralho("duas planilhas com o mesmo nome no Anki, com o trecho que deixa uma de fora", [p["arquivo"]],
                gera=[q for q in PLANILHAS if trecho.lower() in q["arquivo"].name.lower()], extra=(trecho,))
outra["arquivo"].unlink()


# ---------- os erros do formato, das colunas e do estilo ----------

def nada_gerado(descricao, com_erro=True):
    """Roda o baralho com o estrago ja gravado: ERRO (com_erro), que nao e de nenhuma planilha, e nenhum pacote e
    gerado."""
    cod, out = montar()
    linhas = erros(out)
    confere(cod != 0 and (not com_erro or (cod == 1 and linhas)) and not pacotes()
            and not any(p["arquivo"].name in linha for linha in linhas for p in PLANILHAS),
            f"{descricao}: {'ERRO, que não é de nenhuma planilha, e ' if com_erro else ''}nenhum pacote é gerado: "
            f"{out}")
    restaura()
    limpa()


limpa()
grava_json(ARQUIVO_FORMATO, formato_com(documentos=[]))
nada_gerado("nenhum documento dos cartões")
documento = formato_com()["documentos"][0]
grava_json(ARQUIVO_FORMATO, formato_com(documentos=[documento, {**documento, "id": palavra(9, 9)}]))
nada_gerado("dois documentos dos cartões")
grava_json(ARQUIVO_FORMATO, formato_com(colunas=[c for c in MOLDE if c.id != PERGUNTA]))
nada_gerado("o documento dos cartões sem a coluna da pergunta")
grava_json(ARQUIVO_FORMATO, formato_com(colunas=[c._replace(lado=VERSO) for c in MOLDE]))
nada_gerado("o documento dos cartões sem coluna na frente")
i = SORTEIO.randrange(len(MOLDE))
grava_json(ARQUIVO_FORMATO, formato_com(colunas=MOLDE[:i] + [MOLDE[i]._replace(lado=palavra())] + MOLDE[i + 1:]))
nada_gerado("a coluna num lado que o molde não conhece")
grava_json(ARQUIVO_PROJETO, projeto_com(colunas_ocultas=OCULTAS + [SORTEIO.choice(EXTRAS + IMAGENS).id]))
nada_gerado("a coluna oculta que é do molde")
grava_json(ARQUIVO_PROJETO, projeto_com(coluna_subdecks=nova(id_de_coluna)))
nada_gerado("a coluna que divide o baralho que não é do molde nem oculta")


def duas_palavras():
    return f"{palavra(2, 6)}_{palavra(2, 6)}"


duas = nova(duas_palavras)  # "ab_cd" e "abcd" dao "AbCd" e "Abcd"
grava_json(ARQUIVO_FORMATO, formato_com(colunas=MOLDE + [coluna(nome, SORTEIO.choice((FRENTE, VERSO)))
                                                        for nome in (duas, duas.replace("_", ""))]))
nada_gerado("duas colunas do molde que dão o mesmo campo, sem contar maiúscula")
c = SORTEIO.choice(EXTRAS + IMAGENS)
grava_json(ARQUIVO_PROJETO, projeto_com(colunas_ocultas=OCULTAS + [c.id.replace("_", " ").upper()]))
nada_gerado("a coluna oculta que dá o campo de uma do molde")
for nome in montar_deck.CAMPOS_DO_ANKI:
    do_campo = "_".join(p.lower() for p in re.findall(r"[A-Z][a-z]*", nome))
    if not confere(campo(do_campo) == nome, f"o teste acha uma coluna que dá o campo {nome!r}: {do_campo!r}"):
        continue
    if SORTEIO.random() < 0.5:
        grava_json(ARQUIVO_FORMATO, formato_com(colunas=MOLDE + [coluna(do_campo, SORTEIO.choice((FRENTE, VERSO)))]))
        nada_gerado(f"a coluna do molde que dá o campo {nome!r}, que o Anki preenche")
    else:
        grava_json(ARQUIVO_PROJETO, projeto_com(colunas_ocultas=OCULTAS + [do_campo]))
        nada_gerado(f"a coluna oculta que dá o campo {nome!r}, que o Anki preenche")
for nome in ([palavra() + c + palavra() for c in montar_deck.FORA_DO_NOME]
             + [c + palavra() for c in montar_deck.FORA_DO_COMECO] + ["_" * SORTEIO.randint(1, 3)]):
    grava_json(ARQUIVO_PROJETO, projeto_com(colunas_ocultas=OCULTAS + [nome]))
    nada_gerado(f"a coluna oculta {nome!r}, que não dá um campo que o Anki aceite como está")
grava_json(ARQUIVO_FORMATO, {**formato_com(), f"campo_{palavra()}": frase()})
nada_gerado("o formato com um campo que o molde dele não conhece")
ARQUIVO_ESTILO.write_bytes(ESTILO.encode("latin-1"))
nada_gerado("o estilo fora do UTF-8")
ARQUIVO_ESTILO.unlink()
nada_gerado("sem o arquivo de estilo", com_erro=False)
ARQUIVO_FORMATO.unlink()
nada_gerado("sem o formato", com_erro=False)


# ---------- a conferencia dos cartoes ----------

def blocos():
    """{planilha: [{"erro": bool, caixa: bool}] de cada cartao, na ordem} da conferencia dos cartoes: o bloco vai da
    marca da parte ate o titulo seguinte, e tem erro quando uma linha dele diz ERRO."""
    out, atual = {}, None
    for linha in SAIDA.read_text(encoding="utf-8").split("\n"):
        m, t = comum.MARCA_PARTE.match(linha), comum.TIQUE.match(linha)
        if m:
            atual = {"erro": False}
            out.setdefault(m.group(1), []).append(atual)
        elif linha.startswith("#"):
            atual = None
        elif atual is not None and t:
            atual[t.group(2)] = t.group(1) != " "
        elif atual is not None and ERRO in linha:
            atual["erro"] = True
    return out


def tica(p, k):
    """Tica a caixa da pessoa no bloco do cartao k da planilha (contando do 0)."""
    linhas, vistos, dentro = SAIDA.read_text(encoding="utf-8").split("\n"), 0, False
    for i, linha in enumerate(linhas):
        m, t = comum.MARCA_PARTE.match(linha), comum.TIQUE.match(linha)
        if m:
            dentro = m.group(1) == p["arquivo"].stem and vistos == k
            vistos += m.group(1) == p["arquivo"].stem
        elif linha.startswith("#"):
            dentro = False
        elif dentro and t and t.group(2) == PESSOA:
            linhas[i] = linha.replace(f"[{t.group(1)}]", "[x]", 1)
    SAIDA.write_text("\n".join(linhas), encoding="utf-8")


def ticado(p, k):
    seus = blocos().get(p["arquivo"].stem, [])
    return k < len(seus) and seus[k].get(PESSOA, False)


restaura()
confere(not PROJETO.caminho("fontes").exists() and not REFERENCIAS.exists(),
        "o projeto pequeno não tem o arquivo de fontes nem o referencias.py")
cod, out = conferir()
confere(cod == 0 and not erros(out), f"no mundo certo, a conferência dos cartões sai sem erro: {erros(out) or out}")
BLOCOS = blocos()
confere(all(len(BLOCOS.get(p["arquivo"].stem, [])) == len(p["cartoes"])
            and not any(b["erro"] for b in BLOCOS[p["arquivo"].stem]) for p in PLANILHAS),
        f"um bloco por cartão, sem erro: {BLOCOS}")
PRIMEIRA = SAIDA.read_bytes()
conferir()
confere(SAIDA.read_bytes() == PRIMEIRA, "duas rodadas da conferência dão o mesmo arquivo")

# ---------- os tiques ----------
p = PLANILHAS[0]  # o cartao 0 dela cita uma pagina de T1


def muda_o_cartao():
    grava(p, cartoes=com_cartao(p, 0, **{RESPOSTA: frase()}))


def muda_a_prova():
    provas = copy.deepcopy(p["provas"])
    provas[0]["trechos"].append(provas[0]["trechos"][0])
    grava_provas(p, provas)


def muda_o_lugar_citado():
    lugar = PRIMEIROS[0][0]
    TRANSCRICOES[T1].write_text(TRANSCRICOES[T1].read_text(encoding="utf-8").replace(
        ESCRITAS[lugar], f"{ESCRITAS[lugar]} {palavra()}", 1), encoding="utf-8")


for descricao, muda in (("o cartão", muda_o_cartao), ("a prova", muda_a_prova),
                        ("o texto do lugar citado", muda_o_lugar_citado)):
    restaura()
    conferir()
    tica(p, 0)
    conferir()
    if confere(ticado(p, 0), "o tique da pessoa volta quando nada mudou"):
        muda()
        conferir()
        confere(not ticado(p, 0), f"o tique sai quando muda {descricao}")
restaura()


# ---------- os erros de um cartao ----------

def erro_do_cartao(descricao, p, k):
    """Roda a conferencia com o estrago ja gravado: ERRO, que diz a planilha, no bloco do cartao k e em nenhum outro."""
    cod, out = conferir()
    linhas, todos = erros(out), blocos()
    so_ele = all(b["erro"] == (q is p and i == k) for q in PLANILHAS for i, b in enumerate(todos.get(q["arquivo"].stem,
                                                                                                      [])))
    confere(cod == 1 and linhas and all(p["arquivo"].stem in linha for linha in linhas) and so_ele,
            f"{descricao}: ERRO, que diz a planilha, no bloco do cartão e em nenhum outro: {linhas or out}")
    restaura()


def troca_letra(texto):
    """O texto com uma letra trocada por outra."""
    i = SORTEIO.choice([i for i, c in enumerate(texto) if c in LETRAS])
    return texto[:i] + SORTEIO.choice(LETRAS.replace(texto[i], "")) + texto[i + 1:]


def com_virgula(texto):
    """O texto com uma virgula a mais depois da primeira palavra."""
    primeira, resto = texto.split(maxsplit=1)
    return f"{primeira}, {resto}"


def com_prova(p, k, **valores):
    """As provas da planilha, com os valores dados na do cartao k."""
    provas = copy.deepcopy(p["provas"])
    provas[k].update(valores)
    return provas


p = uma_planilha()
k = um_cartao(p)
grava_provas(p, [prova for i, prova in enumerate(p["provas"]) if i != k])
erro_do_cartao("o cartão sem prova", p, k)
p = uma_planilha()
k = um_cartao(p)
grava(p, cartoes=com_cartao(p, k, **{FONTE: f"({frase()})"}))
erro_do_cartao("a coluna fonte sem chamada", p, k)
p = uma_planilha()
k = um_cartao(p)
grava(p, cartoes=com_cartao(p, k, **{FONTE: f"{palavra()} {p['cartoes'][k][FONTE].strip()}"}))
erro_do_cartao("o texto antes da chamada, na coluna fonte", p, k)
p = PLANILHAS[0]
grava(p, cartoes=com_cartao(p, 0, **{FONTE: f"({NUCLEOS[T1]})"}))
erro_do_cartao("a chamada sem lugar, de uma fonte sem texto inteiro", p, 0)
grava(p, cartoes=com_cartao(p, 0, **{FONTE: f"({NUCLEOS[T1]}, "
                                            f"{comum.ROTULO_PAGINA.format(max(PAGINAS_T1) + SORTEIO.randint(1, 9))})"}))
erro_do_cartao("o lugar que a fonte não tem", p, 0)
for descricao, estraga in (("uma letra trocada", troca_letra), ("uma vírgula a mais", com_virgula)):
    p = uma_planilha()
    k = um_cartao(p)
    trechos = p["provas"][k]["trechos"]
    grava_provas(p, com_prova(p, k, trechos=trechos + [estraga(SORTEIO.choice(trechos))]))
    erro_do_cartao(f"o trecho a mais na prova, com {descricao}", p, k)
p = uma_planilha()
k = um_cartao(p)
citados = {(c, r) for c, r in LUGARES if (f"{NUCLEOS[c]}, {r}" if r else NUCLEOS[c]) in p["cartoes"][k][FONTE]}
c, r = SORTEIO.choice([lugar for lugar in LUGARES if lugar not in citados and lugar[0] != B2])
grava(p, cartoes=com_cartao(p, k, **{FONTE: f"{p['cartoes'][k][FONTE].strip()} ({NUCLEOS[c]}, {r})"}))
erro_do_cartao("o lugar citado sem nenhum trecho da prova", p, k)
p = PLANILHAS[0]  # o cartao 1 dela cita a pagina de B1 que a base trata como possibilidade
grava_provas(p, com_prova(p, 1, afirmacao=AFIRMA))
erro_do_cartao("a prova que diz que a fonte afirma, com um trecho que a base trata como possibilidade", p, 1)
p = uma_planilha()
k = um_cartao(p)
grava_provas(p, com_prova(p, k, trechos=[" " * SORTEIO.randint(1, 3)] + p["provas"][k]["trechos"]))
erro_do_cartao("o trecho vazio na prova", p, k)
p = uma_planilha()
k = um_cartao(p)
grava(p, cartoes=com_cartao(p, k, **{PERGUNTA: ""}))
erro_do_cartao("o cartão sem pergunta", p, k)


# ---------- os erros de uma planilha na conferencia ----------

def erro_da_planilha(descricao, p, seus=None):
    """Roda a conferencia com o estrago ja gravado: ERRO, que diz a planilha, sem erro nos blocos das outras; seus diz
    o que se espera dos blocos dela: "nenhum", "todos com erro" ou None (qualquer coisa)."""
    cod, out = conferir()
    linhas, todos = erros(out), blocos()
    outras = not any(b["erro"] for q in PLANILHAS if q is not p for b in todos.get(q["arquivo"].stem, []))
    dela = todos.get(p["arquivo"].stem, [])
    forma = {None: True, "nenhum": not dela,
             "todos com erro": len(dela) == len(p["cartoes"]) and all(b["erro"] for b in dela)}[seus]
    confere(cod == 1 and linhas and all(p["arquivo"].stem in linha for linha in linhas) and outras and forma,
            f"{descricao}: ERRO, que diz a planilha, sem erro nas outras ({seus or 'os blocos dela'}): "
            f"{linhas or out}")
    restaura()


p = uma_planilha()
arquivo_da_prova(p).unlink()
erro_da_planilha("a planilha sem o arquivo de prova", p, "todos com erro")
p = uma_planilha()
grava_provas(p, com_prova(p, um_cartao(p), afirmacao=palavra()))
erro_da_planilha("a prova fora do molde", p, "todos com erro")
p, falta = uma_planilha(), SORTEIO.choice(confere_cartoes.COLUNAS)
grava(p, colunas=[c for c in p["colunas"] if c != falta])
erro_da_planilha("a planilha sem uma das colunas que a conferência lê", p, "nenhum")
p = uma_planilha()
grava(p, cartoes=com_cartao(p, um_cartao(p), **{RESPOSTA: f"ção {frase()}"}), codificacao="latin-1")
erro_da_planilha("a planilha fora do UTF-8", p, "nenhum")
p = uma_planilha()
grava_provas(p, p["provas"] + [{"pergunta": frase() + "?", "trechos": [sentenca()], "afirmacao": AFIRMA}])
erro_da_planilha("a prova sem cartão", p)
p = uma_planilha()
i, j = SORTEIO.sample(range(len(p["cartoes"])), 2)  # o cartao j vira o i, com outros espacos na pergunta
grava(p, cartoes=com_cartao(p, j, **{**p["cartoes"][i], PERGUNTA: espacos(junta(p["cartoes"][i][PERGUNTA]))}))
grava_provas(p, [prova for k, prova in enumerate(p["provas"]) if k != j])
erro_da_planilha("a pergunta repetida na planilha", p)
p = uma_planilha()
k = um_cartao(p)
grava_provas(p, p["provas"] + [{**p["provas"][k], "pergunta": espacos(junta(p["provas"][k]["pergunta"]))}])
erro_da_planilha("a pergunta repetida no arquivo de prova", p)
p = uma_planilha()
linhas = linhas_de(p["colunas"], p["cartoes"])
linhas[um_cartao(p)].append(frase())
grava(p, linhas=linhas)
erro_da_planilha("o cartão com mais valores que colunas", p)


# ---------- os erros do arquivo de chamadas ----------

def erro_das_chamadas(descricao):
    """Roda a conferencia com o estrago ja gravado: ERRO, e nada e gravado."""
    antes = SAIDA.read_bytes()
    cod, out = conferir()
    confere(cod == 1 and erros(out) and SAIDA.read_bytes() == antes,
            f"{descricao}: ERRO, e nada é gravado: {erros(out) or out}")
    restaura()


def chamadas_com(**mudanca):
    """O arquivo de chamadas com a mudanca dada: um campo novo numa chamada (na_chamada) ou no topo (no_topo), uma
    chamada mudada (chamada) ou uma chamada a mais (mais)."""
    dados = copy.deepcopy(CHAMADAS)
    i = SORTEIO.randrange(len(dados["chamadas"]))
    if "na_chamada" in mudanca:
        dados["chamadas"][i][mudanca["na_chamada"]] = frase()
    if "no_topo" in mudanca:
        dados[mudanca["no_topo"]] = frase()
    if "chamada" in mudanca:
        dados["chamadas"][i]["chamada"] = mudanca["chamada"]
    if "mais" in mudanca:
        dados["chamadas"].append(mudanca["mais"])
    return dados


conferir()
ARQUIVO_CHAMADAS.unlink()
erro_das_chamadas("sem o arquivo de chamadas")
for descricao, mudanca in (
        ("um campo que o molde não conhece numa chamada", {"na_chamada": f"campo_{palavra()}"}),
        ("um campo que o molde não conhece no topo", {"no_topo": f"campo_{palavra()}"}),
        ("a chamada sem parênteses", {"chamada": NUCLEOS[B2]}),
        ("a chave repetida", {"mais": {"chave": T1, "chamada": f"({autor()}, {SORTEIO.randint(1950, 2030)})"}}),
        ("duas fontes com a mesma chamada, sem contar os espaços",
         {"mais": {"chave": chave() + palavra(2, 2, CONSOANTES).upper(),
                   "chamada": f"({NUCLEOS[T2].replace(', ', ',  ', 1)})"}})):
    grava_json(ARQUIVO_CHAMADAS, chamadas_com(**mudanca))
    erro_das_chamadas(f"o arquivo de chamadas com {descricao}")


# ---------- o cartao escrito por IA ----------
IA = {"abre": f"[{palavra()}: ", "fecha": "]", "fonte": f"[{palavra()}]"}  # as marcas de IA, inventadas
TEXTO_DE_IA = PROJETO.caminho("material_gerado") / f"{palavra()}{comum.EXTENSAO_DOCUMENTO}"
MARCADO = sentenca()  # o que a IA escreveu


def texto_com(marcado):
    """Grava o texto do material com uma marca de IA em volta do texto dado."""
    TEXTO_DE_IA.parent.mkdir(parents=True, exist_ok=True)
    TEXTO_DE_IA.write_text(f"# {frase()}\n\n{frase()} {IA['abre']}{marcado}{IA['fecha']} {frase()}.\n",
                           encoding="utf-8")


def com_ia(p, k):
    """Grava o projeto com as marcas de IA, o texto do material com a marca e o cartao k de p como cartao de IA, com
    a prova tirada da marca, com outros espacos."""
    grava_json(ARQUIVO_PROJETO, projeto_com(ia=IA))
    texto_com(MARCADO)
    grava(p, cartoes=com_cartao(p, k, **{FONTE: nas_pontas(IA["fonte"])}))
    grava_provas(p, com_prova(p, k, trechos=[espacos(MARCADO)], afirmacao=AFIRMA))


p = uma_planilha()
k = um_cartao(p)
com_ia(p, k)
cod, out = conferir()
dela = blocos().get(p["arquivo"].stem, [])
confere(cod == 0 and not erros(out) and len(dela) == len(p["cartoes"]) and not any(b["erro"] for b in dela),
        f"o cartão de IA, com a prova tirada de uma marca de IA do material, sai sem erro: {erros(out) or out}")
confere(SAIDA.read_text(encoding="utf-8").count(confere_cartoes.AVISO_IA) == 1,
        "o cartão de IA, e só ele, tem o aviso de que precisa ser verificado")
tica(p, k)
conferir()
if confere(ticado(p, k), "o tique do cartão de IA volta quando nada mudou"):
    texto_com(f"{MARCADO} {palavra()}")
    conferir()
    confere(not ticado(p, k), "o tique do cartão de IA sai quando muda o texto da marca")
TEXTO_DE_IA.write_text(f"# {frase()}\n\n{frase()} {MARCADO} {frase()}.\n", encoding="utf-8")
erro_do_cartao("o cartão de IA cuja marca saiu do texto", p, k)

p = uma_planilha()
k = um_cartao(p)
com_ia(p, k)
grava_json(ARQUIVO_PROJETO, projeto_com())
erro_do_cartao("o cartão com a marca de fonte de IA, num projeto sem marcas de IA", p, k)

for quebrada in (f"{frase()} {IA['abre']}{frase()}", f"{IA['abre']} {IA['fecha']}"):
    p = uma_planilha()
    k = um_cartao(p)
    com_ia(p, k)
    conferir()
    TEXTO_DE_IA.write_text(f"# {frase()}\n\n{quebrada}\n", encoding="utf-8")
    erro_das_chamadas(f"a marca de IA quebrada no texto: {quebrada!r}")
TEXTO_DE_IA.unlink()

for f in FALHAS:
    print("FALHA:", f)
print(f"{len(FALHAS)} falha(s)")
sys.exit(1 if FALHAS else 0)
