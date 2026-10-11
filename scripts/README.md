# Scripts

## O que é um script, e por que o método usa

Um script é um programa pequeno que faz sozinho um trabalho repetitivo, sempre do mesmo
jeito, não importa quem rode nem quantas vezes. É por isso que o método confia neles pra
parte mecânica: montar as referências, as conferências e o baralho sem esquecer nada e
sem inventar nada. O que um script não faz é julgar se um conteúdo está certo — isso é
sempre de uma pessoa.

Nenhum script tem nada de disciplina dentro dele, nem caminho de pasta: o que muda de um
projeto pra outro fica nos arquivos de dados do projeto. Os únicos nomes fixos são os do
próprio motor — a pasta `scripts/`, tudo o que está dentro dela e o `projeto.json` — e
eles nunca se mudam: é por esses nomes que os scripts se acham uns aos outros. A pasta do
material de base, `docs/material-base`, também nunca muda de nome nem de lugar: é a pasta
protegida, onde fica todo o material de terceiros (ver o `protege_fontes.py`, abaixo).

## Antes da primeira vez

Você precisa de três coisas. Faça uma vez só, no seu computador.

1. **O Python**, o programa que roda os scripts. Pra saber se já tem, abra o terminal
   (veja abaixo como) e digite `python --version`. Se aparecer algo como
   `Python 3.12.1`, está pronto. Se aparecer erro, tente `python3 --version`; se as duas
   derem erro, instale o Python pelo site [python.org](https://www.python.org/downloads/).
   Se no seu computador o que funcionou foi `python3`, use `python3` no lugar de
   `python` em todos os comandos deste guia.
2. **O mapa do projeto**, o arquivo `projeto.json`. Copie
   [`modelo-dados/projeto.json`](../modelo-dados/projeto.json) pra pasta principal do
   projeto da sua disciplina. Ele diz aos scripts onde fica cada coisa: onde estão as
   aulas, onde ficam as transcrições, onde sai o baralho. Se um dia você mudar uma pasta
   de lugar, muda só nesse arquivo — nenhum script precisa ser mexido. A única que não
   muda é a do material de base, `docs/material-base`, onde fica tudo o que tem texto de
   terceiros: é por ter nome e lugar fixos que a lista do que nunca vai pro GitHub (o
   arquivo `.gitignore`) a deixa sempre de fora. Os caminhos ficam em `caminhos`; entre
   eles, `imagens` é a pasta onde as conferências gravam as imagens das páginas; e
   `licenca_conteudo`, o arquivo da licença do conteúdo. Fora dos caminhos ficam: `prefixo_planilhas`, o começo do nome de toda
   planilha de pergunta (no modelo, `perguntas-`); `resolucao_imagens`, a resolução das
   imagens das conferências, em pontos por polegada; `nome_licenca_conteudo`, o nome da
   licença do conteúdo, que sai no rodapé da lista de referências; e `colunas_ocultas` e
   `coluna_subdecks`, que o `montar_deck.py` usa (ver a seção dele, mais abaixo). Copie
   também o [`modelo-dados/estilo-cartao.css`](../modelo-dados/estilo-cartao.css) pra pasta
   `dados/` do projeto: é a aparência dos cartões do Anki (cores, tamanho da letra), e
   você pode mudá-la ali. A pasta `scripts/` já está no projeto, que é uma cópia do
   modelo inteiro, com as subpastas `esquemas/` e `normas/`: são os próprios scripts e os
   arquivos que eles leem. Não mude o nome dela nem de nada lá dentro.
3. **Quatro complementos**, só pra alguns scripts:
   - pro `montar_deck.py`, a biblioteca `genanki`, um complemento do Python que sabe
     montar os arquivos do Anki: no terminal, digite
     `pip install genanki` (ou `pip3 install genanki`) e aperte Enter;
   - pro `conferencia.py` e o `base_externa.py`, e pro `referencias.py` e o
     `registrar_fonte.py` quando a fonte é PDF, o Poppler, que é o que lê o texto de uma
     página de PDF e a transforma em imagem (a conferência também o usa pra imagem dos
     slides de uma apresentação): no Linux, `sudo apt install poppler-utils`;
     no Mac, `brew install poppler`; no Windows, siga as instruções do Poppler pra
     Windows, ou peça à IA que você usa o passo a passo pro seu computador;
   - pro `transcrever_html.py` e o `transcrever_pptx.py`, quando a fonte tem imagem, o
     Tesseract, que lê o texto de uma imagem (o OCR), com os dados do idioma da fonte: no
     Linux, `sudo apt install tesseract-ocr tesseract-ocr-por` (troque o `por` do fim pelo
     código do idioma: `spa` pro espanhol, `eng` pro inglês); no Mac, `brew install
     tesseract tesseract-lang`; no Windows, peça à IA o passo a passo;
   - pro `transcrever_pptx.py`, quando a apresentação tem imagem num formato que o
     Tesseract não lê (EMF, WMF, SVG), e pro `conferencia.py`, quando a fonte é uma
     apresentação em pptx, o LibreOffice, que converte a imagem e faz a imagem de cada
     slide: no Linux, `sudo apt install libreoffice`; no Mac e no Windows, o instalador
     do site [libreoffice.org](https://www.libreoffice.org/download/).

## Como rodar um script

1. **Abra o terminal.** O terminal é a janela onde se digita um comando em vez de clicar.
   No VSCode (um editor gratuito, onde se abre a pasta do projeto): menu
   **Terminal → Novo Terminal** (ou as teclas `` Ctrl+` ``). Ele abre embaixo, já dentro
   da pasta do projeto. Se você usa outro programa, peça à IA o passo a passo pra abrir o
   terminal na pasta do projeto no seu computador.
2. **Digite o comando** que aparece na seção do script, aqui embaixo, e aperte Enter.
   Você pode estar em qualquer pasta dentro do projeto: o script sobe de pasta em pasta
   até achar o `projeto.json`, e calcula todo o resto a partir dali. A exceção é o
   `validar_dados.py`: ele lê o arquivo pelo caminho que você digitar, a partir da pasta
   onde o terminal está, então os exemplos dele são pra rodar na pasta principal do
   projeto.
3. **Leia o que aparece.** O script sempre diz o que fez. Uma linha que começa com
   `ERRO`, `FALTA` ou `CONFERIR` pede alguma coisa sua e diz o quê. Se não entender o que
   apareceu, copie a mensagem pra IA que você usa e peça ajuda.

Os comandos usam `scripts/...` porque os scripts ficam na pasta `scripts` do projeto. Se
eles estiverem em outro lugar, troque pelo caminho de onde estão. Os caminhos de exemplo,
como `dados/formato.json`, são os do modelo; no seu projeto, valem os do `projeto.json`.

## A ordem em que eles entram

| Quando | Script |
| --- | --- |
| Depois de responder o Descubra seu modelo | `validar_dados.py` |
| Pra transcrever uma fonte em HTML que marca as páginas impressas, como um livro digital | `transcrever_html.py` |
| Pra transcrever uma apresentação de slides em pptx | `transcrever_pptx.py` |
| Assim que cada transcrição é criada | `registrar_fonte.py`, que já roda o `referencias.py` |
| Sempre que mudar os dados das fontes | `referencias.py` |
| Com as transcrições prontas, antes de escrever o material | `conferencia.py` |
| Quando a aula não cobre um eixo de um item | `base_externa.py`, que também roda o `referencias.py` |
| Com as planilhas de pergunta e as provas dos cartões prontas | `confere_cartoes.py` |
| Com as planilhas de pergunta prontas e conferidas | `montar_deck.py` |
| Sempre que um documento define um termo novo, ou deixa de definir (e sozinho, com `--conferir`, antes de cada versão mandada ao GitHub, se a conferência das mensagens estiver ativa) | `glossario.py` |
| Sempre que um documento entra no projeto, sai dele ou muda de lugar (e sozinho, antes de cada versão mandada ao GitHub, se a conferência das mensagens estiver ativa) | `confere_indice.py` |
| Antes de publicar o projeto (e sozinho, antes de cada versão mandada ao GitHub, se a conferência das mensagens estiver ativa) | `protege_fontes.py` |

## `validar_dados.py` — confere um arquivo de dados

**Pra que serve.** Os arquivos de dados do projeto (o `projeto.json`, o `formato.json`, o
`fontes.json`, o arquivo de base de cada item, o de prova de cada
planilha e o `fluxo-ia.json`) têm uma forma certa, descrita num molde —
o *schema* — que fica em `scripts/esquemas/`. Este script confere se o arquivo segue o
molde: se não falta campo obrigatório, se nada está no tipo errado, se nenhum código (id
ou chave) se repete.

**Quando usar.** Depois de preencher qualquer um desses arquivos, e sempre que mexer
neles.

**Como rodar.** Escreva o caminho do arquivo depois do nome do script:

    python scripts/validar_dados.py dados/formato.json

O script acha o molde pelo nome do arquivo (o de `formato.json` é `formato.schema.json`).
Os arquivos de base têm o nome do item, e os de prova, o nome da planilha, então pra eles
diga o molde com `--schema` (`base.schema.json` ou `prova.schema.json`):

    python scripts/validar_dados.py dados/bases/AG1.json --schema scripts/esquemas/base.schema.json

**O que aparece.** `0 erro(s)` quer dizer que está tudo na forma certa. Senão, cada
linha `ERRO` diz onde está o problema. Por exemplo, `$.itens[2].id: deve ser string` quer
dizer: no terceiro item da lista `itens`, o `id` tem de ser um texto (a contagem começa
do zero, então `[2]` é o terceiro).

Usa só o Python: não precisa instalar nada.

## `transcrever_html.py` — transcreve uma fonte em HTML, como um livro digital

**Pra que serve.** Alguns materiais são documentos HTML que marcam onde começa cada página
impressa: é o caso do capítulo de um livro digital (EPUB), lido no computador ou num site.
Neles o texto é texto de verdade, e este script faz a transcrição sozinho, no padrão da
seção 1 da metodologia: copia o texto de cada página, sem ler nada, com o título que diz o
número impresso e a posição dela, que aqui é a ordem da página no documento, como
`## p. 117 (arquivo p. 2)`. Parágrafo vira uma linha; título, `###` ou menos; tabela,
tabela do Markdown (a que passa pra página seguinte continua lá depois de
`[continuação da tabela da p. X]`); índice e expoente, os caracteres próprios (CO₂, Mg²⁺);
negrito e itálico, texto puro. Cada imagem entra no lugar dela como a própria imagem,
`![imagem](caminho)`, que aparece na visualização do VSCode, seguida do texto escrito
dentro dela, lido por OCR, e de `[fim da imagem]`.

**Quando usar.** Pra começar a transcrição de uma fonte assim. Depois, registre cada
transcrição com o `registrar_fonte.py` e rode o `conferencia.py`.

**Como guardar a fonte.** Se você tem o documento, guarde-o na pasta protegida com as
imagens dele, nas mesmas pastas para onde ele aponta. Se ele só se lê num site, salve a
captura do que o navegador recebeu enquanto você o lia: abra o documento, aperte F12 (as
ferramentas do desenvolvedor), vá na aba Rede, marque a opção de não usar o cache e
deixe o filtro em "Tudo"; recarregue a página (F5), passe pelo documento inteiro, até o
fim, pra que tudo seja carregado, e clique com o botão direito na lista pra salvar tudo
como HAR, na pasta protegida. A captura guarda também os dados da sua sessão no site (os
cookies): o script nunca os lê, e a captura pode ser apagada depois que o script fizer a
cópia do documento.

**Como rodar.** O caminho do documento, ou o da captura com `--pasta`, a pasta dentro da
pasta protegida onde fica a cópia:

    python scripts/transcrever_html.py docs/material-base/LIVRO-2020/Text/cap1.xhtml
    python scripts/transcrever_html.py docs/material-base/cap1.har --pasta docs/material-base/LIVRO-2020

Com a captura, o script copia pra essa pasta cada documento com marca de página que ela
tem, com as imagens dele, e transcreve a cópia; `--documento cap1.xhtml` escolhe um só,
quando a captura tem mais de um. O idioma do texto das imagens é o que o documento declara,
traduzido pro código do Tesseract pela tabela de `scripts/normas/idiomas.json`; se o
documento não declara, ou pra escolher outro, use `--idioma` com o código do Tesseract:
`por`, `spa`, `eng`... ou vários juntos, como `spa+eng`. O script não
grava por cima de uma transcrição que já existe, porque o texto das imagens dela pode já
estar conferido; pra fazer de novo, acrescente `--substituir` (o registro da fonte, no
topo, continua).

**O que aparece.** Cada transcrição gravada, com quantas páginas e quantas imagens tem.
`FALTA` lembra de registrar a transcrição. `CONFERIR` avisa o que o script não conseguiu
fazer sozinho: um índice ou expoente sem caractere próprio (fica na linha), uma imagem que
não está na cópia, uma marca de página no meio de uma linha de tabela. `ERRO` aponta o que
impediu a cópia: a captura com duas versões diferentes do mesmo documento, ou um arquivo
da cópia que já existe com outro conteúdo.

Precisa do Tesseract, com o idioma, quando o documento tem imagem.

## `transcrever_pptx.py` — transcreve uma apresentação de slides em pptx

**Pra que serve.** Numa apresentação em pptx (o formato do PowerPoint, que o LibreOffice
e o Google Apresentações também gravam), o texto de cada slide é texto de verdade, guardado
dentro do arquivo. Este script faz a transcrição sozinho, no padrão da seção 1 da
metodologia: copia o texto de cada slide, sem ler nada, com o título que diz a posição
dele no arquivo, que é também o lugar que a citação usa, como `## slide 3 (arquivo p. 3)`.
Dentro do slide, o texto vem na ordem do arquivo, que é a ordem em que o PowerPoint o lê
em voz alta. O título do slide vira `###`; cada tópico, uma linha com `- ` (ou o número,
na lista numerada), recuada conforme o nível; tabela, tabela do Markdown; índice e
expoente, os caracteres próprios (CO₂, 10⁻⁶); o símbolo escrito com uma fonte de símbolos,
como a Symbol, o caractere de verdade (μ, ±), pela tabela de
`scripts/normas/simbolos.json`. Cada imagem entra no lugar dela, como no
`transcrever_html.py`: `![imagem](caminho)`, seguida do texto escrito dentro dela, lido
por OCR, e de `[fim da imagem]`. As imagens saem do pptx pra uma pasta ao lado dele, com
o nome dele. As notas do apresentador, se houver, vêm depois do slide, a partir de
`[notas do apresentador]`; o slide oculto começa com `[slide oculto]`.

**Quando usar.** Pra começar a transcrição de uma apresentação. Depois, registre a
transcrição com o `registrar_fonte.py` e rode o `conferencia.py`.

**Como rodar.** O caminho da apresentação, já na pasta protegida, e, com `--idioma`, o
idioma do texto das imagens, no código do Tesseract — `por`, `eng`, ou vários juntos, como
`por+eng`, quando as figuras misturam idiomas:

    python scripts/transcrever_pptx.py docs/material-base/AULA-1.pptx --idioma por+eng

O idioma é sempre dito assim, porque o que o pptx marca no texto é o idioma do corretor
ortográfico, que muitas vezes não é o do texto. O script não grava por cima de uma
transcrição que já existe; pra fazer de novo, acrescente `--substituir` (o registro da
fonte, no topo, continua).

**O que aparece.** A transcrição gravada, com quantos slides e quantas imagens tem.
`FALTA` lembra de registrar a transcrição. `CONFERIR` avisa o que o script não conseguiu
fazer sozinho: um índice ou expoente sem caractere próprio (fica na linha), um símbolo de
uma fonte que não está na tabela (fica como está), uma imagem recortada no slide (o OCR lê
a imagem inteira, inclusive o que o slide não mostra), um gráfico ou um objeto sem imagem
(aparecem só na imagem do slide, na conferência), uma imagem que é só um link. `ERRO`
aponta o que impediu a transcrição: o arquivo que não se lê como pptx (um download
incompleto, por exemplo) ou uma imagem que já existe na pasta com outro conteúdo.

A tabela da fonte Symbol é o mapeamento oficial dela pro Unicode, publicado pelo
consórcio Unicode (`VENDORS/ADOBE/symbol.txt`), sem os códigos de uso corporativo da
Adobe; quando um código tem dois caracteres, fica o que já está na forma normal (NFKC) e,
entre dois assim, o de menor código.

Precisa do Tesseract, com o idioma, quando a apresentação tem imagem, e do LibreOffice
quando alguma imagem está num formato que o Tesseract não lê.

## `registrar_fonte.py` — liga a transcrição à fonte dela

**Pra que serve.** Grava, no topo da transcrição (ou de outro documento gerado de uma
fonte), de qual arquivo ela veio: a chave da fonte, o caminho do arquivo e a impressão
digital dele — um código que muda se o arquivo mudar. É assim que os outros scripts sabem
qual arquivo de fonte corresponde a qual transcrição: pelo registro, não pelo nome dos
arquivos, que pode ter erro de digitação.

**Quando usar.** Assim que uma transcrição é criada.

**Como rodar.** Três coisas depois do nome do script: a transcrição, o arquivo de onde
ela veio e a chave da fonte — a mesma chave da referência dela no `fontes.json`:

    python scripts/registrar_fonte.py docs/material-base/gerados-ocr/AULA-1.md docs/material-base/AULA-1.pdf AULA-1

Se o arquivo da fonte estiver fora da pasta protegida (a do material de base, que nunca
é publicada), o script mostra pra onde ele iria e pergunta: digite `s` pra mover. Se ele
não for, nada é registrado. Pra mover sem a pergunta — por exemplo, quando é a IA que
roda o script e você já autorizou —, acrescente `--mover` no fim do comando.

**O que aparece.** A linha gravada e, logo depois, o resultado do `referencias.py`, que
este script roda sozinho no fim: se a chave ainda não tem referência, aparece
`FALTA REFERÊNCIA`; se há referências sem o tique da pessoa, aparece `CONFERIR`.

Precisa do Poppler quando a fonte é PDF, porque o `referencias.py`, que ele roda, mostra a
primeira página dela.

## `referencias.py` — monta as referências e a conferência delas

**Pra que serve.** Você, ou a IA, preenche no `fontes.json` os dados de cada fonte:
autoria, título, local, editora, data, endereço, data de acesso. O script escreve cada
referência no padrão da ABNT (NBR 6023), coloca em ordem alfabética e grava o arquivo de
referências do projeto (no modelo, `docs/REFERENCIAS.md`). Ninguém digita a referência à
mão. Ele monta também a chamada de cada fonte, o que vai no meio do texto, como
`(Silva, 2020)`, pela norma de citações (NBR 10520). As [Regras da ABNT](../regras-abnt.md)
explicam cada campo do `fontes.json` e o que cada norma pede.

Junto, ele monta a conferência das referências (no modelo, `CONFERENCIA-REFERENCIAS.md`,
na pasta das transcrições): cada referência e a chamada dela como ficaram, ao lado da
cópia da fonte — a primeira página, se for PDF —, com duas caixas de tique, uma pra IA e
outra pra pessoa. Confira se a referência bate com a folha de rosto ou com a página do
documento.

Três coisas dependem de você, nos dados: o campo `et_al`, no topo do arquivo, diz se uma
fonte com quatro autores ou mais aparece só com o primeiro, seguido de *et al.*, ou com
todos; o campo `idioma` de cada fonte diz em que língua sai o mês da data, e é
obrigatório quando a data tem mês; e o campo `participacao` (`org.`, `coord.`...) diz que
os autores organizaram a obra. O mês da data de acesso sai no idioma do texto, que vem
do formato da disciplina (`dados/formato.json`, no modelo). As expressões "Disponível em:"
e "Acesso em:" são as da norma e saem sempre assim. A abreviatura dos meses de cada
idioma fica em `scripts/normas/meses.json`: são as abreviaturas que a norma adota.

**Quando usar.** Sempre que mudar o `fontes.json`. O `registrar_fonte.py` já roda este
script sozinho.

**Como rodar.**

    python scripts/referencias.py

**O que aparece.** Quantas referências foram gravadas e onde. `ERRO` aponta o que falta
ou não pode ser nos dados, como uma data com mês numa fonte sem `idioma`; nesse caso nada
é gravado. `FALTA REFERÊNCIA` lista fonte registrada que ainda não tem dados no
`fontes.json`; `CONFERIR` lista as referências que ainda não têm o tique da pessoa.

O formato da disciplina pode faltar; se ele existe, o script o confere antes contra o
molde dele e, com algum problema, mostra cada um numa linha `ERRO` e não grava nada. Vale
também pro `confere_cartoes.py` e pro `registrar_fonte.py`, que usam o `referencias.py`:
o `confere_cartoes.py` não grava a conferência dos cartões, e o `registrar_fonte.py`, que
já gravou o registro da fonte, não grava as referências nem a conferência delas. O
`base_externa.py`, que também usa o `referencias.py`, precisa do formato e o confere logo
no começo (ver a seção dele).

Precisa do Poppler quando alguma fonte é PDF, pra mostrar a primeira página.

## `conferencia.py` — monta a conferência das transcrições

**Pra que serve.** Monta um arquivo pra conferir cada transcrição contra o original,
página por página. Se a fonte é PDF, cada página aparece com a imagem dela no PDF, ao lado
do que a transcrição tem pra ela, e duas caixas de tique, uma pra IA e outra pra pessoa: o
script não julga nada, só mostra, e quem confere é quem tica. Se a fonte é um documento
HTML (ver o `transcrever_html.py`) ou uma apresentação em pptx (ver o
`transcrever_pptx.py`), o texto da transcrição é cópia da fonte, e quem o confere é o
próprio script: em cada página, ou slide, as letras, os números e os sinais da
transcrição têm de ser os da mesma página na fonte, na mesma ordem, e também o título da
página e as imagens. Não contam os espaços, as marcas da transcrição (o `#` dos títulos,
as barras das tabelas, o `<br>`, `[slide oculto]`, `[notas do apresentador]`), a forma
dos índices e expoentes e a diferença entre o hífen e o sinal de menos. À mão, só o texto
de dentro de cada imagem: ela aparece com esse texto e com as duas caixas de tique. Na
apresentação, cada slide aparece também inteiro, como imagem, feita pelo LibreOffice, pra
ver o que só o desenho mostra; essa imagem não tem tique. A pessoa é sempre o último
elo.

**Quando usar.** Com as transcrições prontas e registradas, antes de escrever qualquer
material, e de novo sempre que uma transcrição mudar.

**Como rodar.**

    python scripts/conferencia.py

**O que aparece.** Quantas páginas há, quantas têm erro do script, quantas partes há pra
ticar (as páginas de PDF e as imagens dos documentos HTML e das apresentações) e quantas
ainda estão sem o tique da pessoa. Uma linha `ERRO` aparece pra transcrição sem
registro, com mais de uma fonte registrada ou cuja fonte mudou ou não existe; pra PDF da
pasta do material de base que não é a fonte de nenhuma transcrição; e, num documento HTML
ou numa apresentação, pra página cujo texto, título ou imagens não batem com a fonte, com
o trecho onde começa a diferença. O arquivo gerado (no modelo, `CONFERENCIA-COM-IMAGEM.md`,
na pasta das transcrições) fica melhor de ler na visualização do VSCode: abra o arquivo e
aperte `Ctrl+Shift+V`.

Precisa do Poppler quando alguma fonte é PDF ou apresentação, e do LibreOffice quando
alguma fonte é apresentação.

## `base_externa.py` — monta a base do material de fora

**Pra que serve.** Quando a aula não traz o que algum eixo pede pra um item, o fato vem
de um material de fora — um guia oficial, um livro, uma página da internet. Este script
monta a base desse material: um arquivo só com as frases que o item usa, copiadas letra
por letra da fonte, com a página de cada uma. Ninguém copia trecho à mão: o script
recolhe todo o texto das páginas que você declarar, a IA decide o que cada frase é, e a
pessoa confere.

**Como funciona, passo a passo.**

1. Copie [`modelo-dados/base.json`](../modelo-dados/base.json) pra `dados/bases/`, com o
   id do item no nome (por exemplo, `dados/bases/AG1.json`), e preencha. O modelo vem em
   branco: aspas vazias, `""`, esperam um texto; colchetes vazios, `[]`, uma lista; e
   chaves vazias, `{}`, pares de um nome e um valor, como `"1.1": "aula"`, separados por
   uma vírgula. O `versao_schema`, a versão do molde, fica como está. O resto:
   - em `item`, o id do item, o mesmo que ele tem no formato da disciplina;
   - em `lugares`, uma entrada pra cada fonte lida, entre chaves, com: em `fonte`, a
     chave da referência dela; em `arquivo`, o caminho da cópia, a partir da pasta
     principal do projeto (no modelo, as cópias ficam em
     `docs/material-base/fontes-externas/`); e, se a cópia for PDF, em `paginas`, a lista
     das páginas do arquivo que foram lidas, como `[47, 48]`. Se o arquivo estiver fora
     da pasta protegida, o script pergunta se pode levá-lo pra pasta das cópias do
     material de fora e corrige o caminho aqui; `--mover`, no fim do comando, leva sem
     perguntar. Em `desloca`, um número inteiro: quanto somar à página do arquivo pra
     chegar ao número impresso — se a página 47 do arquivo tem impresso "45", é `-2`; se
     os dois são iguais, é `0`. Se a diferença não for a mesma em todas as páginas, use
     `impressas`, com o número impresso de cada página do arquivo:
     `{"47": "45", "48": "xii"}`;
   - em `cobertura`, cada subtópico da grade do formato da disciplina, pelo id dele, e a
     marca dele: `aula` (a aula cobre), `fonte` (vem do material de fora) ou `lacuna`
     (nenhuma fonte cobre). Um eixo sem subtópicos é marcado pelo id do próprio eixo;
   - `classes` e `juntar` ficam vazios por enquanto: eles são do passo 3.

   Um exemplo inventado, de um item lido nas páginas 47 e 48 de uma fonte em PDF, numa
   grade com um eixo 1 dividido nos subtópicos 1.1 e 1.2 e um eixo 2 sem subtópicos:

   ```json
   {
     "versao_schema": 1,
     "item": "AG1",
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
2. Rode o script. Na primeira vez, todas as frases aparecem como **sem classe** no
   arquivo de conferência, cada uma com um código, como `GUIA-2020:p47:3f2a91c0`: uma
   frase da página 47 do arquivo da fonte GUIA-2020. O final do código é uma impressão
   digital do texto da própria frase. Se a frase mudar — o PDF foi trocado, ou a
   separação em frases mudou —, o código muda junto: a classe antiga aparece como
   "classe para frase que não existe" e a frase nova como "sem classe". Assim uma classe
   nunca passa de uma frase para outra sem ninguém ver.
3. A IA, ou você, classifica cada frase em `classes`, no arquivo de dados, pelo código:
   - `usa`, com o `subtopico` e a `afirmacao`: `categorica` se a fonte afirma,
     `possibilidade` se ela trata como possível ou provável;
   - `outro-item`, `repetida` (com `de`: o código da frase que ela repete),
     `fora-do-recorte` ou `nao-e-conteudo` (referência, cabeçalho, legenda solta).

   A separação em frases é mecânica: se ela partir uma frase em duas, junte os códigos em
   `juntar`; se juntar dois pedaços numa frase só, a classe vale pro pedaço inteiro.

   Em `classes`, cada frase é um par: o código dela e, entre chaves, `classe`, com a
   classe, e o que a classe pede (`subtopico` e `afirmacao`, ou `de`). Em `juntar`, cada
   grupo é uma lista com os códigos das frases que formam uma só, na ordem; a classe do
   grupo vai no código da primeira. Um exemplo inventado, na mesma grade de antes:

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
4. Rode de novo. Com tudo classificado, sai a base do item, e a conferência mostra cada
   página com as frases e a classe de cada uma, com os tiques da IA e da pessoa.

**Como rodar.**

    python scripts/base_externa.py

Ele refaz sempre todos os itens de uma vez: a conferência é um arquivo só, e é assim que
os tiques de todos os itens continuam nela.

**O que aparece.** Antes de tudo, o script confere o formato da disciplina contra o molde
dele, como o `montar_deck.py`: se houver algum problema nele, cada um aparece numa linha
`ERRO`, nenhuma base é gravada e a conferência não é refeita. Depois, uma linha `ERRO` pra
tudo o que falta ou se contradiz: frase sem classe, subtópico sem marca, subtópico
marcado como `fonte` sem nenhuma frase usada, frase usada num subtópico que a aula já
cobre ou que está marcado como `lacuna`, um id que aparece mais de uma vez na grade do
formato da disciplina (dois subtópicos com o mesmo id, mesmo em eixos diferentes, ou um
subtópico com o id de um eixo sem subtópicos). Com `ERRO`, a base do item não é gravada:
o arquivo dela fica só com esse aviso. Se um item nem puder ser lido — por exemplo,
porque uma fonte dele ficou fora da pasta protegida —, a conferência não é refeita, pra
não perder os tiques dele: resolva o erro e rode de novo. O script não julga se a classe
está certa — isso é a conferência. Quando a conferência é refeita, logo depois aparece o
resultado das referências: este script também roda o `referencias.py`, porque a base
registra as fontes que usa.

Precisa do Poppler quando alguma fonte é PDF.

## `protege_fontes.py` — confere que nenhuma fonte pode ser publicada

**Pra que serve.** O material de terceiros — as aulas, as transcrições, as cópias do
material de fora e tudo o que traz texto delas — fica numa pasta só, a pasta protegida
(`docs/material-base`), que nunca é publicada e nunca muda de nome nem de lugar. Este
script confere se alguma fonte registrada ficou fora dela e, se você usa o GitHub, se a
lista do que nunca vai pra lá deixa a pasta de fora.

Se a conferência das mensagens estiver ativa (ver o
[README dela](../.githooks/README.md)), ele também roda sozinho antes de cada versão
gravada pra mandar ao GitHub, e barra a versão que levar um arquivo da pasta protegida ou
uma cópia de uma fonte — mesmo com outro nome e em outra pasta, porque ele compara a
impressão digital de cada arquivo com a de cada fonte.

**Quando usar.** Sempre antes de publicar o projeto. Com a conferência das mensagens
ativa, ele roda sozinho a cada versão.

**Como rodar.**

    python scripts/protege_fontes.py

**O que aparece.** "Nenhuma fonte fora da pasta protegida." ou uma linha `ERRO` pra cada
problema, dizendo o que fazer. Quando é ele que barra uma versão, a mensagem diz como
tirar o arquivo dela sem apagá-lo do seu computador.

Usa só o Python; a parte do GitHub usa o git, o programa que guarda as versões, que quem
usa o GitHub já tem.

## Como ticar uma conferência

Os arquivos de conferência têm, em cada parte, duas linhas assim:

    - [ ] IA
    - [ ] pessoa

Pra ticar, abra o arquivo no VSCode, no modo de texto (não na visualização), e troque o
espaço entre os colchetes por um `x`: `- [x] pessoa`. Salve. Quando o script gerar o
arquivo de novo, o tique continua lá — a não ser que o conteúdo daquela parte tenha
mudado depois do tique: aí o tique sai, e a parte diz isso, pra ninguém achar que o texto
novo já foi conferido. Mudar a pasta do projeto de lugar não tira nenhum tique.

## `confere_cartoes.py` — confere cada cartão contra a prova dele

**Pra que serve.** Cada cartão diz um fato com palavras próprias e traz, atrás, a citação
da fonte, na coluna `fonte`. A prova do cartão é o trecho da fonte que diz esse fato,
copiado letra por letra. Ela fica num arquivo à parte, um por planilha, fora do GitHub,
porque é texto de terceiros. Este script confere, cartão por cartão, se o trecho está
mesmo no lugar que a citação diz — a página ou o slide da transcrição da aula, ou uma
frase da base do material de fora — e monta a conferência dos cartões, com os tiques da
IA e da pessoa.

**Como funciona, passo a passo.**

1. Copie [`modelo-dados/prova.json`](../modelo-dados/prova.json) pra pasta das provas,
   com o nome da planilha: no modelo, a prova da planilha `perguntas-nucleo.csv` fica em
   `docs/material-base/gerados-ocr/provas/perguntas-nucleo.json`. O modelo vem com a
   lista `provas` vazia, `[]`, e com o `versao_schema`, a versão do molde, que fica como
   está.
2. Pra cada cartão, a IA, ou você, acrescenta na lista `provas` uma entrada, entre
   chaves, `{ }`, separada da seguinte por uma vírgula, com três coisas:
   - a `pergunta`, igual à da planilha — é por ela que o cartão e a prova se acham;
   - os `trechos`: uma lista com os trechos da fonte que provam a resposta, cada um
     entre aspas, copiado da transcrição ou da base, letra por letra — pelo menos um pra
     cada lugar que a coluna `fonte` do cartão cita;
   - a `afirmacao`: `categorica`, se a fonte afirma, ou `possibilidade`, se ela trata
     como possível. Nesse caso, a resposta do cartão tem de dizer isso.

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
3. Na coluna `fonte` da planilha vão só as chamadas, cada uma com o lugar:
   `(Silva, 2020, p. 12)`, ou, com duas fontes, `(Silva, 2020, p. 12; Souza, 2019,
   slide 3)`. O nome e o ano de cada fonte são os que a conferência das referências
   mostra; o lugar é o título da página na transcrição (`p. 12`, `slide 3`) ou a página da
   frase na base. Fonte sem páginas, como uma página da internet, vai sem lugar.
4. Rode o script. Ele não julga se a resposta está certa: confere só o que é mecânico. O
   resto é a pessoa que confere, na conferência dos cartões.

**Como rodar.**

    python scripts/confere_cartoes.py

**O que aparece.** Uma linha `ERRO` pra cada coisa que não bate: cartão sem prova, prova
sem cartão (a pergunta mudou só de um lado), chamada que não é de nenhuma fonte, lugar
que a fonte não tem, trecho que não está no lugar citado, lugar citado sem trecho, prova
que diz que a fonte afirma quando a base marca o trecho como possibilidade. Na
comparação, a quantidade de espaços, as quebras de linha e as marcas de destaque
(itálico, negrito) não contam; as letras e a pontuação contam. No
fim, quantos cartões há, quantos têm erro e quantos estão sem o tique da pessoa. A
conferência (no modelo, `CONFERENCIA-CARTOES.md`, na pasta das transcrições) mostra cada
cartão com a pergunta, a resposta, a fonte, os trechos e onde cada um foi achado. Se o
cartão, a prova ou o texto da fonte mudarem depois do tique, o tique sai.

Usa só o Python: não precisa instalar nada.

## `montar_deck.py` — das planilhas de pergunta ao baralho do Anki

**Pra que serve.** Transforma cada planilha de perguntas (no modelo, os arquivos
`perguntas-*.csv` de `docs/material-gerado/`) num baralho pronto pra importar no Anki —
um arquivo `.apkg`, que aparece em `anki-decks/`. No Anki, os cartões ficam numa pasta
com o nome da disciplina, que vem do formato da disciplina, e dentro dela uma pasta pra
cada planilha: planilhas e disciplinas diferentes nunca se misturam. As colunas
`pergunta` e `resposta` são obrigatórias; qualquer outra vira campo do cartão, e a
`fonte`, com a citação do fato, aparece atrás do cartão, embaixo da resposta. Duas coisas
você escolhe no `projeto.json`: em `colunas_ocultas`, as colunas que ficam guardadas no
cartão sem aparecer (no modelo, `ordem`); e em `coluna_subdecks`, uma coluna que separa
os cartões de cada planilha em pastas menores, uma pra cada valor que aparece nela — ou
`null` (escrito assim, sem aspas, quer dizer "nenhuma"), pra não separar. A aparência dos cartões vem do arquivo de estilo do projeto (no
modelo, `dados/estilo-cartao.css`).

**Quando usar.** Com as planilhas prontas e conferidas, e de novo sempre que uma
planilha mudar.

**Como rodar.**

    python scripts/montar_deck.py

Também dá pra gerar só uma planilha (`python scripts/montar_deck.py [parte do nome]`) ou
só ver quais seriam usadas, sem gerar nada (`python scripts/montar_deck.py --listar`).

**O que aparece.** Cada baralho gerado, com as pastas e quantos cartões tem. Uma planilha
sem a coluna `pergunta` ou `resposta` aparece com `ERRO` e fica sem baralho. Antes de
gerar qualquer baralho, o script confere o formato da disciplina contra o molde dele, como
o `validar_dados.py` faz: se faltar alguma coisa — o nome da disciplina, por exemplo, que
é o nome da pasta de cima no Anki —, cada problema aparece numa linha `ERRO` e nenhum
baralho é gerado. Pra usar, abra o Anki e arraste o arquivo `.apkg` pra dentro dele (ou
use o menu **Arquivo → Importar**).

Precisa da biblioteca `genanki`.

## `confere_indice.py` — confere que cada documento está no índice

**Pra que serve.** O índice do projeto (no modelo, `INDICE.md`) lista os documentos na
ordem de leitura, cada um com o link e uma linha dizendo o que ele é (ver a seção 13 da
metodologia). Este script confere que cada documento do projeto está nele uma vez só. Um
documento é cada arquivo `.md` que vai com o projeto: os que o git já guarda e os novos
que a lista do que nunca vai pro GitHub (o `.gitignore`) não deixa de fora, menos o
próprio índice. Do índice contam os links pra arquivos `.md`; a parte do link depois de
`#`, que aponta uma seção, não conta, e um link dentro de um trecho de código também não.

**Quando usar.** Sempre que um documento entra no projeto, sai dele ou muda de lugar. Se
a conferência das mensagens estiver ativa (ver o [README dela](../.githooks/README.md)),
ele também roda sozinho antes de cada versão gravada pra mandar ao GitHub, e barra a
versão enquanto houver `FALTA` ou `ERRO`.

**Como rodar.**

    python scripts/confere_indice.py

**O que aparece.** Quantos documentos há, se cada um está no índice uma vez só. Senão, uma
linha `FALTA` pra cada documento que não está no índice e uma linha `ERRO` pra documento
que está mais de uma vez — também num link do rodapé — e pra link a um `.md` que não
existe, ao próprio índice ou a um arquivo que o `.gitignore` deixa de fora. Se o projeto
não usa o git, o script diz isso numa linha `ERRO` e para: sem o git, não há como saber o
que vai com o projeto.

Usa só o Python e o git.

## `glossario.py` — monta o glossário

**Pra que serve.** Um documento que define um termo marca o termo, no lugar da definição,
com `<dfn>termo</dfn>` (ver a seção 13 da metodologia). Este script recolhe essas marcas
de todos os documentos do projeto — os mesmos que o `confere_indice.py` confere —, fora
dos trechos de código, e grava o glossário (no modelo, `GLOSSARIO.md`): cada termo numa
linha, em ordem alfabética, sem contar acentos nem maiúsculas, com o link pra seção onde
ele é definido. O glossário não copia a definição: só aponta pra ela. A mesma marca, nos
mesmos lugares, dá sempre o mesmo glossário.

**Quando usar.** Sempre que um documento define um termo novo ou deixa de definir. Se a
conferência das mensagens estiver ativa (ver o [README dela](../.githooks/README.md)), ele
também roda sozinho, com `--conferir`, antes de cada versão gravada pra mandar ao GitHub, e
barra a versão enquanto o glossário gravado não for o que os documentos definem.

**Como rodar.**

    python scripts/glossario.py
    python scripts/glossario.py --conferir

O `--conferir` não grava nada: só diz se o glossário gravado está em dia.

**O que aparece.** Quantos termos foram gravados. Uma linha `ERRO`, e nada gravado, pra
termo definido em mais de um lugar (sem contar maiúsculas), com cada lugar, e pra marca
vazia. Com `--conferir`, `FALTA` quando o glossário gravado não é o que os documentos
definem. Se o projeto não usa o git, o script diz isso numa linha `ERRO` e para, como o
`confere_indice.py`.

Usa só o Python e o git.

## `comum.py`

Não se roda: é a parte que os outros scripts compartilham (achar o `projeto.json` e as
planilhas de pergunta, ler o formato da disciplina e conferi-lo contra o molde dele, ler
o registro da fonte, guardar os tiques, ler as páginas de um documento HTML e os slides
de uma apresentação, e o que os transcritores fazem do mesmo jeito).

---

*Este documento está licenciado sob [CC BY-NC-SA 4.0](../LICENSE-CONTENT.txt).*
