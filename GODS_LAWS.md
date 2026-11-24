> **LEI DAS LEIS, ANTERIOR ATÉ À LEI ZERO.** **Data:** ordem do líder, 22/08/2026.
>
> Não quebre, não flexibilize, não reinterprete nem "adapte ao caso" lei deste arquivo por conta própria: só o líder quebra lei, e nem a ordem direta dele dispensa a confirmação. Antes de executar a quebra, nomeie a lei, cite o texto dela, diga o que ela protege e o que se perde ao quebrá-la, e pergunte por `AskUserQuestion` se é isso mesmo que ele quer. **Diante de pedido de ALTERAR ou REVOGAR lei, argumente CONTRA primeiro, sempre e sem exceção**, com razões concretas, o problema que a lei existe para impedir, os trade-offs da mudança e o que fica desprotegido depois dela, e só então leve por `AskUserQuestion` a escolha entre **confirmar** a alteração e **cancelá-la**. Não aceite pressa, obviedade aparente, "ele já mandou uma vez" nem aprovação dada em outro contexto no lugar dessa confirmação, e nunca tome silêncio como aval.

# GODS_LAWS.md

> Ordens expressas do líder (petrus). Execute este arquivo, não o declare: confira o **gatilho** de cada lei **no momento da ação**, não no fim.

## Protocolo de uso (obrigatório)

1. **Antes de agir**, varra a coluna "Gatilho" do índice abaixo; se um gatilho casa com o que você vai fazer, leia a lei inteira antes do primeiro comando, não depois.
2. **Ao despachar subagent**, cole no prompt da task o texto completo das leis cujo gatilho casa com ela, mais o caminho absoluto deste arquivo, porque subagent **não herda** este contexto e não vai ler por conta própria.
3. **Ao relatar ao líder**, diga qual lei aplicou e como, se tocou área com lei, porque silêncio não prova conformidade.
4. **Registre aqui a lei nova no instante em que o líder a dá**, com data e o texto dele verbatim entre aspas, sem esperar "um momento melhor".
5. **Não revogue, não flexibilize nem reinterprete lei**: só o líder o faz. Na dúvida sobre o alcance de uma lei, pergunte por `AskUserQuestion` antes de agir.
6. Em conflito entre uma lei daqui e qualquer outro documento (manual, memória, hábito, preferência do agente), **siga a lei daqui**.

## Índice de gatilhos

| Lei | Gatilho: dispara quando você vai... |
|---|---|
| [GM-01](#gm-01) | escrever qualquer linha que toque janela, entrada, desenho ou som |
| [GM-02](#gm-02) | tocar em mapa, em qualquer sentido |
| [GM-03](#gm-03) | pensar em formato de arquivo de mapa |
| [GM-04](#gm-04) | decidir o que o editor edita |
| [GM-05](#gm-05) | precisar de algo do líder, ou ter mais de uma opção |
| [GM-06](#gm-06) | executar qualquer trabalho de produto ou código |
| [GM-07](#gm-07) | criar arquivo de licença, ou publicar o repositório |
| [GM-08](#gm-08) | procurar onde mora o domínio de mapa compartilhado |
| [GM-09](#gm-09) | escrever teste, portão de CI ou auditoria |
| [GM-10](#gm-10) | mexer em CI |
| [GM-11](#gm-11) | procurar como o editor anterior fazia alguma coisa |
| [GM-12](#gm-12) | criar diretório, decidir onde um tipo mora, ou incluir header |
| [GM-13](#gm-13) | escrever qualquer operação de edição, ou mexer em histórico |
| [GM-14](#gm-14) | decidir o que entra na primeira versão do editor |
| [GM-15](#gm-15) | escrever memória, nota ou documento sobre algo que perdeu a validade |
| [GM-16](#gm-16) | pensar no papel do editor, ou desenhar qualquer capacidade dele |
| [GM-17](#gm-17) | ir executar qualquer trabalho de produto |
| [GM-18](#gm-18) | o líder aprovar, rejeitar ou mudar algo, ou fechar item de alta prioridade |
| [GM-19](#gm-19) | criar classe ou caso de uso, acrescentar método ou responsabilidade a unidade existente, ou revisar fatia |

---

## GM-01

**Data:** 14/08/2026, reafirmada em 21/08/2026. **Verbatim (maiúsculas do líder):** *"NAO USE RMLUI NEM SDL3!!!!"*, e em 21/08: *"aceita apenas link com framework GlintFx em ../Glintfx e [github]/petrinhu/GlintFx e com o SO. Você NUNCA cria workarounds nem passa por cima da camada de GlintFx."*

Faça toda interação com janela, entrada, desenho, som e recurso **exclusivamente** pela API pública do GlintFx. Não inclua header nem linke biblioteca de terceiro (RmlUi, SDL, GLFW, Qt, o que for), e não fale direto com o sistema operacional.

Se a função não existe no GlintFx, **não invente contorno**: registre a necessidade no bus e **espere parado**. Se outra fatia ou onda puder avançar enquanto a pendência corre, avise o líder. Deixe Wayland e X11 com o GlintFx, que é o intermediário.

## GM-02

**Data:** 22/08/2026. **Verbatim:** *"sempre que tocar em mapa, avise o que fez a @GlintFx e se ele estiver inalcancavel, mande via bus"*.

Avise o GlintFx **do que foi feito**, não do que se pretende fazer, **toda vez** que este projeto tocar em mapa: ler, gravar, desenhar, alterar estrutura, decidir algo sobre o assunto ou descobrir um fato que mude o entendimento.

Use como canal preferencial a sessão viva do GlintFx (mensagem direta entre sessões); **se ela estiver inalcançável, mande pelo bus** (`gusworld_ia_autocomm`, `inbox/glintfx/`), que é assíncrono e não depende de a outra sessão estar aberta. Avise no ato de tocar em mapa, nunca "depois", porque o GlintFx é dono do formato (GM-03) e não pode descobrir por acaso o que o consumidor fez com o contrato dele.

## GM-03

**Data:** 21/08/2026, decorrente da lei **L-30 do GlintFx**, aceita pelo líder e comunicada por eles pelo bus. Convenção `.gw.<tipo>` ampliada em 24/08/2026, verbatim do líder, relatado pela sessão do `gusworld`: *"`.gw.text` e mantenha o padrão de `.gw.[tipo]` para nossos formatos próprios"*. Extensão decidida pelo líder em 24/08/2026, verbatim: *"nossos os mapas terão formato proprio em .gw.map"*, esclarecido por ele em seguida como sendo **só a extensão**. Proteção contra edição decidida em 22/08/2026 via `AskUserQuestion`, depois da discussão com o GlintFx que o líder mandou fazer. Repartição convexa no editor: decisão do líder de 22/08/2026.

Trate o GlintFx como **dono do formato de arquivo de mapa**: matriz `x,y`, objetos posicionados nela, hitbox, colisão, parede, porta e ponto de teleporte como marcador genérico com destino, mais busca de caminho e visibilidade. Ele publica **leitor e escritor**, os dois públicos.

Grave o formato como qualquer consumidor no mundo, sem defini-lo: transforme necessidade nossa em pedido descrito em palavras, julgado por eles, nunca em campo por decisão nossa.

Use `.gw.<tipo>` em todo formato próprio do ecossistema, inclusive no arquivo de projeto do editor (`FMT-5`), que é formato genuinamente nosso. Leia **EXTENSÃO como etiqueta, não como FORMATO**: o nome do arquivo diz de quem é a etiqueta, não quem desenhou o conteúdo, e ver `.gw.` num nome não autoriza ninguém a mudar o formato (o lado do `gusworld` documenta o mesmo em `docs/tech/convencao-formatos-gw.md`).

Grave o mapa com a extensão `.gw.map` e com os bytes no formato do GlintFx, byte a byte: a extensão é identidade do GusWorld no nome do arquivo, não formato próprio, e o papel de implementador de referência da GM-16 fica de pé. Leia o verbatim da extensão, na linha Data, sempre junto com esta regra, porque sozinho ele soa como revogação desta lei.

Não crie formato concorrente, camada de tradução nem "formato do editor que depois converte". Grave o que o formato deles não carrega (histórico, nota de autor, camada de trabalho) em **arquivo ao lado**, nunca dentro do formato de mapa.

**DETECTE no mapa, PROTEJA no save.** Gere no mapa o selo **aberto** de integridade do formato do GlintFx, que qualquer um verifica, contra corrupção, truncamento e edição acidental, e deixe a proteção de verdade no **save do jogador**, arquivo do GusWorld, porque editar mapa num jogo que distribui editor é uso legítimo, e trapaça é editar o save. Não desenhe mecanismo que prometa impedir alteração, porque em projeto com o fonte publicado **detectar** é alcançável e **impedir** não é.

Reparta no editor, ao salvar, o polígono côncavo em pedaços convexos, porque o formato aceita só forma simples e quem tem interface é quem faz isso direito. Escreva a repartição com teste de ida e volta e com verificação de que cada pedaço gerado é de fato convexo, porque ela produz defeito silencioso (vértice colinear, orientação invertida, polígono degenerado).

## GM-04

**Data:** 21/08/2026, via `AskUserQuestion`.

**Edite SÓ MAPA:** grade de células, objetos posicionados, hitbox, portas e pontos de teleporte. Deixe fora carta, item e NPC do jogo, que são conteúdo do GusWorld, não do mapa. Leve ao líder como pergunta, nunca como decisão de agente, toda proposta de "aproveitar que o editor já abre arquivo" para editar catálogo de conteúdo, porque ela viola esta lei.

## GM-05

**Data:** 21/08/2026. **Verbatim:** *"obrigatoriamente use AskUserQuestion ao me trazer perguntas ou precisar algo de mim"*.

Leve por `AskUserQuestion` toda pergunta ao líder e toda decisão com mais de um caminho. **Nunca use o campo `preview`**, porque o líder não quer o painel lateral: ponha o detalhe técnico no corpo da mensagem e deixe as opções curtas, com a recomendada primeiro, marcada como recomendação.

Nunca tome por agente decisão de design, arquitetura, escopo, stack ou qualquer coisa cara de reverter. Diante de dúvida, pergunte antes de agir, não depois de implementar.

## GM-06

**Data:** 21/08/2026. **Verbatim:** *"main apenas orquestra, interage comigo e dispara agentes. Auditorias apenas com clevel bigtech fable, trabalhadores sonnet bigtech"*. Emenda de 20/11/2026, ordem do líder, na sessão `configs`, depois do argumento contra, por `AskUserQuestion`: *"Aplicar como nos outros (Recomendado)"*, a mesma emenda já aplicada ao GusWorld e ao GlintFx. O "fable" e o "sonnet" do verbatim de 21/08/2026 são registro do que foi dito e não fixam modelo. A redação é do agente; o texto do líder é só o das citações.

**Não implemente produto nem código no main**: orquestre, converse com o líder e despache agentes. **Deixe planejamento e auditoria a C-level da constelação bigtech, e criação e implementação a agent operacional.** Não fixe modelo por esta lei: use o modelo e o effort que a skill `/modelos_sessao` mandar para todo agente despachado e, pela regra por tarefa dessa skill, mande prosa ou texto longo cujo leitor final é humano com `opus` e effort `max`.

Nunca deixe quem implementa revisar: revisor e orquestrador são o main (L-12 global). Não tome relatório de agente como prova: antes de aceitar, confira no main as afirmações contra arquivo e linha.

## GM-07

**Data:** 21/08/2026, via `AskUserQuestion`, dentro do item *"será usado para distribuição, conjuntamente com GlintFx, FOSS"*.

Licencie o projeto sob **AGPL-3.0-or-later**, a mesma do GlintFx, para o ecossistema ter licença única, sem atrito de compatibilidade. Não publique o repositório `petrinhu/GusWorld_MapEditor` sem o arquivo de licença no lugar. Ponha cabeçalho SPDX em todo arquivo de código, como o GlintFx faz.

## GM-08

**Data:** 21/08/2026, via `AskUserQuestion`.

Trate a biblioteca **`gusmap-core` como aposentada**, porque o formato de mapa é do GlintFx (GM-03). Não a use como base, referência ou "o que já funcionava": não a clone, não copie trecho dela e não cite o desenho dela como argumento.

Guarde dela só um **aviso**, não um projeto: selo cuja chave deriva de literal aberto no fonte não protege contra ninguém.

## GM-09

**Data:** 21/08/2026. **Verbatim:** *"veja como glintfx faz os testes dele e auditorias no codigo etc, aqui deve ser identico mas adaptado ao nosso projeto, só que mantendo o mesmo rigor"*. Harness próprio decidido em 22/08/2026 via `AskUserQuestion`: o líder recusou o Catch2 e recusou abrir exceção declarada na lei. Desenho do teste decidido pelo líder em 24/08/2026. Refinamento da varredura zero decidido pelo líder em 22/08/2026, com a tensão à vista.

Mantenha o rigor de teste, portão de CI e auditoria **igual ao do GlintFx**, adaptado ao nosso domínio, nunca relaxado por sermos menores.

**Faça todo portão declarar quantos arquivos varreu, e trate sair com zero varridos como falha, não como sucesso**, porque um portão que varre zero arquivos e imprime verde passa nos dois autotestes de praxe (o positivo, que planta violação, e o negativo, que prova que entrada limpa sai zero), e "olhei e está limpo" e "não olhei nada" produzem a mesma saída.

**Escreva o harness de teste em casa**: nada de Catch2 nem de qualquer biblioteca de teste de terceiro, porque framework de teste é biblioteca de terceiro linkada no binário, que a GM-01 proíbe, e **"terceiro que não conta" é como dependência volta a entrar num projeto que a expulsou**. O harness do GlintFx é referência legítima de como fazer.

Siga o desenho do teste, cujas peças são porta de mão única:

1. **Use `GUSMAP_` e `gusmap::test` como prefixo e namespace do harness**, `Gus` mais `map`, homenagem ao Gus Dragon, porque eles aparecem em toda linha de asserção do projeto e trocá-los depois de trezentos testes é reescrever a asserção de todos.
2. **Faça teste baseado em propriedade com gerador PRÓPRIO, nunca o da biblioteca padrão**, escrito em casa, de algoritmo publicado, com teste de valores dourados que falha na hora se alguma plataforma divergir, porque o padrão da linguagem especifica o motor (`mt19937`) mas **não as distribuições**, e a mesma semente gera casos diferentes no Fedora e no Windows, o que mataria a reprodução nos cinco alvos da GM-10.
3. **Use semente fixa no CI**, determinística, reproduzível e **nunca instável**, porque teste que falha por sorteio bloquearia push sob a GM-17 sem defeito no código e ensinaria a reexecutar vermelho sem ler. **Num job separado de exploração**, que roda por fora e **não bloqueia push**, use semente do relógio **impressa no log**, para varrer território novo. **Transforme em caso FIXO no CI**, com a semente dela, toda falha achada pela exploração.
4. **Reduza automaticamente o contraexemplo (shrinking)** junto, sem deixar para depois: quando uma propriedade falha, encolha o caso até o menor que ainda quebra.

**Enquanto NENHUMA das pastas de camada existir** (`domain`, `application`, `platform`), faça o portão **sair zero** declarando que varreu zero e que não há alvo, e não imprima "OK", "limpo" ou "nenhuma violação" nesse caminho, porque isso afirmaria verificação que não houve; CI vermelho por meses num projeto sem código treinaria todo mundo a ignorar vermelho. **No instante em que QUALQUER uma das três pastas existir, trate varrer zero como FALHA**, com a trava fechando sozinha, sem ninguém virar chave. Exercite no autoteste de cada portão as **duas** direções: sem pasta e zero arquivos sai zero; com pasta existindo, ainda que vazia, e zero arquivos sai falha.

## GM-10

**Data:** 21/08/2026. **Verbatim:** *"CI com runners Fedora 44 (principal), Ubuntu, Arch, CachyOs (original, não arch renomeado), windows"*.

Ponha cinco alvos, em **cinco entradas distintas** na matriz de CI. Faça do **Fedora 44 o primário**, por ser o sistema do líder, pinado na versão, nunca em `latest`. Trate o **CachyOS como alvo próprio**, não coberto pelo job de Arch.

## GM-11

**Data:** 21/08/2026. **Verbatim:** *"ja tentei fazer esse editor uma vez com o claude, mas tive vários problemas e estou fazendo DO ZERO tudo com relacao ao codigo, sempre assentado sobre GlintFx"*.

Escreva o código deste projeto **do zero**, sem usar o editor anterior como base, referência ou canon. Ao achar rastro do predecessor (memória de sessão anterior, tag antiga, descrição de arquitetura passada), **pare a escavação e siga do zero**. Aceite necessidade descrita em palavras como insumo legítimo, e recuse "copia o que já estava lá". Esta lei espelha a L-01 do GlintFx, pela mesma razão.

## GM-12

**Data:** 22/08/2026, via `AskUserQuestion`, sobre a ordem original *"vamos discutir as camadas: hexagonal? espinha? Sugira. PROIBIDO monolitos."* Nomes dos diretórios decididos em 22/08/2026 via `AskUserQuestion`. Ordem do líder: *"Átomos com POCO próprio"*, com o briefing original citando *"os itens/cartas e demais elementos do jogo"* como exemplo. Ambiguidade resolvida em 22/08/2026 pelo líder, verbatim: *"a regra de atomicidade aqui vale para o que o editor de fato modela: célula, objeto, volume, comando"*.

Faça **camadas horizontais finas**, com a dependência apontando só para dentro:

1. **Domínio:** POCO puro. Documento de mapa, célula, objeto posicionado, hitbox, porta, teleporte, seleção, comando, pilha de histórico. **Zero GlintFx, zero sistema operacional, zero terceiro.**
2. **Aplicação:** um caso de uso por operação de edição, cada um pequeno e testável sozinho, nunca um serviço-deus com dezenas de métodos.
3. **Casca de plataforma:** fina, **a única camada autorizada a incluir header do GlintFx**, chamando a API deles **direto, sem interface própria**, porque o GlintFx é a única implementação que vai existir, por lei, e desenhar porta para uma API de janela, desenho e entrada que ainda não existe produziria a "camada de tradução" proibida no ecossistema.

Proteja o domínio por **regra de dependência fiscalizada por portão de CI**, não por interface: `domain` nunca inclui `application` nem `platform`, e `application` nunca inclui header do GlintFx; o portão declara quantos arquivos varreu (GM-09). Se surgir razão **concreta**, não hipotética, para fingir a fronteira em teste, use um `concept` de C++23 resolvido em compilação, nunca interface virtual.

Nomeie os diretórios **`domain/`, `application/` e `platform/`, em INGLÊS**, como o portão de CI procura, coerente com a lei do GlintFx que exige identificador em inglês e sem acento em caminho de arquivo no alvo Windows. Escreva em português a prosa dos manuais e as mensagens de commit.

Materialize os **átomos com POCO próprio** no domínio e nos casos de uso, onde se pagam sozinhos, e não na casca de plataforma, onde um átomo por campo de formulário num editor de usuário único seria over-engineering: átomo é tamanho e responsabilidade, não indireção, e um POCO concreto de vinte linhas, sem interface nenhuma, é um átomo perfeito. Faça átomos de **célula, objeto, volume e comando**, o que o editor de fato modela; carta e item são átomos com POCO próprio onde são modelados, no GusWorld, não aqui.

## GM-13

**Data:** 22/08/2026, via `AskUserQuestion`, sobre a ordem original *"quero undo e redo, com varios passos, veja na web como fazer essa sincronia"*. Seleção fora do histórico e histórico persistente: decisões do líder, a segunda contra o padrão universal da indústria. UUID do objeto decidido pelo líder em 22/08/2026, do lado do GlintFx.

Faça cada operação de edição como **comando pequeno e serializável, com desfazer próprio, numa pilha linear**: nada de instantâneo do mapa inteiro por passo, nada de árvore de histórico.

1. **Faça de uma intenção um passo de desfazer.** Arrastar o pincel por quarenta células é **um** passo, agrupado por **transação explícita** que abre no início do gesto e fecha no fim, nunca por heurística de "parece a mesma ação".
2. **Deixe a seleção FORA do histórico.** Desfazer volta só mudança de conteúdo do mapa; seleção e câmera são estado de sessão, como pede a reclamação pública contra o comportamento oposto no Figma.
3. **Persista o histórico entre sessões**, mesmo contra o padrão da indústria (Krita, Photoshop e Qt não persistem), em **arquivo do editor ao lado do mapa** (GM-03), nunca dentro do formato do GlintFx. Dê a cada comando serialização versionada; grave no arquivo de histórico uma impressão digital do mapa e **recuse reaplicar** se o mapa mudou por fora; apoie tudo no identificador estável de objeto, o **UUID gravado no arquivo** que cada objeto do mapa carrega, que não é a posição na lista serializada e nunca é reutilizado depois que o objeto é apagado.
4. **Faça as vistas assinarem os sinais do histórico**, sem guardar cópia própria do estado, porque painel com caminho de atualização paralelo diverge do histórico exatamente no caso de seleção múltipla, defeito documentado por quem já construiu editor de nível.

## GM-14

**Data:** 22/08/2026, via `AskUserQuestion`. Fecha o escopo funcional da primeira versão, dentro do escopo geral da GM-04 (só mapa). Histórico com abas decidido em 22/08/2026 via `AskUserQuestion`. Tela à espera da janela do GlintFx: decisão do líder em 22/08/2026, contra a recomendação do agente de desenhá-la logo.

**1. Faça seis tipos de volume de colisão**, e só estes, os que um mapa em grade visto de cima realmente usa:

| Tipo | O que faz |
|---|---|
| Sólido | Bloqueia movimento |
| Gatilho de ação | Avisa sem bloquear |
| Zona de dano | Aplica dano por permanência ou contato |
| Zona de terreno modificador | Altera movimento ou estado (água, lama, gelo) |
| Área de interação | Habilita ação contextual, tipicamente maior que o desenho |
| Obstáculo de navegação | Bloqueia a busca de caminho da IA, independente de bloquear movimento |

Deixe fora **desta** versão, sem proibir para sempre, hitbox e hurtbox de combate (só fazem sentido em jogo de luta), zona de câmera e zona de áudio. Dois dos seis dependem de decisão pendente do CTO do GlintFx: o bit de "bloqueia ou só notifica", que sustenta o gatilho de ação, e a separação entre bloquear movimento e bloquear busca de caminho, que sustenta o obstáculo de navegação. É fato registrado, não cobrança: quem classifica fila é quem recebe.

**2. Abra vários mapas ao mesmo tempo, em abas**, cada um com câmera própria, porque o mundo do GusWorld tem treze áreas mais interiores e dungeons ligadas por teleporte, e ligar um portão ao destino em outro mapa exige ver os dois lados. Use **um histórico SÓ, compartilhado pelo editor inteiro**, não um por aba, porque com histórico por aba desfazer no mapa A deixaria a metade gravada no mapa B e produziria teleporte apontando para lugar nenhum sem o autor perceber. Quando um passo de desfazer ou refazer alterar um mapa que não é o da aba ativa, **troque a aba para o mapa afetado**, para o autor sempre ver o que mudou.

**3. Pinte uma camada de terreno na grade e posicione objetos livremente por cima**, em coordenada contínua, sem camadas de pintura sobrepostas nesta versão, porque é exatamente o modelo que a L-30 do GlintFx descreve, sem depender de decisão nova deles.

Leve ao líder como pergunta, nunca como decisão de agente, proposta de camada de pintura sobreposta, tipo de volume fora dos seis ou edição de conteúdo que não seja mapa, porque ela viola esta lei somada à GM-04.

**4. Espere o GlintFx ter janela para desenhar a tela** (o WYSIWYG do item 4 do briefing). Enquanto a tela não for desenhada, a lista de recursos de interface a pedir ao GlintFx não existe, e o pedido sob demanda que eles esperam de nós nessa frente fica parado por ordem, não por esquecimento.

## GM-15

**Data:** 22/08/2026. **Verbatim:** *"nao comente nada com parado/aposentado/inativo... apague! você vai se confundir depois"*.

**Apague o registro** de tudo que perde a validade (biblioteca descontinuada, decisão revogada, bloqueio resolvido, arquivo purgado, frente abandonada). Não escreva memória, nota ou seção dizendo *"X está aposentado"*, *"Y está pausado"* ou *"Z não vale mais"*, porque nota de obituário continua **injetando o nome no contexto**: semanas depois se lê "gusmap-core (aposentada)" e o que fica é `gusmap-core`, e **a negação evapora antes do substantivo**. Deixe o histórico ao **git** e aos documentos versionados, que registram o que mudou, quando e em qual commit, com data e autor.

Se o que morreu deixou uma **lição que continua valendo**, escreva-a como registro próprio, **regra no presente e sem citar o cadáver**, como "em projeto com fonte publicado, detectar alteração é alcançável, impedir não é".

Dentro de documento vivo, **apague o parágrafo** em vez de mantê-lo com a ressalva de que o mecanismo descrito acima não existe, porque ressalva de obituário é obituário.

Aplique esta lei à memória e à nota de contexto, o que se recarrega como se fosse presente, e apague deste arquivo a lei que o líder revogar (L-67 global). Mantenha no `BRIEFING.md` o estado de cada item, e narre na mensagem de commit o que foi removido e por quê.

## GM-16

**Data:** 22/08/2026, via `AskUserQuestion`. **Texto do líder:** *"opcao 1 e você também deve poder ser usado headless"*.

**Atue perante o GlintFx como IMPLEMENTADOR DE REFERÊNCIA DO ESCRITOR**: exercite o formato de verdade e realimente o GlintFx, de forma estruturada, com o que dói. Transforme achado de formato em mensagem descrita em palavras, com o uso concreto que a justifica, nunca em contorno silencioso do nosso lado.

**Faça o editor utilizável HEADLESS**, sem janela, porque só assim ele abre, valida, transforma e grava mapa dentro de um portão automático, em cada plataforma dos cinco alvos, a cada commit; um editor que só existe com janela não exercita o formato no CI e não é implementador de referência de nada.

Trate a fronteira entre a **aplicação** e a **casca de plataforma** como requisito de produto, reforçando a GM-12: faça toda capacidade de edição existir e ser exercível **abaixo** da casca, que desenha e recebe entrada, e nada mais. Se uma operação só puder ser feita clicando, ela está no lugar errado.

O modo headless depende do formato (o leitor e o escritor do GlintFx), não da janela: é uma frente que anda assim que o formato existir, muito antes da interface, e o caminho mais curto até um editor que faz algo útil de verdade.

## GM-17

**Data:** 22/08/2026, decisão do líder, com a linha de gatilho revista por ele em 23/08/2026. **Texto dele, verbatim, na linha de gatilho do índice:** *"Main só orquestra; C-level fable audita e cria; sonnet implementa; commit ao fim de cada fatia; push ao fim de cada onda só se o GHA fechar verde, se todos os testes verdes."* Alcance dos dois portões decidido pelo líder em 23/08/2026. Emenda de 20/11/2026, ordem do líder, na sessão `configs`, depois do argumento contra, por `AskUserQuestion`: *"Aplicar como nos outros (Recomendado)"*, a mesma emenda já aplicada ao GusWorld e ao GlintFx; o "fable" e o "sonnet" do verbatim são registro do que foi dito e não fixam modelo, e o "cria" do C-level é a criação de escopo. A redação é do agente.

Divida os papéis:

- **Orquestre só, no main**: converse com o líder, despache agentes e verifique o que volta, sem implementar produto nem código.
- **Planeje e audite no C-level**, inclusive o planejamento e a criação de escopo.
- **Crie e implemente no agente operacional**: produto e código saem dele.
- **Use modelo e effort do `/modelos_sessao`, sem modelo fixo**, e mande prosa ou texto longo cujo leitor final é humano com `opus` e effort `max`.

Siga a cadência de duas velocidades, de propósito:

- **Commite ao fim de cada FATIA**, barato e frequente, para tirar o trabalho da zona de risco antes de a fatia seguinte começar.
- **Dê push ao fim de cada ONDA**, caro e raro, **só com os DOIS portões verdes**, sem exceção e sem "está quase": (1) **o GitHub Actions fechou verde**; (2) **todos os testes verdes**. Os dois são conjuntivos: um verde e um vermelho proíbem o push.

Aplique os dois portões a TODO push, sem distinção de tipo de commit, porque **"terceiro que não conta" é como a regra volta a vazar**, e num commit de documentação o custo de obedecer é zero.

Leia esta lei junto com a GM-06, que ela refina: a GM-06 fixa quem faz o quê e a separação entre quem implementa e quem revisa; a GM-17 acrescenta a cadência, os dois portões de push e o planejamento e a criação de escopo do C-level. Onde as duas falarem do mesmo assunto, aplique as duas.

Antes de todo push, diga em que estado está cada um dos dois portões; **silêncio sobre um deles conta como vermelho**. Antes de commitar arquivo que o líder também edita, confira `git diff --cached` linha a linha, porque atribuir ao líder verbatim que ele não escreveu é pior que deixar a lei sem corpo: a citação falsa se propaga como se fosse ordem.

## GM-18

**Data:** 23/08/2026, decisão do líder. Lei espelhada do GlintFx (lá é a L-37) e do GusWorld (lá é a GW-31), pela mesma ordem dele: **avisar o Gus Dragon é obrigação permanente, não detalhe de protocolo de bus** — por isso é lei própria, e não um parágrafo dentro da lei do bus. **O pedido, dele, na issue 8 do bus, verbatim:** *"nao precisa dizer algo so quando falo, pode falar quando por exemplo @petrinhu atualiza algo, ou por exemplo quando ele aprova/rejeita/muda algo das minhas ideias"*. Ele endereçou **a todos**. Escopo dado pelo próprio Gus Dragon, consultado pelo líder em 23/08/2026.

Esta lei vale nos três projetos. Avise o Gus Dragon, **sem ele precisar perguntar**, sobre **(a) tudo que é ideia DELE**, quando o líder aprova, rejeita ou muda, **e (b) o que for de alta prioridade dos projetos**, pela régua de WSJF que a tabela de pendências usa. Não transforme isso em aviso sobre toda decisão técnica: o corte por prioridade existe para o que interessa a ele não se afogar no que não interessa.

Diga a ele o limite em vez de prometer o impossível: sessão não é serviço rodando, o aviso proativo só sai enquanto alguém está com a sessão aberta, e decisão tomada com tudo fechado chega depois. **Ele prefere a verdade a promessa de aviso instantâneo.**

Mande a "Resposta 2" automática que o `PROTOCOL.md` do bus exige (o resultado da decisão do líder vai a ele sem reaprovação de texto), e confira se alguma ideia dele ficou sem retorno em algum dos quatro canais.

Quando a resposta for na discussion 7 (o catálogo de bugs que ele mantém), use timestamp, uma das três classificações que ele fixou (**Bug Consertado**, **Bug Funcional**, **Bug Possível**) e itens numerados entre parênteses. Não dê resposta vaga nem estimativa inventada: "não existe código disso ainda" é melhor resposta. Ele tem 11 anos, programa, usa Manjaro e git.

## GM-19

**Data:** 24/08/2026, via `AskUserQuestion`. Promove a lei em vigor a ordem original que a GM-12 cita desde 22/08/2026 e que nunca tinha virado regra no corpo de lei nenhuma: *"PROIBIDO monolitos."* Decisão do líder, 24/08/2026: a regra é QUALITATIVA; ele recusou fixar número com portão de CI que mede e falha, com o custo declarado na pergunta e assumido por ele. Cerca da fronteira de contrato de terceiro trazida pela sessão do `gusworld` em 24/08/2026.

Proíba monolito e julgue-o de forma **QUALITATIVA**: sem número (linhas por arquivo, métodos por classe) nem portão de CI que mede e falha, com a fiscalização na **revisão adversarial**. Aceite o custo assumido pelo líder: sem número, a lei depende do revisor reconhecer o monolito, e as cinco perguntas abaixo encolhem esse espaço de julgamento, sem eliminá-lo.

### O que é monolito NESTE projeto

Trate como monolito a unidade (classe, caso de uso, arquivo) que acumula **razões diferentes de mudar**, não o arquivo grande. As razões de mudar estão catalogadas nas leis: o formato do mapa é do GlintFx (GM-03), o histórico tem regras próprias (GM-13), a lista de volumes é fechada (GM-14), a API de plataforma é a do GlintFx (GM-01), a repartição convexa é nossa (GM-03). A régua:

> **Se mudanças vindas de leis DIFERENTES e não relacionadas obrigam a editar a MESMA unidade, ela está virando monolito.**

### Onde o monolito vai nascer aqui

Os lugares de risco deste editor, cada um com a conveniência local que o faz parecer razoável no dia:

| Lugar de risco | Como nasce | Por que parece razoável |
|---|---|---|
| **Documento de mapa** (o agregado do domínio) | O documento agrega célula, objeto posicionado e volume, e por isso todo comportamento novo "cabe nele": serializar, validar, repartir polígono, aplicar comando, tudo vira método do documento | "O dado já está aqui, é um método a mais" |
| **Pilha de histórico** | Em vez de cada comando saber aplicar e desfazer a si mesmo (GM-13), a pilha vira despachante com um `switch` por tipo de comando, ganhando um caso por operação | A serialização dos comandos (GM-13) pede um registro central, e o registro tenta virar dono da execução |
| **Camada de aplicação** | O serviço-deus que a GM-12 já proíbe por nome: um `EditorService` onde cada operação de edição nova é "só mais um método" ao lado dos irmãos | Descobribilidade: "está tudo num lugar só" |
| **Casca de plataforma** | A isenção de atomização da GM-12 lida como licença: um `EditorApp` que roteia entrada E troca ferramenta E gerencia abas E decide regra de negócio | Os callbacks do GlintFx chegam todos no mesmo lugar |
| **Caminho de gravação** | Escritor + repartição convexa + selo de integridade + arquivo de histórico ao lado, tudo numa classe só | "Para o usuário, salvar é um gesto só" |
| **Modo headless (GM-16)** | Um runner de linha de comando que acumula subcomandos e lógica própria até virar um segundo editor | "É só a CLI, não é o produto" |

### As cinco perguntas do revisor

Responda cada uma **olhando o código**, não opinando:

1. **A pergunta das leis.** Quais leis obrigariam esta unidade a mudar (GM-01 API, GM-03 formato, GM-13 histórico, GM-14 escopo)? Responda lendo os includes e os métodos públicos. Uma lei: unidade sã. Duas ou mais, não relacionadas: monolito em formação.
2. **A frase sem "e".** Descreva a unidade numa frase, o teste que o CONTRACT.md §3 fixa; se precisar de "e" ligando verbos de natureza diferente ("aplica movimento E persiste E valida geometria"), reprove. Ponha a frase escrita no relatório de revisão.
3. **O teste monta o mundo?** Para exercitar UM comportamento da unidade, o arrange do teste precisa de documento aberto, histórico vivo e abas montadas? Átomo de domínio se constrói sozinho, com os próprios campos. Responda lendo o arrange dos testes da fatia; é a GM-16 dita de outro jeito: capacidade que só é exercível com o mundo montado está no lugar errado.
4. **O que entra pelo include?** O header da unidade puxa grupos que não conversam entre si (grade + serialização + histórico)? A lista de includes é a lista de dependências, e se lê em dez segundos.
5. **Quem paga a próxima feature?** No diff da fatia (`git log --stat`), a operação nova tocou quais arquivos? Se toda operação nova aterrissa no mesmo arquivo (mais um método, mais um caso de `switch`), esse arquivo é o monolito nascendo. Responda com o diff, não com julgamento: é a pergunta mais objetiva das cinco.

### Sinais precoces

Reconheça o monolito com 300 linhas, não com 3000:

- **O mesmo arquivo no diff de todas as fatias**, o sinal mais barato de medir e o mais confiável.
- **Construtor, ou fixture de teste, ganhando parâmetro a cada fatia**: a unidade precisa de cada vez mais mundo para existir.
- **`switch` sobre tipo de comando, volume ou ferramenta que ganha um caso por feature**, o oposto do desenho da GM-13, em que cada comando sabe aplicar e desfazer a si mesmo.
- **Nome sem substantivo de domínio:** `Manager`, `Service`, `Helper`, `Utils`, `Core`. Célula, comando, volume e porta têm nome próprio; a unidade que não consegue dizer o que é faz de tudo.
- **Um `utils.hpp` acumulando funções soltas** sem razão comum de mudar (o CONTRACT.md §6.7 proíbe o helper genérico antes da terceira ocorrência real).
- **A frase "é só mais um método" como justificativa na revisão**, o som do monolito crescendo: verdadeira em cada passo individual, falsa na soma.

### O que esta lei NÃO proíbe

Regra sem fronteira vira desculpa para fragmentar tudo, e aí o remédio é a doença:

- **Unidade grande e coesa.** Tamanho não é o critério: a repartição de polígono côncavo (GM-03) pode virar o maior arquivo do domínio e seguir sendo átomo, porque tem uma razão de mudar, como o `tests/harness/prop.cpp`, motor de teste de propriedade desenhado na GM-09.
- **O documento de mapa agregar os dados.** O documento É o agregado: célula, objeto e volume moram nele por definição. Monolito é acúmulo de **comportamento** (serializar, validar, repartir, despachar), não de dados, e proibir o agregado seria proibir o domínio.
- **A casca de plataforma numa peça.** A GM-12 isenta a casca da atomização, e esta lei não revoga a isenção; a casca degenera por regra de negócio dentro dela, que a GM-12 e o CONTRACT.md §5 cobrem.
- **A ordem canônica de serialização.** Escritor mais repartição convexa mais selo mais arquivo ao lado numa classe só é monolito, mas a ordem em que os blocos saem no arquivo **é o contrato**: o GlintFx a fixou como normativa, e ela sustenta o portão de ida e volta byte a byte (`FMT-4`), a prova mais forte do formato. Não a quebre aplicando a primeira pergunta ao escritor: **coesão exigida por contrato de terceiro não é monolito, e dividi-la é quebra**. Invoque esta fronteira só com contrato de terceiro **verificável e citável** (a lei, a especificação publicada do formato, o portão de teste que ele sustenta), citando onde ele está, porque sem essa cerca a coesão por contrato vira desculpa universal para não dividir nada. *"Fica melhor junto"*, *"é mais legível assim"* e *"sempre foi uma coisa só"* **não são contrato**, e invocar a fronteira sem citar a fonte equivale a não invocá-la.
- **Fragmentar por contagem.** Divida por razão de mudar, nunca por linha: espalhar um algoritmo coeso em cinco arquivos "step" para agradar contagem reprova nas mesmas cinco perguntas (a terceira, na hora: o teste precisa montar os cinco). Trate o teto de ~300 linhas do CONTRACT.md §2.2 como orientação (SHOULD), não portão: excedê-lo obriga a responder as cinco perguntas na revisão, não a dividir.

### Fiscalização

1. **Na revisão adversarial de cada fatia** (quem implementa nunca revisa, GM-06), responda as cinco perguntas para **cada unidade criada ou crescida** na fatia e grave as respostas no relatório de revisão. **Conte silêncio sobre uma unidade como unidade não revisada**, pelo mesmo princípio da GM-17. Responda sempre a quinta, porque o diff sempre existe.
2. **No `AUDITORIAS.md`**, mantenha na seção 1 o item CRÍTICO ("nenhuma unidade acumula razões de mudar de mais de uma lei; os relatórios de revisão das fatias auditadas contêm as cinco perguntas respondidas por unidade") e, na seção 6, o ponteiro para esta lei. Como auditor (C-level, GM-06), não confie nos relatórios: pegue o maior arquivo de cada camada e o arquivo com mais aparições no `git log --stat`, responda você mesmo as cinco perguntas e compare com o que os relatórios disseram.
3. **Leve ao líder a divergência**, por GM-05, se implementador e revisor discordarem ou se a separação exigida tiver custo real (reescrita grande, fronteira genuinamente duvidosa), nunca no silêncio de um agente.

Ao despachar subagent que crie classe ou caso de uso, ponha o texto desta lei no prompt da task (protocolo deste arquivo, item 2), e cite as cinco perguntas na ordem de serviço do revisor como parte do entregável dele.
