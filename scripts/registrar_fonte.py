# SPDX-License-Identifier: GPL-3.0-or-later
# Copyright do codigo sob GPL-3.0 -- ver LICENSE e NOTICE.md na raiz do projeto.

"""
Grava, no topo de um documento gerado, de qual arquivo ele veio: a chave da fonte, o
caminho do arquivo (relativo a raiz do projeto, a pasta do projeto.json) e a impressao
digital dele (sha256). E esse registro que liga o documento gerado a sua fonte -- nunca o
nome dos arquivos. A chave e a mesma da referencia da fonte no arquivo de fontes do
projeto. Rodar de novo atualiza a linha daquela chave; um documento que junta varias
fontes tem uma linha por fonte, e as partes dele usam a chave para dizer de onde vieram.

Formato, no topo do documento:
    ---
    fonte AULA-1: docs/material-base/AULA.pdf | sha256: <64 algarismos hexadecimais>
    ---

A fonte tem de ficar na pasta protegida (no projeto.json, "material_base"), que nunca e
publicada. Se estiver fora, o script mostra de onde pra onde ela iria, pergunta e, se a
pessoa confirmar, leva a fonte pra la antes de registrar; com --mover, leva sem
perguntar (pra quando a pessoa ja autorizou). Se ela nao for, nada e registrado.

Depois de registrar, roda as referencias (referencias.py): gera de novo o arquivo de
referencias e a conferencia delas, avisa se a chave ainda nao tem referencia e lista as
referencias que faltam conferir.

Uso (de qualquer pasta dentro do projeto):
    python scripts/registrar_fonte.py DOCUMENTO.md ARQUIVO_DE_ORIGEM CHAVE
    python scripts/registrar_fonte.py DOCUMENTO.md ARQUIVO_DE_ORIGEM CHAVE --mover
    python scripts/registrar_fonte.py DOCUMENTO.md ARQUIVO_DE_ORIGEM CHAVE --projeto projeto.json
"""

import argparse
import os
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from comum import LINHA_FONTE, acha_projeto, dentro, impressao, leva_para, separa_registro  # noqa: E402


def registra(documento, fonte, chave, raiz):
    texto = documento.read_text(encoding="utf-8") if documento.exists() else ""
    registro, resto = separa_registro(texto)
    caminho = Path(os.path.relpath(Path(fonte).resolve(), Path(raiz).resolve())).as_posix()
    nova = f"fonte {chave}: {caminho} | sha256: {impressao(fonte)}"
    mantidas = [l for l in registro if not ((m := LINHA_FONTE.match(l)) and m.group("chave") == chave)]
    resto = resto.lstrip("\n")
    documento.parent.mkdir(parents=True, exist_ok=True)
    documento.write_text("\n".join(["---"] + mantidas + [nova, "---"]) + "\n" + ("\n" + resto if resto else ""),
                         encoding="utf-8")
    return nova


def main(argv=None):
    p = argparse.ArgumentParser(description="Grava no documento gerado de qual arquivo ele veio.")
    p.add_argument("documento", type=Path, help="documento gerado (.md)")
    p.add_argument("fonte", type=Path, help="arquivo de origem")
    p.add_argument("chave", help="chave da fonte, a mesma da referencia dela no arquivo de fontes")
    p.add_argument("--mover", action="store_true",
                   help="leva a fonte pra pasta protegida sem perguntar, se ela estiver fora")
    p.add_argument("--projeto", type=Path, help="projeto.json (padrao: o primeiro achado subindo a partir daqui)")
    a = p.parse_args(argv)
    if not a.fonte.exists():
        raise SystemExit(f"fonte nao encontrada: {a.fonte}")
    if any(c.isspace() for c in a.chave):
        raise SystemExit("a chave nao pode ter espaco")
    projeto = acha_projeto(a.projeto)
    fonte = a.fonte
    if not dentro(fonte, projeto.caminho("material_base")):
        fonte = leva_para(fonte, projeto.caminho("material_base"), a.mover)
        if fonte is None:
            raise SystemExit("ERRO: a fonte precisa ficar na pasta protegida antes de ser registrada; nada foi "
                             "registrado")
    print(registra(a.documento, fonte, a.chave, projeto.raiz))

    # gancho: o registro puxa as referencias e a conferencia delas
    import referencias
    return referencias.roda(projeto, chave_nova=a.chave)


if __name__ == "__main__":
    sys.exit(main())
