# SPDX-License-Identifier: GPL-3.0-or-later
# Copyright do codigo sob GPL-3.0 -- ver LICENSE e NOTICE.md na raiz do projeto.

"""
Confere um arquivo de dados JSON contra o schema dele. Agnostico de materia: nao
conhece nenhum campo de nenhuma disciplina -- tudo vem do schema.

Aqui fica tambem a leitura de todo arquivo de dados que tem molde em esquemas/ (le_dados):
todo script que le um desses arquivos le por ela, e este tambem. Ela le o arquivo e o
confere contra o molde dele; o texto fora do UTF-8, o JSON invalido (com a linha e a
coluna) e o que esta fora do molde viram erro, cada um com o nome do arquivo na frente,
e os dados nao vem. Ela fica neste arquivo porque ele nao depende de nenhum outro script
nem do projeto.json: roda sozinho, e os outros o importam sem importacao circular.

O schema e achado pelo nome do arquivo de dados: "formato.json" ->
"scripts/esquemas/formato.schema.json". Da para indicar outro com --schema.

Usa so a biblioteca padrao do Python, entao entende o subconjunto do JSON Schema que
os schemas deste projeto usam: type, required, properties, additionalProperties,
items, minItems, maxItems, const, enum, not, minLength, pattern, allOf, anyOf, if/then/else e $ref
para "#/$defs/...". Alem disso, uma regra fixa: numa lista de objetos que tem o campo
"id" ou "chave", nenhum id e nenhuma chave se repete. Campos que o schema nao conhece
sao aceitos sem conferir (o formato pode crescer).

Uso (os caminhos de exemplo sao os do modelo; no projeto, valem os do projeto.json):
    python scripts/validar_dados.py dados/formato.json
    python scripts/validar_dados.py DADOS.json --schema OUTRO.schema.json
Sai com codigo 1 se houver qualquer erro.
"""

import argparse
import json
import re
import sys
from pathlib import Path

PASTA_ESQUEMAS = Path(__file__).resolve().parent / "esquemas"
TIPOS = {"object": dict, "array": list, "string": str, "boolean": bool, "null": type(None)}


def tipo_confere(valor, tipo):
    # bool e subclasse de int em Python: "true" nao pode passar por numero
    if tipo == "integer":
        return isinstance(valor, int) and not isinstance(valor, bool)
    if tipo == "number":
        return isinstance(valor, (int, float)) and not isinstance(valor, bool)
    return isinstance(valor, TIPOS[tipo])


def resolve(schema, raiz):
    """Segue "$ref" ate a definicao, so dentro do proprio schema ("#/$defs/...")."""
    while "$ref" in schema:
        ref = schema["$ref"]
        if not ref.startswith("#/"):
            raise SystemExit(f"$ref fora do proprio schema nao e suportado: {ref}")
        alvo = raiz
        for parte in ref[2:].split("/"):
            alvo = alvo[parte]
        schema = alvo
    return schema


def erros_de(valor, schema, raiz, caminho="$"):
    sub = []
    valida(valor, schema, raiz, caminho, sub)
    return sub


def valida(valor, schema, raiz, caminho, erros):
    schema = resolve(schema, raiz)
    for sub in schema.get("allOf", []):
        valida(valor, sub, raiz, caminho, erros)
    if "anyOf" in schema and all(erros_de(valor, s, raiz) for s in schema["anyOf"]):
        erros.append(f"{caminho}: nao confere com nenhuma das formas aceitas")
    if "if" in schema:
        if not erros_de(valor, schema["if"], raiz):
            if "then" in schema:
                valida(valor, schema["then"], raiz, caminho, erros)
        elif "else" in schema:
            valida(valor, schema["else"], raiz, caminho, erros)
    if "const" in schema and valor != schema["const"]:
        erros.append(f"{caminho}: deve ser {schema['const']!r}, e {valor!r}")
    if "enum" in schema and valor not in schema["enum"]:
        erros.append(f"{caminho}: deve ser um de {schema['enum']}, e {valor!r}")
    if "not" in schema and not erros_de(valor, schema["not"], raiz, caminho):
        erros.append(f"{caminho}: valor nao permitido: {valor!r}")
    tipo = schema.get("type")
    if tipo:
        tipos = tipo if isinstance(tipo, list) else [tipo]
        if not any(tipo_confere(valor, t) for t in tipos):
            erros.append(f"{caminho}: deve ser {' ou '.join(tipos)}")
            return
    if isinstance(valor, str):
        if len(valor) < schema.get("minLength", 0):
            erros.append(f"{caminho}: texto vazio ou curto demais")
        if "pattern" in schema and not re.search(schema["pattern"], valor):
            erros.append(f"{caminho}: {valor!r} fora do padrao {schema['pattern']}")
    if isinstance(valor, dict):
        for chave in schema.get("required", []):
            if chave not in valor:
                erros.append(f"{caminho}: falta o campo {chave!r}")
        propriedades = schema.get("properties", {})
        extra = schema.get("additionalProperties", True)
        for chave, sub in valor.items():
            if chave in propriedades:
                valida(sub, propriedades[chave], raiz, f"{caminho}.{chave}", erros)
            elif extra is False:
                erros.append(f"{caminho}: campo nao previsto {chave!r}")
            elif isinstance(extra, dict):
                valida(sub, extra, raiz, f"{caminho}.{chave}", erros)
    if isinstance(valor, list):
        if len(valor) < schema.get("minItems", 0):
            erros.append(f"{caminho}: lista com menos de {schema['minItems']} item(ns)")
        if "maxItems" in schema and len(valor) > schema["maxItems"]:
            erros.append(f"{caminho}: lista com mais de {schema['maxItems']} item(ns)")
        if "items" in schema:
            for i, item in enumerate(valor):
                valida(item, schema["items"], raiz, f"{caminho}[{i}]", erros)
        for campo in ("id", "chave"):
            vistos, repetidos = set(), []
            for item in valor:
                if isinstance(item, dict) and campo in item:
                    v = json.dumps(item[campo], ensure_ascii=False, sort_keys=True)
                    if v in vistos and v not in repetidos:
                        repetidos.append(v)
                    vistos.add(v)
            for r in repetidos:
                erros.append(f"{caminho}: valor repetido no campo {campo!r}: {r}")


def esquema(nome):
    """O molde de um tipo de arquivo de dados, pelo nome: "formato" -> esquemas/formato.schema.json."""
    return PASTA_ESQUEMAS / f"{nome}.schema.json"


def le_json(arquivo, nome):
    """(conteudo, erros) de um arquivo JSON. Com o texto fora do UTF-8 ou JSON invalido, o
    conteudo vem None e o erro diz o que houve, com o nome dado na frente."""
    try:
        return json.loads(Path(arquivo).read_text(encoding="utf-8")), []
    except UnicodeDecodeError:
        return None, [f"{nome}: o texto não está em UTF-8; grave o arquivo de novo em UTF-8"]
    except json.JSONDecodeError as e:
        return None, [f"{nome}: JSON inválido na linha {e.lineno}, coluna {e.colno}: {e.msg}"]


def le_dados(arquivo, schema, nome=None):
    """(dados, erros): a leitura de todo arquivo de dados que tem molde. Le o arquivo e o
    confere contra o molde (o arquivo schema). Com qualquer erro -- texto fora do UTF-8,
    JSON invalido ou fora do molde --, os dados vem None e cada erro vem com o nome do
    arquivo na frente (ou com o nome dado, como o caminho inteiro), pra quem chama mostrar
    com ERRO e nao usar os dados. Nao confere se o arquivo existe: quem chama diz o que
    fazer quando ele falta."""
    nome = nome or Path(arquivo).name
    dados, erros = le_json(arquivo, nome)
    molde, erros_do_molde = le_json(schema, Path(schema).name)
    erros += erros_do_molde
    if not erros:
        erros = [f"{nome}: {e}" for e in erros_de(dados, molde, molde)]
    return (None if erros else dados), erros


def main(argv=None):
    p = argparse.ArgumentParser(description="Confere um arquivo de dados JSON contra o schema dele.")
    p.add_argument("dados", type=Path, help="arquivo de dados .json")
    p.add_argument("--schema", type=Path, help="schema a usar (padrao: scripts/esquemas/<nome>.schema.json)")
    a = p.parse_args(argv)

    caminho_schema = a.schema or esquema(a.dados.stem)
    if not caminho_schema.exists():
        raise SystemExit(f"schema nao encontrado: {caminho_schema}")
    _, erros = le_dados(a.dados, caminho_schema)
    for e in erros:
        print("ERRO:", e)
    print(f"{a.dados}: {len(erros)} erro(s) contra {caminho_schema.name}.")
    return 1 if erros else 0


if __name__ == "__main__":
    sys.exit(main())
