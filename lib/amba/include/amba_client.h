#pragma once

namespace amba
{
    class AmbaClient
    {
        public:
            // Big 6
            AmbaClient() = delete;
            AmbaClient(const char *pBaseUrl);
            AmbaClient(const AmbaClient&);
            AmbaClient& operator=(const AmbaClient&);
            AmbaClient(AmbaClient&&);
            AmbaClient& operator=(AmbaClient&&);
            ~AmbaClient();

            void Ping();

        private:
            const char* pBaseUrl;
    };
}