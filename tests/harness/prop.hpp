// SPDX-License-Identifier: AGPL-3.0-or-later
#pragma once

#include <cstdint>
#include <functional>
#include <string_view>
#include <utility>
#include <vector>

// prop.hpp - deterministic property-based testing module of gusmap's
// own harness (D3, desenho-cor1.md §4; GODS_LAWS.md L-09).
//
// No third-party library (RapidCheck, libFuzzer, ...): L-01 forbids
// it, and the leader confirmed on 24/08/2026 that an in-house generator
// written from a published algorithm is our own code, not a
// dependency. std::mt19937 was rejected on purpose: the C++ standard
// specifies the ENGINE but not the DISTRIBUTIONS, so
// std::uniform_int_distribution et al. can (and do) produce different
// sequences from the same seed across libstdc++ and MSVC STL --
// exactly the cross-platform reproducibility this project's five CI
// targets (GODS_LAWS.md L-10) depend on. Rng below is splitmix64
// (Sebastiano Vigna, public-domain algorithm) plus samplers written by
// hand from plain unsigned 64-bit arithmetic, with no UB and no
// standard-library distribution anywhere in the path -- bit-identical
// on every platform by construction. prop_determinism_test.cpp is the
// portao that actually proves this, not just asserts it.

namespace gusmap::test {

// Rng - deterministic, seedable pseudo-random source.
//
// PROIBIDO no harness inteiro (GODS_LAWS.md L-09): semente de relogio,
// std::random_device, endereco de memoria, qualquer entropia
// ambiente. Toda semente e um literal escrito no teste. Determinismo
// nao e um modo, e a UNICA opcao -- por isso Rng nao tem nenhum
// construtor que nao receba uma semente explicita.
class Rng {
public:
    explicit Rng(std::uint64_t seed) noexcept;

    // Raw 64-bit draw (splitmix64 step). Every other method below
    // routes through this one -- run_property's shrinker (prop.cpp)
    // relies on that to record/replay an iteration's ENTIRE decision
    // history from this single primitive.
    [[nodiscard]] std::uint64_t next_u64();

    // Unbiased in [0, n) by rejection, n > 0. Never `% n` alone: that
    // biases toward the low end whenever n does not divide 2^64 evenly.
    [[nodiscard]] std::uint64_t below(std::uint64_t n);

    // Inclusive [lo, hi].
    [[nodiscard]] std::int64_t int_in(std::int64_t lo, std::int64_t hi);

    [[nodiscard]] bool next_bool();

    // [0.0, 1.0), built from the top 53 bits of next_u64() -- never
    // from a <random> distribution, same cross-platform reason as
    // below().
    [[nodiscard]] double unit_double();

    // Internal to the harness -- used ONLY by run_property's shrinker
    // (prop.cpp). `recording` appends every raw draw this Rng makes
    // into `tape` (owned by the caller, must outlive the Rng);
    // `replaying` returns the values in `tape`, in order, instead of
    // computing splitmix64, and returns a fixed 0 for any draw once
    // the tape is exhausted (an iteration is allowed to draw a
    // variable number of values -- e.g. "how many vertices, then that
    // many coordinates" -- and a SHRUNK tape can legitimately run out
    // mid-body).
    //
    // Deliberately 0, NOT a continuation of any splitmix64 stream: a
    // splitmix64 continuation only depends on HOW MANY draws happened
    // before it, never on what their VALUES were, so it would
    // regenerate the exact bit-for-bit values a truncated suffix of
    // the tape was supposed to remove -- making "drop the trailing
    // draws" a no-op disguised as a successful shrink (measured while
    // building this module: it collapsed a 25-draw failure down to a
    // reported "0 draws" that silently reproduced the original
    // sequence in full). A fixed 0 is also consistent with the OTHER
    // shrink pass (prop.cpp's shrink_tape): both push every draw
    // toward the simplest possible value, zero, instead of toward an
    // arbitrary "different" one. A test body never constructs either
    // of these directly.
    [[nodiscard]] static Rng recording(std::uint64_t seed, std::vector<std::uint64_t>& tape);
    [[nodiscard]] static Rng replaying(const std::vector<std::uint64_t>& tape);

private:
    Rng(std::uint64_t state, std::vector<std::uint64_t>* record_into,
        const std::vector<std::uint64_t>* replay_from) noexcept;

    std::uint64_t state_;
    std::vector<std::uint64_t>* record_into_;
    const std::vector<std::uint64_t>* replay_from_;
    std::size_t replay_pos_ = 0;
};

// run_property_impl - non-template engine (prop.cpp). run_property
// below just type-erases `body` into this; kept non-template so the
// iteration loop and the shrink search are compiled ONCE, not once per
// F instantiation of run_property.
void run_property_impl(std::string_view prop_name, std::uint64_t seed, int iterations,
                        const std::function<void(Rng&, int)>& body);

// run_property - runs `body` for `iterations` deterministic draws of a
// property (desenho-cor1.md §4.2).
//
// For i in [0, iterations): builds an Rng derived from (seed, i) --
// so any single iteration is reproducible in isolation, knowing only
// (seed, i) -- and calls body(rng, i). The asserções dentro do body sao
// os mesmos GUSMAP_CHECK*/GUSMAP_REQUIRE de sempre; o runner nao
// inventa asercao propria.
//
// The FIRST iteration that fails stops the loop (one failing iteration
// already disproves the property) and, before reporting it, SHRINKS
// the sequence of raw draws that iteration made to a smaller one that
// still reproduces the failure (added by order of the leader on
// 24/08/2026 -- desenho-cor1.md §4.2 originally declared this a
// downgrade; the líder decided it enters this slice, not later).
// Shrinking here is generic delta-debugging over the recorded draw
// tape: it never needs to know what a "polygon" or a "byte buffer" IS,
// only whether replaying a smaller/smaller-valued tape through the
// SAME body still fails. It is a bounded, best-effort local reduction
// (prop.cpp documents the exact bound), not a promise of the globally
// smallest possible counterexample.
template <typename F>
void run_property(std::string_view prop_name, std::uint64_t seed, int iterations, F&& body) {
    run_property_impl(prop_name, seed, iterations,
                       std::function<void(Rng&, int)>(std::forward<F>(body)));
}

} // namespace gusmap::test
