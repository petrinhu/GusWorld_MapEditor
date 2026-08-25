# SPDX-License-Identifier: AGPL-3.0-or-later
#
# tests/CMakeLists.txt
#
# Single subject: the harness library and the test executables linked
# against it. mapeditor_add_test() (cmake/MapeditorTest.cmake) creates
# one executable per tests/${name}.cpp.
#
# Tests live FLAT here (tests/*.cpp, prefixed by the layer they
# exercise, e.g. domain_*_test.cpp), never in a tests/domain/
# subdirectory -- desenho-cor1.md §1: a directory literally named
# "domain"/"application"/"platform" anywhere in the tree arms the CI
# layer gate (GODS_LAWS.md L-09/L-12), and this keeps `tests/` itself
# out of that trap while still reading a `"harness/check.hpp"` include
# that check_allowed_includes.py resolves cleanly against this very
# directory.

add_library(mapeditor_test_harness STATIC
    harness/test_registry.cpp
    harness/check.cpp
    harness/prop.cpp
    harness/harness_main.cpp
)
target_include_directories(mapeditor_test_harness PUBLIC "${CMAKE_CURRENT_SOURCE_DIR}")
mapeditor_apply_compile_options(mapeditor_test_harness)

# harness_selftest_fail.cpp - proves that failure REPROVES for real, on
# all five CI targets (desenho-cor1.md §5, item 2): a harness that only
# demonstrates the green path has proven nothing (GODS_LAWS.md L-09).
# WILL_FAIL inverts ctest's own pass/fail reading of this executable's
# exit code, so THIS test shows green in `ctest` output precisely
# because the binary exits 1.
mapeditor_add_test(harness_selftest_fail)
set_tests_properties(harness_selftest_fail PROPERTIES WILL_FAIL TRUE)

# prop_determinism_test.cpp - golden values (KAT) of the Rng generator:
# proves bit-for-bit identity of the SAME seed's output across all five
# CI targets (desenho-cor1.md §5, item 3) -- the reproducibility that
# GODS_LAWS.md L-09's property-test decision depends on stops being a
# promise and becomes a gate the instant this test is green on all five.
mapeditor_add_test(prop_determinism_test)

# domain_version_test.cpp - proves the domain layer (GODS_LAWS.md L-12)
# compiles and links against the harness (desenho-cor1.md §5, item 1).
# This is the test that arms the CI layer gate's trap the moment
# src/domain/ exists (GODS_LAWS.md L-09).
mapeditor_add_test(domain_version_test mapeditor::domain)
