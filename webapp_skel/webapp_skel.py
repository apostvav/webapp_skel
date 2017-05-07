from flask import Flask, render_template, url_for, request, redirect, flash
#from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
import os
#from logging import DEBUG

basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
#app.logger.setLevel(DEBUG)
app.config['SECRET_KEY'] = b'\xb66\x0cv\xe9P\xb4\xf8\xb8\xc6\xbc\xdb\xbaaaG\xb1e<>X"\x7f\x9b'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'webapp_skel.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

from forms import ArticleForm
import models

# Fake logging
def logged_in_user():
    return models.User.query.filter_by(username='tolis').first()

'''articles = []
def store_article(article):
    articles.append(dict(
        title = title,
        article = article,
        user = 'Tolis',
        date = datetime.utcnow()
    ))'''

class User:
    def __init__(self, firstname, lastname):
        self.firstname = firstname
        self.lastname = lastname

@app.route('/')
@app.route('/index')
def index():
    #return "Hello World!"
    return render_template('index.html')
    #return render_template(index.html, new_articles=models.Article.newest(5))

@app.route('/faq')
def faq():
    return render_template('faq.html')

@app.route('/add', methods=['GET', 'POST'])
def add():
    form = ArticleForm()
    #if request.method == 'POST':
    if form.validate_on_submit():
        #article = request.form['article']
        title = form.title.data
        article = form.article.data
        #store_article(article)
        myarticle = models.Article(user=logged_in_user(), title=title, article=article)
        db.session.add(myarticle)
        db.session.commit()
        #app.logger.debug('stored article: ' + article)
        flash("Stored article '{}'".format(article))
        return redirect(url_for('index'))
    return render_template('add.html', form=form)

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.errorhandler(500)
def server_error(e):
    return render_template('500.html'), 500

#if __name__ == '__main__':
#    app.run(debug=True)
