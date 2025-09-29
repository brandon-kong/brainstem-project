# Create the executable from main.cpp
add_executable(brainstem main.cpp)

# Link the executable to the libraries
target_link_libraries(brainstem PRIVATE amba)

# Include headers from the libraries
target_include_directories(brainstem PRIVATE
    ${PROJECT_SOURCE_DIR}/lib/amba
)
