> **LEI DAS LEIS, ANTERIOR ATÉ À LEI ZERO: só o líder pode quebrar uma lei deste arquivo** — agente nenhum quebra, flexibiliza, reinterpreta ou "adapta ao caso" por conta própria — **e nem a ordem direta dele dispensa a confirmação**: antes de executar, nomeie a lei que está sendo quebrada, cite o texto dela, diga o que ela protege e o que se perde ao quebrá-la, e pergunte por `AskUserQuestion` se é isso mesmo que ele quer; **quando o pedido for ALTERAR ou REVOGAR uma lei, argumente CONTRA primeiro, sempre e sem exceção**, com razões concretas, o problema que a lei existe para impedir, os trade-offs da mudança e o que fica desprotegido depois dela, e só então leve a escolha por `AskUserQuestion` entre **confirmar** a alteração e **cancelá-la**; pressa, obviedade aparente, "ele já mandou uma vez" e aprovação dada em outro contexto **nunca** substituem essa confirmação, e silêncio jamais vale como aval. (Ordem do líder, 22/08/2026.)

# GODS_LAWS.md

> Ordens expressas do líder (petrus). Este arquivo **não é declaração, é execução**: cada lei tem um **gatilho**, e o gatilho é conferido **no momento da ação**, não no fim.

## Protocolo de uso (obrigatório)

1. **Antes de agir**, varra a coluna "Gatilho" da tabela abaixo. Se algum gatilho casa com o que você está prestes a fazer, leia a lei inteira antes do primeiro comando, não depois.
2. **Ao despachar subagent**, cole no prompt da task o texto completo das leis cujo gatilho casa com aquela task, mais o caminho absoluto deste arquivo. Subagent **não herda** este contexto e não vai ler por conta própria.
3. **Ao relatar ao líder**, se você tocou uma área com lei, diga qual lei aplicou e como. Silêncio não é prova de conformidade.
4. **Lei nova entra aqui no instante em que o líder a dá**, com data e o texto dele verbatim entre aspas. Não espere "um momento melhor" para registrar.
5. **Nenhum agente revoga, flexibiliza ou reinterpreta lei.** Só o líder. Na dúvida sobre o alcance de uma lei, pergunte via `AskUserQuestion` antes de agir.
6. Conflito entre uma lei daqui e qualquer outro documento (manual, memória, hábito, preferência do agente): **a lei daqui vence**.

## Índice de gatilhos

| Lei | Gatilho: dispara quando você vai... | Resumo |
|---|---|---|
| [L-01](#l-01) | escrever qualquer linha que toque janela, entrada, desenho ou som | Só a API pública do GlintFx. Nunca contornar, nunca terceiro, nunca o SO |
| [L-02](#l-02) | tocar em mapa, em qualquer sentido | Avisar o GlintFx do que foi feito; inalcançável, mandar pelo bus |
| [L-03](#l-03) | pensar em formato de arquivo de mapa | O formato é do GlintFx. Somos consumidores, não autores dele |
| [L-04](#l-04) | decidir o que o editor edita | Só mapa. Carta, item e NPC estão fora |
| [L-05](#l-05) | precisar de algo do líder, ou ter mais de uma opção | `AskUserQuestion`, sem `preview`, recomendada primeiro |
| [L-06](#l-06) | executar qualquer trabalho de produto ou código | O main orquestra e não implementa. Auditoria com C-level fable, execução com sonnet |
| [L-07](#l-07) | criar arquivo de licença, ou publicar o repositório | AGPL-3.0-or-later, a mesma do GlintFx |
| [L-08](#l-08) | procurar onde mora o domínio de mapa compartilhado | A `gusmap-core` está aposentada. Não é base, não é referência |
| [L-09](#l-09) | escrever teste, portão de CI ou auditoria | Mesmo rigor do GlintFx, adaptado ao nosso projeto |
| [L-10](#l-10) | mexer em CI | Cinco alvos: Fedora 44 primário, Ubuntu, Arch, CachyOS, Windows |
| [L-11](#l-11) | procurar como o editor anterior fazia alguma coisa | O projeto é do zero. O editor anterior não é base nem referência |
| [L-12](#l-12) | criar diretório, decidir onde um tipo mora, ou incluir header | Camadas horizontais finas; o GlintFx só na casca externa; regra fiscalizada por portão de CI |
| [L-13](#l-13) | escrever qualquer operação de edição, ou mexer em histórico | Comando com pilha linear, transação por gesto, seleção fora, histórico persistido em arquivo próprio |
| [L-14](#l-14) | decidir o que entra na primeira versão do editor | Seis tipos de volume, vários mapas em abas, uma camada de terreno mais objetos livres |
| [L-15](#l-15) | escrever memória, nota ou documento sobre algo que deixou de valer | Apagar. Nunca registrar que está parado, aposentado ou inativo |
| [L-16](#l-16) | pensar no papel do editor, ou desenhar qualquer capacidade dele | Implementador de referência do escritor, e utilizável headless |
| [L-17](#l-17) | ir executar qualquer trabalho de produto | Main só orquestra; C-level fable audita e cria; sonnet implementa; commit ao fim de cada fatia; push ao fim de cada onda só se o GHA fechar verde, se todos os testes verdes. |
| [L-18](#l-18) | o líder aprovar, rejeitar ou mudar algo, ou fechar item de alta prioridade | Avisar o Gus Dragon sem ele perguntar |
| [L-19](#l-19) | criar classe ou caso de uso, acrescentar método ou responsabilidade a unidade existente, ou revisar fatia | Proibido monolito: uma razão de mudar por unidade. Regra qualitativa, julgada na revisão adversarial pelas cinco perguntas |

---

## L-01

**Data:** 14/08/2026, reafirmada em 21/08/2026. **Verbatim (maiúsculas do líder):** *"NAO USE RMLUI NEM SDL3!!!!"*, e em 21/08: *"aceita apenas link com framework GlintFx em ../Glintfx e [github]/petrinhu/GlintFx e com o SO. Você NUNCA cria workarounds nem passa por cima da camada de GlintFx."*

Toda interação com janela, entrada, desenho, som e recurso passa **exclusivamente** pela API pública do GlintFx. É proibido incluir header ou linkar biblioteca de terceiro (RmlUi, SDL, GLFW, Qt, o que for) e é proibido falar direto com o sistema operacional.

**Aplicação, e é a parte que se esquece:** se a função não existe no GlintFx, **não invente contorno**. Registre a necessidade no bus e **espere parado**. Se houver outra fatia ou onda que possa avançar enquanto a pendência corre, avise o líder. Wayland ou X11 não é problema nosso: o intermediário é o GlintFx.

## L-02

**Data:** 22/08/2026. **Verbatim:** *"sempre que tocar em mapa, avise o que fez a @GlintFx e se ele estiver inalcancavel, mande via bus"*.

**Toda vez** que este projeto tocar em mapa — ler, gravar, desenhar, alterar estrutura, decidir algo sobre o assunto, ou descobrir um fato que mude o entendimento — o GlintFx é avisado **do que foi feito**, não do que se pretende fazer.

**Aplicação:** o canal preferencial é a sessão viva do GlintFx (mensagem direta entre sessões). **Se ela estiver inalcançável, a mensagem vai pelo bus** (`gusworld_ia_autocomm`, `inbox/glintfx/`), que é assíncrono e não depende de a outra sessão estar aberta. Nunca "deixar para avisar depois": o aviso é parte do ato de tocar em mapa, não uma tarefa separada. Isto existe porque o GlintFx é dono do formato (L-03) e não pode descobrir por acaso o que o consumidor fez com o contrato dele.

## L-03

**Data:** 21/08/2026, decorrente da lei **L-30 do GlintFx**, aceita pelo líder e comunicada por eles pelo bus.

**O GlintFx é dono do formato de arquivo de mapa.** Matriz `x,y`, objetos posicionados nela, hitbox, colisão, parede, porta e ponto de teleporte como marcador genérico com destino, mais busca de caminho e visibilidade. A lib publica **leitor e escritor**, os dois públicos.

**O `gusworld_mapeditor` deixa de definir o formato e passa a gravá-lo**, como qualquer consumidor no mundo. Necessidade nossa **não vira campo por decisão nossa**: vira pedido, descrito em palavras, julgado por eles.

**Convenção de extensão da casa, ampliada em 24/08/2026:** todo formato próprio do ecossistema usa `.gw.<tipo>`. Verbatim do líder, relatado pela sessão do `gusworld`: *"`.gw.text` e mantenha o padrão de `.gw.[tipo]` para nossos formatos próprios"*. **Consequência para nós: o arquivo de projeto do editor (`FMT-5`), que é formato genuinamente nosso, segue essa convenção** e não pode ser batizado fora dela.

**A distinção que o caso expôs, e que vale para todo tipo futuro: EXTENSÃO NÃO É FORMATO.** O nome do arquivo diz de quem é a etiqueta; não diz quem desenhou o conteúdo. A armadilha que isto existe para impedir é alguém ver `.gw.` num nome, concluir que o formato é nosso, e sentir-se livre para mudá-lo. Documentado também do lado do `gusworld`, em `docs/tech/convencao-formatos-gw.md`.

**Extensão do arquivo, decidida pelo líder em 24/08/2026: `.gw.map`.** Verbatim: *"nossos os mapas terão formato proprio em .gw.map"*, esclarecido por ele em seguida como sendo **só a extensão**. **Os bytes continuam sendo o formato do GlintFx, byte a byte.** A extensão é identidade do GusWorld no nome do arquivo, não formato próprio: nada nesta lei muda, o editor segue gravando no formato deles, e o papel de implementador de referência da L-16 segue de pé. Registrado com esta redundância de propósito, porque a frase original **lida sozinha soa como revogação desta lei**, e o orquestrador chegou a montar o argumento contra antes de perguntar. Quem reler daqui a um ano lê a resposta junto.

**Aplicação:** é proibido criar formato concorrente, camada de tradução, ou "formato do editor que depois converte". Se o editor precisa gravar algo que o formato deles não carrega (histórico, nota de autor, camada de trabalho), isso vai em **arquivo ao lado**, nunca dentro do formato de mapa — regra declarada por eles e aceita aqui.

**Proteção contra edição, decidida em 22/08/2026 via `AskUserQuestion`, depois da discussão com o GlintFx que o líder mandou fazer: DETECTAR no mapa, PROTEGER no save.** O formato do GlintFx carrega selo **aberto** de integridade, que qualquer um verifica e o editor sabe gerar, cobrindo corrupção, truncamento e edição acidental. A proteção de verdade mora no **save do jogador**, que é arquivo do GusWorld e não do formato de mapa. A razão: **editar mapa num jogo que distribui editor é uso legítimo; trapaça é editar o save.** Fica registrado o fato que sustentou a decisão, porque ele vale além deste item: em projeto com o fonte publicado, **detectar** alteração é alcançável e **impedir** não é. É proibido desenhar mecanismo que prometa impedir.

**Consequência de fronteira que caiu no nosso colo (22/08/2026):** o formato aceita só forma simples. **Repartir polígono côncavo em pedaços convexos na hora de salvar é trabalho do editor**, não da lib — decisão do líder, com a justificativa de que quem tem interface é quem tem como fazer isso direito. Repartição convexa é classe de código que produz defeito silencioso (vértice colinear, orientação invertida, polígono degenerado): nasce com teste de ida e volta e com verificação de que cada pedaço gerado é de fato convexo.

## L-04

**Data:** 21/08/2026, via `AskUserQuestion`.

**O editor edita SÓ MAPA:** grade de células, objetos posicionados, hitbox, portas e pontos de teleporte. **Carta, item e NPC do jogo estão fora do escopo** — são conteúdo do GusWorld, não do mapa.

**Aplicação:** proposta de "aproveitar que o editor já abre arquivo" para editar catálogo de conteúdo é violação desta lei, e vira pergunta ao líder, nunca decisão de agente.

## L-05

**Data:** 21/08/2026. **Verbatim:** *"obrigatoriamente use AskUserQuestion ao me trazer perguntas ou precisar algo de mim"*.

Toda pergunta ao líder e toda decisão com mais de um caminho vai por `AskUserQuestion`. **Nunca usar o campo `preview`** — o líder não quer o painel lateral; detalhe técnico vai no corpo da mensagem, com as opções curtas. A opção recomendada vem primeiro, marcada como recomendação.

**Aplicação:** decisão de design, arquitetura, escopo, stack ou qualquer coisa cara de reverter **nunca** é tomada por agente. Diante de dúvida, pergunte antes de agir, não depois de implementar.

## L-06

**Data:** 21/08/2026. **Verbatim:** *"main apenas orquestra, interage comigo e dispara agentes. Auditorias apenas com clevel bigtech fable, trabalhadores sonnet bigtech"*.

O main **não implementa produto nem código**: orquestra, conversa com o líder e despacha agentes. **Auditoria é feita por C-level da constelação bigtech em modelo fable**; execução é feita por agents operacionais em modelo sonnet.

**Aplicação:** implementador, revisor e orquestrador são **três agentes diferentes**. Relatório de agente não é prova: o main reconfere build limpo e faz spot-check das afirmações contra arquivo e linha antes de aceitar.

## L-07

**Data:** 21/08/2026, via `AskUserQuestion`, dentro do item *"será usado para distribuição, conjuntamente com GlintFx, FOSS"*.

**Licença: AGPL-3.0-or-later**, a mesma do GlintFx — ecossistema sob licença única, sem atrito de compatibilidade.

**Aplicação:** o repositório `petrinhu/GusWorld_MapEditor` está **privado e sem licença** neste momento. Publicar sem o arquivo de licença no lugar é violação. Cabeçalho SPDX em todo arquivo de código, como o GlintFx faz.

## L-08

**Data:** 21/08/2026, via `AskUserQuestion`.

A biblioteca **`gusmap-core` está aposentada**. Ela era dona do formato `.gmap` (esquema v3, selo HMAC) e perdeu a razão de existir com a L-03.

**Aplicação:** não é base, não é referência, não é "o que já funcionava". Não clonar, não copiar trecho, não citar o desenho dela como argumento. O achado técnico que sobrevive dela é um **aviso**, não um projeto: a chave do selo HMAC era derivada de um literal aberto no fonte do jogo, ou seja, o selo não protegia contra ninguém.

## L-09

**Data:** 21/08/2026. **Verbatim:** *"veja como glintfx faz os testes dele e auditorias no codigo etc, aqui deve ser identico mas adaptado ao nosso projeto, só que mantendo o mesmo rigor"*.

O rigor de teste, portão de CI e auditoria é **o mesmo do GlintFx**, adaptado ao nosso domínio — nunca relaxado por sermos menores.

**Aplicação, com um defeito real já herdado deles:** um portão que **varre zero arquivos e imprime verde** passa nos dois autotestes de praxe (o positivo, que planta violação, e o negativo, que prova que entrada limpa sai zero), porque ambos rodam sobre arquivos que existem. "Olhei e está limpo" e "não olhei nada" produzem a mesma saída. **Todo portão nosso declara quantos arquivos varreu, e sair com zero varridos é falha, não sucesso.**

**Framework de teste: HARNESS PRÓPRIO, decidido em 22/08/2026 via `AskUserQuestion`.** Nada de Catch2 nem de qualquer biblioteca de teste de terceiro. A lente de engenharia achou a colisão: o `TESTES.md` recomendava Catch2, e a **L-01 proíbe biblioteca de terceiro**; framework de teste é biblioteca de terceiro linkada no binário. O GlintFx resolveu o mesmo problema escrevendo harness próprio, e o deles é referência legítima de como fazer. O líder recusou tanto o Catch2 quanto a saída de abrir exceção declarada na lei, e a razão de recusar a exceção é a que importa: **"terceiro que não conta" é como dependência volta a entrar num projeto que a expulsou.**

**Desenho do teste, decidido pelo líder em 24/08/2026, e as três peças são porta de mão única.**

**1. Prefixo e namespace do harness: `GUSMAP_` e `gusmap::test`.** É `Gus` mais `map`, homenagem ao Gus Dragon, e aparece em toda linha de asserção do projeto para sempre. Trocar depois de trezentos testes escritos é reescrever a asserção de todos.

**2. Teste baseado em propriedade com gerador PRÓPRIO, nunca da biblioteca padrão.** O padrão da linguagem especifica o motor (`mt19937` dá a mesma sequência crua em qualquer lugar) mas **não especifica as distribuições**, que são a conta que transforma o número cru em valor. Consequência medida: mesma semente, mesmo código, **casos de teste diferentes no Fedora e no Windows**, e a receita de reprodução impressa na falha não reproduz nada. Isso mataria a reprodutibilidade exatamente nos cinco alvos da L-10. O gerador é escrito em casa, de algoritmo publicado, e nasce com teste de valores dourados que falha na hora se alguma plataforma divergir.

**3. Semente fixa no CI, exploração à parte, e toda descoberta vira caso fixo.** Três regras que andam juntas:

- **No CI, semente fixa.** Determinístico, reproduzível, e **nunca instável**. Teste que falha por sorteio bloquearia push sob a L-17 sem defeito nenhum no código, e pior, ensinaria a reexecutar vermelho sem ler, que é o hábito que a L-09 inteira existe para combater.
- **Num job separado de exploração**, que roda por fora e **não bloqueia push**, semente do relógio **impressa no log**. É ele que varre território novo, e resolve a fraqueza real da semente fixa, que é testar sempre os mesmos casos.
- **Falha achada pela exploração vira caso FIXO no CI**, com a semente dela. O bug encontrado nunca mais volta sem ser notado, e a descoberta vira proteção permanente em vez de sumir na execução seguinte.

**4. Redução automática do contraexemplo (shrinking) entra junto**, não fica para depois: quando uma propriedade falha, a ferramenta encolhe o caso até o menor que ainda quebra. Depurar repartição de polígono com quarenta vértices é outra coisa que depurar com quatro.

**Refinamento decidido pelo líder em 22/08/2026, com a tensão à vista.** A regra acima, aplicada ao pé da letra num projeto que ainda não tem código, deixaria o CI **vermelho por meses** — e vermelho crônico treina todo mundo a ignorar vermelho, que é a mesma doença por outro caminho. A distinção que resolve está entre duas frases: *"olhei e está limpo"* quando não se olhou nada é **mentira**, e foi ela que derrubou o portão do GlintFx; *"não há nada para olhar ainda, e eu declaro isso"* é **verdade**.

Portanto: **enquanto NENHUMA das pastas de camada existir** (`domain`, `application`, `platform`), o portão **sai zero**, declarando que varreu zero e que não há alvo — e é **proibido** imprimir "OK", "limpo" ou "nenhuma violação" nesse caminho, porque isso seria afirmar verificação que não houve. **No instante em que QUALQUER uma das três pastas passar a existir, varrer zero volta a ser FALHA**, e a trava fecha sozinha, sem ninguém precisar virar uma chave.

**A trava não vale sem prova:** o autoteste de cada portão exercita as **duas** direções (sem pasta e zero arquivos sai zero; com pasta existindo, ainda que vazia, e zero arquivos sai falha). Guarda não exercitada é onde mora o defeito silencioso, e este guarda nasceu justamente para cobrir um buraco que dois controles não pegavam.

## L-10

**Data:** 21/08/2026. **Verbatim:** *"CI com runners Fedora 44 (principal), Ubuntu, Arch, CachyOs (original, não arch renomeado), windows"*.

Cinco alvos, **cinco entradas distintas** na matriz de CI. **Fedora 44 é o primário**, por ser o sistema do líder, e fica pinado na versão, nunca em `latest`. **CachyOS não é Arch renomeado** e não é coberto pelo job de Arch.

## L-11

**Data:** 21/08/2026. **Verbatim:** *"ja tentei fazer esse editor uma vez com o claude, mas tive vários problemas e estou fazendo DO ZERO tudo com relacao ao codigo, sempre assentado sobre GlintFx"*.

O código deste projeto **nasce do zero**. O editor anterior — que chegou a ter janela, grade, inspetor, `Document` e undo/redo — **não é base, não é referência, não é canon**.

**Aplicação:** ao encontrar rastro do predecessor (memória de sessão anterior, tag antiga, descrição de arquitetura passada), **pare a escavação e siga do zero**. Necessidade descrita em palavras é insumo legítimo; "copia o que já estava lá" não é. Esta lei espelha a L-01 do GlintFx e existe pela mesma razão.

## L-12

**Data:** 22/08/2026, via `AskUserQuestion`, sobre a ordem original *"vamos discutir as camadas: hexagonal? espinha? Sugira. PROIBIDO monolitos."*

**Camadas horizontais finas**, com a dependência apontando só para dentro:

1. **Domínio** — POCO puro. Documento de mapa, célula, objeto posicionado, hitbox, porta, teleporte, seleção, comando, pilha de histórico. **Zero GlintFx, zero sistema operacional, zero terceiro.**
2. **Aplicação** — um caso de uso por operação de edição, cada um pequeno e testável sozinho. Nunca um serviço-deus com dezenas de métodos.
3. **Casca de plataforma** — fina, **única camada autorizada a incluir header do GlintFx**, que chama a API deles **direto, sem interface própria**.

**Por que sem interface:** o GlintFx é a única implementação que vai existir, por lei; e a API de janela, desenho e entrada **ainda não existe** — desenhar uma porta hoje é supor a forma dela. Isso produziria exatamente a "camada de tradução" já proibida no ecossistema.

**Aplicação:** a proteção do domínio **não** vem de interface, vem de **regra de dependência fiscalizada por portão de CI** — `domain` nunca inclui `application` nem `platform`; `application` nunca inclui header do GlintFx. O portão declara quantos arquivos varreu (L-09). Se um dia houver razão **concreta** (não hipotética) para fingir a fronteira em teste, a saída é um `concept` de C++23 resolvido em compilação, nunca interface virtual.

**Nomes dos diretórios, decididos em 22/08/2026 via `AskUserQuestion`: `domain/`, `application/`, `platform/`, em INGLÊS.** É o que o portão de CI já procura, é coerente com a lei do GlintFx que exige identificador em inglês, e evita acento em caminho de arquivo no alvo Windows. A prosa dos manuais e as mensagens de commit continuam em português.

**"Átomos com POCO próprio"** (ordem do líder) se materializa no domínio e nos casos de uso, onde se paga sozinho. **Não** se aplica à casca de plataforma: exigir um átomo por campo de formulário num editor de usuário único é over-engineering. Átomo é sobre tamanho e responsabilidade, não sobre indireção — um POCO concreto de vinte linhas, sem interface nenhuma, é um átomo perfeito.

**Ambiguidade RESOLVIDA em 22/08/2026 pelo líder. Verbatim:** *"a regra de atomicidade aqui vale para o que o editor de fato modela: célula, objeto, volume, comando"*.

O briefing original citava *"os itens/cartas e demais elementos do jogo"* como exemplo do que deveria ser átomo com POCO próprio, e a L-04 depois tirou carta, item e NPC do escopo. Não há contradição: **o princípio não mudou, mudou a lista de coisas a que ele se aplica.** Neste repositório os átomos são **célula, objeto, volume e comando**. Carta e item continuam sendo átomos com POCO próprio onde são modelados, que é o GusWorld, não aqui.

## L-13

**Data:** 22/08/2026, via `AskUserQuestion`, sobre a ordem original *"quero undo e redo, com varios passos, veja na web como fazer essa sincronia"*.

**Comando com pilha linear.** Cada operação de edição é um comando pequeno, **serializável**, com desfazer próprio. Nada de instantâneo do mapa inteiro por passo, nada de árvore de histórico.

Quatro regras que vêm com a lei:

1. **Uma intenção é um passo de desfazer.** Arrastar o pincel por quarenta células é **um** passo, agrupado por **transação explícita** que abre no início do gesto e fecha no fim — não por heurística de "parece a mesma ação".
2. **A seleção fica FORA do histórico.** Desfazer só volta mudança de conteúdo do mapa; seleção e câmera são estado de sessão. Decisão do líder, apoiada na reclamação pública contra o comportamento oposto no Figma.
3. **O histórico PERSISTE entre sessões**, decisão do líder contra o padrão universal da indústria (Krita, Photoshop e Qt não persistem). Ele mora em **arquivo do editor ao lado do mapa** (L-03), nunca dentro do formato do GlintFx. **Três consequências assumidas:** cada comando precisa de serialização versionada; o arquivo de histórico grava uma impressão digital do mapa e **recusa reaplicar** se o mapa mudou por fora; e tudo isso depende do identificador estável de objeto. **Dependência RESOLVIDA em 22/08/2026:** o líder decidiu, do lado do GlintFx, que cada objeto do mapa carrega um **UUID gravado no arquivo, que não é a posição na lista serializada e nunca é reutilizado depois que o objeto é apagado**. O histórico persistente sobrevive e é seguro desenhar em cima dele.
4. **As vistas assinam os sinais do histórico e nunca guardam cópia própria do estado.** Painel com caminho de atualização paralelo diverge do histórico exatamente no caso de seleção múltipla — defeito documentado por quem já construiu editor de nível.

## L-14

**Data:** 22/08/2026, via `AskUserQuestion`. Fecha o escopo funcional da primeira versão, dentro do escopo geral da L-04 (só mapa).

**1. Seis tipos de volume de colisão**, e só estes, escolhidos por serem os que um mapa em grade visto de cima realmente usa:

| Tipo | O que faz |
|---|---|
| Sólido | Bloqueia movimento |
| Gatilho de ação | Avisa sem bloquear |
| Zona de dano | Aplica dano por permanência ou contato |
| Zona de terreno modificador | Altera movimento ou estado (água, lama, gelo) |
| Área de interação | Habilita ação contextual, tipicamente maior que o desenho |
| Obstáculo de navegação | Bloqueia a busca de caminho da IA, independente de bloquear movimento |

**Ficaram de fora, e o motivo importa:** hitbox e hurtbox de combate (só fazem sentido em jogo de luta), zona de câmera e zona de áudio. Não são proibidos para sempre; estão fora **desta** versão.

**Dois dos seis dependem de decisão pendente do CTO do GlintFx** — o bit de "bloqueia ou só notifica", que sustenta o gatilho de ação, e a separação entre bloquear movimento e bloquear busca de caminho, que sustenta o obstáculo de navegação. Fato registrado, não cobrança: quem classifica fila é quem recebe.

**2. Vários mapas abertos ao mesmo tempo, em abas**, cada um com câmera própria. A razão é concreta: o mundo do GusWorld tem treze áreas mais interiores e dungeons ligadas por teleporte, e ligar um portão ao destino em outro mapa exige ver os dois lados. Com um mapa por vez, o autor edita de memória.

**Histórico com abas, decidido em 22/08/2026 via `AskUserQuestion`: um histórico SÓ, compartilhado pelo editor inteiro**, não um por aba. A razão é a ligação entre mapas: com treze áreas mais interiores e dungeons ligadas por teleporte, ligar um portão ao destino no outro mapa é caso central, e com histórico por aba desfazer no mapa A deixaria a metade gravada no mapa B, produzindo teleporte apontando para lugar nenhum sem o autor perceber. **Mitigação obrigatória do incômodo que isso traz:** quando um passo de desfazer ou refazer alterar um mapa que não é o da aba ativa, **o editor troca a aba para o mapa afetado**, de modo que o autor sempre veja o que mudou. Desfazer que altera algo invisível é a única coisa que esta decisão tinha de ruim, e ela fica coberta.

**3. Uma camada de terreno pintada na grade, mais objetos posicionados livremente por cima** em coordenada contínua. **Não** há camadas de pintura sobrepostas nesta versão. Escolhido também por ser exatamente o modelo que a L-30 do GlintFx já descreve, sem depender de decisão nova deles.

**Aplicação:** propor camada de pintura sobreposta, tipo de volume fora dos seis, ou edição de conteúdo que não seja mapa é violação desta lei somada à L-04, e vira pergunta ao líder, nunca decisão de agente.

**4. O desenho da tela (o WYSIWYG do item 4 do briefing) ESPERA o GlintFx ter janela.** Decisão do líder em 22/08/2026, contra a minha recomendação de desenhar agora. Consequência assumida e registrada para ninguém reabrir por engano: enquanto a tela não for desenhada, **nós não temos a lista de recursos de interface a pedir ao GlintFx**, então o pedido sob demanda que eles esperam de nós nessa frente fica parado até lá. Não é esquecimento; é ordem.

## L-15

**Data:** 22/08/2026. **Verbatim:** *"nao comente nada com parado/aposentado/inativo... apague! você vai se confundir depois"*.

Quando algo deixa de valer (biblioteca descontinuada, decisão revogada, bloqueio resolvido, arquivo purgado, frente abandonada), o registro dele **é apagado**. É proibido escrever memória, nota ou seção dizendo *"X está aposentado"*, *"Y está pausado"*, *"Z não vale mais"*.

**A razão, e ela é mecânica, não estética:** nota de obituário continua **injetando o nome no contexto**. Semanas depois se lê "gusmap-core (aposentada)" e o que fica é `gusmap-core`, tratado como peça viva do projeto. **A negação evapora antes do substantivo.** Memória é contexto carregado a cada sessão, não arquivo histórico: o histórico é do **git** e dos documentos versionados, que registram o que mudou, quando e em qual commit, com data e autor.

**Como aplicar sem perder o que importa:** se o que morreu deixou uma **lição que continua valendo**, a lição vira registro próprio, escrita como **regra no presente e sem citar o cadáver**. Exemplo real deste projeto: um formato antigo tinha selo criptográfico cuja chave estava escrita às claras no código-fonte, e não protegia ninguém. O que ficou foi a regra ("em projeto com fonte publicado, detectar alteração é alcançável, impedir não é"), não a memória do formato que morreu.

**Vale também dentro de documento vivo:** em vez de manter um parágrafo dizendo *"o mecanismo descrito acima não existe mais"*, **apague o parágrafo**. Ressalva de obituário é obituário.

**Fronteira, para a lei não ser lida como ordem de apagar história:** esta lei governa **memória e nota de contexto**, não o registro versionado. Uma lei revogada **permanece** neste arquivo com a revogação declarada (o líder é a única autoridade que revoga, e a rastreabilidade da ordem dele é o ponto do arquivo); o `BRIEFING.md` continua registrando o estado de cada item; e mensagem de commit continua narrando o que foi removido e por quê. O que se apaga é o que seria **recarregado como se fosse presente**.

## L-16

**Data:** 22/08/2026, via `AskUserQuestion`. **Texto do líder:** *"opcao 1 e você também deve poder ser usado headless"*.

**O papel do editor perante o GlintFx é o de IMPLEMENTADOR DE REFERÊNCIA DO ESCRITOR.** Não somos consumidor comum: somos quem exercita o formato de verdade e realimenta o GlintFx, de forma estruturada, com o que dói. Isso não é honraria, é obrigação de reporte: achado de formato vira mensagem descrita em palavras, com o uso concreto que a justifica, e não vira contorno silencioso do nosso lado.

**E o editor tem de ser utilizável HEADLESS**, sem janela. As duas metades desta lei são uma só coisa, e a segunda é o que torna a primeira verificável: **um editor que só existe com janela não pode exercitar o formato no CI dos cinco alvos**, e portanto não pode ser implementador de referência de nada. Headless é o que permite abrir, validar, transformar e gravar mapa dentro de um portão automático, em cada plataforma, a cada commit.

**Consequência de arquitetura, e ela reforça a L-12 em vez de mexer nela:** a fronteira entre a **aplicação** e a **casca de plataforma** deixa de ser boa prática e passa a ser requisito de produto. Toda capacidade de edição tem de existir e ser exercível **abaixo** da casca; a casca desenha e recebe entrada, e nada mais. Se uma operação só puder ser feita clicando, ela está no lugar errado.

**Consequência de sequenciamento:** o modo headless depende do formato (o leitor e o escritor do GlintFx), **não** da janela. Ele é uma frente que anda assim que o formato existir, muito antes de existir interface, e é o caminho mais curto entre este projeto e um editor que faz algo útil de verdade.

## L-17

**Data:** 22/08/2026, decisão do líder, com a linha de gatilho revista por ele em 23/08/2026. **Texto dele, verbatim, na linha de gatilho do índice:** *"Main só orquestra; C-level fable audita e cria; sonnet implementa; commit ao fim de cada fatia; push ao fim de cada onda só se o GHA fechar verde, se todos os testes verdes."*

> **Nota de correção, registrada porque o erro foi do tipo mais grave que este arquivo comporta.** A primeira versão deste corpo citava como verbatim do líder uma frase com um **terceiro portão** (revisão de um agente de QA) que ele **removeu** da linha de gatilho enquanto o corpo estava sendo escrito. O corpo foi alinhado ao texto atual dele em 23/08/2026. **Atribuir verbatim ao líder o que ele não escreveu é pior que deixar a lei sem corpo**, porque a citação falsa se propaga como se fosse ordem. Causa mecânica, para não repetir: o orquestrador rodou `git add` no arquivo inteiro e engoliu a edição do líder junto com a própria escrita. **Antes de commitar arquivo que o líder também edita, confira `git diff --cached` linha a linha.**

**Quem faz o quê:**

- **O main só orquestra.** Não implementa produto nem código: conversa com o líder, despacha agentes e verifica o que volta.
- **C-level em fable audita E CRIA.** Não é só o papel de auditor: planejamento e criação de escopo também são dele, no modelo fable.
- **Sonnet implementa.** A execução é de agente operacional.

**Cadência, e ela tem duas velocidades diferentes de propósito:**

- **Commit ao fim de cada FATIA.** Barato e frequente. Tira o trabalho da zona de risco antes de a fatia seguinte começar.
- **Push ao fim de cada ONDA.** Caro e raro, e **só passa se os DOIS portões fecharem verde**, sem exceção e sem "está quase":
  1. **O GitHub Actions fechou verde.**
  2. **Todos os testes verdes.**

**Os dois são conjuntivos.** Um verde e um vermelho não é push adiado por pouco: é push proibido.

**Alcance, decidido pelo líder em 23/08/2026: os dois portões valem para TODO push, sem distinção de tipo de commit.** Não existe categoria de commit que não conte, pela mesma razão pela qual ele recusou abrir categoria de dependência que não conta: **"terceiro que não conta" é como a regra volta a vazar.** E o custo de obedecer é zero num commit de documentação, porque os dois portões são mecânicos e medidos pelo mesmo pipeline que roda de qualquer forma.

**Relação com a L-06:** esta lei **não substitui** a L-06, **refina**. A L-06 fixa quem faz o quê; a L-17 acrescenta a cadência e os dois portões de push, e acrescenta o "cria" ao papel do C-level em fable. Onde as duas falarem do mesmo assunto, valem juntas. **A regra de que implementador, revisor e orquestrador são agentes diferentes continua sendo da L-06**, e não desta lei.

**Aplicação:** antes de todo push, diga em qual estado está cada um dos dois portões. **Silêncio sobre um deles conta como vermelho**, pela mesma razão do protocolo deste arquivo: silêncio não é prova de conformidade.

## L-18

**Data:** 23/08/2026, decisão do líder. Lei espelhada do GlintFx (lá é a L-37) e do GusWorld (lá é a L-31), pela mesma ordem dele: **avisar o Gus Dragon é obrigação permanente, não detalhe de protocolo de bus** — por isso é lei própria, e não um parágrafo dentro da lei do bus.

**O pedido, dele, na issue 8 do bus, verbatim:** *"nao precisa dizer algo so quando falo, pode falar quando por exemplo @petrinhu atualiza algo, ou por exemplo quando ele aprova/rejeita/muda algo das minhas ideias"*. Ele endereçou **a todos**, e é por isso que a lei vale nos três projetos.

**O escopo veio do próprio Gus Dragon**, consultado pelo líder em 23/08/2026: ele é avisado, **sem precisar perguntar**, sobre **(a) tudo que é ideia DELE** — quando o líder aprova, rejeita ou muda — **e (b) o que for de alta prioridade dos projetos**, pela régua de WSJF que a tabela de pendências já usa.

**O que isto NÃO é:** um fluxo de aviso sobre toda decisão técnica. O corte por prioridade existe justamente para que o que interessa a ele não se afogue no que não interessa.

**O limite honesto, que se diz a ele em vez de prometer o impossível:** sessão não é serviço rodando. Aviso proativo só sai enquanto alguém está com a sessão aberta; decisão tomada com tudo fechado chega depois. **Ele prefere a verdade a promessa de aviso instantâneo.**

**Nota de descumprimento, registrada porque é a causa do pedido:** o `PROTOCOL.md` do bus **já obrigava** a "Resposta 2" automática — o resultado da decisão do líder vai a ele sem reaprovação de texto. **Ele não deveria ter precisado pedir.** Se pediu, a resposta automática não estava saindo em algum dos quatro canais, e vale conferir se alguma ideia dele ficou sem retorno.

**Formato, quando a resposta for na discussion 7** (o catálogo de bugs que ele mantém): timestamp, uma das três classificações que ele fixou (**Bug Consertado**, **Bug Funcional**, **Bug Possível**) e itens numerados entre parênteses. Ele tem 11 anos, programa, usa Manjaro e git — **o que ele não merece é resposta vaga**, e "não existe código disso ainda" é melhor resposta que estimativa inventada.

## L-19

**Data:** 24/08/2026, via `AskUserQuestion`. Promove a lei em vigor a ordem original que a L-12 cita desde 22/08/2026 e que nunca tinha virado regra no corpo de lei nenhuma: *"PROIBIDO monolitos."*

**Por que esta lei existe como lei própria:** a frase aparecia uma única vez neste arquivo, dentro das aspas do cabeçalho da L-12, sem gatilho, sem aplicação e sem forma de alguém violar e ser pego. Ordem citada não é ordem em vigor. É a mesma família de defeito que a L-09 registra no portão que varre zero e imprime verde: a promessa existe, a verificação não. Esta lei transforma a citação em regra com gatilho e com lugar no processo.

**Decisão do líder, 24/08/2026: a regra é QUALITATIVA.** Ele recusou explicitamente fixar número (linhas por arquivo, métodos por classe) com portão de CI que mede e falha. A lei descreve o que é monolito neste projeto e a fiscalização mora na **revisão adversarial**, não em portão automático. Custo declarado na pergunta e assumido por ele: sem número, a lei depende do revisor reconhecer o monolito, e casos parecidos podem sair julgados diferente. As cinco perguntas abaixo existem para encolher esse espaço de julgamento, não para eliminá-lo.

### O que é monolito NESTE projeto

Monolito não é arquivo grande: é uma unidade (classe, caso de uso, arquivo) que acumula **razões diferentes de mudar**. E neste projeto as razões de mudar já estão catalogadas, porque as leis as fixaram: o formato do mapa é do GlintFx (L-03), o histórico tem regras próprias (L-13), a lista de volumes é fechada (L-14), a API de plataforma é a do GlintFx (L-01), a repartição convexa é nossa (L-03). A régua concreta:

> **Se mudanças vindas de leis DIFERENTES e não relacionadas obrigam a editar a MESMA unidade, ela está virando monolito.**

### Onde o monolito vai nascer aqui, e por que cada lugar é atraente

Monolito nunca nasce por burrice; nasce por conveniência local que parece razoável no dia. Os lugares de risco deste editor, com a conveniência nomeada:

| Lugar de risco | Como nasce | Por que parece razoável |
|---|---|---|
| **Documento de mapa** (o agregado do domínio) | O documento agrega célula, objeto posicionado e volume, e por isso todo comportamento novo "cabe nele": serializar, validar, repartir polígono, aplicar comando, tudo vira método do documento | "O dado já está aqui, é um método a mais" |
| **Pilha de histórico** | Em vez de cada comando saber aplicar e desfazer a si mesmo (L-13), a pilha vira despachante com um `switch` por tipo de comando, ganhando um caso por operação | A serialização dos comandos (L-13) pede um registro central, e o registro tenta virar dono da execução |
| **Camada de aplicação** | O serviço-deus que a L-12 já proíbe por nome: um `EditorService` onde cada operação de edição nova é "só mais um método" ao lado dos irmãos | Descobribilidade: "está tudo num lugar só" |
| **Casca de plataforma** | A isenção de atomização da L-12 lida como licença: um `EditorApp` que roteia entrada E troca ferramenta E gerencia abas E decide regra de negócio | Os callbacks do GlintFx chegam todos no mesmo lugar |
| **Caminho de gravação** | Escritor + repartição convexa + selo de integridade + arquivo de histórico ao lado, tudo numa classe só | "Para o usuário, salvar é um gesto só" |
| **Modo headless (L-16)** | Um runner de linha de comando que acumula subcomandos e lógica própria até virar um segundo editor | "É só a CLI, não é o produto" |

### As cinco perguntas do revisor

"Isto é monolito?" ninguém sabe responder. As perguntas abaixo, sim, e cada uma se responde **olhando o código**, não opinando:

1. **A pergunta das leis.** Quais leis obrigariam esta unidade a mudar (L-01 API, L-03 formato, L-13 histórico, L-14 escopo)? Responde-se lendo os includes e os métodos públicos. Uma lei: unidade sã. Duas ou mais, não relacionadas: monolito em formação.
2. **A frase sem "e".** O CONTRACT.md §3 já fixa o teste: descreva a unidade numa frase; se precisar de "e" ligando verbos de natureza diferente ("aplica movimento E persiste E valida geometria"), reprova. A frase escrita entra no relatório de revisão.
3. **O teste monta o mundo?** Para exercitar UM comportamento da unidade, o arrange do teste precisa de documento aberto, histórico vivo e abas montadas? Átomo de domínio se constrói sozinho, com os próprios campos. Responde-se lendo o arrange dos testes da fatia. (É a L-16 dita de outro jeito: capacidade que só é exercível com o mundo montado está no lugar errado.)
4. **O que entra pelo include?** O header da unidade puxa grupos que não conversam entre si (grade + serialização + histórico)? A lista de includes é a lista de dependências, e se lê em dez segundos.
5. **Quem paga a próxima feature?** No diff da fatia (`git log --stat`), a operação nova tocou quais arquivos? Se toda operação nova aterrissa no mesmo arquivo (mais um método, mais um caso de `switch`), esse arquivo é o monolito nascendo. É a pergunta mais objetiva das cinco: responde-se com o diff, não com julgamento.

### Sinais precoces

Esta lei nasce com o projeto em 923 linhas e o maior arquivo em 237. Monolito de 3000 linhas todo mundo vê; a lei existe para reconhecê-lo com 300:

- **O mesmo arquivo aparece no diff de todas as fatias.** É o sinal mais barato de medir e o mais confiável.
- **Construtor, ou fixture de teste, ganhando parâmetro a cada fatia.** A unidade está precisando de cada vez mais mundo para existir.
- **`switch` sobre tipo de comando, volume ou ferramenta que ganha um caso por feature.** O desenho da L-13 é o oposto disso: cada comando sabe aplicar e desfazer a si mesmo.
- **Nome sem substantivo de domínio:** `Manager`, `Service`, `Helper`, `Utils`, `Core`. Célula, comando, volume e porta têm nome próprio; a unidade que não consegue dizer o que é, é porque faz de tudo.
- **Um `utils.hpp` acumulando funções soltas** sem razão comum de mudar (o CONTRACT.md §6.7 já proíbe o helper genérico antes da terceira ocorrência real).
- **A frase "é só mais um método" aparecendo como justificativa na revisão.** Essa frase é o som do monolito crescendo: verdadeira em cada passo individual, falsa na soma.

### O que esta lei NÃO proíbe

Regra sem fronteira vira desculpa para fragmentar tudo, e aí o remédio é a doença:

- **Unidade grande e coesa.** Tamanho não é o critério. A repartição de polígono côncavo (L-03) pode legitimamente virar o maior arquivo do domínio e continuar sendo um átomo, porque tem uma razão de mudar. Caso real da casa: `tests/harness/prop.cpp` é hoje o maior arquivo do projeto (237 linhas) e é são: motor de teste de propriedade, uma razão de mudar, o desenho fixado na L-09.
- **O documento de mapa agregar os dados.** O documento É o agregado: célula, objeto e volume moram nele por definição. Monolito é acúmulo de **comportamento** (serializar, validar, repartir, despachar), não de dados. Proibir o agregado seria proibir o domínio.
- **A casca de plataforma numa peça.** A L-12 isenta a casca da atomização, e esta lei não revoga a isenção. A casca degenera por outro caminho, que a L-12 e o CONTRACT.md §5 já cobrem: regra de negócio dentro dela.
- **A ordem canônica de serialização.** O caminho de gravação está listado acima como lugar de risco, e está certo: escritor mais repartição convexa mais selo mais arquivo ao lado numa classe só é monolito. **Mas a ordem em que os blocos saem no arquivo NÃO é detalhe de implementação, é o contrato**: o GlintFx a fixou como normativa, e é ela que sustenta o portão de ida e volta byte a byte (`FMT-4`), que por sua vez é a prova mais forte que o formato tem. Um revisor que aplique a primeira pergunta ao escritor e conclua "isto tem razões demais para mudar, divida" pode quebrar essa ordem sem perceber. **Coesão exigida por contrato de terceiro não é monolito, e dividi-la não é conserto, é quebra.** Achado devolvido pela sessão do `gusworld` em 24/08/2026, ao adaptar esta lei para lá: sem freio escrito, a régua vira desculpa para fragmentar o que não devia.
- **Fragmentar por contagem.** A divisão é por razão de mudar, nunca por linha. Espalhar um algoritmo coeso em cinco arquivos "step" para agradar contagem reprova nas mesmas cinco perguntas (a terceira, na hora: o teste agora precisa montar os cinco). O teto de ~300 linhas do CONTRACT.md §2.2 continua sendo orientação (SHOULD), não portão: excedê-lo obriga a responder as cinco perguntas na revisão, não a dividir.

### Fiscalização (onde a lei mora no processo)

Lei qualitativa sem lugar no processo é lei que ninguém aplica. Três amarras:

1. **Na revisão adversarial de cada fatia** (implementador, revisor e orquestrador são três agentes, L-06): para **cada unidade criada ou crescida** na fatia, o revisor responde as cinco perguntas e grava as respostas no relatório de revisão. **Silêncio sobre uma unidade conta como unidade não revisada**, pelo mesmo princípio da L-17: silêncio não é prova de conformidade. A quinta pergunta se responde sempre, porque o diff sempre existe.
2. **No `AUDITORIAS.md`:** a seção 1 ganha item CRÍTICO ("nenhuma unidade acumula razões de mudar de mais de uma lei; os relatórios de revisão das fatias auditadas contêm as cinco perguntas respondidas por unidade") e a seção 6 passa a apontar para esta lei. O auditor (C-level em fable, L-06) não confia nos relatórios: pega o maior arquivo de cada camada e o arquivo com mais aparições no `git log --stat`, responde ele mesmo as cinco perguntas e compara com o que os relatórios disseram.
3. **Divergência tem dono.** Se implementador e revisor discordarem, ou se a separação exigida tiver custo real (reescrita grande, fronteira genuinamente duvidosa), a decisão vai ao líder por L-05, nunca sai no silêncio de um agente.

**Ao despachar subagent** que crie classe ou caso de uso, o texto desta lei vai no prompt da task (protocolo deste arquivo, item 2); a ordem de serviço do revisor cita as cinco perguntas como parte do entregável dele.

---
