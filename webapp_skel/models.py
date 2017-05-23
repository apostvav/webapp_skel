from datetime import datetime
from sqlalchemy import desc
from flask_login import UserMixin
from werkzeug.security import check_password_hash, generate_password_hash
from webapp_skel import db

# Junction table for Articles and Tags
tags = db.Table('article_tag',
        db.Column('tag_id', db.Integer, db.ForeignKey('tag.id')),
        db.Column('article_id', db.Integer, db.ForeignKey('article.id'))
)

# Article
class Article(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(40), nullable=False)
    article = db.Column(db.Text, nullable=False)
    date = db.Column(db.DateTime, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    _tags = db.relationship('Tag', secondary=tags, backref=db.backref('articles', lazy='dynamic'))

    @staticmethod
    def newest(num):
        return Article.query.order_by(desc(Article.date)).limit(num)

    @property
    def tags(self):
        return ",".join([t.name for t in self._tags])

    @tags.setter
    def tags(self, string):
        if string:
            self._tags = [Tag.get_or_create(name) for name in string.split(',')]

    def __repr__(self):
        return "<Article '{}': '{}'>".format(self.title, self.article)

# User
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True)
    email = db.Column(db.String(40), unique=True)
    articles = db.relationship('Article', backref='user', lazy='dynamic')
    password_hash = db.Column(db.String)

    @property
    def password(self):
        raise AttributeError('password: write-only field')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    @staticmethod
    def get_by_username(username):
        return User.query.filter_by(username=username).first()

    def __repr__(self):
        return "<User '{}'>".format(self.username)

# Tag
class Tag(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False, unique=True, index=True)

    @staticmethod
    def get_or_create(name):
        try:
            return Tag.query.filter_by(name=name).one()
        except:
            return Tag(name=name)

    @staticmethod
    def all():
        return Tag.query.all()

    def __repr__(self):
        return self.name
