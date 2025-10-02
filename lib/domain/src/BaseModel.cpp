#include "BaseModel.h"

domain::BaseModel::BaseModel(int id) : id(id) {}

int domain::BaseModel::GetId() const
{
    return this->id;
}