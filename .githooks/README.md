# Conferência das mensagens e proteção das fontes

O <dfn>git</dfn> é o programa que guarda as versões do projeto. Cada versão gravada é um
<dfn>commit</dfn>, com uma mensagem que diz o que mudou, e o projeto junto com o histórico
dos commits é o <dfn>repositório</dfn>. Esta pasta tem os <dfn>ganchos</dfn> do projeto:
programas que o git roda sozinho na hora de gravar um commit.

## O que é conferido

- **`pre-commit`**, antes de aceitar o commit, roda três scripts e barra o commit quando
  algum aponta um problema: o `protege_fontes.py --versao`, para que nenhum arquivo da
  pasta protegida nem cópia de uma fonte vá no commit; o `glossario.py --conferir`, para
  que o glossário seja o que os documentos definem; e o `confere_indice.py`, para que cada
  documento esteja no índice uma vez só. O que cada um confere está na seção dele no
  [README dos scripts](../scripts/README.md).
- **`commit-msg`** confere a forma da mensagem, nunca o sentido dela. Recusa a mensagem
  que:
  - não tem título (a primeira linha está vazia);
  - tem um título que é item de lista (`- corrigido X`, `1. corrigido X`);
  - não tem uma linha em branco entre o título e a explicação;
  - explica em lista (`-`, `*`, `•`, `1.`, `2)`) em vez de texto corrido;
  - ainda tem uma marca `SUBSTITUA-...` do esqueleto.

  A mensagem de um merge ou de um revert não é conferida.
- **`commit-template.txt`** é o esqueleto com que a mensagem abre no editor: o lugar do
  título e o da explicação, marcados com `SUBSTITUA-...`, e uma linha que lembra que a
  mensagem não põe a IA como coautora.

Título e explicação em texto corrido fazem o histórico se ler como uma história; uma
lista, um item por arquivo mudado, pede a cada commit uma decisão nova sobre quanto
detalhe cabe. O esqueleto mostra a forma antes de o texto existir, e o `commit-msg` recusa
o que foge dela depois de escrito. O sentido, nenhum dos dois confere: é de quem escreve.

## Por que a IA não é coautora

Algumas ferramentas de IA acrescentam à mensagem uma linha `Co-Authored-By:`, que põe a IA
como coautora do commit. Neste projeto, essa linha não entra. Pela Lei de Direitos
Autorais, "autor é a pessoa física criadora de obra literária, artística ou científica"
(Brasil, 1998b, art. 11), e "não se considera co-autor quem simplesmente auxiliou o autor
na produção da obra" (Brasil, 1998b, art. 15, § 1º); os scripts, que são programas, seguem
o mesmo regime (Brasil, 1998a, art. 2º). A IA não é pessoa: não é autora nem coautora de
nada aqui, nem titular dos direitos que as licenças do projeto repassam.

O que a IA fez não se esconde: o projeto diz como ela foi usada, em vez de pôr o nome dela
como autora. Quem responde pelo que está no projeto é a pessoa que o mantém, e quem lê
precisa saber que parte foi feita pela IA para saber o que conferir. A
[metodologia](../metodologia-de-conteudo.md#7-a-conferência) diz o que a IA faz e o que
fica sempre com a pessoa, e o [diário do projeto](../trabalhar-com-ia.md) conta, passo a
passo, como ela foi usada. As revistas médicas seguem o mesmo princípio: uma IA não entra
como autora de um artigo, porque não pode responder pela exatidão, pela integridade e pela
originalidade dele, e quem a usou diz como a usou (International Committee of Medical
Journal Editors, 2026).

## Como ativar

O git roda os ganchos desta pasta e abre o esqueleto no clone que tem estas duas
configurações, digitadas no
[terminal](../MANUAL.md#atualizando-o-baralho-depois-de-editar-as-planilhas), na pasta do
projeto:

    git config core.hooksPath .githooks
    git config commit.template .githooks/commit-template.txt

A configuração fica no clone, não vai com o projeto: um clone novo só confere os commits
depois dessas duas linhas.

## Referências

BRASIL. Lei nº 9.609, de 19 de fevereiro de 1998. Dispõe sobre a proteção da propriedade intelectual de programa de computador, sua comercialização no País, e dá outras providências. **Diário Oficial da União**, Brasília, DF, 20 fev. 1998. Disponível em: https://www.planalto.gov.br/ccivil_03/leis/l9609.htm. Acesso em: 12 out. 2026.

BRASIL. Lei nº 9.610, de 19 de fevereiro de 1998. Altera, atualiza e consolida a legislação sobre direitos autorais e dá outras providências. **Diário Oficial da União**, Brasília, DF, 20 fev. 1998. Disponível em: https://www.planalto.gov.br/ccivil_03/leis/l9610.htm. Acesso em: 12 out. 2026.

INTERNATIONAL COMMITTEE OF MEDICAL JOURNAL EDITORS. **Recommendations for the Conduct, Reporting, Editing, and Publication of Scholarly Work in Medical Journals**. [*S. l.*]: ICMJE, 2026. Disponível em: https://www.icmje.org/recommendations/browse/artificial-intelligence/ai-use-by-authors.html. Acesso em: 12 out. 2026.

---

*Este documento está licenciado sob [CC BY-NC-SA 4.0](../LICENSE-CONTENT.txt); os
ganchos (`pre-commit` e `commit-msg`), que são programas, sob [GPL-3.0](../LICENSE).*
