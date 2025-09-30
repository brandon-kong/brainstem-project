#pragma once

enum class ApiStatus {
    OK = 200,
    Unauthorized = 401,
    NotFound = 404,
    ServerError = 500,
    Timeout = 408,
    Unknown = -1,
};

template<typename T>
struct ApiResult {
    ApiStatus status;
    T payload;
    const char* errorMessage;
};