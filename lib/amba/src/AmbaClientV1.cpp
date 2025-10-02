#include "AmbaClientV1.h"

amba::AmbaClientV1::AmbaClientV1(const std::string& baseUrl, std::unique_ptr<ITransport> transport) : IAmbaClient(baseUrl, std::move(transport))
{}