# Scripts

Os programas do projeto, na pasta `scripts/`: o que cada um faz, como rodar e o que ele
mostra. Os outros documentos apontam para cá quando falam de um script.

## Por que o projeto usa scripts

Um <dfn>script</dfn> é um programa pequeno que faz sozinho um trabalho repetitivo — os
arquivos `.py` desta pasta. Ele trabalha do mesmo jeito, não importa quem rode nem quantas
vezes; por isso a parte mecânica do projeto é deles: transcrever as fontes e montar as
referências, as conferências, o glossário e o baralho, sem esquecer nem inventar nada.
Nenhum script julga se um conteúdo está certo: isso é sempre de uma pessoa.

Os scripts tiram os caminhos do [mapa do projeto](#o-mapa-do-projeto), menos os que se
digitam no comando ([Como rodar](#como-rodar)). Os únicos nomes
fixos são a pasta `scripts/`, tudo o que está dentro dela, o `projeto.json` e a [pasta
protegida](../metodologia-de-conteudo.md#1-as-fontes-e-a-transcrição),
`docs/material-base/`: é por eles que os scripts se acham uns aos outros e acham as fontes.

## O que precisa estar instalado

| Programa | Para quê |
| --- | --- |
| O <dfn>Python</dfn> 3 ([python.org](https://www.python.org/downloads/)) | roda todos os scripts; num computador em que ele se chama `python3`, é esse o nome no começo dos comandos |
| A biblioteca <dfn>genanki</dfn> (`pip install genanki`) | monta o arquivo do Anki, no `montar_deck.py` |
| O <dfn>Tesseract</dfn> ([tesseract-ocr](https://github.com/tesseract-ocr/tesseract)), com os dados de cada idioma do texto das figuras (`por`, o português) | faz o [OCR](../metodologia-de-conteudo.md#o-texto-das-figuras) do texto das figuras, no `transcrever_html.py` e no `transcrever_pptx.py`, e das páginas de PDF que o `extrator.py` lê pelo OCR |
| O <dfn>LibreOffice</dfn> ([libreoffice.org](https://www.libreoffice.org/download/)) | faz o PDF de cada aula, de onde sai a imagem de cada slide na conferência das transcrições, e converte as imagens que o Tesseract ou o GraphicsMagick não leem (EMF, WMF, SVG) |
| O <dfn>Poppler</dfn> ([poppler.freedesktop.org](https://poppler.freedesktop.org/)) | lê PDF: faz a imagem de cada slide, do PDF da aula, lê as fontes em PDF do material de fora, no `base_externa.py` e na conferência das referências, e tira o texto, o negrito e o itálico das fontes em PDF, no `extrator.py` |
| O <dfn>GraphicsMagick</dfn> ([graphicsmagick.org](http://www.graphicsmagick.org/download.html)) | faz a cópia em PNG de cada imagem que não está em PNG, na conferência das transcrições |
| O [git](../.githooks/README.md) | diz o que vai com o projeto, no `protege_fontes.py`, no `confere_indice.py` e no `glossario.py` |

## Como rodar

Cada script roda num
[terminal](../MANUAL.md#atualizando-o-baralho-depois-de-editar-as-planilhas) aberto em
qualquer pasta do projeto, com o comando que a seção dele mostra: o script sobe de pasta
em pasta até achar o `projeto.json` e tira todo caminho dali. A exceção são o
`validar_dados.py`, o `extrator.py` e o `itens.py`, que leem os arquivos pelos caminhos
digitados, a partir da pasta do terminal; os exemplos deles são para a pasta principal do
projeto.

O script sempre diz o que fez. Uma linha que começa com `ERRO`, `FALTA` ou `CONFERIR` pede
alguma coisa e diz o quê.

## Quando cada um entra

| Quando | Script |
| --- | --- |
| Depois de gravar ou mudar um arquivo de dados | `validar_dados.py` |
| Para transcrever um capítulo do livro-texto | `transcrever_html.py` |
| Para transcrever uma aula | `transcrever_pptx.py` |
| Para transcrever uma fonte em PDF, HTML, XML ou JSON, como uma norma ou um artigo | `extrator.py` |
| Depois de transcrever um documento numerado, como uma norma | `itens.py` |
| Assim que uma transcrição é criada | `registrar_fonte.py`, que roda o `referencias.py` |
| Sempre que o arquivo de fontes muda | `referencias.py` |
| Sempre que uma transcrição muda, e antes de escrever o material | `conferencia.py` |
| Quando nem a aula nem o livro-texto chegam a um subtópico de um item | `base_externa.py`, que roda o `referencias.py` |
| Com as planilhas de pergunta e as provas dos cartões prontas | `confere_cartoes.py` |
| Com as planilhas conferidas, e sempre que uma delas muda | `montar_deck.py` |
| Sempre que um documento define um termo novo, ou deixa de definir | `glossario.py` |
| Sempre que um documento entra no projeto, sai dele ou muda de lugar | `confere_indice.py` |
| Antes de publicar | `protege_fontes.py` |

O `protege_fontes.py`, o `glossario.py` e o `confere_indice.py` rodam também sozinhos antes
de cada commit ([Conferência das mensagens e proteção das fontes](../.githooks/README.md)).

## O mapa do projeto

O `projeto.json`, na pasta principal, é o [mapa do projeto](../metodologia-de-conteudo.md).
Em `caminhos`, ele diz onde fica cada arquivo e cada pasta que os scripts leem ou gravam —
entre eles, `imagens`, a pasta das imagens que as conferências fazem, e `licenca_conteudo`,
o arquivo da licença do conteúdo. Uma pasta muda de lugar mudando só ali, menos a pasta
protegida, que nunca muda. Fora dos caminhos:

| Informação | O que guarda |
| --- | --- |
| `prefixo_planilhas` | o começo do nome de toda planilha de pergunta |
| `resolucao_imagens` | a resolução das imagens das conferências, em pontos por polegada |
| `nome_licenca_conteudo` | o nome da licença do conteúdo, que sai no rodapé da lista de referências |
| `colunas_ocultas` e `coluna_subdecks` | as colunas que o baralho guarda sem mostrar e a que o divide ([`montar_deck.py`](#montar_deckpy--das-planilhas-de-pergunta-ao-baralho-do-anki)) |

## O arquivo de formato

O [arquivo de formato](../metodologia-de-conteudo.md#onde-o-formato-fica-gravado),
`dados/formato.json`, guarda as decisões do formato que os scripts usam, só como nomes e
listas, sem explicação:

| Informação | O que guarda |
| --- | --- |
| `versao_schema` | a versão do molde que o arquivo segue |
| `curso`, `disciplina` e `nivel` | para quem é o material |
| `idioma` | o idioma do material, como `pt-BR`, o português do Brasil |
| `itens` | os itens que se estudam um por um; lista vazia, se não houver |
| `eixos` e os `subtopicos` de cada eixo | as linhas da ficha e as partes menores de cada uma; lista vazia de subtópicos, se o eixo não se divide |
| `elos` | as partes do dicionário; lista vazia, se não houver |
| `colunas_extras` | as colunas do cartão além de `pergunta`, `resposta` e `fonte` |

Cada item, elo, eixo e subtópico entra na lista dele entre chaves, `{ }`, com um `id`, um
código curto, e um `nome`; o eixo tem também a lista `subtopicos`. O id vai entre aspas,
mesmo quando é número. Os elos e os eixos são numerados na ordem, `"1"`, `"2"`...; o
subtópico leva o número do eixo, um ponto e o dele, `"1.1"`, `"1.2"`. Assim nenhum id se
repete na grade, e é pelo id que a base de cada item marca a cobertura de cada subtópico.
O id do item aparece no nome dos arquivos dele. Cada coluna extra é só o nome dela, entre
aspas. Os scripts ignoram uma informação que não conhecem.

Um exemplo inventado, com um item, um elo e dois eixos, o primeiro dividido em dois
subtópicos e o segundo sem divisão:

```json
{
  "versao_schema": 1,
  "curso": "Curso de Exemplo",
  "disciplina": "Disciplina de Exemplo",
  "nivel": "revisão para a prova",
  "idioma": "pt-BR",
  "itens": [
    { "id": "A1", "nome": "Primeiro item" }
  ],
  "elos": [
    { "id": "1", "nome": "Primeiro elo" }
  ],
  "eixos": [
    {
      "id": "1",
      "nome": "Primeiro eixo",
      "subtopicos": [
        { "id": "1.1", "nome": "Primeira parte do primeiro eixo" },
        { "id": "1.2", "nome": "Segunda parte do primeiro eixo" }
      ]
    },
    { "id": "2", "nome": "Segundo eixo", "subtopicos": [] }
  ],
  "colunas_extras": ["item", "tipo_pergunta"]
}
```

## `validar_dados.py` — confere um arquivo de dados

**O que faz.** Cada arquivo de dados — como o `projeto.json`, o arquivo de formato, o de
fontes, a base de cada item e a prova de cada planilha — tem uma forma certa, descrita num
molde, o <dfn>schema</dfn>, em `scripts/esquemas/`. O script confere se o arquivo segue o
molde: se não falta campo obrigatório, se nada está no tipo errado, se nenhum código (id ou
chave) se repete.

**Como rodar.** O caminho do arquivo depois do nome do script:

    python scripts/validar_dados.py dados/formato.json

O molde se acha pelo nome do arquivo (o de `formato.json` é `formato.schema.json`). A base
de um item tem o nome do item, e a prova, o da planilha; para elas, `--schema` diz o molde
(`base.schema.json` ou `prova.schema.json`):

    python scripts/validar_dados.py dados/bases/[item].json --schema scripts/esquemas/base.schema.json

**O que mostra.** `0 erro(s)`, quando está tudo na forma certa. Senão, cada linha `ERRO`
diz onde está o problema: `$.itens[2].id: deve ser string` quer dizer que, no terceiro item
da lista `itens`, o `id` tem de ser um texto (a contagem começa do zero).

## `transcrever_html.py` — transcreve uma fonte em HTML, como um livro digital

**O que faz.** O livro-texto se lê num site, em documentos HTML que marcam onde começa
cada página impressa, e o texto deles é texto de verdade. O script faz a transcrição
sozinho, no padrão da [metodologia](../metodologia-de-conteudo.md#a-transcrição): copia o
texto de cada página, sem ler nada, com o título que diz o número impresso e a posição da
página no documento, como `## p. 116 (arquivo p. 1)`. Parágrafo vira uma linha; título,
`###` ou menos; tabela, tabela do Markdown (a que passa para a página seguinte continua lá
depois de `[continuação da tabela da p. X]`); índice e expoente, os caracteres próprios
(CO₂, Mg²⁺); negrito e itálico, texto puro. Cada imagem entra no lugar dela como a própria
imagem, `![imagem](caminho)`, seguida do texto escrito dentro dela, lido por OCR, e de
`[fim da imagem]`. A transcrição fica em `docs/material-base/gerados-ocr/`, com o nome do
documento: a de `chapter12.xhtml` é `chapter12.md`.

O livro chega ao script pela captura que o navegador salva durante a leitura, nas
<dfn>ferramentas do desenvolvedor</dfn> (F12): na aba Rede, com o cache desligado e o
filtro em "Tudo", a página é recarregada e lida até o fim, para tudo carregar, e a lista é
salva como HAR. A captura guarda também os dados da sessão no site, os
<dfn>cookies</dfn>, que o script nunca lê. Dela, o script copia para a pasta do livro,
dentro da pasta protegida, cada documento com marca de página, com as imagens dele, e
transcreve a cópia.

**Como rodar.** O caminho da captura e, com `--pasta`, a pasta da cópia:

    python scripts/transcrever_html.py [captura].har --pasta docs/material-base/MURRAY-2022

Com `--documento chapter12.xhtml`, só esse documento, quando a captura tem mais de um. O
caminho de um documento já copiado, no lugar da captura, transcreve de novo a partir da
cópia:

    python scripts/transcrever_html.py docs/material-base/MURRAY-2022/Text/chapter12.xhtml

O idioma do texto das imagens é o que o documento declara, traduzido para o código do
Tesseract pela tabela de `scripts/normas/idiomas.json`; `--idioma`, com o código do
Tesseract, escolhe outro. O script não grava por cima de uma transcrição que já existe,
porque o texto das imagens dela pode já estar conferido; com `--substituir`, grava, e o
registro da fonte, no topo, continua.

**O que mostra.** Cada transcrição gravada, com quantas páginas e quantas imagens tem.
`FALTA` lembra de registrar a transcrição. `CONFERIR` avisa o que o script não conseguiu
fazer sozinho: um índice ou expoente sem caractere próprio (fica na linha), uma imagem que
não está na cópia, uma marca de página no meio de uma linha de tabela. `ERRO` aponta o que
impediu a cópia: a captura com duas versões diferentes do mesmo documento, ou um arquivo da
cópia que já existe com outro conteúdo.

## `transcrever_pptx.py` — transcreve uma apresentação de slides em pptx

**O que faz.** As aulas são apresentações em <dfn>pptx</dfn>, o formato do PowerPoint, em
que o texto de cada slide é texto de verdade, guardado no arquivo. O script faz a
transcrição sozinho, no mesmo padrão: copia o texto de cada slide, sem ler nada, com o
título que diz a posição dele no arquivo, que é também o lugar que a citação usa, como
`## slide 3 (arquivo p. 3)`. Dentro do slide, o texto vem na ordem do arquivo, que é a
ordem em que o PowerPoint o lê em voz alta. O título do slide vira `###`; cada tópico, uma
linha com `- ` (ou o número, na lista numerada), recuada conforme o nível; tabela, tabela
do Markdown; índice e expoente, os caracteres próprios (CO₂, 10⁻⁶); o símbolo escrito com
uma fonte de símbolos, como a Symbol, o caractere de verdade (μ, ±), pela tabela de
`scripts/normas/simbolos.json`. Cada imagem entra no lugar dela, como no
`transcrever_html.py`, e as imagens saem do pptx para uma pasta ao lado dele, com o nome
dele. As notas do apresentador, se houver, vêm depois do slide, a partir de
`[notas do apresentador]`; o slide oculto começa com `[slide oculto]`. A transcrição fica
em `docs/material-base/gerados-ocr/`, com o nome do pptx.

**Como rodar.** O caminho da aula e, com `--idioma`, o idioma do texto das imagens, no
código do Tesseract — `por`, ou vários juntos, como `por+eng`, quando as figuras misturam
idiomas:

    python scripts/transcrever_pptx.py "docs/material-base/pptx/1-Introdução a Microbiologia.pptx" --idioma por

O idioma é sempre dito assim, porque o que o pptx marca no texto é o idioma do corretor
ortográfico, que muitas vezes não é o do texto. O script não grava por cima de uma
transcrição que já existe; com `--substituir`, grava, e o registro da fonte continua.

**O que mostra.** A transcrição gravada, com quantos slides e quantas imagens tem. `FALTA`
lembra de registrar a transcrição. `CONFERIR` avisa o que o script não conseguiu fazer
sozinho: um índice ou expoente sem caractere próprio (fica na linha), um símbolo de uma
fonte que não está na tabela (fica como está), uma imagem recortada no slide (o OCR lê a
imagem inteira, inclusive o que o slide não mostra), um gráfico ou um objeto sem imagem
(aparecem só na imagem do slide, na conferência), uma imagem que é só um link. `ERRO`
aponta o que impediu a transcrição: o arquivo que não se lê como pptx (um download
incompleto, por exemplo) ou uma imagem que já existe na pasta com outro conteúdo.

A tabela da fonte Symbol é o mapeamento oficial dela para o Unicode, publicado pelo
consórcio Unicode (`VENDORS/ADOBE/symbol.txt`), sem os códigos de uso corporativo da Adobe;
quando um código tem dois caracteres, fica o que já está na forma normal (NFKC) e, entre
dois assim, o de menor código.

## `extrator.py` — transcreve fontes em PDF, HTML, XML e JSON

**O que faz.** Tira o texto de uma fonte por programa, sem ler nada, e grava a transcrição
no padrão da [metodologia](../metodologia-de-conteudo.md#a-transcrição), página por página.
De um PDF, tira o texto da camada de texto do próprio arquivo; a página cujo texto não se
lê vai pelo OCR, quando a lista de extração pede. De uma página da internet, de um XML ou
de um JSON, capta o texto, bloco por bloco, numa página só. Dois arquivos de dados dizem
tudo. `dados/extrator.json` guarda o padrão da transcrição e os leitores de cada tipo de
arquivo. A lista de extração, `docs/material-base/gerados-ocr/extracao.json`, tem as
fontes, cada uma com a transcrição a gravar, as opções dela, a numeração das páginas e as
correções da leitura, cada correção conferida na imagem da página; ela fica na pasta
protegida porque as correções trazem texto da fonte. Os dois nascem de uma cópia dos modelos em branco,
[`modelo-dados/extrator.json`](../modelo-dados/extrator.json) e
[`modelo-dados/extracao.json`](../modelo-dados/extracao.json). Cada leitor é um
`leitor_<tipo>.py`, e o começo de cada um diz as opções dele.

**Como rodar.**

    python scripts/extrator.py dados/extrator.json docs/material-base/gerados-ocr/extracao.json

Com `--so` e o arquivo da fonte, só essa fonte. O script não grava por cima de uma
transcrição que já existe; com `--substituir`, grava, e o registro da fonte, no topo,
continua.

**O que mostra.** Cada transcrição gravada, com quantas páginas tem, quantas sem texto,
quantas lidas pelo OCR, quantas trocas e quantas correções. Com qualquer `ERRO` (uma
correção cujo texto a leitura não dá mais, uma opção que falta), nada é gravado.

## `itens.py` — lista e confere os itens numerados de uma transcrição

**O que faz.** Num documento numerado, como uma norma, cada parte do texto tem um número:
7, 7.1, 7.1.1. O script acha esses itens na transcrição, com o número, o título, a página e
a linha de cada um, e confere a numeração: o número que salta, que se repete ou que sai de
ordem, e a entrada do sumário que não tem, no texto, o item com o mesmo título. É assim que
aparece o número que a extração leu errado. O script também divide os tópicos do sumário
em grupos de um tamanho dado, para dividir o trabalho de quem lê o documento. O arquivo de
dados `dados/itens-numerados.json` diz a forma de uma linha de item e a de uma entrada do
sumário, o tamanho do grupo e, para cada transcrição, as páginas do sumário e as do texto.
Ele nasce de uma cópia do modelo em branco,
[`modelo-dados/itens-numerados.json`](../modelo-dados/itens-numerados.json). Do
`dados/extrator.json`, o script usa o padrão da transcrição.

**Como rodar.** A configuração do extrator, a dos itens e o arquivo da lista que o script
grava:

    python scripts/itens.py dados/extrator.json dados/itens-numerados.json docs/material-base/gerados-ocr/itens-das-normas.json

**O que mostra.** Para cada transcrição, quantos itens, grupos e problemas tem, e uma linha
`CONFERIR` para cada problema, com a linha da transcrição; a lista é gravada mesmo com
problemas. Com qualquer `ERRO` (uma forma escrita errado, um campo que o molde não conhece,
uma faixa fora das páginas), nada é gravado.

## `registrar_fonte.py` — liga a transcrição à fonte dela

**O que faz.** Grava no topo da transcrição de qual arquivo ela veio: a chave da fonte, o
caminho do arquivo e a [impressão digital](../metodologia-de-conteudo.md#a-transcrição)
dele. É pelo registro, não pelo nome dos arquivos, que os outros scripts sabem qual fonte
corresponde a qual transcrição.

**Como rodar.** A transcrição, o arquivo de onde ela veio e a chave da fonte — a mesma da
referência dela no arquivo de fontes:

    python scripts/registrar_fonte.py "docs/material-base/gerados-ocr/1-Introdução a Microbiologia.md" "docs/material-base/pptx/1-Introdução a Microbiologia.pptx" AULA-1

Se o arquivo da fonte está fora da pasta protegida, o script mostra para onde ele iria e
pergunta se pode movê-lo; sem a resposta `s`, nada é registrado. Com `--mover`, ele move
sem perguntar.

**O que mostra.** A linha gravada e, logo depois, o resultado do `referencias.py`, que o
script roda no fim: `FALTA REFERÊNCIA` para a chave sem referência, `CONFERIR` para as
referências sem o tique da pessoa.

## `referencias.py` — monta as referências e a conferência delas

**O que faz.** Com os dados de cada fonte no [arquivo de
fontes](../regras-abnt.md#o-arquivo-de-fontes), escreve cada referência pela norma de
referências da ABNT (NBR 6023), em ordem alfabética, e grava a lista em
`docs/REFERENCIAS.md`; monta também a
[chamada](../metodologia-de-conteudo.md#2-as-citações-e-as-referências) de cada fonte, pela
norma de citações (NBR 10520). Junto, grava a conferência das referências,
`CONFERENCIA-REFERENCIAS.md`, em `docs/material-base/gerados-ocr/`: cada referência e a
chamada dela ao lado da cópia da fonte — a primeira página, se for PDF —, com o tique da IA
e o da pessoa. O que vai em cada campo e o que cada norma pede estão nas [Regras da
ABNT](../regras-abnt.md); a abreviatura dos meses de cada idioma, a que a norma adota, fica
em `scripts/normas/meses.json`.

**Como rodar.**

    python scripts/referencias.py

**O que mostra.** Quantas referências foram gravadas e onde. `ERRO` aponta o que falta ou
não pode ser nos dados, como uma data com mês numa fonte sem `idioma`; com `ERRO`, nada é
gravado. `FALTA REFERÊNCIA` lista a fonte registrada sem dados no arquivo de fontes, e
`CONFERIR`, as referências sem o tique da pessoa.

Se o arquivo de formato existe, o script o confere antes contra o molde dele e, com algum
problema, mostra cada um numa linha `ERRO` e não grava nada. Vale também para os scripts
que rodam o `referencias.py`: o `confere_cartoes.py` não grava a conferência dos cartões, e
o `registrar_fonte.py`, que já gravou o registro da fonte, não grava as referências nem a
conferência delas. O `base_externa.py` precisa do formato e o confere logo no começo.

## `conferencia.py` — monta a conferência das transcrições

**O que faz.** Monta o arquivo para conferir cada transcrição contra a fonte, página por
página, `CONFERENCIA-COM-IMAGEM.md`, em `docs/material-base/gerados-ocr/`. O texto da
transcrição é cópia da fonte, e quem o confere é o próprio script: em cada página, ou
slide, as letras, os números e os sinais da transcrição têm de ser os da mesma página na
fonte, na mesma ordem, e também o título da página e as imagens. Não contam os espaços, as
marcas da transcrição (o `#` dos títulos, as barras das tabelas, o `<br>`,
`[slide oculto]`, `[notas do apresentador]`), a forma dos índices e expoentes e a diferença
entre o hífen e o sinal de menos. À mão, o texto de dentro de cada imagem e, na
transcrição feita pelo extrator, a página lida pelo OCR ou corrigida (abaixo). A imagem
aparece com esse texto e com as duas caixas de tique, uma para a IA e outra para a pessoa,
e mudar esse texto, mesmo só na divisão em linhas, é mudar a parte ([Como ticar uma
conferência](#como-ticar-uma-conferência)). Cada slide aparece também inteiro, como
imagem, para ver o que só o desenho mostra; essa imagem não tem tique. A imagem que não
está em PNG aparece numa cópia em PNG, com o link para o original, porque a visualização
do VSCode não mostra todo formato (EMF, WMF, TIFF): o GraphicsMagick faz a cópia sem mudar
o tamanho da imagem, e a que ele não lê o LibreOffice desenha, com fundo branco e sem
margem.

**Transcrição feita pelo extrator.** A transcrição que está na lista de extração é
conferida contra o que o [`extrator.py`](#extratorpy--transcreve-fontes-em-pdf-html-xml-e-json)
lê da fonte agora, com as trocas e as correções da lista: o texto de cada página tem de
ser o mesmo, letra por letra, e o rótulo também. A página lida pelo OCR, que o script não
lê de novo, e a página com correção aparecem com a imagem da página (na fonte em PDF), as
correções dela e as duas caixas de tique. O texto dessas páginas não se corrige no arquivo
de conferência: a correção vai para a lista de extração.

**Corrigir o texto das imagens.** O texto de uma imagem se corrige no próprio arquivo de
conferência, entre as cercas (` ```` `), olhando a imagem ao lado. A cerca é lida como no
Markdown, de qualquer tamanho, porque um formatador do editor pode trocá-la ao salvar. Com
`--levar-correcoes`, o script leva cada texto corrigido para a transcrição, na mesma
imagem, antes de gerar o arquivo de novo, e diz cada imagem levada. O tique da pessoa
fica, e o da IA sai, porque a IA ticou o texto antigo. Quando alguma correção não pode ser
levada, o script mostra cada caso numa linha `ERRO`, com o motivo, e não grava nada. Sem
essa opção, o arquivo é gerado de novo a partir das transcrições, e o que foi escrito
nele, fora os tiques, se perde.

**Como rodar.**

    python scripts/conferencia.py
    python scripts/conferencia.py --levar-correcoes

**O que mostra.** Quantas páginas há, quantas têm erro do script, quantas partes há para
ticar e quantas estão sem o tique da pessoa. Uma linha `ERRO` aparece para cada coisa que
impede a conferência ou que não bate — o registro da fonte, o texto, o título ou as
imagens de uma página —, com o motivo e, quando é o texto, o trecho onde começa a
diferença. O arquivo fica melhor de ler na visualização do VSCode (`Ctrl+Shift+V`).

## `base_externa.py` — monta a base do material de fora

**O que faz.** Monta a [base de trechos](../metodologia-de-conteudo.md#o-material-de-fora)
de cada item a partir das cópias do material de fora: o script recolhe todo o texto das
páginas declaradas, a IA decide o que cada frase é, e a pessoa confere. Ninguém copia
trecho à mão.

**Os dados de cada item.** O arquivo `dados/bases/[item].json` nasce de uma cópia do
modelo em branco, [`modelo-dados/base.json`](../modelo-dados/base.json), em que aspas
vazias, `""`, esperam um texto; colchetes vazios, `[]`, uma lista; e chaves vazias, `{}`,
pares de um nome e um valor, como `"1.1": "aula"`, separados por vírgula. O
`versao_schema` fica como está. O resto:

- em `item`, o id do item no arquivo de formato;
- em `lugares`, uma entrada para cada fonte lida, entre chaves, com: em `fonte`, a chave
  da referência dela; em `arquivo`, o caminho da cópia, a partir da pasta principal do
  projeto, em `docs/material-base/fontes-externas/`; e, se a cópia for PDF, em `paginas`,
  a lista das páginas do arquivo lidas, como `[47, 48]`. Se o arquivo estiver fora da
  pasta protegida, o script pergunta se pode levá-lo para a pasta das cópias e corrige o
  caminho aqui; com `--mover`, leva sem perguntar. Em `desloca`, quanto somar à página do
  arquivo para chegar ao número impresso — se a página 47 do arquivo tem impresso "45", é
  `-2`; se são iguais, `0`. Se a diferença muda de uma página para outra, `impressas` dá o
  número impresso de cada página do arquivo: `{"47": "45", "48": "xii"}`;
- em `cobertura`, cada subtópico da grade do formato, pelo id, com a marca dele: `aula`
  (a aula cobre), `fonte` (vem do material de fora) ou `lacuna` (nenhuma fonte cobre). Um
  eixo sem subtópicos é marcado pelo id do próprio eixo;
- `classes` e `juntar` começam vazios; são preenchidos depois da primeira rodada.

Um exemplo inventado, de um item lido nas páginas 47 e 48 de uma fonte em PDF, numa grade
com um eixo 1 dividido nos subtópicos 1.1 e 1.2 e um eixo 2 sem subtópicos:

```json
{
  "versao_schema": 1,
  "item": "A1",
  "lugares": [
    {
      "fonte": "GUIA-2020",
      "arquivo": "docs/material-base/fontes-externas/GUIA-2020.pdf",
      "paginas": [47, 48],
      "desloca": -2
    }
  ],
  "classes": {},
  "juntar": [],
  "cobertura": {
    "1.1": "aula",
    "1.2": "fonte",
    "2": "lacuna"
  }
}
```

**As frases e as classes.** Na primeira rodada, todas as frases aparecem como **sem
classe** na conferência, cada uma com um código, como `GUIA-2020:p47:3f2a91c0`: uma frase
da página 47 do arquivo da fonte GUIA-2020. O final do código é uma impressão digital do
texto da própria frase: se a frase muda — o PDF foi trocado, ou a separação em frases
mudou —, o código muda junto, a classe antiga aparece como "classe para frase que não
existe" e a frase nova como "sem classe". Assim uma classe nunca passa de uma frase para
outra sem ninguém ver.

Cada frase recebe, em `classes`, pelo código, uma destas classes:

- `usa`, com o `subtopico` e a `afirmacao`: `categorica` se a fonte afirma,
  `possibilidade` se ela trata como possível ou provável;
- `outro-item`, `repetida` (com `de`: o código da frase que ela repete),
  `fora-do-recorte` ou `nao-e-conteudo` (referência, cabeçalho, legenda solta).

A separação em frases é mecânica: quando ela parte uma frase em duas, os códigos se
juntam em `juntar`, uma lista com os códigos das frases que formam uma só, na ordem, e a
classe do grupo vai no código da primeira; quando junta dois pedaços numa frase só, a
classe vale para o pedaço inteiro. Um exemplo inventado, na mesma grade:

```json
"classes": {
  "GUIA-2020:p47:3f2a91c0": { "classe": "usa", "subtopico": "1.2", "afirmacao": "categorica" },
  "GUIA-2020:p47:9b1c2d3e": { "classe": "repetida", "de": "GUIA-2020:p47:3f2a91c0" },
  "GUIA-2020:p48:5e6f7a8b": { "classe": "nao-e-conteudo" },
  "GUIA-2020:p48:1a2b3c4d": { "classe": "usa", "subtopico": "1.2", "afirmacao": "possibilidade" }
},
"juntar": [
  ["GUIA-2020:p48:1a2b3c4d", "GUIA-2020:p48:4d5e6f70"]
]
```

Com tudo classificado, a rodada seguinte grava a base do item, e a conferência,
`CONFERENCIA-TRECHOS.md`, em `docs/material-base/gerados-ocr/`, mostra cada página com as
frases e a classe de cada uma, com os tiques da IA e da pessoa.

**Como rodar.**

    python scripts/base_externa.py

Ele refaz sempre todos os itens de uma vez: a conferência é um arquivo só, e é assim que
os tiques de todos os itens continuam nela.

**O que mostra.** Antes de tudo, o script confere o arquivo de formato contra o molde
dele: com algum problema, cada um aparece numa linha `ERRO`, nenhuma base é gravada e a
conferência não é refeita. Depois, uma linha `ERRO` para tudo o que falta ou se
contradiz: frase sem classe, subtópico sem marca, subtópico marcado como `fonte` sem
nenhuma frase usada, frase usada num subtópico que a aula já cobre ou que está marcado
como `lacuna`, um id que aparece mais de uma vez na grade do formato (dois subtópicos com
o mesmo id, mesmo em eixos diferentes, ou um subtópico com o id de um eixo sem
subtópicos). Com `ERRO`, a base do item não é gravada: o arquivo dela fica só com esse
aviso. Se um item nem pode ser lido — por exemplo, porque uma fonte dele ficou fora da
pasta protegida —, a conferência não é refeita, para não perder os tiques dele. Quando a
conferência é refeita, logo depois aparece o resultado das referências, porque a base
registra as fontes que usa.

## `protege_fontes.py` — confere que nenhuma fonte pode ser publicada

**O que faz.** Confere se alguma fonte registrada ficou fora da pasta protegida e se a
[lista do que nunca vai pro GitHub](../NOTICE.md#como-o-projeto-trata-esse-material)
deixa a pasta de fora. Com `--versao`, que é como o gancho de antes do commit o roda,
confere também cada arquivo que vai no commit e barra o que for da pasta protegida ou
cópia de uma fonte — mesmo com outro nome e em outra pasta, porque compara a impressão
digital de cada arquivo com a de cada fonte.

**Como rodar.**

    python scripts/protege_fontes.py

**O que mostra.** "Nenhuma fonte fora da pasta protegida." ou uma linha `ERRO` para cada
problema, dizendo o que fazer. Quando é ele que barra um commit, a mensagem diz como tirar
o arquivo do commit sem apagá-lo.

## Como ticar uma conferência

Os arquivos de conferência têm, em cada parte, duas linhas assim:

    - [ ] IA
    - [ ] pessoa

O tique é um `x` entre os colchetes, `- [x] pessoa`, escrito no arquivo no modo de texto,
não na visualização. Quando o script gera o arquivo de novo, o tique continua lá, a não
ser que o conteúdo daquela parte tenha mudado depois dele: aí o tique sai, e a parte diz
isso, para ninguém achar que o texto novo já foi conferido. A exceção é a correção que a
própria pessoa leva com o `conferencia.py`, que mantém o tique dela. Mudar a pasta do
projeto de lugar não tira nenhum tique.

## `confere_cartoes.py` — confere cada cartão contra a prova dele

**O que faz.** Cada cartão diz um fato com palavras próprias e traz, atrás, a citação da
fonte, na coluna `fonte`. A [prova](../metodologia-de-conteudo.md#6-os-cartões-e-o-baralho)
do cartão fica num arquivo à parte, um por planilha. O script confere, cartão por cartão,
se o trecho está mesmo no lugar que a citação diz — a página ou o slide da transcrição, ou
uma frase da base do material de fora — e grava a conferência dos cartões,
`CONFERENCIA-CARTOES.md`, em `docs/material-base/gerados-ocr/`, com os tiques da IA e da
pessoa.

**Os dados de cada planilha.** A prova da planilha `perguntas-[nome].csv` é
`docs/material-base/gerados-ocr/provas/perguntas-[nome].json`, e nasce de uma cópia do
modelo em branco, [`modelo-dados/prova.json`](../modelo-dados/prova.json), com a lista
`provas` vazia, `[]`, e o `versao_schema`, que fica como está. Cada cartão ganha na lista
uma entrada, entre chaves, `{ }`, separada da seguinte por uma vírgula, com três coisas:

- a `pergunta`, igual à da planilha — é por ela que o cartão e a prova se acham;
- os `trechos`: uma lista com os trechos da fonte que provam a resposta, cada um entre
  aspas, copiado da transcrição ou da base, letra por letra — pelo menos um para cada
  lugar que a coluna `fonte` do cartão cita;
- a `afirmacao`: `categorica`, se a fonte afirma, ou `possibilidade`, se ela trata como
  possível; nesse caso, a resposta do cartão diz isso.

Um exemplo inventado, com a prova de um cartão:

```json
{
  "versao_schema": 1,
  "provas": [
    {
      "pergunta": "Quantas etapas tem o processo de exemplo?",
      "trechos": ["O processo de exemplo tem três etapas."],
      "afirmacao": "categorica"
    }
  ]
}
```

Na coluna `fonte` da planilha vão só as chamadas, cada uma com o lugar: `(Silva, 2020, p.
12)`, ou, com duas fontes, `(Silva, 2020, p. 12; Souza, 2019, slide 3)`. O nome e o ano
de cada fonte são os que a conferência das referências mostra; o lugar é o título da
página na transcrição (`p. 12`, `slide 3`) ou a página da frase na base. Fonte sem
páginas, como uma página da internet, vai sem lugar.

**Como rodar.**

    python scripts/confere_cartoes.py

**O que mostra.** Uma linha `ERRO` para cada coisa que não bate: cartão sem prova, prova
sem cartão (a pergunta mudou só de um lado), chamada que não é de nenhuma fonte, lugar
que a fonte não tem, trecho que não está no lugar citado, lugar citado sem trecho, prova
que diz que a fonte afirma quando a base marca o trecho como possibilidade. Na comparação,
a quantidade de espaços, as quebras de linha e as marcas de destaque (itálico, negrito) não
contam; as letras e a pontuação contam. No fim, quantos cartões há, quantos têm erro e
quantos estão sem o tique da pessoa. A conferência mostra cada cartão com a pergunta, a
resposta, a fonte, os trechos e onde cada um foi achado; se o cartão, a prova ou o texto da
fonte mudam depois do tique, o tique sai.

## `montar_deck.py` — das planilhas de pergunta ao baralho do Anki

**O que faz.** Transforma cada planilha de pergunta (os arquivos `perguntas-*.csv` de
`docs/material-gerado/`) num baralho pronto para importar no Anki, um arquivo `.apkg` em
`anki-decks/`. No Anki, os cartões ficam numa pasta com o nome da disciplina, que vem do
arquivo de formato, e dentro dela uma pasta para cada planilha. As colunas `pergunta` e
`resposta` são obrigatórias; qualquer outra vira campo do cartão, com o nome da coluna sem
o sublinhado e com cada palavra em maiúscula (`tipo_pergunta` vira `TipoPergunta`), e a
`fonte`, com a citação do fato, aparece atrás do cartão, embaixo da resposta. No
`projeto.json`, `colunas_ocultas` diz as colunas que ficam guardadas no cartão sem
aparecer, e `coluna_subdecks`, uma coluna que separa os cartões de cada planilha em pastas
menores, uma para cada valor que aparece nela — ou `null`, escrito assim, sem aspas, para
não separar. A aparência dos cartões (cores, tamanho da letra) vem de
`dados/estilo-cartao.css`.

**Como rodar.**

    python scripts/montar_deck.py

Com uma parte do nome de uma planilha depois do nome do script, só essa planilha; com
`--listar`, só a lista das planilhas que seriam usadas, sem gerar nada.

**O que mostra.** Cada baralho gerado, com as pastas e quantos cartões tem. Uma planilha
sem a coluna `pergunta` ou `resposta` aparece com `ERRO` e fica sem baralho. Antes de gerar
qualquer baralho, o script confere o arquivo de formato contra o molde dele: se faltar
alguma coisa — o nome da disciplina, por exemplo, que é o nome da pasta de cima no Anki —,
cada problema aparece numa linha `ERRO` e nenhum baralho é gerado.

## `confere_indice.py` — confere que cada documento está no índice

**O que faz.** O [índice](../INDICE.md) lista os documentos na ordem de leitura, cada um
com o link e uma linha dizendo o que ele é. O script confere que cada [documento do
projeto](../metodologia-de-conteudo.md#8-os-documentos-e-os-arquivos-do-projeto), menos o
próprio índice, está nele uma vez só. Do índice contam os links para arquivos `.md`; a
parte do link depois de `#`, que aponta uma seção, não conta, e um link dentro de um
trecho de código também não.

**Como rodar.**

    python scripts/confere_indice.py

**O que mostra.** Quantos documentos há, se cada um está no índice uma vez só. Senão, uma
linha `FALTA` para cada documento que não está no índice e uma linha `ERRO` para documento
que está mais de uma vez — também num link do rodapé — e para link a um `.md` que não
existe, ao próprio índice ou a um arquivo que o `.gitignore` deixa de fora. Sem o git, o
script diz isso numa linha `ERRO` e para: sem ele, não há como saber o que vai com o
projeto.

## `glossario.py` — monta o glossário

**O que faz.** Um documento que define um termo marca o termo, no lugar da definição, com
a [marca de definição](../metodologia-de-conteudo.md#8-os-documentos-e-os-arquivos-do-projeto),
`<dfn>termo</dfn>`. O script recolhe essas marcas de todos os documentos do projeto — os
mesmos que o `confere_indice.py` confere —, fora dos trechos de código, e grava o
[glossário](../GLOSSARIO.md): cada termo numa linha, em ordem alfabética, sem contar
acentos nem maiúsculas, com o link para a seção onde ele é definido. O glossário não copia
a definição, só aponta para ela, e as mesmas marcas, nos mesmos lugares, dão sempre o mesmo
glossário.

**Como rodar.**

    python scripts/glossario.py
    python scripts/glossario.py --conferir

O `--conferir` não grava nada: só diz se o glossário gravado está em dia.

**O que mostra.** Quantos termos foram gravados. Uma linha `ERRO`, e nada gravado, para
termo definido em mais de um lugar (sem contar maiúsculas), com cada lugar, e para marca
vazia. Com `--conferir`, `FALTA` quando o glossário gravado não é o que os documentos
definem. Sem o git, o script diz isso numa linha `ERRO` e para, como o
`confere_indice.py`.

## `comum.py`

Não se roda: é a parte que os outros scripts compartilham (achar o `projeto.json` e as
planilhas de pergunta, ler o arquivo de formato e conferi-lo contra o molde dele, ler o
registro da fonte, guardar os tiques, ler as páginas de um documento HTML e os slides de
uma apresentação, e o que os transcritores fazem do mesmo jeito). O `extrator_comum.py` e
os `leitor_<tipo>.py` também não se rodam: são as partes do `extrator.py`. O
`extrator_comum.py` serve também ao `itens.py` e ao `conferencia.py`, que leem as
transcrições do mesmo jeito que o extrator as escreve.

---

*Este documento está licenciado sob [CC BY-NC-SA 4.0](../LICENSE-CONTENT.txt).*
