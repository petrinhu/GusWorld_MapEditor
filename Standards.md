# Standards e Manuais de Referência (gusworld_mapeditor)

Índice local dos manuais que regem este repositório. Não é um hub de vault: não referencia
outros projetos nem a estrutura PARA (Areas/Journal/Archive), que não existem aqui. Este é um
repositório público e independente (L-07).

## Autoridade

- [`GODS_LAWS.md`](GODS_LAWS.md): ordens expressas do líder. Vence qualquer manual abaixo em
  caso de conflito. Ler antes de agir, sempre que um gatilho da tabela lá dentro casar com a
  tarefa.

## Manuais de Execução (raiz)

- [`CONTRACT.md`](CONTRACT.md): padrões de código, SOLID, Clean Code, camadas (L-12), C++23 sem
  Qt, Git.
- [`TESTES.md`](TESTES.md): testes, portões de CI e auditoria (T1-T17, A2/A3/A10), adaptado ao
  stack único deste projeto (C++23 + GlintFx, cinco alvos de CI, L-10).
- [`AUDITORIAS.md`](AUDITORIAS.md): checklists de auditoria por prioridade (CRÍTICO/IMPORTANTE/
  COSMÉTICO), separação fable/sonnet (L-06).
- [`DEPLOY_CHECKLIST.md`](DEPLOY_CHECKLIST.md): checklist de release de aplicação desktop (sem
  produção/servidor).
- [`AGILE.md`](AGILE.md): metodologia ágil (não alterado nesta poda; cópia da referência do
  vault).

## Organização e Pipeline (constelação de agents)

- [`ORG.md`](ORG.md): governança, RACI, variantes de pipeline por porte.
- [`pipeline_release_1.0.md`](pipeline_release_1.0.md): pipeline de 12 fases (ideia ao 1.0).
- [`lideranca_pipeline_release.md`](lideranca_pipeline_release.md): teoria de liderança C-level.
- [`TOOLING.md`](TOOLING.md): ferramentas FOSS por agent.

## Como usar com Claude

Sessão nova neste repositório: o [`CLAUDE.md`](CLAUDE.md) da raiz aponta primeiro para
`GODS_LAWS.md`, depois para os manuais acima. Não há memória de vault aplicável aqui além da
convivência com o [`ecossistema GlintFx`](../GlintFx) (repositório irmão).
