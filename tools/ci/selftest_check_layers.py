#!/usr/bin/env python3
# SPDX-License-Identifier: AGPL-3.0-or-later
"""
tools/ci/selftest_check_layers.py

Autoteste de check_layers.py com QUATRO controles (GODS_LAWS.md L-09 +
decisao do lider de 22/08/2026 sobre a TRAVA "verde declarando zero"):

    1. POSITIVO -- planta violacao de camada, prova que o portao acusa.
    2. NEGATIVO -- arvore limpa (so includes permitidos entre camadas),
       prova que o portao nao acusa fantasma.
    3. VAZIO    -- diretorio sem NENHUMA pasta domain/application/platform
       (so um arquivo decorativo fora de qualquer camada). Depois da
       trava, este e o caminho VERDE ("nada a verificar"): prova que o
       portao sai 0 e que a mensagem NAO afirma verificacao bem-sucedida
       (nunca a linha "check_layers: OK").
    4. TRAVA    -- prova as DUAS direcoes da trava, para as TRES pastas
       SEPARADAMENTE (o buraco classico desse tipo de guarda e a condicao
       so olhar a primeira da lista): (a) baseline sem pasta nenhuma ->
       exit 0, sem afirmar sucesso; (b) so a pasta <nome> existindo VAZIA
       -> exit 1; (c) so a pasta <nome> existindo com um arquivo que NAO
       casa a extensao C++ (.md) -> exit 1 -- este ultimo e o buraco
       explicito que o lider apontou (criar domain/ com um .md dentro nao
       pode deixar o portao mudo de novo).

Roda o script real via subprocess (nao importa a funcao e chama direto),
porque o que precisa ser provado e o comportamento observavel do PORTAO
DE CI -- codigo de saida e mensagem -- exatamente como o workflow do
GitHub Actions vai invoca-lo.

Uso:
    python3 tools/ci/selftest_check_layers.py

Exit 0 = os quatro controles se comportaram como esperado.
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
        # Nenhuma pasta domain/application/platform em lugar nenhum -- so
        # um arquivo decorativo fora de qualquer camada, para provar que
        # o portao nao conta "qualquer .cpp" como camada. Com a TRAVA
        # (decisao do lider, 22/08/2026), este e o caminho VERDE: nao ha
        # pasta de camada, entao 0 varrido e "nada a verificar", nao falha.
        _write(root, "solto.cpp", "#include <vector>\n")

        r = _run(root)
        ok = (
            r.returncode == 0
            and "NADA A VERIFICAR" in r.stdout
            and "check_layers: OK" not in r.stdout
        )
        detail = f"exit={r.returncode}\nstdout={r.stdout}\nstderr={r.stderr}"
        return ok, detail


def control_trava() -> tuple[bool, str]:
    """4o controle (exigencia do coordenador, 22/08/2026): prova as DUAS
    direcoes da trava, pastas domain/application/platform SEPARADAMENTE --
    nao so uma, porque o defeito classico de guarda como esta e a condicao
    checar so a primeira da lista e ficar cega para as outras duas."""
    detalhes: list[str] = []
    ok_geral = True

    # (a) baseline: nenhuma pasta de camada -- verde, sem afirmar sucesso.
    with tempfile.TemporaryDirectory(prefix="layers-trava-baseline-") as td:
        root = Path(td)
        r = _run(root)
        ok = (
            r.returncode == 0
            and "NADA A VERIFICAR" in r.stdout
            and "check_layers: OK" not in r.stdout
        )
        detalhes.append(f"baseline (sem pasta nenhuma): {'PASS' if ok else 'FAIL'} "
                         f"exit={r.returncode} stdout={r.stdout!r}")
        ok_geral = ok_geral and ok

    for nome in ("domain", "application", "platform"):
        # (b) so <nome>/ existindo, VAZIA.
        with tempfile.TemporaryDirectory(prefix=f"layers-trava-{nome}-vazia-") as td:
            root = Path(td)
            (root / nome).mkdir(parents=True)
            r = _run(root)
            ok = r.returncode == 1 and "pasta de camada existindo" in r.stderr
            detalhes.append(f"{nome}/ vazia: {'PASS' if ok else 'FAIL'} "
                             f"exit={r.returncode} stderr={r.stderr!r}")
            ok_geral = ok_geral and ok

        # (c) so <nome>/ existindo, com arquivo que NAO casa extensao C++
        #     -- o buraco explicito apontado pelo lider (.md dentro de
        #     domain/ nao pode deixar o portao mudo).
        with tempfile.TemporaryDirectory(prefix=f"layers-trava-{nome}-md-") as td:
            root = Path(td)
            _write(root, f"{nome}/leia.md", "nada de codigo aqui\n")
            r = _run(root)
            ok = r.returncode == 1 and "pasta de camada existindo" in r.stderr
            detalhes.append(f"{nome}/leia.md (nao casa extensao): {'PASS' if ok else 'FAIL'} "
                             f"exit={r.returncode} stderr={r.stderr!r}")
            ok_geral = ok_geral and ok

    return ok_geral, "\n".join(detalhes)


def main() -> int:
    controles = [
        ("positivo", control_positivo),
        ("negativo", control_negativo),
        ("vazio", control_vazio),
        ("trava", control_trava),
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
    print("selftest_check_layers: OK -- os quatro controles se comportaram como esperado.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
