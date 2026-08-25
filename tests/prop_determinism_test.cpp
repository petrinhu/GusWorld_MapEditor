// SPDX-License-Identifier: AGPL-3.0-or-later
#include <cstdint>

#include "harness/check.hpp"
#include "harness/prop.hpp"
#include "harness/test_registry.hpp"

// prop_determinism_test.cpp - golden values (KAT, known-answer-tests)
// of gusmap::test::Rng (desenho-cor1.md §5, item 3).
//
// Splitmix64 plus hand-written samplers are bit-identical across
// platforms BY CONSTRUCTION (plain unsigned 64-bit arithmetic, no UB,
// no <random> distribution -- see prop.hpp's module docstring for why
// that matters). This test is what turns that claim from a promise
// into a gate: the literals below were generated ONCE on the Fedora 44
// primary target (desenho-cor1.md §5's documented procedure, a
// throwaway main() since discarded) and are compared here bit-for-bit.
// Green on all five CI targets (GODS_LAWS.md L-10) is the actual proof
// of cross-platform reproducibility; this file alone, run on a single
// machine, only proves "did not change since it was written".

using gusmap::test::Rng;

GUSMAP_TEST(rng_next_u64_matches_golden_values_seed_a) {
    Rng r(0x1234567890ABCDEFULL);
    GUSMAP_CHECK_EQ(r.next_u64(), 0x1c948e1575796814ULL);
    GUSMAP_CHECK_EQ(r.next_u64(), 0xae9ef1ab67004bdbULL);
    GUSMAP_CHECK_EQ(r.next_u64(), 0x7a2988d31f16e86eULL);
    GUSMAP_CHECK_EQ(r.next_u64(), 0x7a5daea24eba3ba7ULL);
    GUSMAP_CHECK_EQ(r.next_u64(), 0xbb83c0c2207ad3e6ULL);
    GUSMAP_CHECK_EQ(r.next_u64(), 0xe2da71d9f0e79e32ULL);
    GUSMAP_CHECK_EQ(r.next_u64(), 0xf037b46f16a54449ULL);
    GUSMAP_CHECK_EQ(r.next_u64(), 0xafd7e49c4512ee8cULL);
}

GUSMAP_TEST(rng_next_u64_matches_golden_values_seed_b) {
    Rng r(0xDEADBEEFCAFEBABEULL);
    GUSMAP_CHECK_EQ(r.next_u64(), 0x0d7d93560d1929d2ULL);
    GUSMAP_CHECK_EQ(r.next_u64(), 0x491dfb740e50d43fULL);
    GUSMAP_CHECK_EQ(r.next_u64(), 0x42722bf4473e5e7dULL);
    GUSMAP_CHECK_EQ(r.next_u64(), 0xd6ca8a0790fffc45ULL);
    GUSMAP_CHECK_EQ(r.next_u64(), 0xb2d3ab004cdb504bULL);
    GUSMAP_CHECK_EQ(r.next_u64(), 0xb75625fc4e9510a6ULL);
    GUSMAP_CHECK_EQ(r.next_u64(), 0x099454b898764be2ULL);
    GUSMAP_CHECK_EQ(r.next_u64(), 0x796b308a7fe49981ULL);
}

GUSMAP_TEST(rng_below_matches_golden_values) {
    Rng r(0x1234567890ABCDEFULL);
    GUSMAP_CHECK_EQ(r.below(100), 76U);
    GUSMAP_CHECK_EQ(r.below(100), 11U);
    GUSMAP_CHECK_EQ(r.below(100), 70U);
    GUSMAP_CHECK_EQ(r.below(100), 91U);
    GUSMAP_CHECK_EQ(r.below(100), 34U);
}

GUSMAP_TEST(rng_int_in_matches_golden_values) {
    Rng r(0x1234567890ABCDEFULL);
    for (int i = 0; i < 5; ++i) {
        const std::int64_t v = r.int_in(-10, 10);
        GUSMAP_CHECK(v >= -10 && v <= 10);
    }
    Rng expected(0x1234567890ABCDEFULL);
    GUSMAP_CHECK_EQ(expected.int_in(-10, 10), std::int64_t{-8});
    GUSMAP_CHECK_EQ(expected.int_in(-10, 10), std::int64_t{0});
    GUSMAP_CHECK_EQ(expected.int_in(-10, 10), std::int64_t{4});
    GUSMAP_CHECK_EQ(expected.int_in(-10, 10), std::int64_t{5});
    GUSMAP_CHECK_EQ(expected.int_in(-10, 10), std::int64_t{5});
}

GUSMAP_TEST(rng_unit_double_stays_in_unit_range_and_matches_golden_values) {
    Rng r(0x1234567890ABCDEFULL);
    const double golden[5] = {
        0.11164176963709382, 0.68211279329898489, 0.47719626573879348,
        0.47799197638116986, 0.73247914065766939,
    };
    for (double expected : golden) {
        const double v = r.unit_double();
        GUSMAP_CHECK(v >= 0.0 && v < 1.0);
        GUSMAP_CHECK_EQ(v, expected);
    }
}

GUSMAP_TEST(rng_same_seed_produces_same_sequence_twice) {
    Rng a(0xABCULL);
    Rng b(0xABCULL);
    for (int i = 0; i < 20; ++i) {
        GUSMAP_CHECK_EQ(a.next_u64(), b.next_u64());
    }
}

GUSMAP_TEST(run_property_executes_exactly_n_iterations) {
    int counter = 0;
    gusmap::test::run_property("counts_iterations", 0x1u, 37, [&](Rng&, int) { ++counter; });
    GUSMAP_CHECK_EQ(counter, 37);
}

GUSMAP_TEST(run_property_derives_an_independent_rng_per_iteration) {
    // Each iteration's Rng is derived from (seed, i); two DIFFERENT
    // iterations of the same run must not draw the same first value
    // (collision would defeat the point of iterating at all -- this is
    // a smoke check, not a full statistical proof).
    std::uint64_t first_values[5] = {};
    gusmap::test::run_property("distinct_iterations", 0x77u, 5,
                                [&](Rng& rng, int i) { first_values[i] = rng.next_u64(); });
    for (int i = 0; i < 5; ++i) {
        for (int j = i + 1; j < 5; ++j) {
            GUSMAP_CHECK(first_values[i] != first_values[j]);
        }
    }
}
