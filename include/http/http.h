#pragma once

#include <string>
#include <unordered_map>

enum class HttpMethod { GET, POST, PUT, DELETE };

typedef struct HttpResponse
{
    int statusCode;
    std::string body;
    std::unordered_map<std::string, std::string>& headers;
} HttpResponse;

class ITransport
{
public:
    virtual ~ITransport() = default;
    virtual HttpResponse request(
        HttpMethod method,
        std::string url, 
        std::string payload = "",
        const std::unordered_map<std::string, std::string>& headers = {}
    ) = 0;
};