# CHECKLIST DE RELEASE (gusworld_mapeditor)

> Este editor é uma aplicação desktop local, de usuário único, distribuída como binário via
> GitHub Releases (L-07: AGPL-3.0-or-later, junto com o GlintFx). Não há servidor, banco de
> dados, migração de schema, autenticação nem tráfego em produção: o checklist genérico de
> deploy irreversível (blue-green, shadow traffic, dual write, 2FA, HSTS) não se aplica e foi
> substituído pelo fluxo abaixo, adequado a publicação de um artefato binário multiplataforma.
> **Precedência:** [`GODS_LAWS.md`](GODS_LAWS.md) vence este checklist em qualquer conflito.

---

## O que torna uma release irreversível aqui

Não existe "produção" para fazer rollback. O ponto de não-retorno é outro: **assim que a tag é
publicada e o artefato anexado ao GitHub Release, usuários podem baixar** -- não dá para
"desfazer" um download que já aconteceu. Qualquer correção pós-publicação sai como release nova,
nunca como reescrita da tag.

---

## FASE 0  -  Classificação

- [ ] Toda release pública deste projeto e, por definição, o evento irreversível (não ha
      gradação de "só um pouco em produção"): trate toda tag publicada com o mesmo cuidado.
- [ ] Mudança no formato de mapa consumido (o formato é do GlintFx, L-03): confirmar que a
      versão do GlintFx pinada neste release já publicou e testou essa mudança do lado deles.

---

## FASE 1  -  Pré-condições de Qualidade

- [ ] CI verde nos cinco alvos (L-10): Fedora 44 (primário, pinado), Ubuntu, Arch, CachyOS, Windows.
- [ ] TESTES.md T1, T2, T3, T4, T8, T12, T14, T16, T17 completos e verdes.
- [ ] AUDITORIAS.md seções 1-7 sem item CRITICO em aberto.
- [ ] Nenhuma violação pendente de GODS_LAWS.md, checada explicitamente contra L-01, L-03, L-04, L-12.
- [ ] GlintFx pinado em versão publicada e testada (nunca `main`/`latest`).

---

## FASE 2  -  Build dos Artefatos

- [ ] Binário gerado e fumaça-testado (abre, cria mapa vazio, fecha sem crash) em cada um dos
      cinco alvos antes de anexar a release.
- [ ] Round-trip de arquivo (TESTES.md T14) confirmado no binário final de cada plataforma, não
      só no build de desenvolvimento.

---

## FASE 3  -  Publicação

- [ ] Tag semver (`vX.Y.Z`), seguindo o versionamento combinado com o GlintFx.
- [ ] Release notes citam os IDs do `TODO.md` fechados nesta release.
- [ ] Artefatos dos cinco alvos anexados ao GitHub Release.
- [ ] Licença AGPL-3.0-or-later presente em cada artefato distribuído (LICENSE + cabeçalho SPDX,
      L-07).
- [ ] Push, tag e publicação autorizados explicitamente pelo líder nesta sessão (autorização
      anterior não vale para sempre).

---

## FASE 4  -  Pós-Release

- [ ] `TODO.md` atualizado: itens fechados nesta release marcados, nunca `OK` direto sem a onda
      de verificação (ver convenção de frescor da tabela de pendências).
- [ ] Prompt de limpeza de pastas de build oferecido ao usuário (CONTRACT.md §11, Post-Release
      Cleanup Prompt).
- [ ] Se um bug for encontrado após a publicação, a correção sai como release nova: a tag
      publicada nunca e reescrita nem apagada.
