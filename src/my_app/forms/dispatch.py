#! encoding=utf-8
from flask_wtf import Form
from wtforms import SelectMultipleField, IntegerField
from wtforms.validators import DataRequired

class SettingForm(Form):
    number = IntegerField(u'TaskSet大小')
    worker = SelectMultipleField(u'分配人员', coerce=int)
    limit = IntegerField(u'标注重复次数', validators = [DataRequired(u'请输入重复次数')], default=1)
