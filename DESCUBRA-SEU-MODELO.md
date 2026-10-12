# Descubra o formato da disciplina

Este documento traz as perguntas que decidem a parte do formato que pede uma grade fixa, e
a resposta deste projeto a cada uma. O formato nasce da análise da matéria (ver
`metodologia-de-conteudo.md`, seção 3): que tipos de conhecimento cada aula traz e que
forma de estudo serve a cada um. Dois desses tipos pedem uma grade: pra cada assunto que
se estuda um por um (os
[itens](metodologia-de-conteudo.md#analise-cada-parte-do-material)), o método monta dois
documentos, o [dicionário de gatilhos](MANUAL.md#nível-2--de-onde-isso-veio), dividido em
[elos](metodologia-de-conteudo.md#b-dicionário-de-gatilhos), e a [ficha
determinística](MANUAL.md#nível-2--de-onde-isso-veio), dividida em
[eixos](metodologia-de-conteudo.md#c-ficha-determinística). Os cartões de pergunta saem de
uma [planilha](MANUAL.md#atualizando-o-baralho-depois-de-editar-as-planilhas), com uma
coluna pra cada informação do cartão. Cada resposta abaixo aponta a parte da [análise da
matéria](docs/analise-da-materia.md) que a sustenta; é lá que está o porquê.

## Antes das perguntas: para quem é o material

O curso, a disciplina e o nível de estudo decidem o resto: o mesmo assunto pede itens,
eixos e profundidade diferentes em cursos e níveis diferentes.

**Neste projeto:** Microbiologia, no recorte de bacteriologia, pros cursos da área da
saúde que o [README](README.md#o-que-é-isto) nomeia. Como cada curso pede a matéria, e em
que nível, sai da pesquisa ([análise da matéria, parte
1](docs/analise-da-materia.md#1-a-pesquisa)); o que o estudante precisa saber fazer está
em [O que o estudante precisa saber
fazer](docs/analise-da-materia.md#o-que-o-estudante-precisa-saber-fazer).

## Perguntas para decidir o formato

1. **Existem itens que se repetem no material** — coisas que alguém aprende uma por
   uma? Se não existem, a disciplina não precisa de dicionário nem de ficha: o que ela
   traz vai pra teoria fundamental e pras formas de estudo que a análise escolheu.

   **Neste projeto:** sim, as bactérias e os itens de cada família dos fundamentos
   ([Os grupos](docs/analise-da-materia.md#4-os-grupos)). O resto vai pros outros
   documentos ([Os documentos](docs/analise-da-materia.md#os-documentos)).
2. **Se existem itens: quais fatos diferentes alguém precisa saber pra conhecer um item
   por completo?** Esses são os eixos da ficha. Se um eixo se divide em partes menores que
   todo item também tem, essas partes são os <dfn>subtópicos</dfn> dele.

   **Neste projeto:** os eixos da ficha de cada bactéria e os de cada família estão em
   [Os moldes](docs/analise-da-materia.md#os-moldes).
3. **Existe uma cadeia de causa e efeito natural conectando esses fatos**? Se sim,
   quantos passos ela tem, de verdade, no material?

   **Neste projeto:** sim, nas bactérias: os elos do dicionário estão em [Os
   moldes](docs/analise-da-materia.md#os-moldes).
4. **Que colunas uma pergunta de revisão sobre um item precisa?**

   **Neste projeto:** as do cartão em [Os moldes](docs/analise-da-materia.md#os-moldes),
   no parágrafo dos cartões.
5. **O material precisa de imagem, áudio ou outro anexo por item?**

   **Neste projeto:** de imagem, só nos cartões: dois campos, um na frente e um no verso,
   vazios até a pessoa pôr uma imagem; os documentos ensinam as figuras só em palavras
   ([A forma de cada tipo](docs/analise-da-materia.md#a-forma-de-cada-tipo), em Figura e
   esquema).

## Depois de responder

Grave as respostas no [arquivo de formato](metodologia-de-conteudo.md#grave-o-formato) da
disciplina, `dados/formato.json`. Copie
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
o projeto precisar de uma informação que o formato não tem, acrescente: o arquivo aceita
informações novas, e os scripts ignoram o que não conhecem. O campo novo segue a regra
dos modelos de `modelo-dados/` (metodologia, seção 14).

O script que monta os cartões do Anki (`montar_deck.py`) só exige duas colunas com nome
certo na planilha: uma chamada `pergunta` e outra `resposta`. A metodologia pede mais
uma em toda planilha, a `fonte`, com a citação de onde veio cada fato, que aparece atrás
do cartão, embaixo da resposta (seções 2 e 9 da metodologia). Qualquer outra coluna que
você criar vira parte do cartão automaticamente, com o nome que você escolheu; no Anki,
o nome aparece sem o sublinhado e com cada palavra em maiúscula (`tipo_pergunta` vira
`TipoPergunta`).

---

*Este documento está licenciado sob [CC BY-NC-SA 4.0](LICENSE-CONTENT.txt).*
