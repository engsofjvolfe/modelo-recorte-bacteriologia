# Descubra o formato da sua disciplina

Este documento ajuda a decidir a parte do formato de uma disciplina nova que pede uma
grade fixa. O formato nasce da análise da matéria (ver `metodologia-de-conteudo.md`, seção
3): que tipos de conhecimento cada parte do material traz e que forma de estudo serve a
cada um. Dois desses tipos pedem uma grade: pra cada assunto que se estuda um por um (os
*itens*), o método monta dois documentos: o
*dicionário*, que conta o item como uma história dividida em partes, os *elos*; e a
*ficha*, uma tabela direta com uma linha pra cada tipo de fato que todo item tem, os
*eixos*. Os cartões de pergunta saem de uma *planilha*, uma tabela com uma coluna pra
cada informação do cartão. Aqui você decide quantos elos o dicionário tem, quantos eixos
a ficha tem e que colunas a planilha precisa. Nenhum desses números é fornecido aqui —
cada disciplina responde essas perguntas pra si mesma, a partir do próprio material.

## O que é estável entre disciplinas

- Existe conteúdo que é teoria geral, sem ligação com um item específico — isso é
  sempre um documento próprio (ver `metodologia-de-conteudo.md`, seção 5A).
- Quando existe um item que se repete e que alguém precisa aprender individualmente,
  contar esse item de dois jeitos — uma história em cadeia, e uma tabela direta com os
  mesmos fatos — permite estudar de duas formas sem duplicar o trabalho de escrever.
- Os outros tipos de conhecimento que a análise da matéria acha ganham as formas de estudo
  que ela escolheu (ver `metodologia-de-conteudo.md`, seções 3 e 8).

O resto (quantos elos, quantos eixos, que nomes, se existem itens repetidos ou não) é
decisão de cada disciplina.

## Antes das perguntas: para quem é o material

Diga o curso, a disciplina e o nível de estudo de que você precisa (uma revisão pra
prova, uma base pra disciplinas seguintes, um aprofundamento). Tudo o que vem depois
depende disso: o mesmo assunto pede itens, eixos e profundidade diferentes em cursos e
níveis diferentes.

As perguntas abaixo se respondem com a análise da matéria na mão: é nela que estão a
pesquisa sobre como a matéria é estudada e cobrada nas áreas e o que cada parte do
material traz. A ementa ou o plano de ensino de uma oferta da disciplina mostra o que
aquela oferta cobre, não como a matéria é estudada nas áreas. Você pode responder com
ajuda de uma IA: passe a ela a análise da matéria e o material de aula e peça que proponha
cada resposta dizendo por que ela cabe, ou não cabe, nesse curso e nesse nível. A decisão
é sua; a justificativa fica na análise da matéria, e no arquivo de formato vai só a
resposta.

## Perguntas para decidir o formato

1. **Existem itens que se repetem no seu material** — coisas que alguém aprende uma por
   uma? Se não existem, sua disciplina não precisa de dicionário nem de ficha: o que ela
   traz vai pra teoria fundamental e pras formas de estudo que a análise escolheu.
2. **Se existem itens: quais fatos diferentes alguém precisa saber pra conhecer um item
   por completo?** Liste com suas próprias palavras, a partir do seu material — não a
   partir do que outra disciplina já usou. Esses são os eixos da ficha. Se um eixo se
   divide em partes menores que todo item também tem, liste essas partes: são os
   subtópicos dele.
3. **Existe uma cadeia de causa e efeito natural conectando esses fatos**? Se sim,
   quantos passos ela tem, de verdade, no seu material?
4. **Que colunas uma pergunta de revisão sobre um item precisa?** Escreva os nomes você
   mesmo, a partir do que o item efetivamente é.
5. **Seu material precisa de imagem, áudio ou outro anexo por item?** Se precisar, isso
   ainda não tem um formato pronto neste modelo — precisa ser desenhado.

## Depois de responder

Grave as respostas no arquivo de formato da disciplina, `dados/formato.json`. É um
arquivo de texto com as respostas organizadas de um jeito que os scripts (os pequenos
programas do modelo) conseguem ler. Copie
[`modelo-dados/formato.json`](modelo-dados/formato.json) pra lá e preencha. Ele vem só
com o nome de cada informação, entre aspas, e, depois dos dois-pontos, o lugar da
resposta: aspas vazias, `""`, esperam um texto, escrito entre elas; colchetes vazios,
`[]`, esperam uma lista. Não mude os nomes. O que já vem preenchido fica como está: o
`versao_schema`, a versão do molde que o arquivo segue, e o `idioma`, que só muda se o
material for escrito em outro idioma. O arquivo guarda só as respostas — nomes e listas,
sem explicação — e cada informação dele responde a uma pergunta:

| Informação | Pergunta |
|---|---|
| `itens` | 1 (lista vazia, se não houver itens) |
| `eixos` e os `subtopicos` de cada eixo | 2 (lista vazia de subtópicos, se o eixo não se dividir) |
| `elos` | 3 (lista vazia, se não houver cadeia) |
| `colunas_extras` | 4 (só as que vão além de `pergunta`, `resposta` e `fonte`) |
| `curso`, `disciplina` e `nivel` | *Antes das perguntas* |
| `idioma` | o idioma do material gerado: já vem `pt-BR`, o português do Brasil |

Cada item, elo, eixo e subtópico entra na lista dele entre chaves, `{ }`, com um `id`, um
código curto, e um `nome`; um eixo tem também a lista `subtopicos`. Uma vírgula separa
cada informação da seguinte e cada entrada da seguinte. O id vai entre aspas, mesmo
quando é um número. Os elos e os eixos são numerados na ordem, `"1"`, `"2"`...; um
subtópico leva o número do eixo, um ponto e o número dele, `"1.1"`, `"1.2"`. Assim nenhum
id se repete na grade, e é pelo id que o arquivo de base de cada item marca a cobertura
de cada subtópico. O id do item aparece no nome dos arquivos dele. Cada coluna extra é
só o nome dela, entre aspas.

Um exemplo inventado, com dois itens, dois elos e dois eixos, o primeiro dividido em dois
subtópicos e o segundo sem divisão:

```json
{
  "versao_schema": 1,
  "curso": "Curso de Exemplo",
  "disciplina": "Disciplina de Exemplo",
  "nivel": "revisão para a prova",
  "idioma": "pt-BR",
  "itens": [
    { "id": "A1", "nome": "Primeiro item" },
    { "id": "A2", "nome": "Segundo item" }
  ],
  "elos": [
    { "id": "1", "nome": "Primeiro elo" },
    { "id": "2", "nome": "Segundo elo" }
  ],
  "eixos": [
    {
      "id": "1",
      "nome": "Primeiro eixo",
      "subtopicos": [
        { "id": "1.1", "nome": "Primeira parte do primeiro eixo" },
        { "id": "1.2", "nome": "Segunda parte do primeiro eixo" }
      ]
    },
    { "id": "2", "nome": "Segundo eixo", "subtopicos": [] }
  ],
  "colunas_extras": ["item", "tipo_pergunta"]
}
```

Depois, confira se o arquivo ficou bem preenchido com o script `validar_dados.py`: o
[README dos scripts](scripts/README.md) diz, passo a passo, como rodar. É desse arquivo
que sai a grade do que cada item precisa ter, antes de qualquer material ser escrito. Se
a sua disciplina precisar de uma informação que o formato ainda não tem, acrescente: o
arquivo aceita informações novas, e os scripts ignoram o que não conhecem. Registre a
mudança na metodologia (seção 17), pra que o formato cresça no modelo também.

O script que monta os cartões do Anki (`montar_deck.py`) só exige duas colunas com nome
certo na planilha: uma chamada `pergunta` e outra `resposta`. A metodologia pede mais
uma em toda planilha, a `fonte`, com a citação de onde veio cada fato, que aparece atrás
do cartão, embaixo da resposta (seções 2 e 9 da metodologia). Qualquer outra coluna que
você criar vira parte do cartão automaticamente, com o nome que você escolheu; no Anki,
o nome aparece sem o sublinhado e com cada palavra em maiúscula (`tipo_pergunta` vira
`TipoPergunta`).

---

*Este documento está licenciado sob [CC BY-NC-SA 4.0](LICENSE-CONTENT.txt).*
