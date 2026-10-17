# Trabalhar com uma IA

O diário do projeto: os passos gerais que ele percorreu, com a ajuda de uma IA, na ordem em
que aconteceram. Não é regra — como o conteúdo se faz está na
[metodologia](metodologia-de-conteudo.md).

A IA trabalhou dentro do editor, lendo e escrevendo os arquivos do projeto e rodando os
scripts; em alguns passos, dividiu o trabalho entre agentes, um de cada vez. Em todos, ela
propôs, escreveu e conferiu primeiro, e quem mantém o projeto decidiu e conferiu por
último.

## 8 de outubro de 2026 — o projeto e o livro

- O projeto nasceu de um modelo de projetos de estudo, que virou este projeto no próprio
  lugar.
- O livro-texto só se lê num site. A IA escreveu o script que transcreve um documento em
  HTML a partir da captura que o navegador salva durante a leitura, e o que confere a
  transcrição contra a fonte. Os capítulos 12 a 17 foram os primeiros transcritos.

## 9 de outubro — as figuras, as aulas e o resto do livro

- A IA escreveu, figura por figura, o texto de dentro das 38 figuras dos capítulos 12 a 17,
  pelas regras do [Texto das figuras](docs/texto-das-figuras.md).
- A IA escreveu o script que transcreve apresentações em pptx. As 15 aulas e os capítulos
  18 a 35 foram transcritos, com o texto das figuras lido por OCR, e conferidos pelo script
  contra os arquivos.
- A metodologia passou a fazer o formato nascer de uma análise da matéria e de uma
  pesquisa.
- Cada aula foi analisada slide por slide, cada uma por um agente, um de cada vez, todos
  com o mesmo texto de instrução. Da aula 5 em diante, cada agente leu só a própria aula,
  para as análises não copiarem critérios umas das outras.

## 10 de outubro — as análises, as figuras e a pesquisa

- As análises ganharam os fatos do texto das figuras. O texto ilegível foi lido de novo
  pelo OCR, com a imagem ampliada e girada, e a leitura nova só ficou quando lia mais sem
  perder palavra; quem mantém o projeto conferiu palavras olhando as imagens.
- Um script conferiu os campos de todas as análises. Depois, cada ligação entre duas aulas
  foi conferida lendo os dois slides, e só ficou a que os dois mostram.
- A pesquisa: como a Fisioterapia e a Enfermagem pedem a matéria, o que a ciência da
  aprendizagem diz sobre como se estuda e o que o livro e os autores dizem da abordagem
  dele, com o trecho literal de cada ponto guardado nas evidências.
- Quem mantém o projeto respondeu às dúvidas das análises e pediu, como regra de extrema
  importância, que o material ensine, como um professor a quem nunca viu a matéria, e não
  só mostre.

## 11 de outubro — a análise da matéria, os moldes, o índice e o glossário

- A [análise da matéria](docs/analise-da-materia.md) foi escrita e montada por script a
  partir das partes: a pesquisa, as aulas, as ligações, os grupos, os caminhos e a forma de
  estudo.
- Os moldes de cada documento saíram de uma contagem, por script, do que as análises põem
  em cada documento. Quem mantém o projeto os aprovou, e um script confere que todo trecho
  das aulas tem lugar e nenhuma parte fica vazia.
- O índice virou a ordem de leitura do projeto, e o glossário passou a ser montado das
  definições marcadas nos documentos, cada um com um script que o confere.
- A análise da matéria foi reescrita para quem chega sem contexto.
- As ferramentas de trabalho que ficam fora do projeto ganharam uma descrição cada, numa
  prateleira à parte.

## 12 de outubro — a conferência das figuras e os documentos do projeto

- A conferência das transcrições passou a mostrar todas as imagens. Quem mantém o projeto
  conferiu o texto das 790 figuras olhando cada imagem e corrigindo ali mesmo, e um script
  levou as correções para as transcrições.
- Os documentos que vieram do modelo viraram documentos deste projeto: dizem como o
  projeto é, e o que só servia a quem começa um projeto pelo modelo saiu deles.

---

*Este documento está licenciado sob [CC BY-NC-SA 4.0](LICENSE-CONTENT.txt).*
