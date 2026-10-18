# SPDX-License-Identifier: GPL-3.0-or-later
# Copyright do codigo sob GPL-3.0 -- ver LICENSE e NOTICE.md na raiz do projeto.

"""Testes do confere_indice.py com projetos inventados, montados aqui. Cada caso e um
projeto novo: o projeto.json do modelo, com o indice num lugar e com um nome inventados, e
documentos inventados. Uso:
    python3 -I teste_confere_indice.py <pasta do modelo> <pasta de trabalho nova>
A pasta do modelo e a que tem scripts/ e modelo-dados/.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from projeto_inventado import Bancada  # noqa: E402

B = Bancada(sys.argv[1], sys.argv[2])
INDICE = "guia de leitura/ordem.md"  # o indice, numa subpasta, com espaco e outro nome
SCRIPT = "confere_indice.py"


def projeto(nome, arquivos, indice, **opcoes):
    """O projeto com o indice (None: sem indice)."""
    if indice is not None:
        arquivos = {**arquivos, INDICE: indice}
    return B.projeto(nome, arquivos, {"indice": INDICE}, **opcoes)


def roda(raiz, pasta=None):
    return B.roda(SCRIPT, raiz, pasta=pasta)


DOCS = {"alfa.md": "# Alfa\n", "pasta beta/gama.md": "# Gama\n", "delta/epsilon.md": "# Epsilon\n",
        "notas.txt": "não é documento\n"}
CERTO = ("# Ordem\n\n1. [Alfa](../alfa.md) — o primeiro.\n"
         "2. [Gama](<../pasta beta/gama.md>) — o segundo.\n"
         "3. [Epsilon](../delta/epsilon.md#uma-secao) — o terceiro.\n\n"
         "[site](https://example.org/x.md) [notas](../notas.txt) [topo](#ordem)\n")
SEM_EPSILON = CERTO.replace("3. [Epsilon](../delta/epsilon.md#uma-secao) — o terceiro.\n", "")

# tudo certo, rodando de uma subpasta do projeto
raiz = projeto("certo", DOCS, CERTO)
B.confere("certo", roda(raiz, "delta"), (0, ["3 documentos, cada um uma vez no índice."]))
B.confere("deterministico", roda(raiz), roda(raiz))

# documento faltando
raiz = projeto("falta", DOCS, SEM_EPSILON)
B.confere("falta", roda(raiz), (1, ["FALTA: delta/epsilon.md não está no índice",
                                    "1 problema(s) no índice, entre 3 documentos."]))

# documento repetido, com o caminho escrito de outro jeito (raiz do projeto, %20)
raiz = projeto("repetido", DOCS, CERTO + "\n[de novo](/pasta%20beta/gama.md)\n")
B.confere("repetido", roda(raiz), (1, ["ERRO: pasta beta/gama.md está 2 vezes no índice",
                                       "1 problema(s) no índice, entre 3 documentos."]))

# link quebrado e link ao proprio indice
raiz = projeto("quebrado", DOCS, CERTO + "\n[sumiu](../nao-existe.md) [eu](ordem.md)\n")
B.confere("quebrado", roda(raiz), (1, [
    "ERRO: o índice aponta para guia de leitura/ordem.md, que é o próprio índice",
    "ERRO: o índice aponta para nao-existe.md, que não existe",
    "2 problema(s) no índice, entre 3 documentos."]))

# documento que a lista do que nao vai ao GitHub deixa de fora: nao precisa estar no indice
# e, se estiver, e erro
ignorado = {**DOCS, ".gitignore": "rascunhos/\n", "rascunhos/zeta.md": "# Zeta\n"}
fora_do_git = [c for c in ignorado if not c.startswith("rascunhos/")] + [INDICE]
raiz = projeto("ignorado", ignorado, CERTO, versionados=fora_do_git)
B.confere("ignorado fora", roda(raiz), (0, ["3 documentos, cada um uma vez no índice."]))
raiz = projeto("ignorado-no-indice", ignorado, CERTO + "\n[zeta](../rascunhos/zeta.md)\n", versionados=fora_do_git)
B.confere("ignorado no indice", roda(raiz), (1, [
    "ERRO: o índice aponta para rascunhos/zeta.md, que não vai com o projeto (a lista do que não vai ao GitHub "
    "o deixa de fora)",
    "1 problema(s) no índice, entre 3 documentos."]))

# documento novo, ainda fora do git, conta; versionado e apagado da pasta, nao
raiz = projeto("novo", {**DOCS, "teta.md": "# Teta\n"}, CERTO, versionados=list(DOCS) + [INDICE])
B.confere("novo", roda(raiz), (1, ["FALTA: teta.md não está no índice",
                                   "1 problema(s) no índice, entre 4 documentos."]))
raiz = projeto("apagado", {**DOCS, "teta.md": "# Teta\n"}, CERTO)
(raiz / "teta.md").unlink()
B.confere("apagado", roda(raiz), (0, ["3 documentos, cada um uma vez no índice."]))

# link dentro de bloco de codigo ou de codigo na linha nao conta
codigo = (SEM_EPSILON + "\n```\n[Epsilon](../delta/epsilon.md)\n```\n~~~~\n[Epsilon](../delta/epsilon.md)\n```\n"
          "~~~~\nVeja `[Epsilon](../delta/epsilon.md)`.\n")
raiz = projeto("codigo", DOCS, codigo)
B.confere("codigo", roda(raiz), (1, ["FALTA: delta/epsilon.md não está no índice",
                                     "1 problema(s) no índice, entre 3 documentos."]))

# sem indice, sem git e sem projeto.json
raiz = projeto("sem-indice", DOCS, None)
B.confere("sem indice", roda(raiz)[0], 1)
B.confere("sem indice, mensagem", roda(raiz)[1][0].startswith("ERRO: o índice "), True)
raiz = projeto("sem-git", DOCS, CERTO, usa_git=False)
B.confere("sem git", roda(raiz)[0], 1)
B.confere("sem git, mensagem", roda(raiz)[1][0].startswith("ERRO: o projeto não usa o git"), True)
B.confere("sem projeto", roda(B.pasta_vazia("sem-projeto")),
          (0, ["Nenhum projeto.json aqui nem nas pastas acima: não há índice a conferir."]))

sys.exit(B.fim())
