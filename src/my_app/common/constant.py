# -*- coding: utf-8 -*-

class Constants(object):
    _state_mapping = {}

    @classmethod
    def get_desc(cls, name, default='unknown'):
        return cls._state_mapping.get(name, default)

    @classmethod
    def types(cls):
        return cls._state_mapping.keys()


class LoginState(Constants):
    STATE_OFFLINE = '0'
    STATE_ONLINE = '1'

    _state_mapping = {
        STATE_OFFLINE: u'离线',
        STATE_ONLINE: u'在线'
    }


class FileType(Constants):
    FILE_IMAGE = 1
    FILE_LABEL = 2
    FILE_AVATAR = 3

    _state_mapping = {
        FILE_IMAGE: u'图像文件',
        FILE_LABEL: u'标注文件',
        FILE_AVATAR: u'头像文件'
    }

FLASH_MESSAGES = {
    'wrong_password': u'密码错误',
    'cannot_unregister_root': u'你一个root用户删除个毛线啊',
    'cannot_edit_user': u'没有编辑该用户的权限',
    'user_not_exist': u'用户不存在',
    'register_pending': u'正在等待注册通过',
    'error_action': u'不能进行此操作',
    'username_or_password_error': u'用户名或密码错误',
    'no_units_to_allocate': u'没有可分配的任务',
    'no_such_job': u'项目不存在',
    'weak_password': u'密码太弱，请设置一个强密码确保账户和财产的安全',
    'need_activation': u'您的账户尚未激活，请到注册邮箱内查收激活邮件并激活！',
}