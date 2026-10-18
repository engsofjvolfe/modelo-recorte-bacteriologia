# SPDX-License-Identifier: GPL-3.0-or-later
# Copyright do codigo sob GPL-3.0 -- ver LICENSE e NOTICE.md na raiz do projeto.

"""Testes do estraga.py, com uma peca inventada aqui (uma funcao que soma), testes
inventados dela e listas de estragos inventadas. Conferem regras, nunca uma frase pronta:
o estrago que quebra o que o teste confere e pego, o que nao quebra nao e, e o que nao se
aplica e erro; a contagem do fim e a das linhas; o codigo de saida diz se todos foram
pegos; a peca original nao muda; os argumentos de --antes chegam ao teste, e a pasta de
--irma fica ao lado da copia, sem a pasta testes/; lista com campo desconhecido ou que
falta e erro, sem rodar nada; duas rodadas dao a mesma saida. Uso:
    python3 -I teste_estraga.py <pasta do estraga.py> <pasta de trabalho nova>
Precisa do extrator_comum.py, do extrator, na pasta irma "extrator" ou na mesma pasta.
"""
import json
import random
import re
import string
import subprocess
import sys
from pathlib import Path

PECA, TRABALHO = Path(sys.argv[1]).resolve(), Path(sys.argv[2]).resolve()
FALHAS = []
SORTEIO = random.Random(1)


def confere(condicao, descricao):
    if not condicao:
        FALHAS.append(descricao)
    return condicao


def nome():
    return "".join(SORTEIO.choice(string.ascii_lowercase) for _ in range(8))


# a peca inventada e os testes dela, escritos fora dela
PECA_INVENTADA = TRABALHO / "peca"
(PECA_INVENTADA / "testes").mkdir(parents=True)
COMENTARIO = nome()
(PECA_INVENTADA / "calculo.py").write_text(f"def soma(a, b):\n    return a + b  # {COMENTARIO}\n", encoding="utf-8")
(PECA_INVENTADA / "testes" / "nada.txt").write_text("", encoding="utf-8")
ARGUMENTO, IRMA, MARCA = nome(), nome(), nome()
CABECA = """import random, sys
from pathlib import Path
peca, *extra, trabalho = sys.argv[1:]
sys.path.insert(0, peca)
import calculo
r = random.Random(2)
ok = all(calculo.soma(a, b) == a + b for a, b in ((r.randint(-99, 99), r.randint(-99, 99)) for _ in range(50)))
"""
TESTES = {
    "soma": CABECA + "sys.exit(0 if ok else 1)\n",
    "argumento": CABECA + f"sys.exit(0 if ok and extra == [{ARGUMENTO!r}] else 1)\n",
    "irma": CABECA + f"irma = Path(peca).parent / {IRMA!r}\n"
                     f"sys.exit(0 if ok and (irma / {MARCA!r}).is_file() and not (irma / 'testes').exists() else 1)\n",
}
for t, codigo in TESTES.items():
    (TRABALHO / f"teste_{t}.py").write_text(codigo, encoding="utf-8")
(TRABALHO / IRMA / "testes").mkdir(parents=True)
(TRABALHO / IRMA / MARCA).write_text("", encoding="utf-8")

QUEBRA = {"nome": "quebra", "arquivo": "calculo.py", "de": "a + b", "para": "a - b"}
INOFENSIVO = {"nome": "inofensivo", "arquivo": "calculo.py", "de": COMENTARIO, "para": nome()}
AUSENTE = {"nome": "ausente", "arquivo": "calculo.py", "de": nome(), "para": "x"}


def lista(nome_, estragos, **extra):
    caminho = TRABALHO / f"{nome_}.json"
    caminho.write_text(json.dumps(dict({"versao_schema": 1, "estragos": estragos}, **extra)), encoding="utf-8")
    return caminho


def roda(nome_, estragos, teste="soma", *opcoes, **extra):
    trabalho = TRABALHO / f"t-{nome_}"
    r = subprocess.run([sys.executable, "-I", str(PECA / "estraga.py"), str(PECA_INVENTADA),
                        str(TRABALHO / f"teste_{teste}.py"), str(lista(nome_, estragos, **extra)), str(trabalho),
                        *opcoes], capture_output=True, text=True)
    return r.returncode, r.stdout + r.stderr, trabalho


def veredito(saida, nome_):
    """O que a linha do estrago diz: a palavra logo depois do nome."""
    m = re.search(rf"^{nome_}: (\S+)", saida, re.M)
    return m.group(1) if m else None


antes = {p: p.read_bytes() for p in PECA_INVENTADA.rglob("*") if p.is_file()}
cod, out, _ = roda("tres", [QUEBRA, INOFENSIVO, AUSENTE])
contagem = re.search(r"(\d+) de (\d+)", out.strip().split("\n")[-1])
confere(veredito(out, "quebra") == "pego", f"o estrago que quebra o que o teste confere é pego: {out}")
confere(veredito(out, "inofensivo") not in (None, "pego", "ERRO:"), f"o estrago que não quebra nada não é pego: {out}")
confere(veredito(out, "ausente") == "ERRO:", f"o estrago cujo texto não está no arquivo é erro: {out}")
confere(cod == 1 and contagem and contagem.groups() == ("1", "3"),
        f"um de três pego, e o código diz que nem todos: {out}")
confere({p: p.read_bytes() for p in PECA_INVENTADA.rglob("*") if p.is_file()} == antes, "a peça original não muda")
cod2, out2, _ = roda("tres-de-novo", [QUEBRA, INOFENSIVO, AUSENTE])
confere(out2 == out, "duas rodadas dão a mesma saída")
cod, out, _ = roda("so-pegos", [QUEBRA])
confere(cod == 0, f"com todos pegos, o código é 0: {out}")

cod, out, _ = roda("argumento", [dict(INOFENSIVO)], "argumento", "--antes", ARGUMENTO)
confere(veredito(out, "inofensivo") != "pego", f"o argumento de --antes chega ao teste: {out}")
cod, out, _ = roda("sem-argumento", [dict(INOFENSIVO)], "argumento")
confere(veredito(out, "inofensivo") == "pego", f"sem --antes, o teste que pede o argumento falha: {out}")
cod, out, _ = roda("irma", [dict(INOFENSIVO)], "irma", "--irma", str(TRABALHO / IRMA))
confere(veredito(out, "inofensivo") != "pego", f"a pasta de --irma fica ao lado da cópia, sem testes/: {out}")
cod, out, _ = roda("sem-irma", [dict(INOFENSIVO)], "irma")
confere(veredito(out, "inofensivo") == "pego", f"sem --irma, o teste que pede a pasta irmã falha: {out}")

for descricao, estragos, extra in (("campo desconhecido no estrago", [dict(QUEBRA, outro="x")], {}),
                                   ("campo desconhecido na lista", [QUEBRA], {"outra": 1}),
                                   ("campo que falta no estrago", [{k: v for k, v in QUEBRA.items() if k != "para"}],
                                    {})):
    cod, out, trabalho = roda(nome(), estragos, **extra)
    confere(cod == 1 and out.startswith("ERRO") and not trabalho.exists(), f"{descricao} é erro, sem rodar nada: {out}")

for f in FALHAS:
    print("FALHA:", f)
print(f"{len(FALHAS)} falha(s)")
sys.exit(1 if FALHAS else 0)
