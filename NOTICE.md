# Avisos de licença

Este projeto usa duas [licenças](README.md#licença) diferentes, para dois tipos de arquivo
diferentes, mais uma exceção para o material de terceiros.

## 1. Programas — GPL-3.0

Os <dfn>scripts</dfn> deste projeto — programas pequenos que fazem sozinhos um trabalho
repetitivo, sempre do mesmo jeito, os arquivos `.py` da pasta [`scripts/`](scripts/) — e
os verificadores da pasta `.githooks/` (os arquivos [`pre-commit`](.githooks/pre-commit) e
[`commit-msg`](.githooks/commit-msg)) estão sob a GNU General Public License v3.0. Texto
completo em [`LICENSE`](LICENSE). Eles podem ser usados, estudados, mudados e repassados
livremente, mas qualquer versão mudada também precisa continuar sob a mesma licença,
aberta pra todo mundo, com o código dos programas disponível.

## 2. Conteúdo — CC BY-NC-SA 4.0

Tudo neste projeto que não é programa (item 1) nem material de terceiros (item 3) está
sob CC BY-NC-SA 4.0 — isso inclui os documentos de teoria, dicionário e ficha, as
planilhas de pergunta, a lista de referências (`docs/REFERENCIAS.md`), os arquivos de
dados e os documentos de apresentação. A regra vale por tipo de arquivo, não por uma lista
fechada: um arquivo novo do mesmo tipo já nasce coberto.

Texto completo em [`LICENSE-CONTENT.txt`](LICENSE-CONTENT.txt). Esse conteúdo pode ser
usado, adaptado e repassado, desde que se dê o crédito, não se use para fins comerciais,
e qualquer versão adaptada mantenha a mesma licença.

A tabela [`scripts/normas/simbolos.json`](scripts/normas/simbolos.json), que troca os
caracteres da fonte Symbol pelos do Unicode, foi feita a partir do arquivo *Adobe Symbol
Encoding to Unicode* (`VENDORS/ADOBE/symbol.txt`), publicado pelo Unicode Consortium
(Copyright © 1991-2011 Unicode, Inc.), que permite o uso livre das informações dele.

## 3. Material de terceiros — fora de qualquer licença deste projeto

Os arquivos em [`docs/material-base/`](docs/material-base/) — o material de aula, a
transcrição dele, as evidências da pesquisa, as cópias do material de fora em
`fontes-externas/`, a base de trechos do material de fora e a prova dos cartões — não são
cobertos por nenhuma das licenças acima. O material de base são as aulas da disciplina de
Microbiologia da Universidade Federal do Triângulo Mineiro, do Prof. Kennio Ferreira Paim,
e um recorte do livro *Microbiologia médica*, de Patrick R. Murray, Ken S. Rosenthal e
Michael A. Pfaller, publicado pela Guanabara Koogan, de que quem mantém o projeto não é
autor; ainda não há material de fora. Por isso:

- Esse material nunca é publicado nem repassado — fica só no computador de quem mantém o
  projeto. Se o projeto é guardado no GitHub, a <dfn>lista do que nunca vai pro
  GitHub</dfn> (o arquivo [.gitignore](.gitignore)) já deixa essa pasta de fora.
- Quem receber uma cópia deste projeto com essa pasta preenchida deve tratá-la como
  material pessoal de estudo, não como parte do que se pode repassar.

As referências desses materiais ficam em `docs/REFERENCIAS.md`, que é conteúdo deste
projeto e segue o item 2.

## Como dar o crédito

Ao reusar o conteúdo (item 2), escreva: "Núcleo de Microbiologia: bacteriologia,
licenciado sob CC BY-NC-SA 4.0", com o link para este projeto.

---

*Este documento está licenciado sob [CC BY-NC-SA 4.0](LICENSE-CONTENT.txt).*
