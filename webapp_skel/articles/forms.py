from flask_wtf import FlaskForm
from wtforms.fields import StringField
from wtforms.validators import DataRequired, Regexp

from ..models import User


class ArticleForm(FlaskForm):
    title = StringField('title', validators=[DataRequired()])
    article = StringField('article', validators=[DataRequired()])
    tags = StringField('Tags', validators=[Regexp(r'^[a-zA-Z0-9, ]*$',
        message="Tags can only contain letters and numbers")])

    def validate(self):
        if not FlaskForm.validate(self):
            return False

        # filter out empty and dupliocate tag names
        stripped = [t.strip() for t in self.tags.data.split(',')]
        not_empty = [tag for tag in stripped if tag]
        tagset = set(not_empty)
        self.tags.data = ",".join(tagset)

        return True
