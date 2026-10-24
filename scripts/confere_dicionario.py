# SPDX-License-Identifier: GPL-3.0-or-later
# Copyright do codigo sob GPL-3.0 -- ver LICENSE e NOTICE.md na raiz do projeto.

"""
Confere os codigos dos titulos do dicionario das duvidas (o caminho "dicionario_das_duvidas"
do projeto.json), pela regra do titulo de uma duvida: a busca pelo codigo so acha a duvida
cujo titulo segue a regra.

Cada duvida comeca num titulo de segundo nivel, fora dos blocos de codigo: "## " e os codigos
do que ela toca, cada um entre crases e separados por um espaco. Cada codigo e o de uma aula
(so a aula), o de um slide (a aula e o slide) ou o de um trecho das aulas inteiro, lido como
se le o id de um trecho (analises.le_codigo). Nenhum codigo do titulo e o comeco de outro
dele, parte por parte, nem se repete; e os codigos ficam em ordem de aula (a ordem natural,
em que 9 vem antes de 10), de slide e de posicao, do menor numero para o maior.

Cada titulo fora da regra da uma linha ERRO para cada problema, com o arquivo, a linha do
titulo e o motivo, e o script sai com codigo 1; sem problema, diz quantos titulos conferiu.
Sao ERRO tambem o projeto.json sem o caminho do dicionario, o dicionario que falta e o que
nao esta em UTF-8. O script nao grava nada.

Uso (de qualquer pasta dentro do projeto):
    python scripts/confere_dicionario.py
    python scripts/confere_dicionario.py --projeto projeto.json
"""

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from analises import le_codigo, ordem_natural  # noqa: E402
from comum import acha_projeto, linhas_fora_de_codigo, no_projeto  # noqa: E402
from validar_dados import le_texto  # noqa: E402

CAMINHO_DICIONARIO = "dicionario_das_duvidas"  # o caminho do dicionario, nos caminhos do projeto.json
TITULO = "## "  # o comeco do titulo de cada duvida
CRASE = "`"  # o que fica antes e depois de cada codigo do titulo
ENTRE_CODIGOS = " "  # o que separa um codigo do seguinte, no titulo


def entre_crases(pedaco):
    """O codigo de um pedaco do titulo escrito entre crases, sem crase dentro; None quando o pedaco nao e assim."""
    dentro = pedaco[len(CRASE):-len(CRASE)]
    if pedaco.startswith(CRASE) and pedaco.endswith(CRASE) and CRASE not in dentro:
        return dentro
    return None


def codigo_do_titulo(codigo):
    """O Codigo (analises.le_codigo) do codigo de uma aula, de um slide ou de um trecho inteiro; None quando ele nao e
    nenhum dos tres, como o comeco de um id que vai ate a posicao."""
    lido = le_codigo(codigo)
    return None if lido is None or (lido.posicao is not None and lido.hash is None) else lido


def cobre(codigo, outro):
    """Se o Codigo e o comeco do outro, parte por parte; o mesmo codigo cobre a si mesmo."""
    return all(parte is None or parte == do_outro for parte, do_outro in zip(codigo, outro))


def lugar_na_ordem(lido):
    """A chave da ordem dos codigos: a aula na ordem natural, o slide e a posicao, com o que falta antes de tudo."""
    return ordem_natural(lido.aula), lido.aula, lido.slide or 0, lido.posicao or 0


def erros_do_titulo(titulo):
    """Os motivos por que o titulo, sem o TITULO do comeco, sai da regra; nenhum quando ele a segue."""
    codigos = [entre_crases(pedaco) for pedaco in titulo.split(ENTRE_CODIGOS)]
    if None in codigos:
        return ["o título não é só de códigos, cada um entre crases, separados por um espaço"]
    lidos = [codigo_do_titulo(codigo) for codigo in codigos]
    erros = [f"o código {c!r} não é de uma aula, de um slide nem de um trecho"
             for c, lido in zip(codigos, lidos) if lido is None]
    if erros:
        return erros
    pares = [(i, j) for i in range(len(lidos)) for j in range(i + 1, len(lidos))]
    erros = [f"o código {codigos[i]!r} cobre o código {codigos[j]!r}" for i, j in pares
             if cobre(lidos[i], lidos[j]) or cobre(lidos[j], lidos[i])]
    ordem = [lugar_na_ordem(lido) for lido in lidos]
    if ordem != sorted(ordem):
        erros.append("os códigos não estão em ordem de aula, de slide e de posição")
    return erros


def confere(projeto):
    """(erros, quantos titulos): cada erro com o arquivo e a linha do titulo."""
    if CAMINHO_DICIONARIO not in projeto.dados["caminhos"]:
        return [f"o projeto.json não diz o caminho do dicionário das dúvidas ({CAMINHO_DICIONARIO!r}, nos caminhos)"], 0
    arquivo = projeto.caminho(CAMINHO_DICIONARIO)
    nome = no_projeto(arquivo, projeto)
    if not arquivo.is_file():
        return [f"falta o dicionário das dúvidas: {nome}"], 0
    texto, erros = le_texto(arquivo, nome)
    if erros:
        return erros, 0
    titulos = [(n, linha[len(TITULO):]) for n, linha in linhas_fora_de_codigo(texto) if linha.startswith(TITULO)]
    return [f"{nome}:{n}: {erro}" for n, titulo in titulos for erro in erros_do_titulo(titulo)], len(titulos)


def main(argv=None):
    p = argparse.ArgumentParser(description="Confere os códigos dos títulos do dicionário das dúvidas.")
    p.add_argument("--projeto", type=Path, help="projeto.json (padrao: o primeiro achado subindo a partir daqui)")
    a = p.parse_args(argv)
    erros, titulos = confere(acha_projeto(a.projeto))
    for erro in erros:
        print("ERRO:", erro)
    if erros:
        return 1
    print(f"{titulos} título(s) do dicionário das dúvidas conferido(s), todos na regra.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
