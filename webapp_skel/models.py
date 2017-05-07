from datetime import datetime
from sqlalchemy import desc
from webapp_skel import db

class Article(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(40), nullable=False)
    article = db.Column(db.Text, nullable=False)
    date = db.Column(db.DateTime, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    @staticmethod
    def newest(num):
        return Article.query.order_by(desc(Article.date)).limit(num)

    def __repr__(self):
        return "<Article '{}': '{}'>".format(self.title, self.article)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True)
    email = db.Column(db.String(40), unique=True)
    articles = db.relationship('Article', backref='user', lazy='dynamic')

    def __repr__(self):
        return '<User %r>' % self.username
