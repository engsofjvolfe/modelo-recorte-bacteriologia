# Trabalhar com uma IA

O método deste modelo usa IA em quase todas as etapas: transcrever as aulas, preencher os
dados das fontes, pesquisar e analisar a matéria pra propor o formato da disciplina,
escrever os documentos, gerar os cartões. Este guia diz, etapa por etapa, o que pedir à IA, o que entregar a ela, o que
conferir depois e o que é sempre seu, e também as regras que a IA segue em todas as
etapas. Por isso ele é pra você e pra IA: você lê e entrega a ela. Serve pra qualquer
assistente de IA: o modelo não depende de nenhum.

## Antes de começar: escolha como usar a sua IA

Cada IA tem os seus modos. Há versão gratuita e paga; há a que conversa no navegador e
a que trabalha dentro do editor, lendo as pastas do seu computador; há a que trabalha
sozinha e a que divide o trabalho entre vários agentes, como uma equipe. A escolha é
sua. O que muda de um modo pra outro é quanto a IA faz sozinha:

- **Se ela lê e escreve os arquivos do projeto**, ela mesma pode copiar arquivos,
  escrever as transcrições e rodar os scripts. Você confere o que ela fez.
- **Se ela só conversa**, você entrega cada arquivo na conversa, copia o que ela
  devolver pro arquivo certo e roda os scripts você mesmo (o
  [README dos scripts](scripts/README.md) explica como, passo a passo).

Nos dois casos, quem decide e quem dá a palavra final é você.

## Entregue o método à IA

O método chega à IA em duas partes. Uma é este guia: o que fazer em cada etapa e as
regras que valem sempre. A outra é o arquivo
[`modelo-dados/fluxo-ia.json`](modelo-dados/fluxo-ia.json), o método em dados: as etapas
na ordem e, de cada uma, o que entra, o que sai, os scripts e as conferências. Você não
precisa ler esse arquivo; basta entregá-lo.

1. O `fluxo-ia.json` não se copia: o projeto da sua disciplina é uma cópia do modelo
   inteiro, e o arquivo fica onde já está, em `modelo-dados/`. O `projeto.json` (o mapa
   de onde fica cada coisa) fica na pasta principal do projeto.
2. Na primeira conversa, entregue os dois arquivos e este guia, e peça: "Leia o
   `modelo-dados/fluxo-ia.json` e o `trabalhar-com-ia.md` inteiros e guarde os dois na
   sua memória ou nas instruções do projeto."
3. Se a sua ferramenta não guarda nada de uma conversa pra outra, entregue o
   `fluxo-ia.json` e este guia de novo no começo de cada conversa nova, com o pedido:
   "Releia os dois inteiros antes de continuar." Este guia pede isso à IA (ver
   [Para a IA](#para-a-ia)).

Se a IA não consegue abrir os arquivos do modelo, entregue também, em cada etapa, o que
a etapa diz que ela lê antes (a seção da metodologia, o Descubra seu modelo, as regras
da ABNT).

E se você travar em qualquer passo — abrir o terminal, rodar um script, entender uma
mensagem que apareceu na tela —, peça ajuda à própria IA: descreva o que você fez e o
que apareceu, e peça o passo a passo pro seu computador.

## Para a IA

Esta parte diz o que a IA faz ao receber o método e as regras que ela segue em todas as
etapas. Leia você também: é o que você pode esperar dela.

### Ao receber o método

- A IA guarda o `fluxo-ia.json` e este guia inteiros na memória da ferramenta ou nas
  instruções do projeto, se a ferramenta tiver um desses lugares. Se a ferramenta não
  guarda nada de uma conversa pra outra, a IA pede a você que entregue os dois no começo
  de cada conversa, e os relê inteiros antes de continuar.
- Antes de qualquer etapa, ela lê o `projeto.json` do projeto.
- Ela segue as etapas na ordem. Se não estiver claro em que etapa o projeto está, ela
  pergunta a você.
- Antes de cada etapa, ela lê inteiros os documentos e as seções da metodologia que a
  etapa traz em **A IA lê antes**. Eles vêm com o modelo e, por isso, estão no projeto.

### Como ler o método em dados

O `fluxo-ia.json` traz a lista `etapas`, na ordem do trabalho. Em cada etapa:

- `id` é o nome curto da etapa, o mesmo que aparece entre parênteses no título dela, em
  [Etapa por etapa](#etapa-por-etapa);
- `entradas`, `saidas` e `conferencias` são chaves de `caminhos` do `projeto.json`, e o
  caminho de cada uma é o que o `projeto.json` diz;
- `entradas` é o que a etapa lê. Isso inclui o que os scripts dela leem do `projeto.json`
  e o que a IA lê pra fazer o trabalho da etapa, menos o que a etapa só grava;
- `saidas` é tudo o que a etapa grava: o que os scripts dela gravam, até de passagem
  (como as referências, que o `registrar_fonte.py` refaz sozinho), e o que a IA produz
  na etapa;
- `conferencias` são as conferências da etapa;
- `scripts` são os scripts que a etapa usa, da pasta `scripts/`.

### Regras que valem sempre

Valem sempre, junto do tique (ver [Etapa por etapa](#etapa-por-etapa)) e do que é
[sempre seu](#o-que-é-sempre-seu):

- A IA nunca inventa nem deduz um fato que não esteja escrito na fonte. Se um dado falta
  ou é ambíguo, ela pergunta a você.
- A IA lê cada fonte e cada documento inteiro antes de escrever, sem ferramenta que corte
  ou resuma o texto.
- Cada etapa nasce da anterior, nunca direto da fonte: os documentos nascem das
  transcrições conferidas e da base do material de fora; os cartões, dos documentos.
- Todo fato tirado de uma fonte leva a chamada dela, no sistema autor-data da norma de
  citações da ABNT (NBR 10520), com o lugar: a página impressa ou o slide.
- Fato que a fonte trata como possibilidade entra com a ressalva escrita, nunca como
  certeza.
- O material de terceiros nunca entra nas versões gravadas do projeto, como as que vão
  pro GitHub, nem é publicado: o material de aula, as transcrições, as cópias e a base do
  material de fora, as provas dos cartões e os arquivos de conferência.
- Nenhum caminho é escrito de memória: todo caminho sai do `projeto.json`.
- Nunca se renomeia a pasta `scripts/`, nada dentro dela nem o `projeto.json`: é por
  esses nomes que os scripts se acham.
- A pasta do material de base é a pasta protegida: nunca muda de nome nem de lugar, e
  toda fonte fica dentro dela. Se uma fonte estiver fora, os scripts oferecem levá-la; a
  IA só usa o `--mover` depois que você autorizar.
- Nada de disciplina vai pro código dos scripts: o que muda de um projeto pra outro fica
  nos arquivos de dados.
- Todo arquivo JSON (os `.json`, que guardam os dados) que a IA gerar é só dado: chaves e
  valores, ou seja, o nome de cada informação e o valor dela. Nada de texto corrido,
  explicação, instrução, exemplo ou marcador entre colchetes, e nenhuma referência a
  documento (seção da metodologia, nome de arquivo `.md`, item de norma). Vale, sim, o
  texto que é o próprio dado, mesmo corrido: o título de uma fonte, uma nota da
  referência, a pergunta e o trecho literal de uma prova. O que a regra proíbe é o texto
  escrito pra explicar, instruir ou narrar. Também é dado o caminho de um arquivo no
  `projeto.json`, mesmo quando aponta pra um `.md`, e a variável entre chaves de um
  caminho, como `{item}` e `{planilha}`, que os scripts trocam pelo valor. Um documento
  (os `.md`, como este guia) pode citar um JSON; nenhum JSON depende de documento. A
  informação que sai de um JSON não se perde: ou já está num documento, ou passa pra um.
- O script recolhe e confere o que é mecânico, a IA julga na curadoria e você julga na
  aceitação.
- Uma linha `ERRO` ou `FALTA` de script se resolve antes de ticar.
- Se você guarda o projeto no GitHub, cada mensagem que descreve uma mudança tem um
  título e um parágrafo em prosa, sem lista.
- A IA fala com você em palavras simples, porque você pode não saber programar: explica
  cada termo técnico na primeira vez e, quando você travar, dá o passo a passo pro seu
  computador.

## Etapa por etapa

Em cada etapa, a IA faz uma primeira passada e marca o tique dela nas conferências. O
tique que vale é o seu: nada está conferido sem ele (ver a
[seção 11 da metodologia](metodologia-de-conteudo.md#11-confira-primeiro-o-script-depois-a-pessoa)).

### 1. Preparar o projeto (`preparar`)

- **A IA lê antes:** a
  [seção 15 da metodologia](metodologia-de-conteudo.md#15-checklist-adicionando-uma-disciplina-nova)
  e o [README da conferência das mensagens](.githooks/README.md).
- **Peça:** que faça o projeto: uma cópia do modelo inteiro, com o nome do projeto. Nela
  já vêm a pasta `scripts/`, a lista do que nunca vai pro GitHub (`.gitignore`), os dois
  arquivos de licença (`LICENSE` e `LICENSE-CONTENT.txt`) e o `fluxo-ia.json`, que fica
  em `modelo-dados/`. Dentro da cópia, que copie de `modelo-dados/` o mapa do projeto
  (`projeto.json`) pra pasta principal e o estilo dos cartões (`estilo-cartao.css`) pra
  pasta `dados/`. Depois, que confira o mapa do projeto com o script `validar_dados.py`.
- **Confira depois:** se as pastas que o mapa do projeto indica são as que você quer.
- **Se você guarda o projeto no GitHub:** o projeto ganha um repositório próprio (o lugar
  onde o GitHub guarda o projeto e o histórico das mudanças dele), sem o histórico do
  modelo. Ative também a conferência das mensagens e a proteção das fontes. É opcional,
  mas é ela que barra uma fonte que ia pro GitHub por engano (ver o
  [README dela](.githooks/README.md)).
- **Sempre seu:** autorizar a IA a fazer a cópia do modelo e a mover uma fonte pra pasta
  protegida, quando um script perguntar.

### 2. Transcrição da aula (`transcricao`)

- **A IA lê antes:** a
  [seção 1 da metodologia](metodologia-de-conteudo.md#1-trate-as-fontes-da-aula).
- **Entregue:** o material de aula.
- **Peça:** a transcrição de cada página, só com o que está escrito, no padrão da seção
  1; o registro de cada transcrição com o `registrar_fonte.py`, com a chave da
  referência da fonte; e a conferência delas, com o `conferencia.py`. Se o material é
  um documento HTML que marca as páginas impressas, como um livro digital, a transcrição
  sai do script `transcrever_html.py`; se é uma apresentação em pptx, do
  `transcrever_pptx.py`. Nos dois, o que a IA confere é só o texto de dentro de cada
  imagem, contra a própria imagem.
- **Confira depois:** cada página, na conferência das transcrições, contra a imagem; num
  documento HTML ou numa apresentação em pptx, que o script não aponta erro em nenhuma
  página, e o texto de cada imagem.
- **Sempre seu:** o tique de cada página (num documento HTML ou numa apresentação em
  pptx, o de cada imagem).

### 3. Referências das fontes (`referencias`)

- **A IA lê antes:** a
  [seção 2 da metodologia](metodologia-de-conteudo.md#2-cite-cada-fonte-conforme-a-abnt)
  e as [regras da ABNT](regras-abnt.md).
- **Peça:** que preencha os dados de cada fonte no arquivo de fontes (`fontes.json`), como
  estão na folha de rosto ou na página do documento, confira o arquivo com o
  `validar_dados.py` e gere as referências com o `referencias.py`.
- **Confira depois:** cada referência e a chamada dela, na conferência das referências,
  contra a fonte. As regras da ABNT dizem o que cada informação leva.
- **Sempre seu:** a escolha do *et al.* e o tique de cada referência.

### 4. Formato da disciplina (`formato`)

- **A IA lê antes:** a
  [seção 3 da metodologia](metodologia-de-conteudo.md#3-descubra-o-formato-da-disciplina),
  o [Descubra seu modelo](DESCUBRA-SEU-MODELO.md) e as [regras da ABNT](regras-abnt.md).
- **Entregue:** o curso, a disciplina e o nível de estudo.
- **Peça:** que olhe os tiques na conferência das transcrições, pra saber o que já tem o
  seu tique; que pesquise as três bases da seção 3 em fontes acadêmicas robustas, lendo
  cada uma inteira, guardando nas evidências da pesquisa o trecho literal que sustenta
  cada ponto e preenchendo os dados de cada fonte no arquivo de fontes; que leia inteira
  cada transcrição e analise cada parte do material com as perguntas da seção 3, sem
  deixar trecho de fora, e junte o que se repete entre as partes; que escreva a análise da matéria, com a chamada de cada fonte como
  a conferência das referências mostra; e só então proponha cada resposta do Descubra seu
  modelo, dizendo na conversa por que ela cabe, ou não, nesse curso e nesse nível. Depois,
  que grave as respostas aceitas no arquivo de formato, confira os dados com o
  `validar_dados.py` e refaça as referências com o `referencias.py`.
- **Confira depois:** na análise da matéria, se cada parte do material está nela, trecho
  por trecho, e se cada ponto da pesquisa tem a chamada e o trecho literal que o sustenta;
  na conferência das referências, cada fonte da pesquisa; e se o arquivo de formato
  (`formato.json`) tem só as respostas que você aceitou.
- **Sempre seu:** as formas de estudo escolhidas, cada resposta do formato e o tique de
  cada referência. A IA propõe; você decide.

### 5. Material de fora (`material-de-fora`)

- **A IA lê antes:** a
  [seção 4 da metodologia](metodologia-de-conteudo.md#4-complete-a-aula-com-material-de-fora).
- **Peça:** que olhe os tiques na conferência das transcrições, pra saber quais páginas
  já têm o seu tique; que marque, item por item, a partir das transcrições conferidas,
  cada subtópico do formato como coberto pela aula, pelo material de fora ou como
  lacuna, e proponha, com a referência dele, um material oficial ou de referência da
  área pra cada subtópico que a aula não cobre; depois, que monte a base dele: declare as
  páginas lidas no arquivo de dados do item, rode o `base_externa.py` e classifique cada
  frase.
- **Confira depois:** a cobertura e a classe de cada frase, na conferência dos trechos.
- **Sempre seu:** aceitar ou não cada material de fora, e o tique de cada página.

### 6. Documentos de conteúdo (`documentos`)

- **A IA lê antes:** as seções 5 a 8 e 12 da [metodologia](metodologia-de-conteudo.md).
- **Peça:** que olhe os tiques nas conferências das transcrições, dos trechos e das
  referências, pra saber o que já tem o seu tique; que leia inteiras a análise da matéria,
  as transcrições e as bases conferidas e só então escreva, nas formas de estudo que a
  análise escolheu e na grade do formato, primeiro a teoria fundamental e depois os outros
  documentos, com a chamada de cada fato como a conferência das referências mostra.
- **Confira depois:** cada documento contra as fontes, com a auditoria da
  [seção 16 da metodologia](metodologia-de-conteudo.md#16-checklist-auditando-uma-disciplina-existente).
- **Sempre seu:** o recorte — o que entra, o quão fundo e o que é mais importante.

### 7. Cartões (`cartoes`)

- **A IA lê antes:** a
  [seção 9 da metodologia](metodologia-de-conteudo.md#9-cartões-de-revisão-espaçada).
- **Peça:** que olhe os tiques nas conferências das transcrições e dos trechos, pra saber
  o que já tem o seu tique, e só então faça as planilhas de pergunta a partir dos
  documentos de conteúdo, um ou mais cartões, cada um com um fato só, pra cada fato dos
  documentos, com a coluna `fonte` só com as chamadas e o lugar; a prova de
  cada cartão, com a pergunta igual à da planilha, os trechos copiados letra por letra
  das transcrições e das bases conferidas e a afirmação (se a fonte afirma o fato ou o
  trata como possibilidade); e a conferência dos cartões, com o `confere_cartoes.py`.
- **Confira depois:** cada cartão, na conferência dos cartões, contra o trecho que o
  prova; e se a resposta traz a ressalva quando a fonte trata o fato como possibilidade.
- **Sempre seu:** o tique de cada cartão.

### 8. Baralho (`baralho`)

- **A IA lê antes:** a
  [seção 10 da metodologia](metodologia-de-conteudo.md#10-gere-o-baralho-com-o-script-do-modelo).
- **Peça:** que gere os baralhos com o script `montar_deck.py`.
- **Confira depois:** importe os baralhos no Anki e veja se os cartões aparecem como na
  planilha.

### 9. Documentos de apresentação (`raiz`)

- **A IA lê antes:** as seções 13 e 14 da [metodologia](metodologia-de-conteudo.md) e o
  `LEIA-ME.md` da pasta `modelo-documentos-raiz/`, que vem com o modelo.
- **Peça:** que copie os quatro documentos de `modelo-documentos-raiz/` pra pasta
  principal do projeto, no lugar dos documentos do modelo que têm o mesmo nome (o
  `README.md` e o `NOTICE.md`), e preencha cada trecho entre colchetes.
- **Sempre seu:** o aviso do recorte, a origem do material e o contato pra relatar erros.

### 10. Conferência final (`auditoria`)

- **A IA lê antes:** as seções 11 e 16 da [metodologia](metodologia-de-conteudo.md).
- **Peça:** que rode os scripts da análise mecânica da seção 16, resolva cada linha `ERRO`
  ou `FALTA` e aponte toda parte das conferências que ainda não tem o seu tique.
- **Sempre seu:** o tique final em cada parte e a análise humana da lista de revisão
  da [seção 16 da metodologia](metodologia-de-conteudo.md#16-checklist-auditando-uma-disciplina-existente).

## O que é sempre seu

A IA propõe, dizendo por quê, escreve e confere primeiro; você decide e confere por
último. São sempre seus: o formato da disciplina, o recorte, a escolha de cada material
de fora, o tique final de cada conferência e a decisão de publicar. E, se a IA disser
algo que não está na fonte, a fonte vale, não a IA.

---

*Este documento está licenciado sob [CC BY-NC-SA 4.0](LICENSE-CONTENT.txt).*
