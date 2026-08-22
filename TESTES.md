# Guia Completo de Testes, Qualidade e Auditoria (gusworld_mapeditor)

> Documento instrucional para qualquer agente de IA executar a suíte completa de verificação
> deste projeto. Stack único: **C++23, sem Qt, sem SQL, sem rede**, única dependência externa
> e o framework **GlintFx** (`../GlintFx`), incluído apenas na casca de plataforma (L-12).
> **Precedência:** [`GODS_LAWS.md`](GODS_LAWS.md) vence este guia em qualquer conflito.
> Cinco alvos de CI (L-10): **Fedora 44 (primário, pinado)**, Ubuntu, Arch, CachyOS, Windows.

---

## Índice

0. [Regra-Mãe de Todo Portão (L-09)](#0--regra-mãe-de-todo-portão-l-09)
1. [T1  -  Testes Unitários](#t1--testes-unitários)
2. [T2  -  Análise Estática](#t2--análise-estática)
3. [T3  -  Fuzzing / Teste Baseado em Propriedade](#t3--fuzzing--teste-baseado-em-propriedade)
4. [T4  -  Análise Dinâmica de Memória](#t4--análise-dinâmica-de-memória)
5. [T8  -  Verificação de Secrets](#t8--verificação-de-secrets)
6. [T12  -  Busca de CVEs na Dependência](#t12--busca-de-cves-na-dependência)
7. [T14  -  Round-trip de Arquivo (Byte a Byte)](#t14--round-trip-de-arquivo-byte-a-byte)
8. [T15  -  Pré-CI, Espelhar CI Localmente](#t15--pre-ci-espelhar-ci-localmente)
9. [T16  -  Testabilidade sem Janela (Headless)](#t16--testabilidade-sem-janela-headless)
10. [T17  -  Repartição Convexa de Polígono](#t17--repartição-convexa-de-polígono)
11. [A2  -  Auditoria de Arquitetura e Camadas](#a2--auditoria-de-arquitetura-e-camadas)
12. [A3  -  UI/UX (via GlintFx)](#a3--uiux-via-glintfx)
13. [A10  -  Relatório Final de Auditoria](#a10--relatório-final-de-auditoria)
14. [Classificação de Problemas](#classificação-de-problemas)
15. [Formato de Patch](#formato-de-patch)

---

## 0.  Regra-Mãe de Todo Portão (L-09)

O rigor de teste, portão de CI e auditoria deste projeto é o mesmo do GlintFx, adaptado ao nosso domínio, nunca relaxado por sermos menores (L-09, verbatim do líder).

**O defeito já herdado que toda ferramenta nova precisa evitar:** um portão que varre zero arquivos e imprime verde passa nos dois autotestes de praxe (o positivo, que planta uma violação, e o negativo, que prova que entrada limpa sai zero), porque ambos rodam sobre arquivos que existem. "Olhei e está limpo" e "não olhei nada" produzem a mesma saída.

**Regra concreta, válida para TODO script de portão deste projeto** (verificador de camadas, scanner de secrets, análise estática, o que for):

1. O script MUST imprimir explicitamente `Arquivos varridos: N` antes de declarar o resultado.
2. Se `N == 0`, o script MUST sair com código de falha (não-zero), mesmo que nenhuma violação tenha sido encontrada. Zero arquivos varridos é falha, não sucesso.
3. O autoteste do portão (positivo e negativo) MUST incluir um terceiro caso: apontar o portão para um diretório vazio ou inexistente e confirmar que ele falha por `N == 0`, não que ele "passe verde".

```bash
#!/usr/bin/env bash
# Exemplo minimo do padrao exigido por qualquer portão deste projeto.
set -euo pipefail
ALVO="${1:-src}"
ARQUIVOS=$(find "$ALVO" -name '*.cpp' -o -name '*.h' 2>/dev/null)
N=$(printf '%s\n' "$ARQUIVOS" | grep -c . || true)
echo "Arquivos varridos: $N"
if [ "$N" -eq 0 ]; then
    echo "FALHA: portão varreu zero arquivos (ver GODS_LAWS L-09)" >&2
    exit 1
fi
# ... lógica de verificação real aqui ...
```

---

## T1  -  Testes Unitários

**Objetivo:** verificar que cada módulo do domínio e da aplicação se comporta conforme especificado, de forma isolada e sem janela (ver T16).

**Ferramenta recomendada:** Catch2 (mesma ferramenta usada no GlintFx, evita duas suítes de teste diferentes convivendo no ecossistema). **Esta é uma recomendação de tooling, não uma lei confirmada pelo líder** -- ver pendência no relatório de poda.

**Critério de aprovação:** 0 falhas. Cobertura mínima de 80% no domínio e na aplicação (camadas 100% testáveis sem janela, ver T16), sem piso definido para a casca de plataforma enquanto o GlintFx não tiver janela.

---

## T2  -  Análise Estática

**Objetivo:** detectar bugs, ma praticas e problemas de segurança sem executar o código.

**Ferramentas:** `cppcheck` + `clang-tidy`.

**Critério de aprovação:** 0 erros. `clang-tidy` MUST rodar também uma checagem customizada (ou `ast-grep`/`grep` disciplinado, ver A2) que recusa qualquer `#include` de GlintFx fora da casca de plataforma.

---

## T3  -  Fuzzing / Teste Baseado em Propriedade

Este projeto **não** escreve o parser do formato de mapa (isso é do GlintFx, L-03), então fuzzing de parser de mapa não é responsabilidade nossa. O que **é** nosso e testado aqui:

1. **Parsing do arquivo de histórico** (arquivo próprio do editor, L-13): gerar entradas aleatórias/corrompidas (truncadas, bytes inválidos, impressão digital de mapa que não bate) e confirmar que o editor **recusa** reaplicar sem crashar, nunca "adivinha" o estado.
2. **Repartição de polígono côncavo em peças convexas** (fronteira nossa por decisão da L-03): gerar polígonos aleatórios (côncavos, com vértice colinear, com orientação invertida, degenerados) e verificar as invariantes descritas em T17.

**Ferramenta:** teste baseado em propriedade (ex.: `RapidCheck` ou geração própria com seed fixa e registrada em log) rodando sobre as duas superfícies acima; fuzzing puro (libFuzzer) e opcional, priorizar teste de propriedade por cobrir melhor o espaço de polígonos validos/inválidos.

---

## T4  -  Análise Dinâmica de Memória

**Objetivo:** detectar vazamentos de memória, acessos inválidos e comportamento indefinido em runtime.

**Ferramentas:** AddressSanitizer (ASan) + UndefinedBehaviorSanitizer (UBSan).

**Critério de aprovação:** 0 ERROR SUMMARY, em domínio, aplicação e casca de plataforma (a casca só nos alvos onde o GlintFx já permite build, ver T16).

---

## T8  -  Verificação de Secrets

**Objetivo:** garantir que nenhuma credencial, token ou chave privada foi commitada. Baixa probabilidade de ocorrência neste projeto (não há API externa nem autenticação), mantido por higiene geral.

**Ferramentas:** `gitleaks` + `trufflehog`.

---

## T12  -  Busca de CVEs na Dependência

**Objetivo:** identificar vulnerabilidades conhecidas na única dependência externa deste projeto, o GlintFx, e na cadeia de build (CMake, compilador).

**Ferramentas:** `trivy` ou `grype` apontados para o pin de versão do GlintFx usado no `CMakeLists.txt`/submodulo; consulta a NVD/OSV se o GlintFx publicar CVE próprio.

---

## T14  -  Round-trip de Arquivo (Byte a Byte)

**Objetivo:** garantir que gravar e reler um mapa produz dado idêntico, e que a idempotência (CONTRACT.md §13.10) se sustenta.

**Procedimento obrigatório para qualquer PR que toque leitura/escrita de mapa ou de histórico:**

1. Construir um documento de domínio (mapa) com pelo menos: uma célula de terreno pintada, um objeto posicionado com UUID, um dos seis tipos de volume de colisão (L-14), uma porta e um teleporte.
2. Gravar via API do GlintFx (leitor/escritor público, L-03).
3. Ler de volta o arquivo gravado, também via API do GlintFx.
4. Comparar o documento relido contra o original, campo a campo, e comparar os dois arquivos em disco **byte a byte** (`cmp -s arquivo_a arquivo_b` ou equivalente).
5. Repetir o mesmo procedimento para o arquivo de histórico próprio (L-13): gravar a pilha de comandos, ler de volta, comparar byte a byte.
6. Gravar o mesmo estado duas vezes e confirmar que os dois arquivos resultantes são idênticos (idempotência, CONTRACT.md §13.10).

**Critério de aprovação:** identidade byte a byte nos dois arquivos (mapa e histórico), nas duas direções (escrever->ler, e salvar duas vezes). Qualquer divergência é falha bloqueante, não aviso.

---

## T15  -  Pré-CI, Espelhar CI Localmente

**Objetivo:** rodar a MESMA suíte que o CI roda, antes de push/tag, evitando o ciclo "push, esperar, falhar, corrigir". Projeto de stack único (C++23 + CMake + GlintFx): não há script de Python/Rust/Node aqui.

> **Escopo de uso:** rodar APENAS como pre-flight antes de `git push` que dispara CI/release. NÃO substitui o CI remoto: o envio definitivo SEMPRE passa pelos cinco alvos remotos (L-10), que são a fonte de verdade.

### T15.0  Gate de memória para CI pesado (container local)

Builds C++ com o GlintFx como dependência podem passar de 1 GB de artefato intermediário. Ao rodar o espelhamento em container local, capar o container em memória compatível com a máquina atual (ex.: 8 GB / `-j2` numa máquina de 16 GB) e colocar, como primeiro passo do job pesado, um gate que:

1. Lê `MemAvailable` (`/proc/meminfo` em Linux) e só prossegue quando houver folga suficiente (config por variável de ambiente, com default que funciona sem nada setado).
2. Tem timeout máximo para não travar a fila indefinidamente.
3. Reporta progresso legível a cada leitura (um step mudo por dezenas de minutos parece travado e alguém mata a fila achando que enguiçou).
4. Tem **autoteste dos três caminhos**: limiar já satisfeito (sai na hora), nunca satisfeito (estoura e falha o timeout), satisfeito depois de N leituras (reporta quanto esperou) -- um gate cuja única prova e rodar em produção não tem prova.

Os números exatos (RAM do container, paralelismo, timeout) dependem da máquina que roda o CI local e MUST ser confirmados com o líder via `AskUserQuestion` (sem painel lateral) antes de fixar em script, com a primeira opção marcada como recomendada.

### T15.1  C++23 / CMake / Ninja (único stack deste projeto)

`scripts/preci.sh`:

```bash
#!/usr/bin/env bash
set -euo pipefail
BUILD=build/preci

echo "== clang-format check =="
find src/ tests/ -name '*.cpp' -o -name '*.h' | xargs clang-format --dry-run -Werror

echo "== cmake configure (strict warnings) =="
cmake -S . -B "$BUILD" -G Ninja \
  -DCMAKE_BUILD_TYPE=Debug \
  -DCMAKE_CXX_STANDARD=23 \
  -DCMAKE_CXX_FLAGS="-Wall -Wextra -Wpedantic -Werror -Wshadow -Wnull-dereference"

echo "== compile =="
cmake --build "$BUILD" --parallel

echo "== clang-tidy =="
find src/ -name '*.cpp' -exec clang-tidy {} -p "$BUILD" \;

echo "== cppcheck =="
cppcheck --enable=all --inline-suppr --error-exitcode=1 --suppress=missingIncludeSystem src/

echo "== verificador de camadas (L-12, ver A2) =="
scripts/verificar_camadas.sh src/

echo "== ctest =="
ctest --test-dir "$BUILD" --output-on-failure

echo "ALL GREEN"
```

**Ambiente headless:** quando o alvo exigir rodar a casca de plataforma sem sessão gráfica, usar o mecanismo headless que a própria API do GlintFx expuser (não assumir `QT_QPA_PLATFORM` nem inventar variável própria -- se o GlintFx não tiver modo headless ainda, ver T16).

### T15.2  Container-level (por distro)

Necessário para suspeitar de dependência de SO por alvo (Fedora 44 vs Ubuntu vs Arch vs CachyOS). Usar a imagem oficial de cada distro (`fedora:44` pinada por digest, não `latest`), instalar toolchain mínima (cmake, ninja, clang, cppcheck) e rodar `scripts/preci.sh` dentro do container. Windows não se containeriza da mesma forma: usar runner nativo ou uma VM.

### T15.3  Hook git pre-push (opcional, recomendado)

```bash
#!/usr/bin/env bash
exec scripts/preci.sh
```

`chmod +x .git/hooks/pre-push`. Falha local bloqueia push, evitando viajar ate o CI.

---

## T16  -  Testabilidade sem Janela (Headless)

**Declaração obrigatória, não escondida:** domínio e aplicação (L-12) MUST ser 100% testáveis sem janela, nos cinco alvos de CI (L-10), porque não incluem GlintFx nem SO. A **casca de plataforma não e testável de ponta a ponta ate o GlintFx ter janela** (GODS_LAWS L-14, item 4: o desenho da tela espera o GlintFx).

**Consequência prática, para não confundir "sem teste" com "sem prova":**

1. Todo teste de domínio/aplicação roda em CI normal, sem Xvfb, sem GlintFx, nos cinco alvos.
2. Testes de casca de plataforma que hoje **só podem** verificar chamada-para-fora (ex.: "o caso de uso X chama a função Y do GlintFx com estes argumentos", via dublê/stub da API deles) MUST ser rotulados explicitamente como tal no nome do teste ou no relatório -- nunca apresentados como "a UI funciona".
3. Quando o GlintFx expuser janela, este documento MUST ganhar uma seção T18 de teste headless real (Xvfb/kwin_wayland aninhado, seguindo o precedente do próprio GlintFx) -- ate la, a lacuna fica registrada aqui, não escondida.

---

## T17  -  Repartição Convexa de Polígono

**Objetivo:** a repartição de um polígono côncavo em peças convexas (fronteira que caiu no nosso colo por decisão da L-03, já que o formato do GlintFx só aceita forma simples) é uma classe de código que falha em silêncio: vértice colinear, orientação invertida, polígono degenerado. Ela **MUST nascer** com os dois testes abaixo, nunca depois.

### T17.1  Ida e volta

Para um conjunto de polígonos de teste (incluindo os casos difíceis: vértice colinear, orientação horária e anti-horária, quase-degenerado):

1. Repartir o polígono em peças convexas.
2. Reunir as peças de volta (união geométrica) e confirmar que a área total é igual a área do polígono original, dentro de uma tolerância de ponto flutuante explícita e documentada (nunca comparação exata de `double`).
3. Confirmar que nenhum vértice do polígono original foi perdido ou duplicado no processo.

### T17.2  Convexidade de cada peça gerada

Para **cada** peça resultante da repartição:

1. Confirmar convexidade real: percorrer os vértices em ordem e verificar que o sinal do produto vetorial entre arestas consecutivas não muda (sem ângulo reflexo).
2. Rejeitar peça com menos de 3 vértices distintos (degenerada).
3. Rejeitar peça com área próxima de zero (dentro de uma tolerância documentada).
4. Confirmar orientação consistente (todas as peças no mesmo sentido, horário ou anti-horário) para não inverter normal/colisão no GlintFx.

**Critério de aprovação:** as duas suítes (T17.1 e T17.2) MUST rodar sobre um conjunto de polígonos gerado por T3 (fuzzing/propriedade), não apenas sobre exemplos fixos escritos à mão.

---

## A2  -  Auditoria de Arquitetura e Camadas

**Objetivo:** validar que nenhuma camada viola a regra de dependência da L-12.

**Procedimento:**

1. Rodar o verificador de camadas (script próprio, ex.: `scripts/verificar_camadas.sh`, baseado em `grep`/`ast-grep` sobre `#include`) contra `src/dominio/`, `src/aplicacao/` e `src/casca/` (nomes de diretório em ASCII sem acento, por serem caminho de arquivo num projeto que builda em Windows, L-10; os nomes reais definitivos ficam a critério de quem escrever o `CMakeLists.txt`).
2. **O verificador MUST imprimir `Arquivos varridos: N` e falhar se `N == 0` (L-09, ver seção 0 deste documento).**
3. Falha se qualquer arquivo de `dominio/` incluir header de `aplicacao/`, `casca/`, GlintFx ou do SO.
4. Falha se qualquer arquivo de `aplicacao/` incluir header do GlintFx ou do SO.
5. Falha se algum outro diretório, além de `casca/`, incluir header do GlintFx.

**Critério de aprovação:** 0 violações criticas, com `N > 0` arquivos efetivamente varridos.

---

## A3  -  UI/UX (via GlintFx)

**Objetivo:** verificar que a experiência pedida ao GlintFx (CONTRACT.md §7) é coerente -- contraste, navegação por teclado, consistência de tema -- na medida em que a API deles já expõe esses recursos. Onde não expõe, confirmar que a necessidade foi registrada no bus (L-01), não contornada.

---

## A10  -  Relatório Final de Auditoria

**Objetivo:** consolidar todos os resultados (T1-T17, A2-A3) em um único documento com score global (0-100), sumário de problemas classificados (ver seção seguinte) e patches unificados.

**Lembrete (L-06):** este relatório e produzido por um C-level em modelo fable, nunca pelo agente que implementou o código auditado.

---

## Classificação de Problemas

| Prioridade | Significado | Exemplo neste projeto |
|---|---|---|
| 🔴 CRÍTICO | Bloqueia release; viola lei do líder ou corrompe dado do usuário | Header de GlintFx fora da casca; round-trip de mapa não bate byte a byte |
| 🟠 IMPORTANTE | Não bloqueia, mas deve ser corrigido na próxima janela | Peca de polígono quase-degenerada sem teste de fronteira |
| 🟢 COSMÉTICO | Estilo, nomenclatura, comentário | Função maior que 40 linhas sem quebra lógica evidente |

---

## Formato de Patch

Patches de correção encontrados em auditoria MUST ser entregues como diff unificado (`diff -u` / `git diff` de um commit isolado), nunca como descrição em prosa do que mudar. Cada patch referência o item da tabela de classificação (ex.: "corrige CRÍTICO #3") e, se fechar item do `TODO.md`, cita o ID no commit (CONTRACT.md §10.2).
