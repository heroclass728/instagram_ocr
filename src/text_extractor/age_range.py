import json

from utils.folder_file_manager import log_print
from src.image_processor.item_selector import select_item
from settings import LINE_DIFF, RANGE_MARGIN


def get_age_range_values(frame_path, json_data):
    age_range_dict = {}
    age_items = ["All", "Men", "Women"]

    age_range_json = json_data["textAnnotations"][1:]
    age_ranges = []
    age_range_left = 0
    age_range_top = 0
    age_range_right = 0
    age_range_bottom = 0
    first_age_range_coordinate = None
    second_age_range_coordinate = None
    third_age_range_coordinate = None
    forth_age_range_coordinate = None
    fifth_age_range_coordinate = None
    sixth_age_range_coordinate = None
    seventh_age_range_coordinate = None
    all_region = None
    men_region = None
    women_region = None

    try:
        for i, _json_1 in enumerate(age_range_json):

            if _json_1["description"] == "Age" and age_range_json[i + 1]["description"] == "Range":
                tmp_center_y_left = int(0.5 * (_json_1["boundingPoly"]["vertices"][0]["y"]
                                               + _json_1["boundingPoly"]["vertices"][2]["y"]))

                for j, _json_2 in enumerate(age_range_json):
                    if _json_2["description"] == "Women" and age_range_json[j - 1]["description"] == "Men" and \
                            age_range_json[j - 2]["description"] == "All":
                        tmp_center_y_right = int(0.5 * (_json_2["boundingPoly"]["vertices"][0]["y"]
                                                        + _json_2["boundingPoly"]["vertices"][2]["y"]))
                        if abs(tmp_center_y_left - tmp_center_y_right) < RANGE_MARGIN:
                            age_range_left = _json_1["boundingPoly"]["vertices"][0]["x"] - RANGE_MARGIN
                            age_range_top = _json_1["boundingPoly"]["vertices"][0]["y"] - RANGE_MARGIN
                            age_range_right = _json_2["boundingPoly"]["vertices"][1]["x"] + RANGE_MARGIN
                            break

                for _json_3 in age_range_json:
                    if _json_3["description"] == "65" and \
                            age_range_left <= int(0.5 * (_json_3["boundingPoly"]["vertices"][0]["x"] +
                                                         _json_3["boundingPoly"]["vertices"][1]["x"])) <= \
                            age_range_right:
                        age_range_bottom = _json_3["boundingPoly"]["vertices"][2]["y"] + LINE_DIFF
                        break

                age_ranges.append([age_range_left, age_range_top, age_range_right, age_range_bottom])
        correct_range_nums = []

        for i, age_range in enumerate(age_ranges):
            for _json in age_range_json:
                if "%" not in _json["description"]:
                    continue
                center_x = int(0.5 * (_json["boundingPoly"]["vertices"][0]["x"] +
                                      _json["boundingPoly"]["vertices"][1]["x"]))
                center_y = int(0.5 * (_json["boundingPoly"]["vertices"][0]["y"] +
                                      _json["boundingPoly"]["vertices"][3]["y"]))
                if age_range[0] <= center_x <= age_range[2] and age_range[1] <= center_y <= age_range[3]:
                    correct_range_nums.append(i)
                    break

        blog_width = 0

        for correct_range_num in correct_range_nums:

            tmp_dict = {
                "13 - 17": "",
                "18 - 24": "",
                "25 - 34": "",
                "35 - 44": "",
                "45 - 54": "",
                "55 - 64": "",
                "65 + ": ""
            }
            age_range_data = []

            left = age_ranges[correct_range_num][0]
            top = age_ranges[correct_range_num][1]
            right = age_ranges[correct_range_num][2]
            bottom = age_ranges[correct_range_num][3]
            blog_width += right - left

            for i, _json in enumerate(age_range_json):
                range_center_x = int(0.5 * (_json["boundingPoly"]["vertices"][0]["x"] +
                                            _json["boundingPoly"]["vertices"][1]["x"]))
                range_center_y = int(0.5 * (_json["boundingPoly"]["vertices"][0]["y"] +
                                            _json["boundingPoly"]["vertices"][2]["y"]))
                if _json["description"] == "13" and age_range_json[i + 1]["description"] == "-" \
                        and left <= range_center_x < right and top <= range_center_y <= bottom:
                    first_age_range_coordinate = [range_center_y,
                                                  age_range_json[i + 2]["boundingPoly"]["vertices"][1]["x"]]
                if _json["description"] == "18" and age_range_json[i + 1]["description"] == "-" \
                        and left <= range_center_x < right and top <= range_center_y <= bottom:
                    second_age_range_coordinate = [range_center_y,
                                                   age_range_json[i + 2]["boundingPoly"]["vertices"][1]["x"]]
                if _json["description"] == "25" and age_range_json[i + 1]["description"] == "-" \
                        and left <= range_center_x < right and top <= range_center_y <= bottom:
                    third_age_range_coordinate = [range_center_y,
                                                  age_range_json[i + 2]["boundingPoly"]["vertices"][1]["x"]]
                if _json["description"] == "35" and age_range_json[i + 1]["description"] == "-" \
                        and left <= range_center_x < right and top <= range_center_y <= bottom:
                    forth_age_range_coordinate = [range_center_y,
                                                  age_range_json[i + 2]["boundingPoly"]["vertices"][1]["x"]]
                if _json["description"] == "45" and age_range_json[i + 1]["description"] == "-" \
                        and left <= range_center_x < right and top <= range_center_y <= bottom:
                    fifth_age_range_coordinate = [range_center_y,
                                                  age_range_json[i + 2]["boundingPoly"]["vertices"][1]["x"]]
                if _json["description"] == "55" and age_range_json[i + 1]["description"] == "-" \
                        and left <= range_center_x < right and top <= range_center_y <= bottom:
                    sixth_age_range_coordinate = [range_center_y,
                                                  age_range_json[i + 2]["boundingPoly"]["vertices"][1]["x"]]
                if _json["description"] == "65" and left <= range_center_x < right and top <= range_center_y <= bottom:
                    seventh_age_range_coordinate = [range_center_y,
                                                    age_range_json[i + 1]["boundingPoly"]["vertices"][1]["x"]]
                if left <= range_center_x <= right and top <= range_center_y < bottom:
                    age_range_data.append(_json)

            for range_data in age_range_data:
                range_data_center_y = int(0.5 * (range_data["boundingPoly"]["vertices"][0]["y"] +
                                                 range_data["boundingPoly"]["vertices"][2]["y"]))
                range_data_center_x = int(0.5 * (range_data["boundingPoly"]["vertices"][0]["x"] +
                                                 range_data["boundingPoly"]["vertices"][1]["x"]))
                if range_data["description"] == "All":
                    all_region = [range_data["boundingPoly"]["vertices"][0]["x"],
                                  range_data["boundingPoly"]["vertices"][0]["y"],
                                  range_data["boundingPoly"]["vertices"][2]["x"],
                                  range_data["boundingPoly"]["vertices"][2]["y"]]
                if range_data["description"] == "Men":
                    men_region = [range_data["boundingPoly"]["vertices"][0]["x"],
                                  range_data["boundingPoly"]["vertices"][0]["y"],
                                  range_data["boundingPoly"]["vertices"][2]["x"],
                                  range_data["boundingPoly"]["vertices"][2]["y"]]
                if range_data["description"] == "Women":
                    women_region = [range_data["boundingPoly"]["vertices"][0]["x"],
                                    range_data["boundingPoly"]["vertices"][0]["y"],
                                    range_data["boundingPoly"]["vertices"][2]["x"],
                                    range_data["boundingPoly"]["vertices"][2]["y"]]
                if abs(range_data_center_y - first_age_range_coordinate[0]) < LINE_DIFF:
                    if range_data_center_x > first_age_range_coordinate[1]:
                        tmp_dict["13 - 17"] += range_data["description"]
                if abs(range_data_center_y - second_age_range_coordinate[0]) < LINE_DIFF:
                    if range_data_center_x > second_age_range_coordinate[1]:
                        tmp_dict["18 - 24"] += range_data["description"]
                if abs(range_data_center_y - third_age_range_coordinate[0]) < LINE_DIFF:
                    if range_data_center_x > third_age_range_coordinate[1]:
                        tmp_dict["25 - 34"] += range_data["description"]
                if abs(range_data_center_y - forth_age_range_coordinate[0]) < LINE_DIFF:
                    if range_data_center_x > forth_age_range_coordinate[1]:
                        tmp_dict["35 - 44"] += range_data["description"]
                if abs(range_data_center_y - fifth_age_range_coordinate[0]) < LINE_DIFF:
                    if range_data_center_x > fifth_age_range_coordinate[1]:
                        tmp_dict["45 - 54"] += range_data["description"]
                if abs(range_data_center_y - sixth_age_range_coordinate[0]) < LINE_DIFF:
                    if range_data_center_x > sixth_age_range_coordinate[1]:
                        tmp_dict["55 - 64"] += range_data["description"]
                if abs(range_data_center_y - seventh_age_range_coordinate[0]) < LINE_DIFF:
                    if range_data_center_x > seventh_age_range_coordinate[1]:
                        tmp_dict["65 + "] += range_data["description"]

            age_item = select_item(frame_path=frame_path, region=[all_region, men_region, women_region],
                                   items=age_items)
            age_range_dict[age_item] = tmp_dict

        blog_width /= len(correct_range_nums)

        for item in age_items:
            tmp_dict = {
                "13 - 17": "",
                "18 - 24": "",
                "25 - 34": "",
                "35 - 44": "",
                "45 - 54": "",
                "55 - 64": "",
                "65 + ": ""
            }
            if item not in age_range_dict.keys():
                age_range_dict[item] = tmp_dict

        return age_range_dict, blog_width

    except Exception as e:
        log_print(info_str=e)
        for item in age_items:
            tmp_dict = {
                "13 - 17": "",
                "18 - 24": "",
                "25 - 34": "",
                "35 - 44": "",
                "45 - 54": "",
                "55 - 64": "",
                "65 + ": ""
            }
            age_range_dict[item] = tmp_dict

        blog_width = 0

        return age_range_dict, blog_width


if __name__ == '__main__':
    with open('/media/mensa/Data/Task/InstagramOCR/temp/temp_example1.json') as f:
        json_content_ = json.load(f)
    get_age_range_values(frame_path="/media/mensa/Data/Task/InstagramOCR/input/example1.jpg", json_data=json_content_)
