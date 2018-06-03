# -*- coding: utf-8 -*-
from .BaseService import BaseService
from my_app.algorithm import select_alg
from my_app.models import Image, User


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

    def get_label_data(self, id_or_ins):
        from my_app.common.tools import file2json, json2file
        image = self.get(id_or_ins)
        return file2json(image.uri + '.label')
