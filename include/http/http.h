#pragma once

#include <unordered_map>

enum class HttpMethod { GET, POST, PUT, DELETE };

typedef struct HttpResponse
{
    int statusCode;
    const char* body;
    std::unordered_map<const char*, const char*> headers;
} HttpResponse;

class ITransport
{
public:
    virtual ~ITransport() = default;
    virtual HttpResponse request(
        HttpMethod method,
        const char* url, 
        const char* payload = "",
        const std::unordered_map<const char*, const char*>& headers = {}
    ) = 0;
};