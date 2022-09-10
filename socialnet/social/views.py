from urllib import request
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.db.models import Q
from .forms import NewStatusPostForm

from .models import *
from django.views import View
from django.views.generic import UpdateView, ListView
from .forms import *
from django.contrib.auth.mixins import UserPassesTestMixin


# View to display all posts

class StatusPostsView(View):
    def get(self, request, *args, **kwargs):

        # Filtering to retrieve posts created by user and user's friends

        posts = StatusPost.objects.filter(created_by__appuser__friends__in=
                                            [request.user.id]) | StatusPost.objects.filter(created_by=request.user)
        
        # to store unique posts only
        s = []
        for post in posts:
            if post in s:
                continue
            s.append(post)

        # creating new form 
        form = NewStatusPostForm()

        context = {
            'posts': s,
            'form': form, 
        }

        return render(request, 'social/posts.html', context)

    # post method for users to create new status posts
    def post(self, request, *args, **kwargs):
        status_posts = StatusPost.objects.all().order_by('-created')
        status_form = NewStatusPostForm(request.POST, request.FILES)
        if status_form.is_valid():
            new_status = status_form.save(commit=False)
            new_status.created_by = request.user
            new_status.save()
            # to clear form after submitting
            status_form = NewStatusPostForm()
        context = {
            'posts': status_posts,
            'form': status_form,
        }
        return render(request, 'social/posts.html', context)

# View to display user's home page
class AppuserView(View):
    def get(self, request, pk, *args, **kwargs):
        
        # retrieving user's appuser object and posts
        appuser = AppUser.objects.get(pk=pk)
        status_posts = StatusPost.objects.filter(created_by = appuser.user)

        context = {
            'appuser': appuser,
            'posts': status_posts
        }
        return render(request, 'social/appuser.html', context)

# View to edit user's home page
class AppuserEditView(UserPassesTestMixin, UpdateView):
    model = AppUser
    fields = ['name', 'email', 'bio', 'display_img']
    template_name = 'social/appuser_edit.html'
    
    def get_success_url(self):
        pk = self.kwargs['pk']
        return reverse_lazy('home', 
                            kwargs={'pk':pk})

    # to check if requesting user is the user whose view is being requested
    def test_func(self):
        appuser = self.get_object()
        bool = (self.request.user == appuser.user)
        return bool

# View to display all requests received
class RequestsView(View):
    def get(self, request, *args, **kwargs):
        appuser = AppUser.objects.get(user=request.user)
        query = FriendsRelationship.objects.pending_requests(appuser)

        # storing sender from the query
        res = []
        for obj in query:
            res.append(obj.sender)

        is_empty = False
        if len(res) == 0:
            is_empty = True
        
        context = {
            'query':res,
            'is_empty': is_empty,
        }   
        return render(request, 'social/requests.html', context)

# View to display all appusers
class AppusersListView(ListView):
    model = AppUser
    template_name = 'social/appusers_list.html'

    def get_queryset(self):
        query = AppUser.objects.all().exclude(user=self.request.user)
        return query
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        appuser = AppUser.objects.get(user = self.request.user)

        # retrieving all friends of user
        friend_r = FriendsRelationship.objects.filter(sender=appuser)
        friend_s = FriendsRelationship.objects.filter(receiver=appuser)

        friend_receiver = []
        friend_sender = []

        # storing all receivers and senders
        for friend in friend_r:
            friend_receiver.append(friend.receiver.user)
        for friend in friend_s:
            friend_sender.append(friend.sender.user)

        context['friend_receiver'] = friend_receiver
        context['friend_sender'] = friend_sender
        context['is_empty'] = False
        if len(self.get_queryset()) == 0:
            context['is_empty'] = True 
        return context

# To send a friend request
class SendRequestView(View):
    def post(self, request, *args, **kwargs):
        receiver_pk = request.POST.get('appuser_pk')
        curr_user = request.user
        sender = AppUser.objects.get(user=curr_user)
        receiver = AppUser.objects.get(pk=receiver_pk)

        # creating new friend relationship
        new_relation = FriendsRelationship.objects.create(sender=sender, receiver=receiver, status='sent')
        return redirect(request.META.get('HTTP_REFERER'))

# To accept a friend request
class AcceptRequestView(View):
    def post(self, request, *args, **kwargs):
        sender_pk = request.POST.get('appuser_pk')
        sender = AppUser.objects.get(pk = sender_pk)
        curr_user = AppUser.objects.get(user=request.user)
        new_relation = get_object_or_404(FriendsRelationship, sender=sender, receiver=curr_user)
        # changing status to accepted
        if new_relation.status == 'sent':
            new_relation.status = 'accepted'
            new_relation.save()
        return redirect('requests')

# declining friend request
class RejectRequestView(View):
    def post(self, request, *args, **kwargs):
        sender_pk = request.POST.get('appuser_pk')
        sender = AppUser.objects.get(pk=sender_pk)
        curr_user = AppUser.objects.get(user=request.user)

        # deleting the existing friend relationship
        updated_relation = get_object_or_404(FriendsRelationship, sender=sender, receiver=curr_user)
        updated_relation.delete()
        return redirect('requests')

# Removing a friend
class RemoveFriendView(View):
    def post(self, request, *args, **kwargs):
        receiver_pk = request.POST.get('appuser_pk')
        receiver = AppUser.objects.get(pk=receiver_pk)
        curr_user = request.user
        sender = AppUser.objects.get(user = curr_user)

        # retrieving the user to remove, who could be the sender or reciever when the request was sent
        updated_relation = FriendsRelationship.objects.get((Q(sender=sender) & Q(receiver=receiver)) 
                                                            | (Q(sender=receiver) & Q(receiver=sender)))
        # deleting that friend relationship
        updated_relation.delete()
        return redirect(request.META.get('HTTP_REFERER'))

# View to search for appusers
class AppuserSearchView(View):
    def get(self, request, *args, **kwargs):

        # retrieving the search input
        search_word = self.request.GET.get('query')
        appuser_list = AppUser.objects.filter(Q(user__username__icontains=search_word))
        appuser = AppUser.objects.get(user = request.user)
        
        friend_r = FriendsRelationship.objects.filter(sender=appuser)
        friend_s = FriendsRelationship.objects.filter(receiver=appuser)

        friend_receiver = []
        friend_sender = []

        for friend in friend_r:
            friend_receiver.append(friend.receiver.user)
        for friend in friend_s:
            friend_sender.append(friend.sender.user)

        empty = False
        if len(appuser_list) == 0:
            empty = True
        context = {
            'query': search_word,
            'appuser_list': appuser_list,
            'is_empty' : empty,
            'friend_receiver' : friend_receiver,
            'friend_sender' : friend_sender
        }

        return render(request, 'social/search.html', context)


