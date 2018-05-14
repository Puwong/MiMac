#! encoding=utf-8
from flask_wtf import Form
from wtforms import StringField, PasswordField, RadioField, BooleanField, SubmitField
from wtforms.validators import DataRequired, Optional, Length


class UserForm(Form):
    username = StringField(u'用户名', validators=[DataRequired(), Length(1, 20, 'input username')])
    password = PasswordField(u'密码', validators=[Optional()])
    reset_password = BooleanField(u'重置密码', default=False)
    role_admin = BooleanField(u'系统管理员', default=False)
    role_publisher = BooleanField(u'任务发布员', default=False)
    role_manager = BooleanField(u'任务管理员', default=False)
    role_checker = BooleanField(u'检查员', default=False)
    role_editor = BooleanField(u'标注员', default=False)
    submit = SubmitField('Submit')

    def init_with_user(self, user):
        if user:
            self.username.data = user.username
            self.password.data = ''
            self.reset_password.data = False
            self.role_admin.data = (user.role_admin == 1)
            self.role_publisher.data = (user.role_publisher == 1)
            self.role_manager.data = (user.role_manager == 1)
            self.role_checker.data = (user.role_checker == 1)
            self.role_editor.data = (user.role_editor == 1)

