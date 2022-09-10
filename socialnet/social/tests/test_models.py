from django.test import TestCase
from social.models import *
from django.contrib.auth.models import User

class TestModels(TestCase):

    def setUp(self):
        self.User1 = User.objects.create_user('test1', 'test@e.com', 'test@123')
        self.User2 = User.objects.create_user('test2', 'test2@email.com', 'test2@123')
        
        self.appuser1 = AppUser.objects.get(user = self.User1)
        self.appuser2 = AppUser.objects.get(user = self.User2)

        self.relation1 = FriendsRelationship.objects.create(sender=self.appuser1, receiver=self.appuser2, status='accepted')

        self.post1 = StatusPost.objects.create(content='test post 1', created_by = self.User1)

    def tearDown(self):
        User.objects.all().delete()
        AppUser.objects.all().delete()
        StatusPost.objects.all().delete()
        FriendsRelationship.objects.all().delete()

    def test_appuser_on_user_creation(self):
        appuser1 = AppUser.objects.get(user=self.User1)
        self.assertEquals(appuser1.user, self.User1)

    def test_get_friends(self):
        friends = self.appuser1.get_friends()
        self.assertEquals(friends[0].username, self.appuser2.__str__())

    def test_pending_requests(self):
        rel = FriendsRelationship.objects.create(sender=self.appuser1, receiver=self.appuser2, status = 'sent')
        query  = FriendsRelationship.objects.pending_requests(self.appuser2)
        req = query.count()
        self.assertEquals(req, 1)
        self.assertEquals(query[0].status, 'sent')

    def test_requests_received(self):
        query = FriendsRelationship.objects.requests_received(self.appuser2)
        req = query.count()
        self.assertEquals(req, 1)
        self.assertEquals(query[0].status, 'accepted')

    def test_friends_model_str_return_success(self):
        str_val = self.relation1.__str__()
        self.assertEquals(str_val, 'test1:test2:accepted')

    def test_statuspost_count(self):
        query = StatusPost.objects.all()
        count = query.count()
        self.assertEquals(count, 1)
        self.assertEquals(query[0].content, 'test post 1')
    
