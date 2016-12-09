#!coding=utf-8

# Create your models here.
from django.db import models
from django.contrib.auth import get_user_model
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings
from rest_framework.authtoken.models import Token

## If you want every user to have an automatically generated Token, you can simply catch the User's post_save signal.
## Actually, don't need it most of the times. May use it when we need token for a user after register (such as api access, we may need to send api to the user)
@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, USE_TZ=True,**kwargs):
    if created:
        Token.objects.create(user=instance)
