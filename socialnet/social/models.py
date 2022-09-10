from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.core.validators import FileExtensionValidator


class StatusPost(models.Model):
    content = models.TextField()
    image = models.ImageField(upload_to='posts/', 
                                validators=[FileExtensionValidator(['png', 'jpg', 'jpeg'])],
                                blank=True, null=True)
    created = models.DateTimeField(default=timezone.now)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        ordering = ['-created']

class FriendsManager(models.Manager):

    def pending_requests(self, receiver):
        query = FriendsRelationship.objects.filter(receiver=receiver, status='sent')
        return query

    def requests_received(self, receiver):
        """
        Returns the requests recieved by the given user
        """
        query = FriendsRelationship.objects.filter(receiver=receiver, status='sent') | FriendsRelationship.objects.filter(receiver = receiver, status='accepted')
        return query
    
    def requests_sent(self, sender):
        """
        Returns the requests sent by the given user
        """
        query = FriendsRelationship.objects.filter(sender = sender, status='sent') | FriendsRelationship.objects.filter(sender = sender, status='accepted')
        return query

class AppUser(models.Model):
    # only one user with that username hence primary key is true
    user = models.OneToOneField(User, primary_key=True, related_name='appuser', on_delete=models.CASCADE)
    name = models.CharField(max_length=100, blank=True, null=True)
    email = models.EmailField(max_length=150, blank=True, null=True)
    bio = models.CharField(max_length=255, blank=True, null=True)
    display_img = models.ImageField(upload_to='userprofile/', default='userprofile/default_profile_img.png', blank=True)
    friends = models.ManyToManyField(User, blank=True, related_name='friends')

    # objects = AppUserManager()


    def __str__(self):
        return str(self.user)

    def get_friends(self):
        return self.friends.all()

    class Meta:
        ordering = ['user']


class FriendsRelationship(models.Model):
    sender = models.ForeignKey(AppUser, related_name='sender', on_delete=models.CASCADE)
    receiver = models.ForeignKey(AppUser, related_name='receiver', on_delete=models.CASCADE)
    updated = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=10, choices=(('sent', 'sent'), ('accepted', 'accepted')))

    objects = FriendsManager()
   

    def __str__(self):
        return str(self.sender)+":"+str(self.receiver)+":"+str(self.status)

    class Meta:
        ordering = ['id']