#!/usr/bin/env python
from webapp_skel import app, db
from webapp_skel.models import User
from flask_script import Manager, prompt_bool

manager = Manager(app)

@manager.command
def initdb():
    db.create_all()
    #db.session.add(User(username="admin", email="admin@example.com", password="admin"))
    db.session.add(User(username="tolis", email="tolis@example.com", password="tolis"))
    db.session.commit()
    print("Initialized database")

@manager.command
def dropdb():
    if prompt_bool("Are you sure you want to delete the database?"):
        db.drop_all()
        print("Database deleted")

if __name__ == '__main__':
    manager.run()
