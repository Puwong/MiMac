# -*- coding: utf-8 -*-
import os
from my_app.algorithm import select_alg


class ImageService(object):
    @staticmethod
    def create_label(image):
        select_alg(image)(image).create()

