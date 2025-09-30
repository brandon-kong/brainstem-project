#include "cpr_transport.h"
#include <iostream>

HttpResponse CprTransport::request(HttpMethod method, const char* url, const char* payload, const std::unordered_map<const char*, const char*>& headers)
{
    std::printf("Sending a request to %s with payload %s\n", url, payload);
}