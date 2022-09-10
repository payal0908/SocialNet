from django.urls import path
from . import views
from django.contrib.auth.decorators import login_required

urlpatterns = [
    path('', login_required(views.index) , name='chat'),
    path('<str:room_name>/', login_required(views.room), name='room'),
]