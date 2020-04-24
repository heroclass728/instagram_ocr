import glob
import os
import ntpath

from flask import Flask, render_template, request,send_file
from werkzeug.utils import secure_filename
from src.ocr.result import OCRExtractor
from utils.folder_file_manager import log_print
from settings import INPUT_IMG_DIR, CUR_DIR, LOCAL, WEB_SERVER, OUTPUT_DIR, SERVER_HOST, SERVER_PORT

app = Flask(__name__)
UPLOAD_DIR = '/tmp/'

ocr_extractor = OCRExtractor()


@app.route('/')
def upload():

    return render_template("file_upload_form.html")


@app.route('/upload', methods=['POST'])
def success():
    if request.method == 'POST':
        f = request.files['file']
        file_path = os.path.join(UPLOAD_DIR, secure_filename(f.filename))
        f.save(file_path)
        file_name_ext = ntpath.basename(file_path)
        file_name = file_name_ext[:file_name_ext.find(".")]
        saved_path = ocr_extractor.process_ocr_text(frame_path=file_path, file_name=file_name)
        saved_file_name = ntpath.basename(saved_path)
        log_print(info_str="Created {}".format(saved_path))

        return send_file(os.path.join(OUTPUT_DIR, saved_file_name), as_attachment=True)


def perform_ocr_in_local():

    image_paths = glob.glob(os.path.join(INPUT_IMG_DIR, "*.*"))
    for image_path in image_paths:
        file_name_ext = ntpath.basename(image_path)
        file_name = file_name_ext[:file_name_ext.find(".")]
        saved_path = ocr_extractor.process_ocr_text(frame_path=image_path, file_name=file_name)
        print("Successfully saved {}".format(saved_path))

    if not LOCAL:
        for tmp_path in glob.glob(os.path.join(CUR_DIR, "*.jpg")):
            os.remove(tmp_path)


if __name__ == '__main__':

    if WEB_SERVER:
        app.run(debug=True, host=SERVER_HOST, port=SERVER_PORT)
    else:
        perform_ocr_in_local()
