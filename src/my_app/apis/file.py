import os
from flask import Blueprint, request, render_template, current_app, redirect, url_for, flash
from flask_restful import Api, Resource
from werkzeug.utils import secure_filename
from my_app.foundation import csrf
from my_app.common.db_helper import allowed_file

file_bp = Blueprint('File', __name__)
csrf.exempt(file_bp)
file_api = Api(file_bp)


class FilesAPI(Resource):
    def get(self):
        return current_app.make_response(render_template(
            'upload.html',
        ))

    def post(self):
        print request.__dict__
        print request.files
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        print file
        # if user does not select file, browser also
        # submit a empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            print filename
            from my_app import app_conf
            file.save(os.path.join(app_conf('UPLOAD_FOLDER'), filename))
            return redirect(url_for('File.files'))


file_api.add_resource(
    FilesAPI,
    '/files',
    endpoint='files'
)




