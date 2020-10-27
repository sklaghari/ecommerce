from django.db.models.signals import post_save
from .models import MyUser,Profile
from django.dispatch import receiver
@receiver(post_save,sender=MyUser)
def create_profile(sender,instance,created,**kwargs):
    if created:
        Profile.objects.create(user=instance)
@receiver(post_save,sender=MyUser)
def update_profile(sender,instance,created,**kwargs):
    if created==False:
        instance.profile.save()

