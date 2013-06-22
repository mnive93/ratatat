from django.db import models
from django.contrib.auth.models import User

class SignupHandler(models.Model):
	emailaddress = models.EmailField(max_length=200)
	identifiernum = models.IntegerField()

class FacebookProfiles(models.Model):
    user = models.ForeignKey(User)
    fbk_id = models.IntegerField()
    fbk_token = models.CharField(max_length=200)

class TwitterProfiles(models.Model):
    user = models.ForeignKey(User)
    screen_name = models.CharField(max_length=64)
    oauth_token = models.CharField(max_length = 200)
    oauth_secret = models.CharField(max_length = 200)