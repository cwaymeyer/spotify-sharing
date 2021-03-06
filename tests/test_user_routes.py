import sys
sys.path.insert(0, '/home/caleb/capstones/spotify-sharing/tests')

from unittest import TestCase
from models import db, User, Group, UserGroup, Post
from app import app

app.config.from_object('config.TestingConfig')


class TestUserRoutes(TestCase):
    """Testing user routes."""

    def setUp(self):
        self.client = app.test_client()
        db.drop_all()
        db.create_all()

        # signup users
        new_user = User.user_signup(name='Test User', username='testuser', password='password')
        db.session.add(new_user)
        db.session.commit()

        new_user2 = User.user_signup(name='Test User Jr', username='testuserjr', password='passwordjr')
        db.session.add(new_user2)
        db.session.commit()

    def tearDown(self):
        db.session.rollback()
        return super().tearDown()


    def test_profile_content(self):
        """Test that profile page displays correct content."""

        with app.test_client() as client:
            with self.client:
                # login user 2
                client.post('/login', data={
                'username': 'testuserjr',
                'password': 'passwordjr'
                })

                # create test groups
                self.test_group = Group(name='Test Group', description='A group for testing', admin_id=1)
                db.session.add(self.test_group)
                db.session.commit()

                self.test_group = Group(name='Test Group 2', description='Another group for testing', admin_id=2)
                db.session.add(self.test_group)
                db.session.commit()

                user_group = UserGroup(user_id=2, group_id=1)
                db.session.add(user_group)
                db.session.commit()

                song_post = Post(user_id=2, group_id=1, content='Like this post', s_name='song_name', s_image='song_image', s_artist='song_artist', s_link='song_link', s_preview='song_preview')
                db.session.add(song_post)
                db.session.commit()

                resp = client.get('/user/2')
                html = resp.get_data(as_text=True)

                self.assertIn('<h1>Test User Jr</h1>', html)
                self.assertIn('<h3>@testuserjr</h3>', html)

                self.assertIn('<h3>Test Group 2</h3>', html)
                self.assertIn('<h3>Test Group</h3', html)
                self.assertIn('A group for testing', html)

                self.assertIn('<h2>Recent recommendations</h2>', html)
                self.assertIn('song_name', html)


    def test_edit_user(self):
        """Test editing user details works."""

        with app.test_client() as client:
            with self.client:
                # login user 2
                client.post('/login', data={
                'username': 'testuserjr',
                'password': 'passwordjr'
                })

                # follow_redirects=false
                resp = client.post('/user/2/edit', data = {'full_name': 'Test User III', 'username': 'testuserIII', 'introduction': 'Imma test user'})
                html = resp.get_data(as_text=True)

                self.assertEqual(resp.status_code, 302)

                # follow_redirects=true
                redirect_resp = client.post('/user/2/edit', data = {'full_name': 'Test User III', 'username': 'testuserIII', 'introduction': 'Imma test user'}, follow_redirects=True)
                html = redirect_resp.get_data(as_text=True)

                self.assertEqual(redirect_resp.status_code, 200)
                self.assertIn("Test User III", html)
                self.assertIn("testuserIII", html)
                self.assertIn("Imma test user", html)

                # check db
                user = User.query.filter_by(id=2).first()

                self.assertEqual(user.introduction, "Imma test user")


    def test_delete_user(self):
        """Test that deleting a user works."""

        with app.test_client() as client:
            with self.client:
                # login user 2
                client.post('/login', data={
                'username': 'testuserjr',
                'password': 'passwordjr'
                })

                # follow_redirects=true
                redirect_resp = client.delete('/user/2/delete', follow_redirects=True)
                html = redirect_resp.get_data(as_text=True)

                self.assertEqual(redirect_resp.status_code, 200)
                self.assertIn("Sign up", html)

                # check db
                user = User.query.filter_by(id=2).first()
                self.assertEqual(user, None)


    def test_create_new_group_route(self):
        """Test that new group is created."""

        with app.test_client() as client:
            with self.client:
                # login user 1
                client.post('/login', data={
                'username': 'testuser',
                'password': 'password'
                })

                # follow_redirects=false
                resp = client.post('/user/1/new-group', data={
                    'name': 'My Test Group',
                    'description': 'A very descriptive description.'
                })

                self.assertEqual(resp.status_code, 302)

                # follow_redirects=true
                redirect_resp = client.post('/user/1/new-group', data={
                    'name': 'My Test Group 2',
                    'description': 'Another very descriptive description.'
                    }, follow_redirects=True)
                html = redirect_resp.get_data(as_text=True)

                self.assertEqual(redirect_resp.status_code, 200)
                self.assertIn('Test User', html)