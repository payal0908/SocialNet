from urllib import request
from django.dispatch import receiver
from django.contrib.auth.validators import UnicodeUsernameValidator
from rest_framework import serializers
from .models import *
from django.contrib.auth.models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username']

        extra_kwargs = {
            'username': {
                'validators': [UnicodeUsernameValidator()],
            }
        }

class AppUserSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    friends = UserSerializer(many=True)
    class Meta:
        model = AppUser
        fields = ['user', 'name', 'email', 'display_img', 'friends']
        read_only_fields = ('friends','email')

    def to_representation(self, instance):
        self.fields['user'] = UserSerializer(read_only=True)
        return super(AppUserSerializer, self).to_representation(instance)

class AppUserListSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    class Meta:
        model = AppUser
        fields = ['user']

class PostSerializer(serializers.ModelSerializer):
    created_by = UserSerializer(read_only=False)
    image = serializers.ImageField(required=False)
    class Meta:
        model = StatusPost
        fields = ['content', 'image', 'created', 'created_by']

    def create(self, validated_data):
        created_by_data = validated_data.pop('created_by')
        username = created_by_data.pop('username')
        user = User.objects.get(username=username)
        post = StatusPost.objects.create(created_by=user, **validated_data)
        post.save()
        return post

class FriendsSerializer(serializers.ModelSerializer):
    sender = AppUserListSerializer()
    receiver = AppUserListSerializer()
    class Meta:
        model = FriendsRelationship
        fields = ['sender', 'receiver', 'status', 'updated']

class RequestSentSerializer(serializers.ModelSerializer):
    receiver = AppUserListSerializer()
    class Meta:
        model = FriendsRelationship
        fields = ['receiver', 'status']


class RequestReceivedSerializer(serializers.ModelSerializer):
    sender = AppUserListSerializer()
    class Meta:
        model = FriendsRelationship
        fields = ['sender', 'status']
