# SPDX-License-Identifier: GPL-3.0-or-later
# Copyright do codigo sob GPL-3.0 -- ver LICENSE e NOTICE.md na raiz do projeto.

"""
Transcreve uma fonte em HTML que marca as paginas impressas -- como o capitulo de um livro
digital (EPUB) -- e grava na pasta das transcricoes (no projeto.json, "gerados") no padrao
da secao 2 da metodologia: uma secao por pagina impressa, com o titulo "## p. <numero
impresso> (arquivo p. <ordem da pagina no documento>)". O texto e o do proprio documento,
copiado sem leitura nenhuma; so o texto de dentro das imagens e lido, por OCR.

A fonte pode ser:
  - o documento (.xhtml, .html, .htm), ja na pasta protegida ("material_base"), com as
    imagens nos lugares para onde ele aponta;
  - a captura de um site (.har), salva pelo navegador enquanto o documento era lido. Da
    captura, o script le so o endereco e o conteudo de cada resposta -- nunca os
    cabecalhos nem os cookies, que ficam nela -- e guarda, na pasta indicada com --pasta,
    dentro da pasta protegida, uma copia de cada documento com marcas de pagina e das
    imagens e estilos para onde ele aponta, na mesma disposicao de pastas do site. Se o
    mesmo documento veio mais de uma vez, vale a versao com marcas de pagina. A
    transcricao sai dessa copia, que e a que se registra; a captura pode ser apagada
    depois.

Como o documento vira texto:
  - paragrafo, legenda e item de lista: uma linha cada, com os espacos juntados; o item
    leva o marcador ("- ", ou o numero na lista numerada);
  - titulo (h1 a h6): com "#", de "###" pra baixo -- o nivel mais alto do documento vira
    "###", porque "##" e o titulo da pagina;
  - tabela: tabela Markdown, com a primeira linha de cabecalho; numa celula, itens
    diferentes (paragrafos, linhas quebradas) se separam com "<br>"; a celula que ocupa
    varias colunas ou linhas fica com o texto na primeira e as outras vazias. A tabela que
    passa pra pagina seguinte continua nela depois de "[continuação da tabela da p. X]",
    com uma linha de cabecalho vazia;
  - indice e expoente: com os caracteres Unicode (CO₂, Mg²⁺); sem o caractere, o texto
    fica na linha, e o script avisa;
  - negrito e italico: texto puro;
  - imagem: "![imagem](caminho)", no lugar dela, seguida do texto escrito dentro dela,
    lido pelo Tesseract (um pedaco por linha), e de "[fim da imagem]", mesmo sem texto. O
    texto da imagem e so rascunho, conferido contra ela. A legenda, que e texto do
    documento, vem no lugar dela;
  - "#" no comeco da linha e "|" ficam escapados ("\\#", "\\|");
  - pagina sem texto: "[sem texto]".
A marca de pagina no meio de um paragrafo o corta: o que vem antes fica na pagina
anterior, e o resto, na seguinte.

Nao grava por cima de uma transcricao que ja existe -- o texto das imagens pode ja estar
conferido --, a nao ser com --substituir; nesse caso, o registro da fonte no topo dela
continua. Precisa do Tesseract, com os dados do idioma do texto das imagens, quando o
documento tem imagem: o idioma e o que o documento declara (lang), traduzido para o codigo
do Tesseract pela tabela da ISO 639 em normas/idiomas.json, ou o que se escolhe com
--idioma ("por", "spa", "eng"...; varios juntos com "+").

Uso (de qualquer pasta dentro do projeto):
    python scripts/transcrever_html.py docs/material-base/CAPTURA.har --pasta docs/material-base/LIVRO-2020
    python scripts/transcrever_html.py docs/material-base/CAPTURA.har --pasta docs/material-base/LIVRO-2020 --documento cap1.xhtml
    python scripts/transcrever_html.py docs/material-base/LIVRO-2020/Text/cap1.xhtml --idioma eng --substituir
"""

import argparse
import base64
import json
import os
import posixpath
import sys
import unicodedata
from pathlib import Path
from urllib.parse import unquote, urljoin, urlsplit

sys.path.insert(0, str(Path(__file__).resolve().parent))
from comum import (CONTINUACAO, EXTENSOES_HTML, FIGURA, FIM_FIGURA, PASTA_NORMAS, ROTULO_PAGINA,  # noqa: E402
                   SEM_TEXTO, acha_projeto, alvo_markdown, comando, dentro, le_html, lingua, paginas_html, percorre,
                   separa_registro)
from validar_dados import esquema, le_dados  # noqa: E402

MODO_OCR = "11"  # Tesseract --psm 11: texto esparso, cada pedaco numa linha, como os rotulos de uma figura
ARQUIVO_IDIOMAS = PASTA_NORMAS / "idiomas.json"  # lingua (ISO 639-1) -> codigo do Tesseract (ISO 639-2)
TITULOS = {f"h{n}": n for n in range(1, 7)}
BLOCOS = {"address", "article", "aside", "blockquote", "body", "caption", "dd", "div", "dl", "dt", "figcaption",
          "figure", "footer", "header", "hr", "html", "li", "main", "nav", "ol", "p", "pre", "section", "ul", *TITULOS}


def _indices(normais, especiais):
    """Os caracteres que tem a versao de indice ou de expoente no Unicode, so os que voltam
    ao normal pela normalizacao NFKC (e por ela que a conferencia compara o texto)."""
    return {c: e for c, e in zip(normais, especiais) if unicodedata.normalize("NFKC", e) == c}


INDICES = {"sup": _indices("0123456789+−=()in", "⁰¹²³⁴⁵⁶⁷⁸⁹⁺⁻⁼⁽⁾ⁱⁿ"),
           "sub": _indices("0123456789+−=()aehijklmnoprstuvx", "₀₁₂₃₄₅₆₇₈₉₊₋₌₍₎ₐₑₕᵢⱼₖₗₘₙₒₚᵣₛₜᵤᵥₓ")}


def escapa(texto):
    texto = texto.replace("|", "\\|")
    return "\\" + texto if texto.startswith("#") else texto


def junta(partes):
    return " ".join("".join(partes).split())


class Tabela:
    """Uma tabela em montagem: as linhas, cada uma com a pagina onde comeca e as celulas
    ([itens, colunas, linhas que ocupa])."""

    def __init__(self, pagina):
        self.pagina, self.linhas, self.celula, self.item, self.legenda = pagina, [], None, [], []
        self.na_legenda, self.profundidade, self.cortada = False, 1, False

    def nova_linha(self):
        self.fim_linha()
        self.linhas.append([None, []])

    def fim_linha(self):
        if self.linhas and self.linhas[-1][0] is None:
            self.linhas[-1][0] = self.pagina

    def nova_celula(self, no):
        inteiro = lambda v: max(int(v), 1) if str(v).isdigit() else 1  # noqa: E731
        self.celula = [[], inteiro(no.attrs.get("colspan", 1)), inteiro(no.attrs.get("rowspan", 1))]
        self.item = []

    def quebra(self):
        texto = junta(self.item)
        if texto and self.celula is not None:
            self.celula[0].append(escapa(texto))
        self.item = []

    def fim_celula(self):
        self.quebra()
        if self.celula is not None:
            self.linhas[-1][1].append(self.celula)
        self.celula = None

    def texto(self, s):
        if self.na_legenda:
            self.legenda.append(s)
            return
        if self.celula is None:
            if s.strip():  # texto solto fora de celula: fica na legenda, pra nao se perder
                self.legenda.append(s)
            return
        self.item.append(s)
        if s.strip() and self.linhas[-1][0] is None:
            self.linhas[-1][0] = self.pagina

    def nova_pagina(self, pagina):
        if self.celula is not None and self.linhas[-1][0] is not None:
            self.cortada = True  # a linha ja tem texto: fica na pagina onde comecou
        self.pagina = pagina

    def grade(self):
        grade, ocupadas = [], set()
        for r, (_, celulas) in enumerate(self.linhas):
            linha, c = [], 0
            for itens, colunas, linhas in celulas:
                while (r, c) in ocupadas:
                    linha.append("")
                    c += 1
                linha += ["<br>".join(itens)] + [""] * (colunas - 1)
                ocupadas |= {(r + i, c + j) for i in range(1, linhas) for j in range(colunas)}
                c += colunas
            while (r, c) in ocupadas:
                linha.append("")
                c += 1
            grade.append(linha)
        colunas = max((len(l) for l in grade), default=0)
        return [l + [""] * (colunas - len(l)) for l in grade], colunas

    def blocos(self, rotulos):
        """[(pagina, texto)]: a tabela em pedacos, um por pagina, na ordem."""
        grade, colunas = self.grade()
        legenda = junta(self.legenda)
        if not grade:
            return [(self.pagina, escapa(legenda))] if legenda else []
        linha = lambda cs: "| " + " | ".join(cs) + " |"  # noqa: E731
        separador = "|" + "|".join("---" for _ in range(colunas)) + "|"
        grupos = []
        for (pagina, _), cs in zip(self.linhas, grade):
            if grupos and grupos[-1][0] == pagina:
                grupos[-1][1].append(cs)
            else:
                grupos.append([pagina, [cs]])
        inicio = rotulos[grupos[0][0]]
        out = [(grupos[0][0], escapa(legenda))] if legenda else []
        for k, (pagina, linhas) in enumerate(grupos):
            if k == 0:
                out.append((pagina, "\n".join([linha(linhas[0]), separador] + [linha(l) for l in linhas[1:]])))
            else:
                out.append((pagina, CONTINUACAO.format(ROTULO_PAGINA.format(inicio if inicio is not None else "?"))))
                out.append((pagina, "\n".join([linha([""] * colunas), separador] + [linha(l) for l in linhas])))
        return out


class Transcricao:
    """Junta os eventos do documento (comum.percorre) nas paginas da transcricao."""

    def __init__(self, nivel_mais_alto, figura):
        self.desloca = 3 - nivel_mais_alto  # h<n> vira "#" * (n + desloca)
        self.figura = figura  # (src, funcao de aviso) -> linhas do bloco da imagem
        self.paginas = [[None, []]]  # [rotulo, blocos]
        self.linha, self.prefixo, self.marcador, self.espera_marcador = [], "", None, False
        self.tabela, self.indice, self.avisos = None, None, []

    def aviso(self, texto):
        self.avisos.append((len(self.paginas) - 1, texto))

    def bloco(self, texto):
        self.paginas[-1][1].append(texto)

    def fecha_linha(self):
        texto = junta(self.linha)
        if texto:
            self.bloco(self.prefixo + escapa(texto))
        self.linha = []

    def texto(self, s):
        if self.marcador and s.strip():
            s, self.marcador = self.marcador + s, None
        if self.tabela:
            self.tabela.texto(s)
        else:
            self.linha.append(s)

    def evento(self, ev):
        if ev[0] == "pagina":
            if self.tabela:
                self.tabela.nova_pagina(len(self.paginas))
            else:
                self.fecha_linha()
            self.paginas.append([ev[1], []])
        elif ev[0] == "texto":
            if self.espera_marcador:  # o primeiro texto do item e o marcador dele (comum.percorre)
                self.marcador, self.espera_marcador = ev[1], False
            elif self.indice is not None:
                self.indice[1].append(ev[1])
            else:
                self.texto(ev[1])
        elif ev[0] == "abre":
            self.abre(ev[1])
        else:
            self.fecha(ev[1])

    def abre(self, no):
        tag, t = no.tag, self.tabela
        if tag == "li":
            self.espera_marcador = True
        if tag in INDICES:
            if self.indice is None:
                self.indice = [tag, [], 0]
            self.indice[2] += 1
        elif tag == "img":
            if t:
                self.aviso("imagem dentro de uma tabela: fica só a marca, sem o texto dela")
                self.texto(" " + FIGURA.format(no.attrs.get("src", "")) + " ")
            else:
                self.fecha_linha()
                self.bloco("\n".join(self.figura(no.attrs.get("src", ""), self.aviso)))
        elif tag == "table":
            if t:
                t.profundidade += 1
                t.quebra()
            else:
                self.fecha_linha()
                self.tabela = Tabela(len(self.paginas) - 1)
        elif t and t.profundidade == 1 and tag == "tr":
            t.nova_linha()
        elif t and t.profundidade == 1 and tag in ("td", "th"):
            if not t.linhas:
                t.nova_linha()
            t.nova_celula(no)
        elif t and t.profundidade == 1 and tag == "caption":
            t.na_legenda = True
        elif t:
            if tag == "br" or tag in BLOCOS or tag in ("tr", "td", "th"):
                t.quebra()
        elif tag == "br":
            self.fecha_linha()
        elif tag in TITULOS:
            self.fecha_linha()
            self.prefixo = "#" * min(6, TITULOS[tag] + self.desloca) + " "
        elif tag in BLOCOS:
            self.fecha_linha()

    def fecha(self, no):
        tag, t = no.tag, self.tabela
        if tag in INDICES and self.indice is not None:
            self.indice[2] -= 1
            if self.indice[2] == 0:
                tipo, partes, _ = self.indice
                self.indice = None
                bruto = "".join(partes)
                if all(c in INDICES[tipo] or c.isspace() for c in bruto):
                    self.texto("".join(INDICES[tipo].get(c, c) for c in bruto))
                else:
                    self.aviso(f"{'expoente' if tipo == 'sup' else 'índice'} sem caractere Unicode, ficou na linha: "
                               f"\"{junta(partes)}\"")
                    self.texto(bruto)
            return
        if tag == "li" and self.marcador:  # item sem texto: fica o marcador
            marcador, self.marcador = self.marcador, None
            self.texto(marcador)
        if t and tag == "table":
            if t.profundidade > 1:
                t.profundidade -= 1
                t.quebra()
                return
            if t.celula is not None:
                t.fim_celula()
            t.fim_linha()
            rotulos = [r for r, _ in self.paginas]
            for pagina, texto in t.blocos(rotulos):
                self.paginas[pagina][1].append(texto)
            if t.cortada:
                self.aviso("marca de página no meio de uma linha de tabela: a linha ficou na página onde começa")
            self.tabela = None
        elif t and t.profundidade == 1 and tag in ("td", "th"):
            t.fim_celula()
        elif t and t.profundidade == 1 and tag == "tr":
            if t.celula is not None:
                t.fim_celula()
            t.fim_linha()
        elif t and t.profundidade == 1 and tag == "caption":
            t.legenda.append(" ")
            t.na_legenda = False
        elif t:
            if tag in BLOCOS:
                t.quebra()
        elif tag in TITULOS:
            self.fecha_linha()
            self.prefixo = ""
        elif tag in BLOCOS:
            self.fecha_linha()

    def texto_final(self):
        """(texto, [(rotulo, aviso)], quantas paginas): as paginas, cada uma com o titulo e
        os blocos. A pagina antes da primeira marca so entra se tiver alguma coisa, como em
        comum.paginas_html."""
        self.fecha_linha()
        rotulo = lambda r: ROTULO_PAGINA.format(r if r is not None else "?")  # noqa: E731
        paginas = self.paginas if self.paginas[0][1] else self.paginas[1:]
        partes = []
        for k, (r, blocos) in enumerate(paginas, 1):
            partes += [f"## {rotulo(r)} (arquivo p. {k})", "", "\n\n".join(blocos) or SEM_TEXTO, ""]
        return "\n".join(partes), [(rotulo(self.paginas[i][0]), a) for i, a in self.avisos], len(paginas)


def nivel_mais_alto(arvore):
    niveis = [TITULOS[ev[1].tag] for ev in percorre(arvore) if ev[0] == "abre" and ev[1].tag in TITULOS]
    return min(niveis, default=1)


def idiomas_instalados():
    try:
        saida = comando(["tesseract", "--list-langs"])
    except FileNotFoundError:
        raise SystemExit("ERRO: o Tesseract não está instalado -- veja \"Antes da primeira vez\" no README dos scripts")
    return {l.strip() for l in saida.split("\n")[1:] if l.strip()}


def idioma_do_ocr(arvore, escolhido):
    """O idioma do texto das imagens, no codigo do Tesseract: o escolhido com --idioma ou,
    sem ele, o que o documento declara (lang ou xml:lang do elemento html), pela tabela da
    ISO 639 (normas/idiomas.json). None se nao ha nenhum dos dois."""
    if escolhido:
        return escolhido
    html = next((f for f in arvore.filhos if not isinstance(f, str) and f.tag == "html"), None)
    codigo = lingua(html.attrs.get("lang") or html.attrs.get("xml:lang")) if html else None
    if not codigo:
        return None
    tabela, erros = le_dados(ARQUIVO_IDIOMAS, esquema("idiomas"))
    if erros:
        raise SystemExit("\n".join(f"ERRO em {e}" for e in erros))
    return tabela["iso_639_2"].get(codigo)


def leitor_de_figuras(documento, saida, idioma):
    """A funcao que monta o bloco de cada imagem: a marca com o caminho dela a partir da
    transcricao, o texto lido pelo Tesseract e o fim da imagem."""
    conferido = []

    def figura(src, aviso):
        partes = urlsplit(src)
        arquivo = (documento.parent / unquote(partes.path)).resolve() if src and not partes.scheme else None
        if arquivo is None or not arquivo.is_file():
            aviso(f"a imagem {src or '(sem endereço)'} não está na cópia da fonte: ficou sem o texto dela")
            return [FIGURA.format(alvo_markdown(src)), FIM_FIGURA]
        if not conferido:
            if idioma is None:
                raise SystemExit(f"ERRO: {documento.name} não declara o idioma (lang), ou ele não está na tabela "
                                 f"{ARQUIVO_IDIOMAS.name}: diga o idioma do texto das imagens com --idioma")
            faltam = [i for i in idioma.split("+") if i not in idiomas_instalados()]
            if faltam:
                raise SystemExit("ERRO: o Tesseract não tem os dados do idioma " + ", ".join(faltam) + " -- no Linux: "
                                 + " ".join(f"sudo apt install tesseract-ocr-{i}" for i in faltam))
            conferido.append(True)
        lido = comando(["tesseract", str(arquivo), "stdout", "-l", idioma, "--psm", MODO_OCR]).replace("\f", "")
        caminho = Path(os.path.relpath(arquivo, saida.parent)).as_posix()
        return [FIGURA.format(alvo_markdown(caminho))] + [escapa(l.strip()) for l in lido.split("\n") if l.strip()] \
            + [FIM_FIGURA]

    return figura


def transcreve(documento, pasta, idioma, substituir):
    """Grava a transcricao do documento; devolve (caminho dela, se ela ja tinha o registro
    da fonte), ou None se ela ja existia e ficou como estava."""
    saida = pasta / f"{documento.stem}.md"
    registro = []
    if saida.exists():
        if not substituir:
            print(f"Já existe: {saida} (pode ter o texto das imagens conferido; pra fazer de novo por cima, use "
                  "--substituir)")
            return None
        registro, _ = separa_registro(saida.read_text(encoding="utf-8"))
    arvore = le_html(documento.read_text(encoding="utf-8"))
    t = Transcricao(nivel_mais_alto(arvore), leitor_de_figuras(documento, saida, idioma_do_ocr(arvore, idioma)))
    for ev in percorre(arvore):
        t.evento(ev)
    texto, avisos, paginas = t.texto_final()
    if not any(p.rotulo is not None for p in paginas_html(documento.read_text(encoding="utf-8"))):
        print(f"CONFERIR: {documento.name} não tem nenhuma marca de página: a transcrição ficou numa página só, "
              "\"p. ?\"")
    saida.parent.mkdir(parents=True, exist_ok=True)
    saida.write_text("\n".join(["---"] + registro + ["---", "", ""] if registro else []) + texto, encoding="utf-8")
    print(f"{saida}: {paginas} página(s), {texto.count(FIM_FIGURA)} imagem(ns)")
    for rotulo, aviso in avisos:
        print(f"CONFERIR: {saida.name}, {rotulo}: {aviso}")
    return saida, bool(registro)


# ---------- captura do navegador (.har) ----------

def respostas_da_captura(har):
    """{caminho no site: [(endereco, conteudo em bytes, tipo)]} de cada resposta com
    conteudo. Da captura sai so o endereco pedido e o conteudo da resposta: nunca os
    cabecalhos nem os cookies."""
    try:
        entradas = json.loads(Path(har).read_text(encoding="utf-8"))["log"]["entries"]
    except (ValueError, KeyError, TypeError) as e:
        raise SystemExit(f"ERRO: {har} não é uma captura HAR que dê pra ler ({e})")
    out = {}
    for e in entradas:
        url = e.get("request", {}).get("url", "")
        conteudo = e.get("response", {}).get("content", {}) or {}
        texto = conteudo.get("text")
        if not url or not texto:
            continue
        dados = base64.b64decode(texto) if conteudo.get("encoding") == "base64" else texto.encode("utf-8")
        caminho = posixpath.normpath(unquote(urlsplit(url).path))
        out.setdefault(caminho, []).append((url, dados, conteudo.get("mimeType", "")))
    return out


def referencias(texto):
    """Os enderecos para onde o documento aponta e que fazem parte dele: as imagens e os
    estilos."""
    out, pilha = [], [le_html(texto)]
    while pilha:
        no = pilha.pop()
        if no.tag == "img" and no.attrs.get("src"):
            out.append(no.attrs["src"])
        if no.tag == "link" and "stylesheet" in no.attrs.get("rel", "").split() and no.attrs.get("href"):
            out.append(no.attrs["href"])
        pilha += [f for f in reversed(no.filhos) if not isinstance(f, str)]
    return out


def documentos_da_captura(respostas, filtro):
    """([(caminho, endereco, conteudo)], erros): os documentos HTML com marca de pagina."""
    docs, erros = [], []
    for caminho, versoes in sorted(respostas.items()):
        if filtro and caminho != filtro and not caminho.endswith("/" + filtro):
            continue
        com_marcas = {}
        for url, dados, tipo in versoes:
            if "html" not in tipo and not caminho.lower().endswith(EXTENSOES_HTML):
                continue
            texto = dados.decode("utf-8", errors="replace")
            if any(p.rotulo is not None for p in paginas_html(texto)):
                com_marcas.setdefault(dados, url)
        if len(com_marcas) > 1:
            erros.append(f"a captura tem {len(com_marcas)} versões diferentes de {caminho} com marca de página; nada "
                         "foi copiado dele")
        elif com_marcas:
            (dados, url), = com_marcas.items()
            docs.append((caminho, url, dados))
    return docs, erros


def copia(caminho, url, dados, respostas, pasta):
    """Grava o documento e as imagens e estilos dele na pasta, na disposicao do site;
    devolve (documento gravado, avisos, erros). Arquivo que ja existe com outro conteudo
    nao e trocado: e erro, e nada do documento e gravado."""
    arquivos, avisos = {caminho: dados}, []
    for ref in referencias(dados.decode("utf-8", errors="replace")):
        alvo = posixpath.normpath(unquote(urlsplit(urljoin(url, ref)).path))
        if alvo in respostas:
            arquivos.setdefault(alvo, respostas[alvo][0][1])
        else:
            avisos.append(f"{ref} não está na captura")
    base = posixpath.commonpath([posixpath.dirname(c) for c in arquivos])
    destinos = {pasta / posixpath.relpath(c, base): d for c, d in arquivos.items()}
    erros = [f"{d} já existe com outro conteúdo; nada de {posixpath.basename(caminho)} foi copiado"
             for d, conteudo in destinos.items() if d.exists() and d.read_bytes() != conteudo]
    if not erros:
        for d, conteudo in destinos.items():
            if not d.exists():
                d.parent.mkdir(parents=True, exist_ok=True)
                d.write_bytes(conteudo)
    return pasta / posixpath.relpath(caminho, base), avisos, erros


def main(argv=None):
    p = argparse.ArgumentParser(description="Transcreve uma fonte em HTML com as páginas impressas marcadas.")
    p.add_argument("origem", type=Path, help="o documento (.xhtml, .html, .htm) ou a captura do navegador (.har)")
    p.add_argument("--pasta", type=Path,
                   help="com captura: a pasta, dentro da pasta protegida, onde fica a copia dos documentos")
    p.add_argument("--documento", help="com captura: so o documento com este nome, ou com este fim de caminho")
    p.add_argument("--idioma",
                   help="idioma do texto das imagens, no codigo do Tesseract (varios juntos: spa+eng); sem ele, vale "
                        "o que o documento declara")
    p.add_argument("--substituir", action="store_true",
                   help="faz de novo por cima da transcricao que ja existe (o registro da fonte continua)")
    p.add_argument("--projeto", type=Path, help="projeto.json (padrao: o primeiro achado subindo a partir daqui)")
    a = p.parse_args(argv)
    if not a.origem.is_file():
        raise SystemExit(f"fonte nao encontrada: {a.origem}")
    projeto = acha_projeto(a.projeto)
    protegida = projeto.caminho("material_base")
    erros = []
    if a.origem.suffix.lower() == ".har":
        if a.pasta is None:
            raise SystemExit("ERRO: com uma captura, diga com --pasta onde fica a cópia, dentro da pasta protegida")
        if not dentro(a.pasta, protegida):
            raise SystemExit(f"ERRO: a pasta da cópia tem de ficar dentro da pasta protegida, {protegida}")
        respostas = respostas_da_captura(a.origem)
        docs, erros = documentos_da_captura(respostas, a.documento)
        documentos = []
        for caminho, url, dados in docs:
            documento, avisos, erros_doc = copia(caminho, url, dados, respostas, a.pasta)
            erros += erros_doc
            for aviso in avisos:
                print(f"CONFERIR: {posixpath.basename(caminho)}: {aviso}")
            if not erros_doc:
                documentos.append(documento)
        if not docs and not erros:
            erros.append(f"a captura não tem nenhum documento com marca de página"
                         + (f" com o nome {a.documento}" if a.documento else ""))
    elif a.origem.suffix.lower() in EXTENSOES_HTML:
        if not dentro(a.origem, protegida):
            raise SystemExit("ERRO: a fonte precisa ficar na pasta protegida, com as imagens dela, antes de ser "
                             f"transcrita: leve a pasta dela inteira pra {protegida}")
        documentos = [a.origem]
    else:
        raise SystemExit(f"ERRO: {a.origem.name} não é HTML (.xhtml, .html, .htm) nem captura (.har)")

    relativo = lambda c: Path(os.path.relpath(Path(c).resolve(), projeto.raiz)).as_posix()  # noqa: E731
    for documento in documentos:
        feito = transcreve(documento, projeto.caminho("gerados"), a.idioma, a.substituir)
        if feito and not feito[1]:
            print(f"FALTA: registrar de qual arquivo a transcrição veio: python scripts/registrar_fonte.py "
                  f"{relativo(feito[0])} {relativo(documento)} [chave]")
    for erro in erros:
        print(f"ERRO: {erro}")
    if a.origem.suffix.lower() == ".har" and documentos:
        print(f"A captura {a.origem.name} guarda os dados da sua sessão no site (os cookies): com a cópia feita, "
              "apague-a.")
    return 1 if erros else 0


if __name__ == "__main__":
    sys.exit(main())
