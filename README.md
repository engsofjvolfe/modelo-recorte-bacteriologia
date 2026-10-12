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

## Aviso importante — leia antes de usar

Este conteúdo é construído a partir das aulas de uma disciplina de Microbiologia e de um
recorte de um livro-texto da área (ver [Origem do conteúdo](#origem-do-conteúdo) abaixo),
escolhido por quem mantém o projeto:

- A seleção de quais itens entram, qual fato é "o mais importante" e qual resposta é "a
  resposta esperada" reflete essa escolha, essas aulas e esse livro — não é a cobertura completa da
  literatura da área.
- Simplificações são feitas pra organizar o conteúdo nos moldes do material — histórias
  de causa e efeito, fichas com uma resposta só pra cada tipo de fato, quadros e casos
  ([análise da matéria, Os moldes](docs/analise-da-materia.md#os-moldes)) —, o que pode
  deixar de fora nuances e controvérsias que um material de referência completo traria.
- Este material serve como ferramenta de revisão, não como fonte principal de estudo —
  fatos importantes devem ser conferidos com a bibliografia oficial de cada disciplina
  antes de uma prova.

## Como este material foi feito

Parte do trabalho é feita por processos automáticos, e parte com ajuda de IA. Cada parte
do trabalho é uma de duas coisas:

- **<dfn>Mecânica</dfn>:** feita por um programa, sempre do mesmo jeito, sem julgar o
  conteúdo — copiar o texto das aulas, slide por slide, e o do livro, página por página,
  conferir se a cópia é igual ao original, montar as referências, conferir se cada trecho
  citado está na fonte, montar os cartões do Anki.
- **<dfn>Julgamento</dfn>:** de uma pessoa, contra a fonte — escolher o recorte, decidir
  cada fato e conferir, por último, o texto das figuras, cada referência e cada cartão.

O texto das aulas e o do livro é copiado por script dos arquivos dos slides e da versão
digital do livro e conferido por script contra eles, sem leitura por IA. Os scripts são
escritos e adaptados com ajuda de IA. O texto de dentro das figuras é lido por OCR e
conferido por uma pessoa, olhando a imagem. Nas figuras dos capítulos 12 a 17 do livro, a
IA confere esse texto antes da pessoa, figura por figura, e
[`docs/texto-das-figuras.md`](docs/texto-das-figuras.md) diz como ele é escrito; nas outras
figuras, só a pessoa o corrige.

## Origem do conteúdo

O material original que serve de base para este núcleo fica em
[`docs/material-base/`](docs/material-base/). Cada documento e cada cartão cita, junto do
fato, a fonte de onde ele veio, no sistema autor-data da ABNT; as referências completas
ficam em `docs/REFERENCIAS.md`, que o script `referencias.py` gera a partir dos dados de
[`dados/fontes.json`](dados/fontes.json).

O material de base são as aulas da disciplina de Microbiologia do Departamento de
Microbiologia, Imunologia e Parasitologia da Universidade Federal do Triângulo Mineiro, do
Prof. Kennio Ferreira Paim — 15 apresentações de slides, das aulas 1 a 17 —, e o recorte de
bacteriologia — os capítulos 12 a 35, p. 116 a 374 — do livro *Microbiologia médica*, de
Patrick R. Murray, Ken S. Rosenthal e Michael A. Pfaller (9. ed., Guanabara Koogan, 2022),
lido na versão digital. As aulas são a base principal: elas dão os pontos da matéria, e o
livro completa cada ponto com o que diz sobre ele ([metodologia, seção
4](metodologia-de-conteudo.md#4-complete-a-aula-com-material-de-fora)). Esse
material não foi produzido por quem mantém o projeto e não está coberto pela licença deste
projeto. Por isso ele nunca é publicado nem repassado. O mesmo
vale para a transcrição dele, as evidências da pesquisa, a base de trechos do material de
fora e a prova de cada cartão, em `docs/material-base/gerados-ocr/`: são cópias de material de terceiros, usadas
só para conferir o que se escreve.

Material de fora entra onde nem as aulas nem o livro chegam. As cópias dele ficam em
`docs/material-base/fontes-externas/`, também sem publicar, e as referências, em
`docs/REFERENCIAS.md`.

## Licença

Uma <dfn>licença</dfn> diz o que cada pessoa pode fazer com um trabalho: usar, mudar,
repassar. Este projeto usa duas, para duas partes diferentes, mais uma exceção — os
detalhes estão em [`NOTICE.md`](NOTICE.md):

| Parte | Licença | Significa que... |
|---|---|---|
| Programas (os scripts de `scripts/` e os verificadores de `.githooks/`) | [GPL-3.0](LICENSE) | Pode usar, mudar e repassar, mas as versões mudadas também precisam ficar abertas pra todo mundo |
| Conteúdo (tudo o que não é programa nem material de terceiros: documentos, planilhas, referências, dados) | [CC BY-NC-SA 4.0](LICENSE-CONTENT.txt) | Pode usar e adaptar dando o crédito, sem fins comerciais, mantendo a mesma licença |
| Material de terceiros em `docs/material-base/` | Nenhuma — é de terceiros | Não publicar nem repassar |

## Onde fica cada coisa

Consultar [INDICE](INDICE.md)

## Como usar

Consultar [MANUAL](MANUAL.md)


## Referências

As referências de todas as fontes citadas no projeto — as aulas, o livro do recorte, as
fontes da pesquisa e o material de fora (ver [Origem do conteúdo](#origem-do-conteúdo))
—, conforme a ABNT NBR 6023, ficam em `docs/REFERENCIAS.md`, gerado a partir de
[`dados/fontes.json`](dados/fontes.json).

---

*Este documento está licenciado sob [CC BY-NC-SA 4.0](LICENSE-CONTENT.txt). Ver
[NOTICE.md](NOTICE.md) para detalhes.*
