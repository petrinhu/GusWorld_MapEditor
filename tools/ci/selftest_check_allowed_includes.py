#!/usr/bin/env python3
# SPDX-License-Identifier: AGPL-3.0-or-later
"""
tools/ci/selftest_check_allowed_includes.py

Autoteste de check_allowed_includes.py com CINCO controles (GODS_LAWS.md
L-09 + decisao do lider de 22/08/2026 sobre a TRAVA "verde declarando
zero", mesma exigencia do irmao selftest_check_layers.py; o quinto entrou
em 24/08/2026 com a decisao do lider sobre a REGRA DE CORTE da allowlist):

    1. POSITIVO -- planta dependencia proibida de tres formas (lib de
       terceiro fora de platform, lib de terceiro DENTRO de platform --
       prova que a excecao e SO para GlintFx, e um include entre aspas
       que nao resolve para arquivo real -- prova que citar entre aspas
       nao e um jeito de escapar da checagem).
    2. NEGATIVO -- arvore limpa (stdlib em qualquer camada, GlintFx so em
       platform, aspas apontando para arquivo que existe de verdade),
       prova que o portao nao acusa fantasma.
    3. VAZIO    -- diretorio sem NENHUMA pasta domain/application/platform
       e sem nenhum arquivo C++. Depois da trava, este e o caminho VERDE:
       prova que o portao sai 0 e nao afirma verificacao bem-sucedida
       (nunca a linha "check_allowed_includes: OK").
    4. TRAVA    -- prova as DUAS direcoes da trava, para as TRES pastas
       SEPARADAMENTE: (a) baseline sem pasta nenhuma -> exit 0, sem
       afirmar sucesso; (b) so a pasta <nome> existindo VAZIA, zero
       arquivo C++ no repo inteiro -> exit 1; (c) so a pasta <nome>
       existindo com um arquivo que NAO casa extensao C++ -> exit 1 --
       o buraco explicito apontado pelo lider.
    5. DECISAO  -- fixa a REGRA DE CORTE decidida pelo lider em 24/08/2026
       (auditoria do COR-1): <limits> ACEITO (entrou na allowlist por
       decisao), e os cinco headers que compilam em -std=c++23 mas ficaram
       fora POR DECISAO (<iso646.h>, <stdalign.h>, <stdbool.h>,
       <stdatomic.h>, <strstream>) continuam BARRADOS. Existe para ninguem
       "corrigir de volta" a lista achando que foi esquecimento -- ver o
       comentario REGRA DE CORTE em check_allowed_includes.py.

Uso:
    python3 tools/ci/selftest_check_allowed_includes.py
"""
from __future__ import annotations

import subprocess
import sys
import tempfile
from pathlib import Path

SCRIPT = Path(__file__).resolve().parent / "check_allowed_includes.py"


def _write(root: Path, rel: str, content: str) -> None:
    p = root / rel
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(content, encoding="utf-8")


def _run(root: Path) -> subprocess.CompletedProcess:
    return subprocess.run(
        [sys.executable, str(SCRIPT), str(root)],
        capture_output=True, text=True,
    )


def control_positivo() -> tuple[bool, str]:
    with tempfile.TemporaryDirectory(prefix="deps-positivo-") as td:
        root = Path(td)
        # 1) terceiro fora de platform.
        _write(root, "domain/mapa.cpp", "#include <SDL3/SDL.h>\n")
        # 2) terceiro DENTRO de platform, que nao e GlintFx -- a excecao
        #    de platform e so para GlintFx, nao para qualquer lib.
        _write(root, "platform/janela.cpp", "#include <GLFW/glfw3.h>\n")
        # 3) aspas apontando pra arquivo que nao existe -- nao pode ser
        #    um jeito de escapar da checagem de <angulo>.
        _write(root, "application/uso.cpp", '#include "nao/existe/de/verdade.hpp"\n')

        r = _run(root)
        ok = (
            r.returncode == 1
            and "<SDL3/SDL.h>" in r.stderr
            and "<GLFW/glfw3.h>" in r.stderr
            and '"nao/existe/de/verdade.hpp"' in r.stderr
        )
        detail = f"exit={r.returncode}\nstdout={r.stdout}\nstderr={r.stderr}"
        return ok, detail


def control_negativo() -> tuple[bool, str]:
    with tempfile.TemporaryDirectory(prefix="deps-negativo-") as td:
        root = Path(td)
        _write(root, "domain/mapa.hpp", "#include <vector>\n#include <memory>\n")
        _write(root, "application/uso.cpp", '#include "domain/mapa.hpp"\n#include <optional>\n')
        # GlintFx so e permitido em platform, e so via <angulo>.
        _write(root, "platform/janela.cpp", "#include <glintfx/core/version.hpp>\n")

        r = _run(root)
        ok = r.returncode == 0 and "OK" in r.stdout
        detail = f"exit={r.returncode}\nstdout={r.stdout}\nstderr={r.stderr}"
        return ok, detail


def control_vazio() -> tuple[bool, str]:
    with tempfile.TemporaryDirectory(prefix="deps-vazio-") as td:
        root = Path(td)
        # Diretorio existe mas nao tem nenhuma pasta domain/application/
        # platform e nao tem nenhum arquivo de extensao C++ (so um .md).
        # Com a TRAVA (decisao do lider, 22/08/2026), este e o caminho
        # VERDE: nao ha pasta de camada, entao 0 varrido e "nada a
        # verificar", nao falha.
        _write(root, "leia-me.md", "nada de codigo aqui\n")

        r = _run(root)
        ok = (
            r.returncode == 0
            and "NADA A VERIFICAR" in r.stdout
            and "check_allowed_includes: OK" not in r.stdout
        )
        detail = f"exit={r.returncode}\nstdout={r.stdout}\nstderr={r.stderr}"
        return ok, detail


def control_trava() -> tuple[bool, str]:
    """4o controle (exigencia do coordenador, 22/08/2026): prova as DUAS
    direcoes da trava, pastas domain/application/platform SEPARADAMENTE."""
    detalhes: list[str] = []
    ok_geral = True

    with tempfile.TemporaryDirectory(prefix="deps-trava-baseline-") as td:
        root = Path(td)
        r = _run(root)
        ok = (
            r.returncode == 0
            and "NADA A VERIFICAR" in r.stdout
            and "check_allowed_includes: OK" not in r.stdout
        )
        detalhes.append(f"baseline (sem pasta nenhuma): {'PASS' if ok else 'FAIL'} "
                         f"exit={r.returncode} stdout={r.stdout!r}")
        ok_geral = ok_geral and ok

    for nome in ("domain", "application", "platform"):
        with tempfile.TemporaryDirectory(prefix=f"deps-trava-{nome}-vazia-") as td:
            root = Path(td)
            (root / nome).mkdir(parents=True)
            r = _run(root)
            ok = r.returncode == 1 and "pasta de camada existindo" in r.stderr
            detalhes.append(f"{nome}/ vazia: {'PASS' if ok else 'FAIL'} "
                             f"exit={r.returncode} stderr={r.stderr!r}")
            ok_geral = ok_geral and ok

        with tempfile.TemporaryDirectory(prefix=f"deps-trava-{nome}-md-") as td:
            root = Path(td)
            _write(root, f"{nome}/leia.md", "nada de codigo aqui\n")
            r = _run(root)
            ok = r.returncode == 1 and "pasta de camada existindo" in r.stderr
            detalhes.append(f"{nome}/leia.md (nao casa extensao): {'PASS' if ok else 'FAIL'} "
                             f"exit={r.returncode} stderr={r.stderr!r}")
            ok_geral = ok_geral and ok

    return ok_geral, "\n".join(detalhes)


def control_decisao() -> tuple[bool, str]:
    """5o controle (decisao do lider, 24/08/2026, apos a auditoria
    adversarial do COR-1): prova as DUAS direcoes da REGRA DE CORTE da
    allowlist -- <limits> aceito, e cada um dos cinco headers excluidos
    POR DECISAO barrado com violacao nomeada."""
    detalhes: list[str] = []
    ok_geral = True

    with tempfile.TemporaryDirectory(prefix="deps-decisao-limits-") as td:
        root = Path(td)
        _write(root, "domain/limites.cpp", "#include <limits>\n")
        r = _run(root)
        ok = r.returncode == 0 and "OK" in r.stdout
        detalhes.append(f"<limits> aceito: {'PASS' if ok else 'FAIL'} "
                         f"exit={r.returncode} stdout={r.stdout!r} stderr={r.stderr!r}")
        ok_geral = ok_geral and ok

    for header in ("iso646.h", "stdalign.h", "stdbool.h", "stdatomic.h", "strstream"):
        with tempfile.TemporaryDirectory(prefix="deps-decisao-barrado-") as td:
            root = Path(td)
            _write(root, "domain/uso.cpp", f"#include <{header}>\n")
            r = _run(root)
            ok = r.returncode == 1 and f"<{header}>" in r.stderr
            detalhes.append(f"<{header}> barrado: {'PASS' if ok else 'FAIL'} "
                             f"exit={r.returncode} stderr={r.stderr!r}")
            ok_geral = ok_geral and ok

    return ok_geral, "\n".join(detalhes)


def main() -> int:
    controles = [
        ("positivo", control_positivo),
        ("negativo", control_negativo),
        ("vazio", control_vazio),
        ("trava", control_trava),
        ("decisao", control_decisao),
    ]
    falhou = False
    for nome, fn in controles:
        ok, detail = fn()
        status = "PASS" if ok else "FAIL"
        print(f"[{status}] controle {nome}")
        if not ok:
            falhou = True
            print(detail)
    if falhou:
        print("selftest_check_allowed_includes: FALHA -- ver controle(s) acima.")
        return 1
    print("selftest_check_allowed_includes: OK -- os cinco controles se comportaram como esperado.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
