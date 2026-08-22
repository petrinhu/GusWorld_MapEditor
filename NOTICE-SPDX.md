# Política de cabeçalho SPDX

Este projeto usa o identificador **REUSE/SPDX** para declarar a licença em cada
arquivo de código, no mesmo padrão adotado pelo GlintFx (o framework do qual
este editor é consumidor exclusivo).

## Licença do projeto

```
AGPL-3.0-or-later
```

## Formato exato da linha

```
SPDX-License-Identifier: AGPL-3.0-or-later
```

Prefixada pelo marcador de comentário da linguagem do arquivo:

| Linguagem / tipo de arquivo | Linha completa |
|---|---|
| C++ (`.cpp`, `.hpp`, `.h`) | `// SPDX-License-Identifier: AGPL-3.0-or-later` |
| CMake (`.cmake`, `CMakeLists.txt`, `.cmake.in`) | `# SPDX-License-Identifier: AGPL-3.0-or-later` |
| Shell (`.sh`) | `# SPDX-License-Identifier: AGPL-3.0-or-later` |
| PowerShell (`.ps1`) | `# SPDX-License-Identifier: AGPL-3.0-or-later` |
| YAML (`.yml`, `.yaml`, workflows de CI) | `# SPDX-License-Identifier: AGPL-3.0-or-later` |

## Onde a linha fica no arquivo

- **Primeira linha do arquivo**, sem exceção, para todos os tipos acima.
- **Única exceção:** arquivo com shebang (`.sh`, script executável). Nesse
  caso o shebang (`#!/usr/bin/env sh`) ocupa a linha 1 e o SPDX vai na
  **linha 2**.
- Nunca depois de `#pragma once`, de um `#include` ou de qualquer outro
  código. O identificador é a primeira coisa que o arquivo declara.

## Exemplos

Cabeçalho de um `.hpp`:

```cpp
// SPDX-License-Identifier: AGPL-3.0-or-later
#pragma once

#include <cstdint>
```

Cabeçalho de um `.cpp`:

```cpp
// SPDX-License-Identifier: AGPL-3.0-or-later
#include <gusworld_mapeditor/algo.hpp>
```

Cabeçalho de um `CMakeLists.txt` ou `.cmake`:

```cmake
# SPDX-License-Identifier: AGPL-3.0-or-later
#
# CMakeLists.txt - raiz do gusworld_mapeditor.
```

Cabeçalho de um script shell:

```sh
#!/usr/bin/env sh
# SPDX-License-Identifier: AGPL-3.0-or-later
# nome-do-script.sh - o que ele faz.
```

Cabeçalho de um workflow de CI:

```yaml
# SPDX-License-Identifier: AGPL-3.0-or-later
name: CI
```

## Quando isto se aplica

Assim que existir o primeiro arquivo de código do projeto (hoje o repositório
ainda não tem nenhum, ver `README.md`). O portão de CI que vai fiscalizar
esta regra segue a mesma exigência do GlintFx (L-09 de `GODS_LAWS.md`):
**declara quantos arquivos varreu**, porque um portão que varre zero e
imprime verde é uma falha silenciosa, não um sucesso.

## Fonte

Convenção conferida ao vivo no código do GlintFx (`GlintFx/src`,
`GlintFx/include`, `GlintFx/cmake`, `GlintFx/tests/tools`,
`GlintFx/.github/workflows/ci.yml`), não inventada de cabeça. Ver `L-07` de
`GODS_LAWS.md`.
