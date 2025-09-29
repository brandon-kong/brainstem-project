file(GLOB ML_SRC src/*.cpp)
add_library(ml STATIC ${ML_SRC})

target_include_directories(ml PUBLIC ${CMAKE_CURRENT_SOURCE_DIR})
