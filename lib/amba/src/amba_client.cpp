#include "amba_client_v1.h"
#include "cpr_transport.h"

#include <iostream>
#include <cstring>

amba::IAmbaClient::IAmbaClient(std::string& baseUrl) : baseUrl(baseUrl) {}

amba::AmbaClientV1::AmbaClientV1(std::string& baseUrl) : IAmbaClient(baseUrl)
{
    this->transport = new CprTransport();
}

amba::AmbaClientV1::~AmbaClientV1()
{
    delete this->transport;
}