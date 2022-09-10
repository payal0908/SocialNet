from django.contrib.auth.models import User
from django.dispatch import receiver
from .models import *
from django.db.models.signals import post_save, pre_delete


@receiver(post_save, sender=User)
def auto_create_appuser(sender, instance, created, **kwargs):
    """
    This function automatically creates an appuser object when a new user object is created in the User model.
    """
    # checks if the object has been created
    if created:
        appuser = AppUser.objects.create(user=instance)
        appuser.save()

@receiver(post_save, sender=FriendsRelationship)
def post_save_friends_add(sender, instance, created, **kwargs):
    """
    This function adds the users to the AppUser model's friends field when the friend relationship status is updated to 'accepted'
    """
    # extracting the users from the newly created instance
    user_receiver = instance.receiver
    user_sender = instance.sender
    

    if instance.status == 'accepted':
        # adding the user to the friends field
        user_sender.friends.add(user_receiver.user)
        user_receiver.friends.add(user_sender.user)
        user_sender.save()
        user_receiver.save()


@receiver(pre_delete, sender=FriendsRelationship)
def pre_delete_remove_from_friends(sender, instance, **kwargs):
    """
    This function removes the users from the AppUser friends field when the friend relationship has been deleted.
    """
    sender = instance.sender
    receiver = instance.receiver
    sender.friends.remove(receiver.user)
    receiver.friends.remove(sender.user)
    receiver.save()