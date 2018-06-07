# -*- coding: utf-8 -*-
import os
import hashlib
from functools import wraps

from flask import current_app, g
from .BaseService import BaseService
from my_app.models import User
from my_app.common.constant import FLASH_MESSAGES, UserRole


def hack_alert(check):
    def hack_alert_inner(func):
        @wraps(func)
        def decorated_view(*args, **kwargs):
            if check(**kwargs) or UserService.i_am_admin():
                return func(*args, **kwargs)
            else:
                return "Please don't try to hack me"
        return decorated_view
    return hack_alert_inner


class UserService(BaseService):
    model = User

    def get_all(self, **kwargs):
        return super(UserService, self).get_all(delete=False, **kwargs)

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

    @staticmethod
    def i_am_admin():
        return User.query.get(g.user_id).role == UserRole.ADMIN

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
