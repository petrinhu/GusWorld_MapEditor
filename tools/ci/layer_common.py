# SPDX-License-Identifier: AGPL-3.0-or-later
"""
tools/ci/layer_common.py

Utilidades compartilhadas pelos dois portoes de CI de arquitetura/dependencia
(check_layers.py e check_allowed_includes.py). GODS_LAWS.md L-12 (camadas
horizontais finas: domain / application / platform) e L-01 (so a API publica
do GlintFx, lista do permitido).

Nada aqui depende de biblioteca externa: so a stdlib do Python 3, para rodar
sem instalar nada nos cinco alvos de CI (L-10) que tem python3 disponivel
(a matriz de build C++ e outra frente; estes portoes rodam num job unico
ubuntu-latest, GlintFx/.github/workflows/ci.yml faz o mesmo com o job "leis").

Limitacao declarada (regra "no silent caps", GODS_LAWS.md L-09 exige
honestidade sobre o que o portao NAO cobre): a extracao de #include e
textual, nao usa um parser C++ de verdade. Comentario de bloco (/* ... */)
e removido do arquivo inteiro antes de procurar por diretivas; comentario de
linha (//) e removido linha a linha. Diretiva de include partida em duas
linhas por barra invertida no fim da linha NAO e reconhecida -- nenhum
arquivo real deste projeto faz isso hoje (nada a varrer ainda, GODS_LAWS.md
L-11), e se algum dia aparecer, os proprios portoes vao falhar ruidosamente
por "0 arquivos" se a extracao quebrar tudo, nunca em silencio.
"""
from __future__ import annotations

import re
from pathlib import Path
from typing import Iterator, NamedTuple, Optional

# Extensoes de codigo C++ que os dois portoes varrem. Cabecalho e fonte,
# nao importa a camada.
CPP_EXTENSIONS = {
    ".h", ".hh", ".hpp", ".hxx", ".ixx", ".inl", ".tpp",
    ".c", ".cc", ".cpp", ".cxx",
}

# Nomes de diretorio que NUNCA sao codigo nosso: artefato de build, VCS,
# cache, dependencia vendorizada/baixada. Varrer build/ ou _deps/ produziria
# falso positivo constante (o proprio GlintFx baixado por FetchContent
# inclui RmlUi/SDL/etc. no codigo DELE, que nao e nosso para fiscalizar).
EXCLUDE_DIR_NAMES = {
    ".git", ".github", ".claude", "__pycache__", "node_modules",
    ".venv", "venv", "_deps", "third_party", "external", "vendor",
    ".cache",
}
# Prefixos de diretorio de build (build, build-shared, cmake-build-debug, ...)
EXCLUDE_DIR_PREFIXES = ("build", "cmake-build", "out")

# As tres camadas de L-12, nesta ordem porque e a ordem de dependencia
# permitida (dominio no centro, plataforma na casca externa).
LAYER_NAMES = ("domain", "application", "platform")


class Include(NamedTuple):
    line_no: int
    is_angle: bool  # True = <...> ; False = "..."
    path: str       # conteudo entre os delimitadores, ex. "glintfx/core/version.hpp"


_INCLUDE_RE = re.compile(r'^\s*#\s*include\s*([<"])([^">]+)([>"])\s*(//.*)?$')
_BLOCK_COMMENT_RE = re.compile(r"/\*.*?\*/", re.DOTALL)
_LINE_COMMENT_RE = re.compile(r"//.*$")


def _prune_dirs(dirnames: list[str]) -> None:
    dirnames[:] = [
        d for d in dirnames
        if d not in EXCLUDE_DIR_NAMES and not d.lower().startswith(EXCLUDE_DIR_PREFIXES)
    ]


def iter_cpp_files(root: Path) -> Iterator[Path]:
    """Percorre `root` e devolve todo arquivo de codigo C++ (extensoes em
    CPP_EXTENSIONS), pulando diretorios de build/VCS/dependencia vendorizada.
    Ordenado, para saida deterministica entre rodadas."""
    root = Path(root)
    if root.is_file():
        if root.suffix.lower() in CPP_EXTENSIONS:
            yield root
        return
    for dirpath, dirnames, filenames in _walk_sorted(root):
        _prune_dirs(dirnames)
        for name in filenames:
            p = Path(dirpath) / name
            if p.suffix.lower() in CPP_EXTENSIONS:
                yield p


def _walk_sorted(root: Path):
    import os
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames.sort()
        filenames.sort()
        yield dirpath, dirnames, filenames


def find_layer_dirs(root: Path) -> dict[str, list[Path]]:
    """Percorre `root` e devolve, para cada uma das tres camadas, a lista de
    diretorios cujo NOME (sem diferenciar maiuscula) bate com o nome da
    camada -- independente de o diretorio ter arquivo de codigo dentro,
    estar vazio ou so ter arquivo que nao casa com CPP_EXTENSIONS.

    Existe para a TRAVA decidida pelo lider em 22/08/2026 (ver
    check_layers.py e check_allowed_includes.py): a existencia do
    DIRETORIO, nao a contagem de arquivo, e o gatilho. Se a checagem
    fosse "total de arquivo C++ == 0", criar `domain/` so com um `.md`
    dentro nao mudaria o total e o portao continuaria mudo -- exatamente
    o buraco que a lei pede para fechar.

    Usa a MESMA poda de diretorio de build/VCS/dependencia vendorizada
    que iter_cpp_files, para uma pasta "domain" dentro de uma dependencia
    baixada (_deps, vendor, node_modules, ...) nao contar como se fosse
    camada nossa."""
    root = Path(root)
    found: dict[str, list[Path]] = {name: [] for name in LAYER_NAMES}
    if root.is_file():
        return found
    for dirpath, dirnames, _filenames in _walk_sorted(root):
        for d in dirnames:
            low = d.lower()
            if low in LAYER_NAMES:
                found[low].append(Path(dirpath) / d)
        _prune_dirs(dirnames)
    return found


def any_layer_dir_exists(root: Path) -> bool:
    """Atalho: True se QUALQUER uma das tres pastas de camada existe em
    algum lugar da arvore (vazia ou nao)."""
    return any(paths for paths in find_layer_dirs(root).values())


def classify_layer(path: Path, root: Path) -> Optional[str]:
    """Devolve 'domain', 'application' ou 'platform' se algum componente do
    caminho (relativo a `root`), comparado sem diferenciar maiusculas, bater
    com um desses nomes -- o primeiro encontrado a partir da raiz (a camada
    mais externa que contem o arquivo). Devolve None se o arquivo nao esta
    sob nenhuma das tres."""
    try:
        rel = path.resolve().relative_to(Path(root).resolve())
    except ValueError:
        rel = path
    parts_lower = [p.lower() for p in rel.parts[:-1]]  # exclui o nome do arquivo
    for part in parts_lower:
        if part in LAYER_NAMES:
            return part
    return None


def strip_comments(text: str) -> str:
    """Remove comentario de bloco (arquivo inteiro) e devolve o texto pronto
    para ser varrido linha a linha (o chamador ainda remove // por linha)."""
    return _BLOCK_COMMENT_RE.sub("", text)


def extract_includes(path: Path) -> list[Include]:
    """Le `path` e devolve toda diretiva #include encontrada. Limitacao
    conhecida (ver docstring do modulo): a contagem de linha usada aqui e a
    do texto JA COM o comentario de bloco removido, entao um bloco `/* */`
    multi-linha antes de um #include desloca o numero de linha reportado.
    O portao ainda acusa o arquivo certo; so a linha pode escorregar
    quando isso acontece -- aceitavel porque nenhum arquivo real do
    projeto existe ainda (GODS_LAWS.md L-11) e o caso e raro na pratica."""
    try:
        raw = path.read_text(encoding="utf-8", errors="replace")
    except OSError:
        return []
    out: list[Include] = []
    for i, line in enumerate(strip_comments(raw).splitlines(), start=1):
        line = _LINE_COMMENT_RE.sub("", line)
        m = _INCLUDE_RE.match(line)
        if not m:
            continue
        open_delim, inc_path, close_delim = m.group(1), m.group(2), m.group(3)
        if (open_delim, close_delim) not in (("<", ">"), ('"', '"')):
            continue
        out.append(Include(line_no=i, is_angle=(open_delim == "<"), path=inc_path))
    return out


def path_segments(include_path: str) -> list[str]:
    """Normaliza separador (\\ ou /) e devolve os componentes do caminho de
    include em minusculas, para comparacao de segmento (ex.: 'application/
    foo.hpp' -> ['application', 'foo.hpp'])."""
    return [seg.lower() for seg in re.split(r"[\\/]", include_path) if seg]
