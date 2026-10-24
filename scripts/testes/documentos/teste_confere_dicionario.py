# SPDX-License-Identifier: GPL-3.0-or-later
# Copyright do codigo sob GPL-3.0 -- ver LICENSE e NOTICE.md na raiz do projeto.

"""Testes do confere_dicionario.py com projetos inventados, montados pela bancada
(projeto_inventado.py): o projeto.json do modelo, com o dicionario num lugar e com um nome
inventados, e dicionarios inventados, com aulas, slides, posicoes e hashes que nao sao os de
nenhuma analise. Os codigos se montam pelo analises.py, como os ids dos trechos, e os
errados, com o separador e o numero de digitos do hash dele. Os testes conferem o que o
script faz, nunca uma frase pronta:
  - cada titulo na regra passa, e cada titulo fora dela da uma linha ERRO para cada problema,
    com a linha dele: sem crases, entre aspas, com virgula, com dois espacos ou um no fim,
    vazio, com texto solto, com crase dentro, com codigo vazio; o codigo de tres partes, com
    zero na frente, com zero, com o slide que nao e numero, com o hash curto ou em
    maiusculas, sem a aula; o codigo que cobre outro, antes ou depois dele, ou que se repete;
    e os codigos fora da ordem natural das aulas, dos slides e das posicoes;
  - o titulo dentro de um bloco de codigo e o de outro nivel nao contam;
  - sem erro, sai com 0 e diz quantos titulos conferiu; com erro, sai com 1, e cada linha da
    tela e um ERRO;
  - o projeto.json sem o caminho do dicionario, o dicionario que falta e o que nao esta em
    UTF-8 dao ERRO;
  - roda de uma subpasta do projeto, e duas rodadas dao o mesmo.
Uso:
    python3 -I teste_confere_dicionario.py <pasta scripts/> <pasta de trabalho nova>
A pasta modelo-dados/ fica ao lado da pasta scripts/, como no projeto.
"""
import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from projeto_inventado import Bancada  # noqa: E402

B = Bancada(Path(sys.argv[1]).resolve().parent, sys.argv[2], scripts=sys.argv[1])
sys.path.insert(0, str(B.scripts))
import analises  # noqa: E402  -- como o id de um trecho se monta, o separador e o numero de digitos do hash

SCRIPT = "confere_dicionario.py"
CHAVE = "dicionario_das_duvidas"  # o caminho do dicionario, nos caminhos do projeto.json
PASTA, DICIONARIO = "notas", "notas/perguntas-abertas.md"  # o dicionario, num lugar e com um nome inventados
LINHA_DO_ERRO = re.compile(rf"^ERRO: {re.escape(DICIONARIO)}:(\d+): ")  # o arquivo e a linha que o ERRO aponta
S, D = analises.SEPARADOR_DO_ID, analises.DIGITOS_DO_HASH


def trecho(aula, slide, posicao, texto="um trecho inventado"):
    """O codigo de um trecho inventado, montado como o analises.py monta o de um trecho das analises."""
    return analises.id_do_trecho(aula, slide, posicao, texto)


def do_slide(aula, slide):
    return S.join([aula, str(slide)])


def titulo(*codigos):
    return "## " + " ".join(f"`{c}`" for c in codigos)


CERTOS = [
    titulo("4"), titulo(do_slide("4", 7)), titulo(trecho("4", 7, 2)),
    titulo("4", do_slide("6-7", 2), trecho("12", 1, 3)), titulo(do_slide("4", 7), do_slide("4", 30)),
    titulo(trecho("4", 7, 2), trecho("4", 7, 11)), titulo(do_slide("4", 7), trecho("4", 8, 1, "outro trecho")),
]
ERRADOS = [  # (titulo, quantos problemas ele tem)
    ("## 4", 1), ("## '4'", 1), ("## `4`,`5`", 1), ("## `4`  `5`", 1), ("## `4` ", 1), ("## ", 1),
    ("## `4` solto", 1), ("## `4`5`", 1), ("## ``", 1),
    (titulo(S.join(["4", "7", "2"])), 1), (titulo(do_slide("4", "07")), 1), (titulo(do_slide("4", 0)), 1),
    (titulo(do_slide("4", "x")), 1), (titulo(S.join(["4", "7", "2", "7" * (D - 1)])), 1),
    (titulo(S.join(["4", "7", "2", "A" * D])), 1), (titulo(do_slide("", 7)), 1),
    (titulo("4", do_slide("4", 7)), 1), (titulo(do_slide("4", 7), trecho("4", 7, 2)), 1), (titulo("4", "4"), 1),
    (titulo(trecho("4", 7, 2), do_slide("4", 7)), 2),
    (titulo("12", "4"), 1), (titulo(do_slide("4", 30), do_slide("4", 7)), 1),
    (titulo(trecho("4", 7, 11), trecho("4", 7, 2)), 1),
]


def dicionario(titulos):
    """(texto, [linha de cada titulo]) de um dicionario com uma duvida inventada sob cada titulo, depois de um titulo
    de primeiro nivel, de um titulo dentro de um bloco de codigo e de um de terceiro nivel, que nao contam."""
    linhas, numeros = ["# Dicionário inventado", "", "```", "## isto não é um título", "```", "",
                       "### `4` de outro nível", ""], []
    for t in titulos:
        numeros.append(len(linhas) + 1)
        linhas += [t, "", "uma dúvida inventada.", "", "Aberta.", ""]
    return "\n".join(linhas), numeros


def projeto(nome, texto=None):
    return B.projeto(nome, {} if texto is None else {DICIONARIO: texto}, {CHAVE: DICIONARIO}, usa_git=False)


def roda(raiz, pasta=None):
    return B.roda(SCRIPT, raiz, pasta=pasta)


def erros_por_linha(saida):
    """{linha do dicionario: quantas linhas ERRO a apontam}."""
    contagem = {}
    for m in filter(None, map(LINHA_DO_ERRO.match, saida)):
        contagem[int(m.group(1))] = contagem.get(int(m.group(1)), 0) + 1
    return contagem


# um dicionario com titulos na regra e fora dela: cada um fora da regra, e so ele, com uma linha ERRO por problema
texto, numeros = dicionario(CERTOS + [t for t, _ in ERRADOS])
raiz = projeto("misturado", texto)
codigo, saida = roda(raiz)
B.confere("misturado, sai com 1", codigo, 1)
B.confere("misturado, cada título fora da regra dá um ERRO por problema, com a linha dele, e só ele",
          erros_por_linha(saida), {n: problemas for n, (_, problemas) in zip(numeros[len(CERTOS):], ERRADOS)})
B.confere("misturado, cada linha da tela é um ERRO com a linha", all(map(LINHA_DO_ERRO.match, saida)), True)

# so titulos na regra: sai com 0, diz quantos conferiu, roda de uma subpasta e da sempre o mesmo
texto, _ = dicionario(CERTOS)
raiz = projeto("certo", texto)
codigo, saida = roda(raiz)
B.confere("certo, sai com 0 e sem ERRO", (codigo, [l for l in saida if l.startswith("ERRO")]), (0, []))
B.confere("certo, diz quantos títulos conferiu", any(str(len(CERTOS)) in l for l in saida), True)
B.confere("certo, de uma subpasta do projeto", roda(raiz, pasta=PASTA), (codigo, saida))
B.confere("duas rodadas dão o mesmo", roda(raiz), (codigo, saida))

# o projeto.json sem o caminho, o dicionario que falta e o que nao esta em UTF-8
sem_caminho = projeto("sem-caminho", dicionario(CERTOS)[0])
dados = json.loads((sem_caminho / "projeto.json").read_text(encoding="utf-8"))
del dados["caminhos"][CHAVE]
(sem_caminho / "projeto.json").write_text(json.dumps(dados, ensure_ascii=False), encoding="utf-8")
latino = projeto("latino", "")
(latino / DICIONARIO).write_bytes(f"{titulo('4')}\n\nção\n".encode("latin-1"))
for caso, raiz in (("sem o caminho no projeto.json", sem_caminho), ("sem o dicionário", projeto("sem-dicionario")),
                   ("fora do UTF-8", latino)):
    codigo, saida = roda(raiz)
    B.confere(f"{caso}, sai com 1 e um ERRO", (codigo, any(l.startswith("ERRO") for l in saida)), (1, True))

sys.exit(B.fim())
