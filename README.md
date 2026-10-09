# Núcleo de Microbiologia: bacteriologia

![Licenca codigo](https://img.shields.io/badge/C%C3%B3digo-GPL--3.0-blue)
![Licenca conteudo](https://img.shields.io/badge/Conte%C3%BAdo-CC_BY--NC--SA_4.0-blue)

## O que é isto

Um material de estudo de Microbiologia, no recorte de bacteriologia, feito para cursos da
área da saúde como enfermagem, educação física, nutrição e fisioterapia. O
[`INDICE.md`](INDICE.md) tem um link pra cada documento, e o [`MANUAL.md`](MANUAL.md) é um
guia rápido de como estudar com o material. Este README apresenta o projeto: o aviso sobre
o recorte, como o material foi feito, de onde ele veio, as licenças e onde fica cada
arquivo.

Por enquanto, o projeto tem só a fonte transcrita: os documentos de estudo, as planilhas
de pergunta e os baralhos ainda não foram escritos.

## Aviso importante — leia antes de usar

Este conteúdo é construído a partir de um recorte de um livro-texto de Microbiologia (ver
[Origem do conteúdo](#origem-do-conteúdo) abaixo), escolhido por quem mantém o projeto:

- A seleção de quais itens entram, qual fato é "o mais importante" e qual resposta é "a
  resposta esperada" reflete essa escolha e esse livro — não é a cobertura completa da
  literatura da área.
- Simplificações são feitas pra organizar o conteúdo em histórias de causa e efeito, ou outros moldes, conforme o material se desenvolve, e
  em fichas secas, com uma resposta só pra cada tipo de fato, o que pode deixar de fora
  nuances e controvérsias que um material de referência completo traria.
- Este material serve como ferramenta de revisão, não como fonte principal de estudo —
  fatos importantes devem ser conferidos com a bibliografia oficial de cada disciplina
  antes de uma prova.

## Como este material foi feito

Parte do trabalho é feita por processos automáticos, e parte com ajuda de IA. Cada parte
do trabalho é uma de duas coisas:

- **Mecânica:** feita por um programa, sempre do mesmo jeito, sem julgar o conteúdo —
  copiar o texto do livro, página por página, conferir se a cópia é igual ao original,
  montar as referências, conferir se cada trecho citado está na fonte, montar os cartões
  do Anki.
- **Julgamento:** de uma pessoa, contra a fonte — escolher o recorte, decidir cada fato
  e conferir, por último, o texto das figuras, cada referência e cada cartão.

Neste projeto, o texto do livro foi copiado por um script, direto da versão digital, e é
conferido por script contra ela, sem leitura por IA. A IA entrou na escrita e na
adaptação dos scripts e confere, figura por figura, o texto de dentro das figuras, que foi
lido por OCR, antes do tique de uma pessoa. A escrita dos documentos e dos cartões ainda
não começou. O que é mecânico e o que é julgamento em cada etapa está explicado na
seção 11 ("Confira: primeiro o script, depois a pessoa") da
[metodologia](metodologia-de-conteudo.md#11-confira-primeiro-o-script-depois-a-pessoa),
que veio com o modelo `modelo-recorte-disciplina` e está na pasta principal deste projeto.

## Origem do conteúdo

O material original que serve de base para este núcleo fica em
[`docs/material-base/`](docs/material-base/). Cada documento e cada cartão cita, junto do
fato, a fonte de onde ele veio, no sistema autor-data da ABNT; as referências completas
ficam em `docs/REFERENCIAS.md`, que o script `referencias.py` gera a partir dos dados de
[`dados/fontes.json`](dados/fontes.json) assim que o formato da disciplina existir.

O material de base é o recorte de bacteriologia — os capítulos 12 a 17, p. 116 a 181 — do
livro *Microbiologia médica*, de Patrick R. Murray, Ken S. Rosenthal e Michael A. Pfaller
(9. ed., Guanabara Koogan, 2022), lido na versão digital. Ele não foi produzido por quem
mantém o projeto e não está coberto pela licença deste projeto. Por isso esse material
nunca é publicado nem repassado: fica só no computador de quem mantém o projeto. O mesmo
vale para a transcrição dele, a base de trechos do material de fora e a prova de cada
cartão, em `docs/material-base/gerados-ocr/`: são cópias de material de terceiros, usadas
só para conferir o que se escreve.

Ainda não há material de fora: ele só entra onde o recorte não cobre o que algum eixo da
ficha pede, e a ficha ainda não existe. Quando entrar, as cópias dele ficam em
`docs/material-base/fontes-externas/`, também sem publicar, e as referências, em
`docs/REFERENCIAS.md`.

## Licença

Uma licença diz o que cada pessoa pode fazer com um trabalho. Este projeto usa duas,
para duas partes diferentes, mais uma exceção — os detalhes estão em
[`NOTICE.md`](NOTICE.md):

| Parte | Licença | Significa que... |
|---|---|---|
| Programas (os scripts de `scripts/` e os verificadores de `.githooks/`) | [GPL-3.0](LICENSE) | Pode usar, mudar e repassar, mas as versões mudadas também precisam ficar abertas pra todo mundo |
| Conteúdo (tudo o que não é programa nem material de terceiros: documentos, planilhas, referências, dados) | [CC BY-NC-SA 4.0](LICENSE-CONTENT.txt) | Pode usar e adaptar dando o crédito, sem fins comerciais, mantendo a mesma licença |
| Material de terceiros em `docs/material-base/` | Nenhuma — é de terceiros | Não publicar nem repassar |

## Onde fica cada coisa

| Arquivo | O que é |
|---|---|
| `docs/material-gerado/` | Os documentos de teoria, dicionário e ficha, e as planilhas de pergunta — ainda não escritos |
| `docs/REFERENCIAS.md` | As referências, conforme a ABNT, de todas as fontes citadas nos documentos e nos cartões — geradas a partir de `dados/fontes.json` quando o formato da disciplina existir |
| [`dados/fontes.json`](dados/fontes.json) | Os dados de cada fonte (autoria, título, local, editora, data, endereço), de onde saem as referências |
| `dados/formato.json` | O formato da disciplina: curso, nível, itens, eixos, elos e colunas dos cartões — ainda não decidido |
| `dados/bases/` | Um arquivo por item: o que foi lido do material de fora, a decisão sobre cada frase e a cobertura de cada subtópico (só códigos e decisões; o texto das fontes nunca é publicado) — ainda não há material de fora |
| [`dados/estilo-cartao.css`](dados/estilo-cartao.css) | A aparência dos cartões no Anki |
| [`projeto.json`](projeto.json) | O mapa do projeto: onde fica cada coisa; os scripts tiram todo caminho daqui |
| [`metodologia-de-conteudo.md`](metodologia-de-conteudo.md) | A metodologia: o método inteiro, do material de aula ao cartão, com o que é mecânico e o que é julgamento em cada etapa (veio com o modelo) |
| [`DESCUBRA-SEU-MODELO.md`](DESCUBRA-SEU-MODELO.md) | As perguntas que decidem o formato da disciplina; as respostas deste projeto vão para `dados/formato.json` (veio com o modelo) |
| [`regras-abnt.md`](regras-abnt.md) | O que as normas da ABNT de citação e de referência pedem, item por item, e quem cuida de cada regra (veio com o modelo) |
| [`trabalhar-com-ia.md`](trabalhar-com-ia.md) | O guia de trabalho com IA: o que pedir em cada etapa, o que conferir depois e as regras que a IA segue sempre (veio com o modelo) |
| [`modelo-dados/`](modelo-dados/) | Os modelos em branco dos arquivos de dados e do estilo dos cartões, de onde foram copiados o `projeto.json` e os arquivos de `dados/` (veio com o modelo) |
| [`modelo-dados/fluxo-ia.json`](modelo-dados/fluxo-ia.json) | O método em dados: as etapas na ordem, com o que entra e o que sai de cada uma, que a IA recebe junto do guia de trabalho com IA (veio com o modelo e fica como está) |
| [`INDICE.md`](INDICE.md) | O índice, com um link para cada documento; os itens ficam no índice do topo de cada um |
| [`MANUAL.md`](MANUAL.md) | O guia rápido de como estudar com o material e como ajudar a corrigi-lo |
| [`LICENSE`](LICENSE) | O texto completo da GPL-3.0 (programas) |
| [`LICENSE-CONTENT.txt`](LICENSE-CONTENT.txt) | O texto completo da CC BY-NC-SA 4.0 (conteúdo) |
| [`NOTICE.md`](NOTICE.md) | Qual licença vale pra qual arquivo, e a exceção do material de terceiros |
| [`.gitignore`](.gitignore) | Pra quem guarda o projeto no GitHub: a lista do que nunca vai pra lá (o material de terceiros e arquivos temporários) |
| [`.githooks/`](.githooks/README.md) | Pra quem guarda o projeto no GitHub: a proteção das fontes, que barra a versão que levar material de terceiros, e a conferência das mensagens de cada versão (veio com o modelo) |
| [`scripts/`](scripts/README.md) | Os pequenos programas que fazem a parte mecânica do método — o README deles diz, em palavras simples, pra que serve cada um e como rodar |
| `anki-decks/` | Os baralhos prontos pra importar no Anki (os arquivos `.apkg`) — ainda não gerados |

## Como usar

Ainda não há documentos nem baralhos para estudar: por enquanto, o projeto tem a
transcrição da fonte, que nunca é publicada. Quando houver, importe no Anki os baralhos de
`anki-decks/` (os arquivos `.apkg`), ou leia os documentos direto em
`docs/material-gerado/` (ver o [MANUAL.md](MANUAL.md)). Para achar um item, abra o
documento pelo [`INDICE.md`](INDICE.md) e use o índice do topo dele. Para mudar o
conteúdo, mude o documento e a planilha correspondente em `docs/material-gerado/` e gere
os baralhos de novo com o script `montar_deck.py` (o
[README dos scripts](scripts/README.md) diz como rodar).

## Referências

As referências de todas as fontes citadas no projeto — o livro do recorte e o material de
fora (ver [Origem do conteúdo](#origem-do-conteúdo)) —, conforme a ABNT NBR 6023, ficam em
`docs/REFERENCIAS.md`, gerado a partir de [`dados/fontes.json`](dados/fontes.json) quando o
formato da disciplina existir.

---

*Este documento está licenciado sob [CC BY-NC-SA 4.0](LICENSE-CONTENT.txt). Ver
[NOTICE.md](NOTICE.md) para detalhes.*
