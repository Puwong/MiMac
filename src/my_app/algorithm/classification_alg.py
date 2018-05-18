import os
import numpy as np
from flask import g
from keras.applications.vgg16 import VGG16
from keras.models import Model
from keras.layers import Dense, GlobalAveragePooling2D
from keras.models import model_from_json
from keras.preprocessing import image
from keras.applications.vgg16 import preprocess_input
from .base_alg import BaseAlg
from my_app.common.constant import ImageAlgorithm, ImageState
from my_app.foundation import db


class BiClassAlg(BaseAlg):

    def __init__(self, img):
        super(BiClassAlg, self).__init__(img)
        self.type1 = 'type1'
        self.type2 = 'type2'
        self.model_weight = os.path.join(self.alg_dir, 'b_c_basic.h5')
        self.model = os.path.join(self.alg_dir, 'b_c_basic.json')
        self.train_data_dir = ''

    def create(self, save=True):
        from my_app.common.tools import get_label_path, json2file
        info = {
            'alg': ImageAlgorithm.BiClass,
            'data': {
                'key': {
                    0: self.type1,
                    1: self.type2,
                },
                'value': 0,
            }
        }
        json2file(info, get_label_path(g.user_id, self.image.id))

    def edit(self, value):
        from my_app.common.tools import file2json, json2file
        label = file2json(self.image.uri + '.label')
        label['data']['value'] = int(value)
        json2file(label, self.image.uri + '.label')
        self.image.state = ImageState.DONE_LABEL
        db.session.commit()

    def train_dir_prepare(self):
        pass

    def train(self):
        img_width, img_height = 224, 224
        train_data_dir = self.train_data_dir
        # validation_data_dir = 'data/validation'
        nb_train_samples = 2000
        # nb_validation_samples = 800
        epochs = 10
        batch_size = 16

        base_model = VGG16(weights='imagenet', include_top=False)

        x = base_model.output
        x = GlobalAveragePooling2D()(x)
        x = Dense(128, activation='relu')(x)
        predictions = Dense(1, activation='sigmoid')(x)
        model = Model(inputs=base_model.input, outputs=predictions)

        for layer in base_model.layers:
            layer.trainable = False

        model.compile(optimizer='rmsprop', loss='binary_crossentropy')

        train_datagen = image.ImageDataGenerator(rotation_range=20,
                                                 fill_mode='nearest',
                                                 horizontal_flip=True,
                                                 zoom_range=0.2)
        train_generator = train_datagen.flow_from_directory(
            train_data_dir,
            target_size=(img_width, img_height),
            batch_size=batch_size,
            class_mode='binary')

        model.fit_generator(
            train_generator,
            steps_per_epoch=nb_train_samples // batch_size,
            epochs=epochs)

        json_string = model.to_json()
        open(self.model, 'w').write(json_string)
        model.save_weights(self.model_weight)

    def predict(self):
        from my_app.common.tools import file2json, json2file
        model = model_from_json(open(self.model).read())
        model.load_weights(self.model_weight)

        img_path = self.image.uri
        img = image.load_img(img_path, target_size=(224, 224))
        x = image.img_to_array(img)
        x = np.expand_dims(x, axis=0)
        x = preprocess_input(x)

        pred = model.predict(x)
        label = file2json(self.image.uri + '.label')
        label['data']['value'] = round(pred[0][0])
        json2file(label, self.image.uri + '.label')
        self.image.state = ImageState.DONE_LABEL
        db.session.commit()
        return pred


class BiClassAlgCatDog(BiClassAlg):

    def __init__(self, img):
        super(BiClassAlgCatDog, self).__init__(img)
        self.type1 = 'cat'
        self.type2 = 'dog'
        self.model_weight = os.path.join(self.alg_dir, 'b_c_cat_dog.h5')


class MulClassAlg(BaseAlg):

    def __init__(self, img, class_cnt=10):
        super(MulClassAlg, self).__init__(img)
        self.key = ['type'+str(i+1) for i in range(class_cnt)]
        self.model_weight = 'm_c_basic.h5'

    def create(self, save=True):
        from my_app.common.tools import get_label_path, json2file
        info = {
            'alg': ImageAlgorithm.MulClass,
            'data': {
                'key': self.key,
                'weight': [0] * len(self.key),
                'value': 1
            }
        }
        json2file(info, get_label_path(g.user_id, self.image.id))

    def edit(self, label):
        pass

    def train(self):
        pass

    def predict(self):
        pass

