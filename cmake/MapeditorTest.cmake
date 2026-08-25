# SPDX-License-Identifier: AGPL-3.0-or-later
#
# MapeditorTest.cmake
#
# Single subject: the default CTest timeout and the function that
# registers a test executable linked against gusworld_mapeditor's own
# harness (GODS_LAWS.md L-09: no Catch2/GoogleTest, no third-party test
# framework). Mirrors GlintFx's own GlintfxTest.cmake, minus
# glintfx_copy_runtime_dlls_after_build: every layer target in this
# project today is STATIC, so there is no DLL of ours to place next to
# a test executable. The day a test links a SHARED library (GlintFx
# itself, through platform/, in shared mode), the Windows loader
# problem that omission would risk is exactly the WIN-HANG lesson
# GlintFx already documents in its own GlintfxTest.cmake -- fix it the
# same way they did, with $<TARGET_RUNTIME_DLLS:tgt>, on that day
# (desenho-cor1.md §2.4).

# WIN-HANG (GlintFx, ver o comentario identico la): tem de rodar ANTES
# de include(CTest), que le esta variavel uma unica vez, no proprio
# include, para gerar o DartConfiguration.tcl. Um teste travado custaria
# senao o default embutido do CTest (1500s) em vez de falhar em minutos.
function(mapeditor_set_default_test_timeout)
    set(DART_TESTING_TIMEOUT 120 PARENT_SCOPE)
endfunction()

# Um executavel por tests/${name}.cpp, linkado com o harness mais as
# libs de camada que o teste exercita (${ARGN}). O harness em si nao
# linka nenhuma camada.
function(mapeditor_add_test name)
    add_executable(${name} "${CMAKE_CURRENT_SOURCE_DIR}/${name}.cpp")
    target_link_libraries(${name} PRIVATE mapeditor_test_harness ${ARGN})
    mapeditor_apply_compile_options(${name})
    add_test(NAME ${name} COMMAND ${name})
endfunction()
