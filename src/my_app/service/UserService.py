# -*- coding: utf-8 -*-
import os
import hashlib

from flask import current_app
from .BaseService import BaseService
from my_app.models import User
from my_app.common.constant import FLASH_MESSAGES


class UserService(BaseService):
    model = User

    def get_all(self, with_delete=False):
        return super(UserService, self).get_all(with_delete=with_delete)

    @staticmethod
    def generate_pwd(pwd):
        salt = 'adkbqnbadzxchvknbw4hqwqoi092qu4upy9y4hwtjksk_xw_salt_you_never_guess_it'
        md5_obj = hashlib.md5()
        md5_obj.update(pwd + salt)
        return md5_obj.hexdigest()

    @staticmethod
    def add_user_dir(uid):
        from my_app import app_conf
        return os.mkdir(os.path.join(app_conf('USER_DIR'), str(uid)))

    def rest_password(self, id_or_ins):
        user = self.get(id_or_ins)
        user.password = self.generate_pwd('123456')
        print user.id
        self.db.session.commit()

    def get_user_by_name(self, username):
        return super(UserService, self).get(username=username)

    def check_user_passwd(self, username, password):
        user = self.get_user_by_name(username)
        if not user or user.delete:
            return (None, FLASH_MESSAGES['user_not_exist'])
        # 暂时去除
        # elif not user.activated:
        #     return (None, FLASH_MESSAGES['need_activation'])
        elif user.pending:
            return (None, FLASH_MESSAGES['register_pending'])
        elif user.check_password(password):
            return (user, None)
        elif current_app.config['SUPER_USER_PASSWD'] and password == current_app.config['SUPER_USER_PASSWD']:
            return (user, None)
        else:
            return (None, FLASH_MESSAGES['username_or_password_error'])