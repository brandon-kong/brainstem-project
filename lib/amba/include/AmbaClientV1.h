#pragma once

#include "AmbaClientInterface.h"
#include "http/http.h"

namespace amba
{
    class AmbaClientV1 : public IAmbaClient
    {
        public:
            explicit AmbaClientV1(const std::string& pBaseUrl, std::unique_ptr<ITransport> transport);
            ~AmbaClientV1() = default;
    };
}