# Conferência das mensagens e proteção das fontes (opcional, pra quem usa o GitHub)

Você só precisa disto se guarda o projeto no [GitHub](../metodologia-de-conteudo.md). Quem
não usa o GitHub pode ignorar esta pasta.

## O que é

Pra mandar uma mudança ao GitHub, você grava uma versão do projeto no seu computador — o
[git](../scripts/README.md#protege_fontespy--confere-que-nenhuma-fonte-pode-ser-publicada)
chama cada versão gravada de <dfn>commit</dfn> — e escreve uma
mensagem dizendo o que mudou. Esta pasta traz três coisas que entram em ação nessa hora:

- **Uma proteção das fontes, do glossário e do índice** (o arquivo `pre-commit`): antes de
  aceitar a versão, ela roda o script `protege_fontes.py` e barra a versão que levar um
  arquivo da pasta protegida (a do material de base) ou uma cópia de uma fonte, mesmo com
  outro nome e em outra pasta. Assim, nenhum material de terceiros vai pro GitHub por
  engano. Depois, roda o `glossario.py --conferir`, que barra a versão enquanto o glossário
  não for o que os documentos definem, e o `confere_indice.py`, que barra a versão enquanto
  algum documento do projeto não estiver no índice uma vez só (ver o
  [README dos scripts](../scripts/README.md)).

As outras duas ajudam a escrever a mensagem sempre do mesmo jeito:

- **Um esqueleto da mensagem** (o arquivo `commit-template.txt`): quando você vai gravar
  uma versão, o editor já abre com o lugar do título e o lugar da explicação marcados,
  com as palavras `SUBSTITUA-...`, pra você escrever por cima.
- **Um verificador** (o arquivo `commit-msg`): antes de aceitar a versão, ele confere só
  a forma da mensagem — nunca se ela está certa ou bem escrita, que é julgamento de quem
  escreve. Ele recusa a mensagem que:
  - não tem título (a primeira linha está vazia);
  - tem um título que é um item de lista (`- corrigido X`, `1. corrigido X`...);
  - não tem uma linha em branco entre o título e a explicação;
  - explica em lista (`-`, `*`, `•`, `1.`, `2)`...) em vez de texto corrido;
  - ainda tem alguma palavra `SUBSTITUA-...` do esqueleto, ou seja, não foi escrita por
    cima dele.

## Como ativar

Esta pasta já está no projeto da sua disciplina, porque ele é uma cópia do modelo
inteiro. No GitHub, o projeto tem um <dfn>repositório</dfn> próprio, sem o histórico do modelo: o
lugar onde o GitHub guarda o projeto e o histórico das mudanças dele. Abra o
[terminal](../MANUAL.md#atualizando-o-baralho-depois-de-editar-as-planilhas) (o
[README dos scripts](../scripts/README.md) mostra como) dentro da pasta do projeto e
digite estas duas linhas, uma de cada vez, apertando Enter depois de cada uma:

    git config core.hooksPath .githooks
    git config commit.template .githooks/commit-template.txt

A primeira liga a proteção das fontes e o verificador; a segunda liga o esqueleto. A
partir daí, toda vez que você gravar uma versão, as fontes são conferidas, o esqueleto
aparece e a mensagem é conferida antes de a versão ser aceita. Isso vale só no seu
computador: quem copiar o projeto do GitHub pra outro computador precisa digitar as duas
linhas de novo lá. Se travar, peça ajuda à IA que você usa.

## Por que existe

Uma mensagem escrita como lista, um item por arquivo mudado, parece organizada numa
mudança pequena, mas não cresce bem: a cada mudança é preciso decidir de novo quanto
detalhe cabe, e o histórico fica sem um padrão. Título mais explicação em texto corrido
faz o histórico do projeto se ler como uma história.

O esqueleto guia quem escreve, mostrando a forma antes de qualquer texto existir; o
verificador recusa o que foge da forma depois de escrito. Nenhum dos dois garante que o
conteúdo está certo: uma frase cortada ao meio entre o título e a explicação ainda passa,
porque isso é sentido, não forma, e sentido nenhum programa confere sozinho. O que o
verificador confere é só o que dá pra conferir sem julgar: existe título, existe a linha
em branco, não tem lista, o esqueleto foi substituído.

---

*Este documento está licenciado sob [CC BY-NC-SA 4.0](../LICENSE-CONTENT.txt); a
proteção (`pre-commit`) e o verificador (`commit-msg`), que são programas, sob
[GPL-3.0](../LICENSE).*
