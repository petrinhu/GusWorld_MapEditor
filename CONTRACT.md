# AI Coder Contract  -  Best Practices, Architecture & Standards (gusworld_mapeditor)

> **Audience:** AI coding agents (Claude, GPT, Gemini, Copilot, etc.)
> **Purpose:** Mandatory reference before writing, modifying, or reviewing any code neste projeto.
> **Authority:** Rules use RFC 2119 keywords  -  MUST, MUST NOT, SHOULD, SHOULD NOT, MAY.
> **Precedência:** [`GODS_LAWS.md`](GODS_LAWS.md) vence este contrato em qualquer conflito. Leia-o antes de agir; os gatilhos relevantes (L-01, L-04, L-05, L-06, L-09, L-10, L-12, L-13, L-14) estão citados abaixo nos pontos onde se aplicam.
> **Testing & Audit:** All testing, quality and audit procedures are defined in [TESTES.md](TESTES.md). Checklists de auditoria em [AUDITORIAS.md](AUDITORIAS.md).
> **Escopo:** este é um editor de mapa desktop, local, de usuário único, construído em C++23 sobre o framework GlintFx (`../GlintFx` / `github.com/petrinhu/GlintFx`), sem rede, sem banco de dados, sem servidor. Seções da versão genérica deste contrato que pressupunham Qt, SQL, REST/HTTP ou frontend web foram removidas ou reescritas; ver seção 14 para o detalhe.

---

## Table of Contents

1. [How to Use This Document](#1-how-to-use-this-document)
2. [OOP Fundamentals](#2-oop-fundamentals)
3. [SOLID Principles](#3-solid-principles)
4. [Design Patterns  -  Reference](#4-design-patterns--reference)
5. [Camadas de Arquitetura (L-12)](#5-camadas-de-arquitetura-l-12)
6. [Clean Code Rules](#6-clean-code-rules)
7. [UI/UX Guidelines (via GlintFx)](#7-uiux-guidelines-via-glintfx)
8. [Segurança e Validação de Entrada](#8-segurança-e-validação-de-entrada)
9. [Performance](#9-performance)
10. [Git Process for AI Coders](#10-git-process-for-ai-coders)
11. [Testing & Audit Mandate](#11-testing--audit-mandate)
12. [C++23 e a Fronteira com o GlintFx](#12-c23-e-a-fronteira-com-o-glintfx)
13. [Universal Engineering Principles](#13-universal-engineering-principles)
14. [Fora de Escopo  -  o que foi removido e por quê](#14-fora-de-escopo--o-que-foi-removido-e-por-quê)

---

## 1. How to Use This Document

**Before writing any code, the AI coder MUST:**

1. Read [`GODS_LAWS.md`](GODS_LAWS.md) e conferir se algum gatilho casa com a tarefa (protocolo descrito lá).
2. Read this document fully for the first task in a project.
3. Identify the architecture layer being modified  -  Domínio, Aplicação ou Casca de Plataforma (seção 5).
4. Apply section 12 (C++23 sem Qt, fronteira com o GlintFx).
5. After completing any task: run the checklist in section 11.

**Decision flow:**

```
New task received
      │
      ▼
Ler GODS_LAWS.md (gatilhos) ──► Ler código existente ──► Entender o contexto
      │
      ▼
Identificar camada (Domínio / Aplicação / Casca de Plataforma)
      │
      ▼
Aplicar SOLID + Design Patterns + regra de dependência (§5)
      │
      ▼
Escrever código → Build → Sem erros/warnings?
      │
      ▼
Rodar os testes aplicáveis de TESTES.md
      │
      ▼
Commit em Conventional Commits, citando o ID do TODO.md
      │
      ▼
Done
```

**What the AI coder MUST NOT do:**
- Write code without reading existing files first.
- Add features beyond what was requested.
- Introduce hardcoded secrets, credentials, or API keys.
- Skip the build step before committing.
- Use deprecated APIs, unsafe functions, or patterns marked ANTI-PATTERN below.
- Ignore compiler warnings.
- Incluir header de RmlUi, SDL, GLFW, Qt ou qualquer outro terceiro, ou chamar o sistema operacional diretamente (L-01).

---

## 2. OOP Fundamentals

### 2.1 The Four Pillars

**Encapsulation**
- MUST hide internal state. Expose only what callers need.
- MUST use private/protected for data members, public only for interface.

```cpp
// CORRECT
class GerenciadorHistorico {
public:
    bool registrar(const std::string& id_comando, std::vector<std::byte> dados);
    std::optional<std::vector<std::byte>> recuperar(const std::string& id_comando) const;
private:
    std::unordered_map<std::string, std::vector<std::byte>> m_registro;  // hidden
    std::size_t m_tamanho_max{1000};                                     // hidden
};

// INCORRECT  -  exposes internals
class GerenciadorHistorico {
public:
    std::unordered_map<std::string, std::vector<std::byte>> registro;   // direct access = violation
};
```

**Abstraction**
- MUST define interfaces (pure abstract classes) apenas onde há polimorfismo real e presente (não especulativo  -  ver YAGNI §13.2). Ver §5 para a exceção deliberada da fronteira com o GlintFx, que **não** usa interface.
- MUST NOT let callers depend on implementation details.

**Inheritance**
- SHOULD prefer composition over inheritance.
- MUST NOT use inheritance for code reuse alone  -  only for true IS-A relationships.
- Inheritance depth MUST NOT exceed 3 levels.

**Polymorphism**
- MUST use virtual dispatch via interfaces, not type-checking (no `dynamic_cast` chains).
- MUST mark overrides with `override`.

### 2.2 Class Design Rules

- One class = one clearly stated responsibility.
- Class size: SHOULD NOT exceed 300 lines. If it does, decompose.
- Constructor MUST NOT perform heavy work (I/O, cálculo pesado). Use an `inicializar()` method.
- MUST implement the Rule of Five/Zero or equivalent resource management.

---

## 3. SOLID Principles

### S  -  Single Responsibility Principle
> A class should have only one reason to change.

- Each class owns one concept: parsear, desenhar (via GlintFx), aplicar um comando, validar  -  never all at once.
- Test: if you describe the class and use the word "and", split it.

```
CORRECT:  ComandoMoverObjeto      ->  só aplica/desfaz um movimento
CORRECT:  RepositorioHistorico    ->  só persiste/le a pilha de comandos
INCORRECT: ComandoMoverObjeto     ->  aplica movimento E persiste E valida geometria
```

### O  -  Open/Closed Principle
> Open for extension, closed for modification.

- Add behavior via new classes, not by editing existing ones.
- Use Strategy, Decorator, or plugin patterns to extend without modifying.

```cpp
// CORRECT  -  novo tipo de comando sem tocar no código existente
class IComando {
public:
    virtual void aplicar() = 0;
    virtual void desfazer() = 0;
    virtual ~IComando() = default;
};
class ComandoMoverObjeto : public IComando { /* ... */ };
class ComandoPintarCelula : public IComando { /* ... */ };  // extension, not modification
```

### L  -  Liskov Substitution Principle
> Subtypes must be substitutable for their base types without breaking behavior.

- An override MUST NOT weaken preconditions or strengthen postconditions.
- An override MUST NOT throw exceptions the base does not declare.
- MUST NOT override to do nothing or throw silently.

```cpp
// INCORRECT  -  viola LSP: override não faz nada, falha em silencio
class ComandoNulo : public IComando {
    void aplicar() override {}  // silent failure
};

// CORRECT  -  objeto nulo explícito que documenta a intencao
class ComandoNulo : public IComando {
    void aplicar() override {
        // usado apenas em teste; nunca deve chegar a pilha de histórico real
        assert(false && "ComandoNulo não deve ser aplicado em produção");
    }
};
```

### I  -  Interface Segregation Principle
> Clients should not depend on interfaces they do not use.

- Split fat interfaces into role-specific ones.
- Each interface SHOULD have <= 5 methods.

```cpp
// INCORRECT  -  uma interface gorda
class IArmazenamento {
    virtual void salvarMapa() = 0;
    virtual void lerMapa() = 0;
    virtual void salvarHistorico() = 0;
    virtual void lerHistorico() = 0;
    virtual void exportarRelatorio() = 0;   // não relacionado
};

// CORRECT  -  segregado
class ILeitorHistorico  { virtual std::vector<ComandoSerializado> ler() = 0; };
class IEscritorHistorico { virtual void escrever(const std::vector<ComandoSerializado>&) = 0; };
```

### D  -  Dependency Inversion Principle
> Depend on abstractions, not concretions.

- High-level modules MUST NOT import low-level modules directly.
- Inject dependencies via constructor (preferred), setter, or factory.
- **Exceção deliberada:** a casca de plataforma (§5) depende **direto** da API concreta do GlintFx, sem interface própria  -  ver §5 para a justificativa (L-12).

```cpp
// CORRECT  -  aplicação depende de abstracao, injetada via construtor
class ServicoDesfazer {
    std::shared_ptr<IEscritorHistorico> m_escritor;
public:
    explicit ServicoDesfazer(std::shared_ptr<IEscritorHistorico> escritor)
        : m_escritor(std::move(escritor)) {}
};
```

---

## 4. Design Patterns  -  Reference

Apply patterns when they solve a real problem. MUST NOT apply patterns speculatively (YAGNI, §13.2).

### 4.1 Creational Patterns

| Pattern | Use When | Key Rule |
|---------|----------|----------|
| **Singleton** | Exactly one instance needed (ex.: registro de UUIDs em uso) | MUST be thread-safe se acessado de mais de uma thread. AVOID quando dificultar teste  -  prefer DI. |
| **Factory Method** | Subclasses decidem qual comando/volume criar | Define abstract `criar()`, override in subclasses. |
| **Abstract Factory** | Familias de objetos relacionados (ex.: os seis tipos de volume de colisao da L-14) | One factory interface, multiple concrete factories. |
| **Builder** | Construcao de objeto complexo com muitos parâmetros opcionais | Separate construction from representation. |
| **Prototype** | Clonar objetos caros (ex.: duplicar um objeto posicionado) | Implement deep copy. Avoid shared mutable state. |

```cpp
// Builder example
class ComandoBuilder {
    DescricaoComando m_desc;
public:
    ComandoBuilder& tipo(std::string t)      { m_desc.tipo = std::move(t); return *this; }
    ComandoBuilder& alvo(std::string id)     { m_desc.alvo_id = std::move(id); return *this; }
    DescricaoComando build() { return std::move(m_desc); }
};
```

### 4.2 Structural Patterns

| Pattern | Use When | Key Rule |
|---------|----------|----------|
| **Adapter** | Interface incompativel precisa funcionar com a nossa | Wrap external API to match internal interface. |
| **Bridge** | Separar abstracao de implementação | Decouple só both can vary independently. |
| **Composite** | Estruturas em árvore (ex.: selecao múltipla de objetos) | Leaf and composite share same interface. |
| **Decorator** | Adicionar comportamento dinamicamente | Wrap object, delegate, then extend. |
| **Facade** | Simplificar acesso a um subsistema complexo | One simple interface over many complex classes. |
| **Flyweight** | Muitos objetos compartilhando estado comum (ex.: definição do tipo de volume, reaproveitada por muitas instâncias posicionadas) | Separate intrinsic (shared) from extrinsic (unique) state. |
| **Proxy** | Controlar acesso, lazy init | Same interface as real object. |

```cpp
// Composite: aplicar um comando a um grupo de objetos selecionados
class ComandoComposto : public IComando {
    std::vector<std::unique_ptr<IComando>> m_filhos;
public:
    void aplicar() override { for (auto& c : m_filhos) c->aplicar(); }
    void desfazer() override { for (auto& c : m_filhos | std::views::reverse) c->desfazer(); }
};
```

### 4.3 Behavioral Patterns

| Pattern | Use When | Key Rule |
|---------|----------|----------|
| **Chain of Responsibility** | Multiplos handlers podem processar um evento de entrada | Each handler decides to handle or pass forward. |
| **Command** | Encapsular ação como objeto: é a espinha dorsal do undo/redo exigido pela L-13 | Separate invoker from receiver; MUST ser serializável (L-13). |
| **Iterator** | Percorrer coleção sem expor internals | Use standard iteration protocol. |
| **Mediator** | Reduzir acoplamento entre muitos objetos | Central hub coordinates communication. |
| **Memento** | Salvar/restaurar estado de objeto | Snapshot without violating encapsulation; NÃO e a estratégia de undo/redo aqui (L-13 exige comando, não snapshot do mapa inteiro). |
| **Observer** | Notificar dependentes de mudança de estado: e como as vistas assinam o histórico (L-13, regra 4) | Se a API do GlintFx expuser um mecanismo de evento/callback próprio, usa-lo (L-01); nunca inventar um paralelo. |
| **State** | Objeto muda de comportamento conforme estado interno | Replace conditionals with state objects. |
| **Strategy** | Trocar algoritmo em tempo de execucao | Extract algorithm family into interchangeable objects. |
| **Template Method** | Definir esqueleto, subclasses preenchem passos | Base class controls flow, subclasses override steps. |
| **Visitor** | Adicionar operações a uma estrutura de objetos sem modificá-la | Separate algorithm from object structure. |

### 4.4 Modern / Architectural Patterns

| Pattern | Use When |
|---------|----------|
| **Repository** | Abstrair a origem de um dado (ex.: leitura/escrita do arquivo de histórico) da lógica de aplicação. |
| **Event Sourcing** | Aplica-se diretamente a L-13: a pilha de comandos serializados e a fonte de verdade do histórico, não um snapshot do mapa. |
| **Dependency Injection** | Fornecer dependências de fora da classe (via construtor). |
| **Service Locator** | AVOID  -  dependência escondida, difícil de testar. Use DI instead. |
| **MVC / MVP / MVVM** | Separar estado do domínio (Model) da apresentação. Na casca de plataforma, o "View" e a chamada a API de desenho do GlintFx; MUST NOT reconstruir o estado do domínio a partir do que foi desenhado. |
| **Null Object** | Evitar checagens de null: fornecer implementação padrao que não faz nada, documentada. |
| **Specification** | Encapsular regras de negócio como predicados compostos (ex.: validar se um polígono e convexo, ver TESTES.md T17). |

---

## 5. Camadas de Arquitetura (L-12)

Este projeto usa camadas horizontais finas, com a dependência apontando só para dentro. Este modelo substitui integralmente o modelo genérico Frontend/Middleware/Backend/Infraestrutura das versoes anteriores deste contrato, que pressupunha HTTP, SQL e UI framework: nada disso existe aqui.

```
+-------------------------------------------------------------+
|  DOMÍNIO                                                     |
|  Documento de mapa, celula, objeto posicionado, hitbox,      |
|  porta, teleporte, selecao, comando, pilha de histórico.     |
|  POCO puro.                                                  |
|  CAN: regra de negócio pura, estruturas de dados             |
|  CANNOT: incluir header do GlintFx, do SO, ou de terceiro    |
+-------------------------------------------------------------+
|  APLICAÇÃO                                                   |
|  Um caso de uso por operação de edição, pequeno e            |
|  testavel sozinho. Nunca um serviço-deus com dezenas de      |
|  métodos.                                                    |
|  CAN: orquestrar o domínio                                   |
|  CANNOT: incluir header do GlintFx, do SO, ou de terceiro    |
+-------------------------------------------------------------+
|  CASCA DE PLATAFORMA                                         |
|  Fina. ÚNICA camada autorizada a incluir header do           |
|  GlintFx, chamado DIRETO, sem interface própria.             |
|  CAN: chamar a API pública do GlintFx                        |
|  CANNOT: conter regra de negócio do mapa                     |
+-------------------------------------------------------------+
```

**Por que a casca não tem interface própria (L-12):** o GlintFx é a única implementação que vai existir, por lei (L-01); e a API de janela, desenho e entrada ainda está em construção: desenhar uma porta hoje é supor uma forma que pode não existir amanhã. Uma interface aqui reproduziria a "camada de tradução" que a L-03 já proíbe no ecossistema. Se um dia houver razão concreta (não hipotética) para fingir essa fronteira em teste, a saída é um `concept` de C++23 resolvido em compilação, nunca uma interface virtual.

**A proteção do domínio não vem de interface, vem de regra de dependência fiscalizada por portão de CI:**

- `domínio` nunca inclui header de `aplicação` nem de `casca de plataforma`, nem de GlintFx, nem do SO.
- `aplicação` nunca inclui header de GlintFx nem do SO.
- Só `casca de plataforma` inclui GlintFx.
- **O portão que fiscaliza isso DEVE declarar quantos arquivos varreu, e sair com zero arquivos varridos é falha, não sucesso (L-09)**: procedimento e exemplo concreto em [TESTES.md secao A2](TESTES.md#a2--auditoria-de-arquitetura-e-camadas).

**Nomenclatura de diretório real (quando o código nascer):** os nomes acima (domínio, aplicação, casca) são conceituais. Nos diretórios de verdade em `src/`, usar ASCII sem acento (ex.: `dominio/`, `aplicacao/`, `casca/`) por serem caminho de arquivo num projeto que builda em Windows como um dos cinco alvos de CI (L-10); acento em nome de diretório é fonte evitável de dor cross-platform.

**"Átomos com POCO próprio"** vale no domínio e nos casos de uso, onde se paga sozinho: classe pequena, responsabilidade única, sem interface desnecessária. **Não** vale para a casca de plataforma: exigir um átomo por campo de um painel de inspeção num editor de usuário único é over-engineering. Átomo é sobre tamanho e responsabilidade, não sobre indireção: um POCO concreto de vinte linhas, sem interface nenhuma, é um átomo perfeito.

### Checklist antes de commitar

```
[ ] A classe pertence a exatamente uma camada?
[ ] Nenhuma dependência para cima (domínio -> aplicação, aplicação -> casca)?
[ ] Nenhum header de GlintFx fora da casca de plataforma?
[ ] Nenhum header de SO, RmlUi, SDL, GLFW ou Qt em lugar nenhum (L-01)?
```

---

## 6. Clean Code Rules

### 6.1 Naming

- Names MUST reveal intent. No abbreviations unless universally known (`id`, `url`).
- Functions: verb + noun (`buscarObjeto`, `aplicarComando`, `desenharCelula`).
- Booleans: `is`, `has`, `can`, `should` prefix (`isConvexo`, `hasHistoricoValido`, `canDesfazer`).
- Constants: ALL_CAPS with underscores (`MAX_VERTICES`, `TIPOS_DE_VOLUME`).
- Private members: `m_` prefix.
- MUST NOT use single-letter names except loop counters (`i`, `j`) and lambda args.

### 6.2 Functions

- MUST do one thing. If you can extract a sub-function with a meaningful name, do it.
- MUST NOT exceed 40 lines. If longer, decompose.
- MUST NOT take more than 4 parameters. Wrap in struct if needed.
- Return early to avoid deep nesting. MUST NOT exceed 3 levels of nesting.

```cpp
// INCORRECT: deep nesting
void processar(ComandoBruto c) {
    if (c.valido()) {
        if (!histórico.contem(c.id)) {
            if (mapa.aceita(c)) {
                // actual logic buried here
            }
        }
    }
}

// CORRECT: early returns (guard clauses)
void processar(const ComandoBruto& c) {
    if (!c.valido()) return;
    if (histórico.contem(c.id)) return;
    if (!mapa.aceita(c)) { reportarErro("comando rejeitado pelo mapa"); return; }
    // actual logic at top level
}
```

### 6.3 Comments

- MUST NOT comment what the code does. Comment **why** it does it.
- MUST comment every workaround, hack, or non-obvious decision.
- MUST update comments when changing the code they describe.

```cpp
// INCORRECT
i++;  // increment i

// CORRECT
// o formato do GlintFx e 1-based para indice de camada (L-03); nosso domínio e 0-based
camada_gmap = camada_dominio + 1;
```

### 6.4 Error Handling

- MUST handle all error cases. MUST NOT silently swallow exceptions.
- MUST propagate errors to the caller: do not hide failures.
- MUST NOT use exceptions for control flow.
- Use `std::optional` ou `std::expected` (padrao desde C++23) para falhas esperadas (ex.: arquivo de histórico ausente, mapa corrompido).

### 6.5 Constants vs Magic Numbers

```cpp
// INCORRECT
if (vertices.size() < 3) return;

// CORRECT
constexpr std::size_t MIN_VERTICES_POLIGONO = 3;
if (vertices.size() < MIN_VERTICES_POLIGONO) return;
```

### 6.6 RAII and Resource Management

- MUST use RAII for all resources (memória, arquivos, mutexes).
- MUST prefer smart pointers (`unique_ptr`, `shared_ptr`) over raw `new`/`delete`.
- MUST NOT call `delete` manually in application code.
- MUST NOT store raw owning pointers.
- Recursos do GlintFx (janela, textura, etc.) MUST ser envolvidos no wrapper RAII que a própria API deles fornecer; nunca gerenciados por ponteiro cru nosso.

### 6.7 DRY  -  Don't Repeat Yourself

**Regra de Tres:** Na **primeira** ocorrencia, escreva. Na **segunda**, registre a repeticao. Na **terceira**, extraia.

```cpp
// 1a e 2a ocorrencias: duplicação aceitavel (WET: Write Everything Twice)
bool dentroDosLimites(int v, int min, int max) { return v >= min && v <= max; }
bool validarLargura(int v)  { return v >= 1 && v <= 256; }

// 3a ocorrencia: EXTRAIA: nomeie a razão comum de mudança
// Razao: "validar dimensão inteira de celula de mapa dentro do teto do formato"
bool validarDimensaoCelula(int valor, int minimo, int maximo) {
    return valor >= minimo && valor <= maximo;
}
```

**Duplicacao real vs. coincidência:**

| Tipo | Definicao | Regra |
|------|-----------|-------|
| **Duplicacao real** | Mesmo conceito, mesma razão de mudar | MUST extrair |
| **Coincidencia** | Parece similar hoje; divergira amanha | MUST NOT unificar |

**Rules (RFC 2119):**

- MUST name the *common reason to change* when extracting: similarity in code alone is insufficient justification.
- MUST NOT unify logic with distinct meanings even if syntactically identical (ex.: validar largura de celula e validar numero de abas abertas são coincidência, não duplicação, ainda que ambos sejam "int dentro de faixa").
- SHOULD prefer WET over a premature abstraction that fits neither caller.
- MUST NOT create generic helpers to avoid two similar lines; three real occurrences are required.
- MAY tolerate duplication in tests when each test independently documents a distinct behavior.

---

## 7. UI/UX Guidelines (via GlintFx)

Este editor não desenha nada diretamente (L-01, L-12): toda apresentação passa pela API do GlintFx, chamada exclusivamente pela casca de plataforma. As regras abaixo valem para a experiencia que a casca pede ao GlintFx para produzir, não para código de widget: não existe widget aqui.

### 7.1 Responsiveness

- MUST NEVER bloquear a thread principal com I/O ou computacao pesada (ex.: repartição de polígono em lote, leitura de arquivo grande).
- Operacoes que passem de 100ms MUST mostrar indicacao de progresso (se o GlintFx expuser o recurso; senao, registrar a necessidade no bus: L-01).

### 7.2 Feedback

- Every user action MUST produce visible feedback within 200ms.
- Error messages MUST be human-readable, not stack traces or error codes.
- Estados de sucesso/falha MUST ser distinguiveis por mais de uma cor (icone ou texto também).

### 7.3 Acessibilidade

- Elementos interativos MUST ser alcancaveis via teclado, quando a API do GlintFx expuser foco/navegacao por teclado.
- Contraste de texto SHOULD seguir WCAG AA (>= 4.5:1 texto normal, >= 3:1 texto grande) como referência de design, ainda que o tema seja o do GlintFx, não nosso.
- **Se o GlintFx não expuser um destes recursos hoje, a saida e registrar a necessidade pelo bus (L-01), nunca implementar um substituto paralelo.**

### 7.4 Consistency

- MUST usar o sistema de tema do GlintFx para cor, espacamento e tipografia.
- MUST NOT hardcode valor de cor na casca de plataforma: usar o token de tema exposto pela API deles.

### 7.5 Edição de Campos (painel de inspeção)

- MUST validar entrada no momento da submissao, não silenciosamente ao perder o foco.
- MUST mostrar erro de validação junto ao campo problematico.
- MUST NOT limpar o campo em caso de erro: preservar o que o autor digitou.

---

## 8. Segurança e Validação de Entrada

Este projeto não tem rede, servidor, autenticacao, banco de dados nem múltiplos usuários: a superficie de ataque tradicional (OWASP Top 10, SQL injection, SSRF, CSRF) não existe aqui e foi removida desta secao (ver §14). O que resta e hygiene geral e validação de entrada de arquivo/usuario.

### 8.1 Ameaças relevantes para um editor local

| Ameaca | Regra |
|---|---|
| Arquivo de mapa corrompido ou malicioso (lido via API do GlintFx) | MUST tratar toda falha de leitura explicitamente; MUST NOT crashar; ver TESTES.md T14. |
| Arquivo de histórico corrompido ou desatualizado (arquivo próprio, L-13) | MUST recusar reaplicar se a impressao digital do mapa não bater; MUST NOT tentar "adivinhar" o estado. |
| Entrada de usuario em campo numerico/texto do inspetor | MUST validar faixa e tipo antes de aplicar ao domínio. |

### 8.2 Hardcoded Secrets  -  Zero Tolerance

Este editor não fala com nenhuma API externa, mas a regra permanece por hygiene geral:

```cpp
// INCORRECT: NEVER commit this
const std::string TOKEN = "sk-live-abc123xyz789";

// CORRECT: se um dia isso for necessário, carregar de fora do binario
```

### 8.3 Input Validation

- MUST validate all data arriving from: leitura de arquivo (mapa via GlintFx, histórico próprio), entrada do usuario via UI.
- MUST NOT trust data from any external source, incluindo arquivos gravados pelo próprio editor em versão anterior.
- MUST constrain string lengths, numeric ranges, and allowed characters at entry points.

---

## 9. Performance

### 9.1 General Rules

- MUST profile before optimizing. No premature optimization.
- MUST cache results of expensive operations (I/O de disco, repartição de polígono, calculo geométrico).
- MUST use lazy loading for data not immediately needed (ex.: mapas não abertos nas abas).
- MUST NOT copy large objects unnecessarily: use references and move semantics.

### 9.2 Memória

- MUST release resources when they go out of scope (RAII).
- MUST NOT hold large objects in memory indefinitely: histórico ilimitado em memória e aceitavel apenas porque e persistido (L-13); vazamento de objeto de domínio não e.
- Recursos do GlintFx MUST ser liberados conforme o contrato de vida da API deles, nunca gerenciados por conta própria (L-01).

### 9.3 Desenho

- A casca de plataforma MUST NOT fazer calculo geométrico pesado dentro do laco de desenho por quadro: repartição de polígono côncavo (L-03) e operações similares MUST ser calculadas uma vez, no momento da edição/gravacao, e cacheadas.
- Toda chamada a API de desenho do GlintFx acontece na casca; domínio e aplicação nunca desenham (§5).

---

## 10. Git Process for AI Coders

### 10.1 Before Writing Any Code

```bash
# MUST: read current state of files to be modified
# MUST: understand existing patterns before introducing new ones
# MUST: check if a build passes before starting
cmake --build build -j$(nproc) 2>&1 | grep -E "error:|warning:"
```

### 10.2 Conventional Commits (MANDATORY)

Format: `<type>(<scope>): <description>`

| Type | When to use |
|------|------------|
| `feat` | New feature added |
| `fix` | Bug fix |
| `refactor` | Code change without feature or fix |
| `docs` | Documentation only |
| `test` | Adding or fixing tests |
| `chore` | Build, CI, dependencies, tooling |
| `perf` | Performance improvement |
| `style` | Formatting, no logic change |
| `revert` | Reverting a previous commit |

```bash
# CORRECT examples
git commit -m "feat(histórico): add UUID-based undo stack persistence"
git commit -m "fix(mapa): round-trip byte-a-byte falhava em objeto sem UUID"

# INCORRECT
git commit -m "fix stuff"
git commit -m "WIP"
```

**Convencao deste projeto:** ao fechar ou avancar um item do `TODO.md`, citar o ID (ex.: `M1.3`) no corpo/footer do commit e tocar a coluna `Status` no mesmo commit (implementação entregue -> `Pendente verificação`, nunca aprovado direto).

### 10.3 Branch Naming

```
feat/nome-da-feature
fix/descrição-do-bug
refactor/módulo-afetado
docs/nome-do-documento
chore/ferramenta-ou-dep
test/módulo-testado
```

### 10.4 Commit Checklist (MUST complete before every commit)

```
[ ] Build passes with zero errors
[ ] Zero new compiler warnings introduced
[ ] No hardcoded secrets, tokens, or credentials
[ ] .gitignore excludes build artifacts, IDE files
[ ] Commit message follows Conventional Commits format, cita ID do TODO.md quando aplicavel
[ ] Files staged are only those related to the current task
```

### 10.5 What the AI MUST NEVER Do in Git

- MUST NOT force-push to `main` or `master`.
- MUST NOT commit files containing secrets.
- MUST NOT amend published commits (use a new commit instead).
- MUST NOT use `--no-verify` to skip hooks unless explicitly instructed.
- MUST NOT batch unrelated changes into one commit.
- MUST NOT commit generated build artifacts (`build/`, `CMakeFiles/`, binarios).
- MUST NOT push or merge em `main` sem autorizacao explícita do lider (L-05/L-06).

### 10.6 Pull Request Description Template

```markdown
## What
[One sentence: what this PR does]

## Why
[One sentence: why it was needed]

## Checklist
- [ ] Build passes nos alvos aplicaveis (ver TESTES.md T15)
- [ ] Tests pass (referenciar secoes de TESTES.md rodadas)
- [ ] No new warnings
- [ ] No secrets committed
```

---

## 11. Testing & Audit Mandate

> Full procedures, commands, and tools: **[TESTES.md](TESTES.md)**. Checklists de auditoria: **[AUDITORIAS.md](AUDITORIAS.md)**.

**Lembrete permanente (L-09):** todo portão automático (script de CI, verificador de camadas, scanner) DEVE imprimir quantos arquivos varreu, e sair com zero arquivos varridos e falha, não sucesso.

**Lembrete permanente (L-06):** implementador, revisor e orquestrador são três agentes diferentes; auditoria e feita por C-level em modelo fable, execucao por agents operacionais em modelo sonnet; implementador nunca audita o próprio trabalho.

### When to Run Tests

| Event | Required tests |
|-------|---------------|
| Every commit | Build passes, zero warnings |
| Feature de domínio/aplicação completa | T1 (unit), T2 (estática), T4 (ASan/UBSan) |
| Tocar leitura/escrita de mapa ou histórico | T14 (round-trip byte a byte) |
| Tocar repartição de polígono côncavo | T3 (propriedade) + T17 (convexidade) |
| Antes de qualquer release | T1, T2, T3, T4, T8, T12, T14, T15, T16, T17 completos + A2, A3, A10 |
| Nova dependência adicionada | T12 (CVE check) |
| Camada (domínio/aplicação/casca) mudou | A2 (auditoria de camadas) |

### Minimum Quality Gates (MUST pass before release)

```
[ ] T1  Unit tests: 0 falhas
[ ] T2  Static analysis: 0 erros
[ ] T4  ASan/UBSan: 0 ERROR SUMMARY
[ ] T8  Secrets scan: 0 detectados
[ ] T12 CVE scan: 0 CRÍTICO sem patch
[ ] T14 Round-trip de arquivo: byte a byte identico
[ ] T17 Repartição de polígono: toda peça gerada e convexa
[ ] A2  Camadas: 0 violações de dependência, portão declarou N > 0 arquivos varridos
[ ] A10 Relatório de auditoria gerado e revisado
```

### Post-Release Cleanup Prompt (MANDATORY)

Apos uma release ser efetivamente lancada (tag publicada + artefatos anexados + CI verde no remoto), o agente DEVE perguntar ao usuario se deseja apagar pastas desnecessarias geradas durante o ciclo de build/test (`build/`, `build-*/`, `CMakeFiles/`, `_deps/`, `Testing/`).

**Regras invioláveis:** nunca apagar pasta versionada; sempre listar (`du -sh`) antes, confirmar depois; excluir caminhos rastreados pelo git ou com mudanças não commitadas antes de propor a remocao.

---

## 12. C++23 e a Fronteira com o GlintFx

**Versão:** C++23. **Exceção deliberada ao padrao global do vault** (que e C++/Qt23): este projeto usa C++23 sem Qt, por ordem direta do lider (L-01). Nenhum arquivo deste repositorio inclui header de Qt, RmlUi, SDL ou GLFW.

**Única dependência externa:** GlintFx, incluído apenas na casca de plataforma (§5, L-12). Se uma funcionalidade precisar de algo que a API pública do GlintFx não oferece, a resposta e registrar a necessidade pelo bus e esperar: nunca inventar um contorno (L-01).

**Memória:**
```cpp
// MUST use smart pointers
auto obj = std::make_unique<ComandoMoverObjeto>();
auto compartilhado = std::make_shared<RepositorioHistorico>();

// MUST NOT
ComandoMoverObjeto* cru = new ComandoMoverObjeto();  // quem e dono disso?
delete cru;                                           // delete manual = risco de leak
```

**Modern C++23 MUST-use features:**
```cpp
std::optional<Objeto>                       // instead of nullptr checks
std::expected<Objeto, ErroLeitura>          // padrao em C++23, não mais experimental
[[nodiscard]]                                // on functions whose return value must be checked
const auto&                                  // prefer const references
if (auto val = buscar(); val.has_value())    // init-statement in if
```

**MUST NOT use:**
```cpp
NULL           // use nullptr
(Tipo*)ptr     // use static_cast<Tipo*>(ptr)
printf/scanf   // use std::print / std::format (C++23)
gets()         // buffer overflow risk
strcpy/strcat  // use std::string
```

**Concorrencia:** se uma tarefa exigir thread própria (ex.: I/O de arquivo grande sem travar a UI), usar `std::jthread`/`std::stop_token` (C++23). MUST NOT introduzir concorrencia especulativa: só onde há necessidade concreta e presente (YAGNI, §13.2).

---

## 13. Universal Engineering Principles

> Complement to SOLID and DRY. Apply across the codebase.

### 13.1 KISS  -  Keep It Simple, Stupid

- MUST NOT add layers of abstraction without a concrete, present reason.
- MUST NOT use a design pattern just because it fits: only when it removes real pain.
- When two solutions work, MUST choose the one a new team member understands in 30 seconds.

### 13.2 YAGNI  -  You Aren't Gonna Need It

- MUST NOT implement features, flags, or extension points for hypothetical future use.
- MUST NOT add configuration options that no current caller uses.
- MUST NOT generalize a function until the third real use case exists (see DRY § 6.7).

### 13.3 Fail Fast

- MUST validate all external input at the entry point (arquivo, entrada de usuario).
- MUST NOT silently coerce invalid input into a valid-looking value.
- MUST crash or return error immediately when an invariant is violated: never defer.
- MUST include the violated condition and the actual value in the error message.

### 13.4 Law of Demeter  -  Principle of Least Knowledge

**The "one dot" rule:** `a.fazAlgo()` is fine. `a.getB().getC().fazAlgo()` is a violation.

- MUST NOT chain more than one method/property access on a foreign object.
- SHOULD expose behavior, not structure (Tell, Don't Ask).

### 13.5 CQS  -  Command-Query Separation

- Commands MUST return `void` (or `Result`/`Error` for success/failure only).
- Queries MUST be pure: same input -> same output, no side effects.
- MUST NOT have a function that returns meaningful data AND produces a side effect.

### 13.6 Composition over Inheritance

- MUST NOT create inheritance hierarchies deeper than 2 levels.
- MUST NOT use inheritance to share implementation: use composition or free functions.

### 13.7 Immutability by Default

- MUST declare variables as immutable (`const`, `const&`) by default.
- MUST NOT mutate function parameters.
- SHOULD return new values instead of modifying existing ones in domain logic.

### 13.8 Explicit over Implicit

- MUST NOT rely on global mutable state or thread-local singletons silently affecting behavior.
- MUST pass dependencies explicitly (constructor/function parameters), not via globals.

### 13.9 High Cohesion, Low Coupling

- MUST NOT place logic in a module because it is convenient, only because it belongs.
- A module MUST be testable in isolation without instantiating the full system (ver TESTES.md T16, testabilidade sem janela).
- Circular dependencies between modules MUST NOT exist.

### 13.10 Idempotency

- MUST design write operations (gravar mapa, gravar histórico) to be idempotent: gravar o mesmo estado duas vezes produz o mesmo arquivo, byte a byte (ver TESTES.md T14).
- MUST NOT accumulate state on repeated calls (ex.: aplicar o mesmo comando duas vezes sem querer não deve duplicar o efeito na pilha).
- MUST test the "salvar duas vezes" scenario para o arquivo de mapa e para o de histórico.

### 13.11 Tell, Don't Ask

- MUST NOT extract state from an object, compute a decision outside, then push the result back in.
- MUST place the decision inside the object that owns the relevant data.
- SHOULD expose behavior-revealing methods (`aplicar()`, `desfazer()`) over state-revealing getters.

### 13.12 POLA  -  Principle of Least Astonishment

- MUST NOT perform side effects that the name does not indicate (`buscar*` MUST NOT write; `calcular*` MUST NOT mutate).
- MUST NOT return a different type or shape depending on a hidden flag or global state.
- MUST NOT silently ignore parameters: if a parameter is accepted, it MUST affect behavior.

---

## 14. Fora de Escopo  -  o que foi removido e por que

Este contrato e uma poda da versão genérica do vault para um editor de mapa desktop, local, de usuario único, sem rede, sem banco de dados, escrito em C++23 sem Qt sobre o GlintFx. Foram removidas por completo, por não se aplicarem: regras especificas de Qt/widgets, acessibilidade de navegador, OWASP Top 10 e SQL injection, API Design REST, Logging estruturado/observability de servidor, e LGPD (não há dado pessoal processado). O detalhe do que saiu de cada secao, e por que, está no relatório de poda do tech-lead (histórico de sessão/commit desta mudança), não duplicado aqui para não desatualizar em silencio.

---
*This contract is the authoritative reference for all code written in this project, subordinado a [`GODS_LAWS.md`](GODS_LAWS.md).*
