#pragma once

#include "http/http.h"
#include <string>

namespace amba
{
    class IAmbaClient
    {
        public:
            // Big 4
            IAmbaClient() = default;
            IAmbaClient(std::string& baseUrl);
            IAmbaClient(const IAmbaClient&) = delete;
            IAmbaClient& operator=(const IAmbaClient&) = delete;
            IAmbaClient(IAmbaClient&&) = delete;
            IAmbaClient& operator=(IAmbaClient&&) = delete;
            virtual ~IAmbaClient() = default;
        protected:
            ITransport* transport;
            std::string baseUrl;
    };
}