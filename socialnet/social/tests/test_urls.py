from django.test import SimpleTestCase
from django.urls import reverse, resolve
from social.views import *

def resolve_url(url):
    return resolve(url).func.view_class

class TestUrls(SimpleTestCase):

    def test_posts_url_resolves(self):
        url = reverse('posts')
        self.assertEquals(resolve_url(url), StatusPostsView)

    def test_home_url_resolves(self):
        url = reverse('home', args=[1])
        self.assertEquals(resolve_url(url), AppuserView)

    def test_home_edit_resolves(self):
        url = reverse('home-edit', args=[1])
        self.assertEquals(resolve_url(url), AppuserEditView)

    def test_requests_resolves(self):
        url = reverse('requests')
        self.assertEquals(resolve_url(url), RequestsView)
    
    def test_appusers_resolves(self):
        url = reverse('appusers')
        self.assertEquals(resolve_url(url), AppusersListView)

    def test_send_invite_resolves(self):
        url = reverse('send-request')
        self.assertEquals(resolve_url(url), SendRequestView)

    def test_remove_friend_resolves(self):
        url = reverse('remove-friend')
        self.assertEquals(resolve_url(url), RemoveFriendView)

    def test_accept_invite_resolves(self):
        url = reverse('accept-request')
        self.assertEquals(resolve_url(url), AcceptRequestView)

    def test_reject_invite_resolves(self):
        url = reverse('reject-request')
        self.assertEquals(resolve_url(url), RejectRequestView)

    def test_search_appuser_resolves(self):
        url = reverse('appuser-search')
        self.assertEquals(resolve_url(url), AppuserSearchView)