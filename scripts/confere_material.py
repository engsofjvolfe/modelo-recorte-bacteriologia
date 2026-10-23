# SPDX-License-Identifier: GPL-3.0-or-later
# Copyright do codigo sob GPL-3.0 -- ver LICENSE e NOTICE.md na raiz do projeto.

"""
Confere o material escrito: o texto de cada unidade, pelos codigos escondidos nele, e os
cartoes dela. Diz o que falta e o que esta fora do lugar, o estado de cada texto, o proximo
a escrever e os textos que dependem de outros e ja podem ser escritos. Nao grava nada.

Os textos do material sao os do confere_moldes.py (textos): o de cada unidade com material
de um documento de conteudo e o de cada entrada de um documento que recebe todos os trechos
e que e texto -- nas perguntas de prova, cada aula --, cada um com as partes na ordem do
molde e os trechos de cada uma. Com qualquer aviso na conferencia dos moldes, ou com o mesmo
codigo em dois textos, nada se confere: o script para com ERRO.

Os codigos escondidos. Cada texto leva comentarios do Markdown, que a visualizacao nao
mostra, na forma <!-- <nivel> <codigo> -->, lidos pela peca das marcas (marcas.py) em cada
.md da pasta do material gerado e das subpastas dela, fora do codigo (comum.py). Os niveis
(NIVEIS): UNIDADE abre o texto, com o codigo dele; ITEM abre um item da unidade, pelo id;
PARTE abre uma parte, pelo id dela; e TRECHO, dentro da parte, da o codigo de um trecho,
como o analises.py o da. Abrir um nivel fecha os de dentro dele. Cada texto se confere pela
peca: cada trecho na parte dele -- o que vai junto do assunto, em qualquer parte que recebe
trechos --; as partes na ordem do molde, nenhuma aberta duas vezes; nenhum codigo de outra
unidade ou que nao existe, nem numa parte que nao recebe trechos; nenhuma unidade em dois
lugares. A parte sem trecho pode ficar sem texto.

Os cartoes. O texto de uma unidade de documento de conteudo tem a planilha de pergunta do
codigo dele (comum.planilha), e cada cartao leva, na coluna dos trechos ("coluna_trechos",
no projeto.json), os codigos dos trechos dele, separados por espaco. Cada trecho da unidade
esta em pelo menos um cartao; o cartao sem codigo, e o codigo que nao existe ou que e de
outra unidade, sao ERRO; e, com a coluna que divide o baralho ("coluna_subdecks"), cada
cartao traz nela a aula do texto. Com "coluna_trechos" null, os cartoes nao se conferem.

O estado de cada texto: sem texto, quando nem ele nem a planilha dele existem; ERRO ou FALTA,
pelos avisos dele; ou pronta, sem aviso. A ordem de escrita: os textos das unidades pela
aula de cada um e, na mesma aula, na ordem dos documentos e das unidades no formato; o de
cada entrada de um documento que recebe todos os trechos, logo depois do ultimo texto de
unidade com trecho dela, e ele so pode ser escrito com todos esses prontos. O proximo a
escrever e o primeiro, nessa ordem, que nao esta pronto.

Sem --unidade, todos os textos, na ordem de escrita, numa tabela com a aula, o documento, a
unidade, o codigo e o estado de cada um, e depois o proximo a escrever e os que ja podem ser
escritos; o texto sem texto nao da aviso. Com --unidade, so o texto do codigo dado, e sem
texto ele e FALTA; num texto que depende de outros, os que ainda nao estao prontos. Antes,
cada FALTA e cada ERRO, com o arquivo e a linha; os que nao sao de um texto (o codigo fora
de unidade, o comentario que nao fecha, o arquivo fora do UTF-8, a unidade que nenhum texto
tem) saem sempre. Sai com codigo 1 quando ha FALTA ou ERRO. Quem importa este script tem a
conferencia sem a tela (confere), com a ordem de escrita e o estado de cada texto, as marcas
lidas nos textos (marcas_dos_textos), os lugares de cada codigo de trecho nos textos
(lugares_dos_trechos), os codigos dos trechos de um cartao (codigos_do_cartao) e o texto de
um codigo escondido (marca).

Uso (de qualquer pasta dentro do projeto):
    python scripts/confere_material.py
    python scripts/confere_material.py --unidade <codigo>
    python scripts/confere_material.py --projeto projeto.json
"""

import argparse
import collections
import csv
import io
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import confere_moldes  # noqa: E402
import marcas  # noqa: E402
from comum import (EXTENSAO_DOCUMENTO, acha_projeto, linhas_fora_de_codigo, no_projeto, planilha,  # noqa: E402
                   sem_codigo_na_linha)
from relatorio import tabela  # noqa: E402
from validar_dados import le_texto  # noqa: E402

UNIDADE, ITEM, PARTE, TRECHO = "unidade", "item", "parte", "trecho"  # os niveis dos codigos escondidos
NIVEIS = marcas.Niveis([UNIDADE, ITEM, PARTE], TRECHO)  # os que abrem regiao, do de fora para o de dentro, e o trecho
ERRO, FALTA = marcas.ERRO, marcas.FALTA
SEM_TEXTO, PRONTA = "sem texto", "pronta"  # o estado do texto que nao comecou e o do texto sem aviso
NENHUM = confere_moldes.NENHUM
COLUNAS = ["Aula", "Documento", "Unidade", "Código", "Estado"]  # a tabela dos textos
PROXIMA = "A próxima a escrever"  # a linha do proximo texto a escrever
PODE = "Já pode ser escrita"  # a linha de cada texto que depende de outros, todos prontos, e ainda nao esta pronto
PEDE = "Ainda não prontas, das unidades com trechos dela"  # a linha dos textos de que um texto depende
Conferido = collections.namedtuple("Conferido", "moldes lista estados avisos soltos")
# o que o conferidor acha: o que a conferencia dos moldes da (Conferencia, trechos, notas por aula); os textos na ordem
# de escrita, cada um com os textos de que ele depende; o estado e os avisos de cada texto, pelo codigo dele; e os
# avisos que nao sao de texto nenhum
CASOS = {  # cada caso de aviso deste script, com o tipo dele; os dos codigos escondidos sao os de marcas.CASOS
    "sem-texto": FALTA,
    "sem-planilha": FALTA,
    "sem-cartao": FALTA,
    "fora-do-utf8": ERRO,
    "sem-coluna": ERRO,
    "cartao-sem-trecho": ERRO,
    "cartao-que-nao-existe": ERRO,
    "cartao-de-outra-unidade": ERRO,
    "cartao-de-outra-aula": ERRO,
}


def aviso(caso, arquivo, linha, unidade, codigo, texto):
    return marcas.Aviso(CASOS[caso], caso, arquivo, linha, unidade, codigo, texto)


def marca(nivel, codigo):
    """O codigo escondido do nivel e do codigo dados, como a peca das marcas o le."""
    return f"{marcas.ABRE} {nivel} {codigo} {marcas.FECHA}"


def linha_do_aviso(a):
    """A linha de um aviso: o tipo; o arquivo e a linha, quando ha; a unidade, quando ha; e o que houve."""
    onde = ":".join(str(v) for v in (a.arquivo, a.linha) if v is not None)
    return f"{a.tipo}: " + "".join(f"{v}: " for v in (onde, a.unidade) if v) + a.texto


def para(erros):
    """Mostra cada erro de entrada e que nada se conferiu; devolve o codigo de saida."""
    for e in erros:
        print(f"{ERRO}: {e}")
    print("Nada foi conferido.")
    return 1


# ---------- os textos ----------

def marcas_dos_textos(projeto):
    """(marcas, avisos): as marcas de cada .md da pasta do material gerado e das subpastas dela, na ordem dos
    caminhos, cada uma com o caminho do arquivo a partir da pasta do projeto; o arquivo fora do UTF-8 e ERRO, e dele
    nada se le."""
    todas, avisos = [], []
    for arquivo in sorted(a for a in projeto.caminho("material_gerado").rglob(f"*{EXTENSAO_DOCUMENTO}") if a.is_file()):
        nome = no_projeto(arquivo, projeto)
        texto, erros = le_texto(arquivo, nome)
        avisos += [aviso("fora-do-utf8", None, None, None, None, e) for e in erros]
        if not erros:
            linhas = [(n, sem_codigo_na_linha(linha)) for n, linha in linhas_fora_de_codigo(texto)]
            todas += marcas.marcas_das_linhas(linhas, nome, NIVEIS)
    return todas, avisos


def lugares_dos_trechos(projeto):
    """{codigo: [(marca, caminho)]} de cada codigo de trecho nos textos do material, na ordem dos arquivos e das linhas:
    a marca, com o arquivo e a linha, e o caminho das regioes abertas ali (marcas.com_caminho)."""
    todas, _ = marcas_dos_textos(projeto)
    saida = {}
    for m, caminho in marcas.com_caminho(todas, NIVEIS):
        if m.nivel == TRECHO and m.codigo is not None:
            saida.setdefault(m.codigo, []).append((m, caminho))
    return saida


def codigos_do_cartao(linha, coluna):
    """Os codigos dos trechos de um cartao, {coluna: valor}, na coluna dada: separados por espaco, em NFC, sem repetir,
    na ordem."""
    return list(dict.fromkeys(marcas.nfc(linha.get(coluna) or "").split()))


def trechos_do_texto(texto):
    """Os ids dos trechos do texto, sem repetir: os de cada parte, na ordem do molde, e depois os que vao junto."""
    return list(dict.fromkeys([i for p in texto.partes for i in p.trechos] + list(texto.junto)))


def esperados(textos):
    """{codigo: marcas.Esperado} de cada texto: as partes, cada uma pelo caminho dela -- o codigo do texto, o id do
    item (None, na parte da propria unidade) e o da parte --, com os trechos dela e se ela recebe trechos; e os
    trechos que vao junto do assunto."""
    return {t.codigo: marcas.Esperado([marcas.Regiao((t.codigo, p.item["id"] if p.item else None, p.id), p.trechos,
                                                     p.recebe) for p in t.partes], t.junto) for t in textos}


# ---------- os cartoes ----------

def avisos_da_planilha(arquivo, nome, texto, colunas, existem):
    """[Aviso] da planilha do texto: as colunas que faltam nela; cada cartao sem o codigo de nenhum trecho, com codigo
    que nao existe ou de outra unidade, ou com outra aula; e cada trecho do texto sem cartao. colunas e (a dos
    trechos, a da aula ou None)."""
    conteudo, erros = le_texto(arquivo, nome)
    if erros:
        return [aviso("fora-do-utf8", None, None, texto.codigo, None, e) for e in erros]
    leitor = csv.DictReader(io.StringIO(conteudo))
    faltam = [c for c in colunas if c and c not in (leitor.fieldnames or [])]
    if faltam:
        return [aviso("sem-coluna", nome, 1, texto.codigo, None, f"a planilha não tem a coluna {c!r}") for c in faltam]
    dos_trechos, da_aula = colunas
    seus, com_cartao, avisos = trechos_do_texto(texto), set(), []
    for linha in leitor:
        n, codigos = leitor.line_num, codigos_do_cartao(linha, dos_trechos)
        if not codigos:
            avisos.append(aviso("cartao-sem-trecho", nome, n, texto.codigo, None,
                                "cartão sem o código de nenhum trecho"))
        for codigo in codigos:
            if codigo not in existem:
                avisos.append(aviso("cartao-que-nao-existe", nome, n, texto.codigo, codigo,
                                    f"o código {codigo} não existe"))
            elif codigo not in seus:
                avisos.append(aviso("cartao-de-outra-unidade", nome, n, texto.codigo, codigo,
                                    f"o código {codigo} é de outra unidade"))
            else:
                com_cartao.add(codigo)
        aula = marcas.nfc((linha[da_aula] or "").strip()) if da_aula else texto.aula
        if aula != texto.aula:
            avisos.append(aviso("cartao-de-outra-aula", nome, n, texto.codigo, None,
                                f"o cartão é da aula {aula!r}, e a unidade, da aula {texto.aula!r}"))
    return avisos + [aviso("sem-cartao", nome, None, texto.codigo, i, f"o trecho {i} não está em nenhum cartão")
                     for i in seus if i not in com_cartao]


def avisos_dos_cartoes(projeto, texto, colunas, existem):
    """(planilha existe, [Aviso]) dos cartoes do texto: os da planilha dele, ou a FALTA dela; (False, []) quando o
    texto nao tem planilha -- o de uma entrada de um documento que recebe todos os trechos -- ou os cartoes nao se
    conferem."""
    if texto.chave is None or colunas[0] is None:
        return False, []
    arquivo = planilha(projeto, texto.codigo)
    nome = no_projeto(arquivo, projeto)
    if not arquivo.is_file():
        return False, [aviso("sem-planilha", nome, None, texto.codigo, None, "falta a planilha dos cartões da unidade")]
    return True, avisos_da_planilha(arquivo, nome, texto, colunas, existem)


# ---------- o estado e a ordem ----------

def estado(avisos):
    """O estado do texto comecado, pelos avisos dele: ERRO, FALTA ou pronta."""
    tipos = {a.tipo for a in avisos}
    return ERRO if ERRO in tipos else FALTA if FALTA in tipos else PRONTA


def em_ordem_de_escrita(textos, aulas):
    """[(texto, textos de que ele depende)] na ordem de escrita: os textos das unidades dos documentos de conteudo,
    pela aula de cada um e, na mesma aula, na ordem em que o formato os da; e o de cada entrada de um documento que
    recebe todos os trechos logo depois do ultimo desses que tem trecho dele, dependendo de todos os que tem."""
    das_unidades = sorted((t for t in textos if t.chave is not None), key=lambda t: aulas.index(t.aula))
    seus = [set(trechos_do_texto(t)) for t in das_unidades]
    depois = collections.defaultdict(list)
    for t in textos:
        if t.chave is None:
            deps = [k for k, s in enumerate(seus) if s & set(trechos_do_texto(t))]
            depois[deps[-1] if deps else len(das_unidades) - 1].append((t, [das_unidades[k] for k in deps]))
    saida = [] if das_unidades else depois[-1]
    for k, t in enumerate(das_unidades):
        saida += [(t, [])] + depois[k]
    return saida


def apresenta(texto):
    """O texto numa linha: o codigo, com o nome e o documento."""
    return f"{texto.codigo} ({texto.nome}, de {texto.documento['nome']})"


# ---------- a conferencia ----------

def avisos_e_estados(projeto, textos, existem, pedido):
    """({codigo: [Aviso]}, [Aviso] que nao sao de texto nenhum, {codigo: estado}) dos textos: os avisos dos codigos
    escondidos e os dos cartoes. O texto que nao comecou -- nem ele nem a planilha dele existem -- fica sem texto e
    sem aviso, a nao ser o pedido, que e FALTA. marcas.ErroDeMarcas quando o que se espera dos textos nao serve."""
    todas, soltos = marcas_dos_textos(projeto)
    dos_codigos = marcas.confere(todas, NIVEIS, esperados(textos), existem)
    codigos, abertas = {t.codigo for t in textos}, {m.codigo for m in todas if m.nivel == UNIDADE and m.codigo}
    seus = collections.defaultdict(list)
    for x in dos_codigos:
        (seus[x.unidade] if x.unidade in codigos else soltos).append(x)
    colunas, estados = (projeto.valor("coluna_trechos"), projeto.valor("coluna_subdecks")), {}
    for t in textos:
        com_planilha, dos_cartoes = avisos_dos_cartoes(projeto, t, colunas, existem)
        if t.codigo not in abertas and not com_planilha and t.codigo != pedido:
            estados[t.codigo] = SEM_TEXTO
            continue
        if t.codigo not in abertas:
            seus[t.codigo].append(aviso("sem-texto", None, None, t.codigo, None,
                                        f"nenhum texto abre a unidade com {marca(UNIDADE, t.codigo)}"))
        seus[t.codigo] += dos_cartoes
        estados[t.codigo] = estado(seus[t.codigo])
    return seus, soltos, estados


def confere(projeto, pedido=None):
    """(Conferido, []) do material do projeto; com pedido, o codigo de um texto, ele se confere tambem quando nao
    comecou. (None, erros) quando a conferencia dos moldes tem erro ou aviso, dois textos tem o mesmo codigo, nenhum
    texto tem o codigo pedido ou o que se espera dos textos nao serve."""
    moldes, erros = confere_moldes.confere(projeto)
    if erros:
        return None, erros
    c = moldes[0]
    if c.avisos:
        return None, [f"a conferência dos moldes tem {len(c.avisos)} aviso(s): rode o confere_moldes.py e resolva "
                      "cada um antes de conferir o material"]
    textos = [t._replace(codigo=marcas.nfc(t.codigo)) for t in confere_moldes.textos(c)]
    codigos = collections.Counter(t.codigo for t in textos)
    repetidos = sorted(k for k, n in codigos.items() if n > 1)
    if repetidos:
        return None, [f"o código {k!r} é de mais de um texto do material, e os códigos escondidos não os distinguem"
                      for k in repetidos]
    if pedido is not None and pedido not in codigos:
        return None, [f"nenhum texto do material tem o código {pedido!r}"]
    existem = {marcas.nfc(i) for i in c.aula_de}
    try:
        seus, soltos, estados = avisos_e_estados(projeto, textos, existem, pedido)
    except marcas.ErroDeMarcas as e:
        return None, [str(e)]
    return Conferido(moldes, em_ordem_de_escrita(textos, c.aulas), estados, seus, soltos), []


def mostra(conferido, pedido):
    """Mostra os avisos que nao sao de texto nenhum, os de cada texto e a tabela dos textos, na ordem de escrita (com
    pedido, so o texto dele); depois, sem pedido, o proximo a escrever e os que dependem de outros e ja podem ser
    escritos, e quantos ha em cada estado; com pedido, num texto que depende de outros, os que ainda nao estao prontos.
    Devolve o codigo de saida: 1 com FALTA ou ERRO."""
    estados = conferido.estados
    lista = [(t, deps) for t, deps in conferido.lista if pedido in (None, t.codigo)]
    linhas = [linha_do_aviso(x) for x in conferido.soltos]
    linhas += [linha_do_aviso(x) for t, _ in lista for x in conferido.avisos[t.codigo]]
    for linha in linhas:
        print(linha)
    print("\n".join(tabela(COLUNAS, [(t.aula or NENHUM, t.documento["nome"], t.nome, t.codigo, estados[t.codigo])
                                     for t, _ in lista])))
    if pedido is not None:
        for t, deps in lista:
            if t.chave is None:
                print(f"{PEDE}: " + (", ".join(d.codigo for d in deps if estados[d.codigo] != PRONTA) or NENHUM))
    else:
        proxima = next((t for t, _ in lista if estados[t.codigo] != PRONTA), None)
        print(f"{PROXIMA}: {apresenta(proxima) if proxima else NENHUM}")
        for t, deps in lista:
            if t.chave is None and estados[t.codigo] != PRONTA and all(estados[d.codigo] == PRONTA for d in deps):
                print(f"{PODE}: {apresenta(t)}")
        quantos = collections.Counter(estados.values())
        print(f"{len(lista)} textos: {quantos[PRONTA]} prontos, {quantos[FALTA]} com FALTA, {quantos[ERRO]} com ERRO, "
              f"{quantos[SEM_TEXTO]} sem texto")
    return 1 if linhas else 0


# ---------- o comeco ----------

def main(argv=None):
    p = argparse.ArgumentParser(description="Confere o texto e os cartões de cada unidade do material.")
    p.add_argument("--unidade", help="o código de um texto do material: confere só ele")
    p.add_argument("--projeto", type=Path, help="projeto.json (padrao: o primeiro achado subindo a partir daqui)")
    a = p.parse_args(argv)
    pedido = marcas.nfc(a.unidade) if a.unidade is not None else None
    conferido, erros = confere(acha_projeto(a.projeto), pedido)
    return para(erros) if erros else mostra(conferido, pedido)


if __name__ == "__main__":
    sys.exit(main())
