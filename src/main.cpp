#include "amba_client.h"

void main()
{
    amba::AmbaClient pClient("https://api.amba.com/");
    pClient.Ping();
}