# SPDX-License-Identifier: GPL-3.0-or-later
# Copyright do codigo sob GPL-3.0 -- ver LICENSE e NOTICE.md na raiz do projeto.

"""Bancada dos testes dos scripts que leem os documentos de um projeto: monta projetos
inventados (o projeto.json do modelo, com caminhos trocados, e arquivos inventados), roda
um script do modelo dentro deles e junta as falhas. Nao e para rodar sozinho.
"""
import json
import os
import subprocess
import sys
from pathlib import Path


class Bancada:
    def __init__(self, modelo, trabalho):
        self.modelo, self.trabalho = Path(modelo).resolve(), Path(trabalho).resolve()
        self.trabalho.mkdir(parents=True, exist_ok=True)
        # o git nao procura repositorio acima da pasta de trabalho
        self.ambiente = {**os.environ, "GIT_CEILING_DIRECTORIES": str(self.trabalho)}
        self.falhas = []

    def dados_do_modelo(self):
        return json.loads((self.modelo / "modelo-dados" / "projeto.json").read_text(encoding="utf-8"))

    def confere(self, nome, obtido, esperado):
        if obtido != esperado:
            self.falhas.append(nome)
            print(f"FALHOU {nome}:\n  obtido:   {obtido!r}\n  esperado: {esperado!r}")

    def git(self, pasta, *args):
        subprocess.run(["git", "-C", str(pasta), *args], check=True, capture_output=True, env=self.ambiente)

    def projeto(self, nome, arquivos, caminhos=None, usa_git=True, versionados=None):
        """Monta o projeto: {caminho: texto}, com os caminhos do projeto.json trocados pelos
        dados. Com git, os versionados (padrao: todos) vao pro git com add; os outros ficam so
        na pasta."""
        raiz = self.trabalho / nome
        raiz.mkdir(parents=True)
        dados = self.dados_do_modelo()
        dados["caminhos"].update(caminhos or {})
        (raiz / "projeto.json").write_text(json.dumps(dados, ensure_ascii=False), encoding="utf-8")
        for caminho, texto in arquivos.items():
            (raiz / caminho).parent.mkdir(parents=True, exist_ok=True)
            (raiz / caminho).write_text(texto, encoding="utf-8")
        if usa_git:
            self.git(raiz, "init", "-q")
            for caminho in (arquivos if versionados is None else versionados):
                self.git(raiz, "add", "--", caminho)
        return raiz

    def pasta_vazia(self, nome):
        pasta = self.trabalho / nome
        pasta.mkdir()
        return pasta

    def roda(self, script, raiz, *args, pasta=None):
        """(codigo de saida, [linhas da tela]) do script do modelo, rodado na pasta."""
        r = subprocess.run([sys.executable, "-I", str(self.modelo / "scripts" / script), *args],
                           cwd=raiz / (pasta or ""), capture_output=True, text=True, env=self.ambiente)
        return r.returncode, r.stdout.splitlines()

    def fim(self):
        print(f"{len(self.falhas)} falha(s).")
        return 1 if self.falhas else 0
