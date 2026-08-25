# SPDX-License-Identifier: AGPL-3.0-or-later
#
# CMakeLists.txt - root of gusworld_mapeditor (COR-1).
#
# Single subject: orchestrates the modules in cmake/, the layer targets
# in src/ and the test suite in tests/. No detail of compile option,
# warning flag or test registration belongs here; each one has its own
# module in cmake/ -- mirrors GlintFx's own root CMakeLists.txt style
# (desenho-cor1.md §2.1).

cmake_minimum_required(VERSION 3.28)

project(gusworld_mapeditor VERSION 0.1.0 LANGUAGES CXX)

# PROJECT_SOURCE_DIR, not CMAKE_SOURCE_DIR: keeps this module path
# correct even if this project is ever embedded by another one (same
# reasoning GlintFx documents at the identical line in its own root
# CMakeLists.txt).
list(APPEND CMAKE_MODULE_PATH "${PROJECT_SOURCE_DIR}/cmake")
include(MapeditorCompileOptions)

add_subdirectory(src)

# A costura com o GlintFx fica DOCUMENTADA aqui, nao implementada
# (desenho-cor1.md §2.1: "nenhuma opcao morta, nenhum if especulativo").
# No dia em que src/platform/ nascer -- bloqueado ate a API publica de
# janela/desenho do GlintFx existir, GODS_LAWS.md L-01 -- o padrao e:
#
#   find_package(glintfx CONFIG REQUIRED)
#   target_link_libraries(mapeditor_platform PRIVATE glintfx::glintfx)
#
# Ate la, este projeto configura, compila e testa nos cinco alvos do CI
# (GODS_LAWS.md L-10) sem uma unica linha de GlintFx.

# MapeditorTest ANTES de include(CTest) -- licao WIN-HANG do GlintFx:
# aquele modulo le DART_TESTING_TIMEOUT uma unica vez, no include, para
# gerar o DartConfiguration.tcl; feito depois, o timeout default do
# CTest (1500s) fica valendo para qualquer teste que nao declare o
# proprio TIMEOUT.
include(MapeditorTest)
mapeditor_set_default_test_timeout()
include(CTest)
add_subdirectory(tests)
