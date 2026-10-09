# SPDX-License-Identifier: GPL-3.0-or-later
# Copyright do codigo sob GPL-3.0 -- ver LICENSE e NOTICE.md na raiz do projeto.

"""
Protege o material de terceiros: confere que nenhuma fonte fica onde poderia ser
publicada.

A pasta do material de base (no projeto.json, "material_base") e a pasta protegida: tem
nome e lugar fixos, e tudo o que tem texto de terceiros fica dentro dela. O script
confere, sempre:

  - se cada fonte registrada (no topo das transcricoes e das bases do material de fora)
    esta dentro da pasta protegida -- a que estiver fora aparece com ERRO, e o
    registrar_fonte.py ou o base_externa.py a levam pra dentro;
  - se o projeto usa o git, se a lista do que nao vai ao GitHub (o .gitignore) deixa de
    fora a pasta protegida.

Com --versao, chamado pelo verificador antes de cada versao gravada pelo git (o arquivo
pre-commit da pasta .githooks), confere tambem cada arquivo que vai na versao: recusa
arquivo da pasta protegida que a lista deixa de fora e arquivo, em qualquer lugar, cuja
impressao digital seja a de uma fonte -- a de cada arquivo da pasta protegida e a de cada
fonte registrada. Assim, nem uma copia de fonte com outro nome, em outra pasta, passa.

Uso (de qualquer pasta dentro do projeto):
    python scripts/protege_fontes.py
    python scripts/protege_fontes.py --versao
    python scripts/protege_fontes.py --projeto projeto.json
"""

import argparse
import hashlib
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from comum import (acha_projeto, dentro, ignorado_pelo_git, ignorados_pelo_git, impressoes_das_fontes,  # noqa: E402
                   procura_projeto, registros)


def fontes_fora(projeto):
    """Erros das fontes registradas fora da pasta protegida."""
    protegida = projeto.caminho("material_base")
    return [f"a fonte {chave} ({arquivo}), registrada em {doc.name}, está fora da pasta protegida "
            f"{protegida}: rode de novo o registrar_fonte.py (ou o base_externa.py, se ela for do material "
            f"de fora), que a leva pra dentro"
            for doc, chave, arquivo, _ in registros(projeto) if not dentro(arquivo, protegida)]


def lista_deixa_de_fora(projeto):
    """Erros se o projeto usa o git e a lista do que não vai ao GitHub não cobre a pasta
    protegida. O teste usa a pasta das transcrições, que o projeto.json põe dentro dela."""
    protegida = projeto.caminho("material_base")
    if ignorado_pelo_git(projeto.raiz, projeto.caminho("gerados")) is False:
        return [f"a lista do que não vai ao GitHub (o .gitignore) não deixa de fora a pasta protegida "
                f"{protegida}: copie o .gitignore de novo"]
    return []


def arquivos_da_versao(raiz):
    """[(caminho, conteudo)] de cada arquivo que vai na versão que o git está gravando."""
    nomes = subprocess.run(["git", "-C", str(raiz), "diff", "--cached", "--name-only", "--diff-filter=ACMR", "-z"],
                           capture_output=True, check=True).stdout.decode("utf-8").split("\0")
    return [(raiz / n, subprocess.run(["git", "-C", str(raiz), "show", f":{n}"], capture_output=True,
                                      check=True).stdout) for n in nomes if n]


def copias_na_versao(projeto):
    """Erros de arquivo da versão que é fonte ou cópia de fonte."""
    protegida, impressoes, erros = projeto.caminho("material_base"), impressoes_das_fontes(projeto), []
    versao = arquivos_da_versao(projeto.raiz)
    ignorados = ignorados_pelo_git(projeto.raiz, [a for a, _ in versao]) or set()
    for arquivo, conteudo in versao:
        h = hashlib.sha256(conteudo).hexdigest()
        if dentro(arquivo, protegida) and arquivo.resolve() in ignorados:
            erros.append(f"{arquivo} está na pasta protegida e não pode ir ao GitHub")
        elif h in impressoes:
            erros.append(f"{arquivo} é igual à fonte {impressoes[h]} e não pode ir ao GitHub")
    return erros


def main(argv=None):
    p = argparse.ArgumentParser(description="Confere que nenhuma fonte fica onde poderia ser publicada.")
    p.add_argument("--versao", action="store_true",
                   help="confere também os arquivos da versão que o git está gravando (uso do verificador)")
    p.add_argument("--projeto", type=Path, help="projeto.json (padrao: o primeiro achado subindo a partir daqui)")
    a = p.parse_args(argv)
    if a.projeto is None and procura_projeto() is None:
        # sem projeto.json (no proprio modelo, por exemplo) nao ha fonte registrada a proteger
        print("Nenhum projeto.json aqui nem nas pastas acima: não há fonte a proteger.")
        return 0
    projeto = acha_projeto(a.projeto)
    erros = fontes_fora(projeto) + lista_deixa_de_fora(projeto)
    if a.versao:
        erros += copias_na_versao(projeto)
    for e in erros:
        print("ERRO:", e)
    if a.versao and erros:
        print("A versão não foi gravada. Tire cada arquivo dela com: git rm --cached <arquivo> "
              "(ele continua no seu computador, só sai da versão)")
    if not erros:
        print("Nenhuma fonte fora da pasta protegida" + (" nem na versão." if a.versao else "."))
    return 1 if erros else 0


if __name__ == "__main__":
    sys.exit(main())
