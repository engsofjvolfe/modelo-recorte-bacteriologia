# SPDX-License-Identifier: GPL-3.0-or-later
# Copyright do codigo sob GPL-3.0 -- ver LICENSE e NOTICE.md na raiz do projeto.

"""
Transcreve uma apresentacao de slides em pptx e grava na pasta das transcricoes (no
projeto.json, "gerados") no padrao da secao 1 da metodologia: uma secao por slide, com o
titulo "## slide <posicao> (arquivo p. <posicao>)" -- o slide nao tem numero impresso, e
a citacao usa a posicao dele no arquivo. O texto e o do proprio arquivo, copiado sem
leitura nenhuma (comum.Apresentacao); so o texto de dentro das imagens e lido, por OCR.

Como o slide vira texto (os blocos na ordem do arquivo, que e a ordem em que o PowerPoint
os le em voz alta, separados por uma linha em branco):
  - titulo do slide (o espaco reservado de titulo): com "### ";
  - paragrafo: uma linha, com os espacos juntados; a quebra de linha dentro dele abre
    outra. O paragrafo com marcador leva "- ", ou o numero na lista numerada, recuado dois
    espacos por nivel; o marcador que o paragrafo nao diz vem do layout e do mestre;
  - tabela: tabela Markdown, com a primeira linha de cabecalho; numa celula, os paragrafos
    se separam com "<br>"; a celula mesclada fica com o texto na primeira e as outras
    vazias, como no proprio arquivo;
  - SmartArt: o texto de cada forma dele, como um paragrafo;
  - indice e expoente: com os caracteres Unicode (CO₂, 10⁻⁶); sem o caractere, o texto
    fica na linha, e o script avisa;
  - caractere de uma fonte de simbolos (como a Symbol): o do Unicode, pela tabela em
    normas/simbolos.json;
  - imagem (a de fundo do slide primeiro; e a de previa de um objeto incorporado):
    "![imagem](caminho)", seguida do texto escrito dentro dela, lido pelo Tesseract (um
    pedaco por linha), e de "[fim da imagem]", mesmo sem texto. A imagem que o Tesseract
    nao le (EMF, WMF, SVG...) passa antes pro PNG pelo LibreOffice. A imagem recortada no
    slide e lida inteira, e o script avisa;
  - notas do apresentador: depois do slide, a partir da linha "[notas do apresentador]";
  - slide oculto: "[slide oculto]" no comeco; slide sem texto nem imagem: "[sem texto]";
  - "#" no comeco da linha e "|" ficam escapados ("\\#", "\\|").
Grafico e objeto sem imagem de previa nao tem o texto lido: o script avisa, e eles
aparecem na imagem do slide inteiro, na conferencia.

As imagens saem do pptx pra uma pasta ao lado dele, com o nome dele sem a extensao, na
mesma disposicao de pastas de dentro do pacote; arquivo que ja existe com outro conteudo
nao e trocado: e erro, e nada e gravado.

Nao grava por cima de uma transcricao que ja existe -- o texto das imagens pode ja estar
conferido --, a nao ser com --substituir; nesse caso, o registro da fonte no topo dela
continua. Quando a apresentacao tem imagem, precisa do Tesseract com os dados do idioma
do texto delas, escolhido com --idioma ("por", "eng", "por+eng"...): o idioma que o pptx
marca no texto e o do corretor ortografico, nao serve pra isso.

Uso (de qualquer pasta dentro do projeto):
    python scripts/transcrever_pptx.py docs/material-base/AULA-1.pptx --idioma por
    python scripts/transcrever_pptx.py docs/material-base/AULA-1.pptx --idioma por+eng --substituir
"""

import argparse
import posixpath
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from comum import (EXTENSOES_PPTX, NOTAS, ROTULO_SLIDE, SEM_TEXTO, SLIDE_OCULTO, Apresentacao,  # noqa: E402
                   FonteIlegivel, acha_projeto, bloco_da_figura, confere_idioma_do_ocr, dentro, em_indice, escapa, grava_transcricao,
                   junta, lembra_registro, link, registro_da_transcricao, tabela_markdown, texto_da_imagem)


def linhas_do_paragrafo(paragrafo, aviso):
    """O texto de cada linha do paragrafo, com indice e expoente nos caracteres do Unicode."""
    out = []
    for linha in paragrafo.linhas:
        partes = []
        for texto, tipo in linha:
            if tipo:
                convertido = em_indice(tipo, texto)
                if convertido is None:
                    aviso(f"{'expoente' if tipo == 'sup' else 'índice'} sem caractere Unicode, ficou na linha: "
                          f"\"{junta([texto])}\"")
                else:
                    texto = convertido
            partes.append(texto)
        out.append(junta(partes))
    return [l for l in out if l]


def paragrafo_em_markdown(paragrafo, titulo, aviso):
    linhas = linhas_do_paragrafo(paragrafo, aviso)
    marcador = paragrafo.marcador
    com_marcador = [(marcador if i == 0 else " " * len(marcador)) + l for i, l in enumerate(linhas)]
    if titulo:
        return ["### " + escapa(l) for l in com_marcador]
    if marcador:
        return [escapa("  " * paragrafo.nivel + l) for l in com_marcador]
    return [escapa(l) for l in linhas]


def texto_em_markdown(paragrafos, titulo, aviso):
    """Os paragrafos, separados por uma linha em branco; os itens de lista seguidos, por uma
    quebra so, pra lista ficar inteira."""
    out, anterior_na_lista = "", False
    for p in paragrafos:
        linhas = paragrafo_em_markdown(p, titulo, aviso)
        if not linhas:
            continue
        na_lista = bool(p.marcador) and not titulo
        if out:
            out += "\n" if na_lista and anterior_na_lista else "\n\n"
        out += "\n".join(linhas)
        anterior_na_lista = na_lista
    return out


def tabela_em_markdown(linhas, aviso):
    celula = lambda ps: "<br>".join(  # noqa: E731
        (p.marcador if i == 0 else "") + l.replace("|", "\\|") for p in ps
        for i, l in enumerate(linhas_do_paragrafo(p, aviso)))
    grade = [[celula(c) for c in linha] for linha in linhas]
    colunas = max((len(l) for l in grade), default=0)
    if not colunas:
        return ""
    return tabela_markdown([l + [""] * (colunas - len(l)) for l in grade], colunas)


def imagens_da_apresentacao(slides):
    return list(dict.fromkeys(b.conteudo.parte for s in slides for b in s.blocos if b.tipo == "imagem"))


def tira_imagens(apresentacao, partes, pasta):
    """Grava cada imagem na pasta, na disposicao de dentro do pacote; devolve os erros: um
    arquivo que ja existe com outro conteudo nao e trocado, e nada e gravado."""
    destinos = {pasta / parte: apresentacao.bytes(parte) for parte in partes}
    erros = [f"{d} já existe com outro conteúdo; nada foi gravado" for d, conteudo in destinos.items()
             if d.exists() and d.read_bytes() != conteudo]
    if not erros:
        for d, conteudo in destinos.items():
            if not d.exists():
                d.parent.mkdir(parents=True, exist_ok=True)
                d.write_bytes(conteudo)
    return erros


def slide_em_markdown(slide, pasta, saida, ocr, aviso):
    blocos = []
    for bloco in slide.blocos:
        if bloco.tipo in ("titulo", "texto"):
            texto = texto_em_markdown(bloco.conteudo, bloco.tipo == "titulo", aviso)
        elif bloco.tipo == "tabela":
            texto = tabela_em_markdown(bloco.conteudo, aviso)
        else:
            arquivo = pasta / bloco.conteudo.parte
            linhas, problema = ocr(arquivo)
            if problema:
                aviso(problema)
            if bloco.conteudo.recortada:
                aviso(f"a imagem {posixpath.basename(bloco.conteudo.parte)} está recortada no slide: o OCR leu a "
                      "imagem inteira, inclusive o que o slide não mostra")
            texto = "\n".join(bloco_da_figura(link(arquivo, saida), linhas))
        if texto:
            blocos.append(texto)
    if slide.notas:
        blocos += [NOTAS, texto_em_markdown(slide.notas, False, aviso)]
    return "\n\n".join(([SLIDE_OCULTO] if slide.oculto else []) + (blocos or [SEM_TEXTO]))


def transcreve(origem, gerados, idioma, substituir):
    """Grava a transcricao da apresentacao; devolve (caminho dela, se ela ja tinha o registro
    da fonte), ou None se ela ja existia e ficou como estava."""
    saida = gerados / f"{origem.stem}.md"
    registro = registro_da_transcricao(saida, substituir)
    if registro is None:
        return None
    try:
        apresentacao = Apresentacao(origem)
    except FonteIlegivel as e:
        raise SystemExit(f"ERRO: {e}")
    slides = apresentacao.slides()
    partes = imagens_da_apresentacao(slides)
    if partes:
        if not idioma:
            raise SystemExit(f"ERRO: {origem.name} tem imagem: diga com --idioma o idioma do texto delas, no código do "
                             "Tesseract (por, eng, por+eng...)")
        confere_idioma_do_ocr(idioma)
    pasta = origem.parent / origem.stem
    erros = tira_imagens(apresentacao, partes, pasta)
    if erros:
        raise SystemExit("\n".join(f"ERRO: {erro}" for erro in erros))
    lidas = {}

    def ocr(arquivo):
        if arquivo not in lidas:
            lidas[arquivo] = texto_da_imagem(arquivo, idioma)
        return lidas[arquivo]

    texto, avisos, imagens = [], [], 0
    for slide in slides:
        do_slide = list(slide.avisos)
        corpo = slide_em_markdown(slide, pasta, saida, ocr, do_slide.append)
        imagens += sum(b.tipo == "imagem" for b in slide.blocos)
        rotulo = ROTULO_SLIDE.format(slide.numero)
        texto += [f"## {rotulo} (arquivo p. {slide.numero})", "", corpo, ""]
        avisos += [(rotulo, a) for a in dict.fromkeys(do_slide)]
    grava_transcricao(saida, registro, "\n".join(texto))
    print(f"{saida}: {len(slides)} slide(s), {imagens} imagem(ns)")
    for rotulo, aviso in avisos:
        print(f"CONFERIR: {saida.name}, {rotulo}: {aviso}")
    return saida, bool(registro)


def main(argv=None):
    p = argparse.ArgumentParser(description="Transcreve uma apresentação de slides em pptx.")
    p.add_argument("origem", type=Path, help="a apresentacao (" + ", ".join(EXTENSOES_PPTX) + ")")
    p.add_argument("--idioma",
                   help="idioma do texto das imagens, no codigo do Tesseract (varios juntos: por+eng); obrigatorio "
                        "quando a apresentacao tem imagem")
    p.add_argument("--substituir", action="store_true",
                   help="faz de novo por cima da transcricao que ja existe (o registro da fonte continua)")
    p.add_argument("--projeto", type=Path, help="projeto.json (padrao: o primeiro achado subindo a partir daqui)")
    a = p.parse_args(argv)
    if not a.origem.is_file():
        raise SystemExit(f"fonte nao encontrada: {a.origem}")
    if a.origem.suffix.lower() not in EXTENSOES_PPTX:
        raise SystemExit(f"ERRO: {a.origem.name} não é apresentação em pptx (" + ", ".join(EXTENSOES_PPTX) + ")")
    projeto = acha_projeto(a.projeto)
    protegida = projeto.caminho("material_base")
    if not dentro(a.origem, protegida):
        raise SystemExit(f"ERRO: a fonte precisa ficar na pasta protegida antes de ser transcrita: leve-a pra {protegida}")
    feito = transcreve(a.origem, projeto.caminho("gerados"), a.idioma, a.substituir)
    if feito and not feito[1]:
        lembra_registro(projeto, feito[0], a.origem)
    return 0


if __name__ == "__main__":
    sys.exit(main())
