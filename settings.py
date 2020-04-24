import os

from utils.folder_file_manager import make_directory_if_not_exists


CUR_DIR = os.path.dirname(os.path.abspath(__file__))
CREDENTIAL_PATH = os.path.join(CUR_DIR, 'utils', 'credential', 'vision_key.txt')
INPUT_IMG_DIR = os.path.join(CUR_DIR, 'input')
OUTPUT_DIR = make_directory_if_not_exists(os.path.join(CUR_DIR, 'output'))
INPUT_IMAGE_PATH = "/input/example1.jpg"
TEMP_IMG_PATH = os.path.join(CUR_DIR, 'temp.jpg')

EXCEL_FIELDS = ["Discovery", "Start Date", "End Date", "Reach", "Start Date", "End Date", "Impressions", "Gender",
                "Men", "Women", "Age Range - All", "13 - 17", "18 - 24", "25 - 34", "35 - 44", "45 - 54", "55 - 64",
                "65+", "Age Range - Men", "13 - 17", "18 - 24", "25 - 34", "35 - 44", "45 - 54", "55 - 64", "65+",
                "Age Range - Women", "13 - 17", "18 - 24", "25 - 34", "35 - 44", "45 - 54", "55 - 64", "65+",
                "Top Locations - Cities", "City Name 1", "City % 1", "City Name 2", "City % 2", "City Name 3",
                "City % 3", "City Name 4", "City % 4", "City Name 5", "City % 5", "Top Locations - Countries",
                "Country Name 1", "Country % 1", "Country Name 2", "Country % 2", "Country Name 3", "Country % 3",
                "Country Name 4", "Country % 4", "Country Name 5", "Country % 5"]

LINE_DIFF = 10
RANGE_MARGIN = 30

LOCAL = True
