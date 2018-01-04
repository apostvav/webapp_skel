#!/usr/bin/env python
import os
from webapp_skel import create_app, db
from webapp_skel.models import User, Article, Tag
from flask_migrate import Migrate
import click

app = create_app(os.getenv('WEBAPP_SKEL_ENV') or 'dev')
migrate = Migrate(app, db)

@app.shell_context_processor
def make_shell_context():
    return dict(app=app, db=db, User=User, Article=Article, Tag=Tag)

@app.cli.command()
def insert_data():
    admin = User(username="admin", email="admin@example.com", password="admin")
    db.session.add(admin)

    def add_article(title, article, tags):
        db.session.add(Article(title=title, article=article, user=admin, tags=tags))

    for name in ["testing", "staging", "dev"]:
        db.session.add(Tag(name=name))

    add_article("Test1", "This is my 1st test.", "testing,staging,dev")
    add_article("Test2", "This is my 2nd test.", "testing,staging,dev")
    add_article("Test3", "This is my 3rd test.", "testing,staging,dev")
    add_article("Test4", "This is my 4th test.", "testing,staging,dev")
    add_article("Test5", "This is my 5th test.", "testing,staging,dev")

    db.session.commit()

@app.cli.command()
@click.confirmation_option(help='Are you sure you want to delete the db?')
def dropdb():
    db.drop_all()
    print("Database deleted")

@app.cli.command()
@click.confirmation_option(help="Are you sure you want to truncate db tables?")
def emptydb():
    for table in reversed(db.metadata.sorted_tables):
        print("Truncate table: "+str(table))
        db.engine.execute(table.delete())
    db.session.commit()

