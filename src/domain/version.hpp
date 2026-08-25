// SPDX-License-Identifier: AGPL-3.0-or-later
#pragma once

#include <cstdint>
#include <string_view>

// domain/version.hpp - runtime version of the editor itself (COR-1).
//
// First POCO of the domain layer (GODS_LAWS.md L-12: pure value type,
// zero GlintFx, zero OS, zero third party). It exists to give the
// domain layer real content the moment it is born, arming the CI layer
// gate (GODS_LAWS.md L-09) with something to scan instead of an empty
// directory -- mirrors how GlintFx's own core layer was born with
// version.cpp first.
//
// Field names NOT major/minor (same reasoning GlintFx documents at the
// identical struct): on Linux, a system header pulled in transitively
// by another system header can define major/minor/makedev as
// function-like macros (sysmacros.h), which would mangle `v.major`/
// `v.minor` into a call expression in any translation unit that
// happens to include that header before this one. major_version/
// minor_version/patch_version do not collide with any known system
// macro.

namespace mapeditor::domain {

struct Version {
    std::uint32_t major_version;
    std::uint32_t minor_version;
    std::uint32_t patch_version;
};

[[nodiscard]] Version version() noexcept;
[[nodiscard]] std::string_view version_string() noexcept;

} // namespace mapeditor::domain
