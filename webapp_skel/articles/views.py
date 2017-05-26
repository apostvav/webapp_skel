from flask import render_template, url_for, request, redirect, flash
from flask_login import login_required, current_user

from . import articles
from .forms import ArticleForm
from .. import db
from ..models import User, Article, Tag


@articles.route('/add', methods=['GET', 'POST'])
@login_required
def add():
    form = ArticleForm()
    if form.validate_on_submit():
        title = form.title.data
        article = form.article.data
        tags = form.tags.data
        myarticle = Article(user=current_user, title=title, article=article, tags=tags)
        db.session.add(myarticle)
        db.session.commit()
        flash("Stored article '{}'".format(article))
        return redirect(url_for('main.index'))
    return render_template('article_form.html', form=form, title="Add Article")


@articles.route('/edit/<int:article_id>', methods=['GET', 'POST'])
@login_required
def edit(article_id):
    article = Article.query.get_or_404(article_id)
    if current_user != article.user:
        abort(403)
    form = ArticleForm(obj=article)
    if form.validate_on_submit():
        form.populate_obj(article)
        db.session.commit()
        flash("Stored article '{}'".format(article.title))
        return redirect(url_for('.user', username=current_user.username))
    return render_template('article_form.html', form=form, title="Edit Article")


@articles.route('/delete/<int:article_id>', methods=['GET', 'POST'])
@login_required
def delete(article_id):
    article = Article.query.get_or_404(article_id)
    if current_user != article.user:
        abort(403)
    if request.method == "POST":
        db.session.delete(article)
        db.session.commit()
        flash("Deleted '{}'".format(article.title))
        return redirect(url_for('.user', username=current_user.username))
    else:
        flash("Please confirm deleting the article.")
    return render_template('confirm_delete.html', article=article, nolinks=True)


@articles.route('/user/<username>')
def user(username):
    user = User.query.filter_by(username=username).first_or_404()
    return render_template('user.html', user=user)


@articles.route('/tag/<name>')
def tag(name):
    tag = Tag.query.filter_by(name=name).first_or_404()
    return render_template('tag.html', tag=tag)
