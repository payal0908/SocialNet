from http import HTTPStatus
import json

from urllib import response 
from rest_framework import status

from django.urls import reverse
from rest_framework.test import APITestCase

from social.model_factories import *
from social.serializers import *

class SocialTest(APITestCase):

    def setUp(self):

        self.user1 = UserFactory()
        self.user2 = UserFactory(username="alex", password='newpass@123', is_superuser=False)
        self.user = User.objects.create(username='test', email='test@e.com')
        self.user.is_staff = True
        self.user.set_password('test@123!!')
        self.user.save()

        self.appuser1 = AppUserFactory()
        self.appuser2 = AppUserFactory(user=self.user2)

        self.post1 = StatusPostFactory.create(id=1, content="post1", created_by=self.user1)
        self.post2 = StatusPostFactory.create(id=2, content="post1", created_by=self.user2)

        self.friend = FriendsRelationshipFactory.create(sender=self.appuser1, receiver=self.appuser2, status='accepted')

        self.client.login(username='test', password='test@123!!')


    def tearDown(self):
        User.objects.all().delete()
        AppUser.objects.all().delete()
        StatusPost.objects.all().delete()
        FriendsRelationship.objects.all().delete()
        UserFactory.reset_sequence(0)
        StatusPostFactory.reset_sequence(0)
        FriendsRelationshipFactory.reset_sequence(0)

    def test_appuser_detail_return_success(self):
        url = reverse('api-appuser-detail', kwargs={'pk':1})
        
        response = self.client.get(url, format='json')
        self.assertEquals(response.status_code, 200)
        data = json.loads(response.content)
        self.assertEquals(data['user']['username'], 'john')

    def test_appuser_detail_return_fail(self):
        url = 'social/api/appuser/h'
        response = self.client.get(url, format='json')
        self.assertEquals(response.status_code, 404)

    def test_post_return_success_GET(self):
        url = reverse('api-post-detail', kwargs={'pk':1})
        response = self.client.get(url, format='json')
        self.assertEquals(response.status_code, 200)
        self.assertEquals(response.data['results'][0]['created_by']['username'], 'john')

    def test_post_return_fail_GET(self):
        url = 'social/api/post/a'
        response = self.client.get(url, format='json')
        self.assertEquals(response.status_code, status.HTTP_404_NOT_FOUND)
    
    def test_post_return_success_POST(self):
        url = reverse('api-post-detail', kwargs={'pk':1})
        data = {'content': 'test post api', 'created_by': self.user1}
        serializer = PostSerializer(data)
        response = self.client.post(url, data=serializer.data, format='json')
        self.assertEquals(response.status_code, status.HTTP_201_CREATED)
        self.assertEquals(StatusPost.objects.all().count(), 3)

    def test_post_return_fail_POST(self):
        url = reverse('api-post-detail', kwargs={'pk':1})
        data = {'content': '', 'created_by':self.user2}
        serializer = PostSerializer(data)
        response = self.client.post(url, data=serializer.data, format='json')
        self.assertEquals(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_friends_return_success(self):
        url = reverse('api-friends-detail', kwargs={'pk':1})
        response = self.client.get(url, format='json')
        self.assertEquals(response.status_code, 200)
        self.assertEquals(response.data['results'][0]['receiver']['user']['username'], 'alex')

    def test_friends_return_fail(self):
        url = 'social/api/friends/a'
        response = self.client.get(url, format='json')
        self.assertEquals(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_appusers_list_success(self):
        url = reverse('api-appusers-list')
        response = self.client.get(url, format='json')
        self.assertEquals(response.status_code, 200)
        # since count tells us the number returned
        self.assertEquals(response.data['count'], 3)