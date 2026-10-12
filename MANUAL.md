# Manual de Uso — Núcleo de Microbiologia: bacteriologia

Este manual explica como usar este material, do jeito mais rápido possível. Não é
documentação técnica — é um guia para quem só quer estudar, sem precisar entender a
estrutura interna do projeto inteiro.

## Antes de tudo: isto foi feito por uma pessoa só

Todo o material deste projeto — texto ou resposta — foi selecionado e conferido por quem
organizou o projeto. Parte do trabalho foi feita por programas e com
ajuda de IA; o que foi mecânico e o que foi julgamento está explicado no
[README.md](README.md#como-este-material-foi-feito). Não é uma revisão sistemática e não
passou por banca revisora. Na prática:

- Pode ter erro em qualquer parte — texto ou resposta.
- O recorte — que aulas e que partes do livro-texto entram — foi escolha de quem
  organizou o material. Dentro dele, entra tudo o que as aulas trazem sobre bactérias,
  com o que o livro-texto diz sobre cada ponto; a forma de estudo veio de pesquisas sobre
  como os cursos pedem a matéria e sobre como se aprende (ver a [análise da
  matéria](docs/analise-da-materia.md)).

Este material é um apoio de revisão, não a fonte única de verdade — vale conferir com o
material oficial da disciplina antes de uma prova. Erros e sugestões podem ser
reportados como descrito no [Nível 4](#nível-4--erros-e-como-colaborar).

O manual está organizado em níveis, do mais simples ao mais detalhado.

---

## Nível 1 — Só quero estudar agora

1. Abra o <dfn>Anki</dfn> no computador ou celular (programa gratuito de revisão espaçada
   — disponível em [apps.ankiweb.net](https://apps.ankiweb.net)).
2. Importe os arquivos de `anki-decks/` — são arquivos <dfn>.apkg</dfn>, o formato que o
   Anki usa para empacotar um baralho pronto. Arraste o arquivo pra dentro da janela do
   Anki, ou use o menu Arquivo > Importar dentro do Anki.
3. No Anki, os cartões aparecem numa pasta com o nome da disciplina, e dentro dela uma
   pasta pra cada arquivo.

### Atualizando o baralho depois de editar as planilhas

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

## Nível 2 — De onde isso veio

O projeto tem duas pastas de conteúdo bem diferentes:

**`docs/material-base/`** — as aulas originais, o livro-texto e, onde eles não chegam,
as cópias do material de fora usado (as referências de tudo estão em
`docs/REFERENCIAS.md`). Nunca é publicada nem repassada (ver [NOTICE.md](NOTICE.md)) —
fica só localmente.

**`docs/material-gerado/`** — todo o conteúdo do material original reescrito e
reorganizado em texto corrido, mais claro. É material de estudo completo por si só —
dá pra estudar só lendo os documentos, sem depender do baralho. Tem cinco tipos de
documento ([análise da matéria, Os documentos](docs/analise-da-materia.md#os-documentos)):

- **<dfn>Teoria fundamental</dfn>** — os conceitos gerais que vêm antes de entrar em item
  específico, por tema.
- **<dfn>Ficha determinística</dfn>** — cada bactéria, e cada item de uma família (como os
  antimicrobianos), em tabela direta. Bom pra revisão de véspera de prova.
- **<dfn>Dicionário de gatilhos</dfn>** — conta cada bactéria como uma história em cadeia.
  Bom pra entender o porquê.
- **Quadros e casos** — de um quadro, como uma síndrome ou um local do corpo, às bactérias
  que podem causá-lo, com casos pra treinar.
- **Perguntas de prova** — uma por aula, pra treinar a resposta escrita, com uma
  resposta-modelo pra comparar.

Todo fato, nos documentos e nos cartões, traz a citação da fonte de onde veio; as
referências completas estão em `docs/REFERENCIAS.md`.

Resumindo:

```
Material de aula   →   documento reescrito   →   planilha   →   cartão de Anki
(material-base)         (material-gerado)         (mesma pasta)  (anki-decks/*.apkg)
```

## Nível 3 — Quero achar um item específico rápido

O [`INDICE.md`](INDICE.md) tem um link pra cada documento. Abra o dicionário ou a ficha
por ali: no topo de cada um há um índice próprio, com link direto pro trecho de cada
item.

## Nível 4 — Erros e como colaborar

Este material é curadoria de uma pessoa só — pode ter erro. Encontrou um erro ou
tem uma sugestão melhor? Mande um e-mail para **lixotrashlixo@proton.me**, incluindo:

1. **No assunto:** o nome do item + qual parte está errada.
2. **No corpo:** o que está errado, especificamente, e uma sugestão melhor se tiver.

Não precisa formalidade — quanto mais direto, mais rápido dá pra revisar.

## Quer saber mais

Para detalhes técnicos (estrutura de pastas, licença, avisos sobre o recorte), veja o
**[README.md](README.md)**.

---

*Este documento está licenciado sob [CC BY-NC-SA 4.0](LICENSE-CONTENT.txt). Ver
[NOTICE.md](NOTICE.md) para detalhes.*
