# encoding=utf-8


class ErrorCode:
    ERROR_UNKNOWN = (1000, u'未知错误!')
    ERROR_INVALID_PARAM = (1001, u'参数错误!')
    ERROR_NOT_ALLOWED = (1002, u'没有访问权限!, 请返回主界面重新选择')
    ERROR_STILL_WORKING = (1003, u'该用户正在进行相关工作')
    ERROR_INVALID_TASK_TYPE = (1004, u'任务类型错误')
    ERROR_NUMBER_OUT_OF_RANGE = (1005, u'数字超出范围')
    ERROR_TOKEN_MAIL_SENT = (1006, u'验证邮件已发送')
    ERROR_CONFIRM_PWD = (1007, u'密码与确认密码不相同')
    ERROR_PWD = (1008, u'密码错误')
    ERROR_PWD_EQ_UNAME = (1009, u'密码不能与用户名相同')
    ERROR_PWD_WEAK = (1010, u'密码太弱，为了您的账号安全请设置强一点的密码')
    ERROR_DELETE_UNIQUE = (1011, u'该数据具有唯一性校验，不可被删除')
    ERROR_INVALID_APPROVE_PARAM = (1012, u'验收驳回数据，不能直接通过!')
    ERROR_ILLEGAL_NAME = (1013, u'非法用户名(只可以包含最大长度为64的数字，英文字母及_)')
    ERROR_DELETE_STREAM_UNIQUE = (1014, u'流式任务组已经使用该组，不可被删除(请先删除流式分配组关系)')
    ERROR_REJECTION_DENY = (1015, u'禁止驳回')
    ERROR_EMAIL_INVALID = (1016, u'邮箱地址错误')
    ERROR_INVALID_CODE = (1017, u'邀请码错误')

    ERROR_GROUP_EXISTS = (2000, u'群组名称已经被使用!')
    ERROR_GROUP_NOT_EXIST = (2001, u'群组不存在!')

    ERROR_INVALID_JOB = (3000, u'项目有误!')
    ERROR_INVALID_SUBJOB = (3001, u'不存在此子项目!')
    ERROR_INVALID_REVIEW_JOB = (3002, u'验收项目有误!')
    ERROR_INVALID_JOB_PRICE = (3003, u'项目单价或价格分配比例有误!')
    ERROR_INVALID_SAMPLE_JOB = (3004, u'项目有误!!')

    ERROR_FINISHED_SUBJOB = (3004, u'子项目已经完结!')
    ERROR_FINISHED_UNITS = (3005, u'unit已经被抢占完,下次手快点哦!')
    ERROR_INVALID_JOB_STATE = (3006, u'项目状态不符合')

    # manager
    ERROR_USER_NOT_EXIST = (4000, u'用户不存在!')
    ERROR_INVALID_OUTSOURCE_EMAIL = (4001, u'外包邮件有误!')

    # publisher
    ERROR_NOTHING_TO_REVIEW = (5000, u'当前子项目没有可供验收的任务!')
    ERROR_NOTHING_TO_REVIEW_AUTO = (5001, u'当前项目没有可对比的自动标注数据!')
    ERROR_REVIEW_MODIFY_UNIT = (5002, u'当前项目标注数据不允许被修改!')

    # frontend
    ERROR_DUPLICATE_USER_NAME = (6000, u'此用户名已被人使用!')
    ERROR_DUPLICATE_EMAIL = (6001, u'此邮箱已被人使用!')
    ERROR_DUPLICATE_ID_NUMBER = (6002, u'此身份证号已被人使用!')
    ERROR_DUPLICATE_ALIPAY = (6003, u'此支付宝账号已被人使用!')

    # DataStore/Network
    ERROR_DB_FAILED = (7000, u'数据提交失败!')
    ERROR_REDIS_FAILED = (7001, u'服务器缓存失败!')
    ERROR_MUTEX_FAILED = (7002, u'抢占资源失败')
    ERROR_NETWORK_FAILED = (7003, u'网络错误!')

    # editor/checker
    ERROR_NO_SUBJOB_SELECTED = (8000, u'请先选择一个子项目!')
    ERROR_TASKUNIT_NOT_EXIST = (8001, u'任务不存在!')
    ERROR_SUBJOB_ALL_DONE = (8002, u'没有您可以处理的任务!')
    ERROR_DATA_VALIDATION_FAIL = (8003, u'数据验证失败')
    ERROR_ACTION = (8004, u'错误操作')
