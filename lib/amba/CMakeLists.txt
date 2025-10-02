file(GLOB AMBA_SRC src/*.cpp)
add_library(amba STATIC ${AMBA_SRC})

target_include_directories(amba PUBLIC 
${CMAKE_CURRENT_SOURCE_DIR}/include
${PROJECT_SOURCE_DIR}/include
${PROJECT_SOURCE_DIR}/lib/domain/include
${PROJECT_SOURCE_DIR}/internal/http/include
)

target_link_libraries(amba PRIVATE domain http_internal)
