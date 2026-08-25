#!/usr/bin/env python3
# SPDX-License-Identifier: AGPL-3.0-or-later
"""
tools/ci/selftest_measure_hotspots.py

Autoteste da RESTRICAO que measure_hotspots.py nao pode violar (tarefa do
CTO/lider, GODS_LAWS.md L-19): o medidor NUNCA reprova, em nenhuma
circunstancia. Ao contrario dos autotestes de portao (selftest_check_*),
este NAO tem controle "positivo" que espera exit 1 -- nao existe exit 1
neste script, por desenho. Todo controle abaixo verifica exit 0 mais o
texto certo declarando escopo.

Controles:
    1. VAZIO    -- diretorio sem nenhum arquivo e sem git: exit 0,
                   declara "0 arquivo(s)" e "sem repositorio git".
    2. SEM_GIT  -- diretorio COM arquivo de codigo, mas sem `.git`: exit 0,
                   lista [1] preenchida, lista [2] declara ausencia de git
                   (nunca lista vazia muda).
    3. INEXIST  -- raiz que nao existe: exit 0, declara raiz inexistente.
    4. ARG_RUIM -- '--commits' com valor invalido: exit 0, usa default e
                   declara o erro em vez de travar.
    5. COM_GIT  -- repositorio git de verdade, com commits: exit 0, lista
                   [2] preenchida sem aviso de historico raso.

Roda o script real via subprocess, porque o que importa e o comportamento
OBSERVAVEL (codigo de saida + texto), igual ao workflow do GitHub Actions
vai invocar.

Uso:
    python3 tools/ci/selftest_measure_hotspots.py

Exit 0 = os cinco controles se comportaram como esperado.
Exit 1 = pelo menos um controle falhou (a restricao "nunca bloqueia" tem
         um furo real -- isto SIM e um defeito, mesmo o medidor nunca
         devendo bloquear o CI por conta propria).
"""
from __future__ import annotations

import subprocess
import sys
import tempfile
from pathlib import Path

SCRIPT = Path(__file__).resolve().parent / "measure_hotspots.py"


def _run(*args: str) -> subprocess.CompletedProcess:
    return subprocess.run(
        [sys.executable, str(SCRIPT), *args],
        capture_output=True, text=True,
    )


def control_vazio() -> tuple[bool, str]:
    with tempfile.TemporaryDirectory(prefix="hotspots-vazio-") as td:
        r = _run(td)
        ok = (
            r.returncode == 0
            and "0 arquivo(s) varrido(s)" in r.stdout
            and "sem repositorio git" in r.stdout
        )
        return ok, f"exit={r.returncode}\nstdout={r.stdout}\nstderr={r.stderr}"


def control_sem_git() -> tuple[bool, str]:
    with tempfile.TemporaryDirectory(prefix="hotspots-semgit-") as td:
        root = Path(td)
        (root / "algo.cpp").write_text("int main() { return 0; }\n", encoding="utf-8")
        r = _run(td)
        ok = (
            r.returncode == 0
            and "1 arquivo(s) varrido(s)" in r.stdout
            and "sem repositorio git" in r.stdout
        )
        return ok, f"exit={r.returncode}\nstdout={r.stdout}\nstderr={r.stderr}"


def control_inexistente() -> tuple[bool, str]:
    with tempfile.TemporaryDirectory(prefix="hotspots-base-") as td:
        alvo = Path(td) / "nao-existe-mesmo"
        r = _run(str(alvo))
        ok = r.returncode == 0 and "NAO EXISTE" in r.stderr
        return ok, f"exit={r.returncode}\nstdout={r.stdout}\nstderr={r.stderr}"


def control_arg_ruim() -> tuple[bool, str]:
    with tempfile.TemporaryDirectory(prefix="hotspots-argruim-") as td:
        r = _run(td, "--commits", "nao-e-numero")
        ok = r.returncode == 0 and "ERRO ao interpretar argumentos" in r.stderr
        return ok, f"exit={r.returncode}\nstdout={r.stdout}\nstderr={r.stderr}"


def control_com_git() -> tuple[bool, str]:
    with tempfile.TemporaryDirectory(prefix="hotspots-comgit-") as td:
        root = Path(td)
        env_git = ["git", "-C", str(root)]

        def g(*args: str) -> None:
            subprocess.run([*env_git, *args], capture_output=True, text=True, check=True)

        g("init", "-q")
        g("config", "user.email", "teste@example.com")
        g("config", "user.name", "Teste")

        (root / "a.cpp").write_text("int main() { return 0; }\n", encoding="utf-8")
        g("add", "a.cpp")
        g("commit", "-q", "-m", "primeiro")

        (root / "a.cpp").write_text("int main() { return 1; }\n", encoding="utf-8")
        g("commit", "-q", "-a", "-m", "segundo")

        r = _run(str(root), "--commits", "5")
        ok = (
            r.returncode == 0
            and "1 arquivo(s) varrido(s)" in r.stdout
            and "2x  a.cpp" in r.stdout
            and "checkout RASO" not in r.stdout
        )
        return ok, f"exit={r.returncode}\nstdout={r.stdout}\nstderr={r.stderr}"


def main() -> int:
    controles = [
        ("vazio", control_vazio),
        ("sem_git", control_sem_git),
        ("inexistente", control_inexistente),
        ("arg_ruim", control_arg_ruim),
        ("com_git", control_com_git),
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
        print("selftest_measure_hotspots: FALHA -- ver controle(s) acima. "
              "Isto e defeito real: a restricao de nunca bloquear tem furo.")
        return 1
    print("selftest_measure_hotspots: OK -- os cinco controles confirmam "
          "que o medidor sempre sai 0 e sempre declara o proprio escopo.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
