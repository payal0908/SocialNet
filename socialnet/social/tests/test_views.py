from django.test import TestCase, Client
from django.urls import reverse
from social.models import *
from django.contrib.auth.models import User

class TestViews(TestCase):

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create(username='test', email='test@e.com')
        self.user.set_password('test@123!!')
        self.user.save()
        self.user2 = User.objects.create_user('test2', 'email', 'test2@123')

        # to login the dummy user created
        self.client.login(username='test', password='test@123!!')

    def tearDown(self):
        User.objects.all().delete()
        AppUser.objects.all().delete()
        StatusPost.objects.all().delete()
        FriendsRelationship.objects.all().delete()

    # tests if the user can register successfully
    def test_user_can_register(self):
        self.client.logout()
        user_data = {
            'username': 'test', 
            'email': 'test@email.com', 
            'password': 'django124@pass'
        }
        response = self.client.post('/accounts/signup/', data=user_data, format="json")
        self.assertEquals(response.status_code, 200)
    
    # testing if dummy user can successfully login
    def test_user_can_login(self):
        self.client.logout()
        user_data = {
            'username': self.user,
            'password': self.user.password
        }
        response = self.client.post('/accounts/login/', data=user_data, format="json")

        self.assertEquals(response.status_code, 200)


    # testing the StatusPostView 
    def test_posts_view_GET(self):
        response = self.client.get(reverse('posts'))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'social/posts.html')

    # testing the post method of StatusPostView
    def test_posts_view_POST(self):
        response = self.client.post(reverse('posts'), {
            'created_by': self.user,
            'content': 'test post',
        })
        self.assertEquals(response.status_code, 200)
        post = StatusPost.objects.get(created_by=self.user)
        self.assertEquals(StatusPost.objects.count(), 1)
        self.assertEquals(post.content, 'test post')

    # testing invalid data to StatusPostView
    def test_posts_view_POST_no_data(self):
        response = self.client.post(reverse('posts'))
        self.assertEquals(response.status_code, 200)
        self.assertEquals(StatusPost.objects.count(), 0)

    # Appuserview - user's home page
    def test_appuser_view_GET(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse('home', args=[1]))

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'social/appuser.html')

    # testing the edit home page view
    def test_appuser_edit_view_GET(self):
        response = self.client.get(reverse('home-edit', args=[1]))

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'social/appuser_edit.html')

    # testing AppuserListView
    def test_appusers_list_view_GET(self):
        response = self.client.get(reverse('appusers'))

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'social/appusers_list.html')

    # to test send request view works
    def test_send_request_view_POST(self):
        response = self.client.post(reverse('send-request'), data={'appuser_pk':2}, HTTP_REFERER=reverse('appusers'))
        user1 = AppUser.objects.get(user=self.user)
        user2 = AppUser.objects.get(user=self.user2)
        # makes sure that the status is of sent and the receiver is the second appuser
        self.assertEquals(response.status_code, 302)
        rel = FriendsRelationship.objects.get(sender=user1)
        status = rel.status
        receiver = rel.receiver
        self.assertEquals(receiver, user2)
        self.assertEquals(status, 'sent')

    # testing the remove friend view
    def test_remove_friend_view_POST(self):
        # gets 2 appusers creates rel and checks remove

        user1 = AppUser.objects.get(user=self.user)
        user2 = AppUser.objects.get(user=self.user2)

        rel = FriendsRelationship.objects.create(sender=user1, receiver=user2, status='accepted')

        response = self.client.post(reverse('remove-friend'), data={'appuser_pk':2}, HTTP_REFERER=reverse('appusers'))

        self.assertEquals(response.status_code, 302)
        self.assertEquals(user1.get_friends().count(), 0)

    # testing if accept friend request works
    def test_accept_request_view_POST(self):

        user1 = AppUser.objects.get(user=self.user)
        user2 = AppUser.objects.get(user=self.user2)

        rel = FriendsRelationship.objects.create(sender=user2, receiver=user1, status='sent')

        response = self.client.post(reverse('accept-request'), data={'appuser_pk':2})

        self.assertEquals(response.status_code, 302)
        self.assertEquals(FriendsRelationship.objects.get(sender=user2).status, 'accepted')

    # testing to remove friend
    def test_reject_request_view_POST(self):
        user1 = AppUser.objects.get(user=self.user)
        user2 = AppUser.objects.get(user=self.user2)

        rel = FriendsRelationship.objects.create(sender=user2, receiver=user1, status='sent')

        response = self.client.post(reverse('reject-request'), data={'appuser_pk':2})

        self.assertEquals(response.status_code, 302)
        self.assertEquals(FriendsRelationship.objects.count(), 0)

    # testing to search appusers
    def test_appuser_search_view_GET(self):
        response = self.client.get('/social/search/?query=tes')

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'social/search.html')

    # testing to retrieve all appusers
    def test_appuser_request_view_GET(self):
        response = self.client.get(reverse('requests'))
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'social/requests.html')
    
    