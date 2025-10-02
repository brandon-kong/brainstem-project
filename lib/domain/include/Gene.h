#pragma once

#include "BaseModel.h"
#include <string>

namespace domain
{
    class Gene : public BaseModel
    {
        public:
            Gene(int id, std::string name, std::string acronym);

            const std::string GetName() const;
            const std::string GetAcronym() const;
        private:
        std::string name;
        std::string acronym;
    };
}
