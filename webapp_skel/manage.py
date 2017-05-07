#!/usr/bin/env python
from webapp_skel import app, db
from flask_script import Manager, prompt_bool
from models import User

manager = Manager(app)

@manager.command
def initdb():
    db.create_all()
    db.session.add(User(username="tolis", email="tolis@example.com"))
    db.session.commit()
    print("Initialized database")

@manager.command
def dropdb():
    if prompt_bool("Are you sure you want to delete the database?"):
        db.drop_all()
        print("Database deleted")

if __name__ == '__main__':
    manager.run()
