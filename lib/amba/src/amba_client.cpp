#include "amba_client.h"
#include <iostream>
#include <cstring>

amba::AmbaClient::AmbaClient(const char* pBaseUrl)
{
    this->privCopyBaseUrl(pBaseUrl);
}

amba::AmbaClient::AmbaClient(const AmbaClient& rClient)
{
    this->privCopyBaseUrl(rClient.pBaseUrl);
}

amba::AmbaClient& amba::AmbaClient::operator=(const AmbaClient& rClient)
{
    if (this != &rClient)
    {
        delete this->pBaseUrl;
        this->privCopyBaseUrl(rClient.pBaseUrl);
    }

    return *this;
}

void amba::AmbaClient::Ping()
{
    // Ping the endpoints to make sure they are active
    std::printf("Pinging...\n");
}

void amba::AmbaClient::privCopyBaseUrl(const char* pBaseUrl)
{
    size_t size = std::strlen(pBaseUrl) + 1;
    
    // Copy the string
    char* pBuffer = new char[size];
    std::strncpy(pBuffer, pBaseUrl, size);

    this->pBaseUrl = pBuffer;
}

amba::AmbaClient::~AmbaClient()
{
    delete this->pBaseUrl;
}

