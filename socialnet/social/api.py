from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework import generics
from rest_framework import mixins
from rest_framework.parsers import JSONParser
from .models import *
from .serializers import *

# API for all posts created by user
class PostDetail(mixins.CreateModelMixin,
                 mixins.RetrieveModelMixin,
                 generics.ListAPIView):
    
    serializer_class = PostSerializer   

    def get_queryset(self):
        pk = self.kwargs['pk']
        queryset = StatusPost.objects.filter(created_by=pk)
        return queryset


    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)
    
    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)


# API for the user's info
class AppuserDetail(mixins.RetrieveModelMixin, generics.GenericAPIView):
    queryset = AppUser.objects.all()
    serializer_class = AppUserSerializer

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)
        

# API to list all appusers - only for admin user
class AppusersList(generics.ListAPIView):
    queryset = AppUser.objects.all()
    serializer_class = AppUserListSerializer

# API to display all user's friends
class FriendsList(mixins.RetrieveModelMixin, generics.ListAPIView):
    serializer_class = FriendsSerializer

    def get_queryset(self):
        pk = self.kwargs['pk']
        queryset = FriendsRelationship.objects.filter(
            sender=pk, status='accepted')| FriendsRelationship.objects.filter(receiver=pk, status='accepted')
        return queryset

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

# API to display requests sent by a user
class RequestSentList(mixins.RetrieveModelMixin, generics.ListAPIView):
    serializer_class = RequestSentSerializer

    def get_queryset(self):
        pk = self.kwargs['pk']
        queryset = FriendsRelationship.objects.requests_sent(sender=pk)
        return queryset

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

# API to display requests received by a user
class RequestReceivedList(mixins.RetrieveModelMixin, generics.ListAPIView):
    serializer_class = RequestReceivedSerializer

    def get_queryset(self):
        pk = self.kwargs['pk']
        queryset = FriendsRelationship.objects.requests_received(receiver=pk)
        return queryset

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)
