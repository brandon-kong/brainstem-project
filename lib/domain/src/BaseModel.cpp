#include "BaseModel.h"

BaseModel::BaseModel(int id) : id(id) {}

int BaseModel::GetId() const
{
    return this->id;
}