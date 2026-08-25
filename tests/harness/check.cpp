// SPDX-License-Identifier: AGPL-3.0-or-later
#include "check.hpp"

#include <print>

namespace gusmap::test {

namespace {

int g_failure_count = 0;
bool g_checks_muted = false;

} // namespace

void record_check_failure(std::string_view file, int line, std::string_view expr) {
    if (!g_checks_muted) {
        std::println(stderr, "{}:{}: failed: {}", file, line, expr);
    }
    ++g_failure_count;
}

void record_check_failure_with_values(std::string_view file, int line, std::string_view expr_a,
                                       std::string_view expr_b, const std::string& lhs,
                                       const std::string& rhs) {
    if (!g_checks_muted) {
        std::println(stderr, R"({}:{}: failed: {} == {} | lhs="{}" rhs="{}")", file, line, expr_a,
                      expr_b, lhs, rhs);
    }
    ++g_failure_count;
}

int failure_count() { return g_failure_count; }

void reset_failure_count() { g_failure_count = 0; }

void set_checks_muted(bool muted) { g_checks_muted = muted; }

} // namespace gusmap::test
