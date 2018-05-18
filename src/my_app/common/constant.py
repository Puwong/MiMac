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


class ImageAlgorithm(Constants):
    Base = 0
    BiClass = 1101
    BiClassCatDog = 1102
    MulClass = 1201
    # 提示一下，添加算法的时候也要更新 algorithm 的 __init__.py
    _state_mapping = {
        Base: u'基础算法',
        BiClass: u'二分类',
        BiClassCatDog: u'有猫病诊断',
        MulClass: u'多分类',
    }
    AlgDict = _state_mapping
    AlgList = [{'code': key, 'desc': _state_mapping[key]} for key in _state_mapping]


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