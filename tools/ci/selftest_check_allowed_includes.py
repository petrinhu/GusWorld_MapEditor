#!/usr/bin/env python3
# SPDX-License-Identifier: AGPL-3.0-or-later
"""
tools/ci/selftest_check_allowed_includes.py

Autoteste de check_allowed_includes.py com TRES controles (GODS_LAWS.md
L-09, mesma exigencia do irmao selftest_check_layers.py):

    1. POSITIVO -- planta dependencia proibida de tres formas (lib de
       terceiro fora de platform, lib de terceiro DENTRO de platform --
       prova que a excecao e SO para GlintFx, e um include entre aspas
       que nao resolve para arquivo real -- prova que citar entre aspas
       nao e um jeito de escapar da checagem).
    2. NEGATIVO -- arvore limpa (stdlib em qualquer camada, GlintFx so em
       platform, aspas apontando para arquivo que existe de verdade),
       prova que o portao nao acusa fantasma.
    3. VAZIO    -- diretorio sem nenhum arquivo C++, prova que o portao
       FALHA em vez de passar em silencio.

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
        # Diretorio existe mas nao tem nenhum arquivo de extensao C++
        # (so um .md, para provar que o portao filtra por extensao e
        # ainda assim falha por "zero varrido").
        _write(root, "leia-me.md", "nada de codigo aqui\n")

        r = _run(root)
        ok = r.returncode == 1 and "0 arquivos C++" in r.stderr
        detail = f"exit={r.returncode}\nstdout={r.stdout}\nstderr={r.stderr}"
        return ok, detail


def main() -> int:
    controles = [
        ("positivo", control_positivo),
        ("negativo", control_negativo),
        ("vazio", control_vazio),
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
    print("selftest_check_allowed_includes: OK -- os tres controles se comportaram como esperado.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
