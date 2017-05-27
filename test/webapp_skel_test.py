from flask import url_for
from flask_testing import TestCase

import webapp_skel
from webapp_skel.models import User, Article

class TestWebapp(TestCase):
    def create_app(self):
        return webapp_skel.create_app('test')

    def setUp(self):
        self.db = webapp_skel.db
        self.db.create_all()
        self.client = self.app.test_client()

        testUser = User(username='test', email='test@example.com', password='test')
        testArticle = Article(user=testUser, title="My Test", article="My Test Text",
                              tags="test1,test2")
        self.db.session.add(testUser)
        self.db.session.add(testArticle)
        self.db.session.commit()

        self.client.post(url_for('auth.login'),
            data = dict(username='test', password='test'))

    def tearDown(self):
        webapp_skel.db.session.remove()
        webapp_skel.db.drop_all()

    def test_delete_all_tags(self):
        response = self.client.post(
            url_for('articles.edit', article_id=1),
            data = dict(
                title = "My test edited",
                article = "My Test Text edited",
                tags = ""
            ),
            follow_redirects = True
        )

        assert response.status_code == 200
        article1 = Article.query.first()
        assert not article1._tags
