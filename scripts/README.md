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
| A biblioteca <dfn>genanki</dfn> (`pip install genanki`) | monta o arquivo do Anki, no `montar_deck.py` e no teste dele |
| O <dfn>Tesseract</dfn> ([tesseract-ocr](https://github.com/tesseract-ocr/tesseract)), com os dados de cada idioma do texto das figuras (`por`, o português) e os do inglês (`eng`), que os testes usam | faz o [OCR](../metodologia-de-conteudo.md#o-texto-das-figuras) do texto das figuras, no `transcrever_html.py` e no `transcrever_pptx.py`, e das páginas de PDF que o `extrator.py` lê pelo OCR; e nos [testes](testes/README.md) do extrator, da conferência e das aulas em pptx |
| O <dfn>LibreOffice</dfn> ([libreoffice.org](https://www.libreoffice.org/download/)) | faz o PDF de cada aula, de onde sai a imagem de cada slide na conferência das transcrições, e converte as imagens que o Tesseract ou o GraphicsMagick não leem (EMF, WMF, SVG); e no teste das aulas em pptx |
| O <dfn>Poppler</dfn> ([poppler.freedesktop.org](https://poppler.freedesktop.org/)) | lê PDF: faz a imagem de cada slide, do PDF da aula, lê as fontes em PDF do material de fora, no `base_externa.py` e na conferência das referências, e tira o texto, o negrito e o itálico das fontes em PDF, no `extrator.py`; e nos testes do extrator, da conferência e das aulas em pptx |
| O <dfn>GraphicsMagick</dfn> ([graphicsmagick.org](http://www.graphicsmagick.org/download.html)) | faz a cópia em PNG de cada imagem que não está em PNG, na conferência das transcrições; e no teste das aulas em pptx |
| O [git](../.githooks/README.md) | diz o que vai com o projeto, no `protege_fontes.py`, no `confere_indice.py` e no `glossario.py`; e nos testes destes dois |

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
| Sempre que o arquivo de formato, a tabela da leitura, a tabela dos destinos ou a análise de uma aula muda, e antes de escrever o material | `confere_moldes.py` |
| Para saber qual unidade escrever, e depois de escrever ou mudar o texto ou os cartões de uma unidade | `confere_material.py` |
| Antes de escrever uma unidade, para saber o que escrever nela e o que ler | `lista_de_trabalho.py` |
| Quando nem a aula nem o livro-texto chegam a um subtópico de uma unidade | `base_externa.py`, que roda o `referencias.py` |
| Com as planilhas de pergunta e as provas dos cartões prontas | `confere_cartoes.py` |
| Com as planilhas conferidas, e sempre que uma delas muda | `montar_deck.py` |
| Sempre que um documento define um termo novo, ou deixa de definir | `glossario.py` |
| Sempre que um documento entra no projeto, sai dele ou muda de lugar | `confere_indice.py` |
| Antes de publicar | `protege_fontes.py` |
| Depois de mudar um script que tem teste | o teste dele e os estragos dele ([Os testes](#os-testes)) |

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
| `coluna_trechos` | a coluna das planilhas de pergunta com os códigos dos trechos de cada cartão, ou `null` ([`confere_material.py`](#confere_materialpy--confere-o-texto-e-os-cartões-de-cada-unidade)) |

## O arquivo de formato

O [arquivo de formato](../metodologia-de-conteudo.md#onde-o-formato-fica-gravado),
`dados/formato.json`, guarda as decisões do formato que os scripts usam, só como nomes e
listas, sem explicação. Ele nasce de uma cópia do modelo em branco,
[`modelo-dados/formato.json`](../modelo-dados/formato.json).

| Informação | O que guarda |
| --- | --- |
| `versao_schema` | a versão do molde que o arquivo segue |
| `cursos`, `disciplina` e `nivel` | para quem é o material: a lista dos cursos, o nome da disciplina, que é também o da pasta de cima no Anki, e o nível |
| `idioma` | o idioma do material, como `pt-BR`, o português do Brasil |
| `ultima_aula` | a última aula que tem material, pela chave com que as análises das aulas a escrevem |
| `partes_para_tratar` | quantas partes do molde de uma unidade os trechos de uma aula ocupam, pelo menos, para que a aula [trate](../metodologia-de-conteudo.md#o-limite-das-aulas) dela |
| `documentos_vem_de` | de onde vêm os documentos de cada trecho: `regras`, os do grupo e do caminho dele; `destino`, os das unidades que o destino dele nomeia ([`confere_moldes.py`](#confere_moldespy--confere-os-moldes-contra-as-análises-das-aulas)); uma das duas, ou as duas |
| `grupos` | os grupos da matéria; `pelo_assunto: true` marca o grupo cujo trecho vai para o documento do assunto dele, que a tabela da leitura diz |
| `partes_por_tipo` | a sequência das partes de um texto, cada parte com os `tipos` de conhecimento que ela recebe |
| `tipos_junto` | os tipos sem parte própria, que ficam junto do assunto que acompanham |
| `fora` | as regras que tiram um trecho do material: sai o trecho cujos tipos são todos de uma regra |
| `marcas` | as marcas, que só dizem do que um trecho fala: cada uma com o `texto` que as análises escrevem e os `papeis`, os campos da análise onde ele se procura |
| `onde_se_ensina` | para cada tipo, os documentos onde ele se ensina |
| `documentos` | os documentos do material, na ordem em que se escrevem em cada aula, cada um com o `molde` dele e, para as fontes dos documentos, os `grupos` e os `caminhos` cujos trechos ele recebe pelas regras, ou `todos: true`, quando recebe todos os trechos |

Cada grupo, parte, regra, marca, documento e unidade entra na lista dele entre chaves,
`{ }`, com um `id`, um código curto, e um `nome`; o id vai entre aspas, mesmo quando é
número. Num documento, `unidade` é o nome do que ganha material nele, como "bactéria" ou
"tema", e `unidades`, quando ele as lista, são as unidades dele. Numa ficha, uma unidade
pode ter `itens`, cada um com `id` e `nome`: as coisas que ela reúne, cada uma com os
eixos da grade dela. Cada um dos `conjuntos` de um documento junta unidades ou itens dele,
os `membros`, que o destino de um trecho nomeia de uma vez: o trecho que nomeia um
conjunto vai para cada membro dele. `tratada_em`, numa unidade sem itens ou num item, diz
as aulas que tratam dele, no lugar da conta do limite. O `molde` diz como o documento se
divide:

- `partes_por_tipo`: o texto de cada unidade segue a sequência das partes; `casos`, se o
  documento tem, são as partes de cada caso;
- `eixos`: a ficha, uma tabela com uma linha para cada eixo. `abertura` são as partes que
  vêm antes dos eixos, cada uma com `recebe_trechos`, que diz se trechos das aulas vão
  para ela; `eixos` é a grade do documento, e cada eixo pode ter `subtopicos`; a unidade
  que tem os seus `eixos` usa esses, e a que não tem usa os do documento; `elos` são as
  partes do dicionário, cada uma com os `eixos` que a alimentam;
- `formas`: as perguntas de prova; `pergunta` são as partes de cada pergunta, e `formas`,
  as formas de pergunta, cada uma com o `verbo` e os `tipos` que ela pede;
- `colunas`: os cartões, cada coluna com o `lado` dela, `frente` ou `verso`, e `imagem:
  true` na coluna que traz o nome de um arquivo de imagem. O `id` da coluna é também a
  classe dela no estilo dos cartões e dá o nome do campo dela no Anki
  ([`montar_deck.py`](#montar_deckpy--das-planilhas-de-pergunta-ao-baralho-do-anki)); por
  isso, só tem letras sem acento, algarismos, `_` e `-`, e começa com uma letra.

A `ordem` de cada parte diz de onde vem o lugar dela: `dada`, quando a análise da matéria
o dá, ou `proposta`, quando a análise o deixava aberto e o projeto o propôs.

A leitura do formato é a mesma em todo script que o usa: ela confere o arquivo contra o
molde dele, `scripts/esquemas/formato.schema.json`, e as ligações de dentro dele — por
exemplo, que cada grupo, tipo, documento e eixo que o arquivo cita existe, que cada
documento tem as partes que o molde dele pede, que nenhum id se repete onde precisa ser
único e que cada membro de um conjunto é uma unidade ou um item do documento dele. Cada
problema sai numa linha `ERRO`, com o lugar, e o script não usa o formato.

Um exemplo inventado, com três documentos: um de temas, que segue a sequência das partes,
com dois temas, um deles com as aulas que tratam dele; uma ficha com uma abertura, um eixo
dividido em dois subtópicos, outro sem divisão, um elo, duas unidades, uma delas com dois
itens, e um conjunto das duas; e os cartões, com uma coluna de imagem:

```json
{
  "versao_schema": 1,
  "cursos": ["Curso de Exemplo"],
  "disciplina": "Disciplina de Exemplo",
  "nivel": "entender e aplicar",
  "idioma": "pt-BR",
  "ultima_aula": "4",
  "partes_para_tratar": 2,
  "documentos_vem_de": ["destino"],
  "grupos": [
    { "id": "1", "nome": "Seres" },
    { "id": "2", "nome": "Ideias gerais" }
  ],
  "partes_por_tipo": [
    { "id": "conceitos", "nome": "Conceitos", "tipos": ["Conceito e vocabulário"], "ordem": "dada" },
    { "id": "porques", "nome": "Por quê", "tipos": ["Causa e efeito"], "ordem": "proposta" }
  ],
  "tipos_junto": ["Exemplo recorrente"],
  "fora": [
    { "id": "enfeite", "nome": "não é conteúdo", "tipos": ["Não é conteúdo de estudo"] }
  ],
  "marcas": [
    { "id": "outro", "nome": "fala de outro assunto", "texto": "outro assunto", "papeis": ["destino"] }
  ],
  "onde_se_ensina": {
    "Conceito e vocabulário": ["ideias"],
    "Causa e efeito": ["ideias", "fichas"]
  },
  "documentos": [
    {
      "id": "ideias", "nome": "Ideias gerais", "unidade": "tema", "molde": "partes_por_tipo",
      "grupos": ["2"],
      "unidades": [
        { "id": "T1", "nome": "Primeiro tema" },
        { "id": "T2", "nome": "Segundo tema", "tratada_em": ["3"] }
      ]
    },
    {
      "id": "fichas", "nome": "Ficha de cada ser", "unidade": "ser", "molde": "eixos",
      "grupos": ["1"],
      "abertura": [
        { "id": "chaves", "nome": "Palavras-chave", "ordem": "dada", "recebe_trechos": false }
      ],
      "eixos": [
        {
          "id": "1", "nome": "Primeiro eixo", "ordem": "dada",
          "subtopicos": [
            { "id": "1.1", "nome": "Primeira parte do primeiro eixo" },
            { "id": "1.2", "nome": "Segunda parte do primeiro eixo" }
          ]
        },
        { "id": "2", "nome": "Segundo eixo", "ordem": "dada" }
      ],
      "elos": [
        { "id": "1", "nome": "Primeiro elo", "eixos": ["1", "2"], "ordem": "proposta" }
      ],
      "unidades": [
        { "id": "A1", "nome": "Primeiro ser" },
        {
          "id": "A2", "nome": "Segundo ser",
          "itens": [
            { "id": "A2a", "nome": "Primeira forma do segundo ser" },
            { "id": "A2b", "nome": "Segunda forma do segundo ser" }
          ]
        }
      ],
      "conjuntos": [
        { "id": "seres", "nome": "Todos os seres", "membros": ["A1", "A2"] }
      ]
    },
    {
      "id": "cartoes", "nome": "Cartões", "unidade": "fato", "molde": "colunas", "todos": true,
      "colunas": [
        { "id": "pergunta", "lado": "frente", "ordem": "dada" },
        { "id": "resposta", "lado": "verso", "ordem": "dada" },
        { "id": "esquema", "lado": "verso", "ordem": "proposta", "imagem": true }
      ]
    }
  ]
}
```

## `validar_dados.py` — confere um arquivo de dados

**O que faz.** Cada arquivo de dados — como o `projeto.json`, o arquivo de formato, o de
fontes, a base de cada unidade e a prova de cada planilha — tem uma forma certa, descrita
num molde, o <dfn>schema</dfn>, em `scripts/esquemas/`. O script confere se o arquivo segue
o molde: se não falta campo obrigatório, se nada está no tipo errado ou abaixo do mínimo
que o molde pede, se nenhuma lista repete um valor que não pode repetir, se nenhum código
(id ou chave) se repete.

**Como rodar.** O caminho do arquivo depois do nome do script:

    python scripts/validar_dados.py dados/formato.json

O molde se acha pelo nome do arquivo (o de `formato.json` é `formato.schema.json`). A base
de uma unidade tem o id dela no nome, e a prova, o nome da planilha; para elas, `--schema`
diz o molde (`base.schema.json` ou `prova.schema.json`):

    python scripts/validar_dados.py dados/bases/[item].json --schema scripts/esquemas/base.schema.json

**O que mostra.** `0 erro(s)`, quando está tudo na forma certa. Senão, cada linha `ERRO`
diz onde está o problema: `$.grupos[2].id: deve ser string` quer dizer que, no terceiro
grupo da lista `grupos`, o `id` tem de ser um texto (a contagem começa do zero).

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

Se o arquivo de formato existe, o script o lê antes, como diz [O arquivo de
formato](#o-arquivo-de-formato), e, com algum problema nele, mostra cada um numa linha
`ERRO` e não grava nada. Vale também para o `registrar_fonte.py`, que roda o
`referencias.py` no fim: ele já gravou o registro da fonte, e não grava as referências nem
a conferência delas. O `base_externa.py` precisa do formato e o lê logo no começo.

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

## `confere_moldes.py` — confere os moldes contra as análises das aulas

**O que faz.** A análise de cada aula, na pasta protegida, tem uma linha para cada [trecho
das aulas](../docs/analise-da-materia.md#2-as-aulas-slide-por-slide): o texto dele e os
campos que dizem o tipo de conhecimento, o grupo, o caminho e o destino, o texto que diz
para onde ele vai. O script põe cada trecho no lugar dele em cada documento do [arquivo de
formato](#o-arquivo-de-formato). Os documentos do trecho vêm das fontes que o formato diz
em `documentos_vem_de` — as regras, pelo grupo e pelo caminho dele, e o destino, pelas
unidades que ele nomeia —, e o trecho com lugar vai também para cada documento que recebe
todos. Dentro do documento, o lugar é a unidade ou o item de que o trecho fala — o próprio
documento, quando ele não lista unidades — e a parte do molde: a parte da sequência de
cada tipo do trecho, um eixo da ficha, a forma de pergunta, o cartão. O trecho que o
destino põe numa unidade com itens, fora da abertura dela, vai para os itens dela que o
destino nomeia. Depois, o script aplica o limite das aulas (abaixo). Confere que todo
trecho tem lugar e que nenhuma parte de molde fica sem trecho, e grava o relatório,
`CONFERENCIA-MOLDES.md`, em `docs/material-base/gerados-ocr/`: quantos trechos há em cada
classe — com lugar, sem lugar depois do limite, fora do material, marcados à espera de
lugar —; em cada documento, quantos trechos cada parte do molde recebe, de que aulas e se
a ordem dela é dada ou proposta; em cada documento que lista unidades, as aulas que tratam
de cada unidade e de cada item, com as partes, as que só os mencionam e quantos trechos de
depois da última aula ficam ali, e os conjuntos; as unidades só mencionadas; onde as
fontes do documento discordam, em cada sentido; os pedaços do destino sem linha na tabela
dos destinos; e os trechos até a última aula sem lugar depois do limite, com os lugares
que perderam.

**A forma das análises.** O arquivo `dados/forma-analise.json` diz como se lê uma análise:
o nome dos arquivos, as linhas que abrem um slide e as de título, a marca de cada trecho,
os separadores e os campos, em ordem, cada um com a forma do valor e, se tem, o papel
dele — `tipo`, `grupo`, `caminho` ou `destino` — e a `fonte` cujas páginas ele cita, pela
chave dela, como o campo do lugar no livro-texto. O destino e o lugar no livro se leem em
pedaços (a forma `pedacos`): o texto entre os separadores que a forma dá, fora dos
parênteses, cada pedaço inteiro, com o que está entre parênteses dele. O molde da forma é
`scripts/esquemas/forma-analise.schema.json`. Cada trecho tem um código,
`aula/slide/posição/hash`: a posição conta os trechos do slide, e o hash, tirado do texto
do trecho, muda quando o texto muda; assim, uma decisão guardada pelo código não passa para
um texto que mudou.

**A tabela dos destinos.** O destino é escrito à mão, e a mesma coisa aparece escrita de
jeitos diferentes. A tabela dos destinos, `docs/material-base/gerados-ocr/destinos.tsv`,
diz o que cada pedaço do destino nomeia: um arquivo de texto com duas colunas separadas por
tabulação, `destino` e `unidade`, e uma linha para cada id que o pedaço nomeia — o de uma
unidade, de um item ou de um conjunto do formato; a linha com a unidade vazia diz que o
pedaço não nomeia nenhum. As análises não mudam: a tabela só junta os jeitos de escrever o
mesmo nome. Ela fica na pasta protegida porque copia o texto das análises.

**A tabela da leitura.** O que as regras do formato e o destino não dizem sozinhos sai de
uma leitura dos trechos, gravada em `dados/lugares-lidos.tsv`: o eixo de cada trecho numa
ficha; a unidade dele, quando o destino não a nomeia; o documento do trecho que as fontes
deixam em aberto — o de um grupo que vai pelo assunto, o de um trecho marcado —; o lugar
novo do trecho que fica sem lugar (abaixo); e o trecho que a leitura pôs fora do material.
É um arquivo de texto com quatro colunas separadas por tabulação, `id`, `documento`,
`unidade` e `parte`, e uma linha para cada lugar, porque um trecho pode ter mais de um. A
`unidade` é o id de uma unidade, de um item ou de um conjunto do documento, ou fica vazia
quando o lugar vem do destino ou o documento não lista unidades; a `parte` é um eixo da
grade da unidade ou uma abertura que recebe trechos, e fica vazia num documento sem grade.
Na linha com o documento `fora`, a unidade é o id de uma regra de `fora` do formato.

Nas duas tabelas, a primeira linha é o cabeçalho, com os nomes das colunas; a linha em
branco não conta, e a linha sem as colunas vazias do fim vale como se as tivesse, porque o
editor que tira os espaços do fim da linha tira também essas tabulações.

**O limite das aulas.** O script aplica o
[limite](../metodologia-de-conteudo.md#o-limite-das-aulas) com a `ultima_aula` e o
`partes_para_tratar` do formato. Em cada unidade sem itens e em cada item, ele conta as
partes distintas do molde que os trechos de cada aula ocupam ali, só nos lugares diretos —
os do trecho que nomeia a unidade ou o item, não os que vêm de um conjunto —, e
`tratada_em`, quando existe, diz as aulas que tratam, no lugar da conta. O
lugar novo do trecho de uma aula até a última que fica sem lugar — porque o limite tirou
todos os dele, ou porque as fontes não lhe dão documento — é uma linha da tabela da
leitura num documento que as fontes não dão a ele, numa unidade com material, e não entra
na conta.

**Como rodar.**

    python scripts/confere_moldes.py

**O que mostra.** Cada problema numa linha, na tela e no fim do relatório, com o código do
trecho ou o lugar: `FALTA` para o que espera uma leitura ou uma decisão, como o pedaço do
destino sem linha na tabela dos destinos ou o trecho que espera um lugar; `ERRO` para o
que se contradiz entre as análises, as duas tabelas e o formato, como o id da tabela dos
destinos que o formato não tem. O relatório é gravado mesmo com eles, e o script sai com
código 1 quando há algum. Com erro numa entrada — um arquivo que falta, que não se lê, que
não segue o molde dele ou que não fecha com as outras —, cada um sai numa linha `ERRO` e
nada é gravado. No fim, quantos trechos há, quantos têm lugar e quantas linhas `ERRO` e
`FALTA`.

## `confere_material.py` — confere o texto e os cartões de cada unidade

**O que faz.** O material de estudo se escreve em arquivos `.md`, em `docs/material-gerado/`
e nas subpastas dela, um texto para cada unidade. O script confere se cada trecho das aulas
que a [conferência dos moldes](#confere_moldespy--confere-os-moldes-contra-as-análises-das-aulas)
põe numa unidade está no texto dela, na parte do molde em que ele cai, e se tem cartão. Diz
também o estado de cada texto e qual é o próximo a escrever. Não grava nada.

**Os textos.** Há um texto para cada unidade com material de um documento de conteúdo, como
a ficha de uma bactéria ou um tema da teoria (o do documento inteiro, quando ele não lista
unidades), e um para cada aula com trecho, nas perguntas de prova. As partes de cada texto
são as do molde do documento, na ordem dele: as da sequência e, no documento com casos, a
dos casos, depois dos fatos; numa ficha, a abertura e, em cada item que tem trecho (ou na
unidade, sem itens), os eixos da grade e, quando a grade é a do documento, os elos; nas
perguntas de prova, as formas de pergunta. A parte sem trecho pode ficar fora do texto. O
trecho que vai junto do assunto pode ficar em qualquer parte que recebe trechos; nas que não
recebem — a abertura que não recebe, como as palavras-chave, os elos e os casos —, nenhum.

**Os códigos escondidos.** O texto se liga aos trechos por comentários do Markdown, que a
visualização não mostra:

| Código | O que marca |
| --- | --- |
| `<!-- unidade X -->` | o começo do texto de código `X`: o id da unidade no arquivo de formato; o do documento, quando ele não lista unidades; a aula, nas perguntas de prova |
| `<!-- item X -->` | o começo do item de id `X` da unidade |
| `<!-- parte X -->` | o começo da parte de id `X`; a forma de pergunta vai pelo número dela, a partir de 1, e a parte dos casos é `casos` |
| `<!-- trecho X -->` | o trecho de código `X`, o que a análise da aula dá a ele, dentro da parte que o explica |

Abrir um nível fecha os de dentro dele: a marca de uma parte fecha a parte de antes, e a de
um item fecha também o item de antes. O que está num bloco de código, ou em código dentro da
linha, não conta. Um exemplo inventado, o começo da ficha da unidade `A1` do exemplo do
[arquivo de formato](#o-arquivo-de-formato), com o primeiro eixo:

```markdown
<!-- unidade A1 -->
# Primeiro ser

<!-- parte chaves -->
**Palavras-chave:** ...

<!-- parte 1 -->
O texto do primeiro eixo, que explica o trecho.
<!-- trecho 2/5/1/3f2a -->
```

**Os cartões.** O texto de uma unidade de documento de conteúdo tem a planilha de pergunta
dela, `perguntas-X.csv`: o prefixo das planilhas, do `projeto.json`, e o código do texto. Cada
cartão leva, na coluna que `coluna_trechos` diz, os códigos dos trechos de que trata,
separados por espaço, e, na que `coluna_subdecks` diz, a aula do texto. As perguntas de prova
não têm planilha: os trechos delas têm cartão nas unidades em que se explicam. Com
`coluna_trechos` em `null`, os cartões não se conferem; com `coluna_subdecks` em `null`, a
aula deles também não.

**A ordem de escrita.** Os textos das unidades vêm pela aula de cada um — a primeira aula,
até a última, que trata da unidade — e, na mesma aula, na ordem dos documentos e das
unidades no arquivo de formato. As perguntas de prova de uma aula vêm logo depois do último
texto de unidade com trecho dela, e só podem ser escritas com todos esses prontos.

**Como rodar.**

    python scripts/confere_material.py
    python scripts/confere_material.py --unidade [código]

**O que mostra.** Cada problema numa linha, com o arquivo e a linha quando os tem: `FALTA`
para o que ainda não está escrito, como um trecho sem o código dele no texto ou sem cartão;
`ERRO` para o que está fora do lugar ou não existe, como o código de um trecho numa parte
que não é a dele ou uma parte fora da ordem do molde. Depois, uma tabela com a aula, o
documento, a unidade, o código e o estado de cada texto, na ordem de escrita — `sem texto`,
quando nem o texto nem a planilha dele existem, `FALTA`, `ERRO` ou `pronta` —, a próxima a
escrever e as perguntas de prova que já podem ser escritas. O texto que não começou não dá
aviso. Com `--unidade`, só o texto do código dado: sem texto, ele é `FALTA`, e, nas perguntas
de prova, uma linha diz as unidades com trechos delas que ainda não estão prontas. Com aviso
na conferência dos moldes, ou com o mesmo código em dois textos, o script diz isso numa
linha `ERRO` e não confere nada. Sai com código 1 quando há `FALTA` ou `ERRO`.

## `lista_de_trabalho.py` — o que escrever e o que ler em cada unidade

**O que faz.** Antes de escrever o texto de uma unidade, o script grava a lista de trabalho
dele: tudo o que o texto tem de explicar, na ordem do molde, e o que ler antes de escrever.
Os textos, as partes de cada um e os trechos de cada parte são os do
[`confere_material.py`](#confere_materialpy--confere-o-texto-e-os-cartões-de-cada-unidade).
A lista fica na pasta protegida, porque copia o texto das aulas, em
`docs/material-base/gerados-ocr/listas/`, com o id do documento e o código do texto no nome,
como `bacteria-neisseria-meningitidis.md`.

**O que a lista tem.**

- O texto: a unidade, o documento e a aula em que ele se escreve; numa unidade, as aulas
  que tratam dela e as que só a mencionam, a planilha dos cartões, com as colunas dos
  códigos dos trechos e da aula, e a prova dos cartões.
- Os códigos escondidos, na ordem do molde, e os trechos de cada parte. De cada trecho: o
  código, a aula, o slide, o texto, cada campo da análise menos o destino, as marcas e,
  quando é assim, que ele está ali por um conjunto (o destino nomeia um grupo de que a
  unidade faz parte, como o gênero de uma bactéria) ou que é de uma aula depois da última.
  A parte que não recebe trechos, ou que não tem nenhum, diz isso.
- Os capítulos a ler inteiros: as transcrições da fonte que um campo da análise cita, como
  o lugar no livro-texto, que têm uma página citada por um trecho da unidade, na ordem dos
  nomes delas; e os pedaços do campo em que nenhuma página aparece, cada um com os trechos
  que o têm. A página se acha pelo título dela na transcrição, como `p. 248`, inteiro.
- As dúvidas abertas: do arquivo das dúvidas, a seção de cada aula com trecho na unidade e,
  inteiras, as que não são de nenhuma aula.

Nas perguntas de prova de uma aula, a lista só sai com todas as unidades com trechos dela
prontas no conferidor, e cada trecho diz também onde foi explicado: o arquivo, a linha e a
parte.

**O arquivo das dúvidas.** Um arquivo Markdown com uma seção por título de segundo nível,
`## `; a seção de uma aula começa pelo nome do arquivo da análise dela, sem a extensão, como
`## aula-13`.

**Como rodar.**

    python scripts/lista_de_trabalho.py --unidade [código] --duvidas [arquivo das dúvidas]

**O que mostra.** O arquivo gravado e quantas partes, trechos, transcrições a ler, pedaços
sem página e seções das dúvidas a lista tem. Com algum problema — como o código que nenhum
texto tem ou a conferência dos moldes com aviso —, cada um sai numa linha `ERRO`, com o
motivo, e nada é gravado.

## `base_externa.py` — monta a base do material de fora

**O que faz.** Monta a [base de trechos](../metodologia-de-conteudo.md#o-material-de-fora)
de cada unidade com grade a partir das cópias do material de fora: o script recolhe todo o
texto das páginas declaradas, a IA decide o que cada frase é, e a pessoa confere. Ninguém
copia trecho à mão.

**Os dados de cada unidade.** O arquivo `dados/bases/[item].json`, com o id da unidade no
lugar de `[item]`, nasce de uma cópia do modelo em branco,
[`modelo-dados/base.json`](../modelo-dados/base.json), em que aspas vazias, `""`, esperam
um texto; colchetes vazios, `[]`, uma lista; e chaves vazias, `{}`, pares de um nome e um
valor, como `"1.1": "aula"`, separados por vírgula. O `versao_schema` fica como está. O
resto:

- em `item`, o id da unidade no arquivo de formato, de um documento cujo molde tem grade
  (`eixos`);
- em `lugares`, uma entrada para cada fonte lida, entre chaves, com: em `fonte`, a chave
  da referência dela; em `arquivo`, o caminho da cópia, a partir da pasta principal do
  projeto, em `docs/material-base/fontes-externas/`; e, se a cópia for PDF, em `paginas`,
  a lista das páginas do arquivo lidas, como `[47, 48]`. Se o arquivo estiver fora da
  pasta protegida, o script pergunta se pode levá-lo para a pasta das cópias e corrige o
  caminho aqui; com `--mover`, leva sem perguntar. Em `desloca`, quanto somar à página do
  arquivo para chegar ao número impresso — se a página 47 do arquivo tem impresso "45", é
  `-2`; se são iguais, `0`. Se a diferença muda de uma página para outra, `impressas` dá o
  número impresso de cada página do arquivo: `{"47": "45", "48": "xii"}`;
- em `cobertura`, cada subtópico da grade da unidade — os eixos dela ou, quando ela não
  tem os seus, os do documento —, pelo id, com a marca dele: `aula` (a aula cobre),
  `fonte` (vem do material de fora) ou `lacuna` (nenhuma fonte cobre). Um eixo sem
  subtópicos é marcado pelo id do próprio eixo;
- `classes` e `juntar` começam vazios; são preenchidos depois da primeira rodada.

Um exemplo inventado, da unidade `A1` do exemplo do [arquivo de
formato](#o-arquivo-de-formato), cuja grade tem o eixo 1 dividido nos subtópicos 1.1 e 1.2
e o eixo 2 sem subtópicos, lida nas páginas 47 e 48 de uma fonte em PDF:

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
- `outro-item` (de outra unidade), `repetida` (com `de`: o código da frase que ela
  repete), `fora-do-recorte` ou `nao-e-conteudo` (referência, cabeçalho, legenda solta).

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

Com tudo classificado, a rodada seguinte grava a base da unidade, e a conferência,
`CONFERENCIA-TRECHOS.md`, em `docs/material-base/gerados-ocr/`, mostra cada página com as
frases e a classe de cada uma, com os tiques da IA e da pessoa.

**Como rodar.**

    python scripts/base_externa.py

Ele refaz sempre todas as unidades de uma vez: a conferência é um arquivo só, e é assim
que os tiques de todas continuam nela.

**O que mostra.** Antes de tudo, o script lê o arquivo de formato, como diz [O arquivo de
formato](#o-arquivo-de-formato): com algum problema nele, cada um aparece numa linha
`ERRO`, nenhuma base é gravada e a conferência não é refeita. Depois, uma linha `ERRO`
para tudo o que falta ou se contradiz: unidade que o formato não tem, ou cujo documento
não tem grade, frase sem classe, subtópico sem marca, subtópico marcado como `fonte` sem
nenhuma frase usada, frase usada num subtópico que a aula já cobre ou que está marcado
como `lacuna`. Com `ERRO`, a base da unidade não é gravada: o arquivo dela fica só com
esse aviso. Se uma unidade nem pode ser lida — por exemplo, porque uma fonte dela ficou
fora da pasta protegida —, a conferência não é refeita, para não perder os tiques dela.
Quando a conferência é refeita, logo depois aparece o resultado das referências, porque a
base registra as fontes que usa.

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

**As chamadas.** Na coluna `fonte` da planilha vão só as chamadas, cada uma com o lugar:
`(Silva, 2020, p. 12)`, ou, com duas fontes, `(Silva, 2020, p. 12; Souza, 2019, slide 3)`.
O lugar é o título da página na transcrição (`p. 12`, `slide 3`) ou a página da frase na
base; fonte sem páginas, como uma página da internet, vai sem lugar. O script reconhece
cada chamada pelo arquivo de chamadas, `dados/chamadas.json`, escrito à mão pelas [Regras
da ABNT](../regras-abnt.md#citação-no-texto-nbr-105202023): uma entrada para cada fonte,
entre chaves, com a `chave` dela — a mesma do registro da fonte na transcrição e na base —
e a `chamada`, entre parênteses, sem o lugar. Ele nasce de uma cópia do modelo em branco,
[`modelo-dados/chamadas.json`](../modelo-dados/chamadas.json), e o molde dele é
`scripts/esquemas/chamadas.schema.json`. Um exemplo inventado:

```json
{
  "versao_schema": 1,
  "chamadas": [
    { "chave": "SILVA-2020", "chamada": "(Silva, 2020)" },
    { "chave": "SOUZA-2019", "chamada": "(Souza, 2019)" }
  ]
}
```

**Como rodar.**

    python scripts/confere_cartoes.py

**O que mostra.** Uma linha `ERRO` para cada coisa que não bate: a planilha fora do UTF-8,
sem as colunas `pergunta`, `resposta` e `fonte` ou com um cartão com mais valores que
colunas; cartão sem pergunta, cartão sem prova, prova sem cartão (a pergunta mudou só de
um lado), pergunta repetida; chamada que não é de nenhuma fonte, lugar que a fonte não
tem, trecho que não está no lugar citado, lugar citado sem trecho, prova que diz que a
fonte afirma quando a base marca o trecho como possibilidade. Na comparação, a quantidade
de espaços, as quebras de linha e as marcas de destaque (itálico, negrito) não contam; as
letras e a pontuação contam. No fim, quantos cartões há, quantos têm erro e quantos estão
sem o tique da pessoa. A conferência mostra cada cartão com a pergunta, a resposta, a
fonte, os trechos e onde cada um foi achado; se o cartão, a prova ou o texto da fonte
mudam depois do tique, o tique sai. Sem o arquivo de chamadas, com ele fora do molde ou
com duas fontes com a mesma chamada, que não diria de qual delas é o trecho, cada problema
sai numa linha `ERRO` e nada é gravado.

## `montar_deck.py` — das planilhas de pergunta ao baralho do Anki

**O que faz.** Transforma cada planilha de pergunta (os arquivos `perguntas-*.csv` de
`docs/material-gerado/`) num baralho pronto para importar no Anki, um arquivo `.apkg`. As
colunas do cartão são as do documento de molde `colunas` do [arquivo de
formato](#o-arquivo-de-formato), na ordem dele: cada uma vira um campo do cartão, no lado
dela, com o nome da coluna sem o sublinhado e com cada palavra em maiúscula
(`tipo_pergunta` vira `TipoPergunta`), e o campo vazio não aparece. A coluna de imagem
traz o nome de um arquivo da pasta das imagens dos cartões,
`docs/material-base/imagens-dos-cartoes/`: o cartão mostra a imagem, e o arquivo vai junto
no pacote. No `projeto.json`, `colunas_ocultas` diz as colunas que ficam guardadas no
cartão sem aparecer, e `coluna_subdecks`, a coluna que divide o baralho — ou `null`,
escrito assim, sem aspas, para não dividir. A aparência dos cartões (cores, tamanho da
letra) vem de `dados/estilo-cartao.css`, em que cada coluna tem a classe do id dela, como
`.pergunta`.

**No Anki.** Os cartões ficam numa pasta com o nome da disciplina, que vem do arquivo de
formato; dentro dela, uma pasta para cada valor da coluna que divide, com o nome da coluna
e o valor (`Aula 13`, na coluna `aula` com o valor `13`); e, dentro dessa, uma para cada
planilha. O cartão novo entra na posição da linha dele na planilha. O código de cada
cartão no Anki sai do nome da planilha e da pergunta, sem contar os espaços: corrigir a
resposta ou pôr uma imagem atualiza o mesmo cartão, com o histórico de revisão, e mudar a
pergunta faz um cartão novo.

**Onde fica o pacote.** O da planilha com alguma imagem fica em
`docs/material-base/baralhos-com-imagens/`, na pasta protegida, porque a imagem de um slide
ou do livro é material de outras pessoas, que nunca se publica ([`NOTICE.md`](../NOTICE.md));
o da planilha sem imagem, em `anki-decks/`, que vai com o projeto. O pacote da mesma
planilha que estiver na outra pasta sai.

**Como rodar.**

    python scripts/montar_deck.py

Com uma parte do nome de uma planilha depois do nome do script, só as planilhas que a têm
no nome; com `--listar`, só a lista das planilhas que seriam usadas, sem gerar nada.

**O que mostra.** Cada baralho gerado, com as pastas e quantos cartões e imagens tem. Uma
linha `ERRO` diz cada problema de uma planilha, que fica sem baralho: uma coluna do molde
que falta, uma coluna que não é do molde nem oculta, uma coluna repetida, o texto fora do
UTF-8, um cartão com mais valores que colunas, sem pergunta, com a pergunta de outro (sem
contar os espaços) ou sem valor na coluna que divide, uma imagem que não é só o nome de um
arquivo ou que não está na pasta das imagens; e duas planilhas com o mesmo nome no Anki
ficam as duas sem baralho. Antes de gerar qualquer baralho, o script lê o arquivo de
formato, como diz [O arquivo de formato](#o-arquivo-de-formato), e confere as colunas: com
algum problema — sem o documento dos cartões, sem a coluna `pergunta` ou sem coluna na
frente, uma coluna oculta que é do molde, uma coluna que divide que não é do molde nem
oculta, uma coluna que dá o nome de um campo que o próprio Anki preenche, como `Tags`, ou
que o Anki muda ao importar, duas colunas que dão o mesmo campo —, cada um aparece numa
linha `ERRO` e nenhum baralho é gerado.

## Os testes

Os testes dos scripts ficam em `scripts/testes/`, uma pasta para cada parte, e o [README
dos testes](testes/README.md) diz o que cada um confere e como rodar. O `estraga.py` prova
que um teste pega os defeitos: roda o teste contra cópias da pasta `scripts/`, cada uma
com um defeito posto de propósito, um estrago da lista do teste.

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

Não se roda: é a parte que os outros scripts compartilham (achar o `projeto.json`, as
planilhas de pergunta, os cartões e a prova de cada uma, ler o arquivo de formato, conferido contra o
molde dele e nas ligações de dentro dele, e achar nele as unidades, os itens e os
conjuntos de um documento, a grade de cada unidade e o que cada id quer dizer, ler o
registro da fonte, guardar os tiques, ler as páginas de um documento HTML e os slides de
uma apresentação, e o que os transcritores fazem do mesmo jeito). O `extrator_comum.py` e
os `leitor_<tipo>.py` também não se rodam: são as partes do `extrator.py`. O
`extrator_comum.py` serve também ao `itens.py` e ao `conferencia.py`, que leem as
transcrições do mesmo jeito que o extrator as escreve. Do mesmo modo, o `analises.py`, o
`lugares.py`, o `tabela.py`, o `destinos.py`, o `lidos.py`, o `limite.py` e o
`relatorio.py` são as partes do `confere_moldes.py`: leem as análises das aulas pela forma
delas, dizem onde cada trecho cai pelas regras do formato, leem as tabelas em texto, dão a
cada trecho o que o destino dele nomeia, leem a tabela da leitura, aplicam o limite das
aulas e fazem as tabelas do relatório. O `marcas.py` é a parte do `confere_material.py` que
lê os códigos escondidos de um texto e confere cada um contra o lugar em que ele deveria
estar.

---

*Este documento está licenciado sob [CC BY-NC-SA 4.0](../LICENSE-CONTENT.txt).*
