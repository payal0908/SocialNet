from urllib import response
from django.dispatch import receiver
from django.test import TestCase, Client
from django.urls import reverse
from social.models import *
from django.contrib.auth.models import User
import json

class TestChatViews(TestCase):

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user('test', 'test@e.com', 'test@123')
        self.client.login(username='test', password='test@123')

    def tearDown(self):
        User.objects.all().delete()
        AppUser.objects.all().delete()
        StatusPost.objects.all().delete()
        FriendsRelationship.objects.all().delete()

    def test_chat_index_view(self):
        response = self.client.get(reverse('chat'))
        self.assertEquals(response.status_code, 200)

    def test_chat_room_view(self):
        response = self.client.get(reverse('room', kwargs={'room_name':'lobby'}))
        self.assertEquals(response.status_code, 200)
