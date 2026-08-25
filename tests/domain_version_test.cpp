// SPDX-License-Identifier: AGPL-3.0-or-later
#include <cstdint>
#include <string>

#include "domain/version.hpp"

#include "harness/check.hpp"
#include "harness/test_registry.hpp"

// domain_version_test.cpp - proves that the domain layer compiles,
// links against the harness and runs on all five CI targets
// (desenho-cor1.md §5, item 1; mirrors GlintFx's own version_test.cpp).
// This is the commit that arms the CI layer gate's trap (GODS_LAWS.md
// L-09): domain=1+ arquivos varridos from here on.

GUSMAP_TEST(domain_version_matches_project_version) {
    const mapeditor::domain::Version v = mapeditor::domain::version();
    GUSMAP_CHECK_EQ(v.major_version, static_cast<std::uint32_t>(MAPEDITOR_VERSION_MAJOR));
    GUSMAP_CHECK_EQ(v.minor_version, static_cast<std::uint32_t>(MAPEDITOR_VERSION_MINOR));
    GUSMAP_CHECK_EQ(v.patch_version, static_cast<std::uint32_t>(MAPEDITOR_VERSION_PATCH));
}

GUSMAP_TEST(domain_version_string_matches_parts) {
    const std::string expected = std::to_string(MAPEDITOR_VERSION_MAJOR) + "." +
                                  std::to_string(MAPEDITOR_VERSION_MINOR) + "." +
                                  std::to_string(MAPEDITOR_VERSION_PATCH);
    GUSMAP_CHECK_EQ(std::string(mapeditor::domain::version_string()), expected);
}
