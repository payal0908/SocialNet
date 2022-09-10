from django.shortcuts import render
from social.models import AppUser
from django.views.generic import TemplateView

# chat base page
def index(request):
    user = request.user
    return render(request, 'chat/index.html', {'user':user})

# chat room page
def room(request, room_name):
    user = request.user
    username = request.GET.get('username', 'Anonymous')
    return render(request, 'chat/room.html', {'room_name':room_name, 'username': username, 'user':user})