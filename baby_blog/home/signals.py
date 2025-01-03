from django.db.models.signals import post_save, post_delete
# from django.dispatch import receiver
from django.contrib.auth.models import User
from . models import Profile

# @receiver(post_save, sender = User)
def create_profile(sender, instance, created, *args, **kwargs):
    if created:
        Profile.objects.create(user = instance)

# @receiver(post_save, sender = User)
def delete_user(sender, instance, *args, **kwargs):
    instance.user.delete()

post_save.connect(create_profile, sender = User)
post_delete.connect(delete_user, sender = Profile)