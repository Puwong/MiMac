#! encoding=utf-8
from flask_wtf import Form
from wtforms import StringField, BooleanField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Optional, Regexp
import re

class LoginForm(Form):
    username = StringField(u'用户名', validators = [DataRequired()])
    password = PasswordField(u'密码', validators = [DataRequired()])
    token = PasswordField(u'动态密码', validators = 
            [Optional(), Regexp(re.compile(r'\d{6}'))])
    remember_me = BooleanField(u'记住我', default = False)
    submit = SubmitField(u'登录')
