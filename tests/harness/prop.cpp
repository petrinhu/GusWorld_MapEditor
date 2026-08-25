// SPDX-License-Identifier: AGPL-3.0-or-later
#include "prop.hpp"

#include "check.hpp"

#include <cstdint>
#include <cstdio>
#include <print>

namespace gusmap::test {

namespace {

// splitmix64 (Sebastiano Vigna, http://prng.di.unimi.it/splitmix64.c,
// public domain). ~6 lines of unsigned 64-bit arithmetic, no UB, no
// standard-library distribution -- the whole reason this project wrote
// its own generator instead of <random> (see prop.hpp's module
// docstring). kWeyl is Vigna's own golden-ratio Weyl increment.
constexpr std::uint64_t kWeyl = 0x9E3779B97F4A7C15ULL;

std::uint64_t splitmix64_step(std::uint64_t& state) {
    state += kWeyl;
    std::uint64_t z = state;
    z = (z ^ (z >> 30)) * 0xBF58476D1CE4E5B9ULL;
    z = (z ^ (z >> 27)) * 0x94D049BB133111EBULL;
    return z ^ (z >> 31);
}

// Derives an independent per-iteration seed from (seed, iteration):
// one splitmix64 step over `seed + kWeyl * iteration` (desenho-cor1.md
// §4.2: "mix = splitmix64 sobre (seed, i), K = constante dourada de
// Weyl do proprio splitmix64"). This is what lets ANY single iteration
// be reproduced in isolation from just (seed, i), without replaying
// every earlier iteration first.
std::uint64_t derive_iteration_seed(std::uint64_t seed, int iteration) {
    std::uint64_t state = seed + kWeyl * static_cast<std::uint64_t>(iteration);
    return splitmix64_step(state);
}

} // namespace

Rng::Rng(std::uint64_t seed) noexcept : state_(seed), record_into_(nullptr), replay_from_(nullptr) {}

Rng::Rng(std::uint64_t state, std::vector<std::uint64_t>* record_into,
         const std::vector<std::uint64_t>* replay_from) noexcept
    : state_(state), record_into_(record_into), replay_from_(replay_from) {}

Rng Rng::recording(std::uint64_t seed, std::vector<std::uint64_t>& tape) {
    return Rng{seed, &tape, nullptr};
}

Rng Rng::replaying(const std::vector<std::uint64_t>& tape) { return Rng{0, nullptr, &tape}; }

std::uint64_t Rng::next_u64() {
    std::uint64_t value;
    if (replay_from_ != nullptr) {
        // Replaying: read the candidate tape while it lasts, then a
        // fixed 0 forever -- see prop.hpp's docstring on replaying()
        // for why this is 0 and not a continued splitmix64 stream.
        value = (replay_pos_ < replay_from_->size()) ? (*replay_from_)[replay_pos_] : 0;
        ++replay_pos_;
    } else {
        value = splitmix64_step(state_);
    }
    if (record_into_ != nullptr) {
        record_into_->push_back(value);
    }
    return value;
}

std::uint64_t Rng::below(std::uint64_t n) {
    if (n == 0) {
        // Defensive: a generator asking for below(0) has a bug of its
        // OWN, not the Rng's -- there is no valid value to return, and
        // this module never throws across a test body (GUSMAP_CHECK*
        // is how a test reports a problem, not an exception).
        return 0;
    }
    // UINT64_MAX from <cstdint>, not std::numeric_limits<uint64_t>::max()
    // from <limits>: tools/ci/check_allowed_includes.py's STD_HEADERS
    // allowlist (GODS_LAWS.md L-01, existing tool, out of this slice's
    // scope to touch) lists <climits> (the C header) but not the
    // separate C++ <limits> header -- a real gap in that allowlist,
    // flagged to the main/CTO rather than patched here. <cstdint> is
    // already required by this module and covers the same constant.
    constexpr std::uint64_t kMax = UINT64_MAX;
    const std::uint64_t limit = kMax - (kMax % n);
    std::uint64_t r;
    do {
        r = next_u64();
    } while (r >= limit);
    return r % n;
}

std::int64_t Rng::int_in(std::int64_t lo, std::int64_t hi) {
    const std::uint64_t span = static_cast<std::uint64_t>(hi - lo) + 1;
    return lo + static_cast<std::int64_t>(below(span));
}

bool Rng::next_bool() { return (next_u64() & 1U) != 0; }

double Rng::unit_double() { return static_cast<double>(next_u64() >> 11) * 0x1.0p-53; }

namespace {

// Bounded search budget for the shrinker below: declared, not a
// promise of a globally minimal counterexample (GODS_LAWS.md L-09: no
// silent caps -- the budget is a named constant, and run_property_impl
// prints how many probes it actually spent).
constexpr int kMaxShrinkProbes = 2000;

// Replays `tape` through `body` and reports whether THIS replay fails
// (failure_count() increases), without printing the individual
// CHECK/CHECK_EQ line the replay may trigger -- only the FINAL, already
// -minimized replay in run_property_impl prints for real. Consumes one
// unit of `probes_left`; returns false once the budget is spent, which
// simply stops the shrinker from finding further reductions (the tape
// found so far is still a valid, if not maximally shrunk, reproduction).
bool probe(const std::function<void(Rng&, int)>& body, const std::vector<std::uint64_t>& tape,
           int iteration, int& probes_left) {
    if (probes_left <= 0) {
        return false;
    }
    --probes_left;
    set_checks_muted(true);
    const int before = failure_count();
    Rng replay = Rng::replaying(tape);
    body(replay, iteration);
    set_checks_muted(false);
    return failure_count() > before;
}

// Generic delta-debugging shrink over the recorded draw tape: it never
// needs to know what a "polygon" or a "byte buffer" IS, only whether
// replaying a candidate tape through the SAME body still fails. Two
// passes, repeated to a fixed point (or until the probe budget runs
// out): (1) try dropping each element (largest index first, so a
// removal never invalidates the indices still to be tried); (2) try
// shrinking each remaining value toward zero by binary search. Both
// passes are property-agnostic on purpose -- writing a shrinker per
// domain generator is exactly the per-generator custom-shrinker cost
// this design avoids.
std::vector<std::uint64_t> shrink_tape(const std::function<void(Rng&, int)>& body,
                                        std::vector<std::uint64_t> tape, int iteration,
                                        int& probes_left) {
    bool improved = true;
    while (improved && probes_left > 0) {
        improved = false;

        for (std::size_t idx = tape.size(); idx-- > 0 && probes_left > 0;) {
            std::vector<std::uint64_t> candidate = tape;
            candidate.erase(candidate.begin() + static_cast<std::ptrdiff_t>(idx));
            if (probe(body, candidate, iteration, probes_left)) {
                tape = std::move(candidate);
                improved = true;
            }
        }

        for (std::size_t idx = 0; idx < tape.size() && probes_left > 0; ++idx) {
            if (tape[idx] == 0) {
                continue;
            }
            std::vector<std::uint64_t> candidate = tape;
            candidate[idx] = 0;
            if (probe(body, candidate, iteration, probes_left)) {
                tape[idx] = 0;
                improved = true;
                continue;
            }
            std::uint64_t lo = 0;
            std::uint64_t hi = tape[idx];
            while (lo + 1 < hi && probes_left > 0) {
                const std::uint64_t mid = lo + (hi - lo) / 2;
                candidate[idx] = mid;
                if (probe(body, candidate, iteration, probes_left)) {
                    hi = mid;
                } else {
                    lo = mid;
                }
            }
            if (hi < tape[idx]) {
                tape[idx] = hi;
                improved = true;
            }
        }
    }
    return tape;
}

} // namespace

void run_property_impl(std::string_view prop_name, std::uint64_t seed, int iterations,
                        const std::function<void(Rng&, int)>& body) {
    int executed = 0;

    for (int i = 0; i < iterations; ++i) {
        executed = i + 1;

        std::vector<std::uint64_t> tape;
        Rng recorder = Rng::recording(derive_iteration_seed(seed, i), tape);

        // Muted: this natural run is redone, unmuted, AFTER shrinking
        // below, so the log carries exactly one printed contra-example
        // per failing property -- the shrunk one, not this first one.
        set_checks_muted(true);
        const int before = failure_count();
        body(recorder, i);
        set_checks_muted(false);

        if (failure_count() == before) {
            continue;
        }

        int probes_left = kMaxShrinkProbes;
        const std::size_t original_draws = tape.size();
        const std::vector<std::uint64_t> shrunk = shrink_tape(body, tape, i, probes_left);

        std::println(stderr, "property \"{}\": FAIL seed={} iteration={}", prop_name, seed, i);
        std::println(stderr,
                      "property \"{}\": shrink reduziu de {} para {} draw(s) ({} probe(s) "
                      "usada(s) de {})",
                      prop_name, original_draws, shrunk.size(), kMaxShrinkProbes - probes_left,
                      kMaxShrinkProbes);

        // Unmuted, on purpose: this is the replay whose GUSMAP_CHECK/
        // GUSMAP_CHECK_EQ failure actually prints the contra-example
        // (D2 -- concrete lhs/rhs values, not just the source
        // expression) that a human reads to reproduce the bug.
        Rng final_replay = Rng::replaying(shrunk);
        body(final_replay, i);
        break;
    }

    std::println("property \"{}\": {} iteration(s) executadas", prop_name, executed);
}

} // namespace gusmap::test
