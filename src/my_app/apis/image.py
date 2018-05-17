from flask import Blueprint, request, render_template, current_app, flash, g
from flask_restful import Api, Resource
#from werkzeug.utils import secure_filename
from my_app.foundation import csrf, db
from my_app.service import UserService, ImageService
from my_app.models import Image, ImageUserRelationship
from my_app.common.constant import ImageAlgorithm

image_bp = Blueprint('Image', __name__)
csrf.exempt(image_bp)
image_api = Api(image_bp)


class ImageAPI(Resource):
    def patch(self):
        pass


class ImagesAPI(Resource):
    def get(self):
        return current_app.make_response(render_template(
            'images.html'
        ))


class ImageUploadAPI(Resource):
    def get(self):
        return current_app.make_response(render_template(
            'upload.html',
            algs=ImageAlgorithm.AlgList
        ))

    def post(self):
        from my_app.common.tools import get_user_file_path, allowed_file
        if 'file' not in request.files:
            flash('No file part')
            return current_app.make_response(render_template(
                'upload.html',
                result='ERROR! file not found',
                algs=ImageAlgorithm.AlgList
            ))
        print

        file = request.files['file']
        # if user does not select file, browser also
        # submit a empty part without filename
        if file.filename == '':
            flash('No selected file')
            return current_app.make_response(render_template(
                'upload.html',
                result="ERROR! filename shouldn't be empty",
                algs=ImageAlgorithm.AlgList
            ))
        if file and allowed_file(file.filename):
            owner = UserService().get(g.user_id)
            fr = ImageUserRelationship(isOwner=True)
            fr.image = Image(title=file.filename, alg=request.form['imagealglist'])
            owner.images.append(fr)
            db.session.add(owner)
            db.session.commit()
            fr.image.uri = get_user_file_path(fr.image.id)
            db.session.commit()
            file.save(fr.image.uri)
            ImageService.create_label(fr.image)
            return current_app.make_response(render_template(
                'upload.html',
                result='Upload success',
                algs=ImageAlgorithm.AlgList
            ))

image_api.add_resource(
    ImageAPI,
    '/image/<int:id>',
    endpoint='image'
)
image_api.add_resource(
    ImagesAPI,
    '/image',
    endpoint='images'
)
image_api.add_resource(
    ImageUploadAPI,
    '/image/upload',
    endpoint='upload'
)



