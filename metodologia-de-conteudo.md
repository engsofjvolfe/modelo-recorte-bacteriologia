# Metodologia de Conteúdo

Como o conteúdo deste projeto é feito: como as aulas de Microbiologia e o livro-texto que
as completa viram documentos de estudo e cartões do Anki, e como cada parte disso é
conferida. O porquê de cada decisão sobre a forma do material — para quem ele é, que
documentos ele tem e o molde de cada um — está na [análise da
matéria](docs/analise-da-materia.md). Os passos que o projeto percorreu, com a ajuda de
uma IA, estão em [Trabalhar com uma IA](trabalhar-com-ia.md).

O trabalho é uma cadeia. Cada fonte vira uma transcrição conferida e uma referência
(seções 1 e 2); da leitura delas e de uma pesquisa nasce o formato do material (seção 3);
o livro-texto completa cada ponto das aulas (seção 4); das transcrições nascem os
documentos de estudo (seção 5) e, dos documentos, os cartões (seção 6). Cada elo nasce do
anterior, nunca direto da fonte, e tudo passa por uma conferência que termina sempre numa
pessoa (seção 7). A seção 8 trata dos documentos e dos arquivos do próprio projeto.

Parte do trabalho é feita por [scripts](scripts/README.md), que ficam na pasta
`scripts/`; o README deles diz o que cada um faz e como rodar. Quem diz onde fica cada
coisa é o <dfn>mapa do projeto</dfn>, o arquivo `projeto.json`, na pasta principal: é dali
que os scripts tiram todo caminho.

O <dfn>material de terceiros</dfn> é o material de outras pessoas descrito no
[NOTICE](NOTICE.md): as aulas, o livro-texto, a transcrição deles, as evidências da
pesquisa, as cópias do material de fora, a base de trechos dele, a prova dos cartões e
tudo o que traz texto deles. Ele nunca é publicado; <dfn>publicar</dfn> é pôr o projeto
onde outras pessoas o vejam — no <dfn>GitHub</dfn>, um site que guarda projetos na
internet e o histórico de cada mudança deles, ou em qualquer outro lugar. O resto do
projeto pode ser publicado.

---

## 1. As fontes e a transcrição

As fontes ficam na pasta do material de base, `docs/material-base/`, a <dfn>pasta
protegida</dfn>: tudo o que é de terceiros fica nela, e ela nunca é publicada nem muda de
nome ou de lugar. O [README dela](docs/material-base/README.md) diz o que ela guarda, e o
`protege_fontes.py` confere que nenhuma fonte registrada ficou fora dela.

As aulas são apresentações de slides em pptx. O livro-texto é lido na versão digital, num
site: um documento HTML que marca as páginas impressas.

### A transcrição

Cada fonte tem uma transcrição integral e literal, feita por script a partir do próprio
arquivo, sem leitura por IA: o `transcrever_pptx.py` copia o texto de cada slide, e o
`transcrever_html.py`, o de cada página do livro, com o número impresso que o documento
marca. O livro chega ao script pela captura que o navegador salva durante a leitura no
site; o script guarda na pasta protegida uma cópia do documento e das imagens dele, que é
o arquivo da fonte, e a captura, que tem os dados da sessão no site, não fica no projeto.
A transcrição é a base contra a qual se confere tudo o que se escreve: texto literal e
completo se confere com mais facilidade que o arquivo original.

Cada página, ou cada slide, é uma parte da transcrição, que começa por um título com duas
marcas: como a citação chama a página e a posição dela no arquivo — `## p. 12 (arquivo p.
14)` no livro, `## slide 3 (arquivo p. 3)` nas aulas. A posição é por onde se acha a
imagem para conferir; o número impresso é o que a citação usa, e, num slide, que não tem
número impresso, a citação usa a posição. Entra todo texto escrito na página, cada item
junto do rótulo que lhe dá contexto (o título da lista, a legenda, o cabeçalho da coluna),
porque um item solto pode mudar de sentido; e não entra nada que não esteja escrito: nem
descrição de imagem, nem explicação, nem correção. Uma página sem texto fica com o título
e a marca `[sem texto]`.

Assim que a transcrição existe, o `registrar_fonte.py` grava no topo dela de qual arquivo
ela veio: a chave da referência da fonte ([seção 2](#2-as-citações-e-as-referências)), o
caminho do arquivo e a <dfn>impressão digital</dfn> dele — um código calculado a partir do
conteúdo do arquivo, que muda se o arquivo mudar. É esse registro que liga a transcrição
ao original, não o nome dos arquivos.

### O texto das figuras

Onde há uma figura, a transcrição traz a própria imagem, no lugar dela, seguida do texto
escrito dentro dela e da marca `[fim da imagem]`. A marca diz onde a figura está, nunca o
que ela mostra; a legenda, escrita fora da figura, vem no lugar dela na página. O texto de
dentro da figura é lido por <dfn>OCR</dfn>, uma tecnologia que lê o texto de uma imagem e
o devolve como texto comum, e é conferido por uma pessoa, olhando a imagem. Nas figuras
dos capítulos 12 a 17 do livro, a IA confere esse texto antes da pessoa, figura por
figura, do jeito que o [Texto das figuras](docs/texto-das-figuras.md) descreve; nas outras
figuras, só a pessoa o corrige.

Três tipos de figura ficam com o texto como o OCR o leu, e esse texto nunca é fonte de
conteúdo:

- os desenhos com muitos elementos, como os de um mecanismo, em que os rótulos saem fora
  de ordem;
- as tabelas de dados e os gráficos;
- as imagens cujo texto não entra no estudo, como o rótulo de um frasco de meio de
  cultura.

Num ponto de aula que vem de uma figura assim, o conteúdo sai da legenda, se houver, e do
livro-texto ou de outra fonte, nunca do texto da imagem na transcrição. Essas figuras
também têm o tique da pessoa, porque ela as viu e decidiu: o tique não as distingue, e o
tipo da figura se reconhece olhando a imagem, na hora de escrever.

Um fato que só o desenho mostra, sem texto, não está na transcrição. Quando ele entra no
material, a prova dele é a própria imagem, conferida por uma pessoa, ou uma fonte que o
diga por escrito.

### A conferência da transcrição

Até ser conferida, a transcrição não prova nada. Um <dfn>arquivo de conferência</dfn>
mostra cada parte a conferir ao lado daquilo contra o que ela se confere, com duas caixas
de tique, uma para a IA e outra para a pessoa. Como o texto das aulas e do livro é cópia
do arquivo, quem o confere é o script: o `conferencia.py` compara cada página da
transcrição com a mesma página na fonte e aponta o que não bate. À mão, confere-se só o
texto de dentro de cada figura, que veio do OCR: no arquivo de conferência, cada imagem
aparece ao lado desse texto, e é ali, olhando a imagem, que o texto se corrige. Nas aulas,
cada slide aparece também inteiro, como imagem, para se ver o que só o desenho mostra,
como as setas de um esquema. O que o script compara, como a correção chega à transcrição
e quando um tique sai estão no [README dos
scripts](scripts/README.md#conferenciapy--monta-a-conferência-das-transcrições).

---

## 2. As citações e as referências

Todo documento que escreve algo tirado de uma fonte — a análise da matéria, os documentos
de estudo, as planilhas de perguntas — cita essa fonte ali mesmo, junto do fato, no
sistema autor-data da norma de citações da ABNT (NBR 10520): a mesma entrada da referência
(o autor, a instituição ou, sem autor, o começo do título), o ano e o lugar do trecho — a
página impressa ou, num slide, a posição dele no arquivo. O fato é dito com palavras
próprias; o que se copia da fonte vai entre aspas, num trecho curto. Na planilha, a
citação vai numa coluna `fonte`, que aparece no cartão. A <dfn>chamada</dfn> de cada fonte
— o nome e o ano, já com o *et al.* e as letras de desempate quando a norma pede — sai
pronta na conferência das referências. O que cada norma pede, item por item, e o que cabe
ao script, aos dados e a quem escreve está nas [Regras da ABNT](regras-abnt.md).

As referências completas de todas as fontes citadas — as aulas, o livro-texto, as fontes
da pesquisa e o material de fora — ficam num documento só, `docs/REFERENCIAS.md`, como a
lista do fim de um trabalho: em ordem alfabética, segundo a norma de referências (NBR
6023), e nada além delas. Ele não diz onde cada fonte foi usada, porque esse é o papel da
citação, nem onde a cópia está guardada. Toda citação tem a referência ali, e toda
referência é citada em algum lugar. Esse documento é conteúdo do projeto e pode ser
publicado: o que nunca se publica é a cópia da fonte, não a referência a ela.

Ninguém escreve esse documento à mão. Os dados de cada fonte ficam no arquivo de fontes,
`dados/fontes.json` (o que vai em cada campo está nas [Regras da
ABNT](regras-abnt.md#o-arquivo-de-fontes)), e o `referencias.py` monta cada referência pela
norma e grava a lista. Junto, ele grava a conferência das referências: cada referência e a
chamada dela ao lado da cópia registrada da fonte, conferidas contra a folha de rosto ou a
página do documento.

---

## 3. O formato do material

O <dfn>formato da disciplina</dfn> é o conjunto das decisões sobre a forma do material:
para quem ele é e em que nível; que tipos de conhecimento as aulas trazem e que forma de
estudo serve a cada um; os caminhos por que a matéria se estuda; e os documentos, com o
molde de cada um. O formato nasce da própria matéria, não de um molde pronto, e tem duas
bases que não se substituem: a análise das aulas, que mostra o que elas trazem e garante
que nada delas fica de fora, e a pesquisa, que mostra o que a matéria precisa cobrir nos
cursos a que o material serve e com que profundidade. Uma divisão feita só com a lista de
tipos de conhecimento seria um inventário do material, não o formato.

### A pesquisa

A pesquisa tem três bases, em fontes acadêmicas robustas e confiáveis — artigos revisados
por pares, diretrizes de sociedades científicas e de órgãos oficiais, livros de referência
da área —, e vai só até onde precisa para mostrar como a matéria é pedida:

- como a matéria é conhecida, ensinada e cobrada nos cursos a que o material serve, no
  nível deles: as diretrizes curriculares, os documentos das associações de ensino e dos
  conselhos da área, as provas oficiais que avaliam os cursos e o que elas cobram. É
  daqui que sai o nível de cobrança: ele é resultado de pesquisa, não uma escolha;
- o que a ciência da aprendizagem mostra sobre a forma de estudo que serve a cada tipo de
  conhecimento;
- o que o próprio livro-texto e os autores dele dizem da abordagem: a quem ele se dirige,
  o que trata como essencial, até onde vai.

A pesquisa é sobre a forma, não sobre o conteúdo, que vem das aulas e do livro. Cada curso
recebe as mesmas perguntas. Cada busca fica registrada nas evidências, com onde foi feita,
os termos e o que trouxe; o texto de cada fonte é tirado por programa, direto do arquivo
oficial, sem IA lendo ou resumindo no meio, e é lido inteiro, sem corte; e cada ponto tem
o trecho literal que o diz, sem nada deduzido. Fonte da qual não se tira o texto assim,
como uma imagem ou um arquivo escaneado, não é lida. Cada fonte é citada como diz a
[seção 2](#2-as-citações-e-as-referências). O plano de ensino de uma oferta da disciplina
mostra o que aquela oferta cobre, não como a matéria é estudada e cobrada nos cursos, e os
exercícios do livro não são base do formato.

### A análise de cada parte do material

Cada aula é lida inteira, na transcrição conferida, e analisada por si, sempre com as
mesmas perguntas:

1. Que tipos de conhecimento esta parte traz, e em que trecho está cada um?
2. Quanto de cada tipo ela traz?
3. Que forma de estudo serve a cada tipo, segundo a pesquisa?
4. O que liga esta parte às outras: um conceito, um exemplo ou um processo que volta com
   outro papel?
5. Por que caminhos esta parte se estuda: de cada item para os efeitos dele, dos efeitos
   para os itens que podem causá-los, ou outro que a própria fonte use?

Todo trecho da aula — o texto de um slide, uma tabela, uma figura, uma lista — entra em
algum tipo: é isso que mostra que nada ficou de fora. Só o que não traz fato nenhum vai
para "Não é conteúdo de estudo": a linha é fato contra enfeite, não importante contra
pouco importante. Aulas diferentes pesam muito diferente: uma pode ser quase toda de um
tipo que outra nem tem. Os tipos são estes; um trecho que não cabe em nenhum ganha um tipo
novo, com nome e definição, acrescentado aqui.

| Tipo de conhecimento | O que é |
| --- | --- |
| <dfn>Conceito e vocabulário</dfn> | um termo, o que ele quer dizer e como se usa |
| <dfn>Classificação</dfn> | grupos, categorias ou hierarquias, e o critério que separa cada um |
| <dfn>Contraste</dfn> | duas ou mais coisas que diferem nos mesmos pontos |
| <dfn>Parte e função</dfn> | um componente, o que ele faz e o que isso significa pro todo |
| <dfn>Processo em ordem</dfn> | etapas em sequência, e o que acontece quando uma falha ou é bloqueada |
| <dfn>Causa e efeito</dfn> | um fato explicado por outro: o porquê |
| <dfn>Item com os mesmos tipos de fato</dfn> | coisas da mesma espécie que se aprendem uma a uma, cada uma com os mesmos tipos de fato: os itens e os eixos da ficha (seção 5C) |
| <dfn>História em cadeia</dfn> | fatos ligados em sequência, cada um levando ao seguinte: os elos do dicionário (seção 5B) |
| <dfn>Exemplo recorrente</dfn> | um caso, um agente ou um exemplo que volta em vários trechos, mostrando a cada vez uma coisa |
| <dfn>Exceção</dfn> | o caso que foge de uma regra, e por quê |
| <dfn>Número com sentido</dfn> | uma quantidade, um limite, um tempo ou uma dose, com a razão dele |
| <dfn>Relação nos dois sentidos</dfn> | uma associação que se pede de um lado pro outro e de volta, como da causa aos efeitos e do efeito às causas |
| <dfn>Figura e esquema</dfn> | o que está onde num desenho e como as partes dele se ligam |
| <dfn>Aplicação na prática</dfn> | uma situação da área que pede uma decisão tirada do conteúdo |
| <dfn>Analogia e história</dfn> | a comparação ou o episódio que a própria fonte usa pra fixar um ponto |
| <dfn>Mnemônico da fonte</dfn> | o recurso de memorização que a própria fonte dá pra guardar um fato — uma frase, uma sigla, um jogo de letras —, sem ser comparação nem episódio |
| <dfn>Marco histórico</dfn> | um fato situado no tempo da história da matéria: quando ou por quem algo foi descoberto ou introduzido, o primeiro de uma classe, como o uso de algo mudou com o tempo, sem que um fato leve ao seguinte |
| <dfn>Não é conteúdo de estudo</dfn> | o que não traz fato nenhum: bibliografia, créditos, enfeite |

Da figura, entram na análise a legenda, o texto escrito em volta dela e o texto de dentro
dela, quando trazem fato; a imagem em si não é lida nem descrita. O fato de dentro da
figura entra com as palavras lidas e marcado como vindo da figura; texto ilegível não
entra e, quando parece esconder um fato, fica anotado como dúvida.

A divisão da matéria sai depois de todas as aulas lidas: o que se repete entre elas forma
um <dfn>grupo</dfn>, e cada grupo ganha uma abordagem — não uma por slide ou por aula.
Quando a matéria se estuda por mais de um caminho (pergunta 5), cada caminho é parte do
formato, com a forma de estudo dele: a relação nos dois sentidos é um fato que se pede de
um lado e do outro; o <dfn>caminho</dfn> é um jeito de organizar a matéria inteira. A
própria fonte pode dizer quais caminhos usa, ao explicar a abordagem dela.

### A análise da matéria

A pesquisa e a análise ficam na <dfn>análise da matéria</dfn>
(`docs/analise-da-materia.md`), escrita antes de qualquer material de estudo: o que se
sabe das três bases, com a chamada de cada fonte ([parte
1](docs/analise-da-materia.md#1-a-pesquisa)); cada aula, slide por slide, com os tipos de
conhecimento dela ([parte 2](docs/analise-da-materia.md#2-as-aulas-slide-por-slide)); o
que liga as aulas ([parte 3](docs/analise-da-materia.md#3-o-que-liga-as-aulas)); os
grupos ([parte 4](docs/analise-da-materia.md#4-os-grupos)) e os caminhos ([parte
5](docs/analise-da-materia.md#5-os-caminhos)); e a forma de estudo de cada tipo e de cada
caminho, os documentos e o molde de cada um, com o porquê ([parte
6](docs/analise-da-materia.md#6-a-forma-de-estudo)). O trecho literal que sustenta cada
ponto da pesquisa fica nas <dfn>evidências da pesquisa</dfn>
(`docs/material-base/gerados-ocr/pesquisa/`), dentro da pasta protegida, porque é texto de
terceiros: é contra ele que se confere a análise.

### Onde o formato fica gravado

O que a análise decide sobre a forma do material está na parte 6 dela. As decisões que os
scripts usam ficam também no <dfn>arquivo de formato</dfn>, `dados/formato.json`, como
dados: o curso, a disciplina e o nível; os itens, os eixos da ficha e os
<dfn>subtópicos</dfn> de cada eixo — as partes menores dele que todo item também tem —;
os elos do dicionário; e as colunas dos cartões. O que vai em cada campo está no [README
dos scripts](scripts/README.md#o-arquivo-de-formato). É por esse arquivo que os scripts
sabem o que cada item precisa ter, o que a aula cobre e onde falta.

---

## 4. O que entra no material

O recorte deste projeto é o que as aulas trazem, completado pelo livro-texto. As aulas
trazem os pontos da matéria, não o conteúdo de cada um: entra todo trecho delas e, de cada
ponto, tudo o que o livro diz sobre ele, lido no capítulo inteiro, nunca por busca de
palavras. O que o livro diz sobre um assunto que nenhum slide traz fica fora, menos os
fatores de risco de cada bactéria ([análise da matéria, O que o estudante precisa saber
fazer](docs/analise-da-materia.md#o-que-o-estudante-precisa-saber-fazer)). Os trechos de
vírus ficam fora do foco do material, e os de fungo só entram como comparação com uma
bactéria ([análise da matéria, parte
2](docs/analise-da-materia.md#2-as-aulas-slide-por-slide)). O quão fundo cada ponto vai é
o que o livro diz sobre ele, e a forma de estudo vem da análise da matéria. O aviso sobre
o recorte, para quem usa o material, está no
[README](README.md#aviso-importante--leia-antes-de-usar).

Todo fato das aulas aparece em algum documento de estudo; só fica de fora o que é puro
enfeite, como piadas, mascotes e créditos de imagem. Nenhum fato fica sem documento, e
dois documentos nunca mostram o mesmo fato de formas contraditórias — nenhuma das duas
coisas se justifica pelo recorte. Partes diferentes têm densidades diferentes: o número de
cartões de cada item, conceito ou caso segue os fatos que ele tem, com a mesma regra para
todos.

Os nomes e os termos seguem a grafia do livro-texto. Quando uma aula e o livro discordam,
vale o livro, e o documento anota a diferença.

### O material de fora

Onde nem as aulas nem o livro-texto chegam, entra material de fora — de preferência um
documento oficial ou de referência da área. Ele completa, nunca substitui, e vale a mesma
regra: o fato tem de estar escrito nele, nunca deduzido. A cópia de cada material de fora
fica na pasta protegida, em `docs/material-base/fontes-externas/`, com um nome que começa
pela entrada e pelo ano da referência dele, para se achar o arquivo a partir da citação.

Do material de fora sai uma base literal, a <dfn>base de trechos</dfn>, item por item, e
ninguém copia trecho à mão. O arquivo de dados do item (`dados/bases/[item].json`) diz
quais páginas de quais fontes foram lidas e marca cada subtópico do formato como coberto
pela aula, pelo material de fora ou como lacuna; o `base_externa.py` recolhe todo o texto
dessas páginas, em frases; a IA classifica cada frase — usada (com o subtópico e se a
fonte afirma o fato ou o trata como possibilidade), de outro item, repetida, fora do
recorte ou não é conteúdo —; e o script grava a base do item, só com as frases usadas,
letra por letra, com a citação e a página. A base e a conferência dela nunca são
publicadas; o arquivo de dados, que só tem códigos e decisões, pode ser. É contra essa
base que se confere cada fato tirado do material de fora, e a frase que a fonte trata como
possibilidade entra no material com a ressalva escrita, nunca como certeza. O que o script
confere antes de gravar a base está no [README dos
scripts](scripts/README.md#base_externapy--monta-a-base-do-material-de-fora).

---

## 5. Os documentos de estudo

Os documentos de estudo seguem a análise da matéria: cada tipo de conhecimento ganha a
forma de estudo que ela escolheu. São a teoria fundamental, por tema; a ficha e o
dicionário de cada bactéria; a ficha de cada família de itens; os quadros e casos; e as
perguntas de prova, uma por aula ([análise da matéria, Os
documentos](docs/analise-da-materia.md#os-documentos)). Cada documento segue o molde dele
([Os moldes](docs/analise-da-materia.md#os-moldes)).

Quem escreve lê inteiras as transcrições e as bases conferidas antes de escrever, sem
ferramenta que corte ou resuma o texto, e nunca inventa nem deduz um fato que não esteja
escrito na fonte: um dado que parece faltar ou é ambíguo vira pergunta, não palpite.

O texto ensina, como quem ensina a matéria a alguém que nunca a viu: cada fato se apoia no
que o leitor já sabe ou no que o documento ensinou antes, o nome técnico chega depois do
que ele nomeia, e o básico vem antes do que depende dele. Ensinar não é mostrar: nenhum
fato fica só listado ou apontado numa figura, numa página ou numa fonte — o que a figura
mostra é escrito e explicado no documento. Tudo é dito com palavras próprias, claro e sem
jargão solto, nunca num texto que se lê como o livro de onde o fato veio. Um termo técnico
vem explicado onde aparece pela primeira vez, ou citado pela categoria que o define
([abaixo](#a-categoria-citada-pelo-nome)), e onde é explicado leva a marca de definição
([seção 8](#8-os-documentos-e-os-arquivos-do-projeto)). O texto é o mais enxuto que dá sem
perder o tom, a explicação nem o conteúdo, e todo fato tirado de uma fonte leva a citação
dela ([seção 2](#2-as-citações-e-as-referências)).

### A) Teoria fundamental

A teoria fundamental traz o que vem antes de qualquer item: a classificação geral, os
conceitos comuns à matéria e as categorias que os itens usam sem precisar redefinir. Ela
se divide em seções por tema, não por item, e pode citar um item como exemplo de um
conceito geral. A teoria geral que vem de uma aula à parte entra como seção dela, não como
documento próprio.

### B) Dicionário de gatilhos

O dicionário conta cada bactéria como uma história contínua, dividida em partes chamadas
<dfn>elos</dfn>. Cada elo explica o motivo que leva ao seguinte, de modo que se possa
deduzir a bactéria a partir de qualquer ponto da história, em vez de decorar fatos soltos.
Toda bactéria tem os mesmos elos, com os mesmos nomes ([Os
moldes](docs/analise-da-materia.md#os-moldes)). O texto é narrativo, em prosa corrida, sem
tom pessoal e sem comentar o próprio texto, como "isto é uma lista completa"; a citação de
cada fato não é comentário e fica junto dele.

### C) Ficha determinística

A ficha conta cada item numa tabela direta, sempre com o mesmo conjunto de linhas, os
<dfn>eixos</dfn>, para todo item da mesma espécie: é isso que a faz boa para revisão
rápida, ao contrário do dicionário, que é bom para entender o porquê. Há a ficha de cada
bactéria e a de cada família de itens, cada família com os seus eixos ([Os
moldes](docs/analise-da-materia.md#os-moldes)). Quando o item tem dicionário, a ficha traz
os mesmos fatos dele, eixo por eixo, e acrescenta o detalhe que não cabe numa história
corrida: números, listas completas, critérios exatos. O tom é o do dicionário.

### Os mesmos fatos em dois níveis

Dicionário e ficha contam o mesmo conjunto de fatos principais do mesmo item: o
dicionário, só os que sustentam a história; a ficha, esses mesmos e o que a história não
precisava. Um fato principal aparece nos dois com a mesma conclusão, só com mais ou menos
detalhe. Fato contado de formas contraditórias é erro; detalhe que só está na ficha não é.

### A categoria citada pelo nome

Quando a teoria fundamental define uma categoria — um grupo, um tipo de processo, uma
classificação — e um item se encaixa nela, o dicionário e a ficha do item citam a
categoria pelo nome, em vez de descrevê-la de novo. Assim a explicação não se repete em
cada item, a teoria fundamental define tudo o que os itens usam, e quem esqueceu o que a
categoria significa tem um caminho direto até ela. Um conceito da teoria usado num item
sem ser citado pelo nome em nenhum documento dele é uma lacuna.

---

## 6. Os cartões e o baralho

Um <dfn>cartão de revisão espaçada</dfn> é uma técnica de estudo: uma pergunta de um lado,
a resposta do outro, revisada em intervalos crescentes de tempo, num programa como o
[Anki](MANUAL.md#nível-1--só-quero-estudar-agora). Os campos de cada cartão e a ordem em
que os cartões novos entram no baralho estão em [Os
moldes](docs/analise-da-materia.md#os-moldes), no parágrafo dos cartões.

Os cartões saem dos documentos de estudo, nunca direto da fonte, e ficam em planilhas
CSV, uma pergunta por linha, cada planilha com um nome que começa pelo prefixo que o mapa
do projeto dá. Cada cartão pergunta um fato só, com uma resposta curta, escrita com
palavras próprias, clara e sem jargão solto. Todo fato dos documentos ganha pelo menos um
cartão, porque os documentos só têm o que as aulas trazem e o que o livro-texto e o
material de fora dizem dos pontos delas, e tudo isso pode ser cobrado. Um fato pode dar
mais de um cartão: uma associação pedida nos dois sentidos ganha um cartão em cada
sentido, e uma lista vira cartões menores — um por elemento, ou um por posição quando a
ordem importa —, em vez de um cartão que pede a lista inteira. A coluna `fonte` traz só as
chamadas, cada uma com a página ou o slide, e nenhum cartão traz fato que não esteja nos
documentos.

A <dfn>prova</dfn> de um cartão é o trecho da fonte que diz o fato dele, copiado letra
por letra da transcrição ou da base do material de fora, junto da pergunta, igual à da
planilha, e da marca de se a fonte afirma o fato ou o trata como possibilidade. As provas
de cada planilha ficam num arquivo, em `docs/material-base/gerados-ocr/provas/`, e, como
têm texto de terceiros, nunca são publicadas. Quando a fonte trata o fato como
possibilidade, a resposta do cartão diz isso: nenhum cartão apresenta como certo o que a
fonte não afirma. O `confere_cartoes.py` confere cada cartão contra a prova dele e grava a
conferência dos cartões.

O baralho do Anki sai das planilhas pelo `montar_deck.py`, usado sem editar: sempre que
uma planilha muda, o baralho inteiro se refaz em segundos. É a planilha que precisa estar
certa, porque o que se muda direto no Anki se perde quando o baralho é refeito ([MANUAL,
Atualizando o
baralho](MANUAL.md#atualizando-o-baralho-depois-de-editar-as-planilhas)). Como as colunas
da planilha viram campos do cartão está no [README dos
scripts](scripts/README.md#montar_deckpy--das-planilhas-de-pergunta-ao-baralho-do-anki).

---

## 7. A conferência

Tudo o que a IA produz passa por duas análises antes de valer. A primeira é a
<dfn>análise mecânica</dfn>: um script confere, sempre do mesmo jeito, o que dá para
conferir sem julgar — se o dado tem a forma certa, se o trecho está na fonte, se nada
falta dos dois lados. A segunda é a <dfn>análise humana</dfn>: a pessoa confere o conteúdo
contra a fonte. A IA propõe, dizendo por quê, escreve e confere primeiro; a pessoa decide e
confere por último. São sempre da pessoa o formato, o recorte, a escolha de cada material
de fora, o tique final de cada conferência e a decisão de publicar; e, se a IA disser algo
que não está na fonte, vale a fonte.

O `validar_dados.py` confere se cada arquivo de dados segue o molde dele, e cada um dos
scripts abaixo grava um [arquivo de conferência](#a-conferência-da-transcrição), que nunca
é publicado, com o tique da IA e o da pessoa em cada parte:

| O que se confere | Contra o quê | Script | Arquivo de conferência |
| --- | --- | --- | --- |
| Cada página da transcrição: o texto, pelo script, e o de dentro de cada figura, pela pessoa | O texto e as imagens da fonte | `conferencia.py` | `CONFERENCIA-COM-IMAGEM.md` |
| Cada referência e a chamada dela | A folha de rosto ou a página da fonte | `referencias.py` | `CONFERENCIA-REFERENCIAS.md` |
| Cada frase do material de fora e a classe dela | A página da fonte | `base_externa.py` | `CONFERENCIA-TRECHOS.md` |
| Cada cartão | O trecho da prova, no lugar que a citação diz | `confere_cartoes.py` | `CONFERENCIA-CARTOES.md` |

Uma linha `ERRO` ou `FALTA` de um script se resolve antes de ticar: ela diz o que falta ou
não bate nos dados. O script nunca diz se um conteúdo está certo; isso é a análise humana.
Nada vale como conferido sem o tique da pessoa, e os casos em que o tique sai sozinho,
porque a parte mudou depois dele, estão em [Como ticar uma
conferência](scripts/README.md#como-ticar-uma-conferência).

### Antes de o material valer

Antes de o material valer, nenhum script deixa linha `ERRO` nem `FALTA`: o
`validar_dados.py`, em cada arquivo de dados, e o `conferencia.py`, o `referencias.py`, o
`base_externa.py`, o `confere_cartoes.py`, o `glossario.py --conferir`, o
`confere_indice.py` e o `protege_fontes.py`. E a pessoa confere:

1. que o título de cada documento cobre tudo o que está dentro dele;
2. que, em cada item, o dicionário e a ficha mostram os mesmos fatos principais, sem
   contradição entre eles;
3. que nenhum termo definido na teoria fundamental é usado num item sem ser citado pelo
   nome em algum documento desse item;
4. que cada documento de estudo é de um dos tipos da [seção 5](#5-os-documentos-de-estudo);
5. que os documentos do projeto dizem o mesmo que os documentos de estudo;
6. que todo fato das aulas aparece em algum documento de estudo;
7. cada planilha, linha por linha, contra o documento de origem — nenhum fato inventado,
   nenhum fato que devia ter cartão e ficou sem —, e que cada cartão tem prova, sem erro e
   com o tique da pessoa na conferência dos cartões;
8. as citações: todo fato tirado de uma fonte, em qualquer documento ou cartão, cita essa
   fonte; toda citação tem a referência em `docs/REFERENCIAS.md`; toda referência de lá é
   citada em algum lugar e tem o tique da pessoa na conferência das referências; e a cópia
   de cada material de fora está em `docs/material-base/fontes-externas/`;
9. a base literal: cada figura da transcrição tem o tique da pessoa, e nenhuma página tem
   erro do script; o arquivo de base de cada item não deixa frase sem classe nem subtópico
   sem marca, e cada página da conferência dos trechos tem o tique da pessoa;
10. a análise da matéria: cada aula está nela, trecho por trecho; cada busca da pesquisa
    está registrada, e cada ponto dela tem a chamada da fonte e o trecho literal que o
    sustenta, nas evidências da pesquisa; e cada forma de estudo escolhida diz por quê.

---

## 8. Os documentos e os arquivos do projeto

Um <dfn>documento do projeto</dfn> é cada arquivo `.md` que vai com ele: tudo, menos o que
a lista do que nunca vai pro GitHub deixa de fora. Todo documento do projeto está no
[índice](INDICE.md), uma vez só, na ordem de leitura, e o `confere_indice.py` confere
isso. O índice lista documentos, não o que há dentro deles: cada documento de estudo tem o
próprio índice no topo, quando tem itens ou seções que peçam um.

Os documentos do projeto dizem o que o projeto é e como cada coisa se faz nele, no
presente, sem frase de estado como "ainda não foi feito", e não repetem outro documento:
apontam para ele. Os passos que o projeto percorreu ficam em [Trabalhar com uma
IA](trabalhar-com-ia.md).

Todo documento do projeto que define um termo marca o termo no lugar da definição com
`<dfn>termo</dfn>`, a <dfn>marca de definição</dfn> do HTML, que quer dizer "aqui este
termo é definido". Cada termo é definido num lugar só. O glossário (`GLOSSARIO.md`) é
feito pelo `glossario.py`, que recolhe as marcas e grava cada termo, em ordem alfabética,
com o link para o lugar onde ele é definido; ninguém o escreve à mão.

Cada arquivo de código e cada documento diz, de forma breve, qual licença o cobre: um
comentário de uma ou duas linhas no topo do código, uma linha no fim do documento. As
planilhas e os <dfn>arquivos de dados</dfn> — os `.json`, que guardam informação para os
scripts — ficam fora dessa regra: um comentário quebraria a leitura de quem abre a
planilha como tabela, e o `.json` nem aceita comentário. Que licença cobre cada parte do
projeto está no [README](README.md#licença).

Todo arquivo `.json` do projeto é só dado: <dfn>chaves e valores</dfn>, o nome de cada
informação e o valor dela. Nele não entra texto escrito para quem abre o arquivo — texto
corrido, explicação, instrução, exemplo ou marcador entre colchetes — nem referência a
documento: uma seção desta metodologia, o nome de um arquivo `.md`, o item de uma norma.
Vale, sim, o texto que é o próprio dado, mesmo corrido: o título de uma fonte, uma nota da
referência, a pergunta e o trecho literal de uma prova. O que a regra proíbe é o texto
escrito para explicar, instruir ou narrar. Nos modelos de `modelo-dados/`, o lugar de uma
instrução ou de um exemplo fica vazio: `""`, `[]` ou `{}`. Nos moldes de
`scripts/esquemas/`, ficam só os identificadores técnicos (`$schema` e `$id`) e o que os
scripts conferem em cada arquivo. O caminho de um arquivo no mapa do projeto é dado, mesmo
quando aponta para um documento `.md`: é onde o script lê ou grava aquele arquivo. A
variável entre chaves de um caminho, como `{item}` e `{planilha}`, também é dado: ninguém
escreve no lugar dela, é o script que a troca pelo valor, o id do item ou o nome da
planilha. Os documentos podem citar os `.json`; nenhum `.json` depende de um documento. O
que explica um arquivo de dados fica nos documentos, e a informação que sai de um `.json`
não se perde: ou já está num documento, ou passa para um.

Os modelos de `modelo-dados/` e os moldes de `scripts/esquemas/` são genéricos: servem a
qualquer disciplina e podem crescer, mas nunca se ajustam a um projeto só. Quando uma
disciplina precisa de uma informação que eles não têm, o campo novo entra de um jeito que
sirva a qualquer outra; nada que só sirva a uma disciplina, a um material ou a uma fonte
entra neles.

---

*Este documento está licenciado sob [CC BY-NC-SA 4.0](LICENSE-CONTENT.txt).*
