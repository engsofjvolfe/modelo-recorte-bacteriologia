# Testes dos scripts

Os testes dos [scripts](../README.md) do projeto, uma pasta para cada parte. Cada teste
roda os scripts que testa com dados inventados, escritos no próprio teste ou sorteados por
ele: nada do material do projeto entra no teste. A lista inteira do que cada um confere
está no começo do arquivo dele.

Os comandos são para a pasta principal do projeto. A pasta de trabalho é uma pasta que
ainda não existe, fora do projeto: o teste grava nela o que monta, como um projeto pequeno,
com os documentos e o `projeto.json` dele, que os scripts do projeto achariam se ela
estivesse dentro do projeto. O teste cria a pasta, e ela pode ser apagada no fim. O teste
que sorteia usa sempre a mesma semente, e por isso sorteia sempre igual; o que aceita
`--semente` com um número sorteia outro mundo com ele. Cada teste mostra cada conferência
que não passou e sai com código 0 só quando todas passam.

## Os estragos

Um teste que passasse sempre daria uma falsa segurança. Por isso o próprio teste é posto à
prova, como o detector de fumaça que se testa provocando o alarme, sem esperar um
incêndio. Um <dfn>estrago</dfn> é um defeito escrito de propósito numa cópia de um script:
não é um defeito que apareceu, e sim uma troca pequena que quebra uma das regras que o
teste diz conferir, como fazer o código do cartão no Anki mudar quando muda a resposta.
No teste que tem estragos, cada regra que ele confere tem pelo menos um. Se o teste falha
com a cópia estragada, o estrago foi pego: o teste perceberia aquele defeito se ele
acontecesse de verdade. Se o teste passa, ele tem um ponto cego, e quem se conserta é o
teste.

A lista dos estragos de um teste fica na pasta dele, `estragos.json`: cada um com o nome, o
arquivo da pasta `scripts/`, o texto que se troca e o texto estragado, no molde
`scripts/esquemas/estragos.schema.json`. O `estraga.py` copia a pasta `scripts/` uma vez
para cada estrago, troca o texto na cópia e roda o teste contra ela. Ele mostra uma linha
para cada estrago e, no fim, quantos foram pegos, e sai com código 0 só quando todos
foram. O teste roda inteiro uma vez para cada estrago, por isso a lista leva bem mais
tempo que o teste. Para conferir uma mudança só contra os estragos que ela toca, o
`--so <campo>=<valor>` roda só os estragos com esse valor nesse campo, como
`--so arquivo=divergencias.py`, para os de um script, ou `--so nome=` com o nome de um
estrago; pode repetir, e rodam os que batem com qualquer um.

## `cartoes/` — o baralho e a conferência dos cartões

O teste do [`montar_deck.py`](../README.md#montar_deckpy--das-planilhas-de-pergunta-ao-baralho-do-anki)
e do [`confere_cartoes.py`](../README.md#confere_cartoespy--confere-cada-cartão-contra-a-prova-dele),
com a leitura das planilhas do `comum.py`. O projeto pequeno tem um arquivo de formato só
com o documento dos cartões, de colunas sorteadas, planilhas de pergunta, imagens,
transcrições e uma base do material de fora inventadas, as provas e as chamadas. Do
baralho, o teste confere o que vai em cada pacote: os campos, o que aparece na frente e no
verso, as imagens, o baralho de cada cartão, o código e a posição dos cartões, a pasta de
cada pacote; e que cada erro de uma planilha a deixa sem pacote, e cada erro do formato,
das colunas ou do estilo deixa todas. Da conferência, que cada cartão certo passa, que
cada erro aparece no cartão ou na planilha dele, que os tiques voltam e saem, e que, com
erro no arquivo de chamadas, nada é gravado. Do cartão escrito por IA, com marcas de IA
inventadas e um texto do material com uma delas: que ele passa com a prova tirada da marca,
com o aviso de IA; que o tique dele sai quando o texto da marca muda; que ele é erro quando
não tem prova, quando a marca sai do texto e quando o projeto não tem marcas de IA; e que,
com uma marca quebrada no texto, nada é gravado.

Precisa do genanki ([O que precisa estar
instalado](../README.md#o-que-precisa-estar-instalado)): o teste roda com o Python que o
tem.

    python scripts/testes/cartoes/teste_cartoes.py scripts modelo-dados/projeto.json [pasta de trabalho nova]

Com `--semente` e um número, o teste sorteia outro projeto pequeno. Os estragos, com o
mesmo Python, porque o `estraga.py` roda o teste com o Python que roda a ele:

    python scripts/estraga.py scripts scripts/testes/cartoes/teste_cartoes.py scripts/testes/cartoes/estragos.json [pasta de trabalho nova] --antes modelo-dados/projeto.json

## `conferencia/` — a conferência das transcrições feitas pelo extrator

O teste do [`conferencia.py`](../README.md#conferenciapy--monta-a-conferência-das-transcrições),
na parte das transcrições feitas pelo `extrator.py`. O projeto pequeno tem um PDF
inventado de quatro páginas, uma lida pelo OCR e uma com uma correção da leitura, e uma
página HTML, também com uma correção; o extrator do próprio projeto escreve as
transcrições. O teste confere que a transcrição igual ao que o extrator lê não dá erro, e
que só a página do OCR e a corrigida vão a ticar, com a imagem quando a fonte é PDF; que a
página mudada na transcrição é erro, que diz a página; que o tique da pessoa volta quando a
página não mudou e sai quando mudou; que o texto de uma página feita pelo extrator não se
leva do arquivo de conferência para a transcrição; e que a lista de extração e a
configuração do extrator com um campo que o molde não conhece são erro, sem gravar nada.

Precisa do Poppler, do Tesseract com o idioma `eng` e do `pdf_inventado.py`, da pasta
`extrator/` destes testes.

    python scripts/testes/conferencia/teste_conferencia.py scripts modelo-dados/projeto.json [pasta de trabalho nova]
    python scripts/estraga.py scripts scripts/testes/conferencia/teste_conferencia.py scripts/testes/conferencia/estragos.json [pasta de trabalho nova] --antes modelo-dados/projeto.json

## `copias-estragadas/` — o próprio `estraga.py`

O teste do `estraga.py`, com uma peça inventada, com uma função que soma e um texto,
testes inventados dela e listas de estragos inventadas: o estrago que quebra o que o teste
confere é pego, o que não quebra não é, e o que não se aplica é erro; a pasta original não
muda; o `--so` roda só os estragos que batem, na ordem da lista; cada pasta de `--irma`
fica ao lado da cópia; a lista com um campo que o molde não conhece, o `--so` que não bate
com nenhum estrago e duas pastas de `--irma` com o mesmo nome são erro, sem rodar nada.

    python scripts/testes/copias-estragadas/teste_estraga.py scripts [pasta de trabalho nova]

E os estragos do próprio `estraga.py`:

    python scripts/estraga.py scripts scripts/testes/copias-estragadas/teste_estraga.py scripts/testes/copias-estragadas/estragos.json [pasta de trabalho nova]

## `documentos/` — o índice, o glossário, a lista dos trechos de IA, o dicionário das dúvidas, os links que os scripts escrevem e os dos documentos

Os testes do [`confere_indice.py`](../README.md#confere_indicepy--confere-que-cada-documento-está-no-índice),
do [`glossario.py`](../README.md#glossariopy--monta-o-glossário) e do
[`trechos_de_ia.py`](../README.md#trechos_de_iapy--monta-a-lista-dos-trechos-escritos-por-ia). Cada caso é um projeto
inventado, montado pelo `projeto_inventado.py`, que não se roda: o `projeto.json` do
modelo em branco, com o índice ou o glossário numa subpasta e com outro nome, e documentos
inventados, com git ou sem ele. Do índice, o teste confere o projeto certo, rodando de uma
subpasta; o documento que falta e o repetido; o link quebrado e o link ao próprio índice;
o documento que o `.gitignore` deixa de fora; o documento novo, fora do git, e o apagado;
o link dentro de código; e o projeto sem índice, sem git e sem `projeto.json`. Do
glossário, a ordem dos termos, sem contar acentos nem maiúsculas, e o link de cada um para
a seção dele, com a marca partida em duas linhas, com atributo, em maiúsculas e dentro de
código; o `--conferir`; o termo definido em dois lugares e a marca vazia, sem gravar nada;
e o projeto sem marca, sem git e sem `projeto.json`. Da lista dos trechos de IA, com marcas
de IA inventadas, o material e a lista em outros lugares: a ordem dos arquivos e das
linhas, duas marcas na mesma linha, o documento sem título, o caminho com espaço, a marca
dentro de código e a de fora do material; o `--conferir`; a marca que sai do texto, que
tira o item e renumera os outros; a marca que não fecha, a vazia e o texto fora do UTF-8,
sem gravar nada; e o projeto sem marca e sem marcas de IA. Os três comparam as linhas que
o script mostra, e o que ele grava, com o texto que esperam, e mostram, para cada caso que
falhou, o que saiu e o que se esperava.

O `teste_alvos_dos_links.py` lê o código dos scripts, sem rodar nada: confere que nenhum
deles escreve o caminho de um link do Markdown sem passar pelo `alvo_markdown` do
`comum.py`, que põe entre `<>` o caminho com espaço (sem isso, a imagem ou o link não
aparece). Mostra cada linha fora da regra.

Os três primeiros recebem a pasta principal do projeto, a que tem `scripts/` e
`modelo-dados/`; o do índice e o do glossário precisam também do git:

    python scripts/testes/documentos/teste_confere_indice.py . [pasta de trabalho nova]
    python scripts/testes/documentos/teste_glossario.py . [pasta de trabalho nova]
    python scripts/testes/documentos/teste_trechos_de_ia.py . [pasta de trabalho nova]
    python scripts/testes/documentos/teste_alvos_dos_links.py scripts

O `teste_confere_dicionario.py` roda o
[`confere_dicionario.py`](../README.md#confere_dicionariopy--confere-os-códigos-do-dicionário-das-dúvidas)
em projetos inventados, montados pelo `projeto_inventado.py`, com o dicionário num lugar e
com um nome inventados e os códigos montados com o separador e o número de dígitos do hash
que o `analises.py` dá. Confere que cada título na regra passa e que cada título fora dela
dá uma linha `ERRO` para cada problema, com a linha dele: sem crases, entre aspas, com
vírgula, com dois espaços ou um no fim, vazio, com texto solto, com crase dentro ou com
código vazio; o código de três partes, com zero na frente, com zero, com o slide que não é
número, com o hash curto ou em maiúsculas, sem a aula; o código que cobre outro, antes ou
depois dele, ou que se repete; e os códigos fora da ordem natural das aulas, dos slides e
das posições. Confere também que o título dentro de um bloco de código e o de outro nível
não contam; que, sem erro, ele sai com 0 e diz quantos títulos conferiu; que o
`projeto.json` sem o caminho do dicionário, o dicionário que falta e o que não está em
UTF-8 dão `ERRO`; e que ele roda de uma subpasta do projeto e dá o mesmo em duas rodadas.
Recebe a pasta `scripts/`, com a `modelo-dados/` ao lado; os estragos dele estão em
`estragos-confere-dicionario.json`, nesta pasta, e rodam com a `modelo-dados/` ao lado da
cópia:

    python scripts/testes/documentos/teste_confere_dicionario.py scripts [pasta de trabalho nova]
    python scripts/estraga.py scripts scripts/testes/documentos/teste_confere_dicionario.py scripts/testes/documentos/estragos-confere-dicionario.json [pasta de trabalho nova] --irma modelo-dados

O `teste_confere_links.py` roda o
[`confere_links.py`](../README.md#confere_linkspy--confere-os-links-internos-dos-documentos)
em repositórios inventados, com git: o link para um arquivo que falta, para um título que
não existe, para uma linha que o arquivo não tem, para um marcador (o `id` ou o `name` de
uma tag HTML) que falta ou que está em código ou em comentário, com o texto partido em duas
linhas, com espaço, dentro de código e para fora do projeto; o título repetido, com código
e com link; o documento novo, fora do git, e o que o `.gitignore` deixa de fora; e a pasta
sem git. Dos links para uma linha e dos links para um marcador, confere quais dão erro.
Recebe a pasta `scripts/`; os estragos dele estão em `estragos-confere-links.json`, nesta
pasta:

    python scripts/testes/documentos/teste_confere_links.py scripts [pasta de trabalho nova]
    python scripts/estraga.py scripts scripts/testes/documentos/teste_confere_links.py scripts/testes/documentos/estragos-confere-links.json [pasta de trabalho nova]

## `extrator/` — as transcrições de PDF, HTML, XML e JSON

O teste do [`extrator.py`](../README.md#extratorpy--transcreve-fontes-em-pdf-html-xml-e-json),
com documentos inventados: PDFs feitos pelo próprio teste, pelo `pdf_inventado.py`, que não
se roda (um com muitas páginas, uma vazia e uma que vai pelo OCR, com um texto que só a
camada de texto tem; um com negrito e itálico; um que mistura destaques num trecho), um
HTML em ISO-8859-1, um XML com etiquetas de outros nomes e dois JSON, com o texto sorteado
entre todos os caracteres que um texto pode ter, e três padrões de transcrição inventados.
O teste confere que o texto é o do documento, linha por linha; que nenhum caractere que se
escapa fica sem escape, e cada marca fecha na mesma linha; que cada caractere tem o
destaque que tem no documento; que os títulos seguem o modelo e o número impresso é o da
numeração; que as trocas e as correções dão o que a regra delas diz; que todo erro para
tudo, sem gravar nada, e diz o dado que o causou; e que duas rodadas dão a mesma saída.

Precisa do Poppler e do Tesseract com o idioma `eng`.

    python scripts/testes/extrator/teste_extrator.py scripts [pasta de trabalho nova]
    python scripts/estraga.py scripts scripts/testes/extrator/teste_extrator.py scripts/testes/extrator/estragos.json [pasta de trabalho nova]

## `formato/` — os scripts que leem o arquivo de formato

O teste dos scripts que leem o [arquivo de formato](../README.md#o-arquivo-de-formato): a
leitura dele no `comum.py` e o que se acha nele, o `validar_dados.py`, o `base_externa.py`,
o `confere_moldes.py`, com a tabela da leitura, a tabela dos destinos e o limite das aulas,
o `confere_material.py`, o `lista_de_trabalho.py` e o `divergencias.py`, com a citação das
fontes do `confere_cartoes.py`. O projeto pequeno tem um formato sorteado, com documentos
dos quatro tipos de molde, as bases de três unidades, as análises de três a cinco aulas
numa forma sorteada, as duas tabelas, transcrições inventadas, o material escrito, com as
planilhas, um arquivo de chamadas e um de divergências. O teste confere que
o formato certo passa, e cada erro dele é um erro só, que diz o lugar; que o modelo em
branco do formato falha só onde espera um valor; que cada trecho cai nos documentos, nas
entradas e nas partes que o caso dele diz, com cada aviso esperado, e só ele; as regras do
limite; que cada entrada errada é `ERRO` e nada é gravado; que o conferidor do material e a
lista de trabalho dão, no material certo e em cada estrago dele, o que o caso diz; que o
documento das divergências mostra cada uma, com as partes do material que tratam dela; e
que duas rodadas dão o mesmo.

Lê o modelo em branco do formato, o arquivo com o nome do formato na pasta do
`projeto.json` modelo.

    python scripts/testes/formato/teste_formato.py scripts modelo-dados/projeto.json [pasta de trabalho nova]

Com `--semente` e um número, outro sorteio. Os estragos:

    python scripts/estraga.py scripts scripts/testes/formato/teste_formato.py scripts/testes/formato/estragos.json [pasta de trabalho nova] --antes modelo-dados/projeto.json

## `grava-ou-confere/` — gravar ou conferir um documento gerado

O teste do `grava_ou_confere.py`, com arquivos, textos e mensagens inventados, os textos
sempre com letras de fora do ASCII: sem conferir, o texto vai para o arquivo, em UTF-8, com
as pastas que faltam, por cima do que houver, com a mensagem de gravado e o código 0;
conferindo, nada é gravado nem criado, e sai a mensagem de em dia, com 0, ou a de falta,
com 1, quando o arquivo é outro ou não existe; o arquivo vem como caminho ou como texto; a
opção `--conferir` liga a conferência, com a ajuda dada; e duas rodadas dão o mesmo.

    python scripts/testes/grava-ou-confere/teste_grava_ou_confere.py scripts [pasta de trabalho nova]
    python scripts/estraga.py scripts scripts/testes/grava-ou-confere/teste_grava_ou_confere.py scripts/testes/grava-ou-confere/estragos.json [pasta de trabalho nova]

## `itens-numerados/` — os itens numerados de uma transcrição

O teste do [`itens.py`](../README.md#itenspy--lista-e-confere-os-itens-numerados-de-uma-transcrição),
com um documento sorteado: um manual numerado com capa, sumário, corpo e anexos, num
padrão de transcrição e com formas de linha inventados, títulos com caracteres que o
padrão escapa, notas de rodapé numeradas e uma data na capa que parece número de item. O
teste confere que os itens que saem são os do documento, na ordem, com o número, o
título, a página e a linha; que, sem erro no documento, não sai problema, e cada erro posto
nele (um número que salta, um repetido, uma entrada do sumário sem item, um título
diferente) dá o problema dele, só ele, na linha dele; que os grupos, de vários tamanhos,
põem cada item num grupo só, na ordem; e que todo erro para tudo, sem gravar nada, e duas
rodadas dão a mesma saída.

    python scripts/testes/itens-numerados/teste_itens.py scripts [pasta de trabalho nova]
    python scripts/estraga.py scripts scripts/testes/itens-numerados/teste_itens.py scripts/testes/itens-numerados/estragos.json [pasta de trabalho nova]

## `marcas/` — os códigos escondidos de um texto

O teste do `marcas.py`, a parte do
[`confere_material.py`](../README.md#confere_materialpy--confere-o-texto-e-os-cartões-de-cada-unidade)
que lê os códigos escondidos de um texto e confere cada um contra o lugar em que ele
deveria estar. O teste sorteia os níveis, as unidades e as regiões de cada uma, os códigos
de cada região e um texto certo, em arquivos com comentários que não são marca, marcas no
meio da linha, duas na mesma linha, marca em três linhas e marcas em NFD. Confere que as
marcas saem na ordem, cada uma com o arquivo, a linha, o nível e o código; que o caminho de
cada marca é o do lugar dela; que o texto certo não dá aviso, e cada estrago do texto dá
exatamente os avisos do caso dele; que vários estragos juntos saem em ordem de arquivo e
linha; e que níveis e esperado que não servem são erro, que diz o que está errado.

    python scripts/testes/marcas/teste_marcas.py scripts [pasta de trabalho nova]

Com `--semente` e um número, outro sorteio. Os estragos:

    python scripts/estraga.py scripts scripts/testes/marcas/teste_marcas.py scripts/testes/marcas/estragos.json [pasta de trabalho nova]

## `moldes/` — a leitura das análises e o lugar de cada trecho

O teste das partes do
[`confere_moldes.py`](../README.md#confere_moldespy--confere-os-moldes-contra-as-análises-das-aulas)
que leem as análises das aulas e dizem onde cada trecho cai: o `analises.py`, o
`lugares.py`, o `relatorio.py`, o `tabela.py`, o `destinos.py`, o `limite.py` e o molde da
forma das análises. O `mundo_inventado.py`, que não se roda, sorteia uma forma de análise,
regras com tipos de fora, marcas, grupos e documentos, e aulas com trechos de todos os
casos; o teste sorteia também tabelas em texto, a tabela dos destinos e lugares para o
limite. Ele confere que cada trecho é lido de volta, com o texto e cada campo, e tem o
código certo; que o código, e cada começo dele, se lê de volta nas partes dele, e o que não
é código nem começo de um não se lê; que a classe, as marcas, os documentos e os grupos
desconhecidos de cada trecho são os do caso dele; as tabelas do relatório; a tabela em texto
e a dos destinos, com os erros delas; as regras do limite; e que a forma, as regras e as
análises erradas são pegas pela conferência da parte errada.

    python scripts/testes/moldes/teste_moldes.py scripts [pasta de trabalho nova]

Com `--semente` e um número, outro sorteio. Os estragos:

    python scripts/estraga.py scripts scripts/testes/moldes/teste_moldes.py scripts/testes/moldes/estragos.json [pasta de trabalho nova]

## `pptx/` — as aulas em pptx

O teste do leitor de pptx do `comum.py`, do
[`transcrever_pptx.py`](../README.md#transcrever_pptxpy--transcreve-uma-apresentação-de-slides-em-pptx)
e da conferência das aulas, com apresentações montadas pelo próprio teste: listas e
níveis, numeração, símbolos, índice e expoente, tabela, grupo, imagens, objeto, gráfico,
SmartArt, slide oculto com notas e slide vazio. Na conferência, o teste confere os links,
com uma apresentação com espaço no nome; o `--levar-correcoes`, que leva só o texto
corrigido, e as recusas dele, sem gravar nada; e a cópia em PNG de uma imagem BMP e de uma
EMF. Ele compara o que sai com o que espera e mostra, para cada caso que falhou, o que saiu
e o que se esperava.

Precisa do Tesseract com o idioma `eng`, do Poppler, do LibreOffice e do GraphicsMagick, e
do `modelo-dados/projeto.json` ao lado da pasta dos scripts.

    python scripts/testes/pptx/teste_pptx.py scripts [pasta de trabalho nova]

---

*Este documento está licenciado sob [CC BY-NC-SA 4.0](../../LICENSE-CONTENT.txt).*
