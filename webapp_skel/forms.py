from flask_wtf import Form
from wtforms.fields import StringField
from wtforms.validators import DataRequired

class ArticleForm(Form):
    title = StringField('title', validators=[DataRequired()])
    article = StringField('article', validators=[DataRequired()])
