#!/usr/bin/env python3
# SPDX-License-Identifier: AGPL-3.0-or-later
"""
tools/ci/selftest_check_layers.py

Autoteste de check_layers.py com TRES controles (GODS_LAWS.md L-09, ordem
explicita da tarefa que criou este arquivo -- dois controles nao bastam):

    1. POSITIVO -- planta violacao de camada, prova que o portao acusa.
    2. NEGATIVO -- arvore limpa (so includes permitidos entre camadas),
       prova que o portao nao acusa fantasma.
    3. VAZIO    -- diretorio sem nenhum arquivo domain/application/platform,
       prova que o portao FALHA (nao passa em silencio) quando nao ha nada
       para varrer. E o controle que os outros dois nunca exercitam, e o
       motivo exato pelo qual GODS_LAWS.md L-09 existe.

Roda o script real via subprocess (nao importa a funcao e chama direto),
porque o que precisa ser provado e o comportamento observavel do PORTAO
DE CI -- codigo de saida e mensagem -- exatamente como o workflow do
GitHub Actions vai invoca-lo.

Uso:
    python3 tools/ci/selftest_check_layers.py

Exit 0 = os tres controles se comportaram como esperado.
Exit 1 = pelo menos um controle falhou (o portao real tem um defeito).
"""
from __future__ import annotations

import subprocess
import sys
import tempfile
from pathlib import Path

SCRIPT = Path(__file__).resolve().parent / "check_layers.py"


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
    with tempfile.TemporaryDirectory(prefix="layers-positivo-") as td:
        root = Path(td)
        # domain violando: inclui header de application.
        _write(root, "domain/mapa.hpp", '#include "application/abrir_mapa.hpp"\n')
        # application violando: inclui GlintFx direto.
        _write(root, "application/abrir_mapa.hpp",
               "#include <glintfx/core/version.hpp>\n")
        # platform limpo, so para nao ficar com total zero por acidente.
        _write(root, "platform/janela.cpp", "#include <glintfx/core/version.hpp>\n")

        r = _run(root)
        ok = r.returncode == 1 and "domain inclui" in r.stderr and "application inclui" in r.stderr
        detail = f"exit={r.returncode}\nstdout={r.stdout}\nstderr={r.stderr}"
        return ok, detail


def control_negativo() -> tuple[bool, str]:
    with tempfile.TemporaryDirectory(prefix="layers-negativo-") as td:
        root = Path(td)
        _write(root, "domain/mapa.hpp", "#include <vector>\n#include <memory>\n")
        _write(root, "application/abrir_mapa.hpp", '#include "domain/mapa.hpp"\n')
        _write(root, "platform/janela.cpp", "#include <glintfx/core/version.hpp>\n")

        r = _run(root)
        ok = r.returncode == 0 and "OK" in r.stdout
        detail = f"exit={r.returncode}\nstdout={r.stdout}\nstderr={r.stderr}"
        return ok, detail


def control_vazio() -> tuple[bool, str]:
    with tempfile.TemporaryDirectory(prefix="layers-vazio-") as td:
        root = Path(td)
        # Nenhum arquivo domain/application/platform -- so um arquivo
        # decorativo fora de qualquer camada, para provar que o portao
        # nao conta "qualquer .cpp" como camada, e ainda assim falha.
        _write(root, "solto.cpp", "#include <vector>\n")

        r = _run(root)
        ok = r.returncode == 1 and "0 arquivos de camada" in r.stderr
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
        print("selftest_check_layers: FALHA -- ver controle(s) acima.")
        return 1
    print("selftest_check_layers: OK -- os tres controles se comportaram como esperado.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
