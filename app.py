import glob
import os
import ntpath

from src.ocr.result import OCRExtractor
from settings import INPUT_IMG_DIR, CUR_DIR, LOCAL


if __name__ == '__main__':

    ocr_extractor = OCRExtractor()
    image_paths = glob.glob(os.path.join(INPUT_IMG_DIR, "*.*"))
    for image_path in image_paths:

        file_name_ext = ntpath.basename(image_path)
        file_name = file_name_ext[:file_name_ext.find(".")]
        saved_path = ocr_extractor.process_ocr_text(frame_path=image_path, file_name=file_name)
        print("Successfully saved {}".format(saved_path))

    if not LOCAL:
        for tmp_path in glob.glob(os.path.join(CUR_DIR, "*.jpg")):
            os.remove(tmp_path)
