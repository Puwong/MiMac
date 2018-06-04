# -',- coding: utf-8 -*-

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

CHEAT_LIST = {
    3: {
        'g': [
            'CAOHUIJUN_2015-03-26_LCC_1.2.840.113681.2130706433.1427190117.5056.4841.dcm',
            'FANLIDONG_2015-07-07_LCC_1.2.840.113681.2071663199.1436168735.4320.2294.dcm',
            'FUJIE_2015-02-10_LCC_1.2.840.113681.2071663199.1423467792.5100.2650.dcm',
            'HONGSHUE_2015-09-28_RCC_1.2.840.113681.2071663199.1443425810.5116.83.dcm',
            'JIANGJING_2015-08-26_RCC_1.2.840.113681.2071663199.1440575329.5100.31.dcm',
            'JINHUA_2015-10-09_RCC_1.2.840.113681.2071663199.1444375996.5076.81.dcm',
            'JINXIAOYUN_2015-05-20_RCC_1.2.840.113681.2071663199.1431935071.4240.4492.dcm',
            'LINLIN_2015-05-25_RCC_1.2.840.113681.2071663199.1431935071.4240.7077.dcm',
            'LIUCHAN_2015-03-30_LCC_1.2.840.113681.2071663199.1427700169.4368.1346.dcm',
            'LIUNA_2015-04-16_RCC_1.2.840.113681.2071663199.1428910063.4348.5112.dcm'
        ],
        'b': [
            'GONGXIAOHONG_2015-09-06_RCC_1.2.840.113681.2071663199.1441525100.5116.124.dcm',
            'GOUYINGHUA_2015-09-25_RCC_1.2.840.113681.2071663199.1443168328.5092.33.dcm',
            'JIANGJIE_2015-06-25_RCC_1.2.840.113681.2071663199.1435045240.3680.2659.dcm',
            'LINXIN_2015-07-13_RCC_1.2.840.113681.2071663199.1436774447.5108.1767.dcm',
            'LIPING_2015-09-16_RCC_1.2.840.113681.2071663199.1442389550.5104.51.dcm',
            'LIUSHUHUA_2015-06-16_LCC_1.2.840.113681.2071663199.1434354156.5104.2268.dcm',
            'LUOSHIFANG_2015-08-10_LCC_1.2.840.113681.2130706433.1439193487.5024.1396.dcm',
            'LUOSHIFANG_2015-08-10_RCC_1.2.840.113681.2130706433.1439193487.5024.1346.dcm',
            'PANQI_2015-10-14_LCC_1.2.840.113681.2071663199.1444809051.4248.251.dcm',
            'PEIXINGMIN_2015-09-22_LCC_1.2.840.113681.2071663199.1442907938.4300.47.dcm'
        ]
    },
    2: {
        'g': [
            '000015.dcm',
            '000018.dcm',
            '000019.dcm',
            '000031.dcm',
            '000036.dcm',
            '000041.dcm',
            '000050.dcm',
            '000099.dcm',
            '000143.dcm',
        ],
        'b': [
            '000003.dcm',
            '000039.dcm',
            '000054.dcm',
            '000071.dcm',
            '000078.dcm',
            '000121.dcm',
            '000125.dcm',
            '000132.dcm',
        ]
    }
}

