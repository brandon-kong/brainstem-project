#pragma once

#include "http/http.h"
#include <memory>
#include <string>

#include "Domain.h"

namespace amba
{
    class IAmbaClient
    {
        public:
            // Big 4
            IAmbaClient() = delete;
            IAmbaClient(const std::string& baseUrl, std::unique_ptr<ITransport> transport);
            IAmbaClient(const IAmbaClient&) = delete;
            IAmbaClient& operator=(const IAmbaClient&) = delete;
            IAmbaClient(IAmbaClient&&) = delete;
            IAmbaClient& operator=(IAmbaClient&&) = delete;
            virtual ~IAmbaClient() = default;

            domain::Gene GetGeneFromId(const int id) const;
            domain::Gene GetGeneFromAcronym(const std::string& acronym) const;
        protected:
            std::unique_ptr<ITransport> transport;
            const std::string baseUrl;
    };
}