# SPDX-License-Identifier: AGPL-3.0-or-later
#
# src/CMakeLists.txt
#
# Single subject: the layer libraries and the include root they share.
# domain/ is the first layer (GODS_LAWS.md L-12: horizontal layers,
# dependency pointing only inward); application/ and platform/ are
# born, each with its own add_subdirectory() entry here, only on the
# day their first real .cpp lands (GODS_LAWS.md L-09: an empty layer
# directory arms the CI layer gate's trap with nothing to scan).

add_library(mapeditor_domain STATIC)
add_library(mapeditor::domain ALIAS mapeditor_domain)
target_include_directories(mapeditor_domain PUBLIC "${PROJECT_SOURCE_DIR}/src")

# PUBLIC: domain_version_test.cpp (tests/CMakeLists.txt) links against
# mapeditor::domain and compares mapeditor::domain::version() against
# these SAME macros, so it needs to see them too. This is the entire
# "costura" with CMake's own PROJECT_VERSION -- no generated header,
# unlike GlintFx's version_macros.hpp: that machinery exists there for
# an INSTALLED, externally-consumed library (GODS_LAWS.md desenho-cor1.md
# §2.1 already ruled installation/export out for this project).
target_compile_definitions(mapeditor_domain PUBLIC
    MAPEDITOR_VERSION_MAJOR=${PROJECT_VERSION_MAJOR}
    MAPEDITOR_VERSION_MINOR=${PROJECT_VERSION_MINOR}
    MAPEDITOR_VERSION_PATCH=${PROJECT_VERSION_PATCH}
    MAPEDITOR_VERSION_STRING="${PROJECT_VERSION}"
)

mapeditor_apply_compile_options(mapeditor_domain)

add_subdirectory(domain)
