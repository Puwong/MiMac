# -*- coding: utf-8 -*-
from .BaseService import BaseService
from my_app.algorithm import select_alg
from my_app.models import Image, User


class ImageService(BaseService):
    model = Image

    @staticmethod
    def create_label(image):
        select_alg(image)(image).create()

