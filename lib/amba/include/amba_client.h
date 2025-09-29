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
            AmbaClient(AmbaClient&&) = delete;
            AmbaClient& operator=(AmbaClient&&) = delete;
            ~AmbaClient();

            void Ping();

        private:
            void privCopyBaseUrl(const char* pBaseUrl);

        private:
            const char* pBaseUrl;
    };
}