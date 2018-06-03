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
    STATE_OFFLINE = 0
    STATE_ONLINE = 1

    _state_mapping = {
        STATE_OFFLINE: u'离线',
        STATE_ONLINE: u'在线'
    }


class ImageState(Constants):
    NULL = 1
    WAIT_LABEL = 2
    LABELING = 3
    DONE_LABEL = 4

    _state_mapping = {
        NULL: u'其他',
        WAIT_LABEL: u'等待标注',
        LABELING: u'正在标注',
        DONE_LABEL: u'标注完成',
    }
    StateDict = _state_mapping


class MessageType(Constants):
    NORMAL = 1
    REPLY_NEEDED = 2
    YES_OR_NO = 3

    _state_mapping = {
        NORMAL: u'普通消息',
        REPLY_NEEDED: u'需要回复',
        YES_OR_NO: u'态度询问',
    }


class UserRole(Constants):
    ADMIN = 1
    NORMAL = 2

    _state_mapping = {
        ADMIN: u'系统管理员',
        NORMAL: u'普通用户',
    }


class BaseAlgorithm(Constants):
    Base = 0

    Classification = 1100
    BiClass = 1101

    Recognition = 1200

    Segmentation = 1300
    SemanticSegmentation = 1310
    InstanceSegmentation = 1320
    PanopticSegmentation = 1330

    Caption = 1400
    # 提示一下，添加算法的时候也要更新 algorithm 的 __init__.py
    _state_mapping = {
        Classification: u'图像分类',
        BiClass: u'是否题',
        Recognition: u'图像识别',
        SemanticSegmentation: u'语义分割',
        InstanceSegmentation: u'实例分割',
        PanopticSegmentation: u'全景分割',
        Caption: u'图像说明',
    }
    AlgDict = _state_mapping
    AlgList = sorted([{'code': key, 'desc': _state_mapping[key]} for key in _state_mapping], key=lambda x: x['code'])


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