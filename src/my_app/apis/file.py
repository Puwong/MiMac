import os
from flask import Blueprint, request, render_template, current_app, redirect, url_for, flash, g
from flask_restful import Api, Resource
from werkzeug.utils import secure_filename
from my_app.foundation import csrf, db
from my_app.common.db_helper import allowed_file
from my_app.service import UserService
from my_app.models import File, FileUserRelationship

file_bp = Blueprint('File', __name__)
csrf.exempt(file_bp)
file_api = Api(file_bp)


class FilesAPI(Resource):
    def get(self):
        return current_app.make_response(render_template(
            'upload.html'
        ))

    def post(self):
        from my_app import app_conf
        if 'file' not in request.files:
            flash('No file part')
            return current_app.make_response(render_template(
                'upload.html',
                result='ERROR! file not found'
            ))
        file = request.files['file']
        # if user does not select file, browser also
        # submit a empty part without filename
        if file.filename == '':
            flash('No selected file')
            return current_app.make_response(render_template(
                'upload.html',
                result="ERROR! filename shouldn't be empty"
            ))
        if file and allowed_file(file.filename):
            owner = UserService().get(g.user_id)
            fr = FileUserRelationship(isOwner=True)
            fr.file = File(title=file.filename)
            owner.files.append(fr)
            db.session.add(owner)
            db.session.commit()
            file.save(os.path.join(app_conf('USER_DIR'), str(g.user_id), str(fr.file.id)))
            return current_app.make_response(render_template(
                'upload.html',
                result='Upload success'
            ))


file_api.add_resource(
    FilesAPI,
    '/files',
    endpoint='files'
)




