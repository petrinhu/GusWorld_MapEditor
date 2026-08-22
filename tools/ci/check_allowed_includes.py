#!/usr/bin/env python3
# SPDX-License-Identifier: AGPL-3.0-or-later
"""
tools/ci/check_allowed_includes.py

Portao de CI: dependencia proibida (GODS_LAWS.md L-01), desenhado como
LISTA DO PERMITIDO, nunca lista do proibido -- ordem explicita da tarefa,
porque uma lista do proibido so pega quem ela ja conhece (RmlUi hoje, o
proximo framework amanha) e a lista do permitido pega qualquer coisa nova
por definicao, sem precisar de manutencao a cada biblioteca nova que
alguem tente colar.

Regra:
    - Include entre <angulos>: permitido SE o nome for da biblioteca padrao
      C++23 (STD_HEADERS abaixo), OU se o arquivo estiver na camada
      "platform" (GODS_LAWS.md L-12) E o include comecar com "glintfx/"
      -- a UNICA excecao de terceiro que existe neste projeto, por lei.
    - Include entre "aspas": permitido SE resolver para um arquivo REAL
      deste repositorio (relativo ao arquivo que inclui, a raiz do repo,
      a raiz `include/` ou a raiz `src/`) -- ou seja, e codigo NOSSO.
      Isto tambem fecha o furo obvio de "citar RmlUi/SDL entre aspas pra
      escapar da checagem de <angulo>": se o caminho nao existe de verdade
      no repo, nao e permitido, ponto.

Consequencia deliberada: cabecalho de sistema (<windows.h>, <unistd.h>, um
header solto do SDK do SO) tambem cai fora da lista do permitido, mesmo
fora da camada platform -- GODS_LAWS.md L-01 e explicito ("e proibido
falar direto com o sistema operacional"), e mesmo dentro de platform,
sistema operacional so entra via GlintFx, entao nem platform ganha
excecao para header de SO.

GODS_LAWS.md L-09: este portao tambem declara quantos arquivos varreu.

TRAVA decidida pelo lider em 22/08/2026 (mesma semantica do check_layers.py
irmao, gatilho em layer_common.any_layer_dir_exists): enquanto NENHUMA das
tres pastas de camada (domain/application/platform) existir em lugar
nenhum da arvore, varrer zero arquivos C++ sai 0 -- e ausencia de alvo, a
mensagem nunca afirma "OK"/"limpo"/"sucesso". No instante em que QUALQUER
uma das tres passar a existir, varrer zero volta a ser falha (exit 1),
porque a pasta ja existe e mesmo assim nao ha nada para varrer no repo
inteiro -- sintoma de arvore quebrada, nao de projeto novo.

Uso:
    python3 tools/ci/check_allowed_includes.py [RAIZ]

Exit 0 = nenhuma das tres pastas de camada existe ainda (nada a
         verificar), OU pelo menos um arquivo C++ foi varrido e nenhum
         include fora da lista.
Exit 1 = uma pasta de camada existe mas 0 arquivo C++ foi varrido no repo
         inteiro, OU include nao permitido encontrado.
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
)

# Biblioteca padrao C++23 (cppreference, "Standard library headers").
# Enumeravel e finita -- exatamente o motivo de dar pra usar allowlist em
# vez de blocklist aqui. Inclui os headers de compatibilidade C (cXXX) e
# suas contrapartes .h por pragmatismo (nao e regra de estilo deste portao
# escolher entre <cstdint> e <stdint.h> -- isso e clang-tidy, TESTES.md T2).
STD_HEADERS: frozenset[str] = frozenset({
    # C compat (nome C++ e nome C)
    "cassert", "assert.h", "cctype", "ctype.h", "cerrno", "errno.h",
    "cfenv", "fenv.h", "cfloat", "float.h", "cinttypes", "inttypes.h",
    "climits", "limits.h", "clocale", "locale.h", "cmath", "math.h",
    "csetjmp", "setjmp.h", "csignal", "signal.h", "cstdarg", "stdarg.h",
    "cstddef", "stddef.h", "cstdint", "stdint.h", "cstdio", "stdio.h",
    "cstdlib", "stdlib.h", "cstring", "string.h", "ctime", "time.h",
    "cuchar", "uchar.h", "cwchar", "wchar.h", "cwctype", "wctype.h",
    # Concepts / coroutines
    "concepts", "coroutine", "generator",
    # Utilities
    "any", "bit", "bitset", "chrono", "compare", "expected",
    "functional", "initializer_list", "optional", "source_location",
    "tuple", "type_traits", "typeindex", "typeinfo", "utility",
    "variant", "version",
    # Dynamic memory
    "memory", "memory_resource", "new", "scoped_allocator",
    # Numeric
    "complex", "numbers", "numeric", "random", "ratio", "valarray",
    "stdfloat",
    # Error handling
    "exception", "stdexcept", "system_error", "stacktrace",
    # Strings
    "charconv", "format", "string", "string_view",
    # Containers
    "array", "deque", "flat_map", "flat_set", "forward_list", "list",
    "map", "mdspan", "queue", "set", "span", "stack", "unordered_map",
    "unordered_set", "vector",
    # Iterators / ranges / algorithms
    "iterator", "ranges", "algorithm", "execution",
    # IO
    "fstream", "iomanip", "ios", "iosfwd", "iostream", "istream",
    "ostream", "print", "spanstream", "sstream", "streambuf",
    "syncstream",
    # Localization / regex
    "codecvt", "locale", "regex",
    # Concurrency
    "atomic", "barrier", "condition_variable", "future", "latch",
    "mutex", "semaphore", "shared_mutex", "stop_token", "thread",
    # Filesystem
    "filesystem",
})

GLINTFX_PREFIX = "glintfx/"


def _angle_header_name(inc_path: str) -> str:
    """Para comparar contra STD_HEADERS, usa so o ultimo componente quando
    o include padrao tem sub-caminho (nao existe no C++ padrao, mas mantido
    por robustez); e o proprio texto para o caso comum de nome unico."""
    return inc_path.strip()


def _resolve_quoted(inc_path: str, file: Path, root: Path) -> bool:
    candidates = [
        file.parent / inc_path,
        root / inc_path,
        root / "include" / inc_path,
        root / "src" / inc_path,
    ]
    return any(c.is_file() for c in candidates)


def run(root: Path) -> tuple[int, list[str]]:
    scanned = 0
    violations: list[str] = []

    for f in iter_cpp_files(root):
        scanned += 1
        is_platform = classify_layer(f, root) == "platform"

        for inc in extract_includes(f):
            if inc.is_angle:
                name = _angle_header_name(inc.path)
                if name in STD_HEADERS:
                    continue
                if is_platform and inc.path.replace("\\", "/").lower().startswith(GLINTFX_PREFIX):
                    continue
                reason = (
                    "nao e header padrao C++23 e nao e GlintFx em camada platform"
                    if is_platform else
                    "nao e header padrao C++23 (so platform pode incluir GlintFx)"
                )
                violations.append(
                    f'VIOLACAO {f}:{inc.line_no}: include <{inc.path}> fora da '
                    f"lista do permitido ({reason}) -- GODS_LAWS.md L-01."
                )
            else:
                if _resolve_quoted(inc.path, f, root):
                    continue
                violations.append(
                    f'VIOLACAO {f}:{inc.line_no}: include "{inc.path}" nao '
                    "resolve para nenhum arquivo real deste repositorio -- "
                    "so e permitido incluir entre aspas codigo NOSSO "
                    "(GODS_LAWS.md L-01)."
                )

    print(f"check_allowed_includes: {scanned} arquivo(s) C++ varrido(s).")
    return scanned, violations


def main(argv: list[str]) -> int:
    root = Path(argv[1]) if len(argv) > 1 else Path(".")
    if not root.exists():
        print(f"check_allowed_includes: ERRO: raiz '{root}' nao existe.", file=sys.stderr)
        return 1

    scanned, violations = run(root)

    if scanned == 0:
        if not any_layer_dir_exists(root):
            print(
                "check_allowed_includes: NADA A VERIFICAR -- 0 arquivos C++ "
                "varridos e NENHUMA das pastas domain/application/platform "
                f"existe ainda em lugar nenhum de '{root}'. Isto NAO e uma "
                "verificacao bem-sucedida: e ausencia de alvo (GODS_LAWS.md "
                "L-11, projeto do zero). Decisao do lider em 22/08/2026: "
                "este caminho sai 0 SO enquanto nenhuma das tres pastas "
                "existir; no instante em que uma aparecer, varrer zero "
                "arquivos volta a ser falha."
            )
            return 0
        dirs_found = find_layer_dirs(root)
        existentes = ", ".join(
            f"{nome} ({len(paths)} dir.)" for nome, paths in dirs_found.items() if paths
        )
        print(
            "check_allowed_includes: FALHA -- ha pasta de camada existindo "
            f"({existentes}) mas 0 arquivo C++ foi varrido no repositorio "
            f"inteiro sob '{root}'. Isto NAO e o caminho \"projeto ainda "
            "nao comecou\" (GODS_LAWS.md L-11): a pasta ja existe, entao "
            "isto e sintoma de filtro de extensao errado ou arvore "
            "quebrada. GODS_LAWS.md L-09 continua valendo: varrer zero, "
            "com pasta existindo, e falha, nao sucesso.",
            file=sys.stderr,
        )
        return 1

    if violations:
        print(f"check_allowed_includes: FALHA -- {len(violations)} violacao(oes):", file=sys.stderr)
        for v in violations:
            print(v, file=sys.stderr)
        return 1

    print("check_allowed_includes: OK -- todo include e permitido (GODS_LAWS.md L-01).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
