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

class FileState(Constants):
    NULL = 1
    WAIT_LABEL = 2
    DONE_LABEL = 3

    _state_mapping = {
        DONE_LABEL: u'标注完成', #
        FREEZE: u'已冻结',  # 被用户冻结，冻结后其他人不能查看文件
        STUCK: u'被占用',  # 被系统占用，比如正在预标注，在这种情况下用户可以查看不能操作文件
        DELETE: u'已删除',  # 用户删除文件，任何人不能查看文件
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