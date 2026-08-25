// SPDX-License-Identifier: AGPL-3.0-or-later
#include <print>
#include <string_view>

#include "check.hpp"
#include "test_registry.hpp"

// harness_main.cpp - entry point of gusmap's own harness (COR-1).
//
// With no argument: runs every registered case, in registration order
// (link order -- no sort, no shuffle). With "--list": only prints the
// names. With an exact name: runs only that case, and FAILS if the
// name does not exist (never silently ignored).
//
// Contrato de saida (desenho-cor1.md §3.4, porta de mao unica):
//   stdout: "[PASS|FAIL] nome" por caso, sumario final
//           "--- N case(s), M failure(s) ---".
//   stderr: uma linha por asercao falhada (arquivo:linha: ...) e erros
//           do proprio harness.
//   exit:   0 so quando todo caso executado passou; 1 para qualquer
//           falha ou nome inexistente.

namespace {

using gusmap::test::Case;

void print_case_list() {
    for (const Case& c : gusmap::test::all_cases()) {
        std::println("{}", c.name);
    }
}

bool run_single_case(const Case& c) {
    gusmap::test::reset_failure_count();
    c.fn();
    const bool passed = gusmap::test::failure_count() == 0;
    std::println("[{}] {}", passed ? "PASS" : "FAIL", c.name);
    return passed;
}

const Case* find_case_by_name(std::string_view name) {
    for (const Case& c : gusmap::test::all_cases()) {
        if (c.name == name) {
            return &c;
        }
    }
    return nullptr;
}

int run_all_cases() {
    int failures = 0;
    for (const Case& c : gusmap::test::all_cases()) {
        if (!run_single_case(c)) {
            ++failures;
        }
    }
    return failures;
}

int run_named_case(std::string_view name) {
    const Case* c = find_case_by_name(name);
    if (c == nullptr) {
        std::println(stderr, "harness: no test case named \"{}\"", name);
        return 1;
    }
    return run_single_case(*c) ? 0 : 1;
}

void print_summary(std::size_t total, int failures) {
    std::println("--- {} case(s), {} failure(s) ---", total, failures);
}

} // namespace

// NOLINTNEXTLINE(bugprone-exception-escape) reason: every format string
// this harness ever prints is a string literal, validated at COMPILE
// time by std::println's consteval format-string check (P2216); there
// is no runtime input that could make it throw (same reasoning
// GlintFx's own harness_main.cpp documents at this exact line).
int main(int argc, char** argv) {
    if (argc == 2 && std::string_view{argv[1]} == "--list") {
        print_case_list();
        return 0;
    }

    if (argc == 2) {
        return run_named_case(argv[1]);
    }

    const int failures = run_all_cases();
    print_summary(gusmap::test::all_cases().size(), failures);
    return failures == 0 ? 0 : 1;
}
