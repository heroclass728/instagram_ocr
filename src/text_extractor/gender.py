from utils.folder_file_manager import log_print
from settings import RANGE_MARGIN, LINE_DIFF


def get_gender_info(json_data, blog_width):

    gender_dict = {"Women": "", "Men": ""}
    gender_data = []
    gender_ranges = []
    percent_ranges = []
    gender_json = json_data["textAnnotations"][1:]

    try:
        for _json in gender_json:

            if _json["description"] == "Gender":
                left = _json["boundingPoly"]["vertices"][0]["x"] - RANGE_MARGIN
                top = _json["boundingPoly"]["vertices"][0]["y"] - RANGE_MARGIN
                right = left + blog_width + RANGE_MARGIN
                for _json_1 in gender_json:
                    women_center_x = int(0.5 * (_json_1["boundingPoly"]["vertices"][0]["x"] +
                                                _json_1["boundingPoly"]["vertices"][1]["x"]))
                    women_center_y = int(0.5 * (_json_1["boundingPoly"]["vertices"][0]["y"] +
                                                _json_1["boundingPoly"]["vertices"][2]["y"]))
                    if _json_1["description"] == "Women" and left <= women_center_x <= right and women_center_y >= top:
                        for _json_2 in gender_json:
                            if _json_2["description"] == "Men":
                                men_center_x = int(0.5 * (_json_2["boundingPoly"]["vertices"][0]["x"] +
                                                          _json_2["boundingPoly"]["vertices"][1]["x"]))
                                men_center_y = int(0.5 * (_json_2["boundingPoly"]["vertices"][0]["y"] +
                                                          _json_2["boundingPoly"]["vertices"][2]["y"]))
                                if left <= men_center_x <= right and abs(men_center_y - women_center_y) <= LINE_DIFF:
                                    bottom = men_center_y + RANGE_MARGIN
                                    gender_ranges.append([left, top, right, bottom])
                                    percent_ranges.append([_json["boundingPoly"]["vertices"][2]["y"],
                                                            _json_1["boundingPoly"]["vertices"][0]["y"],
                                                            _json_1["boundingPoly"]["vertices"][0]["x"],
                                                            _json_1["boundingPoly"]["vertices"][1]["x"],
                                                            _json_2["boundingPoly"]["vertices"][0]["x"],
                                                            _json_2["boundingPoly"]["vertices"][1]["x"]])
                                    break
                        break

        correct_range_num = 0
        if len(gender_ranges) > 1:

            for i, location_range in enumerate(gender_ranges):
                for _json in gender_json:
                    if "%" not in _json["description"]:
                        continue
                    center_x = int(0.5 * (_json["boundingPoly"]["vertices"][0]["x"] +
                                          _json["boundingPoly"]["vertices"][1]["x"]))
                    center_y = int(0.5 * (_json["boundingPoly"]["vertices"][0]["y"] +
                                          _json["boundingPoly"]["vertices"][3]["y"]))
                    if location_range[0] <= center_x <= location_range[2] and \
                            location_range[1] <= center_y <= location_range[3]:
                        correct_range_num = i
                        break

        left = gender_ranges[correct_range_num][0]
        top = gender_ranges[correct_range_num][1]
        right = gender_ranges[correct_range_num][2]
        bottom = gender_ranges[correct_range_num][3]

        percent_range = percent_ranges[correct_range_num]
        percent_top = percent_range[0]
        percent_bottom = percent_range[1]
        women_percent_left = percent_range[2]
        women_percent_right = percent_range[3]
        men_percent_left = percent_range[4]
        men_percent_right = percent_range[5]

        for _json in gender_json:
            range_center_x = int(0.5 * (_json["boundingPoly"]["vertices"][0]["x"] +
                                        _json["boundingPoly"]["vertices"][1]["x"]))
            range_center_y = int(0.5 * (_json["boundingPoly"]["vertices"][0]["y"] +
                                        _json["boundingPoly"]["vertices"][2]["y"]))
            if left <= range_center_x <= right and top <= range_center_y < bottom:
                gender_data.append(_json)

        for range_data in gender_data:
            percent_center_x = int(0.5 * (range_data["boundingPoly"]["vertices"][0]["x"]
                                          + range_data["boundingPoly"]["vertices"][1]["x"]))
            percent_center_y = int(0.5 * (range_data["boundingPoly"]["vertices"][0]["y"]
                                          + range_data["boundingPoly"]["vertices"][2]["y"]))
            if women_percent_left <= percent_center_x <= women_percent_right and \
                    percent_top <= percent_center_y <= percent_bottom:
                gender_dict["Women"] += range_data["description"]
            if men_percent_left <= percent_center_x <= men_percent_right and \
                    percent_top <= percent_center_y <= percent_bottom:
                gender_dict["Men"] += range_data["description"]

        return gender_dict

    except Exception as e:
        log_print(info_str=e)

        return gender_dict


if __name__ == '__main__':

    get_gender_info(json_data="", blog_width=0)
