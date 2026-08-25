// SPDX-License-Identifier: AGPL-3.0-or-later
#pragma once

#include <concepts>
#include <format>
#include <string>
#include <string_view>

// check.hpp - non-fatal and fatal-to-the-case assertions of gusmap's
// own harness (COR-1, GODS_LAWS.md L-09: no Catch2/GoogleTest).
//
// GUSMAP_CHECK does NOT abort the case on failure (unlike assert): the
// case continues, and the failure is counted. harness_main decides
// PASS/FAIL from that count at the end of the case (mirrors GlintFx's
// GLINTFX_CHECK exactly).
//
// GUSMAP_REQUIRE DOES abort the case (D1, desenho-cor1.md §3.3): a
// failed REQUIRE records the failure exactly like CHECK and then
// RETURNS from the enclosing function. This only works correctly in
// the TOP-LEVEL body of a GUSMAP_TEST case -- see the macro docstring
// below.
//
// GUSMAP_CHECK_EQ prints BOTH operand values, not just the source
// expression (D2, desenho-cor1.md §3.3): when both operands are
// std::formattable, the failure line carries "lhs=... rhs=...";
// otherwise it falls back to GlintFx's plain "expr" form.

namespace gusmap::test {

void record_check_failure(std::string_view file, int line, std::string_view expr);
void record_check_failure_with_values(std::string_view file, int line, std::string_view expr_a,
                                       std::string_view expr_b, const std::string& lhs,
                                       const std::string& rhs);
[[nodiscard]] int failure_count();
void reset_failure_count();

// Internal to the harness -- used ONLY by prop.cpp's shrinker
// (run_property, desenho-cor1.md §4.2 + the shrinking the leader
// added on 24/08/2026) to probe candidate shrinks without flooding
// stderr with the search's own intermediate attempts. A test body must
// never call this: it does not change PASS/FAIL, only whether a given
// CHECK/CHECK_EQ/REQUIRE failure is printed the instant it happens.
void set_checks_muted(bool muted);

template <typename A, typename B>
void check_eq(const A& a, const B& b, std::string_view file, int line, std::string_view expr_a,
              std::string_view expr_b) {
    if (a == b) {
        return;
    }
    if constexpr (std::formattable<A, char> && std::formattable<B, char>) {
        record_check_failure_with_values(file, line, expr_a, expr_b, std::format("{}", a),
                                          std::format("{}", b));
    } else {
        record_check_failure(file, line, std::string(expr_a) + " == " + std::string(expr_b));
    }
}

} // namespace gusmap::test

#define GUSMAP_CHECK(cond)                                                                        \
    do {                                                                                          \
        if (!(cond)) {                                                                            \
            ::gusmap::test::record_check_failure(__FILE__, __LINE__, #cond);                      \
        }                                                                                          \
    } while (false)

#define GUSMAP_CHECK_EQ(a, b) ::gusmap::test::check_eq((a), (b), __FILE__, __LINE__, #a, #b)

// GUSMAP_REQUIRE(cond) - fatal-to-the-case assertion (D1).
//
// LIMITATION, documented on purpose (desenho-cor1.md §3.3): this only
// works in the top-level body of a GUSMAP_TEST case. Used inside a
// lambda or a helper function, the `return` below returns from THAT
// lambda/helper, not from the test case -- a helper that needs a
// precondition guard must use GUSMAP_CHECK and return a bool of its
// own instead.
#define GUSMAP_REQUIRE(cond)                                                                      \
    do {                                                                                          \
        if (!(cond)) {                                                                            \
            ::gusmap::test::record_check_failure(__FILE__, __LINE__, #cond);                      \
            return;                                                                               \
        }                                                                                          \
    } while (false)
