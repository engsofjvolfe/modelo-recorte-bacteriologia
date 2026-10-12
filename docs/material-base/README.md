# Material de base (nunca publicado)

Esta é a [pasta protegida](../../metodologia-de-conteudo.md#1-as-fontes-e-a-transcrição).
Ela guarda o material de base deste projeto (ver o [material de outras
pessoas](../../NOTICE.md)): em `pptx/`, as apresentações das aulas,
cada uma com a pasta das imagens dela ao lado; em `MURRAY-2022/`, a cópia do livro-texto
digital, com as imagens dele; e, na subpasta `fontes-externas/`, as cópias do material de
fora usado onde nem as aulas nem o livro-texto chegam (ver seção 4 da metodologia). Ela
nunca muda de nome nem de lugar: é assim que a lista do que nunca vai pro GitHub e os
scripts sabem sempre onde está o material de terceiros. É uma regra permanente, não uma
pendência a resolver depois (ver a seção 1 da
[metodologia](../../metodologia-de-conteudo.md#1-as-fontes-e-a-transcrição)):

- **Nada daqui é publicado nem repassado**, em lugar nenhum: esse material não é de quem
  mantém o projeto. Se você guarda o projeto no GitHub, a [lista do que nunca vai pro
  GitHub](../../NOTICE.md#como-o-projeto-trata-esse-material)
  já deixa de fora tudo o que está aqui dentro, menos este README.
- A referência de cada material — as aulas, o livro-texto, as fontes da pesquisa e o de
  fora — sai do arquivo de fontes (`dados/fontes.json`) e vai pra lista de referências
  (`docs/REFERENCIAS.md`), que podem ser publicados: o que fica de fora é a cópia, não a
  referência.
- A transcrição das aulas e do livro-texto, letra por letra, e a base de trechos do
  material de fora ficam em `gerados-ocr/` — são a base contra a qual se confere tudo o
  que se escreve, e também nunca são publicadas (ver as seções 1 e 4 da metodologia). Ali
  ficam também:
  - a análise de cada aula, trecho por trecho, na subpasta `analise/`, de onde saem as
    contagens da [análise da matéria](../analise-da-materia.md);
  - as [evidências da pesquisa](../../metodologia-de-conteudo.md#a-análise-da-matéria), na
    subpasta `pesquisa/`;
  - a base de cada item, `[item]-fontes-externas.md`;
  - a prova dos cartões de cada planilha, na subpasta `provas/` (ver seção 6 da
    metodologia);
  - os quatro arquivos de conferência, com as imagens deles na subpasta `imagens/`: o das
    transcrições contra a imagem de cada página, ou contra o texto e as imagens de um
    documento HTML ou de uma apresentação em pptx (`CONFERENCIA-COM-IMAGEM.md`, feito pelo
    script `conferencia.py`); o das referências contra a cópia de cada fonte
    (`CONFERENCIA-REFERENCIAS.md`, feito pelo `referencias.py`); o das frases do material
    de fora (`CONFERENCIA-TRECHOS.md`, feito pelo `base_externa.py`); e o dos cartões
    contra a prova deles (`CONFERENCIA-CARTOES.md`, feito pelo `confere_cartoes.py`). O
    [README dos scripts](../../scripts/README.md) diz como rodar cada um.
- Se uma fonte estiver em outro lugar, o script que a registra (o `registrar_fonte.py`,
  pras aulas) ou o da base do material de fora (o `base_externa.py`) pergunta se pode
  trazê-la pra cá; e o `protege_fontes.py` confere que nenhuma fonte registrada ficou de
  fora.
- Quem diz onde fica cada coisa dentro desta pasta é o [mapa do
  projeto](../../metodologia-de-conteudo.md).
- Antes de escrever qualquer coisa em `docs/material-gerado/`, leia este material
  inteiro, sem ferramenta que corte ou resuma automaticamente o texto (ver seção 5 da
  metodologia).

Este arquivo (`README.md`) é o único desta pasta que pode ser publicado — ele existe só
pra explicar como a pasta funciona, mesmo quando ela está vazia.

---

*Este documento está licenciado sob [CC BY-NC-SA 4.0](../../LICENSE-CONTENT.txt).*
