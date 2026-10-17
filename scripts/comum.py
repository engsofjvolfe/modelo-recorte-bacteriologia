# SPDX-License-Identifier: GPL-3.0-or-later
# Copyright do codigo sob GPL-3.0 -- ver LICENSE e NOTICE.md na raiz do projeto.

"""
Funcoes que os outros scripts usam: achar o projeto e as planilhas de pergunta, ler o
formato da disciplina conferido contra o molde dele e nas ligacoes de dentro dele, achar
no formato as unidades e os conjuntos de um documento, os itens e a grade de cada unidade
e o que cada id quer dizer, o registro da fonte no topo de um documento gerado, a
impressao digital de um arquivo, os tiques de um arquivo de conferencia, a imagem de uma
pagina de PDF, as paginas de uma fonte em HTML, os slides de uma apresentacao em pptx, as
marcas da transcricao e o que os transcritores fazem do mesmo jeito (o texto de uma linha,
o indice e o expoente, a tabela, o texto de dentro de uma imagem, a gravacao da
transcricao). Nao e para rodar sozinho.

Nenhum caminho fica no codigo. O projeto e achado pelo arquivo "projeto.json", subindo
de pasta em pasta a partir de onde o script e chamado (ou pelo arquivo indicado com
--projeto), e todo caminho sai dele, relativo a pasta onde ele esta. O nome
"projeto.json" e fixo: e por ele que o script reconhece o projeto. A pasta do material de
base tambem: o schema do projeto.json so aceita o lugar dela e poe dentro dela tudo o que
tem texto de terceiros, e e ela que o .gitignore deixa de fora.

Registro da fonte, no topo do documento gerado (uma linha por fonte; a chave e a mesma
da referencia da fonte no arquivo de fontes do projeto):
    ---
    fonte <CHAVE>: <caminho relativo a raiz do projeto> | sha256: <64 hexadecimais>
    ---

Tique, no arquivo de conferencia: uma marca com o grupo, a parte e a assinatura do que
foi conferido, seguida das caixas "IA" e "pessoa".

Fonte em HTML (como um livro digital): as paginas impressas sao marcadas no proprio
documento, com epub:type="pagebreak" (EPUB 3) ou role="doc-pagebreak" (DPUB-ARIA), e o
numero impresso vem do atributo title ou aria-label da marca, ou do texto dela. Quem
transcreve e quem confere percorrem o documento pelo mesmo caminho (percorre), e por
isso cortam as paginas no mesmo lugar.

Fonte em pptx (apresentacao de slides, Office Open XML): cada slide e uma pagina, na
ordem da apresentacao, e o lugar dele na citacao e a posicao no arquivo. Quem transcreve
e quem confere leem os slides pela mesma leitura (Apresentacao), e por isso tem o mesmo
texto.
"""

import hashlib
import os
import posixpath
import re
import shutil
import subprocess
import sys
import tempfile
import unicodedata
import xml.etree.ElementTree as ET
import zipfile
from collections import namedtuple
from functools import lru_cache
from html.parser import HTMLParser
from pathlib import Path

from validar_dados import esquema, le_dados

ARQUIVO_PROJETO = "projeto.json"
MOLDE_COM_GRADE = "eixos"  # o tipo de molde de documento que tem grade (esquemas/formato.schema.json)
PASTA_NORMAS = Path(__file__).resolve().parent / "normas"  # as tabelas que vem de normas, como a ISO 639
LINHA_FONTE = re.compile(r"^fonte (?P<chave>\S+): (?P<caminho>.+?) \| sha256: (?P<hash>[0-9a-f]{64})$")
MARCA_PARTE = re.compile(r"^<!-- parte: ([^|]+)\|([^|]+)\|([0-9a-f]+) -->$")
TIQUE = re.compile(r"^- \[([ xX])\] (IA|pessoa)\s*$")
VARIAVEL = re.compile(r"\{[^{}]+\}")

# documentos do projeto, em Markdown
EXTENSAO_DOCUMENTO = ".md"
CERCA = re.compile(r"^ {0,3}(`{3,}|~{3,})")  # abre ou fecha um bloco de codigo
CODIGO_NA_LINHA = re.compile(r"(`+).+?\1")

# marcas da transcricao (secao 1 da metodologia)
TITULO_PAGINA = re.compile(r"^## (.+?) \(arquivo p\. (\d+)\)\s*$")
SEM_TEXTO = "[sem texto]"
FIGURA = "![imagem]({})"  # a figura que e um arquivo proprio na fonte, no lugar dela
LINHA_FIGURA = re.compile(r"^!\[imagem\]\((.+)\)$")
FIM_FIGURA = "[fim da imagem]"
CONTINUACAO = "[continuação da tabela da {}]"  # {} e o rotulo da pagina onde a tabela comeca
LINHA_CONTINUACAO = re.compile(r"^\[continuação da tabela da .+\]$")
ROTULO_PAGINA = "p. {}"  # {} e o numero impresso
ROTULO_SLIDE = "slide {}"  # {} e a posicao do slide no arquivo
SLIDE_OCULTO = "[slide oculto]"
NOTAS = "[notas do apresentador]"
MARCAS_DE_LINHA = (SEM_TEXTO, SLIDE_OCULTO, NOTAS)  # marcas que ocupam a linha inteira e nao sao texto da fonte

# texto de dentro das imagens
MODO_OCR = "11"  # Tesseract --psm 11: texto esparso, cada pedaco numa linha, como os rotulos de uma figura
FORMATOS_DO_OCR = {".png", ".jpg", ".jpeg", ".jpe", ".jfif", ".tif", ".tiff", ".bmp", ".gif", ".webp", ".pbm",
                   ".pgm", ".ppm", ".pnm", ".jp2"}  # os que o Tesseract le; os outros passam antes pelo LibreOffice

# fonte em pptx
EXTENSOES_PPTX = (".pptx", ".pptm", ".ppsx", ".ppsm")
ARQUIVO_SIMBOLOS = PASTA_NORMAS / "simbolos.json"  # fonte de simbolos -> Unicode
NS = {  # os espacos de nomes do Office Open XML (ECMA-376) e das extensoes que ele usa
    "a": "http://schemas.openxmlformats.org/drawingml/2006/main",
    "p": "http://schemas.openxmlformats.org/presentationml/2006/main",
    "r": "http://schemas.openxmlformats.org/officeDocument/2006/relationships",
    "mc": "http://schemas.openxmlformats.org/markup-compatibility/2006",
    "dgm": "http://schemas.openxmlformats.org/drawingml/2006/diagram",
    "dsp": "http://schemas.microsoft.com/office/drawing/2008/diagram",
}
SIMBOLOS_PRIVADOS = range(0xF000, 0xF100)  # onde a fonte de simbolos guarda os caracteres dela (codigo + F000)
MESMO_SINAL = {"−": "-"}  # na comparacao, o sinal de menos e o hifen sao o mesmo sinal

# fonte em HTML
EXTENSOES_HTML = (".xhtml", ".html", ".htm")
VAZIOS = {"area", "base", "br", "col", "embed", "hr", "img", "input", "link", "meta", "param", "source", "track",
          "wbr"}
INVISIVEIS = {"head", "script", "style", "template"}
No = namedtuple("No", "tag attrs filhos")
Pagina = namedtuple("Pagina", "rotulo ancora texto imagens")


class Projeto:
    """Os caminhos do projeto, lidos do projeto.json (dados), relativos a pasta dele."""

    def __init__(self, arquivo, dados):
        self.arquivo = Path(arquivo).resolve()
        self.raiz = self.arquivo.parent
        self.dados = dados

    def caminho(self, nome):
        return self.raiz / self.dados["caminhos"][nome]

    def caminho_com(self, nome, valor):
        """Caminho que o projeto.json da com uma variavel entre chaves, como "{item}" ou
        "{planilha}", com o valor no lugar dela."""
        return self.raiz / VARIAVEL.sub(lambda _: valor, self.dados["caminhos"][nome])

    def todos_com(self, nome):
        """Arquivos que existem para o modelo de caminho com variavel (qualquer valor)."""
        return sorted(self.raiz.glob(VARIAVEL.sub("*", self.dados["caminhos"][nome])))

    def valor(self, nome):
        return self.dados[nome]

    def pasta_de_imagens(self, conferencia):
        """Pasta das imagens de um arquivo de conferencia: dentro da pasta de imagens do
        projeto, uma subpasta com o nome do proprio arquivo de conferencia."""
        return self.caminho("imagens") / Path(conferencia).stem


def procura_projeto():
    """O primeiro projeto.json achado subindo a partir da pasta atual, ou None."""
    atual = Path.cwd().resolve()
    return next((d / ARQUIVO_PROJETO for d in (atual, *atual.parents) if (d / ARQUIVO_PROJETO).is_file()), None)


def acha_projeto(arquivo=None):
    """O projeto.json indicado, ou o primeiro achado subindo a partir da pasta atual, lido
    pela leitura de todo arquivo de dados (validar_dados.le_dados), contra o molde dele.
    Com erro nele, o script para e mostra cada erro com ERRO e o caminho inteiro do
    arquivo, que diz qual projeto.json foi achado."""
    if arquivo is None:
        arquivo = procura_projeto()
        if arquivo is None:
            raise SystemExit(f"nenhum {ARQUIVO_PROJETO} em {Path.cwd().resolve()} nem nas pastas acima -- "
                             f"copie modelo-dados/{ARQUIVO_PROJETO} para a raiz do projeto")
    arquivo = Path(arquivo).resolve()
    dados, erros = le_dados(arquivo, esquema(Path(ARQUIVO_PROJETO).stem), nome=arquivo)
    if erros:
        raise SystemExit("\n".join(f"ERRO em {e}" for e in erros))
    return Projeto(arquivo, dados)


def le_formato(projeto):
    """(formato, erros): o formato da disciplina (no projeto.json, "formato"), lido pela
    leitura de todo arquivo de dados (validar_dados.le_dados), contra o molde dele, e com as
    ligacoes de dentro dele conferidas (erros_das_ligacoes), quando ele segue o molde. E a
    unica leitura do formato: todo script que usa o formato le por aqui. Com qualquer erro
    -- texto fora do UTF-8, JSON invalido, fora do molde ou ligacao que nao fecha --, o
    formato vem None e os erros vem cada um com o nome do arquivo na frente, pra quem chama
    mostrar com ERRO e nao usar o formato. Nao confere se o arquivo existe: o script que
    precisa dele diz o que fazer quando ele falta, e o que funciona sem ele so chama esta
    funcao quando ele existe."""
    arquivo = projeto.caminho("formato")
    formato, erros = le_dados(arquivo, esquema("formato"))
    if not erros:
        erros = [f"{arquivo.name}: {e}" for e in erros_das_ligacoes(formato)]
    return (None if erros else formato), erros


# ---------- o que se acha dentro do formato ----------

Entrada = namedtuple("Entrada", "documento unidade item direto")  # uma coisa que um id quer dizer (o_que_e)


def unidades(documento):
    """As unidades do documento, na ordem do formato; nenhuma, quando ele nao as lista."""
    return documento.get("unidades", [])


def itens(unidade):
    """Os itens da unidade, na ordem do formato; nenhum, quando ela nao os lista."""
    return unidade.get("itens", [])


def conjuntos(documento):
    """Os conjuntos do documento, na ordem do formato; nenhum, quando ele nao os lista."""
    return documento.get("conjuntos", [])


def entradas_do_documento(documento):
    """{id: Entrada} de cada unidade do documento e de cada item delas, como lugar direto: a
    entrada de uma unidade tem o item None; a de um item, a unidade dele."""
    saida = {}
    for u in unidades(documento):
        saida[u["id"]] = Entrada(documento, u, None, True)
        saida.update((i["id"], Entrada(documento, u, i, True)) for i in itens(u))
    return saida


def o_que_e(formato, id_):
    """[Entrada] do que um id do formato quer dizer, cada uma com o documento, a unidade, o
    item (None, na de uma unidade) e se o lugar e direto: a unidade ou o item com esse id,
    como lugar direto; ou cada membro do conjunto com esse id, na ordem dele, como lugar
    indireto. Nenhuma, quando o formato nao tem o id. Cada id e um so em todo o formato, e
    cada membro de um conjunto e unidade ou item do documento dele (erros_das_ligacoes)."""
    for d in formato["documentos"]:
        entradas = entradas_do_documento(d)
        if id_ in entradas:
            return [entradas[id_]]
        for c in conjuntos(d):
            if c["id"] == id_:
                return [entradas[m]._replace(direto=False) for m in c["membros"]]
    return []


def acha_unidade(formato, id_unidade):
    """(documento, unidade) da unidade com o id dado, ou (None, None) quando o id nao e de
    nenhuma unidade (o_que_e)."""
    return next(((e.documento, e.unidade) for e in o_que_e(formato, id_unidade) if e.direto and e.item is None),
                (None, None))


def grade(documento, unidade=None):
    """Os eixos da ficha de uma unidade do documento: os da propria unidade, quando ela tem os
    seus; senao, os do documento, que sao tambem a grade sem unidade. Nenhum, quando nao ha."""
    return (unidade or {}).get("eixos") or documento.get("eixos", [])


def linhas_do_eixo(eixo):
    """As linhas da grade que um eixo da: os subtopicos dele, ou ele mesmo, quando nao se divide."""
    return eixo.get("subtopicos") or [eixo]


def tipos_do_formato(formato):
    """Os tipos de conhecimento que o formato nomeia: os das partes da sequencia, os que se
    ensinam junto de outro trecho, os das regras de fora e os das formas de pergunta."""
    return ({t for p in formato["partes_por_tipo"] for t in p["tipos"]} | set(formato["tipos_junto"])
            | {t for r in formato["fora"] for t in r["tipos"]}
            | {t for d in formato["documentos"] for f in d.get("formas", []) for t in f["tipos"]})


# ---------- as ligacoes de dentro do formato ----------

def repetidos(pares):
    """[(valor, [lugares])] dos valores que aparecem em mais de um lugar, na ordem em que cada
    um aparece primeiro; pares e uma lista de (valor, lugar)."""
    lugares = {}
    for valor, lugar in pares:
        lugares.setdefault(valor, []).append(lugar)
    return [(v, ls) for v, ls in lugares.items() if len(ls) > 1]


def onde(documento, unidade=None, item=None):
    """O lugar de um documento, ou de uma unidade dele, ou de um item dela, numa frase de erro."""
    return (f"documento {documento['id']!r}" + (f", unidade {unidade['id']!r}" if unidade else "")
            + (f", item {item['id']!r}" if item else ""))


def onde_do_conjunto(documento, conjunto):
    return f"{onde(documento)}, conjunto {conjunto['id']!r}"


def ids_do_documento(documento):
    """[(id, lugar)] de cada unidade, item e conjunto do documento, na ordem do formato."""
    return ([(u["id"], onde(documento, u)) for u in unidades(documento)]
            + [(i["id"], onde(documento, u, i)) for u in unidades(documento) for i in itens(u)]
            + [(c["id"], onde_do_conjunto(documento, c)) for c in conjuntos(documento)])


def erros_dos_conjuntos(documento):
    """Os membros dos conjuntos do documento que nao sao unidade nem item dele: um conjunto so
    reune unidades e itens do proprio documento, nunca outro conjunto."""
    entradas = entradas_do_documento(documento)
    return [f"{onde_do_conjunto(documento, c)}: o membro {m!r} não é unidade nem item do documento; um conjunto só "
            "reúne unidades e itens do próprio documento" for c in conjuntos(documento) for m in c["membros"]
            if m not in entradas]


def partes_da_ficha(documento, eixos):
    """[(id, o que e)] das partes de uma ficha do documento: as aberturas dele, os eixos e os
    subtopicos de cada eixo."""
    return ([(a["id"], "abertura") for a in documento.get("abertura", [])] + [(e["id"], "eixo") for e in eixos]
            + [(s["id"], f"subtópico do eixo {e['id']!r}") for e in eixos for s in e.get("subtopicos", [])])


def erros_das_fichas(documento):
    """As ligacoes da ficha de um documento: id repetido entre as partes de uma ficha (a do
    documento e a de cada unidade com eixos proprios), elo com eixo que o documento nao tem
    e, no molde que pede grade, documento ou unidade sem grade."""
    fichas = ([(onde(documento), grade(documento))] if documento.get("eixos") else []) + [
        (onde(documento, u), u["eixos"]) for u in unidades(documento) if u.get("eixos")]
    erros = [f"{lugar}: o id {i!r} se repete entre as partes da ficha: {', '.join(ls)}"
             for lugar, eixos in fichas for i, ls in repetidos(partes_da_ficha(documento, eixos))]
    eixos_do_documento = {e["id"] for e in documento.get("eixos", [])}
    erros += [f"{onde(documento)}: o elo {elo['id']!r} usa o eixo {e!r}, que o documento não tem"
              for elo in documento.get("elos", []) for e in elo["eixos"] if e not in eixos_do_documento]
    if documento["molde"] == MOLDE_COM_GRADE:
        if not documento.get("eixos") and not unidades(documento):
            erros.append(f"{onde(documento)}: o molde {documento['molde']!r} pede uma grade, e o documento não "
                         "tem eixos nem unidades")
        erros += [f"{onde(documento, u)}: sem grade: a unidade não tem eixos, e o documento também não"
                  for u in unidades(documento) if not grade(documento, u)]
    return erros


def erros_dos_tipos(formato):
    """As ligacoes dos tipos: tipo em mais de uma parte da sequencia, ou em mais de uma forma
    de pergunta do mesmo documento; tipo ou documento de onde_se_ensina que o formato nao
    tem."""
    erros = [f"o tipo {t!r} está em mais de uma parte da sequência: {', '.join(ls)}"
             for t, ls in repetidos((t, f"parte {p['id']!r}") for p in formato["partes_por_tipo"] for t in p["tipos"])]
    for d in formato["documentos"]:
        formas = enumerate(d.get("formas", []), 1)
        erros += [f"{onde(d)}: o tipo {t!r} está em mais de uma forma de pergunta: {', '.join(ls)}"
                  for t, ls in repetidos((t, f"forma {n} ({f['verbo']})") for n, f in formas for t in f["tipos"])]
    tipos, documentos = tipos_do_formato(formato), {d["id"] for d in formato["documentos"]}
    for tipo, lista in formato["onde_se_ensina"].items():
        if tipo not in tipos:
            erros.append(f"onde_se_ensina: o tipo {tipo!r} não está em nenhuma parte da sequência, nos tipos que vão "
                         "junto, em fora nem nas formas de pergunta")
        erros += [f"onde_se_ensina, tipo {tipo!r}: o documento {d!r} não existe" for d in lista if d not in documentos]
    return erros


def erros_das_ligacoes(formato):
    """As ligacoes de dentro do formato que nao fecham, cada uma numa frase que diz o lugar:
    id de unidade, de item ou de conjunto que se repete em todo o formato; os membros de
    cada conjunto (erros_dos_conjuntos); as da ficha de cada documento (erros_das_fichas);
    grupo de um documento que o formato nao tem; as dos tipos (erros_dos_tipos); id repetido
    entre as regras de fora e as marcas, que dizem a classe do trecho; documento que nao
    recebe nenhum trecho, sem grupo, sem caminho e sem receber todos."""
    documentos, grupos = formato["documentos"], {g["id"] for g in formato["grupos"]}
    erros = [f"o id {i!r} é de mais de uma unidade, item ou conjunto: {'; '.join(ls)}"
             for i, ls in repetidos(par for d in documentos for par in ids_do_documento(d))]
    erros += [e for d in documentos for e in erros_dos_conjuntos(d)]
    erros += [e for d in documentos for e in erros_das_fichas(d)]
    erros += [f"{onde(d)}: o grupo {g!r} não está nos grupos do formato"
              for d in documentos for g in d.get("grupos", []) if g not in grupos]
    erros += erros_dos_tipos(formato)
    erros += [f"o id {i!r} se repete entre fora e marcas: {', '.join(ls)}"
              for i, ls in repetidos([(r["id"], "fora") for r in formato["fora"]]
                                     + [(m["id"], "marcas") for m in formato["marcas"]])]
    erros += [f"{onde(d)}: não recebe nenhum trecho: não tem grupo, nem caminho, nem recebe todos"
              for d in documentos if not (d.get("todos") or d.get("grupos") or d.get("caminhos"))]
    return erros


def lingua(codigo):
    """"pt-BR" -> "pt": a lingua de um codigo de idioma, sem a variante."""
    return codigo.split("-")[0].lower() if codigo else None


def planilhas(projeto, filtro=None):
    """As planilhas de pergunta: os CSVs direto na pasta do material gerado (sem entrar em
    subpastas) cujo nome comeca com o prefixo do projeto; com filtro, so as que tem o
    trecho no nome, sem diferenca entre maiuscula e minuscula."""
    pasta, prefixo = projeto.caminho("material_gerado"), projeto.valor("prefixo_planilhas")
    todas = sorted(pasta.glob(f"{prefixo}*.csv"))
    return [c for c in todas if filtro.lower() in c.name.lower()] if filtro else todas


def impressao_de(dados):
    return hashlib.sha256(dados).hexdigest()


def impressao(arquivo):
    return impressao_de(Path(arquivo).read_bytes())


def separa_registro(texto):
    """(linhas do registro, resto do texto). O registro e o bloco entre "---" no topo."""
    linhas = texto.split("\n")
    if linhas and linhas[0] == "---" and "---" in linhas[1:]:
        fim = linhas.index("---", 1)
        return linhas[1:fim], "\n".join(linhas[fim + 1:])
    return [], texto


def fontes_registradas(texto):
    """{chave: (caminho, sha256)} do registro no topo do texto."""
    registro, _ = separa_registro(texto)
    out = {}
    for linha in registro:
        m = LINHA_FONTE.match(linha)
        if m:
            out[m.group("chave")] = (m.group("caminho"), m.group("hash"))
    return out


def situacao_da_copia(raiz, caminho, hash_registrado):
    """(arquivo, "confere" | "mudou" | "nao-existe")."""
    arquivo = (Path(raiz) / caminho).resolve()
    if not arquivo.exists():
        return arquivo, "nao-existe"
    return arquivo, "confere" if impressao(arquivo) == hash_registrado else "mudou"


def dentro(caminho, pasta):
    """Se o caminho fica dentro da pasta (ou e a propria pasta)."""
    try:
        Path(caminho).resolve().relative_to(Path(pasta).resolve())
        return True
    except ValueError:
        return False


def ignorados_pelo_git(raiz, arquivos):
    """O conjunto dos arquivos que a lista do que nao vai ao GitHub (o .gitignore) deixa de
    fora, numa pergunta so ao git; None se o projeto nao usa o git ou se o git nao esta
    instalado."""
    arquivos = [Path(a).resolve() for a in arquivos]
    try:
        r = subprocess.run(["git", "-C", str(raiz), "check-ignore", "--no-index", "--stdin", "-z"],
                           input="\0".join(map(str, arquivos)).encode("utf-8"), capture_output=True)
    except FileNotFoundError:
        return None
    if r.returncode not in (0, 1):
        return None
    return {Path(p).resolve() for p in r.stdout.decode("utf-8").split("\0") if p}


def ignorado_pelo_git(raiz, caminho):
    """True ou False pra um arquivo so; None como em ignorados_pelo_git."""
    ignorados = ignorados_pelo_git(raiz, [caminho])
    return None if ignorados is None else Path(caminho).resolve() in ignorados


def documentos_do_projeto(raiz):
    """Os documentos do projeto: os arquivos .md que o git guarda ou guardaria (os
    versionados e os novos que a lista do que nao vai ao GitHub nao deixa de fora) e que
    existem, com o caminho inteiro; None se o projeto nao usa o git ou se o git nao esta
    instalado."""
    try:
        r = subprocess.run(["git", "-C", str(raiz), "ls-files", "--cached", "--others", "--exclude-standard", "-z",
                            "--", "*" + EXTENSAO_DOCUMENTO], capture_output=True)
    except FileNotFoundError:
        return None
    if r.returncode != 0:
        return None
    return {(raiz / n).resolve() for n in r.stdout.decode("utf-8").split("\0") if n and (raiz / n).is_file()}


def fecha_a_cerca(abertura, linha):
    """Se a linha fecha o bloco de codigo aberto pela cerca dada (o grupo 1 de CERCA): o
    mesmo sinal, pelo menos tantas vezes quanto na abertura, e nada mais."""
    return re.fullmatch(rf" {{0,3}}{re.escape(abertura[0])}{{{len(abertura)},}}\s*", linha) is not None


def linhas_fora_de_codigo(texto):
    """(numero da linha, a partir de 1, e a linha) de cada linha de um documento Markdown
    fora dos blocos de codigo. O codigo de dentro da linha fica: quem nao o quer usa
    sem_codigo_na_linha."""
    cerca = None
    for n, linha in enumerate(texto.splitlines(), 1):
        m = CERCA.match(linha)
        if cerca is None and m:
            cerca = m.group(1)
        elif cerca is not None:
            if fecha_a_cerca(cerca, linha):
                cerca = None
        else:
            yield n, linha


def sem_codigo_na_linha(linha):
    return CODIGO_NA_LINHA.sub("", linha)


def registros(projeto):
    """[(documento, chave, caminho do arquivo da fonte, sha256)] de todos os documentos
    gerados que registram fonte: as transcricoes e as bases do material de fora."""
    documentos = sorted(set(projeto.caminho("gerados").glob("*.md")) | set(projeto.todos_com("base_externa")))
    return [(doc, chave, projeto.raiz / caminho, h) for doc in documentos
            for chave, (caminho, h) in fontes_registradas(doc.read_text(encoding="utf-8")).items()]


def impressoes_das_fontes(projeto):
    """{sha256: arquivo}: cada arquivo da pasta do material de base que a lista do que nao
    vai ao GitHub deixa de fora (todos, se o projeto nao usa o git) e cada fonte
    registrada, onde quer que esteja."""
    arquivos = [a for a in sorted(projeto.caminho("material_base").rglob("*")) if a.is_file()]
    ignorados = ignorados_pelo_git(projeto.raiz, arquivos)
    out = {impressao(a): a for a in arquivos if ignorados is None or a.resolve() in ignorados}
    for _, _, arquivo, h in registros(projeto):
        out.setdefault(h, arquivo)
    return out


def leva_para(arquivo, pasta, sem_perguntar=False):
    """Move o arquivo pra pasta, depois de mostrar de onde pra onde e a pessoa confirmar
    (ou direto, com sem_perguntar). Devolve o caminho novo, ou None se nao moveu."""
    arquivo, destino = Path(arquivo), Path(pasta) / Path(arquivo).name
    if destino.exists():
        if impressao(destino) != impressao(arquivo):
            print(f"ERRO: já existe outro arquivo com o nome {destino.name} em {pasta}; renomeie um dos dois")
            return None
        print(f"Já existe uma cópia igual em {destino}; ela é que vale. A cópia em {arquivo} pode ser apagada.")
        return destino
    print(f"A fonte {arquivo} está fora da pasta protegida, onde poderia acabar publicada.")
    print(f"Ela pode ir para {destino}.")
    if not sem_perguntar:
        try:
            resposta = input("Digite s pra mover ou n pra deixar onde está: ")
        except EOFError:
            resposta = ""
        if resposta.strip().lower() not in ("s", "sim"):
            print("Nada foi movido.")
            return None
    destino.parent.mkdir(parents=True, exist_ok=True)
    shutil.move(str(arquivo), str(destino))
    print(f"Movida para {destino}.")
    return destino


def assinatura(*partes):
    junto = re.sub(r"\s+", " ", "|".join(str(p) for p in partes)).strip()
    return hashlib.sha256(junto.encode("utf-8")).hexdigest()[:12]


def tiques_anteriores(arquivo):
    """{(grupo, parte): (assinatura, {"IA": bool, "pessoa": bool})} de um arquivo de conferencia."""
    arquivo = Path(arquivo)
    if not arquivo.exists():
        return {}
    out, chave = {}, None
    for linha in arquivo.read_text(encoding="utf-8").split("\n"):
        m = MARCA_PARTE.match(linha)
        if m:
            chave = (m.group(1), m.group(2))
            out[chave] = (m.group(3), {"IA": False, "pessoa": False})
            continue
        m = TIQUE.match(linha)
        if m and chave in out:
            out[chave][1][m.group(2)] = m.group(1) != " "
    return out


def tiques_da_parte(anteriores, grupo, parte, sig):
    """(tiques, retirado): os tiques voltam se a assinatura e a mesma; se mudou, saem."""
    anterior = anteriores.get((grupo, str(parte)))
    if not anterior:
        return {"IA": False, "pessoa": False}, False
    if anterior[0] == sig:
        return anterior[1], False
    return {"IA": False, "pessoa": False}, any(anterior[1].values())


def marca(grupo, parte, sig):
    return f"<!-- parte: {grupo}|{parte}|{sig} -->"


def caixas(tiques):
    return [f"- [{'x' if tiques['IA'] else ' '}] IA", f"- [{'x' if tiques['pessoa'] else ' '}] pessoa"]


def comando(args):
    return subprocess.run(args, capture_output=True, text=True, check=True).stdout


def numero_de_paginas(pdf):
    m = re.search(r"^Pages:\s+(\d+)", comando(["pdfinfo", str(pdf)]), re.M)
    return int(m.group(1)) if m else 0


def imagem(pdf, n, pasta, nome, resolucao):
    """PNG da pagina, na resolucao dada (dpi), gerado de novo so se nao existe ou se o
    PDF e mais novo que ele."""
    pasta.mkdir(parents=True, exist_ok=True)
    base = pasta / f"{nome}-p{n:03d}"
    png = base.with_suffix(".png")
    if not png.exists() or png.stat().st_mtime < Path(pdf).stat().st_mtime:
        comando(["pdftoppm", "-f", str(n), "-l", str(n), "-r", str(resolucao), "-png", "-singlefile",
                 str(pdf), str(base)])
    return png


def link(alvo, saida):
    return Path(os.path.relpath(alvo, Path(saida).parent)).as_posix()


def ancora(texto):
    return re.sub(r"[^\w-]", "", texto.lower().replace(" ", "-"))


def rodape_da_licenca(licenca, nome_licenca, saida):
    """As linhas do fim de um documento gerado: o traco e a licenca do conteudo, com o link
    pro arquivo dela a partir do documento."""
    return ["---", "", f"*Este documento está licenciado sob [{nome_licenca}]({link(licenca, saida)}).*"]


# ---------- fonte em HTML, com as marcas das paginas impressas ----------

class _Arvore(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.raiz = No("#documento", {}, [])
        self.pilha = [self.raiz]

    def handle_starttag(self, tag, attrs):
        no = No(tag, dict(attrs), [])
        self.pilha[-1].filhos.append(no)
        if tag not in VAZIOS:
            self.pilha.append(no)

    def handle_startendtag(self, tag, attrs):
        self.pilha[-1].filhos.append(No(tag, dict(attrs), []))

    def handle_endtag(self, tag):
        for i in range(len(self.pilha) - 1, 0, -1):
            if self.pilha[i].tag == tag:
                del self.pilha[i:]
                return

    def handle_data(self, dados):
        self.pilha[-1].filhos.append(dados)


def le_html(texto):
    """A arvore do documento: cada elemento e um No(tag, attrs, filhos), e o texto, str."""
    arvore = _Arvore()
    arvore.feed(texto)
    arvore.close()
    return arvore.raiz


def texto_de(no):
    return "".join(f if isinstance(f, str) else texto_de(f) for f in no.filhos)


def rotulo_da_marca(no):
    """O numero impresso da pagina que comeca na marca, ou None se o elemento nao e marca de
    pagina."""
    if "pagebreak" not in no.attrs.get("epub:type", "").split() and no.attrs.get("role") != "doc-pagebreak":
        return None
    return " ".join((no.attrs.get("title") or no.attrs.get("aria-label") or texto_de(no)).split()) or "?"


def percorre(no, lista=None):
    """O documento na ordem de leitura, em eventos: ("abre", no), ("fecha", no), ("texto",
    str) e ("pagina", rotulo, no) numa marca de pagina, que nao e texto. O que nao aparece
    na pagina (cabecalho do documento, script, estilo) fica de fora; o item de lista ganha o
    marcador como texto: "- " na lista sem numero, "1. ", "2. "... na numerada."""
    for filho in no.filhos:
        if isinstance(filho, str):
            yield ("texto", filho)
            continue
        if filho.tag in INVISIVEIS:
            continue
        rotulo = rotulo_da_marca(filho)
        if rotulo is not None:
            yield ("pagina", rotulo, filho)
            continue
        yield ("abre", filho)
        if filho.tag in ("ul", "ol"):
            yield from percorre(filho, [filho.tag, int(filho.attrs.get("start") or 1) if filho.tag == "ol" else 0])
        else:
            if filho.tag == "li":
                if lista and lista[0] == "ol":
                    yield ("texto", f"{lista[1]}. ")
                    lista[1] += 1
                else:
                    yield ("texto", "- ")
            yield from percorre(filho, None if filho.tag == "li" else lista)
        yield ("fecha", filho)


def paginas_html(texto):
    """[Pagina(rotulo, ancora, texto, imagens)]: as paginas do documento, na ordem, cada uma
    com o numero impresso, o id da marca (pro link), o texto que aparece nela e o src de
    cada imagem. A pagina antes da primeira marca so existe se tiver texto ou imagem, e o
    rotulo dela e None: o numero impresso dela nao esta no documento."""
    paginas = [[None, None, [], []]]
    for ev in percorre(le_html(texto)):
        if ev[0] == "pagina":
            paginas.append([ev[1], ev[2].attrs.get("id"), [], []])
        elif ev[0] == "texto":
            paginas[-1][2].append(ev[1])
        elif ev[0] == "abre" and ev[1].tag == "img":
            paginas[-1][3].append(ev[1].attrs.get("src", ""))
    if not "".join(paginas[0][2]).split() and not paginas[0][3]:
        paginas.pop(0)
    return [Pagina(r, a, "".join(t), i) for r, a, t, i in paginas]


def alvo_markdown(caminho):
    """O caminho como alvo de um link Markdown: entre <> se tiver espaco, parentese ou <>."""
    return f"<{caminho}>" if any(c in caminho for c in " ()<>") else caminho


def caminho_do_alvo(alvo):
    return alvo[1:-1] if alvo.startswith("<") and alvo.endswith(">") else alvo


# ---------- o que os transcritores fazem do mesmo jeito ----------

def escapa(texto):
    """O texto de uma linha, com o que o Markdown leria como marca escapado: "|" sempre, e
    "#" no comeco."""
    texto = texto.replace("|", "\\|")
    return "\\" + texto if texto.startswith("#") else texto


def sem_escape(texto):
    """O texto de uma linha sem o escape de escapa(): escapa(sem_escape(linha)) devolve a
    linha escapada, tenha ela o escape ou nao."""
    texto = texto[1:] if texto.startswith("\\#") else texto
    return texto.replace("\\|", "|")


def junta(partes):
    """Os pedacos de texto numa linha so, com os espacos juntados."""
    return " ".join("".join(partes).split())


def comparavel(texto):
    """O texto so com as letras, numeros e sinais, na forma unica do Unicode (NFKC, que
    tambem desfaz indice e expoente: CO₂ fica CO2), com o sinal de menos e o hifen
    contados como o mesmo sinal."""
    return "".join(MESMO_SINAL.get(c, c) for c in unicodedata.normalize("NFKC", texto) if not c.isspace())


MARCAS_DE_INDICE = {"sup": "<super>", "sub": "<sub>"}  # como a decomposicao do Unicode marca expoente e indice


@lru_cache(maxsize=None)
def formas_de_indice(tipo):
    """{caractere, na forma comparavel: a forma dele}: os caracteres que o Unicode tem na
    forma de expoente ("sup") ou de indice ("sub") -- os que a decomposicao marca assim e
    que voltam ao caractere pela forma comparavel. Com mais de uma forma, fica a de menor
    codigo."""
    marca, formas = MARCAS_DE_INDICE[tipo], {}
    for codigo in range(sys.maxunicode + 1):
        forma = chr(codigo)
        decomposicao = unicodedata.decomposition(forma).split()
        if len(decomposicao) == 2 and decomposicao[0] == marca:
            base = comparavel(chr(int(decomposicao[1], 16)))
            if base and comparavel(forma) == base:
                formas.setdefault(base, forma)
    return formas


def em_indice(tipo, bruto):
    """O texto como expoente ("sup") ou indice ("sub"), com os caracteres do Unicode (CO₂,
    10⁻⁶), ou None se algum caractere nao tem essa forma. O espaco e o que ja esta na forma
    ficam como estao."""
    formas, marca, out = formas_de_indice(tipo), MARCAS_DE_INDICE[tipo], []
    for c in bruto:
        if c.isspace() or unicodedata.decomposition(c).startswith(marca + " "):
            out.append(c)
        elif comparavel(c) in formas:
            out.append(formas[comparavel(c)])
        else:
            return None
    return "".join(out)


def tabela_markdown(linhas, colunas):
    """A tabela no Markdown, com a primeira linha de cabecalho; cada linha e a lista do
    texto das celulas, ja escapado."""
    linha = lambda cs: "| " + " | ".join(cs) + " |"  # noqa: E731
    return "\n".join([linha(linhas[0]), "|" + "|".join("---" for _ in range(colunas)) + "|"]
                     + [linha(l) for l in linhas[1:]])


def bloco_da_figura(alvo, linhas):
    """A marca da imagem, com o caminho dela, o texto de dentro dela e o fim da imagem."""
    return [FIGURA.format(alvo_markdown(alvo))] + linhas + [FIM_FIGURA]


def converte(arquivo, formato, pasta, filtro=None):
    """O arquivo convertido pelo LibreOffice, sem abrir janela, na pasta, com o mesmo nome e
    a extensao do formato; None se o LibreOffice nao esta instalado ou nao converteu. Usa um
    perfil proprio, temporario, pra nao depender de outro LibreOffice aberto."""
    programa = shutil.which("soffice") or shutil.which("libreoffice")
    if programa is None:
        return None
    with tempfile.TemporaryDirectory() as perfil:
        subprocess.run([programa, f"-env:UserInstallation={Path(perfil).as_uri()}", "--headless", "--convert-to",
                        f"{formato}:{filtro}" if filtro else formato, "--outdir", str(pasta), str(arquivo)],
                       capture_output=True)
    saida = Path(pasta) / f"{Path(arquivo).stem}.{formato}"
    return saida if saida.is_file() else None


def copia_da_imagem(arquivo, copia):
    """(copia, problema): a imagem copiada no caminho dado, no formato da extensao dele, feita
    so se ele nao existe. O GraphicsMagick converte sem mudar o tamanho; a imagem que ele nao
    le passa pelo LibreOffice, que a desenha numa folha, e sai com fundo branco e sem a margem
    da folha."""
    if copia.exists():
        return copia, None
    gm = shutil.which("gm")
    if gm is None:
        return None, "o GraphicsMagick não está instalado"
    with tempfile.TemporaryDirectory() as temporaria:
        feita = Path(temporaria) / copia.name
        if subprocess.run([gm, "convert", str(arquivo), str(feita)], capture_output=True).returncode != 0:
            desenhada = converte(arquivo, copia.suffix.lstrip("."), Path(temporaria) / "libreoffice")
            if desenhada is not None:
                subprocess.run([gm, "convert", str(desenhada), "-background", "white", "-flatten", "-trim",
                                str(feita)], capture_output=True)
        if not feita.is_file():
            return None, "nem o GraphicsMagick nem o LibreOffice converteram a imagem"
        copia.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(feita), str(copia))
    return copia, None


def idiomas_do_ocr():
    try:
        saida = comando(["tesseract", "--list-langs"])
    except FileNotFoundError:
        raise SystemExit("ERRO: o Tesseract não está instalado -- veja \"Antes da primeira vez\" no README dos scripts")
    return {l.strip() for l in saida.split("\n")[1:] if l.strip()}


def confere_idioma_do_ocr(idioma):
    """Para o script se o Tesseract nao esta instalado ou nao tem os dados do idioma
    ("por", "spa+eng"...)."""
    faltam = [i for i in idioma.split("+") if i not in idiomas_do_ocr()]
    if faltam:
        raise SystemExit("ERRO: o Tesseract não tem os dados do idioma " + ", ".join(faltam) + " -- no Linux: "
                         + " ".join(f"sudo apt install tesseract-ocr-{i}" for i in faltam))


def texto_da_imagem(arquivo, idioma):
    """(linhas, aviso): o texto escrito dentro da imagem, lido pelo Tesseract, um pedaco por
    linha, ja escapado. A imagem num formato que o Tesseract nao le passa antes pro PNG pelo
    LibreOffice. Sem leitura, as linhas vem vazias e o aviso diz por que."""
    with tempfile.TemporaryDirectory() as temporaria:
        lida = Path(arquivo)
        if lida.suffix.lower() not in FORMATOS_DO_OCR:
            lida = converte(lida, "png", temporaria)
            if lida is None:
                return [], (f"a imagem {Path(arquivo).name} está num formato que o Tesseract não lê, e o LibreOffice, "
                            "que a passaria pro PNG, não está instalado ou não a converteu: ficou sem o texto dela")
        try:
            lido = comando(["tesseract", str(lida), "stdout", "-l", idioma, "--psm", MODO_OCR]).replace("\f", "")
        except subprocess.CalledProcessError as e:
            return [], f"o Tesseract não leu a imagem {Path(arquivo).name} ({' '.join(e.stderr.split())}): ficou sem o texto dela"
    return [escapa(l.strip()) for l in lido.split("\n") if l.strip()], None


def registro_da_transcricao(saida, substituir):
    """As linhas do registro da fonte da transcricao que ja existe ([] se ela nao existe), ou
    None se ela existe e nao e pra fazer de novo: o texto das imagens dela pode ja estar
    conferido."""
    if not saida.exists():
        return []
    if not substituir:
        print(f"Já existe: {saida} (pode ter o texto das imagens conferido; pra fazer de novo por cima, use "
              "--substituir)")
        return None
    return separa_registro(saida.read_text(encoding="utf-8"))[0]


def grava_transcricao(saida, registro, texto):
    """Grava a transcricao, com o registro da fonte no topo, se ele existe."""
    saida.parent.mkdir(parents=True, exist_ok=True)
    saida.write_text("\n".join(["---"] + registro + ["---", "", ""] if registro else []) + texto, encoding="utf-8")


def lembra_registro(projeto, transcricao, fonte):
    relativo = lambda c: Path(os.path.relpath(Path(c).resolve(), projeto.raiz)).as_posix()  # noqa: E731
    print(f"FALTA: registrar de qual arquivo a transcrição veio: python scripts/registrar_fonte.py "
          f"{relativo(transcricao)} {relativo(fonte)} [chave]")


# ---------- fonte em pptx (apresentacao de slides) ----------

Paragrafo = namedtuple("Paragrafo", "nivel marcador linhas")  # linhas: [[(texto, None | "sup" | "sub")]]
Bloco = namedtuple("Bloco", "tipo conteudo")  # "titulo" e "texto": [Paragrafo]; "tabela": [[[Paragrafo]]]; "imagem": Imagem
Imagem = namedtuple("Imagem", "parte recortada")  # a parte do pacote (o arquivo dentro do pptx)
Slide = namedtuple("Slide", "numero oculto blocos notas avisos")
FILTRO_PDF = 'impress_pdf_Export:{"ExportHiddenSlides":{"type":"boolean","value":"true"}}'  # o PDF com todos os slides
BALAS = ("buNone", "buChar", "buAutoNum", "buBlip")  # o que diz se o paragrafo tem marcador, e qual
TITULOS_PPTX = ("title", "ctrTitle")  # tipos de espaco reservado que sao o titulo do slide
DO_RODAPE = ("dt", "ftr", "sldNum", "hdr")  # tipos de espaco reservado com o estilo "other" do mestre
NUMERACAO = re.compile(r"^(arabic|alphaLc|alphaUc|romanLc|romanUc)(Period|ParenR|ParenBoth|Plain)$")


class FonteIlegivel(Exception):
    """A fonte nao se le: o arquivo esta incompleto ou nao e do tipo que diz ser."""


def q(nome):
    """"a:p" -> o nome completo do elemento, com o espaco de nomes."""
    prefixo, local = nome.split(":")
    return f"{{{NS[prefixo]}}}{local}"


def local(elemento):
    return elemento.tag.rsplit("}", 1)[-1]


def filhos(elemento):
    """Os filhos do elemento; no lugar de uma alternativa (mc:AlternateContent), os da
    versao de reserva (mc:Fallback), que e a que vale pra quem nao le as extensoes, ou, sem
    ela, os da primeira opcao."""
    for filho in elemento:
        if filho.tag == q("mc:AlternateContent"):
            versao = filho.find(q("mc:Fallback"))
            if versao is None:
                versao = filho.find(q("mc:Choice"))
            if versao is not None:
                yield from filhos(versao)
        else:
            yield filho


def romano(n):
    out = ""
    for valor, letras in ((1000, "m"), (900, "cm"), (500, "d"), (400, "cd"), (100, "c"), (90, "xc"), (50, "l"),
                          (40, "xl"), (10, "x"), (9, "ix"), (5, "v"), (4, "iv"), (1, "i")):
        out += letras * (n // valor)
        n %= valor
    return out


def numero_do_item(esquema, n):
    """(marcador, conhecido): o numero do item no esquema de numeracao do pptx (arabicPeriod
    -> "1. ", alphaLcParenR -> "a) "...); o esquema que nao e de algarismos, letras ou
    romanos sai em algarismos, com ponto, e conhecido False."""
    m = NUMERACAO.match(esquema or "")
    if not m:
        return f"{n}. ", False
    tipo, forma = m.groups()
    valor = {"arabic": str(n), "alphaLc": chr(97 + (n - 1) % 26) * ((n - 1) // 26 + 1), "romanLc": romano(n)}.get(
        tipo, None)
    if valor is None:
        valor = {"alphaUc": chr(97 + (n - 1) % 26) * ((n - 1) // 26 + 1), "romanUc": romano(n)}[tipo].upper()
    return {"Period": f"{valor}. ", "ParenR": f"{valor}) ", "ParenBoth": f"({valor}) ", "Plain": f"{valor} "}[forma], True


@lru_cache(maxsize=None)
def tabela_de_simbolos():
    """{nome da fonte em minusculas: {codigo hexadecimal: caractere}} (normas/simbolos.json)."""
    tabela, erros = le_dados(ARQUIVO_SIMBOLOS, esquema("simbolos"))
    if erros:
        raise SystemExit("\n".join(f"ERRO em {e}" for e in erros))
    return {fonte.casefold(): codigos for fonte, codigos in tabela["fontes"].items()}


class Apresentacao:
    """Uma apresentacao em pptx, lida direto do pacote (um zip de XML), so com a biblioteca
    padrao. Os slides vem na ordem da apresentacao, e cada um com os blocos na ordem do
    arquivo, que e a ordem em que o PowerPoint os le em voz alta: titulo e texto (com o
    marcador e o nivel de cada paragrafo, herdados do layout e do mestre quando o paragrafo
    nao diz), tabela, imagem (a de fundo do slide primeiro), o texto de um SmartArt, a
    imagem de previa de um objeto incorporado. O que nao tem leitura vira aviso."""

    def __init__(self, arquivo):
        self.arquivo = Path(arquivo)
        try:
            self.pacote = zipfile.ZipFile(self.arquivo)
        except (zipfile.BadZipFile, OSError) as e:
            raise FonteIlegivel(f"{self.arquivo.name} não se lê como pptx ({e}); o arquivo pode estar incompleto")
        self.partes = set(self.pacote.namelist())
        self._xml = {}
        principal = self.relacionada("", "officeDocument")
        if principal is None:
            raise FonteIlegivel(f"{self.arquivo.name} não tem a apresentação dentro do pacote")
        self.principal = principal

    def bytes(self, parte):
        return self.pacote.read(parte)

    def xml(self, parte):
        if parte not in self._xml:
            self._xml[parte] = ET.fromstring(self.pacote.read(parte)) if parte in self.partes else None
        return self._xml[parte]

    def relacoes(self, parte):
        """{id: (tipo, parte de destino ou None se o destino e de fora do pacote)}; o tipo e o
        fim do endereco dele ("slide", "image", "slideLayout"...)."""
        pasta, nome = posixpath.split(parte)
        arquivo = posixpath.join(pasta, "_rels", nome + ".rels")
        if arquivo not in self.partes:
            return {}
        out = {}
        for r in ET.fromstring(self.pacote.read(arquivo)):
            alvo = r.get("Target", "")
            if r.get("TargetMode") == "External":
                destino = None
            elif alvo.startswith("/"):
                destino = alvo[1:]
            else:
                destino = posixpath.normpath(posixpath.join(pasta, alvo))
            out[r.get("Id")] = (r.get("Type", "").rsplit("/", 1)[-1], destino)
        return out

    def relacionada(self, parte, tipo):
        return next((d for t, d in self.relacoes(parte).values() if t == tipo and d), None)

    # ---- os slides ----

    def slides(self):
        raiz, relacoes = self.xml(self.principal), self.relacoes(self.principal)
        lista = raiz.find(q("p:sldIdLst"))
        out = []
        for numero, item in enumerate(lista if lista is not None else [], 1):
            parte = relacoes.get(item.get(q("r:id")), (None, None))[1]
            out.append(self.slide(numero, parte))
        return out

    def slide(self, numero, parte):
        avisos, blocos = [], []
        raiz = self.xml(parte) if parte else None
        if raiz is None:
            return Slide(numero, False, [], [], ["o slide não está no pacote"])
        contexto = {"parte": parte, "avisos": avisos}
        fundo = raiz.find(f"{q('p:cSld')}/{q('p:bg')}/{q('p:bgPr')}/{q('a:blipFill')}")
        if fundo is not None:
            blocos += self.imagem(contexto, fundo)
        arvore = raiz.find(f"{q('p:cSld')}/{q('p:spTree')}")
        if arvore is not None:
            blocos += self.formas(contexto, arvore)
        return Slide(numero, raiz.get("show") in ("0", "false"), blocos, self.notas(parte), avisos)

    def formas(self, contexto, arvore):
        out = []
        for forma in filhos(arvore):
            nome = local(forma)
            if nome == "sp":
                out += self.forma(contexto, forma)
            elif nome == "grpSp":
                out += self.formas(contexto, forma)
            elif nome == "pic":
                out += self.imagem(contexto, forma.find(q("p:blipFill")))
            elif nome == "graphicFrame":
                out += self.quadro(contexto, forma)
            elif nome not in ("nvGrpSpPr", "grpSpPr", "extLst", "cxnSp"):
                contexto["avisos"].append(f"um elemento {nome} não tem leitura: ficou de fora")
        return out

    def forma(self, contexto, forma):
        out = []
        preenchimento = forma.find(f"{q('p:spPr')}/{q('a:blipFill')}")
        if preenchimento is not None:
            out += self.imagem(contexto, preenchimento)
        corpo = forma.find(q("p:txBody"))
        if corpo is not None:
            ph = forma.find(f"{q('p:nvSpPr')}/{q('p:nvPr')}/{q('p:ph')}")
            paragrafos = self.paragrafos(corpo, self.estilos(contexto["parte"], ph, corpo), contexto["avisos"])
            if paragrafos:
                titulo = ph is not None and ph.get("type") in TITULOS_PPTX
                out.append(Bloco("titulo" if titulo else "texto", paragrafos))
        return out

    def imagem(self, contexto, preenchimento):
        """[Bloco da imagem] de um preenchimento com imagem (blipFill)."""
        blip = preenchimento.find(q("a:blip")) if preenchimento is not None else None
        if blip is None:
            return []
        relacoes = self.relacoes(contexto["parte"])
        destino = relacoes.get(blip.get(q("r:embed")), (None, None))[1]
        if destino is None or destino not in self.partes:
            contexto["avisos"].append("uma imagem não está dentro do pptx (é um link ou falta no pacote): ficou de fora")
            return []
        recorte = preenchimento.find(q("a:srcRect"))
        recortada = recorte is not None and any(int(recorte.get(k, "0") or 0) for k in "ltrb")
        return [Bloco("imagem", Imagem(destino, recortada))]

    def quadro(self, contexto, quadro):
        dados = quadro.find(f"{q('a:graphic')}/{q('a:graphicData')}")
        tipo = (dados.get("uri", "") if dados is not None else "").rsplit("/", 1)[-1]
        if tipo == "table":
            return self.tabela(contexto, dados.find(q("a:tbl")))
        if tipo == "diagram":
            return self.smartart(contexto, dados.find(q("dgm:relIds")))
        if tipo == "ole":
            objeto = next((f for f in filhos(dados) if local(f) == "oleObj"), None)
            figura = objeto.find(q("p:pic")) if objeto is not None else None
            if figura is not None:
                return self.imagem(contexto, figura.find(q("p:blipFill")))
            contexto["avisos"].append("um objeto incorporado não tem imagem de prévia: ficou de fora")
            return []
        if tipo == "chart":
            contexto["avisos"].append("um gráfico: o texto dele não foi lido, só aparece na imagem do slide")
            return []
        contexto["avisos"].append(f"um objeto do tipo {tipo or 'desconhecido'} não tem leitura: ficou de fora")
        return []

    def tabela(self, contexto, tabela):
        if tabela is None:
            return []
        padrao = self.estilos(contexto["parte"], None, None)
        linhas = [[self.paragrafos(celula.find(q("a:txBody")), padrao, contexto["avisos"])
                   if celula.find(q("a:txBody")) is not None else [] for celula in linha.findall(q("a:tc"))]
                  for linha in tabela.findall(q("a:tr"))]
        return [Bloco("tabela", linhas)] if linhas else []

    def smartart(self, contexto, ids):
        """O texto do SmartArt como aparece no slide: o do desenho dele, forma por forma; sem
        o desenho, o dos dados, na ordem deles, com aviso."""
        relacoes = self.relacoes(contexto["parte"])
        dados = relacoes.get(ids.get(q("r:dm")) if ids is not None else None, (None, None))[1]
        raiz = self.xml(dados) if dados else None
        if raiz is None:
            contexto["avisos"].append("um SmartArt sem os dados dele: ficou de fora")
            return []
        extensao = raiz.find(f".//{q('dsp:dataModelExt')}")
        desenho = relacoes.get(extensao.get("relId") if extensao is not None else None, (None, None))[1]
        desenho = self.xml(desenho) if desenho else None
        out = []
        if desenho is not None:
            for forma in desenho.iter():
                corpo = forma.find(q("dsp:txBody")) if local(forma) == "sp" else None
                if corpo is not None:
                    paragrafos = self.paragrafos(corpo, [corpo.find(q("a:lstStyle"))], contexto["avisos"])
                    if paragrafos:
                        out.append(Bloco("texto", paragrafos))
            return out
        contexto["avisos"].append("um SmartArt sem o desenho: o texto saiu na ordem dos dados, não na do slide")
        for ponto in raiz.iter(q("dgm:pt")):
            corpo = ponto.find(q("dgm:t"))
            if corpo is not None and ponto.get("type", "node") == "node":
                paragrafos = self.paragrafos(corpo, [], contexto["avisos"])
                if paragrafos:
                    out.append(Bloco("texto", paragrafos))
        return out

    def notas(self, parte):
        """[Paragrafo] das notas do apresentador do slide (o corpo das notas)."""
        notas = self.relacionada(parte, "notesSlide")
        raiz = self.xml(notas) if notas else None
        out = []
        if raiz is not None:
            for forma in raiz.iter(q("p:sp")):
                ph = forma.find(f"{q('p:nvSpPr')}/{q('p:nvPr')}/{q('p:ph')}")
                corpo = forma.find(q("p:txBody"))
                if ph is not None and ph.get("type") == "body" and corpo is not None:
                    out += self.paragrafos(corpo, [corpo.find(q("a:lstStyle"))], [])
        return out

    # ---- o texto ----

    def estilos(self, parte, ph, corpo):
        """Os estilos de lista que valem pro texto, do mais proximo ao mais geral: o da propria
        forma; num espaco reservado, o do espaco reservado correspondente no layout e no
        mestre e o estilo do mestre pro tipo dele (titulo, corpo ou o resto); por fim, o
        estilo padrao da apresentacao."""
        out = [corpo.find(q("a:lstStyle")) if corpo is not None else None]
        if ph is not None:
            tipo = ph.get("type", "obj")
            layout = self.relacionada(parte, "slideLayout")
            mestre = self.relacionada(layout, "slideMaster") if layout else None
            tipo_no_mestre = "title" if tipo in TITULOS_PPTX else tipo if tipo in DO_RODAPE else "body"
            for p, t, idx in ((layout, tipo, ph.get("idx")), (mestre, tipo_no_mestre, None)):
                igual = self.espaco_reservado(p, t, idx) if p else None
                out.append(igual.find(f"{q('p:txBody')}/{q('a:lstStyle')}") if igual is not None else None)
            estilos = self.xml(mestre).find(q("p:txStyles")) if mestre and self.xml(mestre) is not None else None
            if estilos is not None:
                nome = {"title": "titleStyle", "body": "bodyStyle"}.get(tipo_no_mestre, "otherStyle")
                out.append(estilos.find(q(f"p:{nome}")))
        out.append(self.xml(self.principal).find(q("p:defaultTextStyle")))
        return out

    def espaco_reservado(self, parte, tipo, idx):
        """A forma da parte (layout ou mestre) que e o espaco reservado com o mesmo indice ou,
        sem ele, do mesmo tipo."""
        raiz = self.xml(parte)
        if raiz is None:
            return None
        formas = [(f, f.find(f"{q('p:nvSpPr')}/{q('p:nvPr')}/{q('p:ph')}")) for f in raiz.iter(q("p:sp"))]
        formas = [(f, ph) for f, ph in formas if ph is not None]
        return (next((f for f, ph in formas if idx is not None and ph.get("idx") == idx), None)
                or next((f for f, ph in formas if ph.get("type", "obj") == tipo), None))

    def paragrafos(self, corpo, estilos, avisos):
        """[Paragrafo] do corpo de texto, so os que tem texto, cada um com o nivel e o marcador
        ("- ", ou o numero na lista numerada, contado dentro do corpo)."""
        out, contagem = [], {}
        for p in corpo.findall(q("a:p")):
            linhas = self.linhas(p, avisos)
            if not "".join(t for linha in linhas for t, _ in linha).strip():
                continue
            propriedades = p.find(q("a:pPr"))
            nivel = int(propriedades.get("lvl", "0")) if propriedades is not None else 0
            for k in [k for k in contagem if k > nivel]:
                del contagem[k]
            bala = self.bala(propriedades, nivel, estilos)
            marcador = ""
            if bala is not None and local(bala) == "buAutoNum":
                esquema, inicio = bala.get("type"), int(bala.get("startAt", "1"))
                anterior = contagem.get(nivel)
                n = anterior[2] + 1 if anterior and anterior[:2] == (esquema, inicio) else inicio
                contagem[nivel] = (esquema, inicio, n)
                marcador, conhecido = numero_do_item(esquema, n)
                if not conhecido:
                    avisos.append(f"numeração do tipo {esquema}: saiu em algarismos")
            else:
                contagem.pop(nivel, None)
                if bala is not None and local(bala) in ("buChar", "buBlip"):
                    marcador = "- "
            out.append(Paragrafo(nivel, marcador, linhas))
        return out

    @staticmethod
    def bala(propriedades, nivel, estilos):
        """O elemento que diz o marcador do paragrafo: o do proprio paragrafo ou, sem ele, o
        do nivel dele no primeiro estilo que diz."""
        candidatos = [propriedades]
        for estilo in estilos:
            if estilo is not None:
                candidatos += [estilo.find(q(f"a:lvl{nivel + 1}pPr")), estilo.find(q("a:defPPr"))]
        for elemento in candidatos:
            if elemento is not None:
                bala = next((f for f in elemento if local(f) in BALAS), None)
                if bala is not None:
                    return bala
        return None

    def linhas(self, paragrafo, avisos):
        """[[(texto, None | "sup" | "sub")]]: o texto do paragrafo, em linhas (a quebra de
        linha dentro dele abre outra), com o caractere da fonte de simbolos trocado pelo do
        Unicode."""
        linhas = [[]]
        for elemento in filhos(paragrafo):
            nome = local(elemento)
            if nome in ("r", "fld"):
                propriedades = elemento.find(q("a:rPr"))
                texto = self.simbolos(elemento.findtext(q("a:t")) or "", propriedades, avisos)
                deslocamento = (propriedades.get("baseline", "0") if propriedades is not None else "0").rstrip("%")
                deslocamento = float(deslocamento or 0)
                linhas[-1].append((texto, "sup" if deslocamento > 0 else "sub" if deslocamento < 0 else None))
            elif nome == "br":
                linhas.append([])
        return linhas

    @staticmethod
    def simbolos(texto, propriedades, avisos):
        """O texto com cada caractere de uma fonte de simbolos (como a Symbol) trocado pelo do
        Unicode, pela tabela da fonte: o que fica na area F000-F0FF, na fonte de simbolos
        (sym) do trecho ou na fonte dele (latin), e o que fica entre 20 e FF quando a fonte
        do trecho e de simbolos."""
        fonte = lambda nome: (propriedades.find(q(nome)).get("typeface", "")  # noqa: E731
                              if propriedades is not None and propriedades.find(q(nome)) is not None else "")
        tabelas, simbolo, latina, out = tabela_de_simbolos(), fonte("a:sym"), fonte("a:latin"), []
        for c in texto:
            codigo = ord(c)
            if codigo in SIMBOLOS_PRIVADOS:
                nome, codigo = simbolo or latina, codigo - SIMBOLOS_PRIVADOS.start
            elif codigo <= 0xFF:
                nome = latina
            else:
                out.append(c)
                continue
            tabela = tabelas.get(nome.casefold())
            trocado = tabela.get(f"{codigo:02X}") if tabela else None
            if trocado is None and ord(c) in SIMBOLOS_PRIVADOS:
                avisos.append(f"o caractere U+{ord(c):04X}, da fonte {nome or '(sem nome)'}, não está na tabela "
                              f"{ARQUIVO_SIMBOLOS.name}: ficou como está")
            out.append(trocado or c)
        return "".join(out)


def texto_do_slide(slide):
    """O texto do slide que a transcricao copia, na ordem: o marcador e o texto de cada
    paragrafo, o das celulas das tabelas e o das notas."""
    paragrafos = []
    for bloco in slide.blocos:
        if bloco.tipo in ("titulo", "texto"):
            paragrafos += bloco.conteudo
        elif bloco.tipo == "tabela":
            paragrafos += [p for linha in bloco.conteudo for celula in linha for p in celula]
    return "\n".join(p.marcador + "".join(t for linha in p.linhas for t, _ in linha)
                     for p in paragrafos + list(slide.notas))


def pdf_dos_slides(fonte, pdf):
    """(pdf, problema): o PDF da apresentacao, com todos os slides, feito pelo LibreOffice no
    caminho dado, de novo so se nao existe ou se a apresentacao e mais nova; sem ele, o
    problema diz por que."""
    if not pdf.exists() or pdf.stat().st_mtime < Path(fonte).stat().st_mtime:
        pdf.parent.mkdir(parents=True, exist_ok=True)
        with tempfile.TemporaryDirectory() as temporaria:
            feito = converte(fonte, "pdf", temporaria, FILTRO_PDF)
            if feito is None:
                return None, "o LibreOffice não está instalado ou não converteu a apresentação"
            shutil.move(str(feito), str(pdf))
    return pdf, None
