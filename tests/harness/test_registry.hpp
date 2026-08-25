// SPDX-License-Identifier: AGPL-3.0-or-later
#pragma once

#include <string_view>
#include <vector>

// test_registry.hpp - test case registry of gusmap's own harness
// (COR-1, GODS_LAWS.md L-09: no Catch2/GoogleTest).
//
// Each test TU declares a case with GUSMAP_TEST(name); the macro
// creates a static object whose constructor registers it in the
// global list before main() runs (classic self-registration idiom via
// static init -- identical mechanism to GlintFx's GLINTFX_TEST).
//
// Prefix and namespace (GUSMAP_ / gusmap::test) fixed by the leader on
// 24/08/2026: Gus + map, homenagem ao Gus Dragon.

namespace gusmap::test {

struct Case {
    std::string_view name;
    void (*fn)() = nullptr;
};

void register_case(Case c);
[[nodiscard]] const std::vector<Case>& all_cases();

struct CaseRegistrar {
    CaseRegistrar(std::string_view name, void (*fn)());
};

} // namespace gusmap::test

#define GUSMAP_TEST(name)                                                                         \
    static void gusmap_test_fn_##name();                                                          \
    namespace {                                                                                   \
    const ::gusmap::test::CaseRegistrar gusmap_test_reg_##name(#name, &gusmap_test_fn_##name);    \
    }                                                                                              \
    static void gusmap_test_fn_##name()
