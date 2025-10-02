#pragma once

#include <string>
#include "http/http.h"

class CprTransport : public ITransport
{
    public:
        CprTransport() = default;
        CprTransport(const CprTransport&) = default;
        CprTransport& operator=(const CprTransport&) = default;
        ~CprTransport() = default;

        HttpResponse Request(HttpMethod method, std::string url, std::string payload = "", const std::unordered_map<std::string, std::string>& headers = {});
};