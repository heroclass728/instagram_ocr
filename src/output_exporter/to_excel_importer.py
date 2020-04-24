import os
import pandas as pd
import openpyxl

from settings import OUTPUT_DIR, EXCEL_FIELDS


def import_info_into_excel(info, file_name):

    excel_path = os.path.join(OUTPUT_DIR, "{}.xlsx".format(file_name))
    wb = openpyxl.Workbook()
    wb.save(excel_path)
    writer = pd.ExcelWriter(excel_path, engine='openpyxl', mode='w')
    df = pd.DataFrame(columns=["Profile Visits", "Values"])
    df.to_excel(writer, sheet_name="sheet1", index=False)
    writer.save()
    writer.close()

    excel_data = []
    for info_key in info.keys():
        excel_data.append("")
        for sub_key in info[info_key].keys():
            excel_data.append(info[info_key][sub_key])
        if info_key == "Reach":
            excel_data.append("")

    excel_info = {"Profile Visits": EXCEL_FIELDS, "Values": excel_data}

    df = pd.DataFrame(excel_info, columns=["Profile Visits", "Values"])
    df.to_excel(excel_path, index=False, header=True)

    return excel_path


if __name__ == '__main__':

    import_info_into_excel(info={}, file_name="")
