import json
import os

from src.image_processor.item_selector import convert_image_color
from src.text_extractor.age_range import get_age_range_values
from src.text_extractor.top_locations import get_top_location_info
from src.text_extractor.gender import get_gender_info
from src.text_extractor.discovery import get_discovery_info
from src.output_exporter.to_excel_importer import import_info_into_excel
from utils.folder_file_manager import save_file
from utils.google_ocr import GoogleVisionAPI
from settings import LOCAL, CUR_DIR, TEMP_IMG_PATH


class OCRExtractor:

    def __init__(self):

        self.google_ocr = GoogleVisionAPI()
        self.info = {
            "Reach": {
                "Start Date": "",
                "End Date": ""
            },
            "Impressions": {
                "Start Date": "",
                "End Date": ""
            },
            "Gender": {
                "Men": "",
                "Women": ""
            },
            "Age Range - All": {},
            "Age Range - Men": {},
            "Age Range - Women": {},
            "Top Locations - Cities": {
                "City Name 1": "",
                "City % 1": "",
                "City Name 2": "",
                "City % 2": "",
                "City Name 3": "",
                "City % 3": "",
                "City Name 4": "",
                "City % 4": "",
                "City Name 5": "",
                "City % 5": ""
            },
            "Top Locations - Countries": {
                "Country Name 1": "",
                "Country % 1": "",
                "Country Name 2": "",
                "Country % 2": "",
                "Country Name 3": "",
                "Country % 3": "",
                "Country Name 4": "",
                "Country % 4": "",
                "Country Name 5": "",
                "Country % 5": ""
            }
        }

    def process_ocr_text(self, frame_path, file_name):

        sharpen_frame_path = convert_image_color(frame_path=frame_path, file_name=file_name)
        image_ocr_json = self.google_ocr.detect_text(path=sharpen_frame_path)

        if LOCAL:
            json_file_path = os.path.join(CUR_DIR, 'temp', "temp_{}.json".format(file_name))
            save_file(filename=json_file_path, content=json.dumps(image_ocr_json), method="w")

        self.extract_whole_info(frame_path=sharpen_frame_path, json_data=image_ocr_json)
        save_path = import_info_into_excel(info=self.info, file_name=file_name)

        return save_path

    def extract_whole_info(self, frame_path, json_data):

        age_dict, age_blog_width = get_age_range_values(frame_path=frame_path, json_data=json_data)
        for age_key in age_dict.keys():
            self.info["Age Range - {}".format(age_key)] = age_dict[age_key]
        location_dict, location_blog_width = get_top_location_info(frame_path=frame_path, json_data=json_data)
        for location_key in location_dict.keys():
            for i, info_sub_key in enumerate(self.info["Top Locations - {}".format(location_key)].keys()):
                location_sub_keys = list(location_dict[location_key].keys())
                if location_sub_keys:
                    location_sub_key = location_sub_keys[i // 2]
                    if i % 2 == 0:
                        self.info["Top Locations - {}".format(location_key)][info_sub_key] = location_sub_key
                    else:
                        self.info["Top Locations - {}".format(location_key)][info_sub_key] = \
                            location_dict[location_key][location_sub_key]
                else:
                    self.info["Top Locations - {}".format(location_key)][info_sub_key] = ""
        gender_dict = get_gender_info(json_data=json_data, blog_width=max(location_blog_width, age_blog_width))
        self.info["Gender"]["Men"] = gender_dict["Men"]
        self.info["Gender"]["Women"] = gender_dict["Women"]
        discovery_dict = get_discovery_info(json_data=json_data, blog_width=max(location_blog_width, age_blog_width))
        self.info["Reach"] = discovery_dict["Reach"]
        self.info["Impressions"] = discovery_dict["Impression"]

        return


if __name__ == '__main__':

    with open('/media/mensa/Data/Task/InstagramOCR/temp/temp_example3.json') as f:
        json_content_ = json.load(f)
    OCRExtractor().extract_whole_info(frame_path="/media/mensa/Data/Task/InstagramOCR/temp_example3.jpg",
                                      json_data=json_content_)
