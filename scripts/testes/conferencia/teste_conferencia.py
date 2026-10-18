# SPDX-License-Identifier: GPL-3.0-or-later
# Copyright do codigo sob GPL-3.0 -- ver LICENSE e NOTICE.md na raiz do projeto.

"""Teste do conferencia.py de um projeto, na parte das transcricoes feitas pelo extrator.

Monta, na pasta de trabalho, um projeto pequeno: a pasta de scripts dada, um projeto.json
feito do modelo dado com as pastas das transcricoes daqui, dentro da pasta das fontes que o
modelo da (a configuracao do extrator e a lista de extracao ficam onde o modelo diz), um
PDF inventado de quatro paginas (uma que vai pelo OCR, uma com uma correcao da leitura),
uma pagina HTML, a configuracao do extrator e a lista de extracao. O extrator do proprio
projeto escreve as transcricoes, que recebem o registro da fonte. O modelo do titulo de
pagina sai da expressao que o comum.py do projeto usa para achar as paginas
(TITULO_PAGINA), porque a conferencia acha as transcricoes por ela; o resto do padrao e
inventado. As marcas do arquivo de conferencia (a da parte, a do tique, a cerca) tambem
vem do comum.py do projeto.

O teste confere regras, nunca uma frase pronta:
  - a transcricao igual ao que o extrator le nao da erro, e so a pagina do OCR e a
    corrigida vao a ticar, com a imagem quando a fonte e PDF;
  - a pagina da camada de texto mudada na transcricao, no texto ou no rotulo, e erro, que
    diz a pagina; a pagina HTML mudada tambem;
  - o tique da pessoa volta se a pagina nao mudou, e sai se mudou;
  - o texto de uma pagina feita pelo extrator nao se leva do arquivo de conferencia para a
    transcricao: e erro, e nada e gravado;
  - a transcricao que nao esta na lista de extracao continua conferida como PDF, com todas
    as paginas a ticar;
  - a transcricao da lista sem a fonte registrada da erro em cada pagina, que nao foi
    conferida;
  - a lista de extracao e a configuracao do extrator com um campo que o molde nao conhece
    sao erro, que diz o arquivo, e nada e gravado;
  - duas rodadas dao o mesmo arquivo.
Precisa do Poppler e do Tesseract com o idioma "eng". Uso:
    python3 -I teste_conferencia.py <pasta scripts do projeto> <projeto.json modelo> <pasta de trabalho nova>
Precisa do pdf_inventado.py, dos testes do extrator, na pasta irma "extrator".
"""
import hashlib
import json
import random
import shutil
import string
import subprocess
import sys
from pathlib import Path

SCRIPTS, MODELO, TRABALHO = (Path(a).resolve() for a in sys.argv[1:4])
PROJ = TRABALHO / "projeto"
PROJ_SCRIPTS = PROJ / SCRIPTS.name  # a pasta de scripts do projeto pequeno, com o nome da pasta dada
shutil.copytree(SCRIPTS, PROJ_SCRIPTS, ignore=shutil.ignore_patterns("__pycache__"))
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "extrator"))  # os testes do extrator, na pasta irma
sys.path.insert(0, str(PROJ_SCRIPTS))
from comum import CERCA, MARCA_PARTE, TIQUE, TITULO_PAGINA, fecha_a_cerca  # noqa: E402
from extrator_comum import como_padrao  # noqa: E402
from pdf_inventado import pagina_de_linhas, pdf_inventado  # noqa: E402

FALHAS = []
SORTEIO = random.Random(1)


def confere(condicao, descricao):
    if not condicao:
        FALHAS.append(descricao)
    return condicao


def frase():
    return " ".join("".join(SORTEIO.choice(string.ascii_letters) for _ in range(SORTEIO.randint(2, 7)))
                    for _ in range(SORTEIO.randint(2, 6)))


# ---------- o projeto pequeno ----------
projeto = json.loads(MODELO.read_text(encoding="utf-8"))
PROTEGIDA = projeto["caminhos"]["material_base"]  # a pasta das fontes, que o modelo do projeto dá
caminhos = {"gerados": f"{PROTEGIDA}/transcricoes", "imagens": f"{PROTEGIDA}/transcricoes/imagens",
            "conferencia_imagens": f"{PROTEGIDA}/transcricoes/CONFERENCIA.md"}
projeto["caminhos"].update(caminhos)
caminhos = projeto["caminhos"]  # os da configuracao do extrator e da lista de extracao sao os do modelo
(PROJ / "projeto.json").write_text(json.dumps(projeto, ensure_ascii=False), encoding="utf-8")

# o modelo do titulo tirado da expressao do comum.py: o primeiro grupo e o rotulo, o
# segundo, a posicao no arquivo; o resto e o texto fixo dele
MODELO_TITULO = TITULO_PAGINA.pattern.strip("^$").replace(r"\s*", "").replace("(.+?)", "{rotulo}", 1) \
    .replace(r"(\d+)", "{arquivo}", 1).replace("\\", "")
if not TITULO_PAGINA.match(MODELO_TITULO.format(rotulo="x", arquivo=1)):
    sys.exit(f"o modelo tirado do comum.py ({MODELO_TITULO!r}) não faz um título que ele reconhece: "
             f"o teste precisa ler a expressão de outro jeito")
PADRAO = {"titulo_pagina": MODELO_TITULO, "rotulo_numerada": "pg {numero}", "rotulo_sem_numero": "pg ?",
          "rotulo_sem_paginas": "inteiro", "sem_texto": "(vazio)", "escape": "~", "escapar": ["~", "|", "#"],
          "escapar_no_comeco": ["#"], "tabela": {"inicio": "| ", "meio": " | ", "fim": " |", "separador": "---"}}
TITULO = como_padrao(PADRAO["titulo_pagina"])
LINHAS = [[frase() for _ in range(SORTEIO.randint(2, 5))] for _ in range(4)]
VISIVEIS = ["LARANJA", "JANELA"]
OCR, CORRIGIDA = 3, 2
PAGINAS_DO_PDF = [pagina_de_linhas(l, 12, 18) for l in LINHAS]
PAGINAS_DO_PDF[OCR - 1] = [(48, 72, 600, " ".join(VISIVEIS), False), (12, 72, 300, frase(), True)]
FONTE = PROJ / PROTEGIDA / "FONTE-1/manual.pdf"
FONTE.parent.mkdir(parents=True)
FONTE.write_bytes(pdf_inventado(PAGINAS_DO_PDF))
PAGINA = PROJ / PROTEGIDA / "FONTE-2/pagina.html"
PAGINA.parent.mkdir(parents=True)
PARAGRAFOS = [frase() for _ in range(3)]
PAGINA.write_text("<html><meta charset=\"utf-8\">" + "".join(f"<p>{p}</p>" for p in PARAGRAFOS) + "</html>",
                  encoding="utf-8")
EXTRATOR = {"versao_schema": 1, "padrao": PADRAO, "leitores": {
    "pdf": {"extensoes": [".pdf"], "opcoes": {"ocr": [], "idioma_ocr": "eng", "modo_ocr": "3", "resolucao_ocr": 300,
                                              "destaques": {}}},
    "marcacao": {"extensoes": [".html"], "opcoes": {
        "codificacao": "utf-8", "blocos": ["p"], "quebras": [], "vazios": ["meta"], "ignorar": [], "conteudo": None,
        "tabela": {"tabela": "table", "linha": "tr", "celulas": ["td"]}, "destaques": {}}}}}
TRANSCRICAO = PROJ / caminhos["gerados"] / "manual.md"
TRANSCRICAO_HTML = PROJ / caminhos["gerados"] / "pagina.md"
CORRECAO = {"pagina": CORRIGIDA, "de": LINHAS[CORRIGIDA - 1][0].split()[0], "para": frase().split()[0]}
DOCS = [{"arquivo": str(FONTE.relative_to(PROJ)), "saida": str(TRANSCRICAO.relative_to(PROJ)),
         "numeracao": [{"de": 2, "ate": 4, "estilo": "arabico", "primeiro": SORTEIO.randint(1, 99)}],
         "opcoes": {"ocr": [{"de": OCR, "ate": OCR}]}, "correcoes": [CORRECAO]},
        {"arquivo": str(PAGINA.relative_to(PROJ)), "saida": str(TRANSCRICAO_HTML.relative_to(PROJ)),
         "correcoes": [{"pagina": 1, "de": PARAGRAFOS[0].split()[0], "para": frase().split()[0]}]}]
for chave in ("extrator", "extracao"):
    (PROJ / caminhos[chave]).parent.mkdir(parents=True, exist_ok=True)
(PROJ / caminhos["extrator"]).write_text(json.dumps(EXTRATOR, ensure_ascii=False), encoding="utf-8")
(PROJ / caminhos["extracao"]).write_text(json.dumps({"versao_schema": 1, "documentos": DOCS}, ensure_ascii=False),
                                         encoding="utf-8")
r = subprocess.run([sys.executable, "-I", str(PROJ_SCRIPTS / "extrator.py"), str(PROJ / caminhos["extrator"]),
                    str(PROJ / caminhos["extracao"]), "--raiz", str(PROJ)], capture_output=True, text=True)
if not confere(r.returncode == 0, f"o extrator do projeto escreve as transcrições: {r.stdout + r.stderr}"):
    print("\n".join(FALHAS))
    sys.exit(1)


def registro(chave, fonte):
    """O registro da fonte no topo da transcricao, como o registrar_fonte.py escreve."""
    impressao = hashlib.sha256(fonte.read_bytes()).hexdigest()
    return f"---\nfonte {chave}: {fonte.relative_to(PROJ)} | sha256: {impressao}\n---\n\n"


for arquivo, chave, fonte in ((TRANSCRICAO, "FONTE-1", FONTE), (TRANSCRICAO_HTML, "FONTE-2", PAGINA)):
    arquivo.write_text(registro(chave, fonte) + arquivo.read_text(encoding="utf-8"), encoding="utf-8")
ORIGINAL, ORIGINAL_HTML = TRANSCRICAO.read_text(encoding="utf-8"), TRANSCRICAO_HTML.read_text(encoding="utf-8")
CONFERENCIA = PROJ / caminhos["conferencia_imagens"]


def conferencia(*extra):
    r = subprocess.run([sys.executable, "-I", str(PROJ_SCRIPTS / "conferencia.py"), "--projeto",
                        str(PROJ / "projeto.json"), *extra], capture_output=True, text=True)
    return r.returncode, r.stdout + r.stderr


def erros(saida):
    return [l for l in saida.split("\n") if l.startswith("ERRO")]


def partes(grupo):
    """{parte: {"IA": bool, "pessoa": bool, "imagem": bool}} das partes a ticar do grupo."""
    out, atual = {}, None
    for linha in CONFERENCIA.read_text(encoding="utf-8").split("\n"):
        m, t = MARCA_PARTE.match(linha), TIQUE.match(linha)
        if m:
            atual = m.group(2) if m.group(1) == grupo else None
            if atual:
                out[atual] = {"IA": False, "pessoa": False, "imagem": False}
        elif linha.startswith("#"):
            atual = None
        elif atual and t:
            out[atual][t.group(2)] = t.group(1) != " "
        elif atual and linha.startswith("![") and linha.endswith(".png)"):
            out[atual]["imagem"] = True
    return out


def muda_na_parte(grupo, parte, muda):
    """O arquivo de conferencia com muda(linha, dentro da cerca) em cada linha da parte."""
    linhas, atual, cerca = CONFERENCIA.read_text(encoding="utf-8").split("\n"), None, None
    for k, linha in enumerate(linhas):
        m = MARCA_PARTE.match(linha)
        if m:
            atual = (m.group(1), m.group(2))
        elif linha.startswith("#"):
            atual = None
        elif atual == (grupo, parte):
            if cerca is not None and fecha_a_cerca(cerca, linha):
                cerca = None
            elif cerca is None and CERCA.match(linha):
                cerca = CERCA.match(linha).group(1)
            else:
                linhas[k] = muda(linha, cerca is not None)
    CONFERENCIA.write_text("\n".join(linhas), encoding="utf-8")


def muda_pagina(original, n, no_titulo=False):
    """A transcricao com uma letra a mais na primeira linha de texto da pagina n, ou no
    rotulo dela."""
    linhas, dentro = original.split("\n"), False
    for k, linha in enumerate(linhas):
        m = TITULO.match(linha)
        if m:
            dentro = int(m.group("arquivo")) == n
            if dentro and no_titulo:
                linhas[k] = PADRAO["titulo_pagina"].format(rotulo=m.group("rotulo") + "x", arquivo=n)
                return "\n".join(linhas)
        elif dentro and linha.strip():
            linhas[k] = linha + "x"
            return "\n".join(linhas)
    sys.exit(f"a página {n} não tem texto")


def rotulo(original, n):
    titulos = [m for m in map(TITULO.match, original.split("\n")) if m]
    return next(m.group("rotulo") for m in titulos if int(m.group("arquivo")) == n)


def tica_pessoa(linha, _):
    t = TIQUE.match(linha)
    return linha.replace(f"[{t.group(1)}]", "[x]") if t and t.group(2) == "pessoa" else linha


# ---------- igual ao que o extrator le ----------
cod, out = conferencia()
confere(cod == 0 and not erros(out), f"a transcrição igual ao que o extrator lê não dá erro: {out}")
ps = partes("manual")
confere(set(ps) == {str(OCR), str(CORRIGIDA)}, f"só a página do OCR e a corrigida vão a ticar: {sorted(ps)}")
confere(all(p["imagem"] for p in ps.values()), "a página a ticar aparece com a imagem dela")
confere(set(partes("pagina")) == {"1"} and not partes("pagina")["1"]["imagem"],
        f"a página HTML corrigida vai a ticar, sem imagem: {partes('pagina')}")
primeira = CONFERENCIA.read_bytes()
conferencia()
confere(CONFERENCIA.read_bytes() == primeira, "duas rodadas dão o mesmo arquivo")

# ---------- o tique da pessoa ----------
muda_na_parte("manual", str(OCR), tica_pessoa)
conferencia()
confere(partes("manual").get(str(OCR), {}).get("pessoa"), "o tique da pessoa volta quando a página não mudou")
TRANSCRICAO.write_text(muda_pagina(ORIGINAL, OCR), encoding="utf-8")
cod, out = conferencia()
confere(not partes("manual").get(str(OCR), {}).get("pessoa", True), "o tique sai quando a página mudou")
confere(not erros(out), f"a página do OCR não é comparada pelo script: {out}")
TRANSCRICAO.write_text(ORIGINAL, encoding="utf-8")

# ---------- a pagina mudada na transcricao ----------
for n in (1, 4):
    TRANSCRICAO.write_text(muda_pagina(ORIGINAL, n), encoding="utf-8")
    cod, out = conferencia()
    confere(cod == 1 and len(erros(out)) == 1 and f"{TRANSCRICAO.name}, {rotulo(ORIGINAL, n)}:" in erros(out)[0],
            f"a página {n} da camada de texto mudada é erro, que diz a página: {erros(out)}")
    confere(str(n) not in partes("manual"), f"a página {n} mudada não vai a ticar")
TRANSCRICAO.write_text(muda_pagina(ORIGINAL, 4, no_titulo=True), encoding="utf-8")
cod, out = conferencia()
confere(cod == 1 and len(erros(out)) == 1 and TRANSCRICAO.name in erros(out)[0], f"o rótulo mudado é erro: {out}")
TRANSCRICAO.write_text(ORIGINAL, encoding="utf-8")
TRANSCRICAO_HTML.write_text(muda_pagina(ORIGINAL_HTML, 1), encoding="utf-8")
cod, out = conferencia()
confere(cod == 1 and len(erros(out)) == 1 and TRANSCRICAO_HTML.name in erros(out)[0],
        f"a página HTML mudada é erro: {out}")
TRANSCRICAO_HTML.write_text(ORIGINAL_HTML, encoding="utf-8")
conferencia()

# ---------- o texto da pagina nao se leva do arquivo de conferencia ----------
for grupo, parte, arquivo, original in (("manual", str(CORRIGIDA), TRANSCRICAO, ORIGINAL),
                                       ("pagina", "1", TRANSCRICAO_HTML, ORIGINAL_HTML)):
    muda_na_parte(grupo, parte, lambda l, na_cerca: l + " mais" if na_cerca and l.strip() else l)
    cod, out = conferencia("--levar-correcoes")
    confere(cod == 1 and erros(out) and arquivo.read_text(encoding="utf-8") == original,
            f"{grupo}: o texto de uma página feita pelo extrator não se leva da conferência, e nada é gravado: {out}")
    conferencia()

# ---------- a transcricao da lista sem a fonte registrada ----------
TRANSCRICAO_HTML.write_text(ORIGINAL_HTML.split("---\n\n", 1)[1], encoding="utf-8")
cod, out = conferencia()
paginas_html = sum(1 for linha in ORIGINAL_HTML.split("\n") if TITULO.match(linha))
confere(cod == 1 and sum(1 for e in erros(out) if TRANSCRICAO_HTML.name in e) == paginas_html + 1,
        f"sem a fonte registrada, um erro do registro e um por página, que não foi conferida: {erros(out)}")
TRANSCRICAO_HTML.write_text(ORIGINAL_HTML, encoding="utf-8")
conferencia()

# ---------- a lista e a configuracao fora do molde param tudo ----------
for arquivo in (PROJ / caminhos["extracao"], PROJ / caminhos["extrator"]):
    antes, gerado = arquivo.read_text(encoding="utf-8"), CONFERENCIA.read_bytes()
    dados = json.loads(antes)
    dados["campo_" + "_".join(frase().split())] = frase()
    arquivo.write_text(json.dumps(dados, ensure_ascii=False), encoding="utf-8")
    cod, out = conferencia()
    confere(cod == 1 and any(arquivo.name in e for e in erros(out)) and CONFERENCIA.read_bytes() == gerado,
            f"{arquivo.name} fora do molde é erro, que diz o arquivo, sem gravar nada: {erros(out)}")
    arquivo.write_text(antes, encoding="utf-8")

# ---------- a transcricao fora da lista continua conferida como PDF ----------
FORA = PROJ / caminhos["gerados"] / "fora.md"
FORA.write_text(registro("FONTE-1", FONTE) + "".join(
    f"{PADRAO['titulo_pagina'].format(rotulo=frase(), arquivo=n)}\n\n{frase()}\n\n" for n in range(1, 5)),
    encoding="utf-8")
conferencia()
confere(set(partes("fora")) == {"1", "2", "3", "4"},
        f"fora da lista, todas as páginas vão a ticar: {partes('fora')}")
confere(set(partes("manual")) == {str(OCR), str(CORRIGIDA)}, "a transcrição da lista não muda por isso")

for f in FALHAS:
    print("FALHA:", f)
print(f"{len(FALHAS)} falha(s)")
sys.exit(1 if FALHAS else 0)
