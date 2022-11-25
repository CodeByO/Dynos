cmake_minimum_required(VERSION 3.9)
project(exploitDll)
include (GenerateExportHeader)
set(CMAKE_CXX_STANDARD 17)

add_library(exploitDll MODULE SHARED dll.cpp)
set_target_properties(exploitDll PROPERTIES COMPILE_FLAGS "-m32" LINK_FLAGS "-m32")
GENERATE_EXPORT_HEADER(exploitDll
    BASE_NAME exploitDll
    EXPORT_MACRO_NAME exploitDll_EXPORT
    EXPORT_FILE_NAME exploitDll_Export.h
    STATIC_DEFINE exploitDll_BUILT_AS_STATIC)