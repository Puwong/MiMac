# -*- coding: utf-8 -*-
import os
from shutil import copyfile
from .BaseService import BaseService
from my_app.algorithm import select_alg
from my_app.models import Image, User
from my_app.common.constant import ImageState, BaseAlgorithm


class ImageService(BaseService):
    model = Image

    @staticmethod
    def create_label(image):
        select_alg(image)(image).create()

    @staticmethod
    def label(image, label):
        select_alg(image)(image).edit(label)

    @staticmethod
    def algorithm(image):
        return select_alg(image)(image)

    def get_tiny_path(self, id_or_ins):
        image = self.get(id_or_ins)
        return image.uri + '.tiny.jpg'

    def create_tiny(self, id_or_ins):
        from my_app.common.tools import resize_img, convert_file
        image = self.get(id_or_ins)
        suffix = image.title.split('.')[-1]
        print image.title
        print image.store_uri, '\n',image.uri
        if suffix == 'dcm':
            convert_file(image.store_uri, image.uri)
            resize_img(image.uri, self.get_tiny_path(image))
            return True
        else :
            copyfile(image.store_uri, image.uri)
            resize_img(image.uri, self.get_tiny_path(image))
            return True

    def get_label_result(self, id_or_ins, with_desc=False, ignore_state=False):
        image = self.get(id_or_ins)
        data = self.get_label_data(image)
        if image.state == ImageState.DONE_LABEL or ignore_state:
            if image.alg.base == BaseAlgorithm.Caption:
                return data['data']['value']
            elif image.alg.base in (BaseAlgorithm.Classification, BaseAlgorithm.BiClass):
                if 'value' in data['data']:
                    value = data['data']['value']
                    if type(data['data']['key']) == list and value < len(data['data']['key']):
                        return data['data']['key'][value] if with_desc else value
        return '' if with_desc else None

    def get_label_data(self, id_or_ins):
        from my_app.common.tools import file2json, json2file
        image = self.get(id_or_ins)
        return file2json(image.uri + '.label')
