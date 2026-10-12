# Manual de Uso — Núcleo de Microbiologia: bacteriologia

Este manual explica como estudar com este material, do jeito mais rápido possível. Não é
documentação técnica — é um guia para quem só quer estudar, sem precisar entender a
estrutura interna do projeto inteiro. O que este material é, e o que ele não é, está no
[aviso do README](README.md#aviso-importante--leia-antes-de-usar).

O manual está organizado em níveis, do mais simples ao mais detalhado.

---

## Nível 1 — Só quero estudar agora

1. Abra o <dfn>Anki</dfn> no computador ou celular (programa gratuito de revisão espaçada
   — disponível em [apps.ankiweb.net](https://apps.ankiweb.net)).
2. Importe os arquivos de `anki-decks/` — são arquivos <dfn>.apkg</dfn>, o formato que o
   Anki usa para empacotar um baralho pronto. Arraste o arquivo pra dentro da janela do
   Anki, ou use o menu Arquivo > Importar dentro do Anki.
3. No Anki, os cartões aparecem numa pasta com o nome da disciplina.

O Anki decide quando cada cartão volta: basta estudar os cartões que ele mostra a cada
dia. Antes de virar um cartão, tente lembrar a resposta.

### Atualizando o baralho depois de editar as planilhas

Uma mudança feita direto num cartão, dentro do Anki, se perde quando o baralho é refeito e
importado de novo. O que vale é a planilha de onde o cartão sai: para mudar um cartão de
vez, mude a planilha e refaça o baralho.

As perguntas de cada cartão ficam guardadas em <dfn>planilhas</dfn> (arquivos `.csv`,
texto simples com colunas separadas por vírgula) dentro de `docs/material-gerado/` — dá
pra mudar no Excel, no Google Sheets ou num editor de texto, como o <dfn>VSCode</dfn> (um
editor gratuito, onde se abre a pasta do projeto). Depois de mudar:

1. No VSCode, abra o <dfn>terminal</dfn>, a janela onde se digita um comando em vez de
   clicar: menu **Terminal → Novo Terminal** (ou o atalho `` Ctrl+` ``).
2. Digite `python scripts/montar_deck.py` e aperte Enter.
3. Os arquivos `.apkg` dentro de `anki-decks/` são substituídos pelos novos; basta
   importar de novo no Anki para ver as mudanças.

O [README dos scripts](scripts/README.md) explica esses passos com mais calma. Se travar,
peça ajuda a uma IA: diga o que você fez e o que apareceu na tela.

## Nível 2 — Os documentos de estudo

Os documentos de estudo ficam em `docs/material-gerado/`. Eles ensinam a matéria das
aulas, com o que o livro-texto diz de cada ponto, em texto corrido e explicado — dá pra
estudar só lendo os documentos, sem depender do baralho. Os cartões do Anki e as perguntas
de prova treinam o que os documentos ensinam. São cinco tipos de documento ([análise da
matéria, Os documentos](docs/analise-da-materia.md#os-documentos)):

- **<dfn>Teoria fundamental</dfn>** — os conceitos gerais que vêm antes de entrar em item
  específico, por tema.
- **<dfn>Ficha determinística</dfn>** — cada bactéria, e cada item de uma família (como os
  antimicrobianos), em tabela direta. Bom pra revisão de véspera de prova.
- **<dfn>Dicionário de gatilhos</dfn>** — conta cada bactéria como uma história em cadeia.
  Bom pra entender o porquê.
- **Quadros e casos** — de um quadro, como uma síndrome ou um local do corpo, às bactérias
  que podem causá-lo, com casos pra treinar.
- **Perguntas de prova** — uma por aula, pra treinar a resposta escrita: escreva a sua
  resposta e depois compare com a resposta-modelo. Use quando quiser.

Todo fato, nos documentos e nos cartões, traz a citação da fonte de onde veio; as
referências completas estão em `docs/REFERENCIAS.md`.

## Nível 3 — Quero achar um item específico rápido

O [`INDICE.md`](INDICE.md) tem um link pra cada documento. Abra o dicionário ou a ficha
por ali: no topo de cada um há um índice próprio, com link direto pro trecho de cada
item.

## Nível 4 — Erros e como colaborar

Encontrou um erro ou tem uma sugestão melhor? Mande um e-mail para
**lixotrashlixo@proton.me**, dizendo onde ele está e o que está errado:

1. **No assunto, onde está:** o título do documento e o título da parte onde está o erro —
   o título mais próximo acima dele. Se o erro está num cartão do Anki, a pergunta do
   cartão.
2. **No corpo, o que está errado:** a frase com o erro, copiada como está, o que há de
   errado nela e, se você souber, como fica certo.

Por exemplo, para um erro de escrita numa ficha:

> **Assunto:** Ficha de Staphylococcus aureus › Fatores de virulência
>
> **Corpo:** Na frase "O *Staphylococus aureus* produz coagulase", o nome está com um "c"
> só. O certo é *Staphylococcus*.

O mesmo vale para qualquer documento de estudo: todos têm um título e partes com título.

Não precisa formalidade — quanto mais direto, mais rápido dá pra revisar.

---

*Este documento está licenciado sob [CC BY-NC-SA 4.0](LICENSE-CONTENT.txt).*
