add_executable(brainstem main.cpp)

target_link_libraries(brainstem PRIVATE amba)

target_include_directories(brainstem PRIVATE
    ${PROJECT_SOURCE_DIR}/lib/amba
)
