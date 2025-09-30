#pragma once

#include "http/http.h"

class CprTransport : public ITransport
{
    public:
        CprTransport() = default;
        CprTransport(const CprTransport&) = default;
        CprTransport& operator=(const CprTransport&) = default;
        ~CprTransport() = default;

        HttpResponse request(HttpMethod method, const char* url, const char* payload = "", const std::unordered_map<const char*, const char*>& headers);
};