from django.urls import path
from .views import *
from .api import *
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
url = '../accounts/login'

urlpatterns = [
    path('', login_required(login_url=url)(StatusPostsView.as_view()), name='posts'),
    path('home/<int:pk>', login_required(login_url=url)(AppuserView.as_view()), name='home'),
    path('home/edit/<int:pk>/', login_required(login_url=url)(AppuserEditView.as_view()), name='home-edit'),
    path('requests/', login_required(login_url=url)(RequestsView.as_view()), name='requests'),
    path('appusers/', login_required(login_url=url)(AppusersListView.as_view()), name='appusers'),
    path('send-invite/', login_required(login_url=url)(SendRequestView.as_view()), name='send-request'),
    path('remove-friend/', login_required(login_url=url)(RemoveFriendView.as_view()), name='remove-friend'),
    path('requests/accept/', login_required(login_url=url)(AcceptRequestView.as_view()), name='accept-request'),
    path('requests/reject', login_required(login_url=url)(RejectRequestView.as_view()), name='reject-request'),
    path('search/', login_required(login_url=url)(AppuserSearchView.as_view()), name='appuser-search'),
    path('api/appuser/<int:pk>',login_required(login_url=url)(AppuserDetail.as_view()), name='api-appuser-detail'),
    path('api/appusers', staff_member_required(login_url='admin:login')(AppusersList.as_view()), name='api-appusers-list'),
    path('api/posts/<int:pk>', login_required(login_url=url)(PostDetail.as_view()), name='api-post-detail'),
    path('api/friends/<int:pk>', login_required(login_url=url)(FriendsList.as_view()), name='api-friends-detail'),
    path('api/request-sent/<int:pk>', login_required(login_url=url)(RequestSentList.as_view()), name='api-request-sent'),
    path('api/request-received/<int:pk>', login_required(login_url=url)(RequestReceivedList.as_view()), name='api-request-received'),
]