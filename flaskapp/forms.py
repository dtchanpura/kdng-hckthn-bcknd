from flask_wtf import Form
from wtforms import StringField
from wtforms.validators import InputRequired

from flaskapp.constants import UIConstants


class IntroForm(Form):
    user_name = StringField(validators=[InputRequired(UIConstants.USERNAME_INVALID)])

    def validate_on_submit(self):
        rv = Form.validate(self)
        # LOG
        return rv
