from flask import Flask, render_template, url_for, request, redirect, flash, abort
from flask_login import login_required, login_user, logout_user, current_user
from webapp_skel import app, db, login_manager
from .forms import ArticleForm, LoginForm, SignupForm
from .models import User, Article, Tag

@login_manager.user_loader
def load_user(userid):
    return User.query.get(int(userid))

@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html', new_articles=Article.newest(5))

@app.route('/faq')
def faq():
    return render_template('faq.html')

@app.route('/add', methods=['GET', 'POST'])
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
        return redirect(url_for('index'))
    return render_template('article_form.html', form=form, title="Add Article")

@app.route('/edit/<int:article_id>', methods=['GET', 'POST'])
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
        return redirect(url_for('user', username=current_user.username))
    return render_template('article_form.html', form=form, title="Edit Article")

@app.route('/delete/<int:article_id>', methods=['GET', 'POST'])
@login_required
def delete(article_id):
    article = Article.query.get_or_404(article_id)
    if current_user != article.user:
        abort(403)
    if request.method == "POST":
        db.session.delete(article)
        db.session.commit()
        flash("Deleted '{}'".format(article.title))
        return redirect(url_for('user', username=current_user.username))
    else:
        flash("Please confirm deleting the article.")
    return render_template('confirm_delete.html', article=article, nolinks=True)

@app.route('/user/<username>')
def user(username):
    user = User.query.filter_by(username=username).first_or_404()
    return render_template('user.html', user=user)

@app.route('/login', methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.get_by_username(form.username.data)
        if user is not None and user.check_password(form.password.data):
            login_user(user, form.remember_me.data)
            flash("Logged in successfully as {}.".format(user.username))
            return redirect(request.args.get('next') or url_for('user', username=user.username))
        flash("Incorrect username or password.")
    return render_template("login.html", form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/signup', methods=["GET", "POST"])
def signup():
    form = SignupForm()
    if form.validate_on_submit():
        user = User(username=form.username.data,
                    password=form.password.data,
                    email=form.email.data)
        db.session.add(user)
        db.session.commit()
        flash('Welcome, {}! Please login'.format(user.username))
        return redirect(url_for('login'))
    return render_template("signup.html", form=form)

@app.route('/tag/<name>')
def tag(name):
    tag = Tag.query.filter_by(name=name).first_or_404()
    return render_template('tag.html', tag=tag)

@app.errorhandler(403)
def page_not_found(e):
    return render_template('403.html'), 403

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.errorhandler(500)
def server_error(e):
    return render_template('500.html'), 500

@app.context_processor
def inject_tags():
    return dict(all_tags=Tag.all)
