# SPDX-License-Identifier: GPL-3.0-or-later
# Copyright do codigo sob GPL-3.0 -- ver LICENSE e NOTICE.md na raiz do projeto.

"""
Monta o documento das divergencias: os fatos que as fontes do material dizem de formas
diferentes, cada um com a forma que o material ensina, as outras e as partes do material que
tratam dele.

O arquivo das divergencias ("divergencias", nos caminhos do projeto.json) segue o molde
esquemas/divergencias.schema.json: para cada fato, o nome dele ("fato"), os codigos dos
trechos das analises que o trazem ("trechos"), a forma que o material ensina ("ensinada") e
as outras ("outras"). Cada forma diz o fato em poucas palavras ("diz") e cita as fontes que a
dao ("fonte"), escrita como a coluna fonte dos cartoes: as chamadas do arquivo de chamadas,
cada uma com o lugar (confere_cartoes.citacao).

O documento ("documento_das_divergencias", nos caminhos) tem o titulo, a abertura e, para
cada fato, na ordem do arquivo, um titulo com o nome dele, a forma ensinada, as outras e,
quando ha, as partes do material que tratam dele, na ordem dos arquivos: cada codigo
escondido de um dos trechos dele nos textos do material (confere_material.lugares_dos_trechos),
com o titulo do texto (o de nivel 1, ou o caminho dele), os nomes do item e da parte abertos
ali e o link para a linha; e cada cartao das planilhas de pergunta com um dos trechos na
coluna dos trechos ("coluna_trechos", no projeto.json), com a planilha, o numero do cartao e a
pergunta. Sem a coluna dos trechos, os cartoes nao entram. As mesmas entradas dao sempre o
mesmo documento.

Aparece ERRO, e nada e gravado: o arquivo das divergencias que falta, fora do UTF-8 ou fora
do molde; o fato repetido, sem contar maiusculas nem espacos; o codigo de trecho que nao
existe nas analises -- o codigo muda quando o texto do trecho muda, e a divergencia tem de
ser vista de novo --; a citacao sem chamada, com texto que nao e chamada, com chamada sem
lugar ou com lugar que a fonte nao tem; o arquivo de chamadas com erro; a planilha que nao se
le (comum.le_planilha); e o que para o conferidor do material (confere_material.confere). Com
--conferir, nada e gravado: aparece FALTA se o documento gravado nao e o que o script
gravaria agora.

Roda tambem sozinho, com --conferir, antes de cada versao gravada pelo git, chamado pelo
verificador (o arquivo pre-commit da pasta .githooks). Quem importa este script tem a leitura
do arquivo das divergencias (le_divergencias), as divergencias de cada codigo de trecho
(por_trecho) e uma divergencia numa linha (em_linha), que a lista de trabalho usa.

Uso (de qualquer pasta dentro do projeto):
    python scripts/divergencias.py
    python scripts/divergencias.py --conferir
    python scripts/divergencias.py --projeto projeto.json
"""

import argparse
import collections
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import confere_material  # noqa: E402
import marcas  # noqa: E402
from comum import (COLUNA_PERGUNTA, acha_projeto, alvo_markdown, le_planilha, link, no_projeto,  # noqa: E402
                   planilhas, rodape_da_licenca)
from confere_cartoes import citacao, le_chamadas, lugares_das_fontes, simples  # noqa: E402
from confere_moldes import nada_gravado  # noqa: E402
from trechos_de_ia import ALVO_DA_LINHA, titulo_do_documento  # noqa: E402
from validar_dados import esquema, le_dados  # noqa: E402

DADOS, DOCUMENTO = "divergencias", "documento_das_divergencias"  # os caminhos do arquivo e do documento
MOLDE = "divergencias"  # o molde do arquivo, em esquemas/, e o nome do modelo em branco dele
TITULO = "# Divergências entre as fontes"
ABERTURA = ("Os fatos que as fontes do material dizem de formas diferentes. De cada um: a forma que o material ensina, "
            "as outras, cada uma com o lugar exato nas fontes, e as partes do material que tratam dele.")
ENSINADA, OUTRA = "o material ensina", "outra forma"  # os rotulos das formas de uma divergencia
TRATAM = "Partes do material que tratam dele"
NA_CITACAO = "citação"  # o lugar da citacao de uma forma, que os erros dela dizem
CARTAO = "cartão {}"  # um cartao de uma planilha, pelo numero dele, a partir de 1
Uso = collections.namedtuple("Uso", "arquivo linha cartao nomes")
# uma parte do material que trata de um fato: o arquivo; a linha, num texto, ou o numero, num cartao (o outro,
# None); e o que a nomeia, numa tupla: o titulo do texto e os nomes da regiao, ou o cartao e a pergunta dele


# ---------- o arquivo das divergencias ----------

def le_divergencias(projeto):
    """(divergencias, erros): a lista do arquivo das divergencias, lido contra o molde dele; sem o arquivo, fora do
    UTF-8 ou fora do molde, so os erros."""
    arquivo = projeto.caminho(DADOS)
    nome = no_projeto(arquivo, projeto)
    if not arquivo.is_file():
        return None, [f"{nome}: o arquivo das divergências não existe -- copie modelo-dados/{MOLDE}.json"]
    dados, erros = le_dados(arquivo, esquema(MOLDE), nome)
    return (None, erros) if erros else (dados["divergencias"], [])


def codigos(divergencia):
    """Os codigos de trecho da divergencia, em NFC, sem repetir, na ordem."""
    return list(dict.fromkeys(marcas.nfc(c) for c in divergencia["trechos"]))


def por_trecho(divergencias):
    """{codigo: [divergencia]} de cada codigo de trecho das divergencias, cada um com as dele, na ordem do arquivo."""
    saida = {}
    for d in divergencias:
        for c in codigos(d):
            saida.setdefault(c, []).append(d)
    return saida


def formas(divergencia):
    """[(rotulo, forma)] da divergencia: a ensinada e, depois, cada uma das outras, na ordem."""
    return [(ENSINADA, divergencia["ensinada"])] + [(OUTRA, f) for f in divergencia["outras"]]


def em_texto(forma):
    """Uma forma em texto: o que ela diz e a citacao das fontes."""
    return f"{forma['diz']} {forma['fonte']}"


def em_linha(divergencia):
    """A divergencia numa linha: o fato e cada forma, com o rotulo dela."""
    return f"{divergencia['fato']} — " + "; ".join(f"{r}: {em_texto(f)}" for r, f in formas(divergencia))


def erros_das_divergencias(projeto, divergencias, existem):
    """Os erros das divergencias: o fato repetido, sem contar maiusculas nem espacos; o codigo de trecho que nao existe;
    e a citacao de cada forma que nao confere (confere_cartoes.citacao). Com erro no arquivo de chamadas, so ele; sem
    divergencia, nenhum, porque nao ha citacao a conferir."""
    if not divergencias:
        return []
    nucleos, erros = le_chamadas(projeto)
    if erros:
        return erros
    indice, primeiro = lugares_das_fontes(projeto), {}
    for k, d in enumerate(divergencias, 1):
        onde, chave = f"divergência {k} ({d['fato']})", simples(d["fato"]).casefold()
        if chave in primeiro:
            erros.append(f"{onde}: o fato é o mesmo da divergência {primeiro[chave]}")
        primeiro.setdefault(chave, k)
        erros += [f"{onde}: o código {c} não existe nas análises -- o texto do trecho pode ter mudado"
                  for c in codigos(d) if c not in existem]
        for rotulo, forma in formas(d):
            erros += [f"{onde}, {rotulo}: {e}" for e in citacao(forma["fonte"], nucleos, indice, NA_CITACAO)[0]]
    return erros


# ---------- as partes do material que tratam de cada fato ----------

def nomes_das_regioes(conferido):
    """{caminho: [nome do item, nome da parte]} de cada regiao dos textos do material, pelo caminho dos codigos
    escondidos, em NFC; o item fica de fora na parte que nao esta num item."""
    saida = {}
    for t, _ in conferido.lista:
        for p in t.partes:
            item = marcas.nfc(p.item["id"]) if p.item else None
            saida[(t.codigo, item, marcas.nfc(p.id))] = ([p.item["nome"]] if p.item else []) + [p.nome]
    return saida


def nos_textos(projeto, conferido, seus):
    """{codigo: [Uso]} de cada codigo dado nos textos do material, na ordem dos arquivos e das linhas: o titulo do texto
    e os nomes da regiao aberta ali -- os codigos dela, quando os textos do material nao a tem."""
    regioes, titulos, saida = nomes_das_regioes(conferido), {}, {}
    for c, lugares_ in confere_material.lugares_dos_trechos(projeto).items():
        if c not in seus:
            continue
        for m, caminho in lugares_:
            arquivo = projeto.raiz / m.arquivo
            if arquivo not in titulos:
                titulos[arquivo] = titulo_do_documento(arquivo, projeto)
            regiao = regioes.get(caminho) or [marcas.mostra(caminho, confere_material.NIVEIS)]
            saida.setdefault(c, []).append(Uso(arquivo, m.linha, None, (titulos[arquivo], *regiao)))
    return saida


def nos_cartoes(projeto, seus):
    """({codigo: [Uso]}, erros) de cada codigo dado nos cartoes das planilhas de pergunta, na coluna dos trechos, na
    ordem das planilhas e dos cartoes: o numero do cartao e a pergunta, quando ha; nenhum, sem a coluna dos trechos
    no projeto.json. A planilha que nao se le e erro."""
    coluna, saida, erros = projeto.valor("coluna_trechos"), {}, []
    if not coluna:
        return saida, erros
    for arquivo in planilhas(projeto):
        _, cartoes, ruins = le_planilha(arquivo, no_projeto(arquivo, projeto))
        erros += ruins
        for k, cartao in enumerate(cartoes, 1):
            pergunta = (cartao.get(COLUNA_PERGUNTA) or "").strip()
            nomes = (CARTAO.format(k), pergunta) if pergunta else (CARTAO.format(k),)
            for c in confere_material.codigos_do_cartao(cartao, coluna):
                if c in seus:
                    saida.setdefault(c, []).append(Uso(arquivo, None, k, nomes))
    return saida, erros


def em_ordem(usos_):
    """Os usos sem repetir, na ordem dos arquivos e, em cada um, das linhas ou dos cartoes."""
    return sorted(set(usos_), key=lambda u: (u.arquivo, u.linha or 0, u.cartao or 0))


def usos(projeto, conferido, divergencias):
    """([[Uso]] de cada divergencia, na ordem do arquivo, erros): as partes do material que tratam do fato, as de
    todos os trechos dele juntas, os textos antes das planilhas, cada grupo em ordem (em_ordem)."""
    seus = set(por_trecho(divergencias))
    dos_textos = nos_textos(projeto, conferido, seus)
    dos_cartoes, erros = nos_cartoes(projeto, seus)
    return [em_ordem(u for c in codigos(d) for u in dos_textos.get(c, []))
            + em_ordem(u for c in codigos(d) for u in dos_cartoes.get(c, [])) for d in divergencias], erros


# ---------- o documento ----------

def linha_do_uso(uso, saida):
    """A linha de uma parte do material no documento: o que a nomeia e o link para a linha do texto, ou o link para a
    planilha do cartao."""
    alvo = link(uso.arquivo, saida)
    if uso.linha is None:
        return f"  - [{uso.arquivo.name}]({alvo_markdown(alvo)}), " + ": ".join(uso.nomes)
    return f"  - {', '.join(uso.nomes)}: [linha {uso.linha}]({alvo_markdown(ALVO_DA_LINHA.format(alvo, uso.linha))})"


def documento(projeto, divergencias, usos_):
    """O texto do documento das divergencias."""
    saida = projeto.caminho(DOCUMENTO)
    corpo = [TITULO, "", ABERTURA, ""]
    for d, seus in zip(divergencias, usos_):
        corpo += [f"## {d['fato']}", ""] + [f"- {r[0].upper()}{r[1:]}: {em_texto(f)}" for r, f in formas(d)]
        corpo += ([f"- {TRATAM}:"] + [linha_do_uso(u, saida) for u in seus] if seus else []) + [""]
    return "\n".join(corpo + rodape_da_licenca(projeto.caminho("licenca_conteudo"),
                                              projeto.valor("nome_licenca_conteudo"), saida)) + "\n"


def monta(projeto):
    """(texto do documento, quantas divergencias, []) ou (None, 0, erros)."""
    divergencias, erros = le_divergencias(projeto)
    if erros:
        return None, 0, erros
    conferido, erros = confere_material.confere(projeto)
    if erros:
        return None, 0, erros
    existem = {marcas.nfc(i) for i in conferido.moldes[0].aula_de}
    erros = erros_das_divergencias(projeto, divergencias, existem)
    usos_, dos_cartoes = usos(projeto, conferido, divergencias)
    erros += dos_cartoes
    if erros:
        return None, 0, erros
    return documento(projeto, divergencias, usos_), len(divergencias), []


def main(argv=None):
    p = argparse.ArgumentParser(description="Monta o documento das divergências entre as fontes do material.")
    p.add_argument("--conferir", action="store_true",
                   help="não grava: confere se o documento gravado é o que o script gravaria agora")
    p.add_argument("--projeto", type=Path, help="projeto.json (padrao: o primeiro achado subindo a partir daqui)")
    a = p.parse_args(argv)
    projeto = acha_projeto(a.projeto)
    texto, quantas, erros = monta(projeto)
    if erros:
        return nada_gravado(erros)
    saida = projeto.caminho(DOCUMENTO)
    if a.conferir:
        if not saida.is_file() or saida.read_text(encoding="utf-8") != texto:
            print(f"FALTA: o documento {no_projeto(saida, projeto)} não é o que as divergências e o material dão: "
                  "rode python scripts/divergencias.py")
            return 1
        print(f"O documento das divergências está em dia: {quantas} divergência(s).")
        return 0
    saida.parent.mkdir(parents=True, exist_ok=True)
    saida.write_text(texto, encoding="utf-8")
    print(f"{quantas} divergência(s) gravada(s) em {no_projeto(saida, projeto)}.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
