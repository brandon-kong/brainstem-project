"""
util/constants.py

This module is responsible for providing constants that are used throughout the
application.

"""

# ENGINES
VISUALIZATION_ENGINES = ["plotly", "matplotlib", "seaborn"]

# CONFIG
CONFIG_FILE = "config.json"


# TERMINAL COLORS
class TERMINAL_COLORS:
    ENDC = '\033[0m'
    RESET = '\033[0m'

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
            "output_K1": "data/parent/output_K1.csv",
            "[70% Edge]": "data/parent/70_edge_voxels.csv",
        }
    },
}

MAX_DIRECTORY_PRINT_DEPTH = 10  # The maximum depth to print the directories in the cache

STRUCTURE_IDS = [
    773, 136, 1098, 939, 970, 235, 143, 978, 1107, 852, 661, 307, 1048
]

STRUCTURE_ID_COLORS = {
    773: "rgb(255, 0, 0)",
    136: "rgb(0, 255, 0)",
    1098: "rgb(0, 0, 255)",
    939: "rgb(255, 255, 0)",
    970: "rgb(0, 255, 255)",
    235: "rgb(255, 0, 255)",
    143: "rgb(192, 192, 192)",
    978: "rgb(128, 128, 128)",
    1107: "rgb(128, 0, 0)",
    852: "rgb(128, 128, 0)",
    661: "rgb(0, 128, 0)",
    307: "rgb(0, 128, 128)",
    1048: "rgb(0, 0, 128)"
}

SAVE_GENERATED_DATA_PATH = "data/generated/"

BACK_KEYWORD = "back"  # The keyword to go back to the previous menu

# DATA HEADER NAMES

CLUSTER_LABEL_COLUMN_PREFIX = "Cluster_"
XYZ_COLUMNS = ["X", "Y", "Z"]
STRUCTURE_IDS_COLUMN = "Structure-ID"
VOXROWNUM_COLUMN = "voxRowNum"

NON_GENE_COLUMNS = [
    "Unnamed: 0",
    "Unnamed: 0.1",
    "Unnamed: 0.1.1",
    "Index",
    "index",
    "voxRowNum",
    CLUSTER_LABEL_COLUMN_PREFIX,
    STRUCTURE_IDS_COLUMN,
    VOXROWNUM_COLUMN,
    XYZ_COLUMNS[0],
    XYZ_COLUMNS[1],
    XYZ_COLUMNS[2],
]

# DATA PROPERTY NAMES

HAS_GENES = "has_genes"
HAS_NON_GENES = "has_non_genes"
HAS_XYZ = "has_xyz"
HAS_STRUCTURE_IDS = "has_structure_ids"
CAN_CLUSTER = "can_cluster"
HAS_NAN = "has_nan"
CAN_VISUALIZE = "can_visualize"
WAYS_TO_VISUALIZE = "ways_to_visualize"

# KMEANS

KMEANS_SEED = 25
