# Metodologia de Conteúdo

Guia prático de como montar e auditar o conteúdo de uma disciplina neste tipo de
projeto: dado que você tem material de aula de uma disciplina disponível, o que fazer
com ele pra chegar num material de estudo estruturado, de um jeito consistente entre
disciplinas diferentes.

Este documento é escrito sem amarrar a nenhuma disciplina específica — onde um exemplo
ajuda a entender uma instrução, ele é descrito de forma abstrata, não com conteúdo real
de nenhuma matéria.

Siga isto por padrão, mas corrija quando sua disciplina expuser um caso que não está
coberto aqui. Quando isso acontecer, atualize este documento também, não só o conteúdo
da sua disciplina.

Algumas partes do trabalho são feitas por *scripts*: pequenos programas que vêm prontos no
modelo e fazem sempre o mesmo trabalho, do mesmo jeito. Quando este guia diz pra rodar um
deles — um comando como `python scripts/conferencia.py` —, o
[README dos scripts](scripts/README.md) explica, passo a passo, como abrir o terminal (a
janela onde se digita o comando) e o que aparece na tela. Você não precisa saber
programar.

Os caminhos de pasta e de arquivo citados aqui são os do modelo. Em cada projeto, quem
diz onde fica cada coisa é o mapa do projeto, o arquivo `projeto.json`, na pasta
principal dele: é dali que os scripts tiram todo caminho.

Uma palavra que aparece muito aqui: *publicar*. O projeto de uma disciplina pode ser
publicado — no GitHub, um site que guarda projetos na internet, ou em qualquer outro
lugar. O material de terceiros (as aulas, a transcrição delas, as cópias do material de
fora e tudo o que traz texto delas) nunca é publicado; o resto pode ser.

As seções seguem a ordem do trabalho, que é uma cadeia: o formato da disciplina dá a
grade de tudo (seção 1); cada fonte vira uma transcrição conferida e uma referência
(seções 2 a 4); das transcrições e da base do material de fora nascem os documentos
(seções 5 a 8) e, dos documentos, os cartões (seções 9 e 10); e tudo passa primeiro por
uma análise mecânica, feita por script, e depois pela análise humana (seção 11). Cada
etapa nasce da anterior, nunca direto da fonte, e a pessoa é sempre o último elo da
conferência.

---

## 1. Descubra o formato da disciplina

Antes de qualquer material, decida o formato da disciplina: o curso, a disciplina e o
nível de estudo; os itens; os eixos da ficha e os subtópicos de cada um; os elos do
dicionário; e as colunas dos cartões. O [Descubra seu modelo](DESCUBRA-SEU-MODELO.md) traz
as perguntas, e as respostas vão para o arquivo de formato, `dados/formato.json`, que se
confere com `python scripts/validar_dados.py dados/formato.json`. Uma IA pode propor cada
resposta, dizendo por que ela cabe naquele curso e naquele nível; a decisão é da pessoa.

Esse arquivo é a grade de tudo o que vem depois: é por ele que se sabe o que cada item
precisa ter, o que a aula cobre e onde falta, antes de qualquer material ser escrito.

---

## 2. Trate as fontes da aula

Guarde o material de aula original da disciplina — slides, apostila, ou o que for — na
pasta do material de base, `docs/material-base/`. É a pasta protegida: tudo o que é de
terceiros fica nela, e ela nunca é publicada nem muda de nome ou de lugar. Ela carrega um
arquivo pequeno e próprio dela, `docs/material-base/README.md`, que só explica como a
pasta funciona. Quem olha o projeto de fora normalmente não vai ver o conteúdo dela nem
saber o que tem lá — ela existe só no seu computador, pra você, enquanto organiza aquela
disciplina. O `protege_fontes.py` confere que nenhuma fonte registrada ficou fora dela.

Faça uma transcrição integral e literal desse material, usando OCR se ele estiver
digitalizado como imagem ou PDF escaneado (OCR é uma tecnologia que lê o texto de uma
imagem e devolve como texto comum). Essa transcrição não é opcional, com ou sem ajuda
de IA: ela é o que permite conferir, depois, que nada do material ficou de fora do que
você escreveu — texto literal e completo é mais fácil de conferir contra o que foi
escrito do que voltar num PDF escaneado toda vez. Guarde essa transcrição também sem
publicar, no padrão de *Como transcrever*, logo abaixo.

Ao escrever o conteúdo de estudo — sozinho, ou com ajuda de um assistente de IA, o que
preferir — leia o material inteiro antes de escrever qualquer coisa, sem usar nenhuma
ferramenta que corte ou resuma automaticamente o texto antes dessa leitura completa
acontecer. Nunca invente ou deduza um fato que não esteja escrito no material — se um
dado parecer faltar ou for ambíguo, pergunte a alguém, não adivinhe.

Faça todo fato relevante do material original aparecer em algum dos três documentos da
[seção 5](#5-escreva-três-documentos-de-conteúdo). Você pode deixar de fora elementos
puramente decorativos (piadas, mascotes, créditos de imagem) que não carregam
informação nenhuma — a linha é "isto é um fato" contra "isto é só enfeite", não "isto
parece pouco importante".

Se o nome de um arquivo de origem não bater com o conteúdo real dele, corrija o nome do
arquivo (registrando essa correção em algum lugar), em vez de conviver com o nome
errado.

### Como transcrever

Transcreva página por página (ou slide por slide), marcando duas coisas em cada uma: a
posição dela no arquivo, que é por onde se acha a imagem pra conferir, e o número
impresso na própria página, que é o que a citação usa. Os dois costumam ser diferentes
(capa, ficha técnica e páginas em algarismos romanos contam no arquivo, mas não na
numeração impressa). Quando a página não tem número impresso, como costuma acontecer
com slides, a citação usa a posição dela no arquivo, como slide. Entra todo texto que
está escrito na página, inclusive o de dentro de figuras, tabelas e esquemas, e cada
item junto do rótulo que lhe dá contexto (o título da lista, a legenda, o cabeçalho da
coluna), porque um item solto pode mudar de sentido. Não entra nada que não esteja
escrito: nem descrição de imagem, nem explicação, nem correção. Onde há uma figura, a
transcrição só marca que ela existe, com `[imagem]`, seguida do texto escrito dentro
dela e de `[fim da imagem]` (figura sem texto fica só com `[imagem]`); a legenda, escrita
fora da figura, vem no lugar dela na página. A marca diz onde a figura está, nunca o que
ela mostra. Guarde a transcrição em
`docs/material-base/gerados-ocr/` e, assim que ela for criada, registre no topo dela de
qual arquivo veio, com `python scripts/registrar_fonte.py [transcrição] [arquivo
original] [chave]` — se o arquivo original estiver fora da pasta protegida, o script
oferece levá-lo pra lá antes de registrar. A chave é a mesma da referência dessa fonte (ver a
[seção 3](#3-cite-cada-fonte-conforme-a-abnt)); o script grava a chave, o caminho do
arquivo e a impressão digital dele — um código calculado a partir do conteúdo do
arquivo, que muda se o arquivo mudar —, e em seguida atualiza as referências. É esse
registro que liga a transcrição ao original, não o nome dos arquivos.

Cada página vira uma parte da transcrição, que começa com uma linha de título escrita
assim: `## [como a citação chama a página] (arquivo p. [posição no arquivo])` — por
exemplo, `## p. 12 (arquivo p. 14)` ou `## slide 3 (arquivo p. 3)`. Os dois `#` no começo
marcam a linha como título. Uma página sem texto nenhum fica com o título e a marca
`[sem texto]`.

Quando o material é um documento HTML que marca as páginas impressas — como o capítulo
de um livro digital —, a transcrição sai do próprio documento, sem leitura nenhuma:
`python scripts/transcrever_html.py [documento ou captura]` copia o texto de cada página
com o número impresso que o documento marca, e a posição no arquivo passa a ser a ordem
da página dentro do documento. Se o documento só se lê num site, guarde a captura que o
navegador salva enquanto você o lê (o [README dos scripts](scripts/README.md) explica
como): o script guarda na pasta protegida uma cópia do documento e das imagens dele, que é
o arquivo que se registra, e a captura, que tem os dados da sua sessão no site, pode ser
apagada. Nesse documento, cada figura é um arquivo próprio, e a marca dela traz a própria
imagem, no lugar dela: `![imagem]([caminho da imagem])`, seguida do texto escrito dentro
dela, lido por OCR, e de `[fim da imagem]`, que fecha a marca sempre, mesmo sem texto.

Um fato que só a imagem mostra, sem texto, não está na transcrição. Se ele precisar
entrar no material, a prova dele é a própria imagem, conferida por uma pessoa, ou uma
fonte de fora que o diga por escrito.

Antes de usar a transcrição como base, ela é conferida contra a imagem de cada página:
OCR e IA trocam letras, pulam linhas e às vezes escrevem o que não está lá. Com a
transcrição pronta, gere o arquivo de conferência (`python scripts/conferencia.py`). Ele
nasce das transcrições, não do PDF, e mostra, página por página, a imagem da página no
arquivo registrado e o que a transcrição tem pra ela — se não tem nada, aparece vazio —,
com duas caixas de tique, uma pra IA e outra pra pessoa. O script não julga o conteúdo:
quem confere é quem tica. A IA pode ticar primeiro, como uma primeira passada; a pessoa é
sempre o último elo, e nenhuma página vale como conferida sem o tique dela. Se o texto
de uma página ou o arquivo original mudar depois do tique, o tique é retirado. Até essa
conferência, a transcrição não prova nada.

Na transcrição de um documento HTML, o texto é cópia do documento, e quem o confere é o
script: a conferência compara, página por página, as letras, os números e os sinais da
transcrição com os da mesma página na fonte, na mesma ordem, e também o número impresso e
as imagens de cada página, e aponta como erro o que não bate. À mão, confere-se só o
texto de dentro de cada imagem, que veio do OCR: cada imagem aparece com esse texto e com
as duas caixas de tique.

---

## 3. Cite cada fonte, conforme a ABNT

Todo documento que escreve algo tirado de uma fonte — teoria fundamental, dicionário,
ficha, planilha de perguntas — cita essa fonte ali mesmo, junto do fato, segundo a norma
de citações (no Brasil, a ABNT NBR 10520, no sistema autor-data): a mesma entrada da
referência (o autor, a instituição ou, sem autor, o começo do título), o ano e o local
do trecho: a página impressa no documento ou, se ela não tiver número impresso, a
posição do slide no arquivo. Diga o fato com suas palavras; se precisar transcrever
literalmente, use aspas e só um trecho curto, como a norma manda. Na planilha, a
citação vai numa coluna `fonte`, que aparece no cartão, e a resposta é sempre com
palavras próprias ([seção 9](#9-cartões-de-revisão-espaçada)). A chamada de cada fonte —
o nome e o ano, já com o *et al.* e as letras de desempate quando a norma pede — sai
pronta na conferência das referências; o que cada norma pede, item por item, e o que cabe
ao script, aos dados e a quem escreve, está nas [Regras da ABNT](regras-abnt.md).

As referências completas de todas as fontes citadas — as aulas e o material de fora —
ficam num documento só, `docs/REFERENCIAS.md`, como a lista de referências do fim de um
trabalho: em ordem alfabética, segundo a norma de referências (ABNT NBR 6023), e nada
além delas. Ele não diz onde cada fonte foi usada, porque isso é o papel da citação em
cada documento, nem onde a cópia está guardada. Toda citação tem a referência ali, e
toda referência é citada em algum lugar. Por exemplo:

```
[TÍTULO da aula]. [S. l.: s. n.], [20--]. 1 arquivo PDF ([n] slides). Material de aula, não publicado.

[AUTOR OU INSTITUIÇÃO]. [Título]. [Local]: [editora], [ano]. Disponível em: [endereço]. Acesso em: [data].
```

Esse documento é conteúdo do projeto e é publicado com ele: o que nunca se publica é a
cópia do material, não a referência a ele.

Ninguém escreve esse documento à mão. Os dados de cada fonte — autoria, título, local,
editora, data, endereço, data de acesso, com uma chave curta — ficam no arquivo de
fontes, `dados/fontes.json` (copiado de `modelo-dados/fontes.json`), e `python
scripts/referencias.py` monta cada referência pela norma, em ordem alfabética, e grava o
`docs/REFERENCIAS.md`. O mês de cada data sai abreviado como manda a tabela do Anexo A da
ABNT NBR 6023, edição de 2025; o modelo guarda essa tabela em `scripts/normas/meses.json`.
Junto, o script gera a conferência das referências: cada referência e a chamada dela como
ficaram, ao lado da cópia registrada da fonte (a primeira página, se for PDF), com uma
caixa de tique pra IA e outra pra pessoa. Confira cada referência contra a folha de rosto
ou a página do documento; se a referência, a chamada ou a cópia mudarem depois do tique, o
tique é retirado.

---

## 4. Complete a aula com material de fora

Se o material de aula não trouxer o que algum eixo da ficha pede pra um item (ver
[seção 5](#5-escreva-três-documentos-de-conteúdo)), busque esse fato num material de fora
— de preferência um documento oficial ou de referência da área. O material de fora
completa a aula, não a substitui: use-o só onde a aula não chega. Vale a mesma regra da
aula: o fato tem de estar escrito nesse material, nunca deduzido.

Guarde uma cópia de cada material de fora junto do material de aula, na subpasta das
cópias do material de fora, `docs/material-base/fontes-externas/`, dentro da pasta
protegida: ele também não é de quem mantém o projeto. Se a cópia estiver fora da pasta
protegida, o `base_externa.py` oferece levá-la pra lá. Dê a cada cópia
um nome que comece pela entrada e pelo ano da referência dela, pra achar o arquivo a
partir da citação.

Do material de fora, faça também uma base literal, item por item — e ninguém copia
trecho à mão. No arquivo de dados do item (`dados/bases/[item].json`, copiado de
`modelo-dados/base.json`), declare quais páginas de quais fontes foram lidas e marque
cada subtópico da grade do formato como coberto pela aula, pelo material de fora ou como
lacuna. `python scripts/base_externa.py` recolhe todo o texto dessas páginas, sem
filtro, separado em frases, cada uma com um código; a IA classifica cada frase — usada
(com o subtópico e se a fonte afirma ou trata como possibilidade), de outro item,
repetida, fora do recorte ou não é conteúdo —, e o script grava a base do item, só com
as frases usadas, letra por letra, com a citação e a página. Ele recusa frase sem classe,
subtópico sem marca, subtópico do material de fora sem frase nenhuma e frase usada onde
a aula já cobre ou num subtópico marcado como lacuna, e não grava a base enquanto houver
erro. A base e a conferência dela — cada página com as frases e a classe de
cada uma, com tique da IA e da pessoa — nunca são publicadas; o arquivo de dados, que só
tem códigos e decisões, pode ser publicado com o projeto. É contra essa base que se confere
cada fato tirado do material de fora, e frase que a fonte trata como possibilidade entra
no material com a ressalva escrita, nunca como certeza.

---

## 5. Escreva três documentos de conteúdo

Escreva, no mínimo, três documentos pra cada disciplina, cada um com uma função própria
e exclusiva. Nos três, todo fato tirado de uma fonte leva a citação dela, como diz a
[seção 3](#3-cite-cada-fonte-conforme-a-abnt):

### A) Teoria fundamental

Escreva aqui o que vem **antes** de qualquer item específico: classificação geral,
conceitos comuns a toda a disciplina, categorias que os itens específicos vão usar sem
precisar redefinir. Organize em seções por tema, não uma seção por item. Você pode
citar um item específico como exemplo de um conceito geral, mesmo que esse item não
tenha (ainda, ou nunca venha a ter) seu próprio dicionário ou ficha — isso é esperado.
Escreva mais de um documento de teoria fundamental se a disciplina tiver mais de um
ramo claramente distinto de conteúdo introdutório.

### B) Dicionário de gatilhos

Escreva uma entrada por item específico, contando o item como uma história contínua,
dividida em partes que você vai chamar de **elos**. Em cada elo, explique o motivo que
leva ao elo seguinte — de forma que dê pra deduzir o item a partir de qualquer ponto da
história, em vez de decorar fatos soltos.

Decida quantos elos usar (a mesma quantidade pra todo item da sua disciplina) e dê um
nome a cada um. O processo central que um item passa muda completamente conforme o
assunto, então o elo do meio — o que faz aquele item "funcionar" — vai precisar de um
nome que só faz sentido pra sua disciplina; não herde o nome que outra disciplina usou.

Escreva num tom narrativo, em prosa corrida, sem tom pessoal e sem comentar sobre o
próprio texto (não escreva algo como "isto é uma lista completa"). Citar a fonte de um
fato não é comentar o texto: a citação continua valendo aqui, junto de cada fato que
veio de uma fonte. Sempre que um item usar uma categoria que você já definiu no
documento de teoria fundamental, cite essa categoria pelo nome (ver
[seção 7](#7-cite-uma-categoria-em-vez-de-redefinir)) em vez de explicá-la de novo ali.

### C) Ficha determinística

Reorganize os mesmos itens do dicionário numa tabela seca e direta. Use sempre o mesmo
conjunto de linhas — que você vai chamar de **eixos** — pra todo item da disciplina.
Isso é o que faz a ficha boa pra revisão rápida, ao contrário do dicionário, que é bom
pra entender o porquê.

Decida quantos eixos usar e o nome de cada um, do mesmo jeito que decidiu os elos do
dicionário. Dentro da sua disciplina, todo item tem a mesma quantidade de eixos — mas
esse número, e o nome de cada eixo, são uma escolha sua: outra disciplina pode escolher
um número diferente e nomes completamente diferentes.

Cubra, na ficha, o mesmo conteúdo principal do dicionário — mas não se limite a ele:
inclua aqui o detalhe que não cabe bem numa história corrida (números, listas
completas, critérios exatos). Siga a mesma regra de tom e de citação de categorias do
dicionário.

---

## 6. Mostre o mesmo conteúdo em dois níveis

Dicionário e ficha não são dois conteúdos independentes — são duas formas de contar o
mesmo conjunto de fatos principais sobre o mesmo item. No dicionário, conte só os fatos
que sustentam a história em cadeia. Na ficha, repita esses mesmos fatos, eixo por eixo,
e adicione o que a história não precisava citar pra fazer sentido.

Faça um fato principal de um item aparecer nos dois documentos, com a mesma conclusão —
só com mais ou menos detalhe. Se você perceber um fato que aparece nos dois documentos
de formas contraditórias (não apenas com detalhe diferente), corrija — isso é um erro.
O dicionário não precisar citar um detalhe que só está na ficha não é erro.

---

## 7. Cite uma categoria, em vez de redefinir

Se o seu documento de teoria fundamental define uma categoria (um grupo, um tipo de
processo, uma classificação), e um item específico se encaixa nela, cite o nome dessa
categoria no dicionário e na ficha desse item, em vez de descrever a mesma coisa de
novo sem nomeá-la.

Fazendo isso, você evita repetir a mesma explicação em todo item que usa aquela
categoria, garante que o documento de teoria fundamental realmente define tudo que os
itens vão precisar, e cria um caminho direto pra quem esqueceu o que a categoria
significa. Se você usar um conceito de teoria fundamental num item sem citar esse
conceito pelo nome em nenhum documento desse item, corrija — isso é uma lacuna.

---

## 8. Escreva um arquivo novo só quando a função for nova

Antes de criar um documento novo, pergunte a si mesmo: que função esse conteúdo cumpre,
e algum dos três tipos da [seção 5](#5-escreva-três-documentos-de-conteúdo) já cumpre
essa função?

Se o conteúdo for teoria geral — não a história de um item específico (dicionário), nem
a tabela de um item específico (ficha) —, coloque-o como uma seção dentro do documento
de teoria fundamental, mesmo que essa teoria tenha vindo de uma parte separada do
material de aula original; não crie um arquivo à parte só por isso. Só crie um arquivo
novo quando a função em si for genuinamente nova, sem nenhum dos três tipos cobrindo
ela — e nesse caso, descreva esse quarto tipo aqui também, porque ele passa a valer pra
qualquer disciplina futura que usar este documento.

---

## 9. Cartões de revisão espaçada

Um cartão de revisão espaçada é uma técnica de estudo: uma pergunta de um lado, uma
resposta do outro, revisada em intervalos crescentes de tempo, num programa como o
Anki (gratuito, disponível pra computador e celular). Isso é opcional — nem toda
disciplina precisa ter cartões, mas quem tiver, siga o resto desta seção.

As perguntas ficam guardadas numa planilha CSV: um arquivo de texto simples,
organizado em linhas e colunas como uma tabela (abre e edita no Excel, no Google
Sheets, ou como texto comum), com uma pergunta por linha. Nomeie o arquivo começando
sempre com a mesma primeira parte, em toda planilha do projeto — por exemplo,
`perguntas-` no início de `perguntas-fundamentos.csv` e de `perguntas-nucleo.csv`.
Assim, o script da [seção 10](#10-gere-o-baralho-com-o-script-do-modelo) sabe quais
arquivos são planilhas de pergunta só pelo nome, sem que ninguém precise listar cada
arquivo um por um dentro do código.

Você não precisa extrair essas perguntas à mão. Envie o dicionário e a ficha (já
escritos, seção 5) pra um assistente de IA, com uma instrução como esta:

> A partir do dicionário de gatilhos e da ficha determinística em anexo, gere uma
> planilha CSV de perguntas e respostas de revisão espaçada. Use uma coluna `pergunta`,
> uma `resposta`, escrita com palavras próprias, e uma `fonte`, com a citação que o fato
> já tem no dicionário ou na ficha (as três obrigatórias), mais as colunas [nomeie as
> que fizerem sentido pra sua disciplina — por exemplo, o que identifica o item, o tipo
> de pergunta]. Para cada item específico, gere uma quantidade pequena e fixa de perguntas (a
> mesma quantidade pra todo item da disciplina), cobrindo os fatos de maior valor de
> revisão espalhados pelos diferentes elos/eixos daquele item — não repita sempre o
> mesmo tipo de pergunta pra todos os itens se isso deixar de fora um fato importante e
> específico de um item em particular. Para a teoria fundamental, gere uma pergunta pra
> cada conceito testável, já que cada conceito aparece uma única vez. Não invente
> nenhum fato que não esteja no texto do dicionário/ficha fornecido. Na coluna `fonte`,
> ponha só as chamadas, cada uma com a página ou o slide. Gere também a prova de cada
> pergunta, no arquivo de prova: a pergunta igual à da planilha, o trecho da
> transcrição ou da base do material de fora que diz o fato, copiado letra por letra, e
> se a fonte afirma (`categorica`) ou trata como possibilidade (`possibilidade`).

A prova fica num arquivo por planilha, copiado de `modelo-dados/prova.json`. Como ela
tem texto de terceiros, fica com o material de base e nunca é publicada
(`docs/material-base/gerados-ocr/provas/`, por convenção). Quando a fonte trata o fato
como possibilidade, a resposta do cartão diz isso: nenhum cartão apresenta como certo o
que a fonte não afirma. `python scripts/confere_cartoes.py` confere cada cartão contra a
prova — se o trecho está, letra por letra, no lugar que a citação do cartão diz, e se
não falta prova pra nenhum cartão nem cartão pra nenhuma prova — e gera a conferência dos
cartões, com tique da IA e da pessoa.

Depois, confira a planilha lado a lado com o dicionário e a ficha, e cada cartão na
conferência dos cartões: a planilha cobre tudo que deveria cobrir, sem inventar nem
perder nada? A resposta de cada cartão diz o que o trecho diz, com a ressalva quando a
fonte trata como possibilidade? Essa conferência é sua, não da IA — é o que garante que
nada ficou de fora.

Uma vez com a planilha pronta e conferida, o baralho do Anki será gerado automaticamente
pelo script do modelo, acionado por você (veja seção 10). Você pode editar um cartão
direto dentro do Anki — mas se depois você mudar a planilha (ou o dicionário/ficha de
origem) e gerar o baralho de novo, o cartão é refeito a partir da planilha, e a edição
feita direto no Anki não sobrevive quando o baralho novo for importado. Ou seja: enquanto
você for refazendo o baralho a partir da planilha, é a planilha (ou o dicionário/ficha)
que precisa estar certa.

Então, se você precisa mudar um baralho, saiba qual cartão ou quais cartões, dê as
instruções pra IA que você usa ou mude você mesmo direto na planilha (no caso da IA,
confira o que ela fez). Em seguida, gere o baralho de novo com o script.

---

## 10. Gere o baralho com o script do modelo

Depois que a planilha da seção 9 existe, falta um último passo mecânico: ler cada linha
dela e montar o arquivo `.apkg` que o Anki importa. Esse passo é sempre o mesmo tipo de
trabalho, não importa a disciplina — por isso é feito por um script (um programa de
computador que faz um trabalho automático e repetitivo), em vez de à mão: rodando o
script de novo, o baralho inteiro é reconstruído em segundos toda vez que a planilha
mudar.

O modelo já traz esse script, o `scripts/montar_deck.py`: use-o sem editar (o
[README dos scripts](scripts/README.md) diz como rodar). No Anki, os cartões aparecem
numa pasta com o nome da disciplina, tirado do formato, e dentro dela uma pasta pra cada
planilha, de modo que planilhas e disciplinas diferentes nunca se misturam.

Se um dia você precisar de um script diferente, não precisa saber programar pra ter um,
nem entender tecnicamente tudo que a instrução abaixo pede — ela é pra copiar e enviar,
não pra decifrar. Envie-a pra um assistente de IA: o mesmo que te ajudou a escrever o
conteúdo, um assistente de IA integrado ao editor de código, ou um assistente de IA comum
na internet. Ela descreve o que o script do modelo faz, e o novo tem de fazer o mesmo.

> Escreva um script em Python que:
> 1. Encontre sozinho, na pasta do material gerado que o `projeto.json` do projeto
>    indica, todos os arquivos CSV cujo nome comece com o prefixo que o mesmo arquivo
>    indica (ex.: `perguntas-`) — sem que ninguém precise listar nomes de arquivo ou de
>    pasta dentro do código.
> 2. Para cada arquivo encontrado, gere um baralho do Anki (`.apkg`) separado, com um
>    cartão por linha. Toda planilha tem uma coluna `pergunta` (frente do cartão) e uma
>    `resposta` (verso). Qualquer outra coluna que existir no arquivo também deve virar
>    um campo do cartão, com esse mesmo nome — os nomes dessas colunas variam de
>    planilha pra planilha, e o script não deve esperar nenhum nome específico. As
>    exceções: a coluna `fonte`, com a citação do fato, aparece no verso, abaixo da
>    resposta; as colunas que o `projeto.json` lista em `colunas_ocultas` ficam no
>    cartão sem aparecer; e a coluna que ele indica em `coluna_subdecks` separa os
>    cartões em pastas, uma pra cada valor.
> 3. Não escreva, em nenhum lugar do código, o nome de uma disciplina, de um item
>    específico, um caminho de pasta ou uma quantidade de perguntas fixada — descubra
>    tudo a partir do `projeto.json` e do que
>    existir nos arquivos a cada execução, pra funcionar com uma planilha nova sem
>    precisar editar o código.
> 4. Ponha os cartões num baralho com o nome da disciplina, que vem do formato da
>    disciplina, e dentro dele um baralho pra cada planilha, e gere o identificador de
>    cada um (o ID que o Anki usa internamente) automaticamente, a partir de um hash do
>    nome completo dele — nunca escolhido à mão.

O que essa instrução garante, em termos simples: se você adicionar uma planilha nova,
com colunas de nomes diferentes das que usa hoje, e rodar o script de novo, ele gera os
cartões certos sem ninguém precisar abrir o código pra ajustar nada. E se duas
disciplinas diferentes gerarem baralhos, o Anki nunca vai confundir um com o outro,
mesmo que ninguém tenha escolhido os números de identificação à mão.

Teste isso: peça pra rodar o script contra uma planilha de teste com nomes de coluna
diferentes dos que sua disciplina usa (mantendo só `pergunta` e `resposta`) — se os
cartões saírem certos mesmo assim, está funcionando do jeito certo.

---

## 11. Confira: primeiro o script, depois a pessoa

Tudo o que a IA produz passa por duas análises antes de valer. A primeira é mecânica:
um script confere, sempre do mesmo jeito, o que dá pra conferir sem julgar — se o dado
tem a forma certa, se o trecho está na fonte, se nada falta dos dois lados. A segunda é
humana: a pessoa confere o conteúdo contra a fonte. O `validar_dados.py` confere se
cada arquivo de dados está bem preenchido, e cada um dos scripts abaixo grava um arquivo
de conferência, que nunca é publicado, com duas caixas de tique em cada parte: a da IA,
uma primeira passada, e a da pessoa, que é sempre o último elo.

| O que se confere | Contra o quê | Script | Arquivo de conferência (no modelo) |
|---|---|---|---|
| Cada página da transcrição (de um documento HTML: o texto de cada imagem, e o resto, só pelo script) | A imagem da página no original (de um documento HTML: a própria imagem, e o texto da fonte) | `conferencia.py` | `CONFERENCIA-COM-IMAGEM.md` |
| Cada referência e a chamada dela | A folha de rosto ou a página da fonte | `referencias.py` | `CONFERENCIA-REFERENCIAS.md` |
| Cada frase do material de fora e a classe dela | A página da fonte | `base_externa.py` | `CONFERENCIA-TRECHOS.md` |
| Cada cartão | O trecho da prova, no lugar que a citação diz | `confere_cartoes.py` | `CONFERENCIA-CARTOES.md` |

Uma linha `ERRO` ou `FALTA` de um script se resolve antes de ticar: ela diz o que falta
ou não bate nos dados. O script nunca diz se um conteúdo está certo — isso é a análise humana, parte
por parte nas conferências e, no fim, na auditoria da
[seção 16](#16-checklist-auditando-uma-disciplina-existente). Nada vale como conferido
sem o tique da pessoa, e o tique sai sozinho se a parte mudar depois dele.

---

## 12. Documente o recorte que você escolheu

Não tente cobrir um tema por completo e de forma objetiva. Escolha quais itens entram,
o quão fundo cada um vai, e o que é mais importante — geralmente em torno de uma grade
curricular específica — e diga isso claramente no guia não técnico da disciplina, sem
esconder que é um julgamento seu.

Densidades diferentes entre tipos de documento não são, por si só, inconsistência: é
esperado que os cartões de revisão de um item específico
([seção 9](#9-cartões-de-revisão-espaçada)) tenham uma quantidade pequena e fixa,
enquanto os cartões de teoria fundamental sejam completos por conceito — desde que você
siga cada regra de forma consistente dentro dela mesma.

Não pule um fato do material original sem tocar nele em nenhum documento, e não deixe
dois documentos mostrarem o mesmo fato central de formas contraditórias — nenhuma das
duas coisas é aceitável sob a desculpa do recorte.

---

## 13. Escreva os quatro documentos de apresentação

Acompanhe toda disciplina de quatro documentos na pasta principal do projeto, com papéis
fixos que não mudam de disciplina pra disciplina — só o conteúdo dentro de cada seção
muda (veja o `LEIA-ME.md` da pasta dos esqueletos deles, logo abaixo, antes de
adicionar os documentos):

| Documento | Papel fixo |
|---|---|
| `README.md` | Apresentação do projeto: o que é, aviso sobre o recorte, como o material foi feito (o que é mecânico e o que é julgamento), origem do material, licença, onde fica cada arquivo, como usar, referências. |
| `INDICE.md` | Índice do projeto: lista e linka os documentos que existem (teoria fundamental, dicionário, ficha, planilhas, fontes), sem explicação. |
| `MANUAL.md` (ou equivalente não técnico) | Guia em níveis, sem jargão, pra quem só quer estudar. Abra com o aviso do recorte e tenha um canal pra reportar erro. |
| `NOTICE.md` | Mapa de licenciamento: qual licença cobre qual categoria de arquivo, e a exceção do material de terceiros. |

O índice do projeto lista documentos, não itens de dentro deles: cada documento de
conteúdo (teoria fundamental, dicionário, ficha) mantém seu próprio índice interno, no
topo do próprio arquivo, se tiver itens ou seções suficientes pra precisar de um. Sem
essa distinção, o índice do projeto cresce junto com o conteúdo e acaba repetindo a
estrutura de cada documento dentro de si mesmo.

Existe um esqueleto pronto desses quatro arquivos em `modelo-documentos-raiz/`, que vem
com o modelo — copie-os pra pasta principal do projeto, no lugar dos documentos do modelo
que têm o mesmo nome (o `README.md` e o `NOTICE.md`), e preencha os trechos entre
colchetes, em vez de escrever cada um do zero (o `LEIA-ME.md` de dentro dessa pasta
explica como, com mais detalhe).

Ao adicionar uma disciplina nova a um projeto que já tem essa estrutura, edite as
seções desses quatro documentos com o conteúdo novo — não crie uma segunda versão
paralela deles, e não pule uma seção só porque a disciplina nova ainda não tem o
equivalente pronto (nesse caso, deixe a seção dizendo isso).

---

## 14. Licencie código, conteúdo e material de terceiros separadamente

Trate cada uma dessas três categorias com um papel fixo, independente de disciplina:

- **Código** (os scripts): escolha uma licença de código aberto que exija que qualquer
  trabalho derivado também seja aberto.
- **Conteúdo gerado** (teoria fundamental, dicionário, ficha, planilhas, a lista de
  referências, e os documentos de metodologia): escolha uma licença de conteúdo que exija
  dar crédito.
- **Material de terceiros** (o material de aula original, sua transcrição literal, as
  cópias do material de fora, a base de trechos dele e a prova dos cartões — ver as
  seções [2](#2-trate-as-fontes-da-aula), [4](#4-complete-a-aula-com-material-de-fora) e
  [9](#9-cartões-de-revisão-espaçada)), tudo na pasta protegida:
  não coloque sob nenhuma licença deste projeto, porque quem mantém o projeto não é
  quem escreveu esse material. Nunca publique, de forma permanente — não "por
  enquanto".

Em todo arquivo de código e todo documento de conteúdo, indique de forma breve qual
licença o cobre — um comentário de uma ou duas linhas no topo do código, uma linha no
fim do documento de conteúdo. Deixe as planilhas e os arquivos de dados (os `.json`, que
guardam informação pros scripts e pra IA) fora dessa regra: um comentário quebraria a
leitura de quem abre a planilha como tabela, e o arquivo `.json` nem aceita comentário.

Todo arquivo `.json`, do modelo ou do projeto, é só dado: chaves e valores. Nele não entra
texto escrito pra quem abre o arquivo — texto corrido, explicação, instrução, exemplo ou
marcador entre colchetes — nem referência a documento: uma seção desta metodologia, o nome
de um arquivo `.md`, o item de uma norma. Vale, sim, o texto que é o próprio dado, mesmo
corrido: o título de uma fonte, uma nota da referência, a pergunta e o trecho literal de
uma prova. O que a regra proíbe é o texto escrito pra explicar, instruir ou narrar. Nos
modelos de `modelo-dados/`, o lugar de uma instrução ou de um exemplo fica vazio: `""`,
`[]` ou `{}`. Nos moldes de `scripts/esquemas/`, ficam só os identificadores técnicos
(`$schema` e `$id`) e o que os scripts conferem em cada arquivo. O caminho de um arquivo
no mapa do projeto é dado, mesmo quando aponta pra um documento `.md`: é onde o script lê
ou grava aquele arquivo. A variável entre chaves de um caminho, como `{item}` e
`{planilha}`, também é dado: ninguém escreve no lugar dela, é o script que a troca pelo
valor, o id do item ou o nome da planilha. Os documentos podem citar os `.json`; nenhum
`.json` depende de um documento. O que explica um arquivo de dados fica nos documentos, e
a informação que sai de um `.json` não se perde: ou já está num documento, ou passa pra
esta metodologia.

Os modelos de `modelo-dados/` e os moldes de `scripts/esquemas/` são genéricos: servem a
qualquer disciplina e podem crescer, mas nunca se ajustam a um projeto só. Quando uma
disciplina precisa de uma informação que eles ainda não têm, o campo novo entra de um
jeito que sirva a qualquer outra, com a mudança registrada na
[seção 17](#17-isto-não-é-definitivo); nada que só sirva a uma disciplina, a um material
ou a uma fonte entra neles.

---

## 15. Checklist: adicionando uma disciplina nova

1. Prepare o projeto: faça uma cópia do modelo inteiro, com o nome do projeto. Ela é a
   pasta principal do projeto e já traz a pasta `scripts/` (sem mudar o nome de nada
   dela), os dois arquivos de licença (`LICENSE` e `LICENSE-CONTENT.txt`), a lista do que
   nunca vai pro GitHub (`.gitignore`) e o método em dados, o
   `modelo-dados/fluxo-ia.json`, que a IA recebe dali mesmo, sem cópia (ver
   [Trabalhar com uma IA](trabalhar-com-ia.md)). Dentro dela, copie de `modelo-dados/` o
   mapa do projeto (`projeto.json`) pra pasta principal e o estilo dos cartões
   (`estilo-cartao.css`) pra pasta `dados/`, junto dos outros dados do projeto. É do mapa
   do projeto que os scripts tiram todo caminho; só a pasta do material de base nunca
   muda, e por isso a lista do que nunca vai pro GitHub a deixa sempre de fora. Se travar
   em algum passo, peça ajuda à IA que você usa. Se você guarda o projeto no GitHub, ele
   ganha um repositório próprio (o lugar onde o GitHub guarda o projeto e o histórico das
   mudanças dele), sem o histórico do modelo; ative também a conferência das mensagens e
   a proteção das fontes: é opcional, mas é ela que barra uma fonte que ia pro GitHub por
   engano (ver o [README dela](.githooks/README.md)).
2. Guarde o material de aula original por convenção e decida o formato da disciplina
   (seção 1): o nome do elo central do dicionário e os nomes dos eixos da ficha — tome
   essa decisão de forma explícita, sem herdar de outra disciplina — gravados em
   `dados/formato.json`, como diz o `DESCUBRA-SEU-MODELO.md`.
3. Transcreva o material de aula por inteiro, literalmente, e confira a transcrição,
   página por página, no arquivo de conferência (seção 2); grave os dados da referência
   de cada aula em `dados/fontes.json` (seção 3) e leia tudo antes de escrever qualquer
   coisa.
4. Marque, item por item, o que a aula cobre de cada subtópico da grade; onde não
   cobrir, complete com material de fora, guardado, com base de trechos e citado (seções
   3 e 4).
5. Escreva o documento de teoria fundamental primeiro — é onde as categorias que os
   itens específicos vão citar precisam estar definidas (seção 5).
6. Escreva dicionário e ficha por item, citando os termos de teoria fundamental que se
   aplicam a cada um (seções 5 a 7).
7. Gere as planilhas a partir do dicionário/ficha, com a prova de cada cartão, rode a
   conferência dos cartões e confira se as planilhas cobrem tudo que deveriam cobrir
   (seção 9).
8. Gere o baralho com o script do modelo (seção 10).
9. Atualize as seções correspondentes nos quatro documentos de apresentação (seção 13).
10. Faça a auditoria de consistência (seção 16) antes de considerar a disciplina pronta.

## 16. Checklist: auditando uma disciplina existente

### Análise mecânica

1. Rode `python scripts/validar_dados.py` em cada arquivo de dados do projeto, e
   `conferencia.py`, `referencias.py`, `base_externa.py`, `confere_cartoes.py` e
   `protege_fontes.py`: nenhum deles pode deixar linha `ERRO` nem `FALTA` (ver a
   [seção 11](#11-confira-primeiro-o-script-depois-a-pessoa)).

### Análise humana

1. Confira se o título de cada documento cobre 100% do que está dentro dele.
2. Pegue um item específico: confira se o dicionário e a ficha mostram os mesmos fatos
   principais, sem contradição entre eles.
3. Procure um termo definido em teoria fundamental que algum item usa implicitamente
   sem citar pelo nome em nenhum documento desse item.
4. Procure um arquivo cujo nome não corresponda a nenhuma das funções da seção 5.
5. Confira se os quatro documentos de apresentação têm as mesmas seções que outras
   disciplinas já cobertas, mesmo que o conteúdo ainda seja "isto não foi feito ainda".
6. Procure um fato do material original que não apareça em nenhum documento gerado.
7. Confira a planilha de perguntas linha por linha contra o dicionário/ficha de origem
   — procure um fato inventado que não está na fonte, ou um fato da fonte que ficou de
   fora — e veja se cada cartão tem prova, sem erro e com o tique da pessoa, na
   conferência dos cartões.
8. Confira as citações: todo fato tirado de uma fonte, em qualquer documento ou cartão,
   cita essa fonte; toda citação tem a referência em `docs/REFERENCIAS.md`; toda
   referência de lá é citada em algum lugar e tem o tique da pessoa na conferência das
   referências; e a cópia de cada material de fora está guardada em
   `docs/material-base/fontes-externas/`.
9. Confira a base literal: a transcrição de cada página tem só o que está escrito nela,
   com a posição no arquivo e o número impresso, e tem o tique da pessoa no arquivo de
   conferência (num documento HTML, cada imagem tem o tique da pessoa, e nenhuma página
   tem erro do script); o arquivo de base de cada item não deixa frase sem classe nem subtópico
   sem marca, e cada página da conferência dos trechos tem o tique da pessoa.

---

## 17. Isto não é definitivo

Siga cada seção acima como o que já funcionou, não como uma imposição. Se sua
disciplina tiver uma necessidade genuína que não se encaixa bem em algum ponto deste
guia, mude o guia — e registre a mudança aqui, com o motivo, pra que a próxima pessoa
se beneficie dela em vez de reabrir a mesma discussão.

---

*Este documento está licenciado sob [CC BY-NC-SA 4.0](LICENSE-CONTENT.txt).*
