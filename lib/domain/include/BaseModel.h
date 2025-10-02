#pragma once

namespace domain
{
    class BaseModel
    {
        public:
            BaseModel(int id);

            int GetId() const;
        private:
            BaseModel() = delete;
        private:
        const int id;
    };
}
