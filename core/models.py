from django.db import models
from django.contrib.auth.models import User

class Genres(models.Model):
	title = models.CharField(max_length=64)
	identifier = models.CharField(max_length=32)
	users = models.ManyToManyField(User, related_name='genretouser')