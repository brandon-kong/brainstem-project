"""
util/constants.py

This module is responsible for providing constants that are used throughout the
application.

"""

# ENGINES
VISUALIZATION_ENGINES = ["plotly", "matplotlib", "seaborn"]

CLUSTER_LABEL_COLUMN_PREFIX = "Cluster_"

# CONFIG
CONFIG_FILE = "config.json"


# TERMINAL COLORS
class TERMINAL_COLORS():
    ENDC = '\033[0m'

    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

    BLACK = '\033[30m'
    RED = '\033[31m'
    GREEN = '\033[32m'
    YELLOW = '\033[33m'
    BLUE = '\033[34m'
    MAGENTA = '\033[35m'
    CYAN = '\033[36m'
    WHITE = '\033[37m'

    BOLD_BLACK = '\033[1;30m'
    BOLD_RED = '\033[1;31m'
    BOLD_GREEN = '\033[1;32m'
    BOLD_YELLOW = '\033[1;33m'
    BOLD_BLUE = '\033[1;34m'
    BOLD_MAGENTA = '\033[1;35m'
    BOLD_CYAN = '\033[1;36m'
    BOLD_WHITE = '\033[1;37m'


# CACHE
CACHE_SIZE = 256

# DATA SETS
# MASTER: Reserved Key for the original data

MASTER_DATASET = "MASTER"

DATA_SETS = {
    "NonGeneColumns": "data/parent/NonGeneColumns.csv",
    "Coronal": {
        "Density": {
            MASTER_DATASET: "data/parent/[4k]_NewDenCor.csv",
            "No_NaN": "data/parent/[4k]_DenCor_No_NaN.csv",
        }
    }
}

NON_GENE_COLUMNS = ["index", "X", "Y", "Z", "Structure-ID"]

MAX_DIRECTORY_PRINT_DEPTH = 20  # The maximum depth to print the directories in the cache
