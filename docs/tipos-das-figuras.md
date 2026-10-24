# Tipos das figuras

O tipo de cada figura já olhada, sob o endereço dela. É um documento de achados: quem
precisa do tipo de uma figura busca o endereço dela e lê só a linha que a busca devolve,
sem abrir o documento. O que é um documento de achados está na [seção 8 da
metodologia](../metodologia-de-conteudo.md#8-os-documentos-e-os-arquivos-do-projeto); para
que serve o tipo de uma figura, em [O texto das
figuras](../metodologia-de-conteudo.md#o-texto-das-figuras).

O endereço de uma figura é o lugar pelo qual o trabalho chega a ela. Numa aula, é a aula e
o slide, escritos como no código de um trecho: a aula 9-10 e o slide 33 dão 9-10/33. Numa
fonte lida inteira, como um capítulo do livro, é o nome da transcrição sem o `.md`, como
chapter25. A busca se faz da pasta principal do projeto, com o endereço de cada lugar que
se tem, entre crases e entre aspas simples, numa opção `-e` cada, e se escreve sempre
assim, com os endereços no lugar dos pontos:

    grep -n -e '`...`' -e '`...`' docs/tipos-das-figuras.md

Cada linha que a busca devolve é uma figura daquele lugar, com o tipo dela. A figura que a
busca não devolve ainda não foi olhada: quem precisa dela a olha e escreve a linha dela no
fim da lista, no mesmo momento. Uma linha nunca se reescreve, e cada uma tem esta forma:

    - `<endereço>` <arquivo>: <tipo> (<dia>)

O endereço vai entre crases; o arquivo é o nome do arquivo da imagem, sem a pasta, como a
linha da imagem na transcrição o traz; o tipo é um dos cinco abaixo, escrito como está; e o
dia é o dia em que a figura foi olhada, como 2026-01-15. Os três primeiros tipos são os da
metodologia, cujo texto nunca é fonte:

- desenho com muitos elementos;
- tabela de dados ou gráfico;
- texto fora do estudo;
- texto que é fonte, para a figura com texto que não é de nenhum dos três;
- sem texto, para a figura que não tem texto nenhum.

## As figuras

- `3/18` image12.png: texto que é fonte (2026-10-24)
- `5/14` image9.jpeg: sem texto (2026-10-24)
- `5/16` image10.jpeg: sem texto (2026-10-24)
- `9-10/7` image2.jpeg: sem texto (2026-10-24)
- `9-10/8` image3.png: sem texto (2026-10-24)
- `9-10/8` image4.png: sem texto (2026-10-24)
- `9-10/9` image5.png: sem texto (2026-10-24)
- `9-10/19` image8.png: tabela de dados ou gráfico (2026-10-24)
- `9-10/32` image20.png: sem texto (2026-10-24)
- `9-10/33` image21.png: tabela de dados ou gráfico (2026-10-24)
- `9-10/34` image22.png: desenho com muitos elementos (2026-10-24)
- `9-10/35` image23.png: desenho com muitos elementos (2026-10-24)
- `9-10/63` image51.png: texto que é fonte (2026-10-24)
- `14/3` image1.png: texto que é fonte (2026-10-24)
- `15/6` image6.png: sem texto (2026-10-24)
- `15/20` image16.png: desenho com muitos elementos (2026-10-24)
- `chapter12` ch12.png: texto que é fonte (2026-10-24)
- `chapter12` fig12-1.png: desenho com muitos elementos (2026-10-24)
- `chapter12` fig12-2.png: desenho com muitos elementos (2026-10-24)
- `chapter12` fig12-3.png: desenho com muitos elementos (2026-10-24)
- `chapter12` fig12-4.png: desenho com muitos elementos (2026-10-24)
- `chapter12` fig12-5.png: desenho com muitos elementos (2026-10-24)
- `chapter12` fig12-6.png: desenho com muitos elementos (2026-10-24)
- `chapter12` fig12-7.png: desenho com muitos elementos (2026-10-24)
- `chapter12` fig12-8.png: desenho com muitos elementos (2026-10-24)
- `chapter12` fig12-9.png: desenho com muitos elementos (2026-10-24)
- `chapter12` fig12-10.png: texto fora do estudo (2026-10-24)
- `chapter12` fig12-11.png: desenho com muitos elementos (2026-10-24)
- `chapter13` ch13.png: texto que é fonte (2026-10-24)
- `chapter13` fig13-1.png: desenho com muitos elementos (2026-10-24)
- `chapter13` fig13-2.png: tabela de dados ou gráfico (2026-10-24)
- `chapter13` fig13-3.png: desenho com muitos elementos (2026-10-24)
- `chapter13` fig13-4.png: desenho com muitos elementos (2026-10-24)
- `chapter13` fig13-5.png: desenho com muitos elementos (2026-10-24)
- `chapter13` fig13-6.png: desenho com muitos elementos (2026-10-24)
- `chapter13` fig13-7.png: desenho com muitos elementos (2026-10-24)
- `chapter13` fig13-8.png: desenho com muitos elementos (2026-10-24)
- `chapter13` fig13-9.png: tabela de dados ou gráfico (2026-10-24)
- `chapter13` fig13-10.png: desenho com muitos elementos (2026-10-24)
- `chapter13` fig13-11.png: desenho com muitos elementos (2026-10-24)
- `chapter13` fig13-12.png: desenho com muitos elementos (2026-10-24)
- `chapter13` fig13-13.png: desenho com muitos elementos (2026-10-24)
- `chapter13` fig13-14.png: desenho com muitos elementos (2026-10-24)
- `chapter17` ch17.png: texto que é fonte (2026-10-24)
- `chapter17` fig17-1.png: desenho com muitos elementos (2026-10-24)
- `chapter25` ch25.png: texto que é fonte (2026-10-24)
- `chapter25` fig25-1.png: sem texto (2026-10-24)
- `chapter25` fig25-2.png: desenho com muitos elementos (2026-10-24)
- `chapter25` fig25-3.png: tabela de dados ou gráfico (2026-10-24)
- `chapter25` fig25-4.png: sem texto (2026-10-24)
- `chapter25` fig25-5.png: sem texto (2026-10-24)

---

*Este documento está licenciado sob [CC BY-NC-SA 4.0](../LICENSE-CONTENT.txt).*
