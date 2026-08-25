// SPDX-License-Identifier: AGPL-3.0-or-later
#include "domain/version.hpp"

// MAPEDITOR_VERSION_* are compile definitions propagated from CMake's
// project(gusworld_mapeditor VERSION ...) call, PUBLIC on the
// mapeditor_domain target (src/CMakeLists.txt) so that
// domain_version_test.cpp, which links against mapeditor::domain, sees
// the exact same macros it compares against.

namespace mapeditor::domain {

namespace {
constexpr std::string_view kVersionString = MAPEDITOR_VERSION_STRING;
} // namespace

Version version() noexcept {
    return Version{
        .major_version = static_cast<std::uint32_t>(MAPEDITOR_VERSION_MAJOR),
        .minor_version = static_cast<std::uint32_t>(MAPEDITOR_VERSION_MINOR),
        .patch_version = static_cast<std::uint32_t>(MAPEDITOR_VERSION_PATCH),
    };
}

std::string_view version_string() noexcept { return kVersionString; }

} // namespace mapeditor::domain
