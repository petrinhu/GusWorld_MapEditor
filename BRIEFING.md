# BRIEFING.md

> Este documento não é o briefing original. O briefing original era um texto em prosa corrida, escrito pelo líder em 28 itens soltos, na ordem em que ele foi lembrando das coisas. Ele **foi purgado do repositório e do histórico do git** por conter um caminho absoluto da máquina do líder e uma referência pessoal, num projeto que vai ser publicado. Por autorização expressa do líder ("você pode reformatar/refatorar esse documento se quiser, até reordenar as ações e acrescentar ações"), este arquivo o substitui: é o **mapa do que foi decidido e do que falta**, reorganizado em ordem lógica, com o caminho local removido e a referência pessoal reduzida aos apelidos que o líder liberou como públicos.
>
> **As leis finais não vivem aqui.** Vivem em [`GODS_LAWS.md`](GODS_LAWS.md), conforme ordem direta do líder. Este documento aponta para cada lei quando ela existe, mas não a repete por inteiro nem a substitui.

## Legenda de estado

| Estado | Significado |
|---|---|
| **Lei (L-XX)** | Virou lei em `GODS_LAWS.md`. O número aponta para a lei. |
| **Decidido, não implementado** | O líder decidiu, mas o código ou artefato ainda não existe. |
| **Aguardando decisão do líder** | Segue em aberto, não é decisão de agente. |
| **Aguardando terceiro (GlintFx / GusWorld)** | Depende de resposta de outro projeto pelo bus. |
| **Não tocado** | Item de pesquisa ou inspiração que ainda não foi trabalhado. |
| **Nota** | Item que o líder deixou em branco de propósito no documento original (ver item 13 abaixo). Não é perda de conteúdo. |

## Pendências visíveis (não enterrar)

Dois itens do briefing original seguem sem decisão e precisam continuar visíveis:

1. **Qual é o papel formal do editor na visão do GlintFx** (item 1 original). A pergunta foi feita a eles; a resposta ainda não chegou.
2. **O mecanismo de proteção contra edição de mapas e saves** (item 25 original: hash, criptografia ou equivalente). Depende de discussão com GlintFx e com GusWorld. O único fato conhecido hoje é um alerta herdado da `gusmap-core` aposentada (L-08): o selo HMAC dela usava uma chave derivada de um literal aberto no fonte do jogo, ou seja, não protegia contra ninguém. Isso é um alerta de o que não fazer, não uma solução.

---

## 1. Governança

Leis, como se pergunta ao líder, quem executa o quê, rigor de teste.

| Item original | O que foi pedido | Estado | Onde vive a decisão |
|---|---|---|---|
| 11 | "main apenas orquestra, interage comigo e dispara agentes. Auditorias apenas com clevel bigtech fable, trabalhadores sonnet bigtech" | Lei (L-06) | `GODS_LAWS.md` L-06 |
| 13 | O líder avisa que bullets sem texto no documento original são propositais, resultado de edição dele, e não devem ser lidos como perda de conteúdo. | Nota | Aplicado neste próprio documento, nos itens 14, 21, 26 e 27 |
| 15 | "veja como glintfx faz os testes dele e auditorias no código etc, aqui deve ser idêntico mas adaptado ao nosso projeto, só que mantendo o mesmo rigor. Tem md na raiz do cwd que explica isso (agile, contract, outros)" | Lei (L-09) | `GODS_LAWS.md` L-09; manuais de referência em `AGILE.md`, `CONTRACT.md`, `TESTES.md` na raiz do repositório |
| 16 | "obrigatoriamente use AskUserQuestion ao me trazer perguntas ou precisar algo de mim" | Lei (L-05) | `GODS_LAWS.md` L-05 |
| 17 | Existência do arquivo `GODS_LAWS.md`, apontado em `CLAUDE.md`, com a intenção de registrar leis inquebráveis do projeto para não esquecê-las; havia um exemplo preenchido no GlintFx para se inspirar. | Decidido e implementado | `GODS_LAWS.md` (arquivo inteiro) e `CLAUDE.md` (protocolo de uso) |
| 18 | "já tentei fazer esse editor uma vez com o claude, mas tive vários problemas e estou fazendo DO ZERO tudo com relação ao código, sempre assentado sobre GlintFx" | Lei (L-11) | `GODS_LAWS.md` L-11 |
| 20 | "essas instruções não devem ser consideradas suficientes, vamos conversar exaustivamente sobre tudo. Preciso de fundação sólida para não ter problemas no futuro." | Cumprido pela conversa que gerou L-01 a L-14; segue valendo como princípio para decisões futuras | As 14 leis de `GODS_LAWS.md` são o produto direto desta conversa |
| 23 | "podemos alterar os arquivos do cwd de contratos e orientações em geral, para ficar adequado a este projeto" | Autorizado; execução em andamento (fora do escopo deste documento) | `CONTRACT.md`, `AGILE.md`, `TESTES.md`, `DEPLOY_CHECKLIST.md`, `AUDITORIAS.md`, `Standards.md`, `TOOLING.md` na raiz do repositório |
| 24 | "você pode reformatar/refatorar esse documento se quiser, até reordenar as ações e acrescentar ações. Mas as leis finais decididas ficam em GODS_LAWS" | Implementado | Este próprio documento é o resultado dessa autorização |
| 28 | "uso web autorizado" | Autorizado e em uso | Referenciado em L-13 ("veja na web como fazer essa sincronia") e nas pesquisas ainda pendentes dos itens 4 e 5 abaixo |

## 2. Fronteiras externas

Só GlintFx; o formato de mapa é deles; Wayland ou X11 é problema deles; o bus.

| Item original | O que foi pedido | Estado | Onde vive a decisão |
|---|---|---|---|
| 1 | "editor de mapas do ecossistema GusWorld / GlintFx. Pergunte seu papel a @GlintFx" | Aguardando terceiro (GlintFx) | Pergunta feita pelo bus; ver "Pendências visíveis" acima |
| 2 | "aceita apenas link com framework GlintFx em ../Glintfx e [github]/petrinhu/GlintFx e com o SO. Vamos discutir possíveis exceções se vc sugerir. Você NUNCA cria workarounds nem passa por cima da camada de GlintFx. Se ainda não existir a função em GlintFx, registre a necessidade no bus e espere parado a resposta dele. Se existir outra fatia ou onda que possa avançar enquanto a pendência é realizada, avise" | Lei (L-01) | `GODS_LAWS.md` L-01 |
| 8 | "não importa se wayland ou x11, o intermediário é GlintFx" | Lei (L-01, aplicação) | `GODS_LAWS.md` L-01, parágrafo de aplicação |
| 12 | Comunicação com Gus Dragon (handle público `Dragon-Drv`), com GlintFx, com o site de registro histórico do jogo e com o editor de mapas, por um bus assíncrono hospedado no repositório público `gusworld_ia_autocomm` (github.com/petrinhu/gusworld_ia_autocomm), que traz as instruções de uso. Gus Dragon fala pelo bus via issues ou discussions; os pedidos dele devem ser lidos e incorporados ao projeto. | Parcialmente lei; parcialmente decidido, não implementado | O aviso ao GlintFx sobre qualquer toque em mapa virou lei (L-02, `GODS_LAWS.md`); a leitura e incorporação sistemática dos pedidos de Gus Dragon via issues/discussions ainda não tem processo implementado |
| Lei adicional, sem item numerado correspondente | Decisão de que a `gusmap-core` (biblioteca que antes era dona do formato `.gmap`) está aposentada, surgida durante a conversa exaustiva do item 20 | Lei (L-08) | `GODS_LAWS.md` L-08 |
| 25 | "os saves e mapas do jogo devem ter mecanismo de proteção contra edição (hash, cripto etc): discutir com @GlintFx e @GusWorld" | Aguardando decisão do líder e de terceiros (GlintFx e GusWorld) | Ver "Pendências visíveis" acima |

## 3. Produto

O que o editor faz, WYSIWYG, tipos de volume, undo/redo, abas.

| Item original | O que foi pedido | Estado | Onde vive a decisão |
|---|---|---|---|
| 4 | "inspirado em outros editores de mapas, a melhor referência é warcraft II, mas busque outros na web. WYSIWYG, salva em matriz x,y, pergunte a @GlintFx" | Parcial: a matriz x,y é o formato do GlintFx (lei L-03); o desenho WYSIWYG da tela espera o GlintFx ter janela (lei L-14, item 4). A pesquisa de outros editores além de Warcraft II não foi feita. | `GODS_LAWS.md` L-03 e L-14; pesquisa comparativa ainda não tocada |
| 5 | "menu de edição de rotação, aumento e redução do objeto, edição de hitbox (todos os tipos: de parede/bloqueio, de execução de ação, etc, busque na web)" | Parcial: os seis tipos de volume de colisão viraram lei (L-14, item 1). O menu de rotação e redimensionamento do objeto ainda não foi decidido. | `GODS_LAWS.md` L-14 (tipos de volume); menu de transformação do objeto aguardando decisão do líder |
| 7 | "quero undo e redo, com vários passos, veja na web como fazer essa sincronia" | Lei (L-13) | `GODS_LAWS.md` L-13 |
| Lei adicional, sem item numerado correspondente | Decisão de abrir vários mapas em abas simultâneas, cada uma com câmera própria, e de manter um histórico único compartilhado entre elas, surgida durante a conversa exaustiva do item 20 | Lei (L-14, item 2) | `GODS_LAWS.md` L-14, item 2 |
| Lei adicional, sem item numerado correspondente | Modelo de mapa como uma camada de terreno pintada na grade mais objetos posicionados livremente por cima, sem camadas de pintura sobrepostas nesta versão | Lei (L-14, item 3) | `GODS_LAWS.md` L-14, item 3 |

## 4. Arquitetura

Camadas, átomos com POCO próprio, proibido monolito.

| Item original | O que foi pedido | Estado | Onde vive a decisão |
|---|---|---|---|
| 3 | "vamos discutir as camadas: hexagonal? espinha? Sugira. PROIBIDO monolitos. OS itens/cartas e demais elementos do jogo devem ser atomos com POCO proprio!" | Lei (L-12), com uma ambiguidade não resolvida por mim | `GODS_LAWS.md` L-12 |

**Ambiguidade registrada, não resolvida:** o item original cita "itens/cartas e demais elementos do jogo" como exemplo do que deveria ser átomo com POCO próprio. A lei L-04, decidida depois, tirou carta, item e NPC do escopo deste editor (só mapa é editado aqui). O princípio arquitetural de átomos com POCO próprio permanece de pé e virou lei (L-12), mas o exemplo original (itens/cartas) não é mais um objeto que este editor edita. Não decidi por conta própria se isso invalida a frase ou se ela só deixou de se aplicar a este repositório; registro a divergência para o líder resolver se quiser.

## 5. Distribuição

Licença, repositório, CI.

| Item original | O que foi pedido | Estado | Onde vive a decisão |
|---|---|---|---|
| 6 | "será usado para distribuição, conjuntamente com GlintFx, FOSS. vamos discutir a licença" | Lei (L-07) | `GODS_LAWS.md` L-07 |
| 9 | "repo: petrinhu/GusWorld_MapEditor" | Decidido, implementado | Repositório existe sob esse caminho na organização; licença sendo adicionada nesta mesma onda de trabalho |
| 10 | "CI com runners Fedora 44 (principal), Ubuntu, Arch, CachyOs (original, não arch renomeado), windows" | Lei (L-10) | `GODS_LAWS.md` L-10 |

## 6. Planejamento

Tabela de pendências.

| Item original | O que foi pedido | Estado | Onde vive a decisão |
|---|---|---|---|
| 19 | "crie a tabela de pendencias no final, com wsjf por bullets no cabeçalho" | Decidido, não implementado | `TODO.md` ainda não existe neste repositório |
| 22 | "a tabela de pendências (TODO.md) deverá ser revista depois de feita e adaptada ao que for decidido aqui no projeto. O projeto não se adapta a tabela, ela é ferramenta, então a lista deve ser revista e adaptada." | Regra de processo registrada; não executável ainda porque depende do item 19 | Aplica-se assim que `TODO.md` for criado |

## Itens deixados em branco pelo líder

Os itens 14, 21, 26 e 27 do documento original não tinham texto. O próprio líder avisou, no item 13, que isso é resultado de edição dele e não deve ser lido como conteúdo perdido. Preservados aqui como nota, não como lacuna a preencher.
