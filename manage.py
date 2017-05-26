#!/usr/bin/env python
import os
from webapp_skel import create_app, db
from webapp_skel.models import User, Article, Tag
from flask_script import Manager, prompt_bool
from flask_migrate import Migrate, MigrateCommand

app = create_app(os.getenv('WEBAPP_SKEL_ENV') or 'dev')
manager = Manager(app)
migrate = Migrate(app, db)

manager.add_command('db', MigrateCommand)

@manager.command
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

    db.session.commit()

@manager.command
def dropdb():
    if prompt_bool("Are you sure you want to delete the database?"):
        db.drop_all()
        print("Database deleted")

if __name__ == '__main__':
    manager.run()
