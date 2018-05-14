#! encoding=utf-8
from flask_wtf import Form
from wtforms import PasswordField
from wtforms.validators import DataRequired, EqualTo

class PasswdForm(Form):
    oldpassword = PasswordField(u'旧密码', validators = [DataRequired()])
    newpassword = PasswordField(u'新密码', validators = [DataRequired()])
    confirm = PasswordField(u'再次输入密码', validators = [
        DataRequired(),
        EqualTo('newpassword', message=u'两次输入的密码不同'),
        ])

