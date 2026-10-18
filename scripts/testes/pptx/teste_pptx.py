# SPDX-License-Identifier: GPL-3.0-or-later
# Copyright do codigo sob GPL-3.0 -- ver LICENSE e NOTICE.md na raiz do projeto.

"""Testes do leitor de pptx (comum.Apresentacao), do transcrever_pptx.py e da conferencia de
pptx, com apresentacoes inventadas, montadas aqui. Uso:
    python3 -I teste_pptx.py <pasta dos scripts> <pasta de trabalho nova>
"""
import io
import json
import os
import re
import shutil
import struct
import subprocess
import sys
import zipfile
import zlib
from pathlib import Path
from urllib.parse import unquote

SCRIPTS, TRABALHO = Path(sys.argv[1]).resolve(), Path(sys.argv[2]).resolve()
sys.path.insert(0, str(SCRIPTS))
import comum  # noqa: E402

NS = ('xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main" '
      'xmlns:p="http://schemas.openxmlformats.org/presentationml/2006/main" '
      'xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships"')
REL = "http://schemas.openxmlformats.org/officeDocument/2006/relationships/"
FALHAS = []


def confere(nome, obtido, esperado):
    if obtido != esperado:
        FALHAS.append(nome)
        print(f"FALHOU {nome}:\n  obtido:   {obtido!r}\n  esperado: {esperado!r}")


def png(largura=4, altura=4, cor=(200, 30, 30)):
    linha = b"\x00" + bytes(cor) * largura
    bloco = lambda tipo, dados: struct.pack(">I", len(dados)) + tipo + dados + struct.pack(  # noqa: E731
        ">I", zlib.crc32(tipo + dados) & 0xFFFFFFFF)
    return (b"\x89PNG\r\n\x1a\n" + bloco(b"IHDR", struct.pack(">IIBBBBB", largura, altura, 8, 2, 0, 0, 0))
            + bloco(b"IDAT", zlib.compress(linha * altura)) + bloco(b"IEND", b""))


def bmp(largura, altura, cor):
    linha = bytes(cor[::-1]) * largura + b"\x00" * (-3 * largura % 4)
    dados = linha * altura
    return (b"BM" + struct.pack("<IHHI", 54 + len(dados), 0, 0, 54)
            + struct.pack("<IiiHHIIiiII", 40, largura, altura, 1, 24, 0, len(dados), 2835, 2835, 0, 0) + dados)


def emf(retangulo):
    """Um desenho EMF: o retangulo (esquerda, topo, direita, base) preto, com a mesma margem dos dois lados, que o
    GraphicsMagick nao le e o LibreOffice desenha numa folha."""
    registro = lambda tipo, dados: struct.pack("<II", tipo, 8 + len(dados)) + dados  # noqa: E731
    corpo = (registro(37, struct.pack("<I", 0x80000004)) + registro(43, struct.pack("<4i", *retangulo))
             + registro(14, struct.pack("<III", 0, 16, 20)))
    limites = (0, 0, retangulo[2] + retangulo[0], retangulo[3] + retangulo[1])
    cabecalho = registro(1, struct.pack("<4i", *limites) + struct.pack("<4i", *(round(x * 2540 / 96) for x in limites))
                         + struct.pack("<IIIIHHIIIiiii", 0x464D4520, 0x10000, 0, 4, 1, 0, 0, 0, 0, 1024, 768, 270, 203))
    tudo = cabecalho + corpo
    return tudo[:48] + struct.pack("<I", len(tudo)) + tudo[52:]


def rels(itens):
    return ('<?xml version="1.0" encoding="UTF-8"?><Relationships '
            'xmlns="http://schemas.openxmlformats.org/package/2006/relationships">'
            + "".join(f'<Relationship Id="{i}" Type="{t if "/" in t else REL + t}" Target="{alvo}"'
                      + (' TargetMode="External"' if externo else "") + "/>" for i, t, alvo, externo in itens)
            + "</Relationships>")


def corpo(paragrafos, estilo=""):
    return f"<p:txBody><a:bodyPr/><a:lstStyle>{estilo}</a:lstStyle>{paragrafos}</p:txBody>"


def forma(paragrafos, ph=None, estilo=""):
    nv = f'<p:nvPr><p:ph {ph}/></p:nvPr>' if ph else "<p:nvPr/>"
    return f'<p:sp><p:nvSpPr><p:cNvPr id="2" name="f"/><p:cNvSpPr/>{nv}</p:nvSpPr><p:spPr/>{corpo(paragrafos, estilo)}</p:sp>'


def par(texto, lvl=None, ppr="", runs=None):
    atributo = f' lvl="{lvl}"' if lvl is not None else ""
    conteudo = runs if runs is not None else f"<a:r><a:t>{texto}</a:t></a:r>"
    return f"<a:p><a:pPr{atributo}>{ppr}</a:pPr>{conteudo}</a:p>"


def figura(rid, recorte=""):
    return (f'<p:pic><p:nvPicPr><p:cNvPr id="3" name="i" descr="nome-do-arquivo.png"/><p:cNvPicPr/><p:nvPr/></p:nvPicPr>'
            f'<p:blipFill><a:blip r:embed="{rid}"/>{recorte}<a:stretch/></p:blipFill><p:spPr/></p:pic>')


def slide(formas, extra_raiz="", fundo=""):
    return (f'<?xml version="1.0" encoding="UTF-8"?><p:sld {NS} {extra_raiz}><p:cSld>{fundo}<p:spTree>'
            f'<p:nvGrpSpPr><p:cNvPr id="1" name=""/><p:cNvGrpSpPr/><p:nvPr/></p:nvGrpSpPr><p:grpSpPr/>'
            f"{formas}</p:spTree></p:cSld></p:sld>")


def apresentacao(caminho, slides, mestre_corpo, padrao="", partes_extras=None):
    """slides: [(nome da parte, xml, [(id, tipo, alvo, externo)])], na ordem da apresentacao."""
    z = zipfile.ZipFile(caminho, "w")
    z.writestr("[Content_Types].xml",
               '<?xml version="1.0" encoding="UTF-8"?><Types xmlns="http://schemas.openxmlformats.org/package/2006/'
               'content-types"><Default Extension="xml" ContentType="application/xml"/><Default Extension="rels" '
               'ContentType="application/vnd.openxmlformats-package.relationships+xml"/><Default Extension="png" '
               'ContentType="image/png"/><Default Extension="bmp" ContentType="image/bmp"/><Default Extension="emf" '
               'ContentType="image/x-emf"/><Override PartName="/ppt/presentation.xml" ContentType="application/'
               'vnd.openxmlformats-officedocument.presentationml.presentation.main+xml"/></Types>')
    z.writestr("_rels/.rels", rels([("rId1", "officeDocument", "ppt/presentation.xml", False)]))
    ids = "".join(f'<p:sldId id="{256 + k}" r:id="rS{k}"/>' for k in range(len(slides)))
    z.writestr("ppt/presentation.xml",
               f'<?xml version="1.0" encoding="UTF-8"?><p:presentation {NS}><p:sldMasterIdLst><p:sldMasterId '
               f'id="2147483648" r:id="rM"/></p:sldMasterIdLst><p:sldIdLst>{ids}</p:sldIdLst>'
               f'<p:sldSz cx="9144000" cy="6858000"/><p:notesSz cx="6858000" cy="9144000"/>'
               f"<p:defaultTextStyle>{padrao}</p:defaultTextStyle></p:presentation>")
    z.writestr("ppt/_rels/presentation.xml.rels", rels(
        [("rM", "slideMaster", "slideMasters/slideMaster1.xml", False)]
        + [(f"rS{k}", "slide", f"slides/{nome}", False) for k, (nome, _, _) in enumerate(slides)]))
    z.writestr("ppt/slideMasters/slideMaster1.xml",
               f'<?xml version="1.0" encoding="UTF-8"?><p:sldMaster {NS}><p:cSld><p:spTree><p:nvGrpSpPr>'
               f'<p:cNvPr id="1" name=""/><p:cNvGrpSpPr/><p:nvPr/></p:nvGrpSpPr><p:grpSpPr/>'
               f'{forma("", ph="type=\"title\"")}{forma("", ph="type=\"body\" idx=\"1\"")}</p:spTree></p:cSld>'
               f'<p:sldLayoutIdLst><p:sldLayoutId id="2147483649" r:id="rL"/></p:sldLayoutIdLst>'
               f"<p:txStyles><p:titleStyle><a:lvl1pPr><a:buNone/></a:lvl1pPr></p:titleStyle>"
               f"<p:bodyStyle>{mestre_corpo}</p:bodyStyle><p:otherStyle/></p:txStyles></p:sldMaster>")
    z.writestr("ppt/slideMasters/_rels/slideMaster1.xml.rels",
               rels([("rL", "slideLayout", "../slideLayouts/slideLayout1.xml", False)]))
    z.writestr("ppt/slideLayouts/slideLayout1.xml",
               f'<?xml version="1.0" encoding="UTF-8"?><p:sldLayout {NS}><p:cSld><p:spTree><p:nvGrpSpPr>'
               f'<p:cNvPr id="1" name=""/><p:cNvGrpSpPr/><p:nvPr/></p:nvGrpSpPr><p:grpSpPr/>'
               f'{forma("", ph="type=\"title\"")}{forma("", ph="idx=\"1\"")}</p:spTree></p:cSld></p:sldLayout>')
    z.writestr("ppt/slideLayouts/_rels/slideLayout1.xml.rels",
               rels([("rM", "slideMaster", "../slideMasters/slideMaster1.xml", False)]))
    for nome, xml, relacoes in slides:
        z.writestr(f"ppt/slides/{nome}", xml)
        z.writestr(f"ppt/slides/_rels/{nome}.rels",
                   rels([("rL", "slideLayout", "../slideLayouts/slideLayout1.xml", False)] + relacoes))
    for parte, dados in (partes_extras or {}).items():
        z.writestr(parte, dados)
    z.close()


# ---------- a apresentacao inventada ----------

MESTRE = ('<a:lvl1pPr><a:buChar char="•"/></a:lvl1pPr><a:lvl2pPr><a:buChar char="–"/></a:lvl2pPr>'
          '<a:lvl3pPr><a:buChar char="»"/></a:lvl3pPr>')
S = []
# slide A (a parte se chama slide9.xml: a ordem e a da apresentacao, nao a do nome)
S.append(("slide9.xml", slide(
    forma(par("Ciclo da água"), ph='type="title"')
    + forma(par("Evaporação") + par("Mares e lagos", lvl=1) + par("") + par("Sem marcador", ppr="<a:buNone/>")
            + par("Condensação"), ph='idx="1"')
    + forma(par("# começa com cerquilha | e barra"))), []))
# slide B: numeracao, simbolos, indice e expoente, quebra de linha
S.append(("slide2.xml", slide(
    forma(par("terceiro", ppr='<a:buAutoNum type="alphaLcParenR" startAt="3"/>')
          + par("quarto", ppr='<a:buAutoNum type="alphaLcParenR" startAt="3"/>')
          + par("dentro", lvl=1, ppr='<a:buAutoNum type="romanUcPeriod"/>')
          + par("quinto", ppr='<a:buAutoNum type="alphaLcParenR" startAt="3"/>')
          + par("outro esquema", ppr='<a:buAutoNum type="circleNumDbPlain"/>'))
    + forma(par(None, runs='<a:r><a:rPr><a:sym typeface="Symbol"/></a:rPr><a:t>m e </a:t></a:r>'
                           '<a:r><a:rPr><a:latin typeface="Symbol"/></a:rPr><a:t>a</a:t></a:r>'
                           '<a:r><a:rPr><a:sym typeface="Wingdings"/></a:rPr><a:t></a:t></a:r>'))
    + forma(par(None, runs='<a:r><a:t>10</a:t></a:r><a:r><a:rPr baseline="30000"/><a:t>-6</a:t></a:r>'
                           '<a:r><a:t> e CO</a:t></a:r><a:r><a:rPr baseline="-25000"/><a:t>2</a:t></a:r>'
                           '<a:r><a:t> marca</a:t></a:r><a:r><a:rPr baseline="30000"/><a:t>®</a:t></a:r>'))
    + forma(par(None, runs='<a:r><a:t>linha um</a:t></a:r><a:br/><a:r><a:t>linha dois</a:t></a:r>'))), []))
# slide C: tabela, grupo, imagens, objeto incorporado, grafico, SmartArt
TABELA = ('<p:graphicFrame><p:nvGraphicFramePr><p:cNvPr id="4" name="t"/><p:cNvGraphicFramePr/><p:nvPr/>'
          '</p:nvGraphicFramePr><p:xfrm/><a:graphic><a:graphicData uri="http://schemas.openxmlformats.org/'
          'drawingml/2006/table"><a:tbl><a:tblGrid><a:gridCol w="1"/><a:gridCol w="1"/><a:gridCol w="1"/></a:tblGrid>'
          '<a:tr h="1"><a:tc gridSpan="2"><a:txBody><a:bodyPr/><a:p><a:r><a:t>Juntas</a:t></a:r></a:p></a:txBody></a:tc>'
          '<a:tc hMerge="1"><a:txBody><a:bodyPr/><a:p><a:endParaRPr/></a:p></a:txBody></a:tc>'
          '<a:tc><a:txBody><a:bodyPr/><a:p><a:r><a:t>C</a:t></a:r></a:p></a:txBody></a:tc></a:tr>'
          '<a:tr h="1"><a:tc><a:txBody><a:bodyPr/><a:p><a:r><a:t>a|b</a:t></a:r></a:p>'
          '<a:p><a:r><a:t>segundo</a:t></a:r></a:p></a:txBody></a:tc>'
          '<a:tc><a:txBody><a:bodyPr/><a:p><a:r><a:t>H</a:t></a:r><a:r><a:rPr baseline="-25000"/><a:t>2</a:t>'
          '</a:r></a:p></a:txBody></a:tc></a:tr></a:tbl></a:graphicData></a:graphic></p:graphicFrame>')
OLE = ('<p:graphicFrame><p:nvGraphicFramePr><p:cNvPr id="5" name="o"/><p:cNvGraphicFramePr/><p:nvPr/>'
       '</p:nvGraphicFramePr><p:xfrm/><a:graphic><a:graphicData uri="http://schemas.openxmlformats.org/'
       'presentationml/2006/ole"><mc:AlternateContent xmlns:mc="http://schemas.openxmlformats.org/markup-'
       'compatibility/2006"><mc:Choice xmlns:v="urn:schemas-microsoft-com:vml" Requires="v"><p:oleObj spid="x" '
       'r:id="rO"><p:embed/></p:oleObj></mc:Choice><mc:Fallback><p:oleObj r:id="rO"><p:embed/>'
       f'{figura("rI3")}</p:oleObj></mc:Fallback></mc:AlternateContent></a:graphicData></a:graphic>'
       '</p:graphicFrame>')
GRAFICO = ('<p:graphicFrame><p:nvGraphicFramePr><p:cNvPr id="6" name="g"/><p:cNvGraphicFramePr/><p:nvPr/>'
           '</p:nvGraphicFramePr><p:xfrm/><a:graphic><a:graphicData uri="http://schemas.openxmlformats.org/'
           'drawingml/2006/chart"/></a:graphic></p:graphicFrame>')
SMART = ('<p:graphicFrame><p:nvGraphicFramePr><p:cNvPr id="7" name="d"/><p:cNvGraphicFramePr/><p:nvPr/>'
         '</p:nvGraphicFramePr><p:xfrm/><a:graphic><a:graphicData uri="http://schemas.openxmlformats.org/'
         'drawingml/2006/diagram"><dgm:relIds xmlns:dgm="http://schemas.openxmlformats.org/drawingml/2006/'
         'diagram" r:dm="{dm}" r:lo="x" r:qs="x" r:cs="x"/></a:graphicData></a:graphic></p:graphicFrame>')
DADOS = ('<?xml version="1.0" encoding="UTF-8"?><dgm:dataModel xmlns:dgm="http://schemas.openxmlformats.org/'
         'drawingml/2006/diagram" xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main"><dgm:ptLst>'
         '<dgm:pt modelId="1" type="doc"><dgm:t><a:bodyPr/><a:p><a:r><a:t>documento</a:t></a:r></a:p></dgm:t>'
         '</dgm:pt><dgm:pt modelId="2"><dgm:t><a:bodyPr/><a:p><a:r><a:t>Nó de dados</a:t></a:r></a:p></dgm:t>'
         '</dgm:pt></dgm:ptLst>{ext}</dgm:dataModel>')
DESENHO = ('<?xml version="1.0" encoding="UTF-8"?><dsp:drawing xmlns:dsp="http://schemas.microsoft.com/office/'
           'drawing/2008/diagram" xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main"><dsp:spTree>'
           '<dsp:sp><dsp:txBody><a:bodyPr/><a:p><a:r><a:t>Etapa 1</a:t></a:r></a:p></dsp:txBody></dsp:sp>'
           '<dsp:sp><dsp:txBody><a:bodyPr/><a:p><a:r><a:t>Etapa 2</a:t></a:r></a:p></dsp:txBody></dsp:sp>'
           '</dsp:spTree></dsp:drawing>')
EXT = ('<dgm:extLst><a:ext uri="x"><dsp:dataModelExt xmlns:dsp="http://schemas.microsoft.com/office/drawing/2008/'
       'diagram" relId="rD"/></a:ext></dgm:extLst>')
GRUPO = ('<p:grpSp><p:nvGrpSpPr><p:cNvPr id="8" name="g"/><p:cNvGrpSpPr/><p:nvPr/></p:nvGrpSpPr><p:grpSpPr/>'
         f'{forma(par("no grupo"))}{figura("rI2", recorte="<a:srcRect l=\"10000\"/>")}</p:grpSp>')
FUNDO = '<p:bg><p:bgPr><a:blipFill><a:blip r:embed="rI1"/></a:blipFill></p:bgPr></p:bg>'
S.append(("slide3.xml", slide(TABELA + GRUPO + OLE + GRAFICO + SMART.format(dm="rDm1") + figura("rX")
                              + SMART.format(dm="rDm2"), fundo=FUNDO),
          [("rI1", "image", "../media/fundo.png", False), ("rI2", "image", "../media/foto.png", False),
           ("rI3", "image", "../media/previa.png", False), ("rO", "oleObject", "../embeddings/o.bin", False),
           ("rDm1", "diagramData", "../diagrams/data1.xml", False),
           ("rD", "http://schemas.microsoft.com/office/2007/relationships/diagramDrawing", "../diagrams/drawing1.xml",
            False), ("rDm2", "diagramData", "../diagrams/data2.xml", False),
           ("rX", "image", "http://exemplo.invalido/imagem.png", True)]))
# slide D: oculto, com notas; slide E: vazio
NOTAS = (f'<?xml version="1.0" encoding="UTF-8"?><p:notes {NS}><p:cSld><p:spTree><p:nvGrpSpPr><p:cNvPr id="1" '
         f'name=""/><p:cNvGrpSpPr/><p:nvPr/></p:nvGrpSpPr><p:grpSpPr/>{forma(par("4"), ph="type=\"sldNum\"")}'
         f'{forma(par("Lembrar do exemplo"), ph="type=\"body\" idx=\"1\"")}</p:spTree></p:cSld></p:notes>')
S.append(("slide4.xml", slide(forma(par("Escondido")), extra_raiz='show="0"'),
          [("rN", "notesSlide", "../notesSlides/notesSlide1.xml", False)]))
S.append(("slide5.xml", slide(""), []))

TRABALHO.mkdir(parents=True)
base = TRABALHO / "docs" / "material-base"
base.mkdir(parents=True)
shutil.copy(SCRIPTS.parent / "modelo-dados" / "projeto.json", TRABALHO / "projeto.json")
arquivo = base / "aula-inventada.pptx"
apresentacao(arquivo, S, MESTRE, partes_extras={
    "ppt/media/fundo.png": png(cor=(10, 10, 10)), "ppt/media/foto.png": png(), "ppt/media/previa.png": png(cor=(0, 90, 0)),
    "ppt/embeddings/o.bin": b"\x00", "ppt/diagrams/data1.xml": DADOS.format(ext=EXT),
    "ppt/diagrams/drawing1.xml": DESENHO, "ppt/diagrams/data2.xml": DADOS.format(ext=""),
    "ppt/notesSlides/notesSlide1.xml": NOTAS})

# ---------- o leitor ----------

ap = comum.Apresentacao(arquivo)
slides = ap.slides()
confere("numero de slides", len(slides), 5)
confere("ordem da apresentacao", comum.texto_do_slide(slides[0]).split("\n")[0], "Ciclo da água")
confere("oculto", [s.oculto for s in slides], [False, False, False, True, False])
confere("notas", [p.linhas for p in slides[3].notas], [[[("Lembrar do exemplo", None)]]])
confere("imagens na ordem", [b.conteudo.parte for b in slides[2].blocos if b.tipo == "imagem"],
        ["ppt/media/fundo.png", "ppt/media/foto.png", "ppt/media/previa.png"])
confere("recortada", [b.conteudo.recortada for b in slides[2].blocos if b.tipo == "imagem"], [False, True, False])
avisos = " | ".join(slides[2].avisos)
for trecho in ("gráfico", "link", "SmartArt sem o desenho"):
    confere(f"aviso: {trecho}", trecho in avisos, True)
try:
    ruim = TRABALHO / "ruim.pptx"
    ruim.write_bytes(arquivo.read_bytes()[:500])
    comum.Apresentacao(ruim)
    confere("pptx incompleto", "nao levantou", "FonteIlegivel")
except comum.FonteIlegivel:
    pass

# ---------- a transcricao ----------

r = subprocess.run([sys.executable, str(SCRIPTS / "transcrever_pptx.py"), str(arquivo), "--idioma", "eng"],
                   cwd=TRABALHO, capture_output=True, text=True)
print(r.stdout, r.stderr)
texto = (TRABALHO / "docs" / "material-base" / "gerados-ocr" / "aula-inventada.md").read_text(encoding="utf-8")
secoes = [s.rstrip("\n") + "\n" for s in texto.split("## slide ")[1:]]
confere("slide 1", secoes[0], "1 (arquivo p. 1)\n\n### Ciclo da água\n\n- Evaporação\n  - Mares e lagos\n\n"
        "Sem marcador\n\n- Condensação\n\n\\# começa com cerquilha \\| e barra\n")
confere("slide 2", secoes[1], "2 (arquivo p. 2)\n\nc) terceiro\nd) quarto\n  I. dentro\ne) quinto\n1. outro esquema\n\n"
        "μm e ±α\n\n10⁻⁶ e CO₂ marca®\n\nlinha um\nlinha dois\n")
pasta = "../aula-inventada/ppt/media"
confere("slide 3", secoes[2], f"3 (arquivo p. 3)\n\n![imagem]({pasta}/fundo.png)\n[fim da imagem]\n\n"
        "| Juntas |  | C |\n|---|---|---|\n| a\\|b<br>segundo | H₂ |  |\n\nno grupo\n\n"
        f"![imagem]({pasta}/foto.png)\n[fim da imagem]\n\n![imagem]({pasta}/previa.png)\n[fim da imagem]\n\n"
        "Etapa 1\n\nEtapa 2\n\nNó de dados\n")
confere("slide 4", secoes[3], "4 (arquivo p. 4)\n\n[slide oculto]\n\nEscondido\n\n[notas do apresentador]\n\n"
        "Lembrar do exemplo\n")
confere("slide 5", secoes[4], "5 (arquivo p. 5)\n\n[sem texto]\n")
for trecho in ("circleNumDbPlain", "U+F0E0", "expoente sem caractere Unicode", "recortada", "gráfico", "FALTA"):
    confere(f"saida: {trecho}", trecho in r.stdout, True)
confere("imagens tiradas", sorted(p.name for p in (base / "aula-inventada" / "ppt" / "media").iterdir()),
        ["foto.png", "fundo.png", "previa.png"])

# nao grava por cima; e imagem com outro conteudo e erro
r2 = subprocess.run([sys.executable, str(SCRIPTS / "transcrever_pptx.py"), str(arquivo), "--idioma", "eng"],
                    cwd=TRABALHO, capture_output=True, text=True)
confere("ja existe", "Já existe" in r2.stdout, True)
(base / "aula-inventada" / "ppt" / "media" / "foto.png").write_bytes(png(cor=(1, 2, 3)))
r3 = subprocess.run([sys.executable, str(SCRIPTS / "transcrever_pptx.py"), str(arquivo), "--idioma", "eng",
                     "--substituir"], cwd=TRABALHO, capture_output=True, text=True)
confere("conflito de imagem", (r3.returncode, "já existe com outro conteúdo" in r3.stderr), (1, True))
(base / "aula-inventada" / "ppt" / "media" / "foto.png").write_bytes(png())

# ---------- a conferencia ----------

transcricao = TRABALHO / "docs" / "material-base" / "gerados-ocr" / "aula-inventada.md"
reg = subprocess.run([sys.executable, str(SCRIPTS / "registrar_fonte.py"), str(transcricao), str(arquivo), "INVENTADA-1"],
                     cwd=TRABALHO, capture_output=True, text=True)
c = subprocess.run([sys.executable, str(SCRIPTS / "conferencia.py")], cwd=TRABALHO, capture_output=True, text=True)
print(c.stdout, c.stderr)
confere("conferencia sem erro", ("com erro do script: 0" in c.stdout, "ERRO" in c.stdout), (True, False))
mudado = transcricao.read_text(encoding="utf-8").replace("Mares e lagos", "Mares e rios")
transcricao.write_text(mudado, encoding="utf-8")
c = subprocess.run([sys.executable, str(SCRIPTS / "conferencia.py")], cwd=TRABALHO, capture_output=True, text=True)
confere("conferencia acha a diferenca", "o texto não é o da fonte" in c.stdout and "slide 1" in c.stdout, True)

# os links da conferencia, com espaco no nome da fonte: alvo que o Markdown aceita (entre <> se tem espaco) e
# arquivo que existe; e o tique fica quando a conferencia e gerada de novo


def alvos_da_conferencia(arquivo):
    """([alvo sem <>], [linha com alvo que o Markdown nao aceita]) dos links fora das cercas."""
    alvos, recusadas, dentro = [], [], False
    for linha in arquivo.read_text(encoding="utf-8").split("\n"):
        if linha == "````":
            dentro = not dentro
        elif not dentro:
            for pedaco in linha.split("](")[1:]:
                m = re.match(r"(?:<([^<>\n]+)>|([^\s<>()]+))\)", pedaco)
                if m:
                    alvos.append(m.group(1) or m.group(2))
                else:
                    recusadas.append(linha)
    return alvos, recusadas


def conferencia():
    return subprocess.run([sys.executable, str(SCRIPTS / "conferencia.py")], cwd=TRABALHO, capture_output=True,
                          text=True)


espacada = base / "aula com espaço.pptx"
shutil.copy(arquivo, espacada)
subprocess.run([sys.executable, str(SCRIPTS / "transcrever_pptx.py"), str(espacada), "--idioma", "eng"], cwd=TRABALHO,
               capture_output=True, text=True)
transcricao2 = transcricao.with_name("aula com espaço.md")
subprocess.run([sys.executable, str(SCRIPTS / "registrar_fonte.py"), str(transcricao2), str(espacada), "INVENTADA-2"],
               cwd=TRABALHO, capture_output=True, text=True)
c = conferencia()
saida = comum.acha_projeto(TRABALHO / "projeto.json").caminho("conferencia_imagens")
alvos, recusadas = alvos_da_conferencia(saida)
locais = [unquote(a.split("#")[0]) for a in alvos if a.split("#")[0]]
confere("links: o Markdown aceita todos", recusadas, [])
confere("links: com espaco, entre <>", any(" " in a for a in alvos), True)
confere("links: imagem do slide inteiro", any("aula com espaço-p001.png" in a for a in alvos), True)
confere("links: arquivos que existem", [a for a in locais if not (saida.parent / a).exists()], [])
marca_img = next(linha for linha in saida.read_text(encoding="utf-8").split("\n")
                 if linha.startswith("<!-- parte: aula com espaço|3.1|"))
antes, depois = saida.read_text(encoding="utf-8").split(marca_img)
saida.write_text(antes + marca_img + depois.replace("- [ ] IA", "- [x] IA", 1), encoding="utf-8")
c = conferencia()
bloco = saida.read_text(encoding="utf-8").split(marca_img)[1].split("<!-- parte:")[0]
confere("tique fica ao gerar de novo", ("- [x] IA" in bloco, "tique da IA: 1 " in c.stdout), (True, True))

# ---------- o texto das imagens corrigido no arquivo de conferencia (--levar-correcoes) ----------

transcricao.write_text(mudado.replace("Mares e rios", "Mares e lagos"), encoding="utf-8")  # desfaz a diferenca
for bruto in ("a|b", "#x", "\\#x", "c:\\|", "sem nada"):
    confere(f"escape volta: {bruto}", comum.escapa(comum.sem_escape(comum.escapa(bruto))), comum.escapa(bruto))


def leva():
    return subprocess.run([sys.executable, str(SCRIPTS / "conferencia.py"), "--levar-correcoes"], cwd=TRABALHO,
                          capture_output=True, text=True)


def limites(texto, grupo, parte):
    """(inicio, fim) do bloco da parte no arquivo de conferencia: da marca ate o titulo ou a marca seguinte."""
    inicio = texto.index(f"<!-- parte: {grupo}|{parte}|")
    fim = min([i + 1 for i in (texto.find("\n#", inicio), texto.find("\n<!-- parte:", inicio + 1)) if i >= 0]
              + [len(texto)])
    return inicio, fim


def bloco(grupo, parte):
    texto = saida.read_text(encoding="utf-8")
    inicio, fim = limites(texto, grupo, parte)
    return texto[inicio:fim]


def no_bloco(grupo, parte, trocar):
    texto = saida.read_text(encoding="utf-8")
    inicio, fim = limites(texto, grupo, parte)
    saida.write_text(texto[:inicio] + trocar(texto[inicio:fim]) + texto[fim:], encoding="utf-8")


G = "aula com espaço"
foto, previa = (f"![imagem](<../{G}/ppt/media/{n}.png>)\n" for n in ("foto", "previa"))
t2 = transcricao2.read_text(encoding="utf-8")
transcricao2.write_text(t2.replace(foto + "[fim", foto + "ij} lixo\nTexto erado\n\\#tag a\\|b\n[fim")
                        .replace(previa + "[fim", previa + "outro lixo\n[fim"), encoding="utf-8")
conferencia()
no_bloco(G, "3.2", lambda b: b.replace("- [ ] IA", "- [x] IA"))
no_bloco(G, "3.2", lambda b: b.replace("Texto erado", "Texto errado").replace("\\#tag a\\|b", "#tag a|b")
         .replace("- [ ] pessoa", "- [X] pessoa"))
no_bloco(G, "3.3", lambda b: re.sub(r"````\n.*?````\n", "", b, flags=re.S))
antes_t2 = transcricao2.read_text(encoding="utf-8")
r = leva()
print(r.stdout, r.stderr)
confere("leva: sem erro", (r.returncode, r.stdout.count("levado para a transcrição")), (0, 2))
confere("leva: a transcricao so muda no texto corrigido", transcricao2.read_text(encoding="utf-8"),
        antes_t2.replace("Texto erado", "Texto errado").replace("outro lixo\n", ""))
b2, b3 = bloco(G, "3.2"), bloco(G, "3.3")
confere("leva: imagem corrigida", ("Texto errado" in b2, "- [ ] IA" in b2, "- [x] pessoa" in b2), (True, True, True))
confere("leva: imagem sem texto", ("Texto da imagem: nenhum" in b3, "- [ ] pessoa" in b3), (True, True))
confere("leva: imagem sem correcao guarda o tique", "- [x] IA" in bloco(G, "3.1"), True)
conf_antes = saida.read_text(encoding="utf-8")
r = leva()
confere("leva de novo: nada a levar",
        (r.returncode, "levado" in r.stdout, saida.read_text(encoding="utf-8") == conf_antes), (0, False, True))
# um formatador de Markdown pode trocar a cerca que o script escreve por uma de 3 crases: a correcao vai igual, e o
# texto das outras imagens nao muda
saida.write_text("\n".join("```" if re.fullmatch(r"`{3,}", linha) else linha
                           for linha in saida.read_text(encoding="utf-8").split("\n")), encoding="utf-8")
no_bloco(G, "3.2", lambda b: b.replace("ij} lixo", "ij} lixo corrigido"))
antes_t2 = transcricao2.read_text(encoding="utf-8")
r = leva()
confere("leva: cerca de 3 crases, de um formatador", (r.returncode, transcricao2.read_text(encoding="utf-8")),
        (0, antes_t2.replace("ij} lixo", "ij} lixo corrigido")))

avulsa = transcricao.with_name("avulsa.md")


def recusa(nome, mexer, trecho):
    """Mexe no projeto, roda --levar-correcoes e confere que recusa sem gravar nada; depois desfaz."""
    guardados = {a: a.read_text(encoding="utf-8") for a in (saida, transcricao2, avulsa) if a.exists()}
    mexer()
    mexidos = {a: a.read_text(encoding="utf-8") for a in guardados}
    r = leva()
    confere(f"recusa: {nome}", (r.returncode, trecho in r.stdout, "nada foi gravado" in r.stdout,
                                all(a.read_text(encoding="utf-8") == m for a, m in mexidos.items())),
            (1, True, True, True))
    for a, texto in guardados.items():
        a.write_text(texto, encoding="utf-8")


recusa("nota no tique", lambda: no_bloco(G, "3.2", lambda b: b.replace("- [x] pessoa", "- [x] pessoa - nota")
                                         .replace("Texto errado", "Texto certo")), "não lê o tique")
recusa("cerca sem fim", lambda: no_bloco(G, "3.2", lambda b: b[:b.rindex("````")] + b[b.rindex("````") + 5:]),
       "não tem fim")
recusa("transcricao mudou depois", lambda: (
    transcricao2.write_text(transcricao2.read_text(encoding="utf-8").replace("Texto errado", "Texto mudado"),
                            encoding="utf-8"),
    no_bloco(G, "3.2", lambda b: b.replace("Texto errado", "Texto certo"))), "mudou na transcrição")
avulsa.write_text("## p. 1 (arquivo p. 1)\n\nTexto da página\n", encoding="utf-8")
conferencia()
r = leva()
confere("leva com pagina de PDF sem correcao", ("nada foi gravado" in r.stdout, "levado" in r.stdout), (False, False))
recusa("pagina de PDF", lambda: no_bloco("avulsa", "1", lambda b: b.replace("Texto da página", "Texto corrigido")),
       "página de PDF")

# ---------- a imagem que nao esta em PNG: copia em PNG, com o link para o original ----------


ALVO = r"\]\((?:<([^<>]+)>|([^\s()]+))\)"


def imagem_mostrada(grupo, parte):
    """O arquivo da imagem que o bloco mostra (Path() se nao mostra nenhuma)."""
    m = re.search(r"^!\[[^\]]*" + ALVO + "$", bloco(grupo, parte), re.M)
    return (saida.parent / unquote(m.group(1) or m.group(2))).resolve() if m else Path()


def links_do_bloco(grupo, parte):
    """Os arquivos para onde levam os links do bloco que nao sao imagem."""
    return [(saida.parent / unquote(m.group(1) or m.group(2))).resolve()
            for m in re.finditer(r"(?<!!)\[[^\]]*" + ALVO, bloco(grupo, parte))]


def png_lido(arquivo):
    """(largura, altura, tem transparencia) do cabecalho do PNG."""
    dados = arquivo.read_bytes()
    return struct.unpack(">II", dados[16:24]) + (dados[25] in (4, 6) or b"tRNS" in dados,)


O = "aula em outros formatos"
FOTO, RETANGULO = (7, 5), (100, 100, 400, 300)
outros = base / f"{O}.pptx"
apresentacao(outros, [("slide1.xml", slide(forma(par("Duas figuras")) + figura("rB") + figura("rE")),
                       [("rB", "image", "../media/foto.bmp", False), ("rE", "image", "../media/desenho.emf", False)])],
             MESTRE, partes_extras={"ppt/media/foto.bmp": bmp(*FOTO, (200, 30, 30)),
                                    "ppt/media/desenho.emf": emf(RETANGULO)})
subprocess.run([sys.executable, str(SCRIPTS / "transcrever_pptx.py"), str(outros), "--idioma", "eng"], cwd=TRABALHO,
               capture_output=True, text=True)
subprocess.run([sys.executable, str(SCRIPTS / "registrar_fonte.py"), str(transcricao.with_name(f"{O}.md")), str(outros),
                "INVENTADA-3"], cwd=TRABALHO, capture_output=True, text=True)
c = conferencia()
print(c.stdout, c.stderr)
foto_bmp, desenho_emf = ((base / O / "ppt" / "media" / n).resolve() for n in ("foto.bmp", "desenho.emf"))
copia_bmp, copia_emf = imagem_mostrada(O, "1.1"), imagem_mostrada(O, "1.2")
confere("copia: BMP em PNG, do mesmo tamanho", (copia_bmp.suffix, copia_bmp.is_file() and png_lido(copia_bmp)),
        (".png", FOTO + (False,)))
largura, altura, transparente = png_lido(copia_emf) if copia_emf.is_file() else (0, 1, True)
forma_do_desenho = (RETANGULO[2] - RETANGULO[0]) / (RETANGULO[3] - RETANGULO[1])
confere("copia: EMF em PNG, com a forma do desenho, nao a da folha, e com fundo",
        (copia_emf.suffix, round(largura / altura, 1), transparente), (".png", round(forma_do_desenho, 1), False))
confere("copia: link para o original", (foto_bmp in links_do_bloco(O, "1.1"), desenho_emf in links_do_bloco(O, "1.2")),
        (True, True))
confere("copia: imagem em PNG aparece como esta", imagem_mostrada(G, "3.1"),
        (base / G / "ppt" / "media" / "fundo.png").resolve())
alvos, recusadas = alvos_da_conferencia(saida)
locais = [unquote(a.split("#")[0]) for a in alvos if a.split("#")[0]]
confere("copia: links que o Markdown aceita, para arquivos que existem",
        (recusadas, [a for a in locais if not (saida.parent / a).exists()]), ([], []))
no_bloco(O, "1.2", lambda b: b.replace("- [ ] IA", "- [x] IA"))
feita = copia_emf.stat().st_mtime_ns
conferencia()
confere("copia: o tique fica e a copia nao e feita de novo",
        ("- [x] IA" in bloco(O, "1.2"), copia_emf.stat().st_mtime_ns), (True, feita))
sem_gm = TRABALHO / "sem-gm"  # todo programa do PATH, menos o GraphicsMagick
sem_gm.mkdir()
for pasta in map(Path, os.environ["PATH"].split(os.pathsep)):
    for programa in sorted(pasta.iterdir()) if pasta.is_dir() else []:
        if programa.name != "gm" and not os.path.lexists(sem_gm / programa.name) and os.access(programa, os.X_OK):
            (sem_gm / programa.name).symlink_to(programa)
if copia_bmp.suffix == ".png":
    copia_bmp.unlink()
subprocess.run([sys.executable, str(SCRIPTS / "conferencia.py")], cwd=TRABALHO, capture_output=True, text=True,
               env={**os.environ, "PATH": str(sem_gm)})
confere("copia: sem o GraphicsMagick, o original aparece, e o bloco diz por que; a copia que ja existe fica",
        (imagem_mostrada(O, "1.1"), "GraphicsMagick" in bloco(O, "1.1"), imagem_mostrada(O, "1.2")),
        (foto_bmp, True, copia_emf))

print("FALHAS:", FALHAS or "nenhuma")
sys.exit(1 if FALHAS else 0)
