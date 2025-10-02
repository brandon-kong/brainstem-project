file(GLOB DOMAIN_SRC src/*.cpp)
add_library(domain STATIC ${DOMAIN_SRC})

target_include_directories(domain PUBLIC 
${CMAKE_CURRENT_SOURCE_DIR}/include
${PROJECT_SOURCE_DIR}/include
)