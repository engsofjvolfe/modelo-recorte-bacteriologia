# SPDX-License-Identifier: GPL-3.0-or-later
# Copyright do codigo sob GPL-3.0 -- ver LICENSE e NOTICE.md na raiz do projeto.

"""
Gera os pacotes do Anki (.apkg) das planilhas de pergunta: os CSVs direto na pasta do material
gerado cujo nome comeca com o prefixo das planilhas (comum.planilhas), um pacote por planilha.
Nenhum nome de disciplina, de coluna, de arquivo ou de pasta fica no codigo: as pastas, o
prefixo, o estilo dos cartoes, as colunas que ficam guardadas sem aparecer ("colunas_ocultas")
e a que divide o baralho ("coluna_subdecks", ou null) vem do projeto.json; o nome da disciplina
e as colunas do cartao vem do formato, conferido contra o molde dele (comum.le_formato).

As colunas do cartao sao as do documento de molde "colunas" do formato, na ordem dele, cada uma
com o lado em que aparece, frente ou verso; a de imagem ("imagem": true) traz o nome de um
arquivo da pasta das imagens dos cartoes ("imagens_cartoes"). Sao ERRO, e nenhum pacote e
gerado: o formato sem esse documento ou com mais de um; o documento sem a coluna da pergunta
(comum.COLUNA_PERGUNTA) ou sem coluna na frente; a coluna num lado que o baralho nao conhece; a
coluna oculta que e do molde; a coluna que divide o baralho que nao e do molde nem oculta; a
coluna que nao tem nenhuma palavra, a que da o nome de um campo que o proprio Anki preenche
(como "Tags" ou "FrontSide") e a que da um nome que o Anki muda ao importar (com ':', '{', '}'
ou '"', ou que comeca com '#', '/' ou '^'); e duas colunas que dao o mesmo campo, sem contar
maiuscula e minuscula, que o Anki nao distingue no nome do campo.

Cada coluna do molde vira um campo do cartao, no lado dela, dentro de um bloco com a classe do
id dela (a classe que o arquivo de estilo, "estilo_cartao", usa para ela), e o campo vazio nao
aparece. O campo de imagem mostra a imagem pelo nome do arquivo, e o arquivo vai no pacote.
Cada coluna oculta vira um campo guardado, que nao aparece, vazio quando a planilha nao a tem.
O nome de cada campo e o da coluna sem o sublinhado e com cada palavra em maiuscula
("tipo_pergunta" -> "TipoPergunta").

Sao ERRO na planilha, e ela fica sem pacote: a coluna do molde que falta, a coluna que nao e do
molde nem oculta, a coluna repetida, o texto fora do UTF-8, o cartao com mais valores que
colunas, o cartao sem pergunta, a pergunta repetida (sem contar os espacos), a imagem que nao e
so o nome de um arquivo ou que nao esta na pasta das imagens dos cartoes, e o cartao sem valor
na coluna que divide o baralho.

O codigo de cada cartao no Anki sai do nome da planilha e da pergunta, sem contar os espacos:
mudar a resposta, o porque, a fonte ou uma imagem atualiza o mesmo cartao, com o historico de
revisao, e mudar a pergunta faz um cartao novo. O cartao novo entra na posicao da linha dele.

No Anki, os cartoes ficam no baralho "<disciplina>::<coluna que divide> <valor>::<planilha>",
cada um no do valor dele; sem a coluna que divide, em "<disciplina>::<planilha>". O nome da
planilha e o do arquivo sem o prefixo, com cada palavra em maiuscula; duas planilhas com o
mesmo nome sao ERRO, e nenhuma das duas ganha pacote. O id de cada baralho sai de um hash do
nome dele, e o do modelo do cartao, da disciplina e dos campos: sempre os mesmos.

O pacote da planilha com alguma imagem fica na pasta dos baralhos com imagens
("baralhos_com_imagens"), na pasta protegida, porque a imagem e de outras pessoas e nunca se
publica; o da planilha sem imagem, na pasta dos baralhos ("baralhos"). O pacote da mesma
planilha que estiver na outra pasta sai. O conteudo do pacote e o mesmo a cada vez; o arquivo
leva a hora em que foi feito. Nada fica na pasta temporaria do sistema.

Uso (de qualquer pasta dentro do projeto):
    python scripts/montar_deck.py              # gera um .apkg para cada planilha
    python scripts/montar_deck.py <trecho>     # so as planilhas cujo nome contem <trecho>
    python scripts/montar_deck.py --listar     # so lista as planilhas, sem gerar nada
    python scripts/montar_deck.py --projeto projeto.json
"""

import argparse
import hashlib
import html
import re
import sys
import tempfile
from collections import namedtuple
from pathlib import Path

import genanki

sys.path.insert(0, str(Path(__file__).resolve().parent))
from comum import (COLUNA_PERGUNTA, EXTENSAO_PLANILHA, MOLDE_DOS_CARTOES, acha_projeto, junta,  # noqa: E402
                   le_formato, le_planilha, no_projeto, planilhas, repetidos)
from validar_dados import le_texto  # noqa: E402

FRENTE, VERSO = "frente", "verso"  # os lados do cartao (esquemas/formato.schema.json)
# os campos que o proprio Anki preenche no cartao (manual do Anki, "Special Fields"), como o que repete a frente no
# verso: um campo da planilha com o nome de um deles se confundiria com ele
FRENTE_NO_VERSO = "FrontSide"
CAMPOS_DO_ANKI = ("Tags", "Type", "Deck", "Subdeck", "CardFlag", "Card", FRENTE_NO_VERSO)
# o que o Anki tira do nome de um campo ao importar (rslib/src/notetype/fields.rs, fix_name): estes caracteres em
# qualquer lugar, e estes no comeco; o nome que ele muda deixa de ser o do modelo
FORA_DO_NOME, FORA_DO_COMECO = ':{}"', "#/^"
SEPARADOR = '<hr id="answer">'  # no verso, entre a frente e o resto: o Anki rola o cartao ate ele
NIVEL_DO_BARALHO = "::"  # o que separa, no nome de um baralho do Anki, o baralho de dentro do de fora
EXTENSAO_DO_PACOTE = ".apkg"  # a do arquivo que o Anki importa com os baralhos, o modelo e as imagens
Coluna = namedtuple("Coluna", "id lado imagem campo")  # uma coluna do molde dos cartoes e o nome do campo dela
# o que vale para todas as planilhas: o nome da disciplina, as colunas do molde, as ocultas e a que divide o baralho,
# o modelo do cartao, o prefixo das planilhas e as pastas das imagens, dos baralhos e dos baralhos com imagens
Config = namedtuple("Config", "disciplina colunas ocultas coluna_subdecks modelo prefixo imagens baralhos com_imagens")


def palavras(nome_coluna):
    """As palavras do nome de uma coluna, separadas por sublinhado ou espaco."""
    return [p for p in re.split(r"[_\s]+", nome_coluna) if p]


def campo_anki(nome_coluna):
    """Nome de coluna do CSV -> nome de campo do Anki (ex.: "tipo_pergunta" -> "TipoPergunta"). Sem espaco, pra nao
    arriscar problema de sintaxe no template do Anki. So formata para leitura: nao muda o que a coluna significa."""
    return "".join(p.capitalize() for p in palavras(nome_coluna))


def id_estavel(nome, minimo=1_000_000_000, maximo=1_999_999_999):
    """ID deterministico de 10 digitos a partir de um nome: o mesmo nome sempre da o mesmo ID, e reimportar o mesmo
    .apkg atualiza no Anki o baralho e o modelo que ja existem, em vez de duplicar."""
    digest = hashlib.sha256(nome.encode("utf-8")).hexdigest()
    return minimo + (int(digest, 16) % (maximo - minimo))


def nome_a_partir_do_arquivo(caminho_csv: Path, prefixo: str):
    """"<prefixo>nucleo-dicionarios.csv" -> "Nucleo-Dicionarios". Tira o prefixo (se existir) e capitaliza cada
    palavra separada por hifen -- funciona pra qualquer nome de arquivo novo."""
    nome = caminho_csv.stem
    if prefixo and nome.startswith(prefixo):
        nome = nome[len(prefixo):]
    partes = [p for p in nome.split("-") if p] or [caminho_csv.stem]
    return "-".join(p.capitalize() for p in partes)


def rotulo_da_coluna(coluna):
    """"aula" -> "Aula": o nome da coluna no nome de um baralho, com espaco no lugar do sublinhado e a primeira letra
    em maiuscula."""
    texto = " ".join(palavras(coluna))
    return texto[:1].upper() + texto[1:]


def valor_de(linha, coluna):
    """O valor do cartao na coluna, sem os espacos das pontas; vazio quando a planilha nao o tem."""
    return (linha.get(coluna) or "").strip()


# ---------- as colunas ----------

def colunas_do_molde(formato):
    """([Coluna], erros): as colunas do documento dos cartoes, na ordem do formato. O formato sem esse documento ou com
    mais de um, e o documento sem a coluna da pergunta ou sem coluna na frente, sao erro."""
    docs = [d for d in formato["documentos"] if d["molde"] == MOLDE_DOS_CARTOES]
    if len(docs) != 1:
        ids = f" ({', '.join(d['id'] for d in docs)})" if docs else ""
        return [], [f"o formato tem {len(docs)} documento(s) de molde {MOLDE_DOS_CARTOES!r}{ids}; o baralho pede um "
                    "só, o dos cartões"]
    doc = docs[0]
    colunas = [Coluna(c["id"], c["lado"], c.get("imagem", False), campo_anki(c["id"])) for c in doc["colunas"]]
    erros = [] if any(c.id == COLUNA_PERGUNTA for c in colunas) else [
        f"o documento {doc['id']!r} não tem a coluna {COLUNA_PERGUNTA!r}, que dá o código de cada cartão no Anki"]
    if not any(c.lado == FRENTE for c in colunas):
        erros.append(f"o documento {doc['id']!r} não tem coluna na frente do cartão")
    erros += [f"a coluna {c.id!r} tem o lado {c.lado!r}, que o baralho não conhece" for c in colunas
              if c.lado not in (FRENTE, VERSO)]
    return colunas, erros


def erro_do_campo(coluna):
    """O que impede o nome de campo da coluna no Anki, ou None: nenhuma palavra, o nome de um campo que o proprio Anki
    preenche, ou o que o Anki tira do nome ao importar."""
    campo = campo_anki(coluna)
    if not campo:
        return f"a coluna {coluna!r} não dá nome de campo no Anki: não tem nenhuma palavra"
    if campo in CAMPOS_DO_ANKI:
        return f"a coluna {coluna!r} dá o campo {campo!r}, que é um dos que o próprio Anki preenche"
    if any(c in FORA_DO_NOME for c in campo) or campo[0] in FORA_DO_COMECO:
        return f"a coluna {coluna!r} dá o campo {campo!r}, que o Anki muda ao importar"
    return None


def erros_das_colunas_do_projeto(colunas, ocultas, coluna_subdecks):
    """O que nao fecha entre as colunas do molde e as do projeto.json: a coluna oculta que e do molde, a coluna que
    divide o baralho que nao e do molde nem oculta, a coluna que nao da um nome de campo que o Anki aceite como esta
    (erro_do_campo) e duas colunas que dao o mesmo campo no Anki, que nao distingue maiuscula de minuscula no nome do
    campo (rslib/src/notetype/mod.rs, ensure_names_unique)."""
    do_molde = [c.id for c in colunas]
    erros = [f"a coluna {o!r} está nas colunas ocultas e no molde dos cartões" for o in ocultas if o in do_molde]
    if coluna_subdecks and coluna_subdecks not in do_molde + ocultas:
        erros.append(f"a coluna que divide o baralho, {coluna_subdecks!r}, não é do molde dos cartões nem oculta")
    erros += [e for e in map(erro_do_campo, do_molde + ocultas) if e]
    return erros + [f"as colunas {', '.join(map(repr, cs))} dão o mesmo campo no Anki, {campo!r}"
                    for campo, cs in repetidos((campo_anki(c).casefold(), c) for c in do_molde + ocultas
                                               if campo_anki(c))]


# ---------- o modelo do cartao ----------

def bloco(coluna):
    """O campo da coluna num bloco com a classe do id dela, que nao aparece quando o campo esta vazio."""
    return f'{{{{#{coluna.campo}}}}}<div class="{coluna.id}">{{{{{coluna.campo}}}}}</div>{{{{/{coluna.campo}}}}}'


def construir_modelo(colunas, ocultas, disciplina, estilo):
    """O modelo do cartao: um campo para cada coluna do molde, na ordem dele, e um para cada coluna oculta, que nao
    aparece; a frente com os blocos das colunas da frente, e o verso com a frente e os das colunas do verso. O id sai
    da disciplina e dos campos: as planilhas usam o mesmo modelo, e o Anki o atualiza ao importar."""
    campos = [c.campo for c in colunas] + [campo_anki(o) for o in ocultas]
    frente = "".join(bloco(c) for c in colunas if c.lado == FRENTE)
    verso = f"{{{{{FRENTE_NO_VERSO}}}}}{SEPARADOR}" + "".join(bloco(c) for c in colunas if c.lado == VERSO)
    return genanki.Model(id_estavel(f"modelo::{disciplina}::" + ",".join(campos)), disciplina,
                         fields=[{"name": c} for c in campos],
                         templates=[{"name": disciplina, "qfmt": frente, "afmt": verso}], css=estilo,
                         sort_field_index=campos.index(campo_anki(COLUNA_PERGUNTA)))


# ---------- uma planilha ----------

def erros_do_cabecalho(cabecalho, cfg):
    do_molde = [c.id for c in cfg.colunas]
    return ([f"falta a coluna {c!r} do molde dos cartões" for c in do_molde if c not in cabecalho]
            + [f"a coluna {c!r} não é do molde dos cartões nem oculta" for c in cabecalho
               if c not in do_molde + cfg.ocultas]
            + [f"a coluna {c!r} se repete" for c, _ in repetidos((c, c) for c in cabecalho)])


def imagem_do_cartao(nome, cfg, projeto):
    """(arquivo, erro): o arquivo da imagem de um cartao, pelo nome que a planilha da, na pasta das imagens dos
    cartoes; o nome que nao e so o de um arquivo, ou o arquivo que nao esta la, e erro."""
    if Path(nome).name != nome or nome in (".", "..") or "\\" in nome:
        return None, f"{nome!r} não é só o nome de um arquivo"
    arquivo = cfg.imagens / nome
    if not arquivo.is_file():
        return None, f"a imagem {nome!r} não está em {no_projeto(cfg.imagens, projeto)}"
    return arquivo, None


def nome_do_deck(cfg, planilha, valor):
    meio = [f"{rotulo_da_coluna(cfg.coluna_subdecks)} {valor}"] if cfg.coluna_subdecks else []
    return NIVEL_DO_BARALHO.join([cfg.disciplina, *meio, planilha])


def notas_da_planilha(caminho, cfg, projeto):
    """({nome do baralho: [nota]}, imagens, erros): as notas da planilha, na ordem das linhas, cada uma no baralho do
    valor dela na coluna que divide o baralho, e os arquivos das imagens que elas mostram; cada erro com o nome da
    planilha na frente."""
    cabecalho, linhas, da_leitura = le_planilha(caminho, caminho.name)
    erros = erros_do_cabecalho(cabecalho, cfg) if cabecalho is not None else []
    if cabecalho is None or erros:
        return {}, set(), da_leitura + [f"{caminho.name}: {e}" for e in erros]
    planilha, decks, imagens, perguntas = nome_a_partir_do_arquivo(caminho, cfg.prefixo), {}, set(), {}
    for k, linha in enumerate(linhas, 1):
        pergunta = junta([valor_de(linha, COLUNA_PERGUNTA)])
        if not pergunta:
            erros.append(f"o cartão {k} não tem pergunta")
        elif pergunta in perguntas:
            erros.append(f"a pergunta do cartão {k} repete a do cartão {perguntas[pergunta]}")
        perguntas.setdefault(pergunta, k)
        campos = []
        for c in cfg.colunas:
            texto = valor_de(linha, c.id)
            if c.imagem and texto:
                arquivo, erro = imagem_do_cartao(texto, cfg, projeto)
                if erro:
                    erros.append(f"o cartão {k}, na coluna {c.id!r}: {erro}")
                else:
                    imagens.add(arquivo)
                texto = f'<img src="{html.escape(texto)}">'
            campos.append(texto)
        valor_do_deck = valor_de(linha, cfg.coluna_subdecks) if cfg.coluna_subdecks else None
        if cfg.coluna_subdecks and not valor_do_deck:
            erros.append(f"o cartão {k} não tem valor na coluna {cfg.coluna_subdecks!r}, que dá o baralho dele")
        nota = genanki.Note(model=cfg.modelo, fields=campos + [valor_de(linha, o) for o in cfg.ocultas],
                            guid=genanki.guid_for(caminho.stem, pergunta), due=k)
        decks.setdefault(nome_do_deck(cfg, planilha, valor_do_deck), []).append(nota)
    return decks, imagens, da_leitura + [f"{caminho.name}: {e}" for e in erros]


def escreve_pacote(pacote, arquivo):
    """Grava o pacote do Anki no arquivo. O genanki grava antes o banco do pacote num arquivo temporario e nao o
    apaga (genanki 0.13, Package.write_to_file); por isso o arquivo temporario fica numa pasta propria, que sai
    inteira no fim, e nada fica na pasta temporaria do sistema."""
    with tempfile.TemporaryDirectory() as propria:
        antes, tempfile.tempdir = tempfile.tempdir, propria
        try:
            pacote.write_to_file(str(arquivo))
        finally:
            tempfile.tempdir = antes


def grava_pacote(caminho, decks, imagens, cfg, projeto):
    """Grava o pacote da planilha na pasta dos baralhos com imagens, se alguma nota mostra imagem, ou na dos
    baralhos; tira o pacote da mesma planilha da outra pasta."""
    pasta, outra = (cfg.com_imagens, cfg.baralhos) if imagens else (cfg.baralhos, cfg.com_imagens)
    nome = f"{nome_a_partir_do_arquivo(caminho, cfg.prefixo)}{EXTENSAO_DO_PACOTE}"
    baralhos = []
    for nome_deck, notas in decks.items():
        deck = genanki.Deck(id_estavel(nome_deck), nome_deck)
        for nota in notas:
            deck.add_note(nota)
        baralhos.append(deck)
    pasta.mkdir(parents=True, exist_ok=True)
    escreve_pacote(genanki.Package(baralhos, media_files=[str(a) for a in sorted(imagens)]), pasta / nome)
    print(f"Baralho gerado: {no_projeto(pasta / nome, projeto)}")
    print(f"  No Anki: {'; '.join(decks)}")
    print(f"  Cartões: {sum(len(n) for n in decks.values())} | imagens: {len(imagens)}")
    velho = outra / nome
    if velho.is_file() and velho.resolve() != (pasta / nome).resolve():
        velho.unlink()
        print(f"  Saiu o pacote da mesma planilha em {no_projeto(outra, projeto)}")


# ---------- todas ----------

def configuracao(projeto):
    """(Config, erros): o que vale para todas as planilhas, do formato e do projeto.json; com erro, None e os erros."""
    formato, erros = le_formato(projeto)
    if erros:
        return None, erros
    colunas, erros = colunas_do_molde(formato)
    ocultas, coluna_subdecks = list(projeto.valor("colunas_ocultas")), projeto.valor("coluna_subdecks")
    erros = erros or erros_das_colunas_do_projeto(colunas, ocultas, coluna_subdecks)
    arquivo_estilo = projeto.caminho("estilo_cartao")
    estilo, erros_do_estilo = le_texto(arquivo_estilo, arquivo_estilo.name)
    erros += erros_do_estilo
    if erros:
        return None, erros
    modelo = construir_modelo(colunas, ocultas, formato["disciplina"], estilo)
    return Config(formato["disciplina"], colunas, ocultas, coluna_subdecks, modelo, projeto.valor("prefixo_planilhas"),
                  projeto.caminho("imagens_cartoes"), projeto.caminho("baralhos"),
                  projeto.caminho("baralhos_com_imagens")), []


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
        raise SystemExit(f"nenhum CSV '{prefixo}*{EXTENSAO_PLANILHA}' encontrado em {pasta}{alvo_desc}")

    print(f"CSVs encontrados ({len(csvs)}): {', '.join(c.name for c in csvs)}")
    if a.listar:
        return 0
    arquivo_estilo = projeto.caminho("estilo_cartao")
    if not arquivo_estilo.exists():
        raise SystemExit(f"o arquivo de estilo dos cartões não existe: {arquivo_estilo} -- "
                         "copie modelo-dados/estilo-cartao.css")
    arquivo_formato = projeto.caminho("formato")
    if not arquivo_formato.exists():
        raise SystemExit(f"o formato da disciplina não existe: {arquivo_formato} -- é dele que vêm o nome "
                         "da disciplina e as colunas dos cartões")
    cfg, erros = configuracao(projeto)
    if erros:
        # o nome da disciplina e o baralho de cima de todos os cartoes, e as colunas sao as de todas as planilhas: com
        # erro no formato ou nas colunas, nenhum baralho e gerado
        for e in erros:
            print(f"ERRO: {e}")
        print("Nenhum baralho gerado: resolva cada ERRO e rode de novo.")
        return 1
    # o nome no Anki e o do arquivo do pacote: o de todas as planilhas, mesmo as que o filtro deixa de fora
    mesmo_nome = {c for _, cs in repetidos((nome_a_partir_do_arquivo(c, prefixo), c) for c in planilhas(projeto))
                  for c in cs}
    sem_baralho = 0
    for caminho in csvs:
        if caminho in mesmo_nome:
            erros = [f"{caminho.name}: o nome dela no Anki, {nome_a_partir_do_arquivo(caminho, prefixo)!r}, é também "
                     "o de outra planilha"]
            decks, imagens = {}, set()
        else:
            decks, imagens, erros = notas_da_planilha(caminho, cfg, projeto)
        if erros:
            for e in erros:
                print(f"ERRO: {e}")
            print(f"  {caminho.name}: baralho não gerado")
            sem_baralho += 1
            continue
        grava_pacote(caminho, decks, imagens, cfg, projeto)
    print(f"{len(csvs)} planilha(s): {len(csvs) - sem_baralho} baralho(s) gerado(s), {sem_baralho} sem baralho")
    return 1 if sem_baralho else 0


if __name__ == "__main__":
    sys.exit(main())
