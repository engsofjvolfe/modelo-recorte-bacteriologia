# SPDX-License-Identifier: GPL-3.0-or-later
# Copyright do codigo sob GPL-3.0 -- ver LICENSE e NOTICE.md na raiz do projeto.

"""Testes do trechos_de_ia.py com projetos inventados, montados aqui. Cada caso e um projeto
novo: o projeto.json do modelo, com marcas de IA inventadas, o material gerado e a lista em
lugares e com nomes inventados, e textos inventados. Uso:
    python3 -I teste_trechos_de_ia.py <pasta do modelo> <pasta de trabalho nova>
A pasta do modelo e a que tem scripts/ e modelo-dados/.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from projeto_inventado import Bancada  # noqa: E402

B = Bancada(sys.argv[1], sys.argv[2])
sys.path.insert(0, str(B.modelo / "scripts"))
import trechos_de_ia  # noqa: E402  -- o titulo e a abertura que o script escreve

MATERIAL, LISTA = "gerado", "gerado/lista/marcados.md"  # o material e a lista, em outros lugares
IA = {"abre": "<<ia ", "fecha": ">>", "fonte": "(ia)"}  # marcas inventadas, que nao sao as de nenhum projeto
SCRIPT = "trechos_de_ia.py"
DADOS = B.dados_do_modelo()
RODAPE = ["---", "", f"*Este documento está licenciado sob [{DADOS['nome_licenca_conteudo']}]"
                     f"(../../{DADOS['caminhos']['licenca_conteudo']}).*"]


def marca(texto):
    return f"{IA['abre']}{texto}{IA['fecha']}"


def esperado(*itens):
    linhas = [trechos_de_ia.TITULO_LISTA, "", trechos_de_ia.ABERTURA, ""] + list(itens)
    return "\n".join(linhas + ([""] if itens else []) + RODAPE) + "\n"


def projeto(nome, arquivos, ia=IA):
    return B.projeto(nome, arquivos, {"material_gerado": MATERIAL, "trechos_de_ia": LISTA}, usa_git=False,
                     valores={"ia": ia})


def roda(raiz, *args):
    return B.roda(SCRIPT, raiz, *args)


def gravado(raiz):
    arquivo = raiz / LISTA
    return arquivo.read_text(encoding="utf-8") if arquivo.is_file() else None


UM = (f"# Texto Um\n\nUma frase {marca('dada pela IA')} no meio.\n\nOutra linha.\n"
      f"Duas na mesma linha: {marca('primeira')} e {marca('segunda')}.\n")
TEXTOS = {
    "gerado/um.md": UM,
    "gerado/pasta x/dois.md": f"Sem título, com {marca('um aposto')}.\n",
    "gerado/codigo.md": f"# Código\n\n```\n{marca('falsa um')}\n```\n\nVeja `{marca('falsa dois')}`.\n",
    "fora/tres.md": f"# Fora\n\n{marca('fora do material')}\n",
}
CERTO = esperado(
    "1. gerado/pasta x/dois.md, [linha 1](<../pasta x/dois.md#L1>): um aposto",
    "2. Texto Um, [linha 3](../um.md#L3): dada pela IA",
    "3. Texto Um, [linha 6](../um.md#L6): primeira",
    "4. Texto Um, [linha 6](../um.md#L6): segunda",
)

# tudo certo: ordem dos arquivos e das linhas, duas marcas na mesma linha, documento sem titulo,
# caminho com espaco, marca dentro de codigo e fora do material
raiz = projeto("certo", TEXTOS)
B.confere("certo, tela", roda(raiz), (0, [f"4 trecho(s) de IA gravado(s) em {raiz / LISTA}."]))
B.confere("certo, arquivo", gravado(raiz), CERTO)
B.confere("certo, conferir", roda(raiz, "--conferir"), (0, ["A lista dos trechos de IA está em dia: 4 trecho(s)."]))
primeiro = gravado(raiz)
roda(raiz)
B.confere("deterministico", gravado(raiz), primeiro)

# a marca sai do texto: --conferir aponta, sem gravar; a rodada seguinte tira o item e renumera
(raiz / "gerado/um.md").write_text(UM.replace(marca("dada pela IA"), "dada pela fonte"), encoding="utf-8")
codigo, tela = roda(raiz, "--conferir")
B.confere("desatualizado", (codigo, tela[0].startswith("FALTA: a lista ")), (1, True))
B.confere("desatualizado, sem gravar", gravado(raiz), CERTO)
roda(raiz)
B.confere("a marca sai", gravado(raiz), esperado(
    "1. gerado/pasta x/dois.md, [linha 1](<../pasta x/dois.md#L1>): um aposto",
    "2. Texto Um, [linha 6](../um.md#L6): primeira",
    "3. Texto Um, [linha 6](../um.md#L6): segunda",
))

# sem lista gravada, --conferir aponta
raiz = projeto("sem-arquivo", TEXTOS)
B.confere("sem arquivo", roda(raiz, "--conferir")[0], 1)

# marca que nao fecha, marca vazia e texto fora do UTF-8: nada e gravado
raiz = projeto("quebrado", {**TEXTOS, "gerado/ruim.md": f"# Ruim\n\nAbre {IA['abre']}e não fecha.\n\n{marca(' ')}\n"})
(raiz / "gerado/latino.md").write_bytes("# Ção\n".encode("latin-1"))
B.confere("quebrado", roda(raiz), (1, [
    "ERRO: gerado/latino.md: o texto não está em UTF-8; grave o arquivo de novo em UTF-8",
    "ERRO: marca de IA que abre e não fecha na mesma linha em gerado/ruim.md:3",
    "ERRO: marca de IA vazia em gerado/ruim.md:5",
    "A lista dos trechos de IA não foi gravada."]))
B.confere("quebrado, sem gravar", gravado(raiz), None)

# sem nenhuma marca: a lista so com o titulo, a abertura e o rodape
raiz = projeto("vazio", {"gerado/um.md": "# Um\n\nNada marcado.\n"})
B.confere("vazio, tela", roda(raiz), (0, [f"0 trecho(s) de IA gravado(s) em {raiz / LISTA}."]))
B.confere("vazio, arquivo", gravado(raiz), esperado())

# sem marcas de IA no projeto.json: nada a montar
raiz = projeto("sem-ia", TEXTOS, ia=None)
B.confere("sem ia", roda(raiz), (0, ['O projeto.json não marca trechos de IA ("ia"): não há lista a montar.']))
B.confere("sem ia, sem gravar", gravado(raiz), None)

sys.exit(B.fim())
