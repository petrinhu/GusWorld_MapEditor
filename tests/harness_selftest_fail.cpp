// SPDX-License-Identifier: AGPL-3.0-or-later
#include "harness/check.hpp"
#include "harness/test_registry.hpp"

// harness_selftest_fail.cpp - deliberately-failing executable that
// proves the harness itself reproves a real failure, on all five CI
// targets (desenho-cor1.md §5, item 2). Registered in tests/CMakeLists.txt
// with WILL_FAIL TRUE: ctest reads this executable's exit 1 as the
// EXPECTED outcome and reports it green -- if this binary ever exited
// 0, THAT is what would turn ctest red here.

namespace {
// Written to by a_require_returns_early, read by
// b_require_proves_early_return -- registration order is execution
// order (test_registry: no sort, no shuffle), so "b" always runs
// after "a" inside this single process. This is the only way to
// OBSERVE, from outside the function, whether GUSMAP_REQUIRE's early
// `return` actually happened: nothing after the return in "a" can
// check its own non-execution from the inside.
bool g_reached_after_require = false;
} // namespace

GUSMAP_TEST(plain_check_fails) {
    // Non-fatal: this line runs, is counted as a failure, and the case
    // continues -- unlike GUSMAP_REQUIRE below.
    GUSMAP_CHECK(false);
}

GUSMAP_TEST(a_require_returns_early) {
    GUSMAP_REQUIRE(false); // records the failure and returns HERE.
    g_reached_after_require = true; // must NEVER execute.
}

GUSMAP_TEST(b_require_proves_early_return) {
    // If GUSMAP_REQUIRE in "a" had NOT returned early, this would be
    // true here, and this CHECK would (correctly) fail too. Because
    // this is a WILL_FAIL executable, that outcome would still show
    // green in ctest -- which is exactly why the adversarial audit
    // (desenho-cor1.md §6, passo 3) has to invert GUSMAP_REQUIRE's own
    // return statement on a copy of the source and watch THIS specific
    // case start failing, to prove the guard is doing its job.
    GUSMAP_CHECK(!g_reached_after_require);
}
