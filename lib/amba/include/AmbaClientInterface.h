#pragma once

#include "http/http.h"
#include <memory>
#include <string>

// Forward declarations
class Gene;

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

            Gene GetGeneFromId(const int id) const;
            Gene GetGeneFromAcronym(const std::string& acronym) const;
        protected:
            std::unique_ptr<ITransport> transport;
            const std::string baseUrl;
    };
}