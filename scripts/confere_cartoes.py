# SPDX-License-Identifier: GPL-3.0-or-later
# Copyright do codigo sob GPL-3.0 -- ver LICENSE e NOTICE.md na raiz do projeto.

"""
Confere cada cartao das planilhas de pergunta contra a prova dele e gera a conferencia
dos cartoes.

A prova fica num arquivo local, fora do controle de versao, porque tem texto literal das
fontes: um arquivo por planilha (no modelo, docs/material-base/gerados-ocr/provas/
<planilha>.json), com, para cada cartao, a pergunta igual a da planilha, os trechos da
fonte que provam a resposta, copiados letra por letra, e se a fonte afirma
("categorica") ou trata como possibilidade ("possibilidade"). O cartao e a prova se
ligam pelo texto da pergunta.

O lugar de cada trecho nao fica na prova: sai da coluna "fonte" do cartao, a citacao
que aparece no verso. Cada chamada dela, como "(Silva, 2020, p. 12)", e reconhecida
pelas chamadas do arquivo de chamadas, escritas a mao, cada uma com a chave da fonte; o
lugar ("p. 12", "slide 3") e o titulo de pagina da transcricao registrada com essa chave,
ou a pagina de uma frase dela na base do material de fora.

O script nao julga se a resposta esta certa. Recusa so o que falta ou nao bate: planilha
com o texto fora do UTF-8 ou com um cartao com mais valores que colunas (comum.le_planilha),
planilha sem as colunas da pergunta, da resposta e da fonte; cartao sem pergunta, cartao
sem prova, prova sem cartao, pergunta repetida; coluna fonte sem chamada, texto nela que
nao e chamada de nenhuma fonte, chamada sem lugar, lugar que a fonte nao tem; trecho que
nao esta, letra por letra, em nenhum dos lugares citados, e lugar citado sem nenhum
trecho; prova "categorica" com trecho que a base do material de fora marca como
possibilidade. Na comparacao, a quantidade de espacos, as quebras de linha e as marcas de
destaque nao contam; letras e pontuacao contam.

A conferencia mostra cada cartao com a pergunta, a resposta, a fonte, os trechos e onde
cada um foi achado, e as caixas de tique "IA" e "pessoa"; o cartao que a fonte trata
como possibilidade aparece com o aviso de que a resposta tem de dizer isso. Se o cartao,
a prova ou o texto dos lugares citados mudarem depois do tique, o tique e retirado.

Os caminhos vem do projeto.json: as planilhas, de "material_gerado" e
"prefixo_planilhas"; as provas, de "provas" (com {planilha} no lugar do nome da
planilha, sem o .csv); as chamadas, de "chamadas"; as transcricoes, de "gerados"; as
bases do material de fora, de "base_externa"; e o arquivo gerado, de
"conferencia_cartoes".

A prova de cada planilha e lida pela leitura de todo arquivo de dados
(validar_dados.le_dados), contra o molde dela (prova.schema.json): com o texto fora do
UTF-8, JSON invalido ou fora do molde, cada erro aparece com ERRO e a prova nao e usada,
entao os cartoes da planilha ficam sem prova. O arquivo de chamadas e lido do mesmo
jeito, contra o molde dele (chamadas.schema.json): com erro nele, quando ele falta ou
quando duas fontes tem a mesma chamada, cada erro aparece com ERRO e nada e gravado.

Uso (de qualquer pasta dentro do projeto):
    python scripts/confere_cartoes.py
    python scripts/confere_cartoes.py --projeto projeto.json
"""

import argparse
import json
import re
import sys
import unicodedata
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from base_externa import AFIRMACAO, TEXTO_INTEIRO, descreve  # noqa: E402
from comum import (COLUNA_PERGUNTA, EXTENSAO_PLANILHA, acha_projeto, ancora, arquivo_da_prova,  # noqa: E402
                   assinatura, caixas, le_planilha, link, marca, planilhas, tiques_anteriores, tiques_da_parte)
from conferencia import fonte_da_transcricao, secoes, transcricoes_da_pasta  # noqa: E402
from validar_dados import esquema, le_dados  # noqa: E402

COLUNA_RESPOSTA, COLUNA_FONTE = "resposta", "fonte"  # as colunas da resposta e da citacao das fontes
COLUNAS = (COLUNA_PERGUNTA, COLUNA_RESPOSTA, COLUNA_FONTE)  # as colunas que o script le de cada cartao
# o que a prova, e a base do material de fora, dizem do trecho: a fonte afirma ou trata como possibilidade
# (esquemas/prova.schema.json e base.schema.json)
CATEGORICA, POSSIBILIDADE = "categorica", "possibilidade"
FRASE_DA_BASE = re.compile(r"^\*\*(?P<chave>\S+), (?P<local>.+?) — (?P<codigo>\S+) — (?P<afirmacao>.+)\*\*$")
ARQUIVO_NO_LOCAL = re.compile(r" \(arquivo p\. \d+\)$")
# a base escreve a afirmacao pela descricao em portugues, ou pelo proprio valor, se ele nao
# tem descricao (ver base_externa.descreve): o texto que nao esta aqui ja e o valor
DE_AFIRMACAO = {texto: chave for chave, texto in AFIRMACAO.items()}


def simples(texto):
    """Pra comparar: forma unica dos caracteres, sem marca de destaque e com os espacos
    juntos."""
    texto = re.sub(r"</?(?:i|em|b|strong)>|\*", "", unicodedata.normalize("NFC", texto))
    return re.sub(r"\s+", " ", texto).strip()


def curto(texto, n=80):
    texto = simples(texto)
    return texto if len(texto) <= n else texto[:n] + "…"


# ---------- os lugares das fontes ----------

def lugares_das_fontes(projeto):
    """{(chave, lugar): [(arquivo, onde, texto, afirmacao ou None)]}: cada pagina das
    transcricoes registradas, pelo titulo dela, e cada frase das bases do material de
    fora, pela pagina impressa (ou "texto inteiro"), com a afirmacao que a base deu."""
    indice = {}
    for arq, texto in transcricoes_da_pasta(projeto.caminho("gerados"), projeto.caminho("conferencia_cartoes")):
        chave, _, _ = fonte_da_transcricao(texto, projeto.raiz)
        if chave:
            for rotulo, n, conteudo in secoes(texto):
                indice.setdefault((chave, rotulo), []).append((arq, f"{rotulo} (arquivo p. {n})", conteudo, None))
    for base in projeto.todos_com("base_externa"):
        linhas = base.read_text(encoding="utf-8").split("\n")
        for i, linha in enumerate(linhas):
            m = FRASE_DA_BASE.match(linha)
            seguinte = next((l for l in linhas[i + 1:] if l.strip()), "")
            if m and seguinte.startswith("> "):
                lugar = ARQUIVO_NO_LOCAL.sub("", m["local"])
                indice.setdefault((m["chave"], lugar), []).append(
                    (base, m["codigo"], seguinte[2:], DE_AFIRMACAO.get(m["afirmacao"], m["afirmacao"])))
    return indice


def le_chamadas(projeto):
    """({nucleo: chave da fonte}, erros): as chamadas do arquivo de chamadas, lido contra o molde dele; o nucleo e o
    que fica dentro dos parenteses da chamada, como "Silva, 2020". Sem o arquivo, ou com duas fontes com a mesma
    chamada, que nao diria de qual delas e o trecho, so os erros."""
    arquivo = projeto.caminho("chamadas")
    if not arquivo.exists():
        return {}, [f"{arquivo.name}: o arquivo de chamadas não existe -- copie modelo-dados/chamadas.json"]
    dados, erros = le_dados(arquivo, esquema("chamadas"))
    if erros:
        return {}, erros
    nucleos = {}
    for c in dados["chamadas"]:
        nucleo = simples(c["chamada"][1:-1])
        if nucleo in nucleos:
            erros.append(f"{arquivo.name}: a chamada {c['chamada']!r} é de duas fontes, {nucleos[nucleo]} e "
                         f"{c['chave']}")
        nucleos.setdefault(nucleo, c["chave"])
    return ({} if erros else nucleos), erros


def chamadas_da_fonte(fonte, nucleos):
    """([(chave, lugar)], sobra): cada chamada da coluna fonte, reconhecida pelo nucleo
    dela (nomes e ano), com o lugar que vem logo depois; e o texto de antes da primeira
    chamada, que nao e de nenhuma."""
    texto = simples(fonte)
    padrao = "|".join(re.escape(n) for n in sorted(nucleos, key=len, reverse=True))
    ms = list(re.finditer(padrao, texto)) if nucleos else []
    citadas = []
    for i, m in enumerate(ms):
        fim = ms[i + 1].start() if i + 1 < len(ms) else len(texto)
        citadas.append((nucleos[m.group(0)], texto[m.end():fim].strip(" ,;()")))
    sobra = texto[:ms[0].start()] if ms else texto
    return citadas, sobra.strip(" ,;()")


# ---------- um cartao ----------

def confere_cartao(linha, prova, nucleos, indice):
    """(erros, citados, achados): citados = [(chave, lugar, textos)]; achados =
    [(trecho, [(chave, lugar, arquivo, onde, afirmacao)])]."""
    erros, citados, achados = [], [], []
    citadas, sobra = chamadas_da_fonte(linha.get(COLUNA_FONTE) or "", nucleos)
    if not citadas:
        erros.append("a coluna fonte não tem a chamada de nenhuma fonte do arquivo de chamadas")
    if sobra:
        erros.append(f"texto na coluna fonte que não é chamada de nenhuma fonte: {sobra!r}")
    for chave, lugar in citadas:
        textos = indice.get((chave, lugar or TEXTO_INTEIRO))
        if textos:
            citados.append((chave, lugar, textos))
        elif not lugar:
            erros.append(f"a chamada de {chave} não diz o lugar do trecho, como a página ou o slide")
        else:
            erros.append(f"{chave} não tem o lugar {lugar!r}: nenhuma transcrição registrada com essa chave "
                         f"tem esse título de página, e nenhuma base tem frase dela nesse lugar")
    if prova is None:
        erros.append("cartão sem prova: a pergunta não está no arquivo de prova da planilha")
        return erros, citados, achados
    for trecho in prova["trechos"]:
        if not simples(trecho):
            erros.append("trecho vazio na prova")
            continue
        onde = [(chave, lugar, arq, de, af) for chave, lugar, textos in citados
                for arq, de, texto, af in textos if simples(trecho) in simples(texto)]
        if not onde:
            erros.append(f"trecho que não está, letra por letra, em nenhum dos lugares citados: {curto(trecho)!r}")
        achados.append((trecho, onde))
    for chave, lugar, _ in citados:
        if not any(c == chave and l == lugar for _, onde in achados for c, l, *_ in onde):
            erros.append(f"lugar citado sem nenhum trecho da prova: {chave}, {lugar or TEXTO_INTEIRO}")
    if prova["afirmacao"] == CATEGORICA and any(o[4] == POSSIBILIDADE for _, onde in achados for o in onde):
        erros.append("a prova diz que a fonte afirma, mas a base do material de fora marca o trecho como possibilidade")
    return erros, citados, achados


def bloco_do_cartao(titulo, linha, prova, erros, achados, marca_, tiques, retirado, saida):
    out = ["", f"### {titulo}", "", marca_, "",
           f"**Pergunta:** {linha.get(COLUNA_PERGUNTA) or ''}", "",
           f"**Resposta:** {linha.get(COLUNA_RESPOSTA) or ''}", "", f"**Fonte:** {linha.get(COLUNA_FONTE) or ''}", ""]
    if prova:
        aviso = " — a resposta tem de dizer isso" if prova["afirmacao"] == POSSIBILIDADE else ""
        out += [f"**Afirmação:** {descreve(AFIRMACAO, prova['afirmacao'])}{aviso}", ""]
        for trecho, onde in achados:
            out += [f"> {l}" for l in trecho.split("\n")]
            out += ["", "Achado em: " + ("; ".join(f"`{link(arq, saida)}`, {de}" for _, _, arq, de, _ in onde)
                                        or "nenhum dos lugares citados"), ""]
    out += [f"**ERRO:** {e}" for e in erros] + ([""] if erros else [])
    if retirado:
        out += ["Tique retirado: o cartão, a prova ou o texto dos lugares citados mudaram depois do tique", ""]
    return out + caixas(tiques)


# ---------- uma planilha ----------

def le_provas(arquivo):
    """({pergunta simplificada: prova}, erros)."""
    if not arquivo.exists():
        return {}, [f"a planilha não tem arquivo de prova: {arquivo} -- copie modelo-dados/prova.json"]
    dados, erros = le_dados(arquivo, esquema("prova"))
    if erros:
        return {}, erros
    provas = {}
    for p in dados["provas"]:
        k = simples(p["pergunta"])
        if k in provas:
            erros.append(f"pergunta repetida no arquivo de prova: {curto(k)!r}")
        provas[k] = p
    return provas, erros


def processa(planilha, projeto, nucleos, indice, anteriores, saida):
    """(bloco, contagem, erros) de uma planilha. Contagem: cartoes, com erro, tique da IA,
    tique da pessoa."""
    nome = planilha.stem
    colunas, linhas, da_leitura = le_planilha(planilha, planilha.name)
    corpo, cont, erros = ["", "---", "", f"## {nome}", "", f"Planilha: `{link(planilha, saida)}`"], [0, 0, 0, 0], []
    faltam = [c for c in COLUNAS if c not in colunas] if colunas is not None else []
    if faltam:
        erros.append(f"faltam as colunas {', '.join(faltam)}")
    elif colunas is not None:
        arquivo_prova = arquivo_da_prova(projeto, planilha)
        provas, erros = le_provas(arquivo_prova)
        corpo.append(f"Prova: `{link(arquivo_prova, saida)}`")
        perguntas = [simples(l.get(COLUNA_PERGUNTA) or "") for l in linhas]
        erros += [f"pergunta repetida na planilha: {curto(k)!r}" for k in sorted(set(perguntas))
                  if k and perguntas.count(k) > 1]
        erros += [f"prova sem cartão: {curto(k)!r}" for k in provas if k not in perguntas]
    corpo += [""] + [f"**ERRO:** {e}" for e in da_leitura + erros]
    erros = da_leitura + [f"{nome}: {e}" for e in erros]
    if colunas is None or faltam:
        return corpo, cont, erros
    for i, (linha, k) in enumerate(zip(linhas, perguntas), 1):
        prova = provas.get(k)
        erros_cartao, citados, achados = confere_cartao(linha, prova, nucleos, indice)
        if not k:
            erros_cartao.insert(0, "cartão sem pergunta")
        sig = assinatura(json.dumps(linha, ensure_ascii=False, sort_keys=True),
                         json.dumps(prova, ensure_ascii=False, sort_keys=True),
                         *[t for _, _, textos in citados for _, _, t, _ in textos])
        parte = assinatura(k)
        tiques, retirado = tiques_da_parte(anteriores, nome, parte, sig)
        corpo += bloco_do_cartao(f"{nome} — cartão {i}", linha, prova, erros_cartao, achados,
                                 marca(nome, parte, sig), tiques, retirado, saida)
        cont = [cont[0] + 1, cont[1] + bool(erros_cartao), cont[2] + tiques["IA"], cont[3] + tiques["pessoa"]]
        erros += [f"{nome}, cartão {i}: {e}" for e in erros_cartao]
    return corpo, cont, erros


def main(argv=None):
    p = argparse.ArgumentParser(description="Confere cada cartão das planilhas contra a prova dele.")
    p.add_argument("--projeto", type=Path, help="projeto.json (padrao: o primeiro achado subindo a partir daqui)")
    a = p.parse_args(argv)
    projeto = acha_projeto(a.projeto)
    todas = planilhas(projeto)
    if not todas:
        raise SystemExit(f"nenhuma planilha '{projeto.valor('prefixo_planilhas')}*{EXTENSAO_PLANILHA}' em "
                         f"{projeto.caminho('material_gerado')}")
    nucleos, erros = le_chamadas(projeto)
    if erros:
        for e in erros:
            print(f"ERRO em {e}")
        return 1
    indice = lugares_das_fontes(projeto)
    saida = projeto.caminho("conferencia_cartoes")
    anteriores = tiques_anteriores(saida)
    resumo, corpo, todos_erros, totais = [], [], [], [0, 0, 0, 0]
    for planilha in todas:
        bloco, cont, erros = processa(planilha, projeto, nucleos, indice, anteriores, saida)
        corpo += bloco
        todos_erros += erros
        totais = [x + y for x, y in zip(totais, cont)]
        resumo.append(f"| [{planilha.stem}](#{ancora(planilha.stem)}) | " + " | ".join(map(str, cont))
                      + f" | {cont[0] - cont[3]} |")
    cabecalho = ["# Conferência dos cartões", "",
                 "| Planilha | Cartões | Com erro | Tique da IA | Tique da pessoa | Sem tique da pessoa |",
                 "| :--- | ---: | ---: | ---: | ---: | ---: |"] + resumo
    cabecalho.append("| **Total** | " + " | ".join(f"**{x}**" for x in totais) + f" | **{totais[0] - totais[3]}** |")
    saida.parent.mkdir(parents=True, exist_ok=True)
    saida.write_text("\n".join(cabecalho + corpo) + "\n", encoding="utf-8")
    for e in todos_erros:
        print("ERRO:", e)
    print(f"{totais[0]} cartão(ões) | com erro: {totais[1]} | sem tique da pessoa: {totais[0] - totais[3]}")
    print(f"conferência: {saida}")
    return 1 if todos_erros else 0


if __name__ == "__main__":
    sys.exit(main())
