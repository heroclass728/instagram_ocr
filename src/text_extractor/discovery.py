from utils.folder_file_manager import log_print
from settings import RANGE_MARGIN


def get_discovery_info(json_data, blog_width):
    discovery_dict = {
        "Reach": {
            "Start Date": "",
            "End Date": ""
        },
        "Impression": {
            "Start Date": "",
            "End Date": ""
        }
    }
    discovery_data = []
    discovery_ranges = []
    discovery_json = json_data["textAnnotations"][1:]

    try:
        for _json in discovery_json:

            if _json["description"] == "Discovery":
                left = _json["boundingPoly"]["vertices"][0]["x"] - RANGE_MARGIN
                top = _json["boundingPoly"]["vertices"][0]["y"] - RANGE_MARGIN
                right = left + blog_width + RANGE_MARGIN
                for _json_1 in discovery_json:
                    interaction_center_x = int(0.5 * (_json_1["boundingPoly"]["vertices"][0]["x"] +
                                                      _json_1["boundingPoly"]["vertices"][1]["x"]))
                    interaction_center_y = int(0.5 * (_json_1["boundingPoly"]["vertices"][0]["y"] +
                                                      _json_1["boundingPoly"]["vertices"][2]["y"]))
                    if _json_1["description"] == "Interactions" and left <= interaction_center_x <= right and \
                            interaction_center_y >= top:
                        bottom = interaction_center_y + RANGE_MARGIN
                        discovery_ranges.append([left, top, right, bottom])
                        break

        correct_range_num = 0
        if len(discovery_ranges) > 1:

            for i, location_range in enumerate(discovery_ranges):
                for _json in discovery_json:
                    if "Reach" not in _json["description"] or "Impressions" not in _json["description"]:
                        continue
                    center_x = int(0.5 * (_json["boundingPoly"]["vertices"][0]["x"] +
                                          _json["boundingPoly"]["vertices"][1]["x"]))
                    center_y = int(0.5 * (_json["boundingPoly"]["vertices"][0]["y"] +
                                          _json["boundingPoly"]["vertices"][3]["y"]))
                    if location_range[0] <= center_x <= location_range[2] and \
                            location_range[1] <= center_y <= location_range[3]:
                        correct_range_num = i
                        break

        left = discovery_ranges[correct_range_num][0]
        top = discovery_ranges[correct_range_num][1]
        right = discovery_ranges[correct_range_num][2]
        bottom = discovery_ranges[correct_range_num][3]

        for _json in discovery_json:
            range_center_x = int(0.5 * (_json["boundingPoly"]["vertices"][0]["x"] +
                                        _json["boundingPoly"]["vertices"][1]["x"]))
            range_center_y = int(0.5 * (_json["boundingPoly"]["vertices"][0]["y"] +
                                        _json["boundingPoly"]["vertices"][2]["y"]))
            if left <= range_center_x <= right and top <= range_center_y < bottom:
                discovery_data.append(_json)

        reach_top = None
        reach_bottom = None
        impression_top = None
        impression_bottom = None

        for range_data in discovery_data:
            if range_data["description"] == "Reach":
                reach_top = range_data["boundingPoly"]["vertices"][2]["y"]
            if range_data["description"] == "Impressions":
                reach_bottom = range_data["boundingPoly"]["vertices"][0]["y"]
                impression_top = range_data["boundingPoly"]["vertices"][2]["y"]
            if range_data["description"] == "Interactions":
                impression_bottom = range_data["boundingPoly"]["vertices"][0]["y"]

        reach_data = ""
        impression_data = ""
        for range_data in discovery_data:
            center_y = int(0.5 * (range_data["boundingPoly"]["vertices"][0]["y"] +
                                  range_data["boundingPoly"]["vertices"][2]["y"]))

            if reach_top <= center_y <= reach_bottom:
                reach_data += range_data["description"] + " "
            if impression_top <= center_y <= impression_bottom:
                impression_data += range_data["description"] + ""

        discovery_dict["Reach"]["Start Date"] = reach_data[reach_data.rfind(".") + 1:reach_data.rfind("-")]
        discovery_dict["Reach"]["End Date"] = reach_data[reach_data.rfind("-") + 1:]
        discovery_dict["Impression"]["Start Date"] = \
            impression_data[impression_data.rfind(".") + 1:impression_data.rfind("-")]
        discovery_dict["Impression"]["End Date"] = reach_data[reach_data.rfind("-") + 1:]

        return discovery_dict

    except Exception as e:
        log_print(info_str=e)

        return discovery_dict


if __name__ == '__main__':
    get_discovery_info(json_data="", blog_width=0)
