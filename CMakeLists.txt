cmake_minimum_required(VERSION 3.15)
project(uutils_hash)

set(CMAKE_CXX_STANDARD 17)

# read from env BINSTALL_DIR, otherwise use bin_install
if(DEFINED ENV{BINSTALL_DIR})
    set(CUSTOM_INSTALL_PREFIX $ENV{BINSTALL_DIR} CACHE PATH "Custom installation prefix")
else()
    set(CUSTOM_INSTALL_PREFIX "./bin_install" CACHE PATH "Custom installation prefix")
    message(WARNING "Environment variable BINSTALL_DIR not set, using default path: ${CUSTOM_INSTALL_PREFIX}")
endif()

list(APPEND CMAKE_PREFIX_PATH "${CUSTOM_INSTALL_PREFIX}")
list(APPEND CMAKE_LIBRARY_PATH "${CUSTOM_INSTALL_PREFIX}/lib")
list(APPEND CMAKE_INCLUDE_PATH "${CUSTOM_INSTALL_PREFIX}/include")

find_package(pybind11 REQUIRED)

include(UUtils/cmake/xxhash.cmake)
include(UUtils/cmake/stdcpp.cmake)
include(UUtils/cmake/sanitizer.cmake)
# include(UUtils/cmake/boost.cmake)

pybind11_add_module(_c_uutils_hash_compute pyuutils/hash/_c_uutils_hash_compute.cpp)
target_link_libraries(_c_uutils_hash_compute PRIVATE xxHash)
target_include_directories(_c_uutils_hash_compute PRIVATE
    ${CMAKE_CURRENT_SOURCE_DIR}
    ${CUSTOM_INSTALL_PREFIX}/include
)

install(TARGETS _c_uutils_hash_compute DESTINATION pyuutils/hash)

# 设置 rpath 以便在运行时能找到自定义安装路径中的库
if(APPLE)
    set(CMAKE_INSTALL_RPATH "@loader_path;@loader_path/../../lib;${CUSTOM_INSTALL_PREFIX}/lib")
elseif(UNIX)
    set(CMAKE_INSTALL_RPATH "$ORIGIN:$ORIGIN/../../lib:${CUSTOM_INSTALL_PREFIX}/lib")
endif()
set(CMAKE_INSTALL_RPATH_USE_LINK_PATH TRUE)
