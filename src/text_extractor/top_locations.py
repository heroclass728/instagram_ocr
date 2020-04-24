import json

from src.image_processor.item_selector import select_item
from utils.folder_file_manager import log_print
from settings import RANGE_MARGIN, LINE_DIFF


def get_top_location_info(frame_path, json_data):
    top_location_dict = {}
    location_items = ["Cities", "Countries"]

    top_location_json = json_data["textAnnotations"][1:]
    location_ranges = []
    countries = []
    location_left = 0
    location_top = 0
    location_right = 0
    cities_region = None
    countries_region = None

    try:
        for i, _json_1 in enumerate(top_location_json):

            if _json_1["description"] == "Top" and top_location_json[i + 1]["description"] == "Locations":
                tmp_center_y_left = int(0.5 * (_json_1["boundingPoly"]["vertices"][0]["y"]
                                               + _json_1["boundingPoly"]["vertices"][2]["y"]))
                tmp_location_left = _json_1["boundingPoly"]["vertices"][0]["x"]
                tmp_location_right = top_location_json[i + 1]["boundingPoly"]["vertices"][1]["x"]
                tmp_location_bottom = _json_1["boundingPoly"]["vertices"][2]["y"]
                for j, _json_2 in enumerate(top_location_json):
                    if _json_2["description"] == "Countries" and top_location_json[j - 1]["description"] == "Cities":
                        tmp_center_y_right = int(0.5 * (_json_2["boundingPoly"]["vertices"][0]["y"]
                                                        + _json_2["boundingPoly"]["vertices"][2]["y"]))
                        if abs(tmp_center_y_left - tmp_center_y_right) < RANGE_MARGIN:
                            location_left = _json_1["boundingPoly"]["vertices"][0]["x"] - RANGE_MARGIN
                            location_top = _json_1["boundingPoly"]["vertices"][0]["y"] - RANGE_MARGIN
                            location_right = _json_2["boundingPoly"]["vertices"][1]["x"] + RANGE_MARGIN
                            break

                tmp_countries = []
                tmp_country = {"name": "", "y": 0}
                cnt = 0
                tmp_right_side = tmp_location_right
                while len(tmp_countries) < 5:
                    _json_3 = top_location_json[cnt]
                    _json_3_center_y = int(0.5 * (_json_3["boundingPoly"]["vertices"][0]["x"] +
                                                   _json_3["boundingPoly"]["vertices"][1]["x"]))
                    if tmp_location_left <= _json_3_center_y <= tmp_location_right and \
                            _json_3["boundingPoly"]["vertices"][0]["y"] > tmp_location_bottom and \
                            _json_3["description"] != "Less":
                        tmp_country_y = int(0.5 * (_json_3["boundingPoly"]["vertices"][0]["y"] +
                                                   _json_3["boundingPoly"]["vertices"][2]["y"]))
                        if abs(tmp_country_y - tmp_country["y"]) < LINE_DIFF:
                            tmp_country["name"] += _json_3["description"] + " "
                            tmp_right_side = _json_3["boundingPoly"]["vertices"][1]["x"]
                        else:
                            if tmp_country["name"] != "":
                                tmp_countries.append(tmp_country.copy())
                                if len(tmp_countries) == 1:
                                    tmp_location_right = tmp_right_side
                            tmp_country["name"] = _json_3["description"]
                            tmp_country["y"] = tmp_country_y
                    cnt += 1

                location_bottom = tmp_countries[-1]["y"] + RANGE_MARGIN
                location_ranges.append([location_left, location_top, location_right, location_bottom])
                countries.append(tmp_countries)

        correct_range_nums = []

        for i, location_range in enumerate(location_ranges):
            for _json in top_location_json:
                if "%" not in _json["description"]:
                    continue
                center_x = int(0.5 * (_json["boundingPoly"]["vertices"][0]["x"] +
                                      _json["boundingPoly"]["vertices"][1]["x"]))
                center_y = int(0.5 * (_json["boundingPoly"]["vertices"][0]["y"] +
                                      _json["boundingPoly"]["vertices"][3]["y"]))
                if location_range[0] <= center_x <= location_range[2] and \
                        location_range[1] <= center_y <= location_range[3]:
                    correct_range_nums.append(i)
                    break

        blog_width = 0

        for correct_range_num in correct_range_nums:

            top_location_data = []
            tmp_dict = {}
            location_coordinates = []

            left = location_ranges[correct_range_num][0]
            top = location_ranges[correct_range_num][1]
            right = location_ranges[correct_range_num][2]
            bottom = location_ranges[correct_range_num][3]

            blog_width += right - left

            sub_countries = countries[correct_range_num]
            for sub_country in sub_countries:
                tmp_dict[sub_country["name"]] = ""
                location_coordinates.append(sub_country["y"])

            for i, _json in enumerate(top_location_json):
                range_center_x = int(0.5 * (_json["boundingPoly"]["vertices"][0]["x"] +
                                            _json["boundingPoly"]["vertices"][1]["x"]))
                range_center_y = int(0.5 * (_json["boundingPoly"]["vertices"][0]["y"] +
                                            _json["boundingPoly"]["vertices"][2]["y"]))
                if left <= range_center_x <= right and top <= range_center_y < bottom:
                    top_location_data.append(_json)

            for range_data in top_location_data:
                range_data_center_y = int(0.5 * (range_data["boundingPoly"]["vertices"][0]["y"] +
                                                 range_data["boundingPoly"]["vertices"][2]["y"]))
                if range_data["description"] == "Cities":
                    cities_region = [range_data["boundingPoly"]["vertices"][0]["x"],
                                     range_data["boundingPoly"]["vertices"][0]["y"],
                                     range_data["boundingPoly"]["vertices"][2]["x"],
                                     range_data["boundingPoly"]["vertices"][2]["y"]]
                if range_data["description"] == "Countries":
                    countries_region = [range_data["boundingPoly"]["vertices"][0]["x"],
                                        range_data["boundingPoly"]["vertices"][0]["y"],
                                        range_data["boundingPoly"]["vertices"][2]["x"],
                                        range_data["boundingPoly"]["vertices"][2]["y"]]

                for sub_country in sub_countries:
                    if abs(range_data_center_y - sub_country["y"]) < LINE_DIFF \
                            and range_data["description"] not in sub_country["name"]:
                        tmp_dict[sub_country["name"]] += range_data["description"]

            location_item = select_item(frame_path=frame_path, region=[cities_region, countries_region],
                                        items=location_items)

            top_location_dict[location_item] = tmp_dict

        blog_width /= len(correct_range_nums)

        for item in location_items:
            tmp_dict = {}
            if item not in top_location_dict.keys():
                top_location_dict[item] = tmp_dict

        return top_location_dict, blog_width

    except Exception as e:
        log_print(info_str=e)
        for item in location_items:
            tmp_dict = {}
            top_location_dict[item] = tmp_dict

        blog_width = 0

        return top_location_dict, blog_width


if __name__ == '__main__':
    with open('') as f:
        json_content_ = json.load(f)
    get_top_location_info(frame_path="", json_data=json_content_)
