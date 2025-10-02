#include "Gene.h"

domain::Gene::Gene(int id, std::string name, std::string acronym) : BaseModel(id), name(name), acronym(acronym) {}

const std::string domain::Gene::GetName() const
{
    return this->name;
}

const std::string domain::Gene::GetAcronym() const
{
    return this->acronym;
}
