# Material de base

A [pasta protegida](../../metodologia-de-conteudo.md#1-as-fontes-e-a-transcrição): as
fontes do projeto e tudo o que traz texto delas. Nada daqui é publicado — de quem é esse
material e como o projeto o trata estão no [NOTICE](../../NOTICE.md) —, e este README é o
único arquivo da pasta que vai com o projeto.

| Pasta | O que guarda |
| --- | --- |
| `pptx/` | as apresentações das aulas, cada `.pptx` com a pasta das imagens dele ao lado |
| uma pasta por fonte, com a chave da referência dela, como `MURRAY-2022/` | a cópia da fonte; a do livro-texto, que o `transcrever_html.py` faz da captura, tem os documentos em `Text/`, as imagens em `Images/` e os estilos em `Styles/` |
| `fontes-externas/` | as cópias do [material de fora](../../metodologia-de-conteudo.md#o-material-de-fora) |
| `gerados-ocr/` | o que se gera das fontes, abaixo |

Em `gerados-ocr/`:

| O quê | O que é |
| --- | --- |
| uma transcrição por fonte, e uma por documento do livro | o texto da fonte, página por página, com o nome do arquivo dela: a da apresentação tem o nome do `.pptx`, e a do livro, o do documento (`chapter12.md` é o capítulo 12; `fm02.md`, o prefácio) |
| `extracao.json` | a lista de extração: as fontes que o `extrator.py` transcreve, cada uma com as opções, a numeração das páginas e as correções da leitura, que trazem texto da fonte |
| a lista dos itens numerados | os itens numerados das transcrições de documentos numerados, como uma norma, com a página e a linha de cada item e os grupos de tópicos do sumário |
| `CONFERENCIA-*.md` e `imagens/` | os [arquivos de conferência](../../metodologia-de-conteudo.md#7-a-conferência) e as imagens que eles mostram, e o relatório da conferência dos moldes |
| `pesquisa/` | as [evidências da pesquisa](../../metodologia-de-conteudo.md#a-análise-da-matéria) |
| `analise/` | a análise de cada aula e dos capítulos 12 a 17, trecho por trecho, as ligações entre as aulas e o registro do trabalho, `REGISTRO.md` |
| `provas/` | a [prova](../../metodologia-de-conteudo.md#6-os-cartões-e-o-baralho) dos cartões, um arquivo por planilha |
| `[item]-fontes-externas.md` | a [base de trechos](../../metodologia-de-conteudo.md#o-material-de-fora) de cada unidade, com o id dela no lugar de `[item]` |

Os scripts que gravam nesta pasta, e onde, estão no [README dos
scripts](../../scripts/README.md).

---

*Este documento está licenciado sob [CC BY-NC-SA 4.0](../../LICENSE-CONTENT.txt).*
