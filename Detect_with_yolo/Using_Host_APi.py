from flask import Flask, flash, request, redirect, url_for
from flask_restful import Resource, Api
from json import dumps

from werkzeug.utils import secure_filename

from  detect import  Detect_Shape_C
import  os

app = Flask(__name__)

ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

class Using_API :


    def __init__(self) -> None:

        super().__init__()

    @app.route('/Insert_image', methods=["POST"])
    def insert_image(self) :
            if 'file' not in request.files:
                flash('No file part')
                return redirect(request.url)
            file = request.files['file']
            # If the user does not select a file, the browser submits an
            # empty file without a filename.
            if file.filename == '':
                flash('No selected file')
                return redirect(request.url)
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                return redirect(url_for('download_file', name=filename))

    @app.route('/Get_RemoveBg' , methods = ["GET"])
    def get_image(self)  :
        pass

    @app.route('/get_real' , method = ["GET"])
    def get_border(self):
        pass

class Detect_shape(Resource) :
    object =  Detect_Shape_C()
    def __init__(self) -> None:
        super().__init__()


    def get(self):
        pass
class Coordinate(Resource) :
    def __init__(self) -> None:
        super().__init__()
    def get(self):
        pass







