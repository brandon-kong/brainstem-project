#include "AmbaClientV1.h"
#include "CprTransport.h"

int main()
{
    std::unique_ptr<CprTransport> transport = std::make_unique<CprTransport>();
    amba::AmbaClientV1 pClient("https://api.brain-map.org/api/v2/", std::move(transport));
    return 0;
}