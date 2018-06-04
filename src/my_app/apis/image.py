from flask import Blueprint, request, render_template, current_app, g, send_file, redirect, url_for
from flask_restful import Api, Resource
from flask_login import login_required
from werkzeug.utils import secure_filename
from my_app.foundation import csrf, db
from my_app.service import UserService, ImageService, AlgService
from my_app.models import Image, ImageUserRelationship
from my_app.common.constant import BaseAlgorithm

image_bp = Blueprint('Image', __name__)
csrf.exempt(image_bp)
image_api = Api(image_bp)


def permission_check(image_id):
    iur = ImageUserRelationship.query.filter_by(user_id=g.user_id, image_id=image_id).all()
    image = ImageService(db).get(image_id)
    return len(iur) and not image.delete


class ImageShowAPI(Resource):
    @login_required
    def get(self, image_id):
        if not permission_check(image_id):
            return "Permission Deny !"
        image = ImageService(db).get(image_id)
        return send_file(image.uri, attachment_filename=image.title)


class ImageTinyAPI(Resource):
    @login_required
    def get(self, image_id):
        if not permission_check(image_id):
            return "Permission Deny !"
        image = ImageService(db).get(image_id)
        return send_file(ImageService(db).get_tiny_path(image), attachment_filename=image.title)


class ImageEditAPI(Resource):
    @login_required
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
            db.session.commit()
            return current_app.make_response(redirect(url_for('Image.images')))
        db.session.commit()
        if action == 'label':
            label = ImageService(db).get_label_data(image)
            return current_app.make_response(render_template(
                'image.html',
                result=ImageService(db).get_label_result(image, with_desc=True),
                image=image,
                action='label',
                base_alg=BaseAlgorithm,
                label_num=len(label['data']['key']) if 'key' in label['data'].keys() else 0,
                label=label
            ))
        elif action == 'rename':
            image_name = image.title.rsplit('.', 1)[0]
            image_suffix = image.title.rsplit('.', 1)[1]
            return current_app.make_response(render_template(
                'image.html',
                result=ImageService(db).get_label_result(image, with_desc=True),
                image=image,
                image_name=image_name,
                image_suffix=image_suffix,
                action='rename'
            ))
        else:
            return current_app.make_response(render_template(
                'image.html',
                result=ImageService(db).get_label_result(image, with_desc=True),
                image=image
            ))

    @login_required
    def post(self, action, image_id):
        image = ImageService(db).get(image_id)
        if action == 'rename':
            image.title = request.form['filename'] + '.' + image.title.rsplit('.', 1)[1]
            db.session.commit()
        elif action == 'label':
            ImageService(db).label(image, request.form['label'])
        return current_app.make_response(render_template(
            'image.html',
            result=ImageService(db).get_label_result(image, with_desc=True),
            image=image
        ))


class ImageAPI(Resource):
    @login_required
    def get(self, image_id):
        if not permission_check(image_id):
            return "Permission Deny !"
        image = ImageService(db).get(image_id)
        return current_app.make_response(render_template(
            'image.html',
            result=ImageService(db).get_label_result(image, with_desc=True),
            image=image
        ))


class ImagesAPI(Resource):

    @login_required
    def get(self):
        user = UserService(db).get(g.user_id)
        images = list()
        for i in user.images:
            if not i.image.delete:
                images.append((i.image, ImageService(db).get_label_result(i.image, with_desc=True)))
        images = sorted(images, key=lambda x: x[0].id, reverse=True)
        images = {i: images[i] for i in range(len(images))}
        return current_app.make_response(render_template(
            'images.html',
            images=images
        ))


class ImageUploadAPI(Resource):
    @login_required
    def get(self):
        return current_app.make_response(render_template(
            'upload.html',
            algs=AlgService(db).get_my_alg_ids(with_title=True)
        ))

    @login_required
    def post(self):
        from my_app.common.tools import get_user_file_path, allowed_file, resize_img
        from my_app.tasks import predict
        if not request.form.get('alg'):
            return current_app.make_response(render_template(
                'upload.html',
                result='ERROR! Please pick up at least one algorithm',
                algs=AlgService(db).get_my_alg_ids(with_title=True)
            ))
        if 'file' not in request.files:
            return current_app.make_response(render_template(
                'upload.html',
                result='ERROR! file not found',
                algs=AlgService(db).get_my_alg_ids(with_title=True)
            ))
        file = request.files['file']
        # if user does not select file, browser also
        # submit a empty part without filename
        if file.filename == '':
            return current_app.make_response(render_template(
                'upload.html',
                result="ERROR! filename shouldn't be empty",
                algs=AlgService(db).get_my_alg_ids(with_title=True)
            ))
        if file and allowed_file(file.filename):
            owner = UserService(db).get(g.user_id)
            fr = ImageUserRelationship(isOwner=True)
            fr.image = Image(title=secure_filename(file.filename), alg=AlgService(db).get(int(request.form.get('alg'))))
            owner.images.append(fr)
            db.session.add(owner)
            db.session.commit()
            fr.image.uri = get_user_file_path(fr.image.id)
            db.session.commit()
            file.save(fr.image.store_uri)
            ImageService(db).create_tiny(fr.image)
            ImageService.create_label(fr.image)
            predict(fr.image.id)
            return current_app.make_response(render_template(
                'upload.html',
                result='Upload success',
                algs=AlgService(db).get_my_alg_ids(with_title=True)
            ))
        else:
            return current_app.make_response(render_template(
                'upload.html',
                result="We only support dcm, dicm, png, jpg, jpeg, gif suffix now",
                algs=AlgService(db).get_my_alg_ids(with_title=True)
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
    ImageTinyAPI,
    '/image/tiny/<int:image_id>',
    endpoint='tiny'
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

