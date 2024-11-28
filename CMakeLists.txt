cmake_minimum_required(VERSION 3.15)
project(uutils_hash)

set(CMAKE_CXX_STANDARD 17)

find_package(pybind11 REQUIRED)

include(UUtils/cmake/xxhash.cmake)
include(UUtils/cmake/stdcpp.cmake)
include(UUtils/cmake/sanitizer.cmake)
# include(UUtils/cmake/boost.cmake)

pybind11_add_module(_c_uutils_hash_compute pyuutils/hash/_c_uutils_hash_compute.cpp)
target_link_libraries(_c_uutils_hash_compute PRIVATE xxHash)
target_include_directories(_c_uutils_hash_compute PRIVATE ${CMAKE_CURRENT_SOURCE_DIR})

install(TARGETS _c_uutils_hash_compute DESTINATION pyuutils/hash)