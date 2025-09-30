cmake_minimum_required(VERSION 3.15)
project(BrainstemProject)

set(CMAKE_CXX_STANDARD 17)

include_directories(${PROJECT_SOURCE_DIR}/include)

add_subdirectory(lib/amba)
add_subdirectory(internal/http)
add_subdirectory(src)
