from rest_framework.test import APITestCase

from social.model_factories import *
from social.serializers import *
from django.core.files.uploadedfile import SimpleUploadedFile


class SerializerTest(APITestCase):

    # initializing
    appuserserializer = None
    userserializer = None
    postserializer = None
    friendsserializer = None
    appuserlistserializer = None

    def setUp(self):

        self.user1 = UserFactory()
        self.user2 = UserFactory(username="alex")
        self.appuser1 = AppUserFactory()
        self.appuser2 = AppUserFactory(user=self.user2)
        
        
        self.post1 = StatusPostFactory.create(id=1, content="post1", created_by=self.user1)
        self.post1.image = SimpleUploadedFile(name='test_image.jpg', content=open('/Users/payal/Downloads/base-img.jpg', 'rb').read(), content_type='image/jpeg')
        self.post2 = StatusPostFactory.create(id=2, content="post1", created_by=self.user2)
        self.friend = FriendsRelationshipFactory.create(sender=self.appuser1, receiver=self.appuser2, status='sent')

        self.userserializer = UserSerializer(instance=self.user1)
        self.appuserserializer = AppUserSerializer(instance=self.appuser1)
        self.postserializer = PostSerializer(instance=self.post1)
        self.friendsserializer = FriendsSerializer(instance=self.friend)

    def tearDown(self):
        User.objects.all().delete()
        AppUser.objects.all().delete()
        StatusPost.objects.all().delete()
        FriendsRelationship.objects.all().delete()
        UserFactory.reset_sequence(0)
        StatusPostFactory.reset_sequence(0)
        FriendsRelationshipFactory.reset_sequence(0)

    def test_user_serializer(self):
        data = self.userserializer.data
        self.assertEquals(data['username'], 'john')

    def test_appuser_serializer(self):
        data = self.appuserserializer.data
        self.assertEquals(data['name'], 'John A')

    def test_appuser_serializer_keys(self):
        data = self.appuserserializer.data
        self.assertEquals(data.keys(), set(['user', 'name', 'email', 'display_img', 'friends']))

    def test_post_serializer(self):
        data = self.postserializer.data
        self.assertEquals(data['content'], 'post1')
    
    def test_post_serializer_keys(self):
        data = self.postserializer.data
        self.assertEquals(data.keys(), set(['content', 'image', 'created', 'created_by']))

    def test_friends_serializer(self):
        data = self.friendsserializer.data
        self.assertEquals(data['sender']['user']['username'], 'john')

    def test_friends_serializer_keys(self):
        data = self.friendsserializer.data
        self.assertEquals(data.keys(), set(['sender', 'receiver', 'status', 'updated']))    
