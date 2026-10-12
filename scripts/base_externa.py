# SPDX-License-Identifier: GPL-3.0-or-later
# Copyright do codigo sob GPL-3.0 -- ver LICENSE e NOTICE.md na raiz do projeto.

"""
Monta a base de trechos literais do material de fora de um item, e a conferencia dela.
O script recolhe, a IA julga na curadoria, a pessoa julga na aceitacao:

  1. o arquivo de dados do item (no modelo, dados/bases/<item>.json) declara os lugares
     lidos: de qual fonte (pela chave da referencia), de qual arquivo e de quais paginas;
  2. o script recolhe todo o texto desses lugares e separa em frases, sem filtro nenhum,
     cada uma com um codigo que sai do proprio texto dela:
     <chave>:p<pagina no arquivo>:<impressao digital curta do texto> (ou
     <chave>:<impressao>, em fonte sem paginas, como HTML). Se o texto ou a separacao
     mudar, o codigo muda: a classe antiga aparece como "classe para frase que nao
     existe" e a frase nova como "sem classe" -- nada passa de uma frase para outra em
     silencio;
  3. a IA classifica cada frase no arquivo de dados, numa lista fechada: "usa" (com o
     subtopico e se a fonte afirma ou trata como possibilidade), "outro-item",
     "repetida" (com a frase que ela repete), "fora-do-recorte" ou "nao-e-conteudo";
  4. cada subtopico da grade do formato da disciplina fica marcado como "aula", "fonte"
     ou "lacuna". A grade junta os subtopicos de todos os eixos e os eixos sem
     subtopicos, pelo id: cada id aparece nela uma vez so;
  5. sem nenhum erro nos dados do item, o script grava a base do item (so as frases
     "usa", literais, com a citacao e a pagina, e o registro das fontes no topo); com
     erro, a base fica so com o aviso de que nao foi gerada. E grava a conferencia dos
     trechos: cada pagina
     (ou documento, quando nao ha paginas), com a imagem quando e PDF, as frases e a
     classe de cada uma, e as caixas de tique "IA" e "pessoa".

O script nao julga nada; so recusa o que falta ou contradiz os dados: frase sem classe,
classe para frase que nao existe, subtopico da grade sem marca, subtopico "fonte" sem
nenhuma frase, frase usada num subtopico que a aula cobre ou que e lacuna, id que se
repete na grade do formato da disciplina. A separacao em frases e mecanica (ponto final
seguido de maiuscula, ou marcador de lista); quando ela parte uma frase em duas, o campo
"juntar" do arquivo de dados as une.

As listas fechadas (a classe, a afirmacao e a cobertura) sao as do molde do arquivo de
dados (base.schema.json). A base e a conferencia mostram cada valor com uma descricao em
portugues; um valor que o molde passe a aceitar e que ainda nao tenha descricao aparece
como esta.

Depois de gravar, roda as referencias (referencias.py), porque a base registra as
fontes que usa. Os caminhos vem do projeto.json: "bases", "base_externa",
"conferencia_trechos", "formato" e "imagens", e a resolucao das imagens, de
"resolucao_imagens". O formato da disciplina e o arquivo de dados de cada item sao lidos
pela leitura de todo arquivo de dados (validar_dados.le_dados), cada um contra o molde dele
(formato.schema.json e base.schema.json), com o texto fora do UTF-8, o JSON invalido e o
que esta fora do molde como erro: com erro no formato, cada erro aparece com ERRO e nada e
gerado; com erro nos dados de um item, cada erro aparece com ERRO, o item nao e gerado e a
conferencia nao e refeita. Precisa dos comandos pdftotext e pdftoppm (Poppler) quando
alguma fonte e PDF.

Roda sempre todos os itens que tem arquivo de dados: a conferencia e um arquivo so, e os
tiques de um item so continuam nela se o item for gerado de novo junto com os outros.

A copia de cada fonte tem de ficar na pasta protegida ("material_base"). Se um lugar
declara uma fonte fora dela, o script mostra de onde pra onde ela iria (a pasta
"fontes_externas"), pergunta e, se a pessoa confirmar, leva a fonte e corrige o caminho
no arquivo de dados do item; com --mover, leva sem perguntar. Se ela nao for, o item nao
e gerado.

Uso (de qualquer pasta dentro do projeto):
    python scripts/base_externa.py
    python scripts/base_externa.py --mover
    python scripts/base_externa.py --projeto projeto.json
"""

import argparse
import hashlib
import html
import json
import os
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from comum import (acha_projeto, ancora, assinatura, caixas, comando, dentro, imagem, impressao,  # noqa: E402
                   le_formato, leva_para, link, marca, tiques_anteriores, tiques_da_parte)
from validar_dados import esquema, le_dados  # noqa: E402

# descricao em portugues dos valores das listas fechadas do molde (base.schema.json); o
# valor que o molde aceitar e nao estiver aqui aparece como esta (ver descreve)
CLASSES = {
    "usa": "usa",
    "outro-item": "fala de outro item",
    "repetida": "repete outra frase",
    "fora-do-recorte": "fora do recorte",
    "nao-e-conteudo": "não é conteúdo",
}
AFIRMACAO = {"categorica": "a fonte afirma", "possibilidade": "a fonte trata como possibilidade"}
COBERTURA = {"aula": "coberto pela aula", "fonte": "coberto pelo material de fora",
             "lacuna": "lacuna: nenhuma fonte cobre"}
TEXTO_INTEIRO = "texto inteiro"  # o lugar de uma frase de fonte sem paginas
PARAGRAFO = "¶"  # marca interna de quebra de bloco (linha em branco no PDF, fim de bloco no HTML)
FIM_DE_FRASE = re.compile(r'(?<=[.!?])\s+(?=[A-ZÀ-Ý"“(])|\s*[•▪●¶]\s*')
BLOCO_HTML = re.compile(r"(?i)</?(p|div|h[1-6]|li|tr|td|th|br|section|article|header|footer|ul|ol|table|caption"
                        r"|dt|dd|blockquote|title)\b[^>]*>")
CERCA = "````"


# ---------- texto das fontes ----------

def normaliza(texto):
    """Junta as linhas, desfaz a hifenizacao silabica de fim de linha, marca a linha em
    branco como quebra de bloco e junta espacos."""
    texto = texto.replace("­\n", "").replace("­", "")
    texto = re.sub(r"-\n(?=[a-zà-ÿ])", "", texto)
    texto = re.sub(r"\n\s*\n", f" {PARAGRAFO} ", texto)
    return re.sub(r"\s+", " ", texto).strip()


def texto_pdf(arquivo, pagina):
    return normaliza(comando(["pdftotext", "-f", str(pagina), "-l", str(pagina), str(arquivo), "-"]))


def texto_marcado(arquivo):
    """Texto de HTML ou XML: sem script e estilo, com as marcas de texto corrido juntas."""
    s = Path(arquivo).read_text(encoding="utf-8", errors="ignore")
    s = re.sub(r"(?is)<(script|style)[^>]*>.*?</\1>", " ", s)
    s = BLOCO_HTML.sub(f" {PARAGRAFO} ", s)
    s = re.sub(r"(?i)</?(em|i|strong|b|a|span|sup|sub|u|abbr)(\s[^>]*)?>", "", s)
    s = normaliza(html.unescape(re.sub(r"<[^>]+>", " ", s)))
    return re.sub(r"\s+([,.;:)])", r"\1", s)


def frases(texto):
    return [f.strip() for f in FIM_DE_FRASE.split(texto) if f and f.strip() and f.strip() != PARAGRAFO]


def eh_pdf(arquivo):
    return arquivo.suffix.lower() == ".pdf"


def pagina_impressa(lugar, p):
    impressas = lugar.get("impressas", {})
    if str(p) in impressas:
        return f"p. {impressas[str(p)]}"
    if "desloca" in lugar:
        return f"p. {p + lugar['desloca']}"
    return "p. ?"


def com_codigos(prefixo, fs):
    """[(codigo, frase)]: o codigo e o prefixo mais a impressao digital curta do texto da
    frase; frase repetida na mesma parte ganha -2, -3..., na ordem."""
    out, vistos = [], {}
    for f in fs:
        h = hashlib.sha256(f.encode("utf-8")).hexdigest()[:8]
        vistos[h] = vistos.get(h, 0) + 1
        out.append((f"{prefixo}:{h}" + (f"-{vistos[h]}" if vistos[h] > 1 else ""), f))
    return out


def partes_do_lugar(lugar, raiz):
    """[(parte, pagina ou None, [(codigo, frase)])]: uma parte por pagina, ou o documento inteiro."""
    arquivo = raiz / lugar["arquivo"]
    if eh_pdf(arquivo):
        return [(f"{lugar['fonte']}:p{p}", p, com_codigos(f"{lugar['fonte']}:p{p}", frases(texto_pdf(arquivo, p))))
                for p in lugar["paginas"]]
    return [(lugar["fonte"], None, com_codigos(lugar["fonte"], frases(texto_marcado(arquivo))))]


def junta(partes, grupos, erros):
    """Une as frases de cada grupo do campo "juntar" na primeira delas."""
    texto = {c: f for _, _, fs in partes for c, f in fs}
    some = set()
    for grupo in grupos:
        faltam = [c for c in grupo if c not in texto]
        if faltam:
            erros.append(f"juntar: frase que não existe: {', '.join(faltam)}")
            continue
        texto[grupo[0]] = " ".join(texto[c] for c in grupo)
        some.update(grupo[1:])
    return [(parte, p, [(c, texto[c]) for c, _ in fs if c not in some]) for parte, p, fs in partes]


# ---------- dados ----------

def unidades_da_grade(formato):
    """({id: (rotulo, eixo)}, erros): os subtopicos de cada eixo, ou o proprio eixo quando
    nao tem subtopicos. Os ids de todos eles formam uma grade so, entao um id que aparece
    nela mais de uma vez -- em eixos diferentes, ou num subtopico e num eixo sem
    subtopicos -- e erro: a cobertura e as classes nao teriam como dizer de qual falam."""
    out, onde = {}, {}
    for eixo in formato["eixos"]:
        for sub in eixo["subtopicos"] or [eixo]:
            out[sub["id"]] = (f"{sub['id']} {sub['nome']}", eixo)
            onde.setdefault(sub["id"], []).append(f"subtópico {sub['nome']}, do eixo {eixo['id']}"
                                                 if eixo["subtopicos"] else f"eixo {eixo['nome']}, sem subtópicos")
    erros = [f"id repetido na grade do formato da disciplina: {u} ({'; '.join(lugares)})"
             for u, lugares in onde.items() if len(lugares) > 1]
    return out, erros


def confere(dados, grade, partes, item_ok):
    """Erros de dados: tudo o que falta ou se contradiz. Nao julga conteudo."""
    erros = []
    if not item_ok:
        erros.append(f"o item {dados['item']!r} não está nos itens do formato da disciplina")
    codigos = {c for _, _, fs in partes for c, _ in fs}
    classes, cobertura = dados["classes"], dados["cobertura"]
    for c in sorted(set(classes) - codigos):
        erros.append(f"classe para frase que não existe: {c}")
    sem_classe = [c for _, _, fs in partes for c, _ in fs if c not in classes]
    if sem_classe:
        erros.append(f"{len(sem_classe)} frase(s) sem classe: {', '.join(sem_classe)}")
    for u in grade:
        if u not in cobertura:
            erros.append(f"subtópico {u} da grade sem marca de cobertura")
    for u in sorted(set(cobertura) - set(grade)):
        erros.append(f"cobertura para subtópico que não está na grade: {u}")
    usadas = {}
    for c, cl in classes.items():
        if cl["classe"] == "usa":
            sub = cl["subtopico"]
            usadas.setdefault(sub, []).append(c)
            if sub not in grade:
                erros.append(f"{c}: subtópico {sub} não está na grade")
            elif cobertura.get(sub) in ("aula", "lacuna"):
                erros.append(f"{c}: usada no subtópico {sub}, que está marcado como {cobertura[sub]}")
        if cl["classe"] == "repetida" and cl["de"] not in codigos:
            erros.append(f"{c}: repete uma frase que não existe: {cl['de']}")
    for u, marca_ in cobertura.items():
        if marca_ == "fonte" and u in grade and not usadas.get(u):
            erros.append(f"subtópico {u} marcado como fonte, sem nenhuma frase usada")
    return erros


# ---------- arquivos gerados ----------

def descreve(tabela, valor):
    """A descricao em portugues do valor de uma lista fechada do molde; o proprio valor, se
    o molde aceita um valor que a tabela ainda nao descreve -- o script nao para por isso."""
    return tabela.get(valor, valor)


def descricao(classe):
    if classe is None:
        return "**sem classe**"
    texto = descreve(CLASSES, classe["classe"])
    if classe["classe"] == "usa":
        texto += f", subtópico {classe['subtopico']}, {descreve(AFIRMACAO, classe['afirmacao'])}"
    if classe["classe"] == "repetida":
        texto += f" ({classe['de']})"
    return texto


def grava_base(dados, formato, grade, partes, lugares, raiz, saida, com_erro):
    item = next((i for i in formato["itens"] if i["id"] == dados["item"]), {"nome": dados["item"]})
    if com_erro:
        saida.parent.mkdir(parents=True, exist_ok=True)
        saida.write_text(f"# Base de trechos do material de fora — {item['nome']}\n\nBase não gerada: os dados do "
                         "item ou o formato da disciplina têm erro. Resolva cada ERRO e rode o base_externa.py de "
                         "novo.\n", encoding="utf-8")
        return
    registro, vistos = [], set()
    for lugar in lugares:
        if lugar["fonte"] not in vistos:
            vistos.add(lugar["fonte"])
            arquivo = raiz / lugar["arquivo"]
            registro.append(f"fonte {lugar['fonte']}: {lugar['arquivo']} | sha256: {impressao(arquivo)}")
    por_codigo = {c: (parte, p, f) for parte, p, fs in partes for c, f in fs}
    lugar_da_fonte = {l["fonte"]: l for l in lugares}
    corpo = ["---"] + registro + ["---", "", f"# Base de trechos do material de fora — {item['nome']}"]
    for eixo in formato["eixos"]:
        corpo += ["", f"## {eixo['id']}. {eixo['nome']}"]
        for sub in eixo["subtopicos"] or [eixo]:
            if eixo["subtopicos"]:
                corpo += ["", f"### {sub['id']} {sub['nome']}"]
            marca_ = dados["cobertura"].get(sub["id"])
            corpo += ["", f"Cobertura: {'sem marca' if marca_ is None else descreve(COBERTURA, marca_)}"]
            for c, cl in dados["classes"].items():
                if cl["classe"] != "usa" or cl["subtopico"] != sub["id"] or c not in por_codigo:
                    continue
                _, p, f = por_codigo[c]
                fonte = c.split(":")[0]
                local = (f"{pagina_impressa(lugar_da_fonte[fonte], p)} (arquivo p. {p})" if p is not None
                         else TEXTO_INTEIRO)
                corpo += ["", f"**{fonte}, {local} — {c} — {descreve(AFIRMACAO, cl['afirmacao'])}**", "", f"> {f}"]
    saida.parent.mkdir(parents=True, exist_ok=True)
    saida.write_text("\n".join(corpo) + "\n", encoding="utf-8")


def bloco_do_item(dados, arquivo_dados, base, partes, lugares, raiz, saida, anteriores, pasta_img, resolucao):
    item = dados["item"]
    lugar_da_fonte = {l["fonte"]: l for l in lugares}
    corpo = ["", "---", "", f"## {item}", "", f"Dados: `{link(arquivo_dados, saida)}` · base gerada: `{link(base, saida)}`"]
    cont = [0, 0, 0, 0]  # partes, tique IA, tique pessoa, sem classe
    sig_cob = assinatura(json.dumps(dados["cobertura"], sort_keys=True))
    tiques, retirado = tiques_da_parte(anteriores, item, "cobertura", sig_cob)
    corpo += ["", f"### {item} — cobertura da grade", "", marca(item, "cobertura", sig_cob), ""]
    corpo += [f"- {u}: {descreve(COBERTURA, m)}" for u, m in sorted(dados["cobertura"].items())] + [""]
    if retirado:
        corpo += ["Tique retirado: a cobertura mudou depois do tique", ""]
    corpo += caixas(tiques)
    cont = [cont[0] + 1, cont[1] + tiques["IA"], cont[2] + tiques["pessoa"], cont[3]]
    for parte, p, fs in partes:
        fonte = parte.split(":")[0]
        lugar = lugar_da_fonte[fonte]
        arquivo = raiz / lugar["arquivo"]
        classes = [dados["classes"].get(c) for c, _ in fs]
        sig = assinatura(impressao(arquivo), parte, *[f"{c}|{f}|{json.dumps(cl, sort_keys=True)}"
                                                      for (c, f), cl in zip(fs, classes)])
        tiques, retirado = tiques_da_parte(anteriores, item, parte, sig)
        titulo = f"{pagina_impressa(lugar, p)} (arquivo p. {p})" if p is not None else TEXTO_INTEIRO
        corpo += ["", f"### {fonte} — {titulo}", "", marca(item, parte, sig), ""]
        if p is not None:
            nome_img = re.sub(r"[^\w.-]", "_", f"{item}-{fonte}")
            corpo += [f"[original, arquivo p. {p}]({link(arquivo, saida)}#page={p})", "",
                      f"![{fonte}, arquivo p. {p}]({link(imagem(arquivo, p, pasta_img, nome_img, resolucao), saida)})",
                      ""]
        else:
            corpo += [f"[original]({link(arquivo, saida)})", ""]
        for (c, f), cl in zip(fs, classes):
            corpo += [f"- **{c}** — {descricao(cl)}", f"  > {f}"]
            cont[3] += cl is None
        corpo.append("")
        if retirado:
            corpo += ["Tique retirado: o texto, a fonte ou as classes desta parte mudaram depois do tique", ""]
        corpo += caixas(tiques)
        cont = [cont[0] + 1, cont[1] + tiques["IA"], cont[2] + tiques["pessoa"], cont[3]]
    return corpo, cont


def leva_lugares(projeto, lugares, sem_perguntar):
    """Leva pra pasta das copias do material de fora cada fonte declarada que esteja fora
    da pasta protegida, e muda o caminho dela nos lugares. Devolve quantos caminhos
    mudaram, ou None se alguma fonte ficou fora."""
    raiz, protegida, novos = projeto.raiz, projeto.caminho("material_base"), {}
    for lugar in lugares:
        if lugar["arquivo"] not in novos:
            arquivo = raiz / lugar["arquivo"]
            if not arquivo.exists() or dentro(arquivo, protegida):
                continue
            novo = leva_para(arquivo, projeto.caminho("fontes_externas"), sem_perguntar)
            if novo is None:
                return None
            novos[lugar["arquivo"]] = Path(os.path.relpath(novo, raiz)).as_posix()
        lugar["arquivo"] = novos[lugar["arquivo"]]
    return len(novos)


def processa(projeto, arquivo_dados, formato, anteriores, sem_perguntar):
    dados, erros = le_dados(arquivo_dados, esquema("base"))
    if erros:
        return None, erros
    raiz, lugares = projeto.raiz, dados["lugares"]
    movidos = leva_lugares(projeto, lugares, sem_perguntar)
    if movidos is None:
        return None, [f"{arquivo_dados.name}: uma fonte declarada está fora da pasta protegida e não foi "
                      "levada pra dentro; nada foi gerado pra este item"]
    if movidos:
        arquivo_dados.write_text(json.dumps(dados, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    erros = []
    for lugar in lugares:
        arquivo = raiz / lugar["arquivo"]
        if not arquivo.exists():
            erros.append(f"{lugar['fonte']}: arquivo não existe: {lugar['arquivo']}")
        elif eh_pdf(arquivo) and (not lugar.get("paginas") or min(lugar["paginas"]) < 1):
            erros.append(f"{lugar['fonte']}: fonte em PDF precisa das páginas lidas (a partir de 1)")
    chaves = [l["fonte"] for l in lugares]
    for chave in sorted({c for c in chaves if chaves.count(c) > 1 and
                         len({l["arquivo"] for l in lugares if l["fonte"] == c}) > 1}):
        erros.append(f"a chave {chave} aponta para mais de um arquivo")
    if erros:
        return None, [f"{arquivo_dados.name}: {e}" for e in erros]
    partes = junta([pt for l in lugares for pt in partes_do_lugar(l, raiz)], dados.get("juntar", []), erros)
    grade, erros_da_grade = unidades_da_grade(formato)
    erros += erros_da_grade + confere(dados, grade, partes, any(i["id"] == dados["item"] for i in formato["itens"]))
    base = projeto.caminho_com("base_externa", dados["item"])
    grava_base(dados, formato, grade, partes, lugares, raiz, base, bool(erros))
    saida = projeto.caminho("conferencia_trechos")
    bloco, cont = bloco_do_item(dados, arquivo_dados, base, partes, lugares, raiz, saida, anteriores,
                                projeto.pasta_de_imagens(saida), projeto.valor("resolucao_imagens"))
    return (dados["item"], bloco, cont), [f"{dados['item']}: {e}" for e in erros]


def main(argv=None):
    p = argparse.ArgumentParser(description="Monta a base de trechos do material de fora e a conferência dela.")
    p.add_argument("--mover", action="store_true",
                   help="leva pra pasta protegida, sem perguntar, a fonte declarada que estiver fora dela")
    p.add_argument("--projeto", type=Path, help="projeto.json (padrao: o primeiro achado subindo a partir daqui)")
    a = p.parse_args(argv)
    projeto = acha_projeto(a.projeto)
    if not projeto.caminho("formato").exists():
        raise SystemExit(f"o formato da disciplina não existe: {projeto.caminho('formato')} -- "
                         "grave nele o formato da disciplina; o README dos scripts diz o que vai em cada campo")
    formato, erros = le_formato(projeto)
    if erros:
        # a grade, os itens e os titulos da base saem do formato: com erro nele, nada e
        # gerado, e a base e a conferencia de antes ficam como estavam
        for e in erros:
            print("ERRO:", e)
        print("Nenhuma base gerada e a conferência não foi refeita: resolva cada ERRO no formato da disciplina "
              "e rode de novo.")
        return 1
    arquivos = projeto.todos_com("bases")
    if not arquivos:
        raise SystemExit("nenhum arquivo de dados de base encontrado")
    saida = projeto.caminho("conferencia_trechos")
    anteriores = tiques_anteriores(saida)
    resumo, corpo, todos_erros, sem_bloco = [], [], [], []
    totais = [0, 0, 0, 0]
    for arquivo_dados in arquivos:
        resultado, erros = processa(projeto, arquivo_dados, formato, anteriores, a.mover)
        todos_erros += erros
        if not resultado:
            sem_bloco.append(arquivo_dados.name)
            continue
        item, bloco, (partes, ia, pessoa, sem_classe) = resultado
        corpo += bloco
        totais = [a + b for a, b in zip(totais, (partes, ia, pessoa, sem_classe))]
        resumo.append(f"| [{item}](#{ancora(item)}) | {partes} | {sem_classe} | {ia} | {pessoa} | {partes - pessoa} |")
    for e in todos_erros:
        print("ERRO:", e)
    if sem_bloco:
        # a conferencia e um arquivo so: regrava-la sem um item apagaria os tiques dele
        print(f"A conferência não foi refeita, pra não perder os tiques de {', '.join(sem_bloco)}: "
              "resolva os erros acima e rode de novo.")
        return 1
    cabecalho = ["# Conferência dos trechos do material de fora", "",
                 "| Item | Partes | Frases sem classe | Tique da IA | Tique da pessoa | Sem tique da pessoa |",
                 "| :--- | ---: | ---: | ---: | ---: | ---: |"] + resumo
    cabecalho.append(f"| **Total** | **{totais[0]}** | **{totais[3]}** | **{totais[1]}** | **{totais[2]}** | "
                     f"**{totais[0] - totais[2]}** |")
    saida.parent.mkdir(parents=True, exist_ok=True)
    saida.write_text("\n".join(cabecalho + corpo) + "\n", encoding="utf-8")
    print(f"{totais[0]} parte(s) | frases sem classe: {totais[3]} | sem tique da pessoa: {totais[0] - totais[2]}")
    print(f"conferência: {saida}")

    # gancho: a base registra as fontes que usa, entao as referencias sao refeitas
    import referencias
    resultado_refs = referencias.roda(projeto)
    return 1 if (todos_erros or resultado_refs) else 0


if __name__ == "__main__":
    sys.exit(main())
