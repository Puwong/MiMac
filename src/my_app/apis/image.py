from flask import Blueprint, request, render_template, current_app, flash, g, send_file, redirect, url_for
from flask_restful import Api, Resource
from werkzeug.utils import secure_filename
from my_app.foundation import csrf, db
from my_app.service import UserService, ImageService
from my_app.models import Image, ImageUserRelationship
from my_app.common.constant import ImageAlgorithm

image_bp = Blueprint('Image', __name__)
csrf.exempt(image_bp)
image_api = Api(image_bp)


def permission_check(image_id):
    iur = ImageUserRelationship.query.filter_by(user_id=g.user_id, image_id=image_id).all()
    image = ImageService(db).get(id)
    return len(iur) and not image.delete


class ImageShowAPI(Resource):

    def get(self, image_id):
        if not permission_check(image_id):
            return "Permission Deny !"
        image = ImageService(db).get(image_id)
        return send_file(image.uri, attachment_filename=image.title)


class ImageEditAPI(Resource):

    def get(self, action, image_id):
        if not permission_check(image_id):
            return "Permission Deny !"
        image = ImageService(db).get(image_id)
        if action == 'freeze':
            image.freeze = True
        elif action == 'unfreeze':
            image.freeze = False
        elif action == 'delete':
            image.delete = True
            return current_app.make_response(redirect(url_for('Image.images')))
        db.session.commit()
        if action == 'label':
            return current_app.make_response(render_template(
                'label.html',
                image=image
            ))
        else:
            return current_app.make_response(render_template(
                'image.html',
                image=image
            ))


class ImageAPI(Resource):

    def get(self, image_id):
        if not permission_check(image_id):
            return "Permission Deny !"
        image = ImageService(db).get(image_id)
        return current_app.make_response(render_template(
            'image.html',
            image=image
        ))

    def patch(self, image_id):
        pass


class ImagesAPI(Resource):
    def get(self):
        user = UserService(db).get(g.user_id)
        images = user.images
        return current_app.make_response(render_template(
            'images.html',
            images=images
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
            owner = UserService(db).get(g.user_id)
            fr = ImageUserRelationship(isOwner=True)
            fr.image = Image(title=secure_filename(file.filename), alg=request.form['imagealglist'])
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
    '/image/<int:image_id>',
    endpoint='image'
)
image_api.add_resource(
    ImagesAPI,
    '/image',
    endpoint='images'
)
image_api.add_resource(
    ImageShowAPI,
    '/image/show/<int:image_id>',
    endpoint='show'
)
image_api.add_resource(
    ImageUploadAPI,
    '/image/upload',
    endpoint='upload'
)
image_api.add_resource(
    ImageEditAPI,
    '/image/edit/<string:action>/<int:image_id>',
    endpoint='edit'
)

