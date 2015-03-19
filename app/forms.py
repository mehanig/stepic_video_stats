from flask.ext.wtf import Form
from wtforms import StringField, BooleanField, PasswordField
from wtforms.validators import DataRequired

# class LoginForm(Form):
#     openid = StringField('openid', validators=[DataRequired()])
#     remember_me = BooleanField('remember_me', default=False)


class LoginForm2Fields(Form):
    username = StringField('username', validators=[DataRequired()])
    password = PasswordField('password', validators=[DataRequired()])

    def validate(self):
        return True and super(Form, self).validate()