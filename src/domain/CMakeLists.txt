# SPDX-License-Identifier: AGPL-3.0-or-later
#
# src/domain/CMakeLists.txt
#
# Domain layer (GODS_LAWS.md L-12): pure POCO, zero GlintFx, zero OS,
# zero third party. Single subject: the sources of this layer; the
# mapeditor_domain target's properties (include dirs, compile options,
# compile definitions) live in the parent src/CMakeLists.txt.

target_sources(mapeditor_domain PRIVATE version.cpp)
