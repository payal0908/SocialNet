import django
import factory
from django.test import TestCase
from django.conf import settings
from django.core.files import File
from django.contrib.auth.models import User
from social.signals import post_save
import factory.fuzzy

from social.models import *

@factory.django.mute_signals(post_save)
class UserFactory(factory.django.DjangoModelFactory):

    class Meta:
        model = User
        django_get_or_create = ('username', )
    username = "john"
    password = 'pass@123!!'
    is_superuser = True
    

@factory.django.mute_signals(post_save)
class AppUserFactory(factory.django.DjangoModelFactory):

    class Meta:
        model = AppUser
        django_get_or_create = ('user', )

    user = factory.SubFactory(UserFactory)
    name = "John A"
    email = "john@email.com"

class StatusPostFactory(factory.django.DjangoModelFactory):
    content = "test post 2"
    created = "2022-02-17T08:35:18Z"
    created_by = factory.SubFactory(UserFactory)

    class Meta:
        model = StatusPost

class FriendsRelationshipFactory(factory.django.DjangoModelFactory):
    sender = factory.SubFactory(AppUserFactory)
    receiver = factory.SubFactory(AppUserFactory)
    status = "accepted"

    class Meta:
        model = FriendsRelationship