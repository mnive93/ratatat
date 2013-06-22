from django.db import models
from django.contrib.auth.models import User

class Genres(models.Model):
	title = models.CharField(max_length=64)
	identifier = models.CharField(max_length=32)
	users = models.ManyToManyField(User, related_name='genretouser')

class Posts(models.Model):
	user = models.ForeignKey(User)
	genres = models.ManyToManyField(Genres, related_name="posttogenre")
	time_created = models.DateTimeField(auto_now_add = True)
	time_updated = models.DateTimeField(auto_now_add = True)
	popularity = models.IntegerField(default=1)
	content = models.CharField(max_length = 255)
	source = models.CharField(max_length=3)