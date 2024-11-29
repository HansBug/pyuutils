cmake_minimum_required(VERSION 3.15)
project(uutils_hash)

set(CMAKE_CXX_STANDARD 17)

# Check if LINETRACE environment variable is set
if(DEFINED ENV{LINETRACE})
    # Add coverage flags only when LINETRACE is not empty
    if(NOT "$ENV{LINETRACE}" STREQUAL "")
        message(STATUS "Coverage analysis enabled via LINETRACE")
        set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -fprofile-arcs -ftest-coverage")
        set(CMAKE_EXE_LINKER_FLAGS "${CMAKE_EXE_LINKER_FLAGS} -fprofile-arcs -ftest-coverage")
    endif()
endif()

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

# find all libraries from uutils library
file(GLOB STATIC_LIBS "${CUSTOM_INSTALL_PREFIX}/lib/*.a" "${CUSTOM_INSTALL_PREFIX}/lib/*.lib")
set(ALL_STATIC_LIBS "")
foreach(LIB ${STATIC_LIBS})
    get_filename_component(LIB_NAME ${LIB} NAME_WE)
    add_library(${LIB_NAME} STATIC IMPORTED)
    set_target_properties(${LIB_NAME} PROPERTIES IMPORTED_LOCATION ${LIB})
    list(APPEND ALL_STATIC_LIBS ${LIB_NAME})
endforeach()

# set options
if(UNIX AND NOT APPLE)
    set(LINK_OPTIONS "-Wl,--whole-archive" ${ALL_STATIC_LIBS} "-Wl,--no-whole-archive")
elseif(APPLE)
    set(LINK_OPTIONS "-Wl,-all_load" ${ALL_STATIC_LIBS})
elseif(WIN32)
    set(LINK_OPTIONS ${ALL_STATIC_LIBS})
    # Windows need more operations
endif()
message(INFO "LINK OPTIONS: ${LINK_OPTIONS}")

include(UUtils/cmake/xxhash.cmake)
include(UUtils/cmake/stdcpp.cmake)
include(UUtils/cmake/sanitizer.cmake)
# include(UUtils/cmake/boost.cmake)

pybind11_add_module(_c_uutils_hash_compute pyuutils/hash/compute.cpp)
target_link_libraries(_c_uutils_hash_compute PRIVATE xxHash ${LINK_OPTIONS})
target_include_directories(_c_uutils_hash_compute PRIVATE
    ${CMAKE_CURRENT_SOURCE_DIR}
    ${CUSTOM_INSTALL_PREFIX}/include
)

install(TARGETS _c_uutils_hash_compute DESTINATION pyuutils/_core)

pybind11_add_module(_c_uutils_base_random pyuutils/base/random.cpp)
target_link_libraries(_c_uutils_base_random PRIVATE xxHash ${LINK_OPTIONS})
target_include_directories(_c_uutils_base_random PRIVATE
    ${CMAKE_CURRENT_SOURCE_DIR}
    ${CUSTOM_INSTALL_PREFIX}/include
)

install(TARGETS _c_uutils_base_random DESTINATION pyuutils/_core)


# list(APPEND PYBIND_MODULES
#     "_c_uutils_hash_compute|pyuutils/hash/compute.cpp"
#     "_c_uutils_base_random|pyuutils/base/random.cpp"
# )
#
# foreach(MODULE_PAIR IN LISTS PYBIND_MODULES)
#     message(STATUS "Current Pair: ${MODULE_PAIR}")
#     string(FIND "${MODULE_PAIR}" "|" SEMICOLON_POS)
#     if(SEMICOLON_POS GREATER -1)
#         string(SUBSTRING "${MODULE_PAIR}" 0 ${SEMICOLON_POS} MODULE_NAME)
#         math(EXPR SOURCE_START "${SEMICOLON_POS} + 1")
#         string(SUBSTRING "${MODULE_PAIR}" ${SOURCE_START} -1 SOURCE_FILE)
#         message(STATUS "Module: ${MODULE_NAME}, Source file: ${SOURCE_FILE}")
#
#         pybind11_add_module(${MODULE_NAME} ${SOURCE_FILE})
#         target_link_libraries(${MODULE_NAME} PRIVATE xxHash ${LINK_OPTIONS})
#         target_include_directories(${MODULE_NAME} PRIVATE
#             ${CMAKE_CURRENT_SOURCE_DIR}
#             ${CUSTOM_INSTALL_PREFIX}/include
#         )
#
#         get_filename_component(INSTALL_DIR "${SOURCE_FILE}" PATH)
#         install(TARGETS ${MODULE_NAME} DESTINATION ${INSTALL_DIR})
#     else()
#         message(FATAL_ERROR "Invalid module pair format: ${MODULE_PAIR}")
#     endif()
# endforeach()
