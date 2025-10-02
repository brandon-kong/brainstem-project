#include "CprTransport.h"
#include <iostream>

HttpResponse CprTransport::request(HttpMethod method, std::string url, std::string payload, const std::unordered_map<std::string, std::string>& headers)
{
    std::printf("Sending a request to %s with payload %s\n", url.c_str(), payload.c_str());
    std::unordered_map<std::string, std::string> resp_headers;
    return HttpResponse{ 200, std::string("body"), resp_headers };
}