# SPDX-License-Identifier: GPL-3.0-or-later
# Copyright do codigo sob GPL-3.0 -- ver LICENSE e NOTICE.md na raiz do projeto.

"""Testes do glossario.py com projetos inventados, montados aqui. Cada caso e um projeto
novo: o projeto.json do modelo, com o glossario num lugar e com um nome inventados, e
documentos inventados. Uso:
    python3 -I teste_glossario.py <pasta do modelo> <pasta de trabalho nova>
A pasta do modelo e a que tem scripts/ e modelo-dados/.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from projeto_inventado import Bancada  # noqa: E402

B = Bancada(sys.argv[1], sys.argv[2])
sys.path.insert(0, str(B.modelo / "scripts"))
import glossario  # noqa: E402  -- o titulo e a abertura que o script escreve

GLOSSARIO = "referencia/termos.md"  # o glossario, numa subpasta, com outro nome
SCRIPT = "glossario.py"
DADOS = B.dados_do_modelo()
RODAPE = ["---", "", f"*Este documento está licenciado sob [{DADOS['nome_licenca_conteudo']}]"
                     f"(../{DADOS['caminhos']['licenca_conteudo']}).*"]


def esperado(*entradas):
    linhas = [glossario.TITULO_GLOSSARIO, "", glossario.ABERTURA, ""] + list(entradas)
    return "\n".join(linhas + ([""] if entradas else []) + RODAPE) + "\n"


def projeto(nome, arquivos, **opcoes):
    return B.projeto(nome, arquivos, {"glossario": GLOSSARIO}, **opcoes)


def roda(raiz, *args):
    return B.roda(SCRIPT, raiz, *args)


def gravado(raiz):
    arquivo = raiz / GLOSSARIO
    return arquivo.read_text(encoding="utf-8") if arquivo.is_file() else None


DOCS = {
    "um.md": ("# Documento Um\n\nUm animal listrado, a <dfn>zebra</dfn>.\n\n## Seção Ação\n\n"
              "O <dfn>**Ábaco**</dfn> conta.\n"),
    "pasta x/dois.md": ("# Dois\n\n## Parte\n\nnada\n\n## Parte\n\nUma <dfn>casa\ncomprida</dfn> aqui, e um\n"
                        "<DFN id=\"b\">*bule*</DFN> ali.\n"),
    "sem-titulo.md": "Texto sem título com a <dfn>Duna</dfn>.\n",
    "codigo.md": ("# Código\n\n```\n<dfn>falso um</dfn>\n```\n\nVeja `<dfn>falso dois</dfn>`.\n\n"
                  "~~~\n<dfn>falso três</dfn>\n~~~\n"),
}
CERTO = esperado(
    "- **Ábaco** — [Documento Um › Seção Ação](../um.md#seção-ação)",
    "- **bule** — [Dois › Parte](<../pasta x/dois.md#parte-1>)",
    "- **casa comprida** — [Dois › Parte](<../pasta x/dois.md#parte-1>)",
    "- **Duna** — [sem-titulo.md](../sem-titulo.md)",
    "- **zebra** — [Documento Um](../um.md)",
)

# tudo certo: ordem sem acento nem maiuscula, secao, titulo repetido, marca partida em duas
# linhas, marca com atributo e em maiusculas, documento sem titulo, codigo de fora
raiz = projeto("certo", DOCS)
B.confere("certo, tela", roda(raiz), (0, [f"5 termo(s) gravado(s) em {raiz / GLOSSARIO}."]))
B.confere("certo, arquivo", gravado(raiz), CERTO)
B.confere("certo, conferir", roda(raiz, "--conferir"), (0, ["O glossário está em dia: 5 termo(s)."]))
primeiro = gravado(raiz)
roda(raiz)
B.confere("deterministico", gravado(raiz), primeiro)

# o glossario muda quando um documento muda: --conferir aponta, sem gravar
(raiz / "um.md").write_text(DOCS["um.md"] + "\nE a <dfn>girafa</dfn>.\n", encoding="utf-8")
codigo, tela = roda(raiz, "--conferir")
B.confere("desatualizado", (codigo, tela[0].startswith("FALTA: o glossário ")), (1, True))
B.confere("desatualizado, sem gravar", gravado(raiz), CERTO)

# sem glossario gravado, --conferir aponta
raiz = projeto("sem-arquivo", DOCS)
B.confere("sem arquivo", roda(raiz, "--conferir")[0], 1)

# termo definido em dois lugares e marca vazia: nada e gravado
raiz = projeto("repetido", {**DOCS, "tres.md": "# Três\n\nOutra <dfn>Zebra</dfn>.\n\nE <dfn> </dfn>.\n"})
B.confere("repetido", roda(raiz), (1, [
    "ERRO: marca <dfn> vazia em tres.md:5",
    "ERRO: o termo \"Zebra\" é definido em mais de um lugar: tres.md:3, um.md:3",
    "O glossário não foi gravado."]))
B.confere("repetido, sem gravar", gravado(raiz), None)

# a marca no proprio glossario e num arquivo que o .gitignore deixa de fora nao conta
docs = {**DOCS, GLOSSARIO: "# Velho\n\n<dfn>antigo</dfn>\n", ".gitignore": "rascunho.md\n",
        "rascunho.md": "<dfn>rascunhado</dfn>\n"}
raiz = projeto("fora", docs, versionados=[c for c in docs if c != "rascunho.md"])
roda(raiz)
B.confere("fora", gravado(raiz), CERTO)

# sem nenhuma marca: o glossario so com o titulo, a abertura e o rodape
raiz = projeto("vazio", {"um.md": "# Um\n\nNada definido.\n"})
B.confere("vazio, tela", roda(raiz), (0, [f"0 termo(s) gravado(s) em {raiz / GLOSSARIO}."]))
B.confere("vazio, arquivo", gravado(raiz), esperado())

# sem git e sem projeto.json
raiz = projeto("sem-git", DOCS, usa_git=False)
codigo, tela = roda(raiz)
B.confere("sem git", (codigo, tela[0].startswith("ERRO: o projeto não usa o git")), (1, True))
B.confere("sem projeto", roda(B.pasta_vazia("sem-projeto")),
          (0, ["Nenhum projeto.json aqui nem nas pastas acima: não há glossário a montar."]))

sys.exit(B.fim())
