#pragma once

#include "amba_client_interface.h"
#include "http/http.h"

namespace amba
{
    class AmbaClientV1 : public IAmbaClient
    {
        public:
            explicit AmbaClientV1(std::string& pBaseUrl);
            ~AmbaClientV1();
    };
}