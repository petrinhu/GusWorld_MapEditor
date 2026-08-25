#!/usr/bin/env python3
# SPDX-License-Identifier: AGPL-3.0-or-later
"""
tools/ci/measure_hotspots.py

MEDIDOR informativo de L-19 (GODS_LAWS.md), decidido pelo lider depois do
CTO propor numero e ele aprovar so a MEDICAO, nunca o julgamento. Razao
dele, verbatim relatada na tarefa: "lei qualitativa falha exatamente
quando ninguem olha", e a quinta pergunta do revisor (git log --stat) fica
mais barata com o dado ja impresso.

RESTRICAO QUE NAO PODE SER VIOLADA, e por isso esta em maiuscula aqui
tambem: este script NUNCA reprova nada.

    - Sempre sai com codigo 0. Sem excecao -- inclusive erro interno,
      inclusive raiz inexistente, inclusive git ausente.
    - Zero limite, zero numero magico, zero comparacao com teto. Ele nao
      diz "grande demais". So imprime.
    - Ele NAO e um portao, entao a regra da L-09 de falhar em zero
      arquivos varridos NAO se aplica a ele -- mas o ESPIRITO dela sim:
      declarar o proprio escopo. Se varreu zero, ele diz "0 arquivos" com
      todas as letras, nunca lista vazia em silencio.

Duas listas, cada uma calculada e impressa de forma INDEPENDENTE (uma
falhar nao apaga a outra -- um relatorio parcial declarado vale mais que
nenhum relatorio, e um relatorio que finge sucesso quando so meio saiu):

    [1] Arquivos de codigo do projeto por TAMANHO, decrescente. Usa o
        mesmo iter_cpp_files() dos portoes de camada (layer_common.py):
        so codigo nosso, nunca build/_deps/vendor/dependencia.

    [2] Arquivos por FREQUENCIA DE APARICAO nos ultimos N commits
        (--commits, configuravel, default DEFAULT_COMMITS abaixo -- nunca
        magico, sempre visivel e sempre alteravel na linha de comando ou
        no workflow). E a lista que sustenta a 5a pergunta da L-19 ("quem
        paga a proxima feature?").

        Cuidado real, documentado porque ja mordeu outro portao da casa:
        um checkout RASO (fetch-depth padrao do GitHub Actions e 1) nao
        tem o que contar. Este script DETECTA a rasura
        (git rev-parse --is-shallow-repository) e a ausencia de git
        (git rev-parse --is-inside-work-tree) e DECLARA a causa em vez de
        imprimir lista vazia de um jeito que parece "ninguem tocou em
        nada" -- exatamente o defeito que a L-09 registra no portao de
        camadas, vestido de outra roupa.

Uso:
    python3 tools/ci/measure_hotspots.py [RAIZ] [--commits N]

RAIZ default: "." . --commits default: DEFAULT_COMMITS.
Exit: SEMPRE 0.
"""
from __future__ import annotations

import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from layer_common import (  # noqa: E402
    CPP_EXTENSIONS,
    EXCLUDE_DIR_NAMES,
    EXCLUDE_DIR_PREFIXES,
    iter_cpp_files,
)

# Configuravel, nunca magico (exigencia explicita da tarefa). Mude aqui ou
# passe --commits N na linha de comando / no workflow.
DEFAULT_COMMITS = 20


def _parse_args(argv: list[str]) -> tuple[Path, int]:
    root = Path(".")
    commits = DEFAULT_COMMITS
    args = argv[1:]
    i = 0
    while i < len(args):
        a = args[i]
        if a == "--commits":
            i += 1
            commits = int(args[i])
        elif a.startswith("--commits="):
            commits = int(a.split("=", 1)[1])
        else:
            root = Path(a)
        i += 1
    if commits <= 0:
        raise ValueError(f"--commits precisa ser > 0, recebido {commits}")
    return root, commits


def _rel_dir_excluded(path_parts_lower: list[str]) -> bool:
    """Mesma poda de build/VCS/dependencia vendorizada que layer_common usa
    em iter_cpp_files, aplicada aqui a caminho textual (nao percorrido por
    os.walk) vindo do `git log --name-only`."""
    for part in path_parts_lower:
        if part in EXCLUDE_DIR_NAMES or part.startswith(EXCLUDE_DIR_PREFIXES):
            return True
    return False


def medir_tamanho(root: Path) -> list[tuple[Path, int]]:
    """Lista (arquivo, linhas) de todo arquivo de codigo do projeto sob
    `root`, maior primeiro. Reusa iter_cpp_files: mesma definicao de
    'codigo nosso' que os portoes de camada usam (exclui build/_deps/
    vendor/etc.)."""
    resultado: list[tuple[Path, int]] = []
    for f in iter_cpp_files(root):
        try:
            n = sum(1 for _ in f.open("r", encoding="utf-8", errors="replace"))
        except OSError:
            continue
        resultado.append((f, n))
    resultado.sort(key=lambda par: par[1], reverse=True)
    return resultado


def _git(root: Path, *args: str) -> subprocess.CompletedProcess:
    return subprocess.run(
        ["git", "-C", str(root), *args],
        capture_output=True, text=True, check=False,
    )


def _is_git_repo(root: Path) -> bool:
    r = _git(root, "rev-parse", "--is-inside-work-tree")
    return r.returncode == 0 and r.stdout.strip() == "true"


def _is_shallow(root: Path) -> bool:
    r = _git(root, "rev-parse", "--is-shallow-repository")
    return r.returncode == 0 and r.stdout.strip() == "true"


def _commit_count(root: Path) -> int:
    r = _git(root, "rev-list", "--count", "HEAD")
    if r.returncode != 0:
        return 0
    try:
        return int(r.stdout.strip())
    except ValueError:
        return 0


def medir_frequencia(root: Path, commits: int) -> tuple[list[tuple[str, int]], str]:
    """Devolve (lista_ordenada_desc, aviso). `aviso` e "" quando nao ha
    nada de especial a declarar; caso contrario explica por que a lista
    pode estar vazia ou incompleta -- NUNCA deixa lista vazia falar
    sozinha."""
    if not _is_git_repo(root):
        return [], ("sem repositorio git nesta raiz -- lista de frequencia "
                     "NAO calculada (nao e 'ninguem tocou em nada', e "
                     "'nao ha historico para consultar').")

    disponiveis = _commit_count(root)
    if disponiveis == 0:
        return [], ("repositorio git sem nenhum commit alcancavel em HEAD -- "
                     "lista de frequencia vazia porque nao ha o que contar.")

    usados = min(commits, disponiveis)
    aviso = ""
    if _is_shallow(root):
        aviso = (
            f"AVISO: checkout RASO (shallow). Pedido {commits} commit(s); "
            f"HEAD so enxerga {disponiveis} localmente. A lista abaixo cobre "
            f"apenas o que o checkout raso permite ver, NAO os ultimos "
            f"{commits} commits reais do projeto -- isto e historico "
            "indisponivel, nao ausencia de mudanca (GODS_LAWS.md L-09, "
            "mesmo espirito aplicado aqui)."
        )
    elif disponiveis < commits:
        aviso = (
            f"AVISO: repositorio tem so {disponiveis} commit(s) alcancavel(is) "
            f"no total, menos que os {commits} pedidos. Lista cobre todos os "
            f"{disponiveis} disponiveis."
        )

    r = _git(root, "log", f"-n{usados}", "--name-only", "--pretty=format:")
    if r.returncode != 0:
        return [], f"AVISO: 'git log' falhou (exit {r.returncode}): {r.stderr.strip()}"

    contagem: dict[str, int] = {}
    for linha in r.stdout.splitlines():
        linha = linha.strip()
        if not linha:
            continue
        partes = [p.lower() for p in linha.replace("\\", "/").split("/") if p]
        if _rel_dir_excluded(partes[:-1]):
            continue
        sufixo = Path(linha).suffix.lower()
        if sufixo not in CPP_EXTENSIONS:
            continue
        contagem[linha] = contagem.get(linha, 0) + 1

    ordenado = sorted(contagem.items(), key=lambda par: (-par[1], par[0]))
    return ordenado, aviso


def _imprimir_lista_tamanho(root: Path) -> None:
    por_tamanho = medir_tamanho(root)
    print(f"\n[1] Arquivos de codigo por TAMANHO, decrescente -- "
          f"{len(por_tamanho)} arquivo(s) varrido(s).")
    if not por_tamanho:
        print("    0 arquivos: nenhum arquivo de codigo C++ do projeto "
              "encontrado sob esta raiz.")
        return
    for f, n in por_tamanho:
        try:
            rel = f.resolve().relative_to(root.resolve())
        except ValueError:
            rel = f
        print(f"    {n:6d} linhas  {rel}")


def _imprimir_lista_frequencia(root: Path, commits: int) -> None:
    print(f"\n[2] Arquivos por FREQUENCIA nos ultimos {commits} commit(s) "
          "pedidos (--commits, configuravel -- sustenta a 5a pergunta da "
          "L-19: 'quem paga a proxima feature?').")
    freq, aviso = medir_frequencia(root, commits)
    if aviso:
        print(f"    {aviso}")
    print(f"    {len(freq)} arquivo(s) distinto(s) tocado(s).")
    if not freq and not aviso:
        print("    0 arquivos: nenhum arquivo de codigo tocado nos commits "
              "varridos.")
        return
    for caminho, n in freq:
        print(f"    {n:4d}x  {caminho}")


def main(argv: list[str]) -> int:
    print("=" * 72)
    print("measure_hotspots -- MEDIDOR INFORMATIVO (GODS_LAWS.md L-19).")
    print("NAO E PORTAO: nunca reprova CI, nunca compara com teto, so imprime.")
    print("=" * 72)

    try:
        root, commits = _parse_args(argv)
    except Exception as exc:  # noqa: BLE001 -- medidor nunca bloqueia
        print(f"measure_hotspots: ERRO ao interpretar argumentos "
              f"({type(exc).__name__}: {exc}) -- usando default RAIZ='.' "
              f"e commits={DEFAULT_COMMITS}.", file=sys.stderr)
        root, commits = Path("."), DEFAULT_COMMITS

    if not root.exists():
        print(f"\nmeasure_hotspots: raiz '{root}' NAO EXISTE -- 0 arquivo "
              "varrido, 0 commit varrido. Declarado, nao escondido.",
              file=sys.stderr)
        print("\nmeasure_hotspots: fim (nada a medir). Exit sempre 0.")
        return 0

    try:
        _imprimir_lista_tamanho(root)
    except Exception as exc:  # noqa: BLE001 -- medidor nunca bloqueia
        print(f"\n[1] ERRO INTERNO ao medir tamanho ({type(exc).__name__}: "
              f"{exc}) -- declarado, lista [1] indisponivel nesta rodada.",
              file=sys.stderr)

    try:
        _imprimir_lista_frequencia(root, commits)
    except Exception as exc:  # noqa: BLE001 -- medidor nunca bloqueia
        print(f"\n[2] ERRO INTERNO ao medir frequencia ({type(exc).__name__}: "
              f"{exc}) -- declarado, lista [2] indisponivel nesta rodada.",
              file=sys.stderr)

    print("\nmeasure_hotspots: fim. Relatorio informativo -- exit sempre 0, "
          "sem excecao.")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main(sys.argv))
    except Exception as exc:  # noqa: BLE001 -- ultima rede, mesma restricao
        print(f"measure_hotspots: ERRO INTERNO FATAL ({type(exc).__name__}: "
              f"{exc}) -- mesmo assim, exit 0 (restricao explicita: este "
              "medidor NUNCA bloqueia).", file=sys.stderr)
        raise SystemExit(0)
