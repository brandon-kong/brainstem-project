#include "AmbaClientInterface.h"
#include "Gene.h"

amba::IAmbaClient::IAmbaClient(const std::string& baseUrl, std::unique_ptr<ITransport> transport) : baseUrl(baseUrl), transport(std::move(transport)) {}

Gene amba::IAmbaClient::GetGeneFromId(const int id) const
{
    // Check if the gene data is in the cache
    HttpResponse res = this->transport.get()->request(HttpMethod::GET, "data/SectionDataSet/query.json?criteria=%5Bfailed$eqfalse%5D%5Bdelegate$eqtrue%5D,products%5Bid$eq1%5D,specimen(donor(age%5Bname$eqP56%5D)),plane_of_section[name$eqsagittal]&include=genes&num_rows=all");
    std::printf("Status code: %d\n", res.statusCode);
    return Gene(0, "name", "acronym");
}