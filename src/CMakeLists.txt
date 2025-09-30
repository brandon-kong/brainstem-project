add_executable(brainstem main.cpp)

target_link_libraries(brainstem PRIVATE amba http_internal)

target_include_directories(brainstem PRIVATE
    ${PROJECT_SOURCE_DIR}/lib/amba
    ${PROJECT_SOURCE_DIR}/internal/http
    ${PROJECT_SOURCE_DIR}/include
)
