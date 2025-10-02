#include "Gene.h"

Gene::Gene(int id, std::string name, std::string acronym) : BaseModel(id), name(name), acronym(acronym) {}

const std::string Gene::GetName() const
{
    return this->name;
}

const std::string Gene::GetAcronym() const
{
    return this->acronym;
}
