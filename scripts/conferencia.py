# SPDX-License-Identifier: GPL-3.0-or-later
# Copyright do codigo sob GPL-3.0 -- ver LICENSE e NOTICE.md na raiz do projeto.

"""
Gera o arquivo de conferencia das transcricoes das fontes. O arquivo nasce do que foi
gerado da fonte, nao da fonte: cada transcricao e mostrada pagina por pagina, com o link
para o original, e o script nao julga o conteudo.

Fonte em PDF: cada pagina da transcricao aparece ao lado da imagem da mesma pagina no
PDF, com duas caixas de tique, "IA" e "pessoa". Quem confere e quem tica -- a IA pode
ticar primeiro, e nenhuma pagina vale como conferida sem o tique da pessoa. Pagina do PDF
que a transcricao nao tem aparece com a imagem e sem texto; secao que aponta para pagina
que o PDF nao tem aparece com o texto e sem imagem.

Fonte em HTML com as paginas impressas marcadas (ver transcrever_html.py): o texto da
transcricao e copia do documento, e quem o confere e o script, pagina por pagina, contra
o texto da mesma pagina na fonte -- as mesmas letras, numeros e sinais, na mesma ordem,
sem contar os espacos, as marcas da transcricao (titulo, tabela, "<br>", escapes,
continuacao de tabela, "[sem texto]") e a forma dos indices e expoentes. Confere tambem o
numero impresso no titulo da pagina e as imagens dela, na ordem. O que nao bate e ERRO. O
texto de dentro de cada imagem, que veio do OCR, e o que se confere a mao: cada imagem
aparece com esse texto e as duas caixas de tique.

A transcricao e ligada a fonte pelo registro no topo dela (ver registrar_fonte.py), nunca
pelo nome dos arquivos: uma transcricao registra uma fonte so. O arquivo gerado diz, para
cada transcricao, se a fonte registrada ainda e a mesma, se mudou depois do registro ou
se nao existe.

Convencao da transcricao (secao 2 da metodologia): o registro da fonte no topo e uma
secao por pagina, com o titulo "## <como a citacao chama a pagina> (arquivo p. <posicao
no arquivo>)" -- por exemplo, "## p. 12 (arquivo p. 14)" ou "## slide 3 (arquivo p. 3)".
Pagina sem texto nenhum fica com a secao e a marca "[sem texto]".

Os tiques ficam no proprio arquivo gerado, com a assinatura do que foi conferido. Ao
gerar de novo, o tique volta se a assinatura e a mesma; se o texto ou a fonte mudou, o
tique e retirado, e a parte diz isso.

As pastas, o arquivo gerado, a pasta das imagens e a resolucao delas vem do projeto.json
("gerados", "conferencia_imagens", "material_base", "imagens" e "resolucao_imagens").
Precisa dos comandos pdfinfo e pdftoppm (pacote Poppler) quando ha fonte em PDF.

Uso (de qualquer pasta dentro do projeto):
    python scripts/conferencia.py
    python scripts/conferencia.py --projeto projeto.json
"""

import argparse
import re
import sys
import unicodedata
from pathlib import Path
from urllib.parse import unquote, urlsplit

sys.path.insert(0, str(Path(__file__).resolve().parent))
from comum import (EXTENSOES_HTML, FIM_FIGURA, LINHA_CONTINUACAO, LINHA_FIGURA, ROTULO_PAGINA, SEM_TEXTO,  # noqa: E402
                   TITULO_PAGINA, acha_projeto, ancora, assinatura, caixas, caminho_do_alvo, fontes_registradas,
                   imagem, impressao, link, marca, numero_de_paginas, paginas_html, situacao_da_copia,
                   tiques_anteriores, tiques_da_parte)

CERCA = "````"  # cerca de 4 crases: a transcricao pode ter blocos de 3
SEPARADOR = re.compile(r"^\|(?:\s*:?-{3,}:?\s*\|)+$")
TITULO_DE_SECAO = re.compile(r"^#{3,6} ")
FIGURA_NA_LINHA = re.compile(r"!\[imagem\]\([^)]*\)")
CONTEXTO = 30  # caracteres mostrados em volta da primeira diferenca

SITUACAO = {
    "confere": "é o mesmo do registro",
    "mudou": "mudou depois do registro",
    "nao-existe": "não existe",
    "sem-registro": "a transcrição não registra de qual arquivo veio",
    "varias": "a transcrição registra mais de uma fonte",
}


def secoes(texto):
    """[(rotulo, pagina, texto)] na ordem do arquivo."""
    out, atual = [], None
    for linha in texto.split("\n"):
        m = TITULO_PAGINA.match(linha)
        if m:
            atual = [m.group(1).strip(), int(m.group(2)), []]
            out.append(atual)
        elif linha.startswith("## "):
            atual = None
        elif atual is not None:
            atual[2].append(linha)
    return [(r, n, "\n".join(t).strip()) for r, n, t in out]


def transcricoes_da_pasta(pasta, saida):
    """Todo .md da pasta que tem pelo menos um titulo de pagina, menos o arquivo gerado."""
    out = []
    for arq in sorted(pasta.glob("*.md")):
        if arq.resolve() == saida.resolve():
            continue
        texto = arq.read_text(encoding="utf-8")
        if secoes(texto):
            out.append((arq, texto))
    return out


def fonte_da_transcricao(texto, raiz):
    """(chave ou None, caminho do arquivo da fonte ou None, situacao do registro)."""
    registradas = fontes_registradas(texto)
    if not registradas:
        return None, None, "sem-registro"
    if len(registradas) > 1:
        return None, None, "varias"
    chave, (caminho, hash_registrado) = next(iter(registradas.items()))
    arquivo, situacao = situacao_da_copia(raiz, caminho, hash_registrado)
    return chave, arquivo, situacao


def por_pagina(texto):
    """{posicao no arquivo: [(rotulo, texto)]} das secoes da transcricao."""
    out = {}
    for rotulo, n, conteudo in secoes(texto):
        out.setdefault(n, []).append((rotulo, conteudo))
    return out


# ---------- fonte em PDF ----------

def partes_pdf(nome, texto, pdf, situacao, anteriores, pasta_img, resolucao):
    com_pdf = situacao in ("confere", "mudou")
    hash_pdf = impressao(pdf) if com_pdf else ""
    total = numero_de_paginas(pdf) if com_pdf else 0
    paginas = por_pagina(texto)
    out = []
    for n in sorted(set(range(1, total + 1)) | set(paginas)):
        secs = paginas.get(n, [])
        rotulo = " / ".join(r for r, _ in secs) or f"arquivo p. {n}"
        sig = assinatura(hash_pdf, n, rotulo, "\n\n".join(c for _, c in secs))
        tiques, retirado = tiques_da_parte(anteriores, nome, n, sig)
        out.append({"n": n, "rotulo": rotulo, "secoes": secs, "sig": sig, "tiques": tiques, "retirado": retirado,
                    "imagem": imagem(pdf, n, pasta_img, nome, resolucao) if com_pdf and n <= total else None})
    return out


def bloco_pdf(nome, pdf, parte, saida):
    n = parte["n"]
    out = ["", f"### {nome} — {parte['rotulo']} (arquivo p. {n})", "", marca(nome, n, parte["sig"]), ""]
    if parte["imagem"]:
        out += [f"[original, arquivo p. {n}]({link(pdf, saida)}#page={n})", "",
                f"![{nome}, arquivo p. {n}]({link(parte['imagem'], saida)})", ""]
    else:
        out += ["Imagem: nenhuma (o PDF não tem esta página ou não está disponível)", ""]
    if parte["secoes"]:
        for _, conteudo in parte["secoes"]:
            out += [CERCA, conteudo, CERCA, ""]
    else:
        out += ["Transcrição: nenhuma seção para esta página", ""]
    if parte["retirado"]:
        out += ["Tique retirado: o texto desta página ou o PDF mudou depois do tique", ""]
    return out + caixas(parte["tiques"])


# ---------- fonte em HTML ----------

def comparavel(texto):
    """O texto so com as letras, numeros e sinais, na forma unica do Unicode (NFKC, que
    tambem desfaz indice e expoente: CO₂ fica CO2)."""
    return "".join(unicodedata.normalize("NFKC", texto).split())


def le_pagina(conteudo):
    """(texto comparavel, [(alvo, linhas do texto)] das imagens, imagem sem fim): o que a
    transcricao da pagina tem de texto da fonte, sem as marcas da transcricao, e as
    imagens, com o texto de dentro de cada uma."""
    linhas, figuras, figura = [], [], None
    for linha in conteudo.split("\n"):
        if figura is not None:
            if linha == FIM_FIGURA:
                figuras.append(figura)
                figura = None
            else:
                figura[1].append(linha)
            continue
        m = LINHA_FIGURA.match(linha)
        if m:
            figura = (caminho_do_alvo(m.group(1)), [])
            continue
        if linha == SEM_TEXTO or LINHA_CONTINUACAO.match(linha) or SEPARADOR.match(linha):
            continue
        linha = FIGURA_NA_LINHA.sub("", TITULO_DE_SECAO.sub("", linha))
        if linha.startswith("|"):
            linha = re.sub(r"(?<!\\)\|", "", linha.replace("<br>", ""))
        linhas.append(re.sub(r"^\\#", "#", linha).replace("\\|", "|"))
    if figura is not None:
        figuras.append(figura)
    return comparavel("".join(linhas)), figuras, figura is not None


def primeira_diferenca(fonte, transcricao):
    i = next((k for k, (a, b) in enumerate(zip(fonte, transcricao)) if a != b), min(len(fonte), len(transcricao)))
    trecho = lambda s: ("…" if i > CONTEXTO else "") + s[max(0, i - CONTEXTO):i + CONTEXTO] + (  # noqa: E731
        "…" if len(s) > i + CONTEXTO else "")
    return f"a fonte tem \"{trecho(fonte)}\"; a transcrição, \"{trecho(transcricao)}\""


def arquivo_da_imagem(pasta, alvo):
    """O arquivo da imagem, se o alvo e um caminho local que existe; senao, o proprio alvo."""
    partes = urlsplit(alvo)
    if alvo and not partes.scheme:
        arquivo = (pasta / unquote(partes.path)).resolve()
        if arquivo.is_file():
            return arquivo
    return alvo


def partes_html(nome, arq, texto, fonte, situacao, anteriores):
    """[pagina], cada uma com o resultado do script ("erros") e as imagens, com os tiques."""
    com_fonte = situacao in ("confere", "mudou")
    da_fonte = paginas_html(fonte.read_text(encoding="utf-8")) if com_fonte else []
    paginas = por_pagina(texto)
    out = []
    for n in sorted(set(range(1, len(da_fonte) + 1)) | set(paginas)):
        secs = paginas.get(n, [])
        rotulo = " / ".join(r for r, _ in secs) or f"arquivo p. {n}"
        conteudo = "\n\n".join(c for _, c in secs)
        lido, figuras, sem_fim = le_pagina(conteudo)
        erros = []
        if com_fonte and n > len(da_fonte):
            erros.append("a fonte não tem esta página")
        elif com_fonte:
            pagina = da_fonte[n - 1]
            if not secs:
                erros.append("a transcrição não tem esta página")
            elif pagina.rotulo is not None and rotulo != ROTULO_PAGINA.format(pagina.rotulo):
                erros.append(f"na fonte, esta é a {ROTULO_PAGINA.format(pagina.rotulo)}")
            esperado = comparavel(pagina.texto)
            if secs and lido != esperado:
                erros.append("o texto não é o da fonte: " + primeira_diferenca(esperado, lido))
            imagens = [arquivo_da_imagem(fonte.parent, src) for src in pagina.imagens]
            if [arquivo_da_imagem(arq.parent, alvo) for alvo, _ in figuras] != imagens:
                erros.append(f"as imagens não são as da fonte, na ordem (a fonte tem {len(imagens)}, a transcrição, "
                             f"{len(figuras)})")
        if sem_fim:
            erros.append(f"uma imagem não tem a linha \"{FIM_FIGURA}\"")
        imgs = []
        for j, (alvo, linhas) in enumerate(figuras, 1):
            arquivo = arquivo_da_imagem(arq.parent, alvo)
            sig = assinatura(impressao(arquivo) if isinstance(arquivo, Path) else alvo, n, j, "\n".join(linhas))
            tiques, retirado = tiques_da_parte(anteriores, nome, f"{n}.{j}", sig)
            imgs.append({"j": j, "arquivo": arquivo, "linhas": linhas, "sig": sig, "tiques": tiques,
                         "retirado": retirado})
        out.append({"n": n, "rotulo": rotulo, "ancora": da_fonte[n - 1].ancora if n <= len(da_fonte) else None,
                    "erros": erros, "imagens": imgs})
    return out


def bloco_html(nome, fonte, pagina, saida):
    n = pagina["n"]
    out = ["", f"### {nome} — {pagina['rotulo']} (arquivo p. {n})", ""]
    if fonte is not None and fonte.exists():
        out += [f"[original, arquivo p. {n}]({link(fonte, saida)}{'#' + pagina['ancora'] if pagina['ancora'] else ''})",
                ""]
    out += [f"ERRO: {e}" for e in pagina["erros"]] or ["Texto: o mesmo da fonte."]
    for img in pagina["imagens"]:
        j, arquivo = img["j"], img["arquivo"]
        out += ["", f"#### {nome} — {pagina['rotulo']}, imagem {j}", "", marca(nome, f"{n}.{j}", img["sig"]), ""]
        out += [f"![{nome}, {pagina['rotulo']}, imagem {j}]({link(arquivo, saida)})" if isinstance(arquivo, Path)
                else f"Imagem: o arquivo {arquivo} não existe", ""]
        out += [CERCA, "\n".join(img["linhas"]), CERCA, ""] if img["linhas"] else ["Texto da imagem: nenhum", ""]
        if img["retirado"]:
            out += ["Tique retirado: a imagem ou o texto dela mudou depois do tique", ""]
        out += caixas(img["tiques"])
    return out


# ---------- arquivo de conferencia ----------

def gera(transcricoes, saida, raiz, pasta_img, resolucao):
    anteriores = tiques_anteriores(saida)
    resumo, corpo, totais, problemas_de_registro, diferencas, registrados = [], [], [0] * 6, [], [], set()
    for arq, texto in transcricoes_da_pasta(transcricoes, saida):
        nome = arq.stem
        chave, fonte, situacao = fonte_da_transcricao(texto, raiz)
        if fonte is not None:
            registrados.add(fonte)
        if situacao != "confere":
            problemas_de_registro.append((arq, situacao))
        corpo += ["", "---", "", f"## {nome}", "", f"Transcrição: `{link(arq, saida)}`",
                  f"Fonte registrada: {chave or '—'}, `{link(fonte, saida) if fonte else '—'}` ({SITUACAO[situacao]})"]
        if fonte is not None and fonte.suffix.lower() in EXTENSOES_HTML:
            ps = partes_html(nome, arq, texto, fonte, situacao, anteriores)
            tiques = [i["tiques"] for p in ps for i in p["imagens"]]
            com_erro = [p for p in ps if p["erros"]]
            diferencas += [(arq, p["rotulo"], e) for p in com_erro for e in p["erros"]]
            cont = [len(ps), len(com_erro)]
            for p in ps:
                corpo += bloco_html(nome, fonte, p, saida)
        else:
            ps = partes_pdf(nome, texto, fonte, situacao, anteriores, pasta_img, resolucao)
            tiques = [p["tiques"] for p in ps]
            cont = [len(ps), None]
            for p in ps:
                corpo += bloco_pdf(nome, fonte, p, saida)
        cont += [len(tiques), sum(t["IA"] for t in tiques), sum(t["pessoa"] for t in tiques)]
        cont.append(cont[2] - cont[4])
        totais = [a + (b or 0) for a, b in zip(totais, cont)]
        resumo.append(f"| [{nome}](#{ancora(nome)}) | {chave or '—'} | {SITUACAO[situacao]} | "
                      + " | ".join("—" if x is None else str(x) for x in cont) + " |")
    cabecalho = ["# Conferência das transcrições das fontes", "",
                 "Fonte em PDF: cada página tem a imagem e os tiques. Fonte em HTML: o texto de cada página é "
                 "conferido pelo script contra a fonte, e cada imagem tem os tiques.", "",
                 "| Transcrição | Chave da fonte | Fonte registrada | Páginas | Páginas com erro do script | "
                 "A ticar | Tique da IA | Tique da pessoa | Sem tique da pessoa |",
                 "| :--- | :--- | :--- | ---: | ---: | ---: | ---: | ---: | ---: |"] + resumo
    cabecalho.append("| **Total** | | | " + " | ".join(f"**{x}**" for x in totais) + " |")
    saida.parent.mkdir(parents=True, exist_ok=True)
    saida.write_text("\n".join(cabecalho + corpo) + "\n", encoding="utf-8")
    return totais, problemas_de_registro, diferencas, registrados


def main(argv=None):
    p = argparse.ArgumentParser(description="Gera o arquivo de conferência das transcrições das fontes.")
    p.add_argument("--projeto", type=Path, help="projeto.json (padrao: o primeiro achado subindo a partir daqui)")
    a = p.parse_args(argv)
    projeto = acha_projeto(a.projeto)
    transcricoes, saida = projeto.caminho("gerados"), projeto.caminho("conferencia_imagens")
    if not transcricoes_da_pasta(transcricoes, saida):
        raise SystemExit(f"nenhuma transcricao em {transcricoes}")
    (paginas, com_erro, a_ticar, ia, pessoa, sem_pessoa), problemas_de_registro, diferencas, registrados = gera(
        transcricoes, saida, projeto.raiz, projeto.pasta_de_imagens(saida), projeto.valor("resolucao_imagens"))
    for arq, situacao in problemas_de_registro:
        print(f"ERRO: {arq.name} -- fonte registrada: {SITUACAO[situacao]}")
    for arq, rotulo, erro in diferencas:
        print(f"ERRO: {arq.name}, {rotulo}: {erro}")
    sem_transcricao = [pdf for pdf in sorted(projeto.caminho("material_base").glob("*.pdf"))
                       if pdf.resolve() not in registrados]
    for pdf in sem_transcricao:
        print(f"ERRO: {pdf.name} não é a fonte registrada de nenhuma transcrição")
    print(f"{paginas} páginas | com erro do script: {com_erro} | a ticar: {a_ticar} | tique da IA: {ia} | "
          f"tique da pessoa: {pessoa} | sem tique da pessoa: {sem_pessoa}")
    print(f"arquivo: {saida}")
    return 1 if problemas_de_registro or sem_transcricao or diferencas else 0


if __name__ == "__main__":
    sys.exit(main())
