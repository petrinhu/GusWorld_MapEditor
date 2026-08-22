# Auditorias Técnicas (gusworld_mapeditor)

> Checklists operacionais de auditoria para este editor de mapa desktop, local, C++23 sem Qt,
> sobre o GlintFx. Cada item tem prioridade **CRÍTICO / IMPORTANTE / COSMÉTICO** (ver
> [TESTES.md, Classificação de Problemas](TESTES.md#classificação-de-problemas)).
> **Precedência:** [`GODS_LAWS.md`](GODS_LAWS.md) vence este guia em qualquer conflito.

**Lembrete permanente (L-06, verbatim do líder):** "main apenas orquestra, interage comigo e
dispara agentes. Auditorias apenas com clevel bigtech fable, trabalhadores sonnet bigtech."
Toda auditoria abaixo é conduzida por um C-level em modelo fable; a implementação auditada foi
feita por um agent operacional em modelo sonnet; **o implementador nunca audita o próprio
trabalho**. O relatório de um agente não é prova: quem recebe o relatório reconfere build limpo
e faz spot-check das afirmações contra arquivo e linha antes de aceitar.

---

## Índice

1. [Arquitetura e Camadas (L-12)](#1-arquitetura-e-camadas-l-12)
2. [Integridade do Arquivo de Mapa (L-03)](#2-integridade-do-arquivo-de-mapa-l-03)
3. [Histórico Persistido (L-13)](#3-histórico-persistido-l-13)
4. [Fronteira com o GlintFx (L-01)](#4-fronteira-com-o-glintfx-l-01)
5. [Escopo do Editor (L-04, L-14)](#5-escopo-do-editor-l-04-l-14)
6. [Qualidade de Código Geral](#6-qualidade-de-código-geral)
7. [Robustez de Entrada](#7-robustez-de-entrada)
8. [Relatório Final](#8-relatório-final)

---

## 1. Arquitetura e Camadas (L-12)

🔴 **CRÍTICO**

- [ ] Nenhum arquivo de domínio inclui header de aplicação, casca de plataforma, GlintFx ou do SO.
- [ ] Nenhum arquivo de aplicação inclui header de GlintFx ou do SO.
- [ ] Só a casca de plataforma inclui header de GlintFx, e o chama direto, sem interface própria.
- [ ] O portão automático que checou isso declarou `Arquivos varridos: N` com `N > 0` (L-09; ver TESTES.md seção 0).
- [ ] Nenhuma dependência circular entre módulos.
- [ ] Nenhum "serviço-deus" na aplicação com dezenas de casos de uso; um caso de uso por operação de edição.

🟠 **IMPORTANTE**

- [ ] Classes de domínio não excedem ~300 linhas sem justificativa.
- [ ] Nenhuma interface virtual criada na fronteira com o GlintFx sem razão concreta e presente registrada (CONTRACT.md §5).

---

## 2. Integridade do Arquivo de Mapa (L-03)

🔴 **CRÍTICO**

- [ ] Round-trip byte a byte passou (TESTES.md T14): gravar → ler → comparar, e gravar duas vezes → arquivos idênticos.
- [ ] Nenhum campo próprio do editor foi infiltrado no formato `.gmap` do GlintFx; qualquer necessidade adicional foi resolvida em arquivo ao lado (histórico, nota de autor), nunca dentro do formato deles.
- [ ] Identificador estável (UUID) de cada objeto nunca é reescrito nem reciclado após exclusão (dependência da L-13 resolvida pelo GlintFx).
- [ ] Repartição de polígono côncavo em peças convexas passou nos dois testes de T17: ida e volta (área preservada) e convexidade de cada peça gerada.

🟠 **IMPORTANTE**

- [ ] Nenhuma suposição sobre a forma de um recurso do GlintFx que ainda não existe (ex.: desenho de porta) foi hardcoded na casca antes da API real.

---

## 3. Histórico Persistido (L-13)

🔴 **CRÍTICO**

- [ ] Cada comando e serializável e desfaz corretamente o que aplicou.
- [ ] Um gesto contínuo (ex.: arrastar o pincel por várias células) vira **um** passo de desfazer, agrupado por transação explícita que abre no início e fecha no fim do gesto, nunca por heurística.
- [ ] Seleção e câmera ficam fora do histórico (são estado de sessão, não de conteúdo).
- [ ] O arquivo de histórico grava uma impressão digital do mapa e recusa reaplicar se o mapa mudou por fora.
- [ ] Vistas assinam os sinais do histórico e não guardam cópia própria do estado (nenhum caminho de atualização paralelo).
- [ ] Com várias abas abertas (L-14): quando um passo de desfazer/refazer afeta um mapa que não é o da aba ativa, o editor troca a aba automaticamente para o mapa afetado.

---

## 4. Fronteira com o GlintFx (L-01)

🔴 **CRÍTICO**

- [ ] Zero `#include` de RmlUi, SDL, GLFW, Qt ou qualquer terceiro em qualquer arquivo do projeto.
- [ ] Zero chamada direta ao sistema operacional (janela, arquivo bruto de SO, entrada) fora da API do GlintFx.
- [ ] Toda funcionalidade que a API pública do GlintFx não cobre foi registrada como pedido pelo bus (`gusworld_ia_autocomm`), nunca contornada com implementação própria.

---

## 5. Escopo do Editor (L-04, L-14)

🟠 **IMPORTANTE**

- [ ] Nenhuma feature de carta, item ou NPC do jogo vazou para o editor (L-04).
- [ ] Só os seis tipos de volume de colisão definidos na L-14 existem; nenhum tipo extra (hitbox de combate, zona de câmera, zona de audio) foi adicionado sem nova lei do líder.
- [ ] Só uma camada de terreno pintada mais objetos livres por cima; nenhuma camada de pintura sobreposta adicional.
- [ ] Nenhuma tentativa de desenhar a tela (WYSIWYG) antes do GlintFx ter janela (L-14, item 4) -- se isso apareceu, e violação de ordem direta do líder, não decisão técnica.

---

## 6. Qualidade de Código Geral

🟠 **IMPORTANTE / 🟢 COSMÉTICO**

- [ ] SOLID respeitado (CONTRACT.md §3): nenhuma classe com mais de uma razão para mudar.
- [ ] DRY, regra de três (CONTRACT.md §6.7): nenhuma abstração criada antes da terceira ocorrência real.
- [ ] Funções <= 40 linhas, <= 4 parâmetros, <= 3 níveis de aninhamento.
- [ ] Nomes revelam intenção; comentários explicam o porquê, não o que.
- [ ] Nenhum `new`/`delete` manual fora de RAII.

---

## 7. Robustez de Entrada

🟠 **IMPORTANTE**

- [ ] Arquivo de mapa corrompido não crasha o editor: falha explícita, tratada, reportada.
- [ ] Arquivo de histórico corrompido ou desatualizado não crasha o editor: recusa reaplicar, não adivinha.
- [ ] Entrada de usuário em campo do inspetor é validada antes de chegar ao domínio.
- [ ] Nenhuma credencial ou token hardcoded (baixa probabilidade neste projeto, mantido por higiene, ver CONTRACT.md §8.2).

---

## 8. Relatório Final

**Entregável obrigatório:** documento com score global (0-100), lista de problemas por prioridade
(🔴/🟠/🟢) e patches unificados (formato descrito em [TESTES.md, Formato de Patch](TESTES.md#formato-de-patch)).

Produzido por um C-level em modelo fable (L-06); nunca pelo agente que implementou o código
auditado. Antes de aceitar o relatório, o orquestrador reconfere o build e faz spot-check de pelo
menos três afirmações do relatório contra arquivo e linha reais.
