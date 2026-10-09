# SPDX-License-Identifier: GPL-3.0-or-later
# Copyright do codigo sob GPL-3.0 -- ver LICENSE e NOTICE.md na raiz do projeto.

"""
Gera pacotes Anki (.apkg) a partir de QUALQUER CSV de perguntas encontrado direto na
pasta do material gerado (sem entrar em subpastas -- uma eventual subpasta de material
arquivado de outra disciplina nao e conteudo ativo e nao deve ser descoberta aqui). O
script e agnostico de disciplina, de nome de coluna e de caminho: nenhum nome de
disciplina, item, arquivo ou pasta fica fixado no codigo. As pastas, o prefixo das
planilhas e o arquivo de estilo dos cartoes vem do projeto.json ("material_gerado",
"baralhos", "prefixo_planilhas" e "estilo_cartao"), assim como as colunas que ficam
guardadas sem aparecer ("colunas_ocultas") e a coluna que separa os cartoes de uma
planilha em subdecks ("coluna_subdecks", ou null); o nome da disciplina vem do formato
("formato"), que antes e conferido contra o molde dele (formato.schema.json): com erro no
formato, cada erro aparece com ERRO e nenhum pacote e gerado.
O contrato estavel e minimo:

  1. o nome do arquivo comeca com o prefixo das planilhas e termina em ".csv";
  2. existe uma coluna "pergunta" e uma coluna "resposta" -- os dois unicos nomes de
     coluna que o script realmente exige, porque sao intrinsecos a qualquer cartao de
     revisao, nao especificos de nenhuma disciplina.

Qualquer outra coluna e opcional e vira campo do cartao automaticamente, com o nome que
a propria coluna tiver -- nao exige nenhuma mudanca neste script. Uma coluna "fonte" (a
citacao da fonte do fato, que a metodologia pede em toda planilha), se presente,
aparece no verso, abaixo da resposta.

No Anki, os cartoes ficam num deck com o nome da disciplina e, dentro dele, um deck por
planilha (o nome do arquivo sem o prefixo); com "coluna_subdecks", um subdeck por valor
dessa coluna. O ID de cada deck sai de um hash do nome completo dele, entao planilhas e
disciplinas diferentes nunca caem no mesmo deck. Cada arquivo processado vira seu
proprio pacote .apkg. O modelo de nota (campos e template do cartao) e construido a
partir do cabecalho de cada CSV -- CSVs com conjuntos de coluna diferentes ganham
modelos diferentes automaticamente, cada um com ID deterministico a partir do proprio
conjunto de colunas. Planilha sem "pergunta" ou "resposta" aparece com ERRO e fica sem
pacote.

Uso (de qualquer pasta dentro do projeto):
    python scripts/montar_deck.py              # gera um .apkg para cada CSV encontrado
    python scripts/montar_deck.py <trecho>     # gera so os .apkg cujo nome de arquivo contem <trecho>
    python scripts/montar_deck.py --listar     # so lista os CSVs que seriam processados, sem gerar nada
    python scripts/montar_deck.py --projeto projeto.json
"""

import argparse
import csv
import hashlib
import re
import sys
import unicodedata
from pathlib import Path

import genanki

sys.path.insert(0, str(Path(__file__).resolve().parent))
from comum import acha_projeto, le_formato, planilhas  # noqa: E402

# Coluna com a citacao da fonte do fato: se existir, aparece no verso, abaixo da
# resposta, e nao na linha de metadados da frente.
COLUNA_FONTE = "fonte"


def normalizar(texto):
    sem_acento = unicodedata.normalize("NFKD", texto).encode("ascii", "ignore").decode("ascii")
    return sem_acento.lower()


def campo_anki(nome_coluna):
    """Nome de coluna do CSV -> nome de campo do Anki (ex.: "tipo_pergunta" ->
    "TipoPergunta"). Sem espaco, pra nao arriscar problema de sintaxe no template do
    Anki. So formata para leitura -- nao muda o que a coluna significa, e nao presume
    nenhum nome especifico de coluna."""
    return "".join(p.capitalize() for p in re.split(r"[_\s]+", nome_coluna) if p) or "Campo"


def construir_modelo(colunas_extra, rotulo, estilo, ocultas):
    """Monta um genanki.Model com campos Pergunta, Resposta, mais um campo pra cada
    coluna extra que o CSV realmente tiver -- nenhum nome de coluna e exigido pra isso
    funcionar. CSVs com conjuntos de coluna diferentes ganham modelos diferentes, cada
    um com ID deterministico a partir do proprio conjunto de colunas, entao o mesmo
    "formato" de CSV sempre reusa o mesmo modelo ao reimportar. O nome do modelo vem do
    nome da planilha, e o estilo do cartao, do arquivo de estilo do projeto. As colunas
    ocultas viram campo (pra nao perder a informacao), mas nao aparecem na frente."""
    campos_extra = [campo_anki(c) for c in colunas_extra]
    campos_visiveis = [
        campo_anki(c)
        for c in colunas_extra
        if c.lower() not in ocultas and c.lower() != COLUNA_FONTE
    ]
    campo_fonte = next(
        (campo_anki(c) for c in colunas_extra if c.lower() == COLUNA_FONTE), None
    )
    assinatura = ",".join(colunas_extra) or "minimo"
    model_id = id_estavel("modelo::" + assinatura)

    linha_meta = "".join(
        f"{{{{#{c}}}}}<span class=\"meta-item\">{{{{{c}}}}}</span>{{{{/{c}}}}}"
        for c in campos_visiveis
    )

    return genanki.Model(
        model_id,
        rotulo,
        fields=[{"name": "Pergunta"}, {"name": "Resposta"}] + [{"name": c} for c in campos_extra],
        templates=[{
            "name": "Cartao Padrao",
            "qfmt": f'<div class="meta">{linha_meta}</div><div class="pergunta">{{{{Pergunta}}}}</div>',
            "afmt": (
                '{{FrontSide}}<hr id="answer">'
                '<div class="resposta">{{Resposta}}</div>'
                + (
                    f'{{{{#{campo_fonte}}}}}<div class="fonte">{{{{{campo_fonte}}}}}</div>{{{{/{campo_fonte}}}}}'
                    if campo_fonte
                    else ""
                )
            ),
        }],
        css=estilo,
    )


def id_estavel(nome, minimo=1_000_000_000, maximo=1_999_999_999):
    """ID deterministico de 10 digitos a partir do nome do deck: o mesmo nome sempre
    gera o mesmo ID, sem precisar cadastrar cada disciplina manualmente no codigo.
    Reimportar o mesmo .apkg atualiza os cartoes existentes no Anki em vez de duplicar
    o deck, desde que o nome do deck nao mude."""
    digest = hashlib.sha256(nome.encode("utf-8")).hexdigest()
    return minimo + (int(digest, 16) % (maximo - minimo))


def nome_a_partir_do_arquivo(caminho_csv: Path, prefixo: str):
    """"<prefixo>nucleo-dicionarios.csv" -> "Nucleo-Dicionarios". Tira o prefixo (se
    existir) e capitaliza cada palavra separada por hifen -- funciona pra qualquer nome
    de arquivo novo."""
    nome = caminho_csv.stem
    if prefixo and nome.startswith(prefixo):
        nome = nome[len(prefixo):]
    partes = [p for p in nome.split("-") if p] or [caminho_csv.stem]
    return "-".join(p.capitalize() for p in partes)


def montar_pacote(caminho_csv: Path, pasta_saida: Path, prefixo: str, estilo: str, disciplina: str,
                  ocultas, coluna_subdecks):
    """Grava o .apkg da planilha; devolve False, sem gravar nada, se faltar coluna exigida."""
    nome_saida = nome_a_partir_do_arquivo(caminho_csv, prefixo)
    deck_da_planilha = f"{disciplina}::{nome_saida}"

    decks = {}  # chave de deck normalizada -> genanki.Deck, criado sob demanda
    total_cartoes = 0

    with open(caminho_csv, encoding="utf-8") as f:
        leitor = csv.DictReader(f)
        colunas = leitor.fieldnames or []
        if "pergunta" not in colunas or "resposta" not in colunas:
            print(f'ERRO: {caminho_csv.name} precisa ter uma coluna "pergunta" e uma "resposta" '
                  f"(colunas encontradas: {', '.join(colunas) or 'nenhuma'}) -- baralho não gerado")
            return False
        colunas_extra = [c for c in colunas if c not in ("pergunta", "resposta")]
        modelo = construir_modelo(colunas_extra, nome_saida, estilo, ocultas)
        tem_subdecks = bool(coluna_subdecks) and coluna_subdecks in colunas

        for linha in leitor:
            nota = genanki.Note(
                model=modelo,
                fields=[linha["pergunta"].strip(), linha["resposta"].strip()]
                + [linha[c].strip() for c in colunas_extra],
            )

            valor = linha.get(coluna_subdecks, "").strip() if tem_subdecks else ""
            chave_deck = normalizar(valor)
            nome_deck = f"{deck_da_planilha}::{valor.capitalize()}" if valor else deck_da_planilha
            if chave_deck not in decks:
                decks[chave_deck] = genanki.Deck(id_estavel(nome_deck), nome_deck)
            decks[chave_deck].add_note(nota)
            total_cartoes += 1

    caminho_saida = pasta_saida / f"{nome_saida}.apkg"
    pacote = genanki.Package(list(decks.values()))
    pasta_saida.mkdir(parents=True, exist_ok=True)
    pacote.write_to_file(caminho_saida)

    print(f"Deck gerado: {caminho_saida}")
    print(f"  Decks: {', '.join(d.name for d in decks.values())}")
    print(f"  Total de cartões: {total_cartoes}")
    return True


def main(argv=None):
    p = argparse.ArgumentParser(description="Gera pacotes Anki (.apkg) a partir das planilhas de perguntas.")
    p.add_argument("filtro", nargs="?", help="gera só as planilhas cujo nome contém este trecho")
    p.add_argument("--listar", action="store_true", help="só lista as planilhas, sem gerar nada")
    p.add_argument("--projeto", type=Path, help="projeto.json (padrão: o primeiro achado subindo a partir daqui)")
    a = p.parse_args(argv)
    projeto = acha_projeto(a.projeto)
    pasta, prefixo = projeto.caminho("material_gerado"), projeto.valor("prefixo_planilhas")

    csvs = planilhas(projeto, a.filtro)
    if not csvs:
        alvo_desc = f" com filtro {a.filtro!r}" if a.filtro else ""
        raise SystemExit(f"nenhum CSV '{prefixo}*.csv' encontrado em {pasta}{alvo_desc}")

    print(f"CSVs encontrados ({len(csvs)}): {', '.join(c.name for c in csvs)}")
    if a.listar:
        return 0
    arquivo_estilo = projeto.caminho("estilo_cartao")
    if not arquivo_estilo.exists():
        raise SystemExit(f"o arquivo de estilo dos cartões não existe: {arquivo_estilo} -- "
                         "copie modelo-dados/estilo-cartao.css")
    arquivo_formato = projeto.caminho("formato")
    if not arquivo_formato.exists():
        raise SystemExit(f"o formato da disciplina não existe: {arquivo_formato} -- é dele que vem o nome "
                         "da disciplina no Anki")
    formato, erros = le_formato(projeto)
    if erros:
        # o nome da disciplina e o deck de cima de todos os cartoes: com erro no formato
        # (fora do molde, como a disciplina vazia, ou JSON invalido), nenhum baralho e gerado
        for e in erros:
            print(f"ERRO: {e}")
        print("Nenhum baralho gerado: resolva cada ERRO no formato da disciplina e rode de novo.")
        return 1
    disciplina = formato["disciplina"]
    estilo = arquivo_estilo.read_text(encoding="utf-8")
    ocultas = {c.lower() for c in projeto.valor("colunas_ocultas")}
    gerados = [montar_pacote(caminho, projeto.caminho("baralhos"), prefixo, estilo, disciplina, ocultas,
                             projeto.valor("coluna_subdecks")) for caminho in csvs]
    return 0 if all(gerados) else 1


if __name__ == "__main__":
    sys.exit(main())
