# GusWorld Map Editor

Editor de mapas do jogo [GusWorld](https://github.com/petrinhu/GusWorld). Aplicação de desktop em C++23, para Linux e
Windows, software livre.

## Estado real do projeto

Este repositório está na fundação. **Ainda não existe código de aplicação.**
O que existe hoje é governança: leis do líder, contrato do projeto, política
de teste e de CI, e este par de arquivos de licenciamento.

O motivo é concreto, não é atraso de trabalho: o editor se assenta
exclusivamente sobre o framework [GlintFx](https://github.com/petrinhu/GlintFx),
que foi reiniciado do zero em 21/08/2026 e ainda não expõe janela, desenho
nem entrada. Sem essas três coisas na API pública do GlintFx, não há sobre o
que construir a interface do editor. Este README não promete data para isso
mudar.

## Como isto se relaciona com o resto

- **GlintFx** é o framework de base: janela, desenho, entrada, e também o
  dono do formato de arquivo de mapa (leitor e escritor públicos).
- **GusWorld** é o jogo que consome esse formato em tempo de execução.
- **Este editor** é a ferramenta de autoria desse formato: abre, edita e
  grava mapas, sem duplicar nem reinterpretar o que o GlintFx já define.

## O que já está decidido

Decisões abaixo vêm de `GODS_LAWS.md` (leis do líder, que têm precedência
sobre qualquer outro documento deste repositório).

- **Escopo:** o editor edita só mapa: grade de células, objetos posicionados,
  hitbox, portas e pontos de teleporte. Carta, item e NPC do jogo ficam de
  fora, porque são conteúdo do jogo, não do mapa.
- **Formato de arquivo:** pertence ao GlintFx. Este projeto é consumidor do
  formato, nunca autor concorrente dele; necessidade nova vira pedido ao
  GlintFx, não campo decidido aqui.
- **Camada de mapa:** uma camada de terreno pintada na grade, mais objetos
  posicionados livremente por cima em coordenada contínua. Sem camadas de
  pintura sobrepostas nesta versão.
- **Volumes de colisão:** seis tipos na primeira versão, a saber sólido,
  gatilho de ação, zona de dano, zona de terreno modificador, área de
  interação e obstáculo de navegação.
- **Múltiplos mapas:** vários mapas abertos ao mesmo tempo, em abas, cada um
  com câmera própria, porque o mundo do GusWorld liga áreas por teleporte e
  editar um portão exige ver os dois lados.
- **Desfazer e refazer:** por comando, com pilha linear (sem árvore de
  histórico). Uma intenção do autor é um passo de desfazer, agrupado por
  transação explícita. A seleção fica fora do histórico. O histórico
  persiste entre sessões, em arquivo próprio do editor ao lado do mapa,
  nunca dentro do formato do GlintFx, e é compartilhado por todas as abas
  (não um histórico por mapa).
- **Plataforma:** a aplicação se assenta exclusivamente na API pública do
  GlintFx. Nenhuma biblioteca de terceiro e nenhuma chamada direta ao sistema
  operacional.

## Licença

Distribuído sob **GNU Affero General Public License v3.0 ou posterior**
(`AGPL-3.0-or-later`), a mesma licença do GlintFx. Texto completo em
[`LICENSE`](LICENSE). Convenção de cabeçalho por arquivo de código em
[`NOTICE-SPDX.md`](NOTICE-SPDX.md).

Este programa é distribuído na esperança de que seja útil, mas **sem
qualquer garantia**, nem mesmo a garantia implícita de comercialização ou de
adequação a um propósito específico. Ver a licença para mais detalhes.

## Como construir

Não há nada para construir ainda: o repositório não contém código-fonte de
aplicação. Instruções de build vão aparecer aqui quando o primeiro alvo de
build existir, não antes.

## Como contribuir

O projeto ainda não aceita contribuição de código, pela mesma razão do
estado descrito acima. O trabalho corrente é de fundação e segue as leis em
`GODS_LAWS.md` e as normas do projeto em `CONTRACT.md`, `AGILE.md`,
`TESTES.md` e `TOOLING.md`.
