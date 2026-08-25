# SPDX-License-Identifier: AGPL-3.0-or-later
#
# MapeditorCompileOptions.cmake
#
# Single subject: the C++23 language standard and the warning flags
# applied to every gusworld_mapeditor target (layer library, test
# harness or test executable). Mirrors GlintFx's own
# GlintfxCompileOptions.cmake, minus the sanitizer flags -- COR-1 does
# not need them; a later slice adds glintfx_apply_sanitizer_flags's
# equivalent the day it does (desenho-cor1.md §2.2).

# Default OFF: a compiler upgrade that starts emitting a brand-new
# warning must not break the leader's own local build out of nowhere.
# Turned ON in CI only (desenho-cor1.md §2.5), where warning-as-error is
# exactly the point.
option(MAPEDITOR_WERROR "Tratar warning como erro" OFF)

function(mapeditor_apply_cxx_standard target)
    set_target_properties(${target} PROPERTIES
        CXX_STANDARD 23
        CXX_STANDARD_REQUIRED ON
        CXX_EXTENSIONS OFF
    )
endfunction()

function(mapeditor_apply_warning_flags target)
    target_compile_options(${target} PRIVATE
        $<$<CXX_COMPILER_ID:GNU,Clang>:-Wall;-Wextra;-Wpedantic>
        $<$<CXX_COMPILER_ID:MSVC>:/W4>
    )
    if(MAPEDITOR_WERROR)
        target_compile_options(${target} PRIVATE
            $<$<CXX_COMPILER_ID:GNU,Clang>:-Werror>
            $<$<CXX_COMPILER_ID:MSVC>:/WX>
        )
    endif()
endfunction()

# Single entry point that the target files (src/CMakeLists.txt,
# tests/CMakeLists.txt, MapeditorTest.cmake) call. Composition of the
# two functions above, with no logic of its own.
function(mapeditor_apply_compile_options target)
    mapeditor_apply_cxx_standard(${target})
    mapeditor_apply_warning_flags(${target})
endfunction()
