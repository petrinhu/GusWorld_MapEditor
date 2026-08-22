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
achou nada. Por isso este script SEMPRE declara quantos arquivos varreu
por camada, e VARRER ZERO NO TOTAL E FALHA, nao sucesso -- hoje (2026-08-22)
isso significa que este job sai vermelho, porque o codigo de aplicacao
ainda nao existe (GODS_LAWS.md L-11/L-12). E o comportamento certo: melhor
vermelho e honesto do que verde e mentiroso.

Uso:
    python3 tools/ci/check_layers.py [RAIZ]

RAIZ default: diretorio de trabalho atual (a raiz do repo, em CI).
Exit 0 = pelo menos um arquivo por camada foi varrido e nenhuma violacao.
Exit 1 = zero arquivos de camada varridos, OU violacao de dependencia.
"""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from layer_common import (  # noqa: E402
    classify_layer,
    extract_includes,
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
        print(
            "check_layers: FALHA -- 0 arquivos de camada (domain/application/"
            "platform) encontrados sob "
            f"'{root}'. GODS_LAWS.md L-09: varrer zero arquivos NUNCA e "
            "sucesso. Se o codigo de aplicacao ainda nao existe "
            "(GODS_LAWS.md L-11), este vermelho e o comportamento ESPERADO, "
            "nao um bug do portao.",
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
