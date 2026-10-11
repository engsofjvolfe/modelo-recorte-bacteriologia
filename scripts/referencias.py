# SPDX-License-Identifier: GPL-3.0-or-later
# Copyright do codigo sob GPL-3.0 -- ver LICENSE e NOTICE.md na raiz do projeto.

"""
Monta as referencias do projeto a partir dos dados. Le o arquivo de fontes, confere o
arquivo contra o schema dele, formata cada fonte pela ABNT NBR 6023 e grava:

  - o arquivo de referencias: so as referencias, em ordem alfabetica, como a lista de
    referencias do fim de um trabalho;
  - a conferencia das referencias: para cada fonte, a referencia como ficou, a chamada
    dela no texto (NBR 10520, sistema autor-data), a copia registrada dela (com a imagem
    da primeira pagina, se for PDF, pra conferir contra a folha de rosto) e as caixas de
    tique "IA" e "pessoa". Se a referencia, a chamada ou a copia mudarem depois do tique,
    o tique e retirado. A copia entra na assinatura do tique pelo caminho do registro, a
    partir da pasta principal do projeto, e pela impressao digital registrada: mudar a
    pasta do projeto de lugar nao retira o tique.

Os caminhos vem do projeto.json: "fontes", "referencias", "conferencia_referencias",
"gerados", "licenca_conteudo", "imagens" e "formato" (de onde vem o idioma do texto, que
e o da data de acesso); a resolucao das imagens, de "resolucao_imagens"; e o nome da
licenca do conteudo, do rodape do arquivo de referencias, de "nome_licenca_conteudo". A abreviatura
dos meses em cada idioma vem de normas/meses.json, na pasta deste script. O formato da
disciplina pode faltar. O arquivo de fontes, a tabela dos meses e o formato, se existe,
sao lidos pela leitura de todo arquivo de dados (validar_dados.le_dados), cada um contra o
molde dele: com erro em qualquer um -- texto fora do UTF-8, JSON invalido ou fora do
molde --, cada erro aparece com ERRO, com o nome do arquivo, e nada e gravado.

A copia de cada fonte e achada pelo registro no topo dos documentos gerados (ver
registrar_fonte.py), pela chave. O script lista no terminal as chaves registradas que
ainda nao tem referencia e as referencias que faltam conferir.

Tipos de fonte: "monografia" (livro, guia, manual, documento ou pagina online, material
de aula), "parte" (capitulo ou parte de uma monografia), "artigo" (de periodico) e
"outro" (a referencia vem pronta, no campo "referencia", e so passa pela conferencia).
Sem autoria, a entrada e pelo titulo, que vai nos dados ja com a primeira palavra em
maiusculas (e a seguinte, se a primeira for artigo ou monossilabo), como a norma pede.

O que depende de escolha ou de dado:
  - "et_al", no arquivo de fontes: com quatro autores ou mais, so o primeiro, seguido de
    et al., na referencia e na chamada, igual para todas as fontes;
  - "participacao" (org., coord., ed., comp.): uma vez, depois do ultimo nome;
  - "idioma" da fonte: o mes da data sai abreviado no idioma da publicacao;
  - mesma chamada e mesmo ano em fontes diferentes: se forem pessoas diferentes com o
    mesmo sobrenome, a chamada ganha as iniciais dos prenomes (ou os prenomes, se as
    iniciais tambem coincidirem); se ainda coincidir, letras depois do ano (2020a,
    2020b), na chamada e na referencia, na ordem da lista.

Uso (de qualquer pasta dentro do projeto):
    python scripts/referencias.py
    python scripts/referencias.py --projeto projeto.json
"""

import argparse
import json
import re
import string
import sys
import unicodedata
from collections import namedtuple
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from comum import (PASTA_NORMAS, acha_projeto, ancora, assinatura, caixas, fontes_registradas, imagem,  # noqa: E402
                   le_formato, lingua, link, marca, rodape_da_licenca, situacao_da_copia, tiques_anteriores,
                   tiques_da_parte)
from validar_dados import esquema, le_dados  # noqa: E402

ARQUIVO_MESES = PASTA_NORMAS / "meses.json"
DATA = re.compile(r"(\d{4})(?:-(\d{2})(?:-(\d{2}))?)?")
SITUACAO = {"confere": "é a mesma do registro", "mudou": "mudou depois do registro", "nao-existe": "não existe"}

# et_al: a escolha do arquivo de fontes; meses: {idioma: abreviaturas}; texto: idioma do texto
Regras = namedtuple("Regras", "et_al meses texto")


def sem_fontes(fontes):
    """O aviso de que o arquivo de fontes ainda nao existe."""
    return f"{fontes} não existe -- crie a partir de modelo-dados/fontes.json"


# ---------- formatacao pela NBR 6023 ----------

def data_abnt(valor, idioma, meses, letra=""):
    """"2024-09-04" -> "4 set. 2024"; "2024-09" -> "set. 2024"; "2024" -> "2024". O mes sai
    no idioma dado e a letra (2024a), logo depois do ano. Outro valor fica como esta."""
    m = DATA.fullmatch(valor)
    if not m:
        return valor + letra
    ano, mes, dia = m.groups()
    if not mes:
        return ano + letra
    texto = f"{meses[idioma][int(mes) - 1]} {ano}{letra}"
    return f"{int(dia)} {texto}" if dia else texto


def ponto(texto):
    """Fecha o elemento com ponto, se ele ja nao acaba em pontuacao (mesmo dentro de um
    destaque, como em *et al.*)."""
    texto = texto.rstrip()
    return texto if texto.rstrip("*").endswith((".", "?", "!")) else texto + "."


def autor(a):
    if "entidade" in a:
        primeiro = a["entidade"][0].upper() + (f" ({a['qualificador']})" if a.get("qualificador") else "")
        return ". ".join([primeiro] + a["entidade"][1:])
    return a["sobrenome"].upper() + (f", {a['prenomes']}" if a.get("prenomes") else "")


def autoria(obra, r):
    autores = obra["autores"]
    corta = r.et_al and len(autores) >= 4
    texto = "; ".join(autor(a) for a in (autores[:1] if corta else autores)) + (" *et al.*" if corta else "")
    return texto + (f" ({obra['participacao']})" if obra.get("participacao") else "")


def titulo(obra, destaque):
    t = f"**{obra['titulo']}**" if destaque else obra["titulo"]
    return t + (f": {obra['subtitulo']}" if obra.get("subtitulo") else "")


def publicacao(obra, data):
    """Local: editora, data -- com [S. l.] e [s. n.] onde faltar."""
    local, editora = obra.get("local"), obra.get("editora")
    if local and editora:
        texto = f"{local}: {editora}"
    elif local:
        texto = f"{local}: [*s. n.*]"
    elif editora:
        texto = f"[*S. l.*]: {editora}"
    else:
        texto = "[*S. l.*: *s. n.*]"
    return f"{texto}, {data}"


def obra_inteira(obra, r, idioma, letra):
    """Elementos de uma monografia: titulo (com destaque se ha autoria), edicao e publicacao."""
    tem_autoria = bool(obra.get("autores"))
    els = ([autoria(obra, r)] if tem_autoria else []) + [titulo(obra, tem_autoria)]
    if obra.get("edicao"):
        els.append(obra["edicao"])
    return els + [publicacao(obra, data_abnt(obra["data"], idioma, r.meses, letra))]


def referencia(f, r, letra=""):
    if f["tipo"] == "outro":
        return f["referencia"]
    idioma = lingua(f.get("idioma"))
    if f["tipo"] == "monografia":
        els = obra_inteira(f, r, idioma, letra)
    elif f["tipo"] == "parte":
        els = ([autoria(f, r)] if f.get("autores") else []) + [titulo(f, False)]
        livro = obra_inteira(f["parte_de"], r, idioma, letra)
        els += ["*In*: " + livro[0]] + livro[1:] + [f"p. {f['paginas']}"]
    else:  # artigo
        els = ([autoria(f, r)] if f.get("autores") else []) + [titulo(f, False)]
        pub = [f"**{f['periodico']}**"] + [f[c] for c in ("local",) if f.get(c)]
        pub += [f"{p} {f[c]}" for c, p in (("volume", "v."), ("numero", "n."), ("paginas", "p.")) if f.get(c)]
        els.append(", ".join(pub + [data_abnt(f["data"], idioma, r.meses, letra)]))
    if f.get("descricao_fisica"):
        els.append(f["descricao_fisica"])
    if f.get("serie"):
        els.append(f"({f['serie']})")
    els += f.get("notas", [])
    if f.get("isbn"):
        els.append(f"ISBN {f['isbn']}")
    if f.get("doi"):
        els.append(f"DOI: {f['doi']}")
    if f.get("url"):
        els.append(f"Disponível em: {f['url']}")
    if f.get("acesso"):
        els.append(f"Acesso em: {data_abnt(f['acesso'], r.texto, r.meses)}")
    return " ".join(ponto(e) for e in els)


def ordem(texto):
    """Chave de ordem alfabetica: sem destaque, sem colchetes, sem acento, em maiusculas, e
    numero pelo valor (9 antes de 12)."""
    simples = unicodedata.normalize("NFKD", re.sub(r"[*\[\]]", "", texto))
    simples = "".join(c for c in simples if not unicodedata.combining(c)).upper()
    return [int(p) if p.isdigit() else p for p in re.split(r"(\d+)", simples)]


def erros_de_idioma(fontes, r):
    """Datas com mes cujo idioma nao esta na tabela dos meses."""
    erros = []
    for f in fontes:
        datas = [f.get("data"), f.get("parte_de", {}).get("data")]
        if any(d and DATA.fullmatch(d) and DATA.fullmatch(d).group(2) for d in datas) \
                and lingua(f.get("idioma")) not in r.meses:
            erros.append(f"a fonte {f['chave']} tem idioma {f.get('idioma')!r}, que a tabela dos meses "
                         f"({ARQUIVO_MESES.name}) não traz: escreva a data como está na publicação")
        acesso = f.get("acesso")
        if acesso and DATA.fullmatch(acesso) and DATA.fullmatch(acesso).group(2) and r.texto not in r.meses:
            erros.append(f"a fonte {f['chave']} tem data de acesso, cujo mês sai no idioma do texto, que é o "
                         "\"idioma\" do formato da disciplina: "
                         + ("o formato ainda não existe" if r.texto is None else
                            f"{r.texto!r} não está na tabela dos meses ({ARQUIVO_MESES.name})"))
    return erros


# ---------- chamada no texto pela NBR 10520 (autor-data) ----------

def ano(f):
    data = f.get("data") or f.get("parte_de", {}).get("data", "")
    m = DATA.fullmatch(data)
    return m.group(1) if m else data


def nomes_da_chamada(f):
    """Os nomes da chamada, cada um como (entre parenteses, na frase): o sobrenome de cada
    pessoa ou o primeiro nome de cada entidade, como estao escritos nos dados; sem autoria,
    as palavras do comeco do titulo que estao em maiusculas, seguidas de [...] se o titulo
    continua."""
    if f.get("autores"):
        return [(n, n) for n in (a.get("sobrenome") or a["entidade"][0] for a in f["autores"])]
    palavras = f["titulo"].split()
    n = next((i for i, p in enumerate(palavras) if p != p.upper() or not any(c.isalpha() for c in p)),
             len(palavras))
    n = max(n, 1)
    inicio = " ".join(palavras[:n]).rstrip(",;:.").lower()
    letra = next((i for i, c in enumerate(inicio) if c.isalpha()), 0)
    inicio = inicio[:letra] + inicio[letra:letra + 1].upper() + inicio[letra + 1:]
    inicio += "]" * (inicio.count("[") - inicio.count("]")) + (" [...]" if len(palavras) > n else "")
    return [(inicio, inicio)]


def chamada(nomes, ano_e_letra, r):
    """(entre parenteses, na frase): "(Silva; Souza, 2020)" e "Silva e Souza (2020)"."""
    if r.et_al and len(nomes) >= 4:
        dentro, fora = f"{nomes[0][0]} *et al.*", f"{nomes[0][1]} *et al.*"
    else:
        dentro = "; ".join(d for d, _ in nomes)
        frase = [f for _, f in nomes]
        fora = frase[0] if len(frase) == 1 else ", ".join(frase[:-1]) + " e " + frase[-1]
    return f"({dentro}, {ano_e_letra})", f"{fora} ({ano_e_letra})"


def iniciais(prenomes):
    """"Maria Cecília" -> "M. C."; "I. N. de" -> "I. N." (partícula em minúscula fica de fora)."""
    return " ".join(p[0] + "." for p in prenomes.replace(".", " ").split() if p[0].isupper())


def iguais(fontes, nomes):
    """Grupos de fontes com os mesmos nomes de chamada e o mesmo ano."""
    grupos = {}
    for f in fontes:
        grupos.setdefault((tuple(d for d, _ in nomes[f["chave"]]), ano(f)), []).append(f)
    return [g for g in grupos.values() if len(g) > 1]


def desempata(fontes, nomes, r):
    """{chave: letra}. Muda em "nomes" o primeiro nome dos grupos de pessoas diferentes."""
    for grupo in iguais(fontes, nomes):
        primeiros = [(f.get("autores") or [{}])[0] for f in grupo]
        pessoas = {json.dumps(a, ensure_ascii=False, sort_keys=True): a for a in primeiros}
        if len(pessoas) < 2 or not all(a.get("sobrenome") and a.get("prenomes") for a in primeiros):
            continue
        curtas = {iniciais(a["prenomes"]) for a in pessoas.values()}
        forma = iniciais if len(curtas) == len(pessoas) else (lambda p: p)
        for f, a in zip(grupo, primeiros):
            nomes[f["chave"]][0] = (f"{a['sobrenome']}, {forma(a['prenomes'])}", f"{forma(a['prenomes'])} {a['sobrenome']}")
    letras = {}
    for grupo in iguais(fontes, nomes):
        grupo.sort(key=lambda f: ordem(referencia(f, r)))
        letras.update((f["chave"], letra) for f, letra in zip(grupo, string.ascii_lowercase))
    return letras


# ---------- arquivos ----------

def copias_registradas(transcricoes, raiz):
    """{chave: [(documento, caminho, arquivo, situacao, hash registrado)]} dos registros dos
    documentos gerados. O caminho e o do registro, a partir da pasta principal do projeto; o
    arquivo e o mesmo caminho, completo, no computador onde o script roda."""
    out = {}
    for doc in sorted(transcricoes.glob("*.md")):
        for chave, (caminho, hash_registrado) in fontes_registradas(doc.read_text(encoding="utf-8")).items():
            arquivo, situacao = situacao_da_copia(raiz, caminho, hash_registrado)
            out.setdefault(chave, []).append((doc, caminho, arquivo, situacao, hash_registrado))
    return out


def grava_fontes_md(refs, saida, licenca, nome_licenca):
    corpo = ["# Referências", ""] + [linha for _, r in refs for linha in (r, "")]
    corpo += rodape_da_licenca(licenca, nome_licenca, saida)
    saida.parent.mkdir(parents=True, exist_ok=True)
    saida.write_text("\n".join(corpo) + "\n", encoding="utf-8")


def grava_conferencia(refs, chamadas, fontes, copias, saida, pasta_img, resolucao):
    anteriores = tiques_anteriores(saida)
    por_chave = {f["chave"]: f for f in fontes}
    resumo, corpo, sem_pessoa = [], [], []
    for chave, ref in refs:
        cs = copias.get(chave, [])
        dentro, fora = chamadas.get(chave, ("", ""))
        # a copia entra pelo caminho do registro, nao pelo caminho completo: assim o tique
        # nao cai quando a pasta do projeto muda de lugar
        sig = assinatura(json.dumps(por_chave[chave], ensure_ascii=False, sort_keys=True), ref, dentro,
                         *sorted(f"{c}|{h}" for _, c, _, _, h in cs))
        tiques, retirado = tiques_da_parte(anteriores, "referencias", chave, sig)
        if not tiques["pessoa"]:
            sem_pessoa.append(chave)
        situacoes = ", ".join(dict.fromkeys(SITUACAO[s] for _, _, _, s, _ in cs)) or "nenhuma"
        resumo.append(f"| [{chave}](#{ancora(chave)}) | {dentro or '—'} | {situacoes} | "
                      f"{'sim' if tiques['IA'] else 'não'} | {'sim' if tiques['pessoa'] else 'não'} |")
        corpo += ["", "---", "", f"## {chave}", "", marca("referencias", chave, sig), "", f"> {ref}", ""]
        corpo += [f"Chamada no texto: {dentro} — na frase: {fora}" if dentro else
                  "Chamada no texto: a referência veio pronta, então a chamada também é escrita à mão", ""]
        if not cs:
            corpo += ["Cópia registrada: nenhuma", ""]
        for doc, _, arquivo, situacao, _ in cs:
            corpo += [f"Cópia registrada: `{link(arquivo, saida)}` ({SITUACAO[situacao]}), no registro de "
                      f"`{link(doc, saida)}`", ""]
            if arquivo.suffix.lower() == ".pdf" and situacao != "nao-existe":
                nome = re.sub(r"[^\w.-]", "_", chave)
                corpo += [f"[original, primeira página]({link(arquivo, saida)}#page=1)", "",
                          f"![{chave}, primeira página]({link(imagem(arquivo, 1, pasta_img, nome, resolucao), saida)})", ""]
        if retirado:
            corpo += ["Tique retirado: a referência, a chamada ou a cópia mudaram depois do tique", ""]
        corpo += caixas(tiques)
    cabecalho = ["# Conferência das referências", "",
                 "| Chave | Chamada | Cópia registrada | Tique da IA | Tique da pessoa |",
                 "| :--- | :--- | :--- | :---: | :---: |"] + resumo
    saida.parent.mkdir(parents=True, exist_ok=True)
    saida.write_text("\n".join(cabecalho + corpo) + "\n", encoding="utf-8")
    return sem_pessoa


def monta(projeto):
    """(fontes, referencias, chamadas, erros): as fontes do arquivo de fontes, as
    referencias em ordem [(chave, referencia)] e a chamada de cada fonte {chave: (entre
    parenteses, na frase)}; com erro nos dados ou no formato da disciplina, so os erros."""
    fontes = projeto.caminho("fontes")
    if not fontes.exists():
        return [], [], {}, [sem_fontes(fontes)]
    dados, erros = le_dados(fontes, esquema("fontes"))
    meses, erros_meses = le_dados(ARQUIVO_MESES, esquema("meses"))
    # o formato e opcional (sem ele, a data de acesso fica sem o idioma do texto); se
    # existe, so e usado sem erro
    texto, erros_formato = None, []
    if projeto.caminho("formato").exists():
        formato, erros_formato = le_formato(projeto)
        if not erros_formato:
            texto = lingua(formato["idioma"])
    # cada erro de leitura ja vem com o nome do arquivo dele
    erros += erros_meses + erros_formato
    if not erros:
        r = Regras(dados["et_al"], meses["meses"], texto)
        erros = [f"{fontes.name}: {e}" for e in erros_de_idioma(dados["fontes"], r)]
    if erros:
        return [], [], {}, erros
    lista = dados["fontes"]
    com_chamada = [f for f in lista if f["tipo"] != "outro"]
    nomes = {f["chave"]: nomes_da_chamada(f) for f in com_chamada}
    letras = desempata(com_chamada, nomes, r)
    refs = sorted(((f["chave"], referencia(f, r, letras.get(f["chave"], ""))) for f in lista),
                  key=lambda x: ordem(x[1]))
    chamadas = {f["chave"]: chamada(nomes[f["chave"]], ano(f) + letras.get(f["chave"], ""), r) for f in com_chamada}
    return lista, refs, chamadas, []


def roda(projeto, chave_nova=None):
    fontes, saida = projeto.caminho("fontes"), projeto.caminho("referencias")
    conferencia, transcricoes = projeto.caminho("conferencia_referencias"), projeto.caminho("gerados")
    if not fontes.exists():
        print(f"FALTA REFERÊNCIA: {sem_fontes(fontes)}" + (f" e acrescente a chave {chave_nova}" if chave_nova else ""))
        return 1
    lista, refs, chamadas, erros = monta(projeto)
    if erros:
        for e in erros:
            print(f"ERRO em {e}")
        return 1
    grava_fontes_md(refs, saida, projeto.caminho("licenca_conteudo"), projeto.valor("nome_licenca_conteudo"))
    copias = copias_registradas(transcricoes, projeto.raiz) if transcricoes.exists() else {}
    sem_pessoa = grava_conferencia(refs, chamadas, lista, copias, conferencia,
                                   projeto.pasta_de_imagens(conferencia), projeto.valor("resolucao_imagens"))
    chaves = {f["chave"] for f in lista}
    faltam = sorted(set(copias) - chaves)
    print(f"{len(refs)} referência(s) gravadas em {saida}")
    print(f"conferência: {conferencia}")
    if chave_nova and chave_nova not in chaves and chave_nova not in faltam:
        faltam.append(chave_nova)
    for chave in faltam:
        print(f"FALTA REFERÊNCIA: a chave {chave} está registrada, mas não está em {fontes.name}")
    if sem_pessoa:
        print(f"CONFERIR: {len(sem_pessoa)} referência(s) sem o tique da pessoa: {', '.join(sem_pessoa)}")
    return 1 if faltam else 0


def main(argv=None):
    a = argparse.ArgumentParser(description="Monta as referências do projeto a partir do arquivo de fontes.")
    a.add_argument("--projeto", type=Path, help="projeto.json (padrao: o primeiro achado subindo a partir daqui)")
    args = a.parse_args(argv)
    return roda(acha_projeto(args.projeto))


if __name__ == "__main__":
    sys.exit(main())
