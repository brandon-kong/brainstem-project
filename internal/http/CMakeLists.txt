file(GLOB HTTP_SRC src/*.cpp)
add_library(http_internal STATIC ${HTTP_SRC})

target_include_directories(http_internal PRIVATE ${CMAKE_CURRENT_SOURCE_DIR}/include)
