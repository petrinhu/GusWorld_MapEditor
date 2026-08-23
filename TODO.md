> **ESTRUTURA CANÔNICA DO ARQUIVO, NÃO QUEBRAR A TABELA:** título → preâmbulo (bullets) → `## INBOX` → `## TABELA UNIFICADA` (uma tabela só, 10 colunas com `WSJF` como primeira, zero linha em branco dentro dela) → **EOF logo após a última linha da tabela**. Legenda, bloqueios e a fórmula do WSJF vivem em bullets no preâmbulo, nunca em tabela auxiliar. **Proibido:** segunda tabela; linha em branco dentro da tabela.

# TODO.md: GusWorld_MapEditor

Tabela de pendências e planejamento, ordenada de cima para baixo na ordem de execução que minimiza retrabalho. A ordem das linhas **é** o ranking WSJF dentro de cada nível de dependência; **dependência sempre vence WSJF** quando os dois conflitam. A coluna `Onda` marca passos de igual valor que podem rodar em paralelo.

## Proveniência (de onde vem cada peça desta tabela)

Esta seção existe porque a ausência dela já custou caro nesta noite: um agente leu as leis e o briefing, não achou registro de uma pesquisa que tinha acabado de acontecer, e escreveu "não foi feita" sobre um trabalho de duas horas. **Lei e decisão guardam a conclusão, não a procedência.** Aqui fica a procedência.

- **Leis, sem exceção:** `GODS_LAWS.md` na raiz. Vence este arquivo em qualquer conflito.
- **Lista bruta dos itens e o mapa dos 28 pedidos originais:** `BRIEFING.md` na raiz.
- **Porte do projeto: MÉDIO (scale)**, por decisão do líder em 22/08/2026, corrigindo a classificação "early" do Chief of Staff. É essa correção que torna a pontuação WSJF item a item **obrigatória** (`AGILE.md` §17.2) em vez de qualitativa.
- **Custo de Atraso (Valor + Criticidade + Redução de Risco) de cada item:** lente do `product-manager`, 22/08/2026.
- **Job Size de cada item:** lente do `engineering-manager`, 22/08/2026, na unidade "fatia de trabalho de agente" (implementação + revisão adversarial + teste), não hora-pessoa.
- **Montagem por thread direta** (sem as lentes de arquitetura e de sequenciamento), por decisão do Chief of Staff: o grafo de dependência e as portas de mão única deste projeto já estão congelados nas próprias leis, então não sobrava julgamento para uma lente paralela descobrir.
- **Os itens `COR-10`, `COR-11` e `FMT-7` foram pontuados pelo ORQUESTRADOR**, em 23/08/2026, não pelas lentes de produto e de engenharia que pontuaram todo o resto. Eles nasceram das decisões 7, 8 e 9 do GlintFx, que chegaram depois da montagem da tabela. A escala usada é a mesma, mas **o número deles vale menos que o dos outros** e deve ser refeito pelas lentes na próxima reordenação.
- **Pesquisa que sustenta as decisões de produto e de histórico:** levantamento de prior art de 21/08/2026 sobre Warcraft II (formato PUD), Warcraft III, Tiled, LDtk, Godot, Valve Hammer, Ogmo e RPG Maker, mais taxonomia de volumes de colisão e arquitetura de undo/redo. É a base das `L-13` e `L-14` e do documento de necessidade de formato enviado ao GlintFx.

## Como o WSJF foi calculado

- `CoD = Valor de Negócio + Criticidade Temporal + Redução de Risco`, cada componente na régua Fibonacci modificada `1, 2, 3, 5, 8, 13, 20`.
- `WSJF = CoD / Job Size`, também na mesma régua. Maior primeiro, **dentro do nível topológico**.
- **Criticidade Temporal aqui mede porta que se fecha**, não pressão de calendário: decisão que fica cara depois de existir arquivo gravado, ou depois de a API de terceiro congelar, pontua alto mesmo com valor baixo.
- **Ressalva declarada, e ela é importante para não ler o número errado:** nos grupos bloqueados por terceiro (integração com o formato, e aplicação), o WSJF é **ordenação relativa para o instante em que o bloqueio cair**, não custo de calendário. Não há como dizer o que custa uma semana de atraso quando o atraso não é nosso e não tem data.

## Bloqueios externos (não recebem WSJF nem Onda: priorizar fila de terceiro é teatro)

- **`EXT-1` Formato de mapa v1 publicado pelo GlintFx**, leitor E escritor públicos. Sem data. Trava o grupo `FMT-*`. **O que já foi conquistado:** UUID estável de objeto e de mapa, rotação livre, lista de volumes por objeto, bit separado para bloquear busca de caminho, canal de propriedades nomeadas, e preservação de bloco desconhecido ao regravar com bit "seguro de copiar".
- **`EXT-2` GlintFx expõe janela, desenho e entrada.** Sem data. Trava **todo** o grupo `APP-*` e o `DES-1`. Hoje o `src` deles tem três arquivos.

## Achados das lentes que o líder precisa decidir (não decididos por agente)

- **Falta possivelmente uma decisão sobre teste baseado em propriedade** (ferramenta pronta ou geração própria com semente fixa), distinta da `DEC-2`. Apontado pela lente de engenharia. **Vai ao líder** decidir se vira item próprio.
- **Duas escolhas técnicas de `COR-7` mudam o tamanho da bateria de teste** e não foram tomadas: a tolerância de ponto flutuante para comparar área, e se o teste soma as áreas das peças ou reconstrói a união geométrica. Decidir antes de escrever o teste, não depois.

## Vocabulário de Status (fechado)

- **✅ Concluído**, **🔄 Em andamento**, **🟡 Parcial**, **⏳ Pendente**, **💡 Decisão tomada**, **🎨 Pendente design** (aguarda decisão do líder, não pode ser puxado), **🔍 Pendente verificação** (implementado, aguarda validação).
- Regra de trânsito: implementação entregue vira **🔍**, nunca **✅** direto. **✅** só depois do teste ou da auditoria correspondente passar.

## Fundação já entregue em 22/08/2026 (registro, não pendência)

Leis em `GODS_LAWS.md`; licença AGPL-3.0-or-later com política SPDX; `README.md` público declarando o estado real; `BRIEFING.md`; poda e reescrita dos cinco manuais; CI nos cinco alvos com dois portões próprios e autoteste de quatro controles; hook do bus; repositório publicado.

## INBOX

Vazia.

## TABELA UNIFICADA

| WSJF | ID | Onda | Grupo | Descrição Técnica | Prioridade | Pré-requisito | Dificuldade | Status | Estado Auditado |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| 11.5 | DEC-1 | W0 | Decisão | Nome dos diretórios de camada. **Decidido em 22/08/2026: `domain/`, `application/`, `platform/`, em inglês** (`L-12`). Coerente com o portão de CI já entregue e sem acento em caminho no alvo Windows. | Alta | — | Baixa | 💡 Decisão tomada | — |
| 4.7 | DEC-2 | W0 | Decisão | Framework de teste unitário. **Decidido em 22/08/2026: harness próprio, sem Catch2 e sem biblioteca de teste de terceiro** (`L-09`). O líder recusou também a saída de abrir exceção na `L-01`: "terceiro que não conta" é como dependência volta a entrar. | Alta | — | Média | 💡 Decisão tomada | — |
| 12.0 | COR-1 | W1 | Núcleo | Scaffolding CMake C++23 e harness de teste rodando nos cinco alvos. Destrava literalmente todo o resto do núcleo. | Alta | DEC-1, DEC-2 | Média | ⏳ Pendente | — |
| 5.8 | COR-2 | W2 | Núcleo | Modelo de documento de edição: mapa carregado mais estado de autoria. Domínio POCO puro, zero GlintFx, zero sistema operacional (`L-12`). | Alta | COR-1 | Média | ⏳ Pendente | — |
| 1.6 | COR-7 | W2 | Núcleo | Repartir polígono côncavo em pedaços convexos ao salvar. Caiu no nosso colo por decisão de fronteira do GlintFx. Classe de código que falha em silêncio: nasce com ida e volta, conservação de área e verificação de convexidade de cada peça. | Média | COR-1 | Alta | ⏳ Pendente | — |
| 15.3 | COR-3 | W3 | Núcleo | Comando com pilha linear de histórico (`L-13`). Nasce serializável e sem árvore. Toda operação futura é um comando; decidir isso depois da primeira operação obriga a reescrevê-la. | Alta | COR-2 | Média | ⏳ Pendente | — |
| 10.5 | COR-8 | W3 | Núcleo | Seleção como estado de sessão, fora do histórico (`L-13`). Desacoplar depois seria retrabalho na pilha inteira. | Alta | COR-2 | Baixa | ⏳ Pendente | — |
| 8.7 | COR-9 | W4 | Núcleo | Modelo de ferramenta (pincel, seleção, transformação) sem nenhuma interface. É o que permite provar que a edição funciona sem uma linha de GlintFx. | Alta | COR-3, COR-8 | Média | ⏳ Pendente | — |
| 8.0 | COR-4 | W4 | Núcleo | Transação explícita por gesto: arrastar o pincel por quarenta células é **um** passo de desfazer. O caro é o gesto abortado no meio, não o caminho feliz. | Alta | COR-3 | Média | ⏳ Pendente | — |
| 4.3 | COR-5 | W4 | Núcleo | Serialização versionada de comando, exigida pelo histórico persistido (`L-13`). Terceiro contrato de dado do projeto, sem prior art: nenhum editor grande persiste histórico. | Alta | COR-3 | Alta | ⏳ Pendente | — |
| 4.2 | COR-6 | W5 | Núcleo | Impressão digital do mapa gravada no histórico e recusa graciosa de reaplicar quando o mapa mudou por fora. Sem ela, o histórico persistido corrompe o documento em silêncio. | Média | COR-5 | Média | ⏳ Pendente | — |
| 3.7 | COR-11 | W5 | Núcleo | Recálculo de redimensionamento de mapa. **É trabalho nosso** por decisão do GlintFx (item 8): a lib só fixa a convenção de coordenada na especificação, porque redimensionar é operação de autoria e não de mecanismo. Sem isto, crescer o mapa desloca objeto para fora sem o autor perceber. | Média | COR-2 | Média | ⏳ Pendente | — |
| 3.6 | COR-10 | W5 | Núcleo | Herança de tipo com marca de sobrescrita por instância, chaveada por UUID de instância. **É trabalho nosso** por decisão do GlintFx (item 7): o formato guarda instâncias resolvidas mais referência de tipo opaca, e a herança fica no editor. Sem a marca, ao reabrir não se sabe se o valor foi escolhido pelo autor ou herdado, e a próxima mudança de tipo sobrescreve o trabalho dele. | Alta | COR-2 | Média | ⏳ Pendente | — |
| 3.0 | FMT-5 | W6 | Formato | Arquivo de projeto do editor ao lado do mapa: histórico persistido, notas de autoria, configuração de grade. Nunca dentro do formato do GlintFx (`L-03`). **Não depende de EXT-1**: o formato é nosso. | Alta | COR-6 | Alta | ⏳ Pendente | — |
| 2.3 | FMT-7 | W7 | Formato | Agrupamento de objetos da sessão de edição, no nosso arquivo ao lado. **Fica fora do formato** por decisão do GlintFx (item 9): grupo de sessão é do editor; grupo que o jogo precisa em runtime vai no canal de propriedades deles. | Baixa | FMT-5 | Média | ⏳ Pendente | — |
| 8.0 | FMT-1 | W7 | Formato | Abrir mapa pelo leitor público do GlintFx. Primeira vez que o editor toca um mapa real: valida ou derruba tudo que COR-2 supôs. Dispara a `L-02`. | Alta | EXT-1, COR-2 | Média | ⏳ Pendente | — |
| 9.0 | FMT-6 | W8 | Formato | Validação de teleporte entre mapas: o destino aponta para um mapa que existe. Viável porque o destino é endereço direto por UUID de mapa. | Média | FMT-1 | Baixa | ⏳ Pendente | — |
| 5.2 | FMT-2 | W8 | Formato | Gravar pelo escritor público do GlintFx. Fecha o ciclo abrir, editar, salvar. Sai errado em silêncio se COR-7 não estiver pronto e testado antes. | Alta | FMT-1, COR-7 | Média | ⏳ Pendente | — |
| 7.0 | HL-1 | W9 | Headless | **Modo headless**: abrir, validar, transformar e gravar mapa por linha de comando, sem janela (`L-16`). Depende do formato, **não** da janela. É o que torna o papel de implementador de referência verificável, porque permite exercitar o formato no CI dos cinco alvos a cada commit. | Alta | FMT-2, COR-9 | Média | ⏳ Pendente | — |
| 8.0 | FMT-4 | W10 | Formato | Portão de ida e volta byte a byte: abrir, salvar sem mudar nada, comparar. A `L-09` exige que nasça junto com a leitura e a escrita, não depois. Roda **por dentro do modo headless**, nos cinco alvos. | Alta | FMT-1, FMT-2, HL-1 | Média | ⏳ Pendente | — |
| 4.2 | FMT-3 | W9 | Formato | Preservar bloco desconhecido ao regravar, honrando o bit "seguro de copiar". Exigência normativa do formato, conquistada por pedido nosso. Sem ela, salvar num editor desatualizado destrói dado alheio sem aviso. | Alta | FMT-2 | Média | ⏳ Pendente | — |
| 9.7 | APP-1 | W10 | Aplicação | Janela e laço principal sobre a API do GlintFx. Primeira vez que o editor existe como programa visível. | Alta | EXT-2 | Média | ⏳ Pendente | — |
| 0.8 | DES-1 | W10 | Design | Desenho da tela em alta fidelidade (o WYSIWYG). Espera o GlintFx ter janela, por ordem do líder e contra a recomendação registrada. Enquanto não for feito, não temos a lista de recursos de interface a pedir a eles. | Média | EXT-2 | Alta | 🎨 Pendente design | — |
| 6.3 | APP-2 | W11 | Aplicação | Viewport da grade com câmera enquadrando o conteúdo. Armadilha conhecida: câmera padrão centra a origem do mundo, não o conteúdo. | Alta | APP-1, DES-1 | Média | ⏳ Pendente | — |
| 5.2 | APP-3 | W12 | Aplicação | Pintura de terreno na grade, uma camada (`L-14`). Primeiro fluxo interativo de ponta a ponta: une câmera, entrada, comando e transação num só gesto. | Alta | APP-2, COR-4 | Média | ⏳ Pendente | — |
| 4.2 | APP-7 | W12 | Aplicação | Painéis (inspetor, paleta, lista de objetos) assinando o sinal do histórico, sem cópia própria de estado. Implementado errado uma vez, é difícil de erradicar: o defeito documentado aparece na seleção múltipla. | Alta | APP-2, COR-3 | Média | ⏳ Pendente | — |
| 5.2 | APP-4 | W13 | Aplicação | Posicionar objeto e transformá-lo: rotação e escala em ponto flutuante, conforme o formato aceita. | Alta | APP-3, DEC-3 | Média | ⏳ Pendente | — |
| 3.6 | APP-5 | W13 | Aplicação | Edição dos seis tipos de volume da `L-14`, com lista de volumes por objeto. Dois dos seis dependem de `EXT-5`. | Alta | APP-3, EXT-5 | Alta | ⏳ Pendente | — |
| 3.0 | APP-6 | W13 | Aplicação | Abas multi-mapa com histórico único compartilhado, e troca automática de aba quando o desfazer alterar um mapa que não é o da aba ativa. A troca é mitigação **obrigatória** pela `L-14`. | Alta | APP-3, COR-3 | Alta | ⏳ Pendente | — |
| 4.3 | APP-8 | W14 | Aplicação | Exibir o diagnóstico do GlintFx (escala desigual em forma redonda) na interface **antes** de salvar, enquanto o autor ainda pode consertar. | Média | APP-5 | Média | ⏳ Pendente | — |
| 2.5 | DEC-3 | W14 | Decisão | Menu de transformação do objeto na interface: rotação, aumento, redução. Pode esperar sem custo porque não existe tela onde desenhá-lo. | Baixa | DES-1 | Baixa | 🎨 Pendente design | — |
| 2.6 | TST-1 | W15 | Testes | Testes não unitários conforme o `TESTES.md` deste projeto: estática, propriedade, sanitizers, segredos, CVE, ida e volta, espelho local de CI e headless, nos cinco alvos. Teste unitário não é item: anda dentro da fatia. | Alta | APP-8, FMT-4 | Alta | ⏳ Pendente | — |
| 5.3 | AUD-1 | W16 | Auditoria | Auditorias conforme o `AUDITORIAS.md` deste projeto: fronteira de camadas, integridade do arquivo gravado, histórico persistido, fronteira com o GlintFx, escopo. Por `L-06`, C-level em fable, e implementador nunca audita o próprio trabalho. | Alta | TST-1 | Média | ⏳ Pendente | — |
| 0.8 | WIKI | W17 | Documentação | Wiki do repositório mais documentação extensa em registro didático para iniciante em computação, explicando todo jargão sem assumir conhecimento. Item fixo de fim de tabela. | Baixa | AUD-1 | Alta | ⏳ Pendente | — |
