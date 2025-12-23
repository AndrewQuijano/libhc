cmake_minimum_required(VERSION 3.15)

set (CMAKE_CONFIGURATION_TYPES "Release" CACHE STRING "Configs" FORCE)
set(CMAKE_VERBOSE_MAKEFILE OFF)

# Read version number from command line argument
if(DEFINED LIBHC_VERSION)
    string(REGEX MATCH "v?([0-9]+)\\.([0-9]+)\\.([0-9]+)" _ ${LIBHC_VERSION})
    set(CPACK_PACKAGE_VERSION_MAJOR ${CMAKE_MATCH_1})
    set(CPACK_PACKAGE_VERSION_MINOR ${CMAKE_MATCH_2})
    set(CPACK_PACKAGE_VERSION_PATCH ${CMAKE_MATCH_3})
    set(PROJECT_VERSION_MAJOR ${CMAKE_MATCH_1})
    set(PROJECT_VERSION_MINOR ${CMAKE_MATCH_2})
    set(PROJECT_VERSION_PATCH ${CMAKE_MATCH_3})
else()
    set(CPACK_PACKAGE_VERSION_MAJOR "0")
    set(CPACK_PACKAGE_VERSION_MINOR "0")
    set(CPACK_PACKAGE_VERSION_PATCH "0")
    set(PROJECT_VERSION_MAJOR "0")
    set(PROJECT_VERSION_MINOR "0")
    set(PROJECT_VERSION_PATCH "0")
endif()

project(libhc VERSION ${PROJECT_VERSION_MAJOR}.${PROJECT_VERSION_MINOR}.${PROJECT_VERSION_PATCH} LANGUAGES C CXX)

# --- Installation ---
include(GNUInstallDirs)

# Install the header file, we want this /usr/include/panda/hypercall.h
install(FILES include/hypercall.h
        DESTINATION ${CMAKE_INSTALL_INCLUDEDIR}/panda)

install(FILES "${CMAKE_CURRENT_SOURCE_DIR}/LICENSE" 
        DESTINATION "${CMAKE_INSTALL_DOCDIR}"
        RENAME "copyright")

include(CPackConfig.txt)
