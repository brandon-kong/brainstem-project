#pragma once

constexpr float SMALL_DATA_SIZE_BYTES = 1e6f;

namespace settings {
    typedef struct Settings {
        /** Determines whether to load files <= 1MB in memory on startup */
        bool loadSmallDataInMemory;
        /** Determines whether to use multithreading for tasks that support it */
        bool useMultithreading;
    } Settings;
}
