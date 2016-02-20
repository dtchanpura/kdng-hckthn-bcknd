from flask_wtf import Form
from wtforms import StringField
from wtforms.validators import InputRequired

from flaskapp.constants import UIConstants


class IntroForm(Form):
    user_name = StringField(validators=[InputRequired(UIConstants.USERNAME_INVALID)])

    def validate_on_submit(self):
        rv = Form.validate(self)
        # LOG
        if not rv:
            return False
        users = User.query.filter(User.user_name == self.user_name.data).all()
        if len(users) == 0:
            flash(messages.ERROR_INVALID_LOGIN, 'danger')
            return False
        self.qr_data.data = users[0].qr_data
        return True
