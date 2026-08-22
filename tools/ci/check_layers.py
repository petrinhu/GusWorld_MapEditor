#!/usr/bin/env python3
# SPDX-License-Identifier: AGPL-3.0-or-later
"""
tools/ci/check_layers.py

Portao de CI: regra de dependencia entre camadas (GODS_LAWS.md L-12).

    1. domain      -- POCO puro. NUNCA inclui application nem platform.
    2. application -- caso de uso. NUNCA inclui header do GlintFx.
    3. platform    -- casca fina. UNICA camada autorizada a incluir GlintFx.

A camada de um arquivo e decidida pelo NOME DO DIRETORIO que o contem
(qualquer componente do caminho, sem diferenciar maiuscula, igual a
"domain", "application" ou "platform" -- ver layer_common.classify_layer).
Isto e deliberado: nao existe ainda uma convencao de onde o codigo mora
(GODS_LAWS.md L-11, projeto do zero), entao o portao nao assume um layout
de topo especifico (nem `src/domain/`, nem `domain/`, nem `libs/x/domain/`)
-- ele reconhece a camada onde quer que ela apareca na arvore.

GODS_LAWS.md L-09, regra que motivou esta tarefa: um portao que varre ZERO
arquivos e imprime verde e indistinguivel de um portao que olhou e nao
achou nada. Este script SEMPRE declara quantos arquivos varreu por camada.

TRAVA decidida pelo lider em 22/08/2026, depois de ver o job "leis" vermelho
por dias (raciocinio dele: CI vermelho por meses treina todo mundo a
ignorar vermelho, e ai o vermelho de verdade passa batido). O gatilho da
trava e a EXISTENCIA DE DIRETORIO (domain/ ou application/ ou platform/ em
qualquer lugar da arvore -- layer_common.any_layer_dir_exists), nao a
contagem de arquivo, para nao ter buraco: criar `domain/` so com um `.md`
dentro nao muda o total de arquivo C++, mas MUDA a existencia do diretorio,
e a trava tem de perceber isso.

    - NENHUMA das tres pastas existe em lugar nenhum da arvore E total==0:
      Exit 0. Este e o caminho "ainda nao ha o que auditar" -- a mensagem
      NUNCA afirma "OK", "limpo" ou "sucesso", porque nao houve verificacao
      nenhuma, so ausencia de alvo (GODS_LAWS.md L-11).
    - QUALQUER uma das tres pastas existe (vazia ou nao) E total==0:
      Exit 1. A pasta de camada existe e mesmo assim nada foi varrido --
      sintoma de filtro quebrado ou arvore incoerente, exatamente a mesma
      semantica de "varrer zero e falha" que valia antes da trava.
    - total > 0: segue a checagem de violacao de dependencia normalmente,
      trava nao entra em jogo.

Uso:
    python3 tools/ci/check_layers.py [RAIZ]

RAIZ default: diretorio de trabalho atual (a raiz do repo, em CI).
Exit 0 = nenhuma das tres pastas de camada existe ainda (nada a verificar),
         OU pelo menos um arquivo por camada foi varrido e nenhuma violacao.
Exit 1 = uma pasta de camada existe mas 0 arquivo foi varrido dentro dela,
         OU violacao de dependencia.
"""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from layer_common import (  # noqa: E402
    any_layer_dir_exists,
    classify_layer,
    extract_includes,
    find_layer_dirs,
    iter_cpp_files,
    path_segments,
)


def _violation_str(file: Path, line_no: int, msg: str) -> str:
    return f"VIOLACAO {file}:{line_no}: {msg}"


def run(root: Path) -> tuple[int, list[str]]:
    """Devolve (total_arquivos_de_camada, lista_de_violacoes_formatadas).
    Tambem imprime o resumo de contagem -- e a parte que L-09 exige."""
    counts = {"domain": 0, "application": 0, "platform": 0}
    violations: list[str] = []

    for f in iter_cpp_files(root):
        layer = classify_layer(f, root)
        if layer is None:
            continue
        counts[layer] += 1

        includes = extract_includes(f)

        if layer == "domain":
            for inc in includes:
                segs = path_segments(inc.path)
                if "application" in segs:
                    violations.append(_violation_str(
                        f, inc.line_no,
                        f'domain inclui "{inc.path}" (camada application) -- '
                        "proibido por GODS_LAWS.md L-12: dominio e POCO puro.",
                    ))
                elif "platform" in segs:
                    violations.append(_violation_str(
                        f, inc.line_no,
                        f'domain inclui "{inc.path}" (camada platform) -- '
                        "proibido por GODS_LAWS.md L-12: dominio e POCO puro.",
                    ))

        elif layer == "application":
            for inc in includes:
                segs = path_segments(inc.path)
                if "glintfx" in segs:
                    violations.append(_violation_str(
                        f, inc.line_no,
                        f'application inclui "{inc.path}" (header do GlintFx) -- '
                        "proibido por GODS_LAWS.md L-12: so platform pode "
                        "incluir GlintFx direto.",
                    ))

        # platform: nenhuma regra de camada aqui. A proibicao de dependencia
        # de terceiro fora do GlintFx e do escopo do OUTRO portao
        # (check_allowed_includes.py, GODS_LAWS.md L-01).

    total = sum(counts.values())
    print(
        f"check_layers: domain={counts['domain']} arquivos, "
        f"application={counts['application']} arquivos, "
        f"platform={counts['platform']} arquivos, total={total}"
    )
    return total, violations


def main(argv: list[str]) -> int:
    root = Path(argv[1]) if len(argv) > 1 else Path(".")
    if not root.exists():
        print(f"check_layers: ERRO: raiz '{root}' nao existe.", file=sys.stderr)
        return 1

    total, violations = run(root)

    if total == 0:
        dirs_found = find_layer_dirs(root)
        if not any_layer_dir_exists(root):
            print(
                "check_layers: NADA A VERIFICAR -- 0 arquivos de camada "
                "varridos e NENHUMA das pastas domain/application/platform "
                f"existe ainda em lugar nenhum de '{root}'. Isto NAO e uma "
                "verificacao bem-sucedida: e ausencia de alvo (GODS_LAWS.md "
                "L-11, projeto do zero). Decisao do lider em 22/08/2026: "
                "este caminho sai 0 SO enquanto nenhuma das tres pastas "
                "existir; no instante em que uma aparecer, varrer zero "
                "arquivos volta a ser falha."
            )
            return 0
        existentes = ", ".join(
            f"{nome} ({len(paths)} dir.)" for nome, paths in dirs_found.items() if paths
        )
        print(
            "check_layers: FALHA -- ha pasta de camada existindo "
            f"({existentes}) mas 0 arquivo de codigo C++ foi varrido dentro "
            f"delas sob '{root}'. Isto NAO e o caminho \"projeto ainda nao "
            "comecou\" (GODS_LAWS.md L-11): a pasta ja existe, entao isto e "
            "sintoma de filtro de extensao errado, pasta so com arquivo que "
            "nao casa (ex.: um .md dentro de domain/), ou arvore quebrada. "
            "GODS_LAWS.md L-09 continua valendo aqui: varrer zero, com "
            "pasta existindo, e falha, nao sucesso.",
            file=sys.stderr,
        )
        return 1

    if violations:
        print(f"check_layers: FALHA -- {len(violations)} violacao(oes):", file=sys.stderr)
        for v in violations:
            print(v, file=sys.stderr)
        return 1

    print("check_layers: OK -- nenhuma violacao de camada (GODS_LAWS.md L-12).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
